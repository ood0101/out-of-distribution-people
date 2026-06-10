#!/usr/bin/env python3
"""
today.py
========
Daily outreach queue. Shows MAX 5 names you should reach out to today.

Designed for ADHD-friendly daily use:
  - Hard cap at 5 names. Not 20. Not "all T1." Five.
  - Each entry shows the WHY-NOW + the EXACT next action + the channel
  - One channel per session — sorted to surface them grouped
  - Stale entries (no urgency_reason set) drop to triage list at bottom

Usage:
    python3 scripts/today.py            # show daily queue
    python3 scripts/today.py --all      # show full ranked list (debugging)
    python3 scripts/today.py --triage   # show people needing urgency/action fields

Ranking:
    priority = tier_weight × 100  +  urgency_decay_proximity  +  cluster_boost
        tier_weight: T0=4, T1=3, T2=2, T3=1, None=0
        urgency_decay_proximity: 100 - days_until_decay (capped 0..100)
        cluster_boost: +20 if cluster moves recently (TODO)

Filters:
    - status != 'not-contacted' → drop (already in flight)
    - next_action_date > today → drop (snoozed)
    - missing urgency_reason → demote to triage section
"""
from __future__ import annotations
import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import quote

REPO = Path(__file__).resolve().parent.parent
STATE = REPO / "data" / "outreach_state.json"

MAX_DAILY = 5
TIER_WEIGHT = {0: 4, 1: 3, 2: 2, 3: 1, None: 0}

# Signal-events engine (dated/sourced/decaying inflection) — lazy singleton.
_INFLECTIONS: dict[str, float] | None = None


def inflection_for(slug: str) -> float:
    global _INFLECTIONS
    if _INFLECTIONS is None:
        try:
            sys.path.insert(0, str(REPO / "scripts"))
            from signals import all_inflections
            _INFLECTIONS = all_inflections()
        except Exception:
            _INFLECTIONS = {}
    return _INFLECTIONS.get(slug, 0.0)

# ───────────────────────────────────────────────────────────────────────
# COMPOSITE RANKING — what makes someone "best 5 today"
# ───────────────────────────────────────────────────────────────────────
# score = base(tier) + decay + signals + recency + indian + urgency + quality
#         + inflection
#
#   inflection (NEW)  dated, sourced, half-life-decayed events from
#                     data/signal_events.json (scripts/signals.py) —
#                     domain regs, departures, bio flips, filings.
#                     Clamped [-80, +120]. Negative events (round closed,
#                     joined a big lab) DRAG the score down. This is the
#                     "how NOW" axis the phrase-greps could never measure.
#
#   base(tier)       T0=400, T1=300, T2=200, T3=100, untiered=0
#   decay            100 - days_until_decay (max 100, only if decay set)
#   signals          stealth-founder=35, stealth=30, departed=30,
#                    raising=25, founded=15 (sum of detected signals)
#   recency          30 - days_since_dossier_update (max 30, decays in 30d)
#   indian           +10 if Indian-origin (sourcing thesis priority)
#   urgency          +30 if you've manually seeded urgency_reason
#   quality (NEW)    +20 at frontier lab (Anthropic/OpenAI/DeepMind/etc.)
#                    +15 part of a tracked cluster
#                    +20 dossier researched in last 7 days
#                    (caps at 55 — captures "high conviction without inflection")
#
# Tunable — edit these weights if the daily 5 doesn't match your gut.
# ───────────────────────────────────────────────────────────────────────

# Frontier companies — research-pedigree multiplier. Stays in sync with
# CLAUDE.md's "20 non-negotiable departure-tracking companies" + close peers.
FRONTIER_COMPANIES = {
    "anthropic", "openai", "deepmind", "google deepmind", "meta", "meta fair",
    "meta superintelligence", "xai", "mistral", "cursor", "anysphere",
    "runway", "midjourney", "character ai", "perplexity", "scale ai",
    "databricks", "mosaic", "together ai", "physical intelligence",
    "nvidia", "nvidia research", "tesla", "apple mlr", "anduril", "palantir",
    "cohere", "thinking machines", "cartesia", "luma", "genmo", "pika",
    "black forest labs", "bfl", "inflection", "reflection ai",
    "evolutionaryscale", "cz biohub", "arc institute", "ai21",
    "essential ai", "standard intelligence",
}

# ANSI for terminal readability
BOLD = "\033[1m"
DIM = "\033[2m"
RED = "\033[31m"
YELLOW = "\033[33m"
GREEN = "\033[32m"
CYAN = "\033[36m"
RESET = "\033[0m"


def today_iso() -> str:
    return date.today().isoformat()


def days_until(iso: str | None) -> int:
    if not iso:
        return 999
    try:
        return (date.fromisoformat(iso) - date.today()).days
    except ValueError:
        return 999


def days_since(iso: str | None) -> int:
    if not iso:
        return 9999
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return (datetime.now(timezone.utc) - dt).days
    except ValueError:
        return 9999


def at_frontier_company(entry: dict) -> bool:
    """Check if the entry mentions a frontier company in one_liner or tags."""
    ol = (entry.get("one_liner") or "").lower()
    tags = " ".join(entry.get("tags") or []).lower()
    haystack = ol + " " + tags
    return any(c in haystack for c in FRONTIER_COMPANIES)


def in_cluster(entry: dict) -> bool:
    """Has a cluster tag set (means part of a coherent cohort)."""
    return bool(entry.get("cluster"))


def score_components(entry: dict, slug: str | None = None) -> dict:
    """Return component breakdown for transparency. Sum = total score."""
    tier = entry.get("tier")
    base = TIER_WEIGHT.get(tier, 0) * 100

    decay_bonus = 0
    if entry.get("urgency_decay_date"):
        d = days_until(entry["urgency_decay_date"])
        # Window still open: closer = higher, capped 0..100.
        # Window CLOSED (d < 0): strip the urgency entirely — the "why now" is
        # over, so it must DROP, not climb. (Prior code had no ceiling, so a
        # past-due date inflated the bonus without limit — ranked higher forever.)
        decay_bonus = 0 if d < 0 else max(0, min(100, 100 - d))

    sigs = entry.get("signals") or {}
    signal_bonus = (
        (35 if sigs.get("tag_stealth_founder") else 0)
        + (30 if sigs.get("phrase_stealth") else 0)
        + (30 if sigs.get("phrase_departed") else 0)
        + (25 if sigs.get("phrase_raising") else 0)
        + (15 if sigs.get("phrase_founded") else 0)
    )

    git_days = days_since(entry.get("last_git_touch"))
    recency_bonus = max(0, 30 - git_days) if git_days < 30 else 0

    indian_bonus = 10 if entry.get("indian") else 0
    urgency_bonus = 30 if entry.get("urgency_reason") else 0

    # Quality bonus — captures "high conviction even without inflection signal".
    # Honors gut signal from curator + frontier lab employment + cohort membership.
    quality_bonus = 0
    if at_frontier_company(entry):
        quality_bonus += 20
    if in_cluster(entry):
        quality_bonus += 15
    if git_days <= 7:
        # Researched in last week = strong curator interest signal
        quality_bonus += 20

    # Inflection — dated/sourced/decaying events (signals.py). Clamped so one
    # hot week can't bury tier entirely, and negatives genuinely drag.
    inflect_bonus = 0
    if slug:
        inflect_bonus = int(round(max(-80.0, min(120.0, inflection_for(slug)))))

    total = (base + decay_bonus + signal_bonus + recency_bonus + indian_bonus
             + urgency_bonus + quality_bonus + inflect_bonus)
    return {
        "base": base,
        "decay": decay_bonus,
        "signal": signal_bonus,
        "recency": recency_bonus,
        "indian": indian_bonus,
        "urgency": urgency_bonus,
        "quality": quality_bonus,
        "inflect": inflect_bonus,
        "total": total,
    }


def priority(entry: dict, slug: str | None = None) -> int:
    return score_components(entry, slug)["total"]


def is_eligible(entry: dict) -> bool:
    if entry.get("status") != "not-contacted":
        return False
    next_dt = entry.get("next_action_date")
    if next_dt and next_dt > today_iso():
        return False
    # Only score T0/T1/T2 entries for the daily queue.
    # T3 and untiered fall out (they're indexed-for-future, not active outreach).
    tier = entry.get("tier")
    if tier not in (0, 1, 2):
        return False
    return True


def has_urgency(entry: dict) -> bool:
    return bool(entry.get("urgency_reason"))


def tier_badge(tier) -> str:
    if tier is None:
        return f"{DIM}[--]{RESET}"
    colors = {0: RED, 1: YELLOW, 2: CYAN, 3: DIM}
    return f"{colors.get(tier, '')}[T{tier}]{RESET}"


def resolve_email(e: dict) -> tuple[str | None, str | None]:
    """Return (email, kind). Uses override if set, else derived primary."""
    if e.get("email_override"):
        return e["email_override"], "override"
    return e.get("email_primary"), e.get("email_primary_kind")


def gmail_compose_url(email: str | None, subject: str | None, body: str | None) -> str | None:
    if not email:
        return None
    base = "https://mail.google.com/mail/?view=cm&fs=1&tf=1"
    parts = [f"to={quote(email)}"]
    if subject:
        parts.append(f"su={quote(subject)}")
    if body:
        if len(body) > 6000:
            body = body[:5900] + "\n\n[truncated — see full draft in dossier]"
        parts.append(f"body={quote(body)}")
    return base + "&" + "&".join(parts)


def channel_compose_links(slug: str, e: dict, subject: str | None, body: str | None) -> list[tuple[str, str]]:
    """Return list of (label, url) tuples appropriate for the chosen channel.

    For ADHD-friendly UX, prioritize the channel-of-record but show alternates.
    """
    channel = (e.get("channel") or "").lower()
    links: list[tuple[str, str]] = []

    # Resolve identifiers
    email, _kind = resolve_email(e)
    twitter = e.get("twitter_handle")
    linkedin = e.get("linkedin_slug")

    # Primary action by channel
    if channel == "twitter" and twitter:
        # Twitter "compose DM" intent — opens DM box if user has access, else profile
        links.append(("dm", f"https://twitter.com/messages/compose?recipient_screen_name={twitter}"))
        links.append(("profile", f"https://twitter.com/{twitter}"))
    elif channel == "linkedin" and linkedin:
        links.append(("profile", f"https://linkedin.com/in/{linkedin}/"))
    elif channel == "email" and email:
        url = gmail_compose_url(email, subject, body)
        if url:
            links.append(("gmail", url))
    elif channel == "warm-intro":
        # No direct compose — surface profile links so user can reach the warm-intro person
        if linkedin:
            links.append(("linkedin", f"https://linkedin.com/in/{linkedin}/"))
        if twitter:
            links.append(("twitter", f"https://twitter.com/{twitter}"))

    # Always show Gmail draft as a fallback if email is available
    if email and not any(label == "gmail" for label, _ in links):
        url = gmail_compose_url(email, subject, body)
        if url:
            links.append(("gmail-alt", url))

    return links


def render_row(slug: str, e: dict, i: int) -> str:
    name = e.get("name", slug)
    tier = e.get("tier")
    reason = e.get("urgency_reason") or "—"
    action = e.get("next_action") or "(no action set)"
    channel = e.get("channel") or "?"
    decay = e.get("urgency_decay_date")
    decay_str = f" {DIM}closes {decay} ({days_until(decay)}d){RESET}" if decay else ""
    cluster = e.get("cluster")
    cluster_str = f" {DIM}#{cluster}{RESET}" if cluster else ""

    # Subject + body (live, respects override).
    subject = e.get("outreach_subject_override") or e.get("outreach_subject")
    body = e.get("outreach_body_override")
    email, kind = resolve_email(e)

    # Identifier line: show what we have
    ident_parts = []
    if email:
        all_emails = e.get("emails") or []
        alts = [x for x in all_emails if x != email]
        alt_str = f" {DIM}(also: {', '.join(alts)}){RESET}" if alts else ""
        ident_parts.append(f"{CYAN}✉ {email}{RESET}{DIM}[{kind}]{RESET}{alt_str}")
    if e.get("twitter_handle"):
        ident_parts.append(f"{CYAN}𝕏 @{e['twitter_handle']}{RESET}")
    if e.get("linkedin_slug"):
        ident_parts.append(f"{CYAN}in/{e['linkedin_slug']}{RESET}")
    ident_line = "\n   " + "  ".join(ident_parts) if ident_parts else f"\n   {DIM}no contact info — mark.py {slug} email <addr>{RESET}"

    # Channel-appropriate compose links
    links = channel_compose_links(slug, e, subject, body)
    link_lines = []
    for label, url in links:
        icon = {"dm": "🐦", "profile": "👤", "gmail": "📧", "gmail-alt": "📧 alt", "twitter": "🐦", "linkedin": "💼"}.get(label, "🔗")
        link_lines.append(f"   {GREEN}{icon} {url}{RESET}")
    link_block = "\n" + "\n".join(link_lines) if link_lines else ""

    lines = [
        f"{BOLD}{i}. {tier_badge(tier)} {name}{RESET} {DIM}({slug}){RESET}{cluster_str}",
        f"   {DIM}WHY:{RESET} {reason}{decay_str}",
        f"   {GREEN}→ {channel}{RESET}  {action}{ident_line}{link_block}",
    ]
    return "\n".join(lines)


def main():
    args = sys.argv[1:]
    state = json.loads(STATE.read_text())
    people = state["people"]

    eligible = [(slug, e) for slug, e in people.items() if is_eligible(e)]
    ranked = sorted(eligible, key=lambda x: priority(x[1], x[0]), reverse=True)

    if "--all" in args:
        print(f"{BOLD}ALL ELIGIBLE — {len(ranked)} entries (T0/T1/T2 not-contacted){RESET}\n")
        print(f"{DIM}{'name':30s} {'base':4s} {'dcy':4s} {'sig':4s} {'rec':4s} {'in':3s} {'urg':4s} {'qua':4s} {'inf':4s} {'TOTAL':5s} seeded{RESET}")
        for i, (slug, e) in enumerate(ranked, 1):
            tier = e.get("tier")
            sc = score_components(e, slug)
            seeded = "✓" if e.get("urgency_reason") else ""
            name = (e.get("name") or slug)[:28]
            print(f"  {tier_badge(tier)} {name:30s} {sc['base']:4d} {sc['decay']:4d} {sc['signal']:4d} {sc['recency']:4d} {sc['indian']:3d} {sc['urgency']:4d} {sc['quality']:4d} {sc['inflect']:+4d} {BOLD}{sc['total']:5d}{RESET}  {seeded}")
        return

    if "--why" in args:
        # Detailed breakdown for the top 10 so you understand the ranking
        print(f"\n{BOLD}═══ RANKING BREAKDOWN — top 10 ═══{RESET}\n")
        print(f"{DIM}Formula: tier(400/300/200) + decay(max 100) + signals(max ~135) + recency(max 30) + indian(10) + urgency_seeded(30) + quality(max 55){RESET}\n")
        for i, (slug, e) in enumerate(ranked[:10], 1):
            sc = score_components(e, slug)
            tier = e.get("tier")
            name = e.get("name", slug)
            seeded = f" {GREEN}[SEEDED]{RESET}" if e.get("urgency_reason") else f" {DIM}[auto]{RESET}"
            print(f"{BOLD}{i:2d}. {tier_badge(tier)} {name}{RESET}{seeded} {DIM}({slug}){RESET}")
            print(f"    {sc['total']:>5d} total = "
                  f"{sc['base']} base"
                  + (f" + {sc['decay']} decay" if sc['decay'] else "")
                  + (f" + {sc['signal']} signals" if sc['signal'] else "")
                  + (f" + {sc['recency']} recency" if sc['recency'] else "")
                  + (f" + {sc['indian']} indian" if sc['indian'] else "")
                  + (f" + {sc['urgency']} urgency_seeded" if sc['urgency'] else "")
                  + (f" + {sc['quality']} quality" if sc['quality'] else "")
                  + (f" {GREEN if sc['inflect'] > 0 else RED}{sc['inflect']:+d} inflection{RESET}" if sc['inflect'] else ""))
            # Decompose signals
            sigs = e.get("signals") or {}
            sig_list = [k.replace("phrase_", "").replace("tag_", "") for k, v in sigs.items() if v]
            quality_parts = []
            if at_frontier_company(e):
                quality_parts.append("frontier-lab")
            if in_cluster(e):
                quality_parts.append(f"cluster={e.get('cluster')}")
            if days_since(e.get("last_git_touch")) <= 7:
                quality_parts.append("researched-this-week")
            qstr = f" · quality: {', '.join(quality_parts)}" if quality_parts else ""
            if sig_list or qstr:
                print(f"    {DIM}signals: {', '.join(sig_list) if sig_list else 'none'}{qstr}{RESET}")
            ol = (e.get("one_liner") or "")[:100]
            if ol:
                print(f"    {DIM}{ol}{RESET}")
            print()
        return

    if "--triage" in args:
        triage = [(s, e) for s, e in ranked if not has_urgency(e) and e.get("tier") in (0, 1)]
        print(f"{BOLD}TRIAGE — {len(triage)} tiered entries missing urgency_reason{RESET}")
        print(f"{DIM}Add urgency_reason / next_action / channel to scripts/seed_priorities.py{RESET}\n")
        for slug, e in triage[:30]:
            tier = e.get("tier")
            name = e.get("name", slug)
            ol = (e.get("one_liner") or "")[:90]
            sc = score_components(e, slug)
            print(f"  {tier_badge(tier)} {name:35s} score={sc['total']:3d}  {DIM}{ol}{RESET}")
        return

    # Default: daily 5 — ranked across ALL T0/T1/T2 not-contacted (not just seeded).
    # If you only want seeded entries, pass --seeded-only.
    if "--seeded-only" in args:
        candidates = [(s, e) for s, e in ranked if has_urgency(e)]
    else:
        candidates = ranked
    daily = candidates[:MAX_DAILY]
    alternates = candidates[MAX_DAILY:MAX_DAILY + 5]

    if not daily:
        print(f"{DIM}No actionable entries. Check status filters.{RESET}")
        return

    print(f"\n{BOLD}═══ TODAY'S OUTREACH — {today_iso()} ═══{RESET}")
    print(f"{DIM}{MAX_DAILY} max. Send these, then close the terminal.{RESET}")
    print(f"{DIM}Run with --why for ranking breakdown · --seeded-only to limit to curated{RESET}\n")

    for i, (slug, e) in enumerate(daily, 1):
        print(render_row(slug, e, i))
        print()

    # Show alternates (#6-#10) so you see what's just below the cut
    if alternates:
        print(f"{DIM}─ Alternates (next 5, in case you disagree) ─{RESET}")
        for i, (slug, e) in enumerate(alternates, MAX_DAILY + 1):
            tier = e.get("tier")
            name = e.get("name", slug)
            sc = score_components(e, slug)
            seeded_mark = " (seeded)" if e.get("urgency_reason") else ""
            print(f"  {i}. {tier_badge(tier)} {name:30s} {DIM}score={sc['total']:3d}{seeded_mark}{RESET}")
        print()

    # Footer summary
    total_pool = len(candidates)
    in_flight = sum(1 for e in people.values() if e.get("status") in ("queued", "contacted"))
    replied = sum(1 for e in people.values() if e.get("status") == "replied")
    print(f"{DIM}─" * 70 + RESET)
    print(f"{DIM}Pool: {total_pool} actionable · In flight: {in_flight} · Replied: {replied}{RESET}")
    print(f"{DIM}Mark sent: python3 scripts/mark.py <slug> sent{RESET}\n")


if __name__ == "__main__":
    main()
