#!/usr/bin/env python3
"""
refresh_due.py
==============
Surface T0/T1 dossiers that are due for a refresh — i.e., haven't been
touched (git-wise) in N days. Designed for the morning ritual.

Pattern: rather than running stale refreshes on a hard cron, surface
candidates each morning as "approvals you need to make." You pick 1-2 to
refresh per day. Keeps the corpus fresh without overwhelming the daily flow.

A "refresh" means: spawn the dossier agent again with a focused brief on
"what's NEW since last update?" The agent looks for funding announcements,
hiring, departure signals, new papers, bio changes.

Usage:
    python3 scripts/refresh_due.py            # top 5 most stale T0/T1
    python3 scripts/refresh_due.py --all      # full list
    python3 scripts/refresh_due.py --top N

Default surfacing rules:
    - T0: refresh if >14 days since last_git_touch
    - T1: refresh if >30 days
    - T2: refresh if >60 days
"""
from __future__ import annotations
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
STATE = REPO / "data" / "outreach_state.json"

REFRESH_THRESHOLDS = {0: 14, 1: 30, 2: 60}  # days

BOLD = "\033[1m"
DIM = "\033[2m"
RED = "\033[31m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
RESET = "\033[0m"


def parse_iso(s):
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None


def days_since(iso):
    dt = parse_iso(iso)
    if not dt:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - dt).days


def tier_badge(t):
    return f"{RED}T0{RESET}" if t == 0 else f"{YELLOW}T1{RESET}" if t == 1 else f"{CYAN}T2{RESET}" if t == 2 else "--"


def main():
    args = sys.argv[1:]
    top_n = 5
    show_all = "--all" in args
    if "--top" in args:
        i = args.index("--top")
        if i + 1 < len(args):
            try:
                top_n = int(args[i + 1])
            except ValueError:
                pass

    state = json.loads(STATE.read_text())
    people = state["people"]

    candidates = []
    for slug, p in people.items():
        tier = p.get("tier")
        if tier not in (0, 1, 2):
            continue
        # Skip if no dossier (Delta-fellow-only entries)
        if p.get("status") == "indexed":
            continue
        threshold = REFRESH_THRESHOLDS[tier]
        days = days_since(p.get("last_git_touch"))
        if days is None:
            continue
        if days < threshold:
            continue
        candidates.append((days, tier, slug, p))

    # Sort: most-stale first within tier; T0 always before T1
    candidates.sort(key=lambda x: (x[1], -x[0]))

    if not candidates:
        print(f"{DIM}No T0/T1/T2 dossiers due for refresh.{RESET}")
        return

    shown = candidates if show_all else candidates[:top_n]

    print(f"\n{BOLD}═══ REFRESH DUE — {len(candidates)} dossiers ═══{RESET}")
    print(f"{DIM}T0 >14d, T1 >30d, T2 >60d. Pick 1-2 per morning to refresh.{RESET}\n")

    for days, tier, slug, p in shown:
        name = p.get("name", slug)
        ol = (p.get("one_liner") or "")[:90]
        urgency = "⚠️ " if days > 90 else ""
        print(f"{urgency}{tier_badge(tier)}  {BOLD}{name}{RESET} {DIM}({slug}){RESET}  {RED}{days}d stale{RESET}")
        if ol:
            print(f"     {DIM}{ol}{RESET}")
        print(f"     {DIM}Ask Claude: \"refresh {slug}\" — agent will check for new signals since last touch{RESET}")
        print()


if __name__ == "__main__":
    main()
