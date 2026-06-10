#!/usr/bin/env python3
"""
signals.py
==========
The signal-events engine: dated, sourced, decaying inflection events.

WHY THIS EXISTS
---------------
The old "signals" were six booleans regex-grepped over dossier prose
(build_outreach_state.py) — they measured what the dossier AUTHOR typed,
not what the PERSON did. No dates, no sources, no decay, no velocity —
despite "rate of change" being the fund's #1 stated criterion. The signal
type that cracked Index Robots (a domain registration) had no home at all.

THE MODEL
---------
data/signal_events.json is an APPEND-ONLY log. One event =
    {
      "date":       "2025-09-26",     # when it HAPPENED (estimate ok)
      "observed":   "2026-06-09",     # when we saw it
      "slug":       "raunaq-bhirangi",
      "type":       "domain_registration",   # see TAXONOMY
      "value":      "indexrobots.ai registered (registrant email raunaq@...)",
      "direction":  1,                # +1 toward founding/inflection, -1 away
      "source_url": "https://rdap.org/domain/indexrobots.ai",
      "source_kind":"rdap",           # rdap|edgar|x_bio|x_post|linkedin|lab_page|
                                      # own_site|news|calendar|manual|git
      "confidence": 0.95,
      "note":       "registrant matches personal handle"
    }
Rules: append-only; dedupe on (slug, type, value); manual events are
first-class — research agents should append events IN ADDITION TO prose.

INFLECTION SCORE
----------------
inflection(slug) = Σ  weight(type) × direction × confidence
                      × exp(−ln2 · age_days / half_life(type))
A dated event decays on its half-life; no events ⇒ 0. This is the "how NOW"
axis, orthogonal to tier (how special). today.py adds it to the ranking.

USAGE
-----
    python3 scripts/signals.py list [slug]
    python3 scripts/signals.py scores [--top 20]
    python3 scripts/signals.py add <slug> <type> "<value>" \
        [--date YYYY-MM-DD] [--src URL] [--kind manual] [--conf 0.8] [--neg]
"""
from __future__ import annotations

import json
import math
import sys
from datetime import date, datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EVENTS_FILE = REPO / "data" / "signal_events.json"

# ── TAXONOMY — weight (predictive value for "about to found") + half-life ──
# Ranked from the signal review: filings & domains beat bio changes beat
# engagement noise. Negative types model "moved AWAY from the window".
TAXONOMY: dict[str, dict] = {
    "incorporation_filing":   {"weight": 100, "half_life": 60},   # Form D / SoS
    "domain_registration":    {"weight": 90,  "half_life": 90},
    "departure":              {"weight": 85,  "half_life": 120},  # left tracked co/lab
    "bio_change":             {"weight": 80,  "half_life": 60},   # X/LinkedIn → stealth/building
    "co_departure_cluster":   {"weight": 80,  "half_life": 90},   # computed, ≥2 same org
    "founding_listed":        {"weight": 85,  "half_life": 150},  # résumé/lab page says co-founder
    "hiring_surface":         {"weight": 60,  "half_life": 45},   # careers page / recruiting@
    "repo_burst":             {"weight": 60,  "half_life": 45},   # new org / push burst
    "raise_in_progress":      {"weight": 55,  "half_life": 30},
    "research_shipped":       {"weight": 45,  "half_life": 90},   # launch/post/paper from their co
    "paper_award":            {"weight": 40,  "half_life": 365},  # feeds spike more than inflection
    "engagement_velocity":    {"weight": 30,  "half_life": 30},
    "talk_circuit_shift":     {"weight": 25,  "half_life": 180},
    "calendar_window":        {"weight": 50,  "half_life": 60},   # graduation/vesting, decays past
    "tier_change":            {"weight": 30,  "half_life": 60},   # internal judgment event
    "round_closed":           {"weight": 80,  "half_life": 180},  # NEGATIVE (use --neg)
    "joined_big_lab":         {"weight": 60,  "half_life": 180},  # NEGATIVE
    "manual":                 {"weight": 40,  "half_life": 60},
}

LN2 = math.log(2)


def _now_iso() -> str:
    return date.today().isoformat()


def load_events() -> list[dict]:
    if not EVENTS_FILE.exists():
        return []
    data = json.loads(EVENTS_FILE.read_text())
    return data.get("events", []) if isinstance(data, dict) else data


def save_events(events: list[dict]) -> None:
    EVENTS_FILE.write_text(json.dumps(
        {"_doc": "Append-only signal-event log — see scripts/signals.py. "
                 "Dedupe key: (slug, type, value).",
         "events": events}, indent=2, ensure_ascii=False))


def dedupe_key(e: dict) -> tuple:
    return (e.get("slug"), e.get("type"), e.get("value"))


def append_event(events: list[dict], e: dict) -> bool:
    """Append if not a duplicate. Returns True if added."""
    keys = {dedupe_key(x) for x in events}
    if dedupe_key(e) in keys:
        return False
    events.append(e)
    return True


def _age_days(e: dict, asof: date) -> int:
    d = e.get("date") or e.get("observed") or _now_iso()
    try:
        return max(0, (asof - date.fromisoformat(d[:10])).days)
    except ValueError:
        return 9999


def event_score(e: dict, asof: date | None = None) -> float:
    """Decayed contribution of one event."""
    asof = asof or date.today()
    t = TAXONOMY.get(e.get("type"), TAXONOMY["manual"])
    w = t["weight"]
    hl = t["half_life"]
    conf = float(e.get("confidence", 0.7))
    direction = int(e.get("direction", 1))
    decay = math.exp(-LN2 * _age_days(e, asof) / hl)
    return w * direction * conf * decay


def inflection(slug: str, events: list[dict] | None = None,
               asof: date | None = None) -> float:
    """Sum of decayed event scores for one person. Can be negative."""
    events = events if events is not None else load_events()
    return round(sum(event_score(e, asof) for e in events
                     if e.get("slug") == slug), 1)


def all_inflections(events: list[dict] | None = None) -> dict[str, float]:
    events = events if events is not None else load_events()
    out: dict[str, float] = {}
    for e in events:
        s = e.get("slug")
        if not s:
            continue
        out[s] = out.get(s, 0.0) + event_score(e)
    return {k: round(v, 1) for k, v in out.items()}


# ── CLI ──────────────────────────────────────────────────────────────────

def _cli_add(args: list[str]) -> None:
    if len(args) < 3:
        print("usage: signals.py add <slug> <type> \"<value>\" "
              "[--date D] [--src URL] [--kind K] [--conf F] [--neg] [--note S]")
        sys.exit(1)
    slug, etype, value = args[0], args[1], args[2]
    if etype not in TAXONOMY:
        print(f"unknown type '{etype}'. known: {', '.join(sorted(TAXONOMY))}")
        sys.exit(1)
    opts = args[3:]

    def opt(flag: str, default=None):
        return opts[opts.index(flag) + 1] if flag in opts else default

    e = {
        "date": opt("--date", _now_iso()),
        "observed": _now_iso(),
        "slug": slug,
        "type": etype,
        "value": value,
        "direction": -1 if "--neg" in opts else 1,
        "source_url": opt("--src"),
        "source_kind": opt("--kind", "manual"),
        "confidence": float(opt("--conf", 0.8)),
        "note": opt("--note"),
    }
    events = load_events()
    if append_event(events, e):
        save_events(events)
        print(f"added: {slug} {etype} → inflection now {inflection(slug, events)}")
    else:
        print("duplicate (slug,type,value) — not added")


def _cli_list(args: list[str]) -> None:
    events = load_events()
    slug = args[0] if args else None
    rows = [e for e in events if not slug or e.get("slug") == slug]
    rows.sort(key=lambda e: e.get("date") or "", reverse=True)
    for e in rows:
        sc = event_score(e)
        neg = " (NEG)" if int(e.get("direction", 1)) < 0 else ""
        print(f"  {e.get('date','?'):10s}  {e.get('slug','?'):24s} "
              f"{e.get('type','?'):22s} {sc:+6.1f}{neg}  {e.get('value','')[:70]}")
        if e.get("source_url"):
            print(f"  {'':10s}  {'':24s} src: {e['source_url']}")
    print(f"\n{len(rows)} events")


def _cli_scores(args: list[str]) -> None:
    top = int(args[args.index("--top") + 1]) if "--top" in args else 20
    scores = all_inflections()
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    print(f"{'slug':28s} {'inflection':>10s}")
    for slug, sc in ranked[:top]:
        print(f"{slug:28s} {sc:>10.1f}")


def main() -> None:
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return
    cmd, rest = args[0], args[1:]
    if cmd == "add":
        _cli_add(rest)
    elif cmd == "list":
        _cli_list(rest)
    elif cmd == "scores":
        _cli_scores(rest)
    else:
        print(f"unknown command '{cmd}' — try add | list | scores")
        sys.exit(1)


if __name__ == "__main__":
    main()
