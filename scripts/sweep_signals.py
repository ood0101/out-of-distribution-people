#!/usr/bin/env python3
"""
sweep_signals.py
================
First automated signal feed: RDAP domain checks + SEC EDGAR Form-D search
for the active watch set. Appends events to data/signal_events.json
(dedupe-safe — re-running never double-counts).

WHY THESE TWO FIRST
-------------------
They are the exact signal types behind the system's two best recent wins,
and both are free, unauthenticated public APIs:
  - RDAP (rdap.org): a personal email on a NOVEL domain → the domain's
    registration date ≈ the stealth company's founding window. This is the
    generalized "raunaq@indexrobots.ai → Index Robots (reg 2025-09-26)" move.
  - EDGAR full-text search: a Form D names the person → a raise is closing.
    (CA SoS would be next; it needs scraping, EDGAR doesn't.)

SCOPE (bounded, polite)
-----------------------
Targets = every T0, plus T1s with a stealth signal — ~25 people, a handful
of HTTP calls each, 0.4s spacing. Common mail/edu/big-co domains skipped.
EDGAR hits for common names are noisy → recorded at confidence 0.6 with the
filing URL so the owner verifies before acting.

Usage:
    python3 scripts/sweep_signals.py            # sweep + append events
    python3 scripts/sweep_signals.py --dry-run  # show what would be added
"""
from __future__ import annotations

import json
import sys
import time
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
STATE = REPO / "data" / "outreach_state.json"

sys.path.insert(0, str(REPO / "scripts"))
from signals import load_events, append_event, save_events  # noqa: E402

UA = {"User-Agent": "ood-people-research/1.0 (subscriptions@boldcap.com)"}
TIMEOUT = 10
SPACING = 0.4  # seconds between calls — be polite

# Domains that tell us nothing about a stealth company.
BORING_DOMAINS = {
    "gmail.com", "googlemail.com", "yahoo.com", "outlook.com", "hotmail.com",
    "icloud.com", "me.com", "fastmail.com", "fastmail.fm", "proton.me",
    "protonmail.com", "hey.com", "pm.me",
    "google.com", "openai.com", "anthropic.com", "deepmind.com", "meta.com",
    "fb.com", "nvidia.com", "apple.com", "microsoft.com", "x.ai", "tesla.com",
}


def is_boring(domain: str) -> bool:
    d = domain.lower()
    if d in BORING_DOMAINS:
        return True
    # academic / government
    return d.endswith((".edu", ".ac.uk", ".ac.in", ".gov", ".gov.in", ".mil"))


def get_json(url: str) -> dict | None:
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return json.loads(r.read().decode("utf-8", "replace"))
    except Exception:
        return None


def rdap_registration(domain: str) -> tuple[str | None, bool]:
    """Return (registration_date, exists). rdap.org redirects to the right registry."""
    data = get_json(f"https://rdap.org/domain/{urllib.parse.quote(domain)}")
    if not data:
        return None, False
    for ev in data.get("events", []):
        if ev.get("eventAction") in ("registration", "created"):
            return (ev.get("eventDate") or "")[:10], True
    return None, True  # exists, registration date not exposed


def edgar_form_d(name: str) -> list[dict]:
    """SEC EDGAR full-text search, Form D only. Returns raw hits (may be noisy)."""
    q = urllib.parse.quote(f'"{name}"')
    data = get_json(f"https://efts.sec.gov/LATEST/search-index?q={q}&forms=D")
    if not data:
        return []
    return (data.get("hits") or {}).get("hits") or []


def watch_set(people: dict) -> list[tuple[str, dict]]:
    out = []
    for slug, e in people.items():
        tier = e.get("tier")
        sigs = e.get("signals") or {}
        stealthy = sigs.get("tag_stealth_founder") or sigs.get("phrase_stealth")
        if tier == 0 or (tier == 1 and stealthy):
            out.append((slug, e))
    return out


def main() -> None:
    dry = "--dry-run" in sys.argv
    people = json.loads(STATE.read_text())["people"]
    targets = watch_set(people)
    events = load_events()
    known_domains = {
        (e.get("value") or "").split(" ")[0]
        for e in events if e.get("type") == "domain_registration"
    }
    added = 0
    edgar_review: list[tuple] = []
    print(f"sweep: {len(targets)} people in watch set (T0 + stealth-T1)")

    for slug, e in targets:
        name = e.get("name", slug)

        # ── RDAP: novel domains in their email set ──
        domains = {addr.split("@", 1)[1].lower()
                   for addr in (e.get("emails") or []) if "@" in addr}
        for dom in sorted(domains):
            if is_boring(dom) or any(dom in k for k in known_domains):
                continue
            reg_date, exists = rdap_registration(dom)
            time.sleep(SPACING)
            if not exists:
                continue
            ev = {
                "date": reg_date or date.today().isoformat(),
                "observed": date.today().isoformat(),
                "slug": slug,
                "type": "domain_registration",
                "value": f"{dom} registered{' ' + reg_date if reg_date else ''} "
                         f"(novel domain in {name}'s contact emails)",
                "direction": 1,
                "source_url": f"https://rdap.org/domain/{dom}",
                "source_kind": "rdap",
                "confidence": 0.85 if reg_date else 0.7,
                "note": "auto: sweep_signals.py RDAP check",
            }
            if dry:
                print(f"  [dry] {slug}: domain_registration {dom} ({reg_date})")
            elif append_event(events, ev):
                added += 1
                print(f"  + {slug}: domain_registration {dom} ({reg_date})")

        # ── EDGAR Form D (T0 only) — PRINT FOR REVIEW, never auto-append.
        # A Form D is a strong raise signal, but full-text match on a bare
        # NAME is too noisy to score (it hit a generic PE fund for "Scott
        # Reed"). Surface candidates; the owner adds a real one by hand via
        # `signals.py add <slug> incorporation_filing "..." --src <url>`.
        if e.get("tier") == 0:
            hits = edgar_form_d(name)
            time.sleep(SPACING)
            for h in hits[:2]:
                src = h.get("_source") or {}
                fdate = (src.get("file_date") or "")[:10]
                co = (src.get("display_names") or ["?"])[0]
                edgar_review.append((slug, name, co, fdate))

    if not dry:
        save_events(events)
    if edgar_review:
        print("\nEDGAR Form-D candidates (REVIEW — not scored; name-match only):")
        for slug, name, co, fdate in edgar_review:
            print(f"  ? {slug}: '{name}' appears in Form D → {co} ({fdate})")
        print("  add a real one: signals.py add <slug> incorporation_filing \"...\" --src <url> --kind edgar")
    print(f"\ndone: {added} new events" + (" (dry run — nothing written)" if dry else ""))


if __name__ == "__main__":
    main()
