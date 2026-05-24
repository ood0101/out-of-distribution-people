#!/usr/bin/env python3
"""
build_outreach_state.py
=======================
Backfill/refresh data/outreach_state.json from people/*.html.

WHY THIS EXISTS
---------------
The dossiers are the source of truth for *research*. They're not a source of
truth for *outreach state* (have I emailed this person? did they reply?
when do I follow up?). This script crystallizes the dossier-derived facts
into a single JSON keyed by slug, and reserves a user-owned section for
outreach state that the script will never overwrite.

MERGE CONTRACT (read before adding fields)
------------------------------------------
Idempotent. Safe to re-run after editing dossiers OR after hand-editing state.

DERIVED fields (REGENERATED on every run from dossier HTML):
    name, tier, tier_label, category, tags, indian, delta,
    one_liner, signals, last_git_touch

USER-OWNED fields (PRESERVED across runs — never overwritten):
    status, last_contacted, next_action_date, response, notes

Status vocabulary:
    not-contacted | queued | contacted | replied | passed

Orphans (state entry whose dossier was renamed/deleted): kept with
_orphan: true and logged. Do not silently drop user notes.

Tiering policy:
    Only canonical tag spans count: <span class="tag ...">tier-N: ...</span>
    Untiered dossiers get tier=null, needs_triage=true. No auto-inference.

Usage:
    python3 data/build_outreach_state.py
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PEOPLE_DIR = REPO / "people"
STATE_FILE = REPO / "data" / "outreach_state.json"

DERIVED_KEYS = {
    "name", "tier", "tier_label", "category", "tags", "indian", "delta",
    "one_liner", "signals", "last_git_touch", "needs_triage",
    # Email + Gmail compose (added 2026-05-21).
    "emails", "email_primary", "email_primary_kind",
    "outreach_subject", "outreach_body_preview", "gmail_url",
    # Social handles (added 2026-05-22) — for channel-aware compose.
    "twitter_handle", "linkedin_slug", "github_handle",
}
USER_KEYS = {
    "status", "last_contacted", "next_action_date", "response", "notes",
    # Urgency / daily-queue fields (added 2026-05-21). Preserved across rebuilds.
    "urgency_decay_date", "urgency_reason", "channel", "next_action", "cluster",
    # Email override (added 2026-05-21). When set, beats derived email_primary.
    "email_override", "outreach_subject_override", "outreach_body_override",
}
DEFAULT_USER = {
    "status": "not-contacted",
    "last_contacted": None,
    "next_action_date": None,
    "response": None,
    "notes": "",
    # urgency_decay_date: ISO date when the "why now" window closes. None = open-ended.
    "urgency_decay_date": None,
    # urgency_reason: one-line "why this person right now". Free text.
    "urgency_reason": None,
    # channel: twitter | email | linkedin | warm-intro | meeting
    "channel": None,
    # next_action: short verb phrase ("send congrats DM ref Osiris")
    "next_action": None,
    # cluster: optional cluster tag (scalerl, hazy, architecture, diffusion, etc.)
    "cluster": None,
    # Email overrides. Set these to bypass auto-extracted values.
    "email_override": None,
    "outreach_subject_override": None,
    "outreach_body_override": None,
}

TAG_SPAN_RE = re.compile(r'<span\s+class="tag[^"]*"[^>]*>([^<]+)</span>', re.IGNORECASE)
TIER_RE = re.compile(r'^tier-(\d)\b(.*)$', re.IGNORECASE)
ONE_LINER_RE = re.compile(r'class="one-liner"[^>]*>\s*(?:<strong>)?([^<]+)', re.IGNORECASE)
H1_RE = re.compile(r'<h1>([^<]+)</h1>', re.IGNORECASE)

# Email extraction. Greedy email regex + mailto: capture.
EMAIL_RE = re.compile(r'\b([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\b')
MAILTO_RE = re.compile(r'mailto:([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', re.IGNORECASE)

# Social handle extraction from dossier links.
# Matches twitter.com/handle OR x.com/handle (not /messages, /home, /search, /i/, etc.).
TWITTER_RE = re.compile(
    r'https?://(?:www\.)?(?:twitter\.com|x\.com)/(?!messages|home|search|i/|intent|notifications|explore|share|hashtag)([A-Za-z0-9_]{1,15})\b',
    re.IGNORECASE,
)
# Matches linkedin.com/in/handle
LINKEDIN_RE = re.compile(
    r'https?://(?:www\.)?linkedin\.com/in/([A-Za-z0-9\-_%]+)/?',
    re.IGNORECASE,
)
# Matches github.com/handle (not /search, /orgs, /topics)
GITHUB_RE = re.compile(
    r'https?://(?:www\.)?github\.com/(?!search|orgs|topics|features|pricing|enterprise|login)([A-Za-z0-9\-_]+)(?:/|"|\b)',
    re.IGNORECASE,
)

# Outreach draft extraction. Looks for "Subject:" in any outreach section.
SUBJECT_RE = re.compile(r'Subject\s*:\s*([^\n<]+)', re.IGNORECASE)

# Personal email providers — high confidence personal.
PERSONAL_DOMAINS = {
    "gmail.com", "googlemail.com", "fastmail.com", "fastmail.fm",
    "protonmail.com", "proton.me", "pm.me", "outlook.com", "hotmail.com",
    "icloud.com", "me.com", "mac.com", "hey.com", "yahoo.com", "ymail.com",
    "duck.com", "tutanota.com", "tuta.io", "zoho.com",
}

# Academic TLDs / suffixes. Treated as "academic" not "personal" not "company".
ACADEMIC_SUFFIXES = (
    ".edu", ".ac.uk", ".ac.in", ".ac.jp", ".ac.kr", ".ac.il", ".ac.cn",
    ".edu.au", ".edu.cn", ".edu.sg", ".uni-tuebingen.de", "ethz.ch",
)


def classify_email(addr: str) -> str:
    """Return one of: 'personal' | 'academic' | 'company'."""
    domain = addr.split("@", 1)[-1].lower()
    if domain in PERSONAL_DOMAINS:
        return "personal"
    if any(domain.endswith(suf) for suf in ACADEMIC_SUFFIXES):
        return "academic"
    return "company"


def extract_emails(html: str) -> list[str]:
    """Extract all unique emails. Includes mailto: links + plain text."""
    found = set()
    for m in MAILTO_RE.findall(html):
        found.add(m.lower())
    for m in EMAIL_RE.findall(html):
        # Filter junk like "noreply@anthropic.com" from co-author tags
        if "noreply" in m.lower() or "example.com" in m.lower():
            continue
        found.add(m.lower())
    # Stable order: by classification then alphabetical, so primary picks are deterministic.
    return sorted(found, key=lambda a: (classify_email(a), a))


def pick_primary_email(emails: list[str], signals: dict) -> tuple[str | None, str | None]:
    """Pick the primary email + return (email, kind).

    Rules (per user spec):
      - Stealth signal present → prefer personal (then academic, then company)
      - Else if company email present → prefer company (then academic, then personal)
      - Else → academic first, then personal
    """
    if not emails:
        return None, None

    by_kind = {"personal": [], "academic": [], "company": []}
    for e in emails:
        by_kind[classify_email(e)].append(e)

    is_stealth = bool(
        signals.get("phrase_stealth")
        or signals.get("tag_stealth_founder")
    )

    if is_stealth:
        order = ["personal", "academic", "company"]
    else:
        # Default: prefer the most "current" email. Company > academic > personal.
        # Academic email implies still affiliated with university (could be active).
        order = ["company", "academic", "personal"]

    for kind in order:
        if by_kind[kind]:
            return by_kind[kind][0], kind
    return None, None


def extract_outreach_subject(html: str) -> str | None:
    """Find the first 'Subject: ...' line in the dossier."""
    m = SUBJECT_RE.search(html)
    if not m:
        return None
    return strip_html_entities(m.group(1).strip())


def extract_outreach_body(html: str) -> str | None:
    """Extract the body text of the first outreach email draft.

    Strategy: find 'Subject:' line, take everything from the line AFTER it
    until we hit a sign-off ('— Vansh', 'Vansh\\n', or end of the outreach section).
    Returns plain text (HTML stripped).
    """
    # Find the position of Subject:
    sm = SUBJECT_RE.search(html)
    if not sm:
        return None
    # Take a generous chunk after Subject (next ~3500 chars).
    after = html[sm.end():sm.end() + 3500]
    # Strip tags
    text = re.sub(r'<[^>]+>', '\n', after)
    text = strip_html_entities(text)
    # Collapse whitespace
    lines = [ln.strip() for ln in text.split("\n")]
    # Skip leading blank lines
    while lines and not lines[0]:
        lines.pop(0)
    # Stop at sign-off
    body_lines = []
    for ln in lines:
        # Sign-off detection (any of these on their own line)
        if ln.strip() in ("Vansh", "— Vansh", "-- Vansh", "Vansh."):
            body_lines.append(ln)
            break
        # Hard stop if we hit a new HTML section header that leaked through
        if ln.startswith("◆") and len(body_lines) > 5:
            break
        body_lines.append(ln)
    # Collapse internal blank-line runs to single
    out = []
    blank = False
    for ln in body_lines:
        if not ln:
            if not blank:
                out.append("")
            blank = True
        else:
            out.append(ln)
            blank = False
    body = "\n".join(out).strip()
    return body if body else None


def build_gmail_url(email: str | None, subject: str | None, body: str | None) -> str | None:
    """Construct Gmail compose URL. Returns None if no recipient email."""
    if not email:
        return None
    from urllib.parse import quote
    base = "https://mail.google.com/mail/?view=cm&fs=1&tf=1"
    parts = [f"to={quote(email)}"]
    if subject:
        parts.append(f"su={quote(subject)}")
    if body:
        # Gmail URL has length limits (~8KB safe). Truncate body if needed.
        if len(body) > 6000:
            body = body[:5900] + "\n\n[truncated — see full draft in dossier]"
        parts.append(f"body={quote(body)}")
    return base + "&" + "&".join(parts)

# Signal detection — kept tight and explicit. Each signal is a boolean.
# We deliberately use a small set of high-precision phrases over a large
# set of fuzzy ones. False positives here pollute the daily briefing.
SIGNAL_PATTERNS = {
    "tag_stealth_founder": lambda tags, text: "stealth-founder" in tags,
    "tag_founders": lambda tags, text: any(
        t in tags for t in ("founders", "founders (latent)", "founders (potential)")
    ),
    "phrase_stealth": lambda tags, text: bool(re.search(r'\bstealth\b', text, re.IGNORECASE)),
    "phrase_departed": lambda tags, text: bool(
        re.search(r'\b(departed|just left|recently left)\b', text, re.IGNORECASE)
    ),
    "phrase_raising": lambda tags, text: bool(
        re.search(r'\b(raising|fundraising|raised\s+(seed|pre-?seed|series))\b', text, re.IGNORECASE)
    ),
    "phrase_founded": lambda tags, text: bool(
        re.search(r'\b(co-?founded|founded\s+\w|founding\s+team)\b', text, re.IGNORECASE)
    ),
}


def strip_html_entities(s: str) -> str:
    """Cheap entity decode for the few we actually see in dossiers."""
    return (
        s.replace("&middot;", "·")
         .replace("&mdash;", "—")
         .replace("&ndash;", "–")
         .replace("&amp;", "&")
         .replace("&rsquo;", "'")
         .replace("&lsquo;", "'")
         .replace("&ldquo;", '"')
         .replace("&rdquo;", '"')
         .replace("&hellip;", "…")
         .replace("&#x27;", "'")
         .replace("&nbsp;", " ")
         .strip()
    )


def get_git_commit_time(file_path: Path) -> str | None:
    """Last commit time for this file as ISO-8601, or None if not in git history."""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI", "--", str(file_path.relative_to(REPO))],
            cwd=REPO, capture_output=True, text=True, check=True,
        )
        ts = result.stdout.strip()
        return ts or None
    except subprocess.CalledProcessError:
        return None


def parse_dossier(path: Path) -> dict:
    html = path.read_text(encoding="utf-8", errors="replace")

    tag_spans = [strip_html_entities(t) for t in TAG_SPAN_RE.findall(html)]

    # Tier from canonical tag spans only.
    tier = None
    tier_label = None
    for t in tag_spans:
        m = TIER_RE.match(t)
        if m:
            tier = int(m.group(1))
            tier_label = t
            break

    # Category: tier label hints at outreach target vs. network/investor node.
    label_lower = (tier_label or "").lower()
    if any(k in label_lower for k in ("investor", "co-investor", "deal source", "network hub")):
        category = "network"
    elif tier is not None:
        category = "outreach"
    else:
        category = None

    # Non-tier tags
    other_tags = [t for t in tag_spans if not TIER_RE.match(t)]

    indian = "indian" in other_tags
    delta = "delta" in other_tags

    one_liner_m = ONE_LINER_RE.search(html)
    one_liner = strip_html_entities(one_liner_m.group(1)) if one_liner_m else ""

    h1_m = H1_RE.search(html)
    name = strip_html_entities(h1_m.group(1)) if h1_m else path.stem.replace("-", " ").title()

    # Strip tags for signal scanning so we don't match attribute text.
    text_only = re.sub(r'<[^>]+>', ' ', html)
    signals = {key: bool(fn(other_tags, text_only)) for key, fn in SIGNAL_PATTERNS.items()}

    # Email + outreach extraction.
    emails = extract_emails(html)
    email_primary, email_primary_kind = pick_primary_email(emails, signals)
    outreach_subject = extract_outreach_subject(html)
    outreach_body = extract_outreach_body(html)
    # Preview = first 300 chars of body for index panel display.
    outreach_body_preview = (outreach_body[:300] + "…") if outreach_body and len(outreach_body) > 300 else outreach_body
    gmail_url = build_gmail_url(email_primary, outreach_subject, outreach_body)

    # Social handle extraction.
    twitter_matches = TWITTER_RE.findall(html)
    twitter_handle = twitter_matches[0].lower() if twitter_matches else None
    linkedin_matches = LINKEDIN_RE.findall(html)
    linkedin_slug = linkedin_matches[0].lower() if linkedin_matches else None
    github_matches = GITHUB_RE.findall(html)
    # Filter out obvious noise (project repos that just happen to be linked)
    github_handle = github_matches[0].lower() if github_matches else None

    return {
        "name": name,
        "tier": tier,
        "tier_label": tier_label,
        "category": category,
        "tags": other_tags,
        "indian": indian,
        "delta": delta,
        "one_liner": one_liner,
        "signals": signals,
        "last_git_touch": get_git_commit_time(path),
        "needs_triage": tier is None,
        # Email + Gmail compose
        "emails": emails,
        "email_primary": email_primary,
        "email_primary_kind": email_primary_kind,
        "outreach_subject": outreach_subject,
        "outreach_body_preview": outreach_body_preview,
        "gmail_url": gmail_url,
        # Social handles
        "twitter_handle": twitter_handle,
        "linkedin_slug": linkedin_slug,
        "github_handle": github_handle,
    }


def load_existing_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"version": 1, "last_built": None, "people": {}}


def merge(existing: dict, derived: dict, slug: str) -> dict:
    """Overwrite derived keys; preserve user keys; default user keys for new entries."""
    prior = existing.get(slug, {})
    out = {}
    out.update(derived)  # all derived keys
    # User-owned fields: keep prior values if present, else defaults.
    for k, default in DEFAULT_USER.items():
        out[k] = prior.get(k, default)
    # Clear any orphan flag that might have stuck from a prior run.
    out.pop("_orphan", None)
    return out


def main() -> int:
    dossiers = sorted(PEOPLE_DIR.glob("*.html"))
    if not dossiers:
        print(f"No dossiers found in {PEOPLE_DIR}", file=sys.stderr)
        return 1

    # Slug collision check (defensive — filesystem already prevents this).
    slugs = [p.stem for p in dossiers]
    dupes = {s for s in slugs if slugs.count(s) > 1}
    if dupes:
        print(f"FATAL: duplicate slugs detected: {dupes}", file=sys.stderr)
        return 1

    state = load_existing_state()
    prior_people = state.get("people", {})
    new_people = {}

    for path in dossiers:
        slug = path.stem
        derived = parse_dossier(path)
        new_people[slug] = merge(prior_people, derived, slug)

    # Orphans: entries in prior state whose dossier has disappeared.
    orphans = []
    for slug, entry in prior_people.items():
        if slug not in new_people:
            entry["_orphan"] = True
            new_people[slug] = entry
            orphans.append(slug)

    state["people"] = new_people
    state["last_built"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n")

    # -------- READOUT --------
    people = state["people"]
    by_tier = {0: [], 1: [], 2: [], 3: [], None: []}
    for slug, p in people.items():
        if p.get("_orphan"):
            continue
        by_tier[p["tier"]].append(slug)

    print(f"\nWrote {STATE_FILE.relative_to(REPO)}")
    print(f"  total dossiers: {len(dossiers)}")
    print(f"  tier 0 (active pursuit):   {len(by_tier[0])}")
    print(f"  tier 1 (high conviction):  {len(by_tier[1])}")
    print(f"  tier 2 (tracking):         {len(by_tier[2])}")
    print(f"  tier 3 (indexed):          {len(by_tier[3])}")
    print(f"  untiered (NEEDS TRIAGE):   {len(by_tier[None])}")
    if orphans:
        print(f"  orphans (dossier gone):    {len(orphans)} -> {orphans[:5]}{'...' if len(orphans) > 5 else ''}")

    # Top 10 outreach candidates: tier 0/1, category=outreach, not yet contacted,
    # ranked by git-freshness (most recently worked on first).
    candidates = [
        (slug, p) for slug, p in people.items()
        if not p.get("_orphan")
        and p["tier"] in (0, 1)
        and p.get("category") != "network"
        and p["status"] == "not-contacted"
    ]
    candidates.sort(key=lambda x: x[1].get("last_git_touch") or "", reverse=True)

    print(f"\nTOP 10 OUTREACH CANDIDATES (tier 0/1, not yet contacted, freshest first):")
    for slug, p in candidates[:10]:
        tier_str = f"T{p['tier']}"
        flags = []
        if p["indian"]: flags.append("IN")
        if p["signals"]["tag_stealth_founder"] or p["signals"]["phrase_stealth"]: flags.append("stealth")
        if p["signals"]["phrase_departed"]: flags.append("departed")
        if p["signals"]["phrase_raising"]: flags.append("raising")
        flag_str = f" [{','.join(flags)}]" if flags else ""
        touch = (p.get("last_git_touch") or "")[:10]
        oneliner = (p["one_liner"] or "")[:80]
        print(f"  {tier_str} {touch} {p['name']:<28}{flag_str} — {oneliner}")

    # Untiered-but-has-departure-signal: the highest-priority triage bucket.
    untiered_hot = [
        (slug, p) for slug, p in people.items()
        if not p.get("_orphan")
        and p["tier"] is None
        and any(p["signals"][k] for k in ("tag_stealth_founder", "phrase_stealth", "phrase_departed", "phrase_raising"))
    ]
    untiered_hot.sort(key=lambda x: x[1].get("last_git_touch") or "", reverse=True)
    print(f"\nUNTIERED w/ founder/departure/raising signal — TRIAGE FIRST ({len(untiered_hot)}):")
    for slug, p in untiered_hot[:15]:
        touch = (p.get("last_git_touch") or "")[:10]
        sigs = [k.replace("phrase_", "").replace("tag_", "") for k, v in p["signals"].items() if v]
        oneliner = (p["one_liner"] or "")[:70]
        print(f"  {touch} {p['name']:<28} [{','.join(sigs)}] — {oneliner}")
    if len(untiered_hot) > 15:
        print(f"  ... and {len(untiered_hot) - 15} more")

    return 0


if __name__ == "__main__":
    sys.exit(main())
