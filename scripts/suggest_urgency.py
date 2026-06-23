#!/usr/bin/env python3
"""
suggest_urgency.py — RETIRED (2026-06-23)
=========================================
This script used to SCORE people by founder/startup-probability — tier weight
plus stealth/departed/raising/founded signal bonuses — and rank an "urgency"
queue from it. That is exactly the behavior the owner asked us to stop:

    "we anchor around the starting up probability and score agent runs —
     lets not do that."

The repo is no longer a founder-screening system. Every person the owner sends
is already a reach-out target; we do not rank them by likelihood-of-founding.
There is nothing to score.

What replaced it: the dossier itself now delivers **1–3 outreach angles** per
person (see AGENT_SOP.md → "Outreach Angles & Email"). The hand-curated
intent lives in scripts/seed_priorities.py (urgency_reason / next_action =
the outreach angle), set by the owner — not computed by a heuristic.

This file is kept only so nothing that imports it breaks. Running it does
nothing but print this notice.
"""
from __future__ import annotations
import sys


def main() -> int:
    sys.stderr.write(
        "suggest_urgency.py is RETIRED — founder/startup-probability scoring "
        "was removed (owner call). The dossier's 1–3 outreach angles replace it; "
        "see AGENT_SOP.md and scripts/seed_priorities.py.\n"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
