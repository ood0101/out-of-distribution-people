#!/usr/bin/env python3
"""
build_outreach_view.py
======================
Inject auto-generated outreach panel into index.html.

Reads data/outreach_state.json. Generates HTML for the daily outreach queue.
Finds the marker block in index.html and replaces only the content between them:

    <!-- OUTREACH_QUEUE_START -->
    ... auto-generated panel ...
    <!-- OUTREACH_QUEUE_END -->

Idempotent. Re-run after editing dossiers + rebuilding state.

Panels:
    1. Reach out next — T0/T1 outreach, not-contacted, freshest first (top 8)
    2. Triage queue   — untiered with founder/departure/raising signals (top 12)
    3. In flight      — status ∈ {queued, contacted, replied}, if any
    4. Stats footer   — tier × category counts

Status badges:
    not-contacted -> no badge
    queued        -> "queued"
    contacted     -> grey strikethrough + "contacted DATE"
    replied       -> green "★ replied"
    passed        -> hidden from all panels

Usage:
    python3 data/build_outreach_view.py
"""
from __future__ import annotations

import html as html_mod
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
STATE_FILE = REPO / "data" / "outreach_state.json"
INDEX_FILE = REPO / "index.html"

START_MARKER = "<!-- OUTREACH_QUEUE_START -->"
END_MARKER = "<!-- OUTREACH_QUEUE_END -->"

# How many rows to render per panel. Tight by design — daily glanceability.
TOP_N_OUTREACH = 8
TOP_N_TRIAGE = 12


def esc(s: str | None) -> str:
    return html_mod.escape(s or "", quote=True)


def short_date(iso: str | None) -> str:
    if not iso:
        return "—"
    return iso[:10]


def signal_chips(p: dict) -> str:
    """Render a compact signal-flag strip for a person."""
    chips = []
    sigs = p.get("signals", {})
    if p.get("indian"):
        chips.append('<span class="ooq-chip ooq-chip-in">IN</span>')
    if sigs.get("tag_stealth_founder") or sigs.get("phrase_stealth"):
        chips.append('<span class="ooq-chip ooq-chip-stealth">stealth</span>')
    if sigs.get("phrase_departed"):
        chips.append('<span class="ooq-chip ooq-chip-departed">departed</span>')
    if sigs.get("phrase_raising"):
        chips.append('<span class="ooq-chip ooq-chip-raising">raising</span>')
    return "".join(chips)


def gmail_button(p: dict) -> str:
    """Render Gmail compose button if an email is available.

    Uses email_override → gmail_url. Falls back to a minimal compose URL
    if user has overridden the email but the derived gmail_url is stale.
    """
    from urllib.parse import quote
    # Resolve email + subject + body live (respects overrides)
    email = p.get("email_override") or p.get("email_primary")
    if not email:
        return '<a class="ooq-noemail" title="No email on file — add via mark.py">no email</a>'
    subject = p.get("outreach_subject_override") or p.get("outreach_subject") or ""
    body = p.get("outreach_body_override") or ""
    parts = [f"to={quote(email)}"]
    if subject:
        parts.append(f"su={quote(subject)}")
    if body:
        if len(body) > 6000:
            body = body[:5900] + "\n\n[truncated — see full draft in dossier]"
        parts.append(f"body={quote(body)}")
    url = "https://mail.google.com/mail/?view=cm&fs=1&tf=1&" + "&".join(parts)
    kind = p.get("email_primary_kind") or "?"
    if p.get("email_override"):
        kind = "override"
    return (
        f'<a class="ooq-gmail" href="{esc(url)}" target="_blank" rel="noopener" '
        f'title="{esc(email)} [{esc(kind)}]">&#9993; Gmail</a>'
    )


def truncate_at_word(text: str, max_chars: int) -> str:
    """Truncate at word boundary so we don't show 'CEO & Co-Founder,' cut mid-comma."""
    if not text or len(text) <= max_chars:
        return text
    # Cut at max_chars, then back up to last word boundary
    cut = text[:max_chars]
    # Strip trailing punctuation/whitespace common in mid-sentence cuts
    cut = cut.rstrip(",.;:—–- ")
    last_space = cut.rfind(" ")
    if last_space > max_chars * 0.5:
        cut = cut[:last_space]
    return cut.rstrip(",.;:—–- ") + "…"


def channel_links(p: dict) -> str:
    """Render channel-appropriate compose links inline.

    Browser equivalent of today.py's channel logic. Shows Gmail + Twitter +
    LinkedIn buttons inline based on what's available + the channel-of-record.
    """
    from urllib.parse import quote
    channel = (p.get("channel") or "").lower()
    twitter = p.get("twitter_handle")
    linkedin = p.get("linkedin_slug")
    email = p.get("email_override") or p.get("email_primary")
    subject = p.get("outreach_subject_override") or p.get("outreach_subject") or ""

    btns = []
    # Primary action by channel-of-record
    if channel == "twitter" and twitter:
        btns.append(f'<a class="ooq-btn ooq-btn-tw" href="https://twitter.com/messages/compose?recipient_screen_name={esc(twitter)}" target="_blank" rel="noopener" title="DM @{esc(twitter)}">𝕏 DM</a>')
    elif channel == "linkedin" and linkedin:
        btns.append(f'<a class="ooq-btn ooq-btn-li" href="https://linkedin.com/in/{esc(linkedin)}/" target="_blank" rel="noopener" title="LinkedIn">in</a>')
    elif channel == "email" and email:
        body = p.get("outreach_body_override") or ""
        parts = [f"to={quote(email)}"]
        if subject:
            parts.append(f"su={quote(subject)}")
        if body:
            if len(body) > 6000:
                body = body[:5900] + "\n\n[truncated]"
            parts.append(f"body={quote(body)}")
        url = "https://mail.google.com/mail/?view=cm&fs=1&tf=1&" + "&".join(parts)
        btns.append(f'<a class="ooq-btn ooq-btn-gm" href="{esc(url)}" target="_blank" rel="noopener" title="{esc(email)}">✉ Gmail</a>')

    # Always show Gmail if we have an email and it's not the primary
    if email and not any("Gmail" in b for b in btns):
        body = p.get("outreach_body_override") or ""
        parts = [f"to={quote(email)}"]
        if subject:
            parts.append(f"su={quote(subject)}")
        if body:
            if len(body) > 6000:
                body = body[:5900] + "\n\n[truncated]"
            parts.append(f"body={quote(body)}")
        url = "https://mail.google.com/mail/?view=cm&fs=1&tf=1&" + "&".join(parts)
        btns.append(f'<a class="ooq-btn ooq-btn-gm" href="{esc(url)}" target="_blank" rel="noopener" title="{esc(email)}">✉ Gmail</a>')
    # Always show Twitter profile if handle available and not primary
    if twitter and not any("ooq-btn-tw" in b for b in btns):
        btns.append(f'<a class="ooq-btn ooq-btn-tw" href="https://twitter.com/{esc(twitter)}" target="_blank" rel="noopener" title="@{esc(twitter)}">𝕏</a>')

    if not btns:
        return '<a class="ooq-noemail" title="No contact info — add via mark.py">no contact</a>'
    return "".join(btns)


def row(slug: str, p: dict, *, show_tier: bool = True, show_urgency: bool = False) -> str:
    tier = p.get("tier")
    tier_str = (
        f'<span class="ooq-tier ooq-tier-{tier}">T{tier}</span>'
        if show_tier and tier is not None
        else '<span class="ooq-tier ooq-tier-x">—</span>'
    )
    name = esc(p.get("name") or slug)
    touch = short_date(p.get("last_git_touch"))
    chips = signal_chips(p)
    href = f"people/{slug}.html"
    btns = channel_links(p)

    # Status overlay
    status = p.get("status", "not-contacted")
    status_html = ""
    name_style = ""
    if status == "queued":
        status_html = '<span class="ooq-status ooq-status-queued">queued</span>'
    elif status == "contacted":
        last = short_date(p.get("last_contacted"))
        status_html = f'<span class="ooq-status ooq-status-contacted">contacted {esc(last)}</span>'
        name_style = ' style="text-decoration:line-through; color:var(--fg-muted);"'
    elif status == "replied":
        status_html = '<span class="ooq-status ooq-status-replied">&#9733; replied</span>'

    # Body line: urgency_reason if seeded, otherwise truncated one_liner.
    urgency_reason = p.get("urgency_reason")
    next_action = p.get("next_action")
    channel_label = p.get("channel")
    decay = p.get("urgency_decay_date")

    body_parts = []
    if show_urgency and urgency_reason:
        body_parts.append(f'<span class="ooq-why">{esc(truncate_at_word(urgency_reason, 180))}</span>')
        if next_action:
            ch = f' <span class="ooq-channel">→ {esc(channel_label)}</span>' if channel_label else ""
            body_parts.append(f'<div class="ooq-action">{ch} {esc(truncate_at_word(next_action, 130))}</div>')
        if decay:
            body_parts.append(f'<span class="ooq-decay">closes {esc(decay)}</span>')
    else:
        ol = truncate_at_word(p.get("one_liner") or "", 160)
        body_parts.append(f'<span class="ooq-oneliner">{esc(ol)}</span>')

    body_html = '<div class="ooq-body">' + "".join(body_parts) + '</div>'

    return (
        f'<li class="ooq-row">'
        f'{tier_str}'
        f'<span class="ooq-date">{esc(touch)}</span>'
        f'<a href="{href}" class="ooq-name"{name_style}>{name}</a>'
        f'<span class="ooq-chips">{chips}</span>'
        f'{status_html}'
        f'<span class="ooq-btns">{btns}</span>'
        f'{body_html}'
        f'</li>'
    )


def style_block() -> str:
    """Inline scoped styles so this panel is self-contained."""
    return """<style>
.ooq-panel { border:1px solid var(--border); border-left:3px solid var(--accent); background:var(--card-bg); padding:1rem 1.1rem; margin:1.25rem 0 1.75rem; font-size:0.85rem; }
.ooq-head { display:flex; justify-content:space-between; align-items:baseline; font-family:var(--mono); font-size:0.7rem; text-transform:uppercase; letter-spacing:0.1em; color:var(--fg-muted); margin-bottom:0.6rem; }
.ooq-head .ooq-built { font-size:0.65rem; color:var(--fg-faint); text-transform:none; letter-spacing:0; }
.ooq-section-h { font-family:var(--mono); font-size:0.7rem; text-transform:uppercase; letter-spacing:0.08em; color:var(--accent); margin:0.9rem 0 0.4rem; padding-bottom:0.2rem; border-bottom:1px solid var(--border-light); }
.ooq-section-h.ooq-h-triage { color:#9c6500; }
.ooq-section-h.ooq-h-flight { color:#4a7a3a; }
.ooq-section-h.ooq-h-today { color:var(--accent); border-bottom:2px solid var(--accent); font-size:0.78rem; }
.ooq-section-h.ooq-h-capital { color:#3a5a7a; }
.ooq-list { list-style:none; padding:0; margin:0; }
.ooq-row { display:grid; grid-template-columns: 36px 78px 1fr auto auto auto; gap:0.45rem 0.6rem; align-items:baseline; padding:0.5rem 0; border-bottom:1px dotted var(--border-light); }
.ooq-btns { display:flex; gap:0.25rem; flex-wrap:nowrap; }
.ooq-btn { font-family:var(--mono); font-size:0.62rem; padding:0.1rem 0.4rem; border-radius:2px; text-decoration:none; border:1px solid transparent; white-space:nowrap; }
.ooq-btn-gm { border-color:var(--accent); color:var(--accent); background:#fff; }
.ooq-btn-gm:hover { background:var(--accent); color:#fff; }
.ooq-btn-tw { border-color:#1da1f2; color:#1da1f2; background:#fff; }
.ooq-btn-tw:hover { background:#1da1f2; color:#fff; }
.ooq-btn-li { border-color:#0a66c2; color:#0a66c2; background:#fff; }
.ooq-btn-li:hover { background:#0a66c2; color:#fff; }
.ooq-gmail { font-family:var(--mono); font-size:0.65rem; padding:0.1rem 0.45rem; border:1px solid var(--accent); color:var(--accent); border-radius:2px; text-decoration:none; background:#fff; }
.ooq-gmail:hover { background:var(--accent); color:#fff; }
.ooq-noemail { font-family:var(--mono); font-size:0.62rem; color:var(--fg-faint); font-style:italic; }
.ooq-row:last-child { border-bottom:none; }
.ooq-body { grid-column: 3 / -1; margin-top:0.2rem; }
.ooq-why { font-size:0.78rem; color:var(--fg); font-weight:500; }
.ooq-action { font-size:0.74rem; color:var(--fg-muted); margin-top:0.15rem; }
.ooq-channel { font-family:var(--mono); font-size:0.65rem; color:var(--accent); text-transform:uppercase; letter-spacing:0.05em; }
.ooq-decay { font-family:var(--mono); font-size:0.65rem; color:#9c6500; margin-left:0.5rem; }
.ooq-tier { font-family:var(--mono); font-size:0.7rem; font-weight:600; text-align:center; padding:0.1rem 0.3rem; border-radius:2px; }
.ooq-tier-0 { background:var(--accent); color:#fff; }
.ooq-tier-1 { background:#f0e0dd; color:var(--accent); }
.ooq-tier-2 { background:#f4e9d8; color:#9c6500; }
.ooq-tier-3 { background:#eee; color:var(--fg-muted); }
.ooq-tier-x { background:transparent; color:var(--fg-faint); }
.ooq-date { font-family:var(--mono); font-size:0.7rem; color:var(--fg-faint); }
.ooq-name { font-weight:600; text-decoration:none; color:var(--fg); }
.ooq-name:hover { text-decoration:underline; }
.ooq-chips { display:flex; gap:0.25rem; flex-wrap:wrap; }
.ooq-chip { font-family:var(--mono); font-size:0.62rem; padding:0.05rem 0.32rem; border-radius:2px; text-transform:lowercase; letter-spacing:0.03em; }
.ooq-chip-in { background:#e8eef5; color:#3a5a7a; }
.ooq-chip-stealth { background:#f0e0dd; color:var(--accent); }
.ooq-chip-departed { background:#fdf2d6; color:#9c6500; }
.ooq-chip-raising { background:#dfeede; color:#3a6a2a; }
.ooq-status { font-family:var(--mono); font-size:0.65rem; padding:0.05rem 0.35rem; border-radius:2px; }
.ooq-status-queued { background:#eef; color:#447; }
.ooq-status-contacted { background:#eee; color:var(--fg-muted); }
.ooq-status-replied { background:#dfeede; color:#3a6a2a; }
.ooq-oneliner { grid-column: 3 / -1; font-size:0.78rem; color:var(--fg-muted); margin-top:-0.1rem; }
.ooq-stats { font-family:var(--mono); font-size:0.7rem; color:var(--fg-faint); margin-top:0.9rem; padding-top:0.6rem; border-top:1px solid var(--border-light); }
.ooq-empty { color:var(--fg-faint); font-style:italic; padding:0.4rem 0; }
</style>"""


def build_panel(state: dict) -> str:
    from datetime import date
    people = state.get("people", {})
    live = {s: p for s, p in people.items() if not p.get("_orphan")}

    def sort_key(item):
        slug, p = item
        return p.get("last_git_touch") or ""

    today_iso = date.today().isoformat()

    # PANEL 0 (NEW): TODAY'S 5 — seeded urgency entries, ranked
    # These have urgency_reason set, status not-contacted, and next_action_date
    # is today or earlier (or null).
    def days_until(iso: str | None) -> int:
        if not iso:
            return 999
        try:
            return (date.fromisoformat(iso) - date.today()).days
        except ValueError:
            return 999

    def priority(p: dict) -> int:
        tier = p.get("tier")
        weights = {0: 4, 1: 3, 2: 2, 3: 1}
        w = weights.get(tier, 0)
        urgency = max(0, 100 - days_until(p.get("urgency_decay_date"))) if p.get("urgency_decay_date") else 0
        return w * 100 + urgency

    todays = [
        (s, p) for s, p in live.items()
        if p.get("status") == "not-contacted"
        and p.get("urgency_reason")
        and (not p.get("next_action_date") or p["next_action_date"] <= today_iso)
    ]
    todays.sort(key=lambda x: priority(x[1]), reverse=True)

    # PANEL 1: Reach out next (broader — all T0/T1 outreach not contacted)
    outreach = [
        (s, p) for s, p in live.items()
        if p.get("tier") in (0, 1)
        and p.get("category") == "outreach"
        and p.get("status") == "not-contacted"
    ]
    # T0 first, then T1, freshest within tier
    outreach.sort(key=lambda x: (x[1].get("tier", 99), -1 * (int((x[1].get("last_git_touch") or "0000")[:4]) * 10000 + int((x[1].get("last_git_touch") or "0000-00")[5:7]) * 100 + int((x[1].get("last_git_touch") or "0000-00-00")[8:10]))))

    # PANEL 2: Triage — untiered with hot signal, EXCLUDING LP/peer/network entries
    hot_signal_keys = ("tag_stealth_founder", "phrase_stealth", "phrase_departed", "phrase_raising")
    triage = [
        (s, p) for s, p in live.items()
        if p.get("tier") is None
        and any(p.get("signals", {}).get(k) for k in hot_signal_keys)
        and p.get("category") not in ("network",)  # Exclude LPs/investors/peer VCs
        and "lp-prospect" not in (p.get("tags") or [])
        and "vc-talent" not in (p.get("tags") or [])
    ]
    triage.sort(key=sort_key, reverse=True)

    # PANEL: Capital / LP / VC peers — separate from founder triage
    capital = [
        (s, p) for s, p in live.items()
        if (
            "lp-prospect" in (p.get("tags") or [])
            or "vc-talent" in (p.get("tags") or [])
            or p.get("category") == "network"
        )
        and p.get("status") == "not-contacted"
    ]
    capital.sort(key=sort_key, reverse=True)

    # PANEL 3: In flight — anything queued/contacted/replied
    in_flight = [
        (s, p) for s, p in live.items()
        if p.get("status") in ("queued", "contacted", "replied")
    ]
    in_flight.sort(key=lambda x: ({"queued": 0, "replied": 1, "contacted": 2}.get(x[1].get("status"), 9),
                                  -1 * (int((x[1].get("last_contacted") or x[1].get("last_git_touch") or "0000")[:4]) * 10000)))

    # Stats footer
    from collections import Counter
    tier_counts = Counter(p.get("tier") for p in live.values())
    cat_counts = Counter((p.get("tier"), p.get("category")) for p in live.values())
    network_t1 = cat_counts.get((1, "network"), 0)
    network_t2 = cat_counts.get((2, "network"), 0)

    built = state.get("last_built", "")[:19].replace("T", " ") + " UTC"

    parts = [style_block(), '<div class="ooq-panel">']
    parts.append(
        f'<div class="ooq-head"><span>&#9670; Outreach Queue &mdash; auto</span>'
        f'<span class="ooq-built">built {esc(built)} &middot; {len(live)} entries</span></div>'
    )

    # Panel 0 (NEW): Today's 5 — the ADHD-friendly daily queue
    parts.append('<div class="ooq-section-h ooq-h-today">Today\'s 5 &mdash; seeded urgency, ranked by tier &times; decay</div>')
    parts.append('<ul class="ooq-list">')
    if todays:
        for slug, p in todays[:5]:
            parts.append(row(slug, p, show_urgency=True))
    else:
        parts.append('<li class="ooq-empty">No urgency-seeded entries. Run scripts/seed_priorities.py to add some.</li>')
    parts.append('</ul>')

    # Panel 1: broader tier-0/1 outreach
    parts.append('<div class="ooq-section-h">Reach out next &mdash; tier 0/1, not yet contacted</div>')
    parts.append('<ul class="ooq-list">')
    if outreach:
        for slug, p in outreach[:TOP_N_OUTREACH]:
            parts.append(row(slug, p))
    else:
        parts.append('<li class="ooq-empty">No tier 0/1 outreach candidates pending.</li>')
    parts.append('</ul>')

    # Panel 2
    parts.append(
        f'<div class="ooq-section-h ooq-h-triage">'
        f'Triage queue &mdash; untiered + founder/departure/raising signal '
        f'({len(triage)})'
        f'</div>'
    )
    parts.append('<ul class="ooq-list">')
    if triage:
        for slug, p in triage[:TOP_N_TRIAGE]:
            parts.append(row(slug, p, show_tier=False))
        if len(triage) > TOP_N_TRIAGE:
            parts.append(f'<li class="ooq-empty">&hellip; and {len(triage) - TOP_N_TRIAGE} more in state file</li>')
    else:
        parts.append('<li class="ooq-empty">No untiered dossiers with hot signal.</li>')
    parts.append('</ul>')

    # Capital panel (LPs, investors, VC peers — separate from founder triage)
    if capital:
        parts.append(f'<div class="ooq-section-h ooq-h-capital">Capital &mdash; LPs / VC peers ({len(capital)})</div>')
        parts.append('<ul class="ooq-list">')
        for slug, p in capital[:8]:
            parts.append(row(slug, p, show_urgency=True))
        parts.append('</ul>')

    # Panel 3 (only if anything in flight)
    if in_flight:
        parts.append(f'<div class="ooq-section-h ooq-h-flight">In flight ({len(in_flight)})</div>')
        parts.append('<ul class="ooq-list">')
        for slug, p in in_flight:
            parts.append(row(slug, p))
        parts.append('</ul>')

    # Stats
    untiered = tier_counts.get(None, 0)
    parts.append(
        f'<div class="ooq-stats">'
        f'T0: {tier_counts.get(0, 0)} &middot; '
        f'T1: {tier_counts.get(1, 0)} (+{network_t1} network) &middot; '
        f'T2: {tier_counts.get(2, 0)} (+{network_t2} network) &middot; '
        f'T3: {tier_counts.get(3, 0)} &middot; '
        f'untiered: <strong>{untiered}</strong>'
        f'</div>'
    )
    parts.append('</div>')
    return "\n".join(parts)


def inject(index_html: str, panel_html: str) -> str:
    pattern = re.compile(
        re.escape(START_MARKER) + r"(.*?)" + re.escape(END_MARKER),
        re.DOTALL,
    )
    if not pattern.search(index_html):
        raise SystemExit(
            f"Markers not found in {INDEX_FILE.name}. Expected:\n"
            f"  {START_MARKER}\n  ... content ...\n  {END_MARKER}"
        )
    replacement = (
        f"{START_MARKER}\n"
        f"  <!-- Auto-generated by data/build_outreach_view.py from data/outreach_state.json. -->\n"
        f"  <!-- Do not hand-edit between these markers; edits will be overwritten on next build. -->\n"
        f"{panel_html}\n"
        f"  {END_MARKER}"
    )
    return pattern.sub(lambda _m: replacement, index_html, count=1)


def main() -> int:
    if not STATE_FILE.exists():
        print(f"State file missing: {STATE_FILE}. Run build_outreach_state.py first.", file=sys.stderr)
        return 1
    state = json.loads(STATE_FILE.read_text())

    panel_html = build_panel(state)

    original = INDEX_FILE.read_text(encoding="utf-8")
    updated = inject(original, panel_html)

    if updated == original:
        print("No change — panel content already current.")
        return 0

    INDEX_FILE.write_text(updated, encoding="utf-8")

    # Report what's now visible.
    people = state["people"]
    live = [p for p in people.values() if not p.get("_orphan")]
    outreach_pending = sum(
        1 for p in live
        if p.get("tier") in (0, 1) and p.get("category") == "outreach" and p.get("status") == "not-contacted"
    )
    triage = sum(
        1 for p in live
        if p.get("tier") is None
        and any(p.get("signals", {}).get(k) for k in
                ("tag_stealth_founder", "phrase_stealth", "phrase_departed", "phrase_raising"))
    )
    in_flight = sum(1 for p in live if p.get("status") in ("queued", "contacted", "replied"))

    delta_bytes = len(updated) - len(original)
    print(f"Injected outreach panel into {INDEX_FILE.name} ({delta_bytes:+d} bytes)")
    print(f"  Reach out next:   {outreach_pending} candidates (showing top {TOP_N_OUTREACH})")
    print(f"  Triage queue:     {triage} untiered+hot (showing top {TOP_N_TRIAGE})")
    print(f"  In flight:        {in_flight}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
