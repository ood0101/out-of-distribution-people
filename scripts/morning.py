#!/usr/bin/env python3
"""
morning.py
==========
The full daily ritual in one command. Run this when you sit down.

Sequence:
  1. Refresh state from dossiers (catches new dossiers, updated handles, emails)
  2. Render index outreach panel (so browser view is fresh)
  3. Cluster activity check (who in your clusters moved overnight?)
  4. Triage suggestions (any new untriaged high-signal entries?)
  5. Today's 5 — the actual queue

Total runtime: ~2 seconds. Replaces the need for cron.

Usage:
    python3 scripts/morning.py

Add to your shell (~/.zshrc or ~/.bash_profile) for one-keystroke access:
    alias morning='cd "/Users/vansh/out of distribution people repo" && python3 scripts/morning.py'

Then each morning, just type: morning
"""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "data"
SCRIPTS = REPO / "scripts"

BOLD = "\033[1m"
DIM = "\033[2m"
CYAN = "\033[36m"
RESET = "\033[0m"


def section(title: str):
    print(f"\n{BOLD}{CYAN}━━━ {title} ━━━{RESET}")


def run(script: Path, *args, capture: bool = False) -> str | None:
    """Run a script; print stdout inline unless capture=True."""
    cmd = ["python3", str(script), *args]
    try:
        if capture:
            r = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, check=True)
            return r.stdout
        else:
            subprocess.run(cmd, cwd=REPO, check=True)
            return None
    except subprocess.CalledProcessError as e:
        print(f"  ERROR: {script.name} failed: {e}", file=sys.stderr)
        return None


def main():
    # 1. Refresh state (silent — only show if it surfaces something interesting)
    section("Refreshing state from dossiers")
    out = run(DATA / "build_outreach_state.py", capture=True)
    if out:
        # Only show the final tier breakdown lines
        for line in out.splitlines()[-10:]:
            if line.strip():
                print(f"  {DIM}{line}{RESET}")

    # 2. Re-render index panel
    section("Re-rendering index outreach panel")
    out = run(DATA / "build_outreach_view.py", capture=True)
    if out:
        for line in out.splitlines():
            print(f"  {DIM}{line.strip()}{RESET}")

    # 3. Cluster activity
    section("Cluster activity check")
    run(SCRIPTS / "cluster_check.py")

    # 4. Recursive discoveries — adjacents surfaced by past dossier agents
    section("Recursive discoveries — approve to research next")
    run(SCRIPTS / "discoveries.py", "--top", "5")

    # 5. Refresh due — stale T0/T1 dossiers needing re-check
    section("Refresh due — pick 1-2 to refresh today")
    run(SCRIPTS / "refresh_due.py", "--top", "5")

    # 6. Promotion candidates (Delta Fellows ready for full dossier)
    section("Promote candidates — Delta Fellows with signals")
    out = run(SCRIPTS / "promote_candidates.py", "--top", "3", capture=True)
    if out:
        for line in out.splitlines()[2:]:  # skip header
            print(line)

    # 7. Triage suggestions (top 5 only here — full list via suggest_urgency.py)
    section("Top untriaged entries (consider adding to seed)")
    out = run(SCRIPTS / "suggest_urgency.py", "--top", "5", capture=True)
    if out:
        skip_header = True
        for line in out.splitlines():
            if skip_header and line.startswith(("\033", "═", "Edit")):
                continue
            if line.strip().startswith("["):
                skip_header = False
            if not skip_header:
                print(line)

    # 8. Today's queue
    section("TODAY'S 5 — send these and close the terminal")
    run(SCRIPTS / "today.py")


if __name__ == "__main__":
    main()
