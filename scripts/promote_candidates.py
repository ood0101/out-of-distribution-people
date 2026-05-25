#!/usr/bin/env python3
"""
promote_candidates.py
=====================
Surface Delta Fellows (and other thin-page indexed entries) that have
high signal density but haven't been promoted to full 6-agent dossiers.

These are the "next Michael Wornow" candidates — already in the corpus as
auto-generated thin pages, with founder/stealth/departed/raising signals
that warrant the full SOP treatment.

Run in your morning ritual to find ONE entry per day to promote.

Usage:
    python3 scripts/promote_candidates.py            # top 15
    python3 scripts/promote_candidates.py --top 30
    python3 scripts/promote_candidates.py --all      # full list
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
STATE = REPO / "data" / "outreach_state.json"

BOLD = "\033[1m"
DIM = "\033[2m"
RED = "\033[31m"
YELLOW = "\033[33m"
GREEN = "\033[32m"
CYAN = "\033[36m"
RESET = "\033[0m"


def score_for_promotion(p: dict) -> int:
    """Heuristic for 'should this thin page be upgraded to full dossier'.

    Weights signals more than the daily-queue formula does, because thin
    pages don't have urgency_decay etc. — only signals tell us if there's
    an inflection.
    """
    sigs = p.get("signals") or {}
    score = 0
    if sigs.get("tag_stealth_founder"): score += 40
    if sigs.get("phrase_stealth"): score += 30
    if sigs.get("phrase_departed"): score += 30
    if sigs.get("phrase_raising"): score += 25
    if sigs.get("phrase_founded"): score += 15
    if sigs.get("tag_founders"): score += 20
    # Bonus for cohorts the owner explicitly tracks
    if p.get("indian"): score += 10
    one_liner = (p.get("one_liner") or "").lower()
    # Bonus if at a frontier-tracked company
    if any(c in one_liner for c in ("anthropic", "openai", "deepmind", "thinking machines", "perplexity", "cursor", "anysphere", "scale ai", "humans&", "humans &", "physical intelligence", "reflection", "cartesia", "luma", "black forest", "bfl", "essential ai", "standard intelligence")):
        score += 25
    return score


def main():
    args = sys.argv[1:]
    top_n = 15
    if "--all" in args:
        top_n = 9999
    elif "--top" in args:
        i = args.index("--top")
        if i + 1 < len(args):
            try: top_n = int(args[i + 1])
            except ValueError: pass

    state = json.loads(STATE.read_text())
    people = state["people"]

    candidates = []
    for slug, p in people.items():
        # Already a full dossier (tier set) — skip
        if p.get("tier") is not None: continue
        # Already contacted / passed — skip
        if p.get("status") not in ("not-contacted", "indexed"): continue
        # Must be a thin Delta Fellow / indexed entry
        if not (p.get("delta") or p.get("source")): continue
        # Must have at least one signal worth promoting
        sigs = p.get("signals") or {}
        if not any(sigs.values()): continue
        score = score_for_promotion(p)
        if score < 30: continue  # noise floor
        candidates.append((score, slug, p))

    candidates.sort(reverse=True)
    shown = candidates[:top_n]

    if not shown:
        print(f"{DIM}No promotion candidates. Either all high-signal Delta Fellows are already promoted, or none have signals.{RESET}")
        return

    print(f"\n{BOLD}═══ PROMOTION CANDIDATES — {len(candidates)} thin pages with signals ═══{RESET}")
    print(f"{DIM}Run the full 6-agent SOP on one of these (the 'next Michael Wornow').{RESET}")
    print(f"{DIM}Ask Claude: \"promote SLUG to full dossier\"{RESET}\n")

    for score, slug, p in shown:
        name = p.get("name", slug)
        sigs = [k.replace("phrase_", "").replace("tag_", "") for k, v in (p.get("signals") or {}).items() if v]
        sig_str = ",".join(sigs[:4])
        source = "delta" if p.get("delta") else (p.get("source") or "?")
        indian = "🇮🇳" if p.get("indian") else "  "
        print(f"{BOLD}[{score:3d}]{RESET} {indian} {BOLD}{name:35s}{RESET} {DIM}[{source}]{RESET}")
        ol = (p.get("one_liner") or "")[:90]
        print(f"        {DIM}{ol}{RESET}")
        print(f"        {YELLOW}signals: {sig_str}{RESET}")
        print(f"        {DIM}slug: {slug}{RESET}")
        print()


if __name__ == "__main__":
    main()
