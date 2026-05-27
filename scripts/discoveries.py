#!/usr/bin/env python3
"""
discoveries.py
==============
Surface recursive discoveries — people that dossier agents have flagged as
worth following up but haven't been enriched yet.

The pattern: when we run a 6-agent SOP on (say) Saksham, the agent surfaces
Sumith Kulal + Chenlin Meng + Robin Rombach + Sharon Zhou as adjacents.
Before this script, those names lived only in the chat transcript and
got lost. Now they live in data/recursive_discoveries.json and surface
in the morning ritual.

Workflow:
    1. Agent finishes dossier → mentions adjacent candidates
    2. (Manual for now) entries get added to data/recursive_discoveries.json
       with status="pending"
    3. Morning ritual surfaces top N pending → you approve/defer/reject
    4. Approved entries get a real dossier built next

Usage:
    python3 scripts/discoveries.py             # top 5 pending (morning ritual default)
    python3 scripts/discoveries.py --all       # full list
    python3 scripts/discoveries.py --top N
    python3 scripts/discoveries.py --approve SLUG  (TODO)

CLI status updates (for now, edit JSON or call mark_discovery.py).
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SOURCE = REPO / "data" / "recursive_discoveries.json"

BOLD = "\033[1m"
DIM = "\033[2m"
RED = "\033[31m"
YELLOW = "\033[33m"
GREEN = "\033[32m"
CYAN = "\033[36m"
RESET = "\033[0m"

PRIORITY_WEIGHT = {"P0": 3, "P1": 2, "P2": 1}


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

    if not SOURCE.exists():
        print(f"{DIM}No recursive_discoveries.json yet.{RESET}")
        return

    data = json.loads(SOURCE.read_text())
    discoveries = data.get("discoveries", [])

    pending = [d for d in discoveries if d.get("status") == "pending"]
    pending.sort(key=lambda d: PRIORITY_WEIGHT.get(d.get("priority", "P2"), 0), reverse=True)

    if not pending:
        print(f"{DIM}No pending recursive discoveries. All triaged.{RESET}")
        return

    shown = pending if show_all else pending[:top_n]

    print(f"\n{BOLD}═══ RECURSIVE DISCOVERIES — {len(pending)} pending ═══{RESET}")
    print(f"{DIM}From your dossier agents. Approve to research next.{RESET}\n")

    for d in shown:
        name = d["name"]
        priority = d.get("priority", "P2")
        from_dossier = d.get("from_dossier", "?")
        context = d.get("context", "")
        tags = d.get("tags", [])
        discovered = d.get("discovered_at", "")
        priority_color = RED if priority == "P0" else YELLOW if priority == "P1" else DIM
        print(f"{priority_color}[{priority}]{RESET} {BOLD}{name}{RESET} {DIM}from {from_dossier} · {discovered}{RESET}")
        print(f"     {context[:200]}{'...' if len(context) > 200 else ''}")
        if tags:
            print(f"     {DIM}tags: {', '.join(tags)}{RESET}")
        print()

    if not show_all and len(pending) > top_n:
        print(f"{DIM}... and {len(pending) - top_n} more. Run with --all to see full list.{RESET}\n")

    print(f"{DIM}Approve a discovery: edit data/recursive_discoveries.json (status=approved){RESET}")
    print(f"{DIM}Ask Claude: \"build dossier for SLUG\" to enrich an approved candidate{RESET}\n")


if __name__ == "__main__":
    main()
