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
from datetime import date
from pathlib import Path
from urllib.parse import quote

REPO = Path(__file__).resolve().parent.parent
STATE = REPO / "data" / "outreach_state.json"

MAX_DAILY = 5
TIER_WEIGHT = {0: 4, 1: 3, 2: 2, 3: 1, None: 0}

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


def priority(entry: dict) -> int:
    tier = entry.get("tier")
    weight = TIER_WEIGHT.get(tier, 0)
    urgency = max(0, 100 - days_until(entry.get("urgency_decay_date"))) if entry.get("urgency_decay_date") else 0
    return weight * 100 + urgency


def is_eligible(entry: dict) -> bool:
    if entry.get("status") != "not-contacted":
        return False
    next_dt = entry.get("next_action_date")
    if next_dt and next_dt > today_iso():
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

    # Email + Gmail compose URL (live, respects override).
    email, kind = resolve_email(e)
    subject = e.get("outreach_subject_override") or e.get("outreach_subject")
    body = e.get("outreach_body_override")  # full body only available if user pasted it
    gmail_url = gmail_compose_url(email, subject, body) if email else None

    email_line = ""
    if email:
        all_emails = e.get("emails") or []
        alts = [x for x in all_emails if x != email]
        alt_str = f"  {DIM}(also: {', '.join(alts)}){RESET}" if alts else ""
        email_line = f"\n   {CYAN}✉  {email}{RESET} {DIM}[{kind}]{RESET}{alt_str}"
    else:
        email_line = f"\n   {DIM}✉  no email — add via: mark.py {slug} email <addr>{RESET}"

    gmail_line = ""
    if gmail_url:
        # Most modern terminals (iTerm2, macOS Terminal) make this cmd-clickable.
        gmail_line = f"\n   {GREEN}📧 {gmail_url}{RESET}"

    lines = [
        f"{BOLD}{i}. {tier_badge(tier)} {name}{RESET} {DIM}({slug}){RESET}{cluster_str}",
        f"   {DIM}WHY:{RESET} {reason}{decay_str}",
        f"   {GREEN}→ {channel}{RESET}  {action}{email_line}{gmail_line}",
    ]
    return "\n".join(lines)


def main():
    args = sys.argv[1:]
    state = json.loads(STATE.read_text())
    people = state["people"]

    eligible = [(slug, e) for slug, e in people.items() if is_eligible(e)]
    ranked = sorted(eligible, key=lambda x: priority(x[1]), reverse=True)

    if "--all" in args:
        print(f"{BOLD}ALL ELIGIBLE — {len(ranked)} entries{RESET}\n")
        for i, (slug, e) in enumerate(ranked, 1):
            tier = e.get("tier")
            print(f"{tier_badge(tier)} {priority(e):4d}  {slug}")
        return

    if "--triage" in args:
        triage = [(s, e) for s, e in ranked if not has_urgency(e) and e.get("tier") in (0, 1)]
        print(f"{BOLD}TRIAGE — {len(triage)} tiered entries missing urgency_reason{RESET}")
        print(f"{DIM}Add urgency_reason / next_action / channel to scripts/seed_priorities.py{RESET}\n")
        for slug, e in triage[:30]:
            tier = e.get("tier")
            name = e.get("name", slug)
            ol = (e.get("one_liner") or "")[:90]
            print(f"  {tier_badge(tier)} {name:35s} {DIM}{ol}{RESET}")
        return

    # Default: daily 5
    actionable = [(s, e) for s, e in ranked if has_urgency(e)]
    daily = actionable[:MAX_DAILY]

    if not daily:
        print(f"{DIM}No actionable entries today. Seed urgency fields via scripts/seed_priorities.py{RESET}")
        return

    print(f"\n{BOLD}═══ TODAY'S OUTREACH — {today_iso()} ═══{RESET}")
    print(f"{DIM}{MAX_DAILY} max. Send these, then close the terminal.{RESET}\n")

    for i, (slug, e) in enumerate(daily, 1):
        print(render_row(slug, e, i))
        print()

    # Footer summary
    total_pool = len(actionable)
    in_flight = sum(1 for e in people.values() if e.get("status") in ("queued", "contacted"))
    replied = sum(1 for e in people.values() if e.get("status") == "replied")
    print(f"{DIM}─" * 70 + RESET)
    print(f"{DIM}Pool: {total_pool} actionable · In flight: {in_flight} · Replied: {replied}{RESET}")
    print(f"{DIM}Mark sent: python3 scripts/mark.py <slug> sent{RESET}\n")


if __name__ == "__main__":
    main()
