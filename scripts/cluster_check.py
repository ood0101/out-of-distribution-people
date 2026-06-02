#!/usr/bin/env python3
"""
cluster_check.py
================
Detect cluster activity: when one member of a cluster has recent dossier
activity (git commit) or status change, surface all other members for
re-evaluation.

Idea: people in the same cluster (ScaleRL, Hazy, architecture, Indian-IIT-Delhi,
diffusion-video, etc.) often move together. If Devvrit's status flips to
"contacted" while Lovish and Rishabh are still "not-contacted", that's a
prompt to outreach the whole cluster within the same window.

Run as a cron job (daily at 7am):
    0 7 * * * cd /path/to/repo && python3 scripts/cluster_check.py

Output: list of clusters with recent activity + the under-engaged members.
"""
from __future__ import annotations
import json
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
STATE = REPO / "data" / "outreach_state.json"

# Window of "recent" activity. Adjustable.
RECENT_DAYS = 14

BOLD = "\033[1m"
DIM = "\033[2m"
RED = "\033[31m"
YELLOW = "\033[33m"
GREEN = "\033[32m"
CYAN = "\033[36m"
RESET = "\033[0m"


def parse_iso(s: str | None):
    if not s:
        return None
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        try:
            dt = datetime.fromisoformat(s + "T00:00:00+00:00")
        except ValueError:
            return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def days_since(s: str | None) -> int:
    dt = parse_iso(s)
    if dt is None:
        return 9999
    return (datetime.now(timezone.utc) - dt).days


def main():
    state = json.loads(STATE.read_text())
    people = state["people"]

    # Group by cluster
    clusters = defaultdict(list)
    for slug, e in people.items():
        c = e.get("cluster")
        if not c:
            continue
        clusters[c].append((slug, e))

    if not clusters:
        print(f"{DIM}No clusters tagged. Seed via scripts/seed_priorities.py.{RESET}")
        return

    today = date.today()
    cutoff_days = RECENT_DAYS

    active_clusters = []
    for cluster_name, members in clusters.items():
        # Detect activity in window
        events = []  # (slug, kind, days_ago, detail)
        for slug, e in members:
            git_days = days_since(e.get("last_git_touch"))
            contact_days = days_since(e.get("last_contacted"))
            if git_days <= cutoff_days:
                events.append((slug, "git", git_days, f"dossier updated {git_days}d ago"))
            if contact_days <= cutoff_days and e.get("status") == "contacted":
                events.append((slug, "sent", contact_days, f"you reached out {contact_days}d ago"))
            if e.get("status") == "replied":
                events.append((slug, "replied", 0, "REPLIED — this is the cluster trigger"))
        if events:
            active_clusters.append((cluster_name, members, events))

    if not active_clusters:
        print(f"{DIM}No cluster activity in the last {cutoff_days} days.{RESET}")
        return

    print(f"\n{BOLD}═══ CLUSTER ACTIVITY — last {cutoff_days} days ═══{RESET}\n")

    # Sort clusters: those with reply > those with sent > those with only git activity
    def cluster_priority(c):
        _, _, events = c
        if any(e[1] == "replied" for e in events):
            return 3
        if any(e[1] == "sent" for e in events):
            return 2
        return 1

    active_clusters.sort(key=cluster_priority, reverse=True)

    for cluster_name, members, events in active_clusters:
        print(f"{BOLD}{CYAN}#{cluster_name}{RESET}  {DIM}({len(members)} members){RESET}")
        # Show events
        for slug, kind, days_ago, detail in sorted(events, key=lambda x: x[2]):
            icon = {"git": "📝", "sent": "📤", "replied": "★"}.get(kind, "•")
            print(f"  {icon} {DIM}{slug:30s}{RESET} {detail}")
        # Show under-engaged members (not-contacted, no urgency)
        cold = [s for s, e in members if e.get("status") == "not-contacted" and not e.get("urgency_reason")]
        hot_uncontacted = [s for s, e in members if e.get("status") == "not-contacted" and e.get("urgency_reason")]
        if hot_uncontacted:
            print(f"  {YELLOW}→ urgency set but not yet contacted: {', '.join(hot_uncontacted)}{RESET}")
        if cold:
            print(f"  {RED}→ COLD members (consider re-evaluating urgency): {', '.join(cold)}{RESET}")
        print()

    # Quick action hint
    print(f"{DIM}Re-evaluate cluster urgency: scripts/seed_priorities.py (edit + re-run){RESET}\n")


if __name__ == "__main__":
    main()
