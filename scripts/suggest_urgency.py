#!/usr/bin/env python3
"""
suggest_urgency.py
==================
Auto-suggest urgency fields for entries that have signals but no urgency
set yet. Surfaces them so the daily queue never goes dry.

Score formula (heuristic, tune as needed):
    Tier 0  → +50
    Tier 1  → +30
    Tier 2  → +10
    Recent git touch (<30d) → +20
    phrase_stealth          → +30
    phrase_departed         → +30
    phrase_raising          → +25
    phrase_founded          → +15
    indian flag             → +5

Output: top N untriaged entries with proposed urgency fields you can
copy into scripts/seed_priorities.py.

Usage:
    python3 scripts/suggest_urgency.py            # top 15
    python3 scripts/suggest_urgency.py --json     # machine-readable
    python3 scripts/suggest_urgency.py --top 30   # custom limit
"""
from __future__ import annotations
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
STATE = REPO / "data" / "outreach_state.json"

DEFAULT_TOP = 15

BOLD = "\033[1m"
DIM = "\033[2m"
RED = "\033[31m"
YELLOW = "\033[33m"
GREEN = "\033[32m"
CYAN = "\033[36m"
RESET = "\033[0m"


def days_since(iso: str | None) -> int:
    if not iso:
        return 9999
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    except ValueError:
        return 9999
    return (datetime.now(timezone.utc) - dt).days


def score(p: dict) -> int:
    s = 0
    tier = p.get("tier")
    if tier == 0: s += 50
    elif tier == 1: s += 30
    elif tier == 2: s += 10

    git_days = days_since(p.get("last_git_touch"))
    if git_days <= 30:
        s += 20

    sigs = p.get("signals") or {}
    if sigs.get("phrase_stealth"): s += 30
    if sigs.get("tag_stealth_founder"): s += 35
    if sigs.get("phrase_departed"): s += 30
    if sigs.get("phrase_raising"): s += 25
    if sigs.get("phrase_founded"): s += 15
    if p.get("indian"): s += 5

    return s


def suggest_urgency_reason(p: dict) -> str:
    """Heuristic-based one-liner suggestion you can paste + customize."""
    sigs = p.get("signals") or {}
    parts = []
    if sigs.get("phrase_departed"):
        parts.append("Recent departure signal")
    if sigs.get("phrase_stealth") or sigs.get("tag_stealth_founder"):
        parts.append("Stealth mode")
    if sigs.get("phrase_raising"):
        parts.append("Raising")
    if sigs.get("phrase_founded"):
        parts.append("Founded company")
    if not parts:
        tier = p.get("tier")
        if tier == 0:
            parts.append("T0 active pursuit — verify and customize")
        elif tier == 1:
            parts.append("T1 high conviction — relationship build")
    one_liner = (p.get("one_liner") or "")[:80]
    return " · ".join(parts) + (f" — {one_liner}" if one_liner else "")


def suggest_channel(p: dict) -> str:
    """Default channel based on signals + available identifiers."""
    sigs = p.get("signals") or {}
    if sigs.get("phrase_stealth") or sigs.get("tag_stealth_founder"):
        if p.get("twitter_handle"):
            return "twitter"
        return "email"
    if p.get("email_primary"):
        return "email"
    if p.get("twitter_handle"):
        return "twitter"
    if p.get("linkedin_slug"):
        return "linkedin"
    return "email"


def main():
    args = sys.argv[1:]
    top_n = DEFAULT_TOP
    json_out = False
    if "--json" in args:
        json_out = True
    if "--top" in args:
        i = args.index("--top")
        if i + 1 < len(args):
            try:
                top_n = int(args[i + 1])
            except ValueError:
                pass

    state = json.loads(STATE.read_text())
    people = state["people"]

    # Eligible: not contacted, no urgency_reason set yet, tier exists or has signals
    eligible = []
    for slug, p in people.items():
        if p.get("status") != "not-contacted":
            continue
        if p.get("urgency_reason"):
            continue  # already seeded
        if p.get("_orphan"):
            continue
        # Must have at least one signal or tier
        sigs = p.get("signals") or {}
        has_signal = any(sigs.values()) or p.get("tier") is not None
        if not has_signal:
            continue
        eligible.append((slug, p, score(p)))

    eligible.sort(key=lambda x: x[2], reverse=True)
    eligible = eligible[:top_n]

    if json_out:
        out = []
        for slug, p, sc in eligible:
            out.append({
                "slug": slug,
                "name": p.get("name"),
                "tier": p.get("tier"),
                "score": sc,
                "suggested_urgency_reason": suggest_urgency_reason(p),
                "suggested_channel": suggest_channel(p),
                "email": p.get("email_primary"),
                "twitter": p.get("twitter_handle"),
            })
        print(json.dumps(out, indent=2))
        return

    if not eligible:
        print(f"{DIM}No untriaged entries with signals. Add new dossiers or rebuild state.{RESET}")
        return

    print(f"\n{BOLD}═══ TRIAGE — top {len(eligible)} untriaged entries with signals ═══{RESET}")
    print(f"{DIM}Edit scripts/seed_priorities.py to promote these (add slug + urgency fields){RESET}\n")

    for slug, p, sc in eligible:
        name = p.get("name", slug)
        tier = p.get("tier")
        tier_str = f"T{tier}" if tier is not None else "--"
        sigs = [k.replace("phrase_", "").replace("tag_", "") for k, v in (p.get("signals") or {}).items() if v]
        sig_str = ",".join(sigs[:4]) if sigs else "—"
        indian = "IN" if p.get("indian") else "  "
        print(f"{BOLD}[{tier_str}] {name:32s}{RESET} {DIM}score={sc:3d} [{indian}] {sig_str}{RESET}")
        print(f"  slug:    {slug}")
        print(f"  why:     {suggest_urgency_reason(p)}")
        print(f"  channel: {suggest_channel(p)}")
        if p.get("email_primary"):
            print(f"  email:   {p['email_primary']}")
        if p.get("twitter_handle"):
            print(f"  twitter: @{p['twitter_handle']}")
        print()


if __name__ == "__main__":
    main()
