#!/usr/bin/env python3
"""
build_directory.py
==================
Build data/directory.json — the data the interactive table in index.html
renders from.

SINGLE SOURCE OF TRUTH for everything volatile = data/outreach_state.json
(regenerated daily by build_outreach_state.py). This script merges in the
curated short display text from data/blurbs.json (slug -> {role, spike}),
which is the ONE stable home for the hand-written blurbs.

Because the table reads from this derived artifact and we regenerate it in
the morning ritual + after every mark.py, the table never goes stale:
status / last_contacted / next_action / tier all reflect live state.

Only people who have a dossier page (people/<slug>.html) are included, so
every row is clickable.

Usage:
    python3 data/build_directory.py
"""
from __future__ import annotations
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
STATE = REPO / "data" / "outreach_state.json"
BLURBS = REPO / "data" / "blurbs.json"
PEOPLE = REPO / "people"
OUT = REPO / "data" / "directory.json"

# "researched: YYYY-MM-DD" in a dossier footer = when the PERSON was added.
# This is the honest recency signal for the Feed (vs. git-commit time, which a
# typo-fix re-floats). Fall back to git-touch when a dossier has no stamp.
_RESEARCHED_RE = re.compile(r"researched:\s*(\d{4}-\d{2}-\d{2})")
_added_cache: dict[str, str] = {}


def added_date(slug: str, fallback: str) -> str:
    if slug in _added_cache:
        return _added_cache[slug]
    val = fallback
    try:
        m = _RESEARCHED_RE.search((PEOPLE / f"{slug}.html").read_text())
        if m:
            val = m.group(1)
    except OSError:
        pass
    _added_cache[slug] = val
    return val


def signal_list(sig: dict | None) -> list[str]:
    """Compress the signals dict into short human labels."""
    if not sig:
        return []
    out = []
    if sig.get("tag_stealth_founder") or sig.get("phrase_stealth"):
        out.append("stealth")
    if sig.get("phrase_departed"):
        out.append("departed")
    if sig.get("phrase_raising"):
        out.append("raising")
    if sig.get("phrase_founded") or sig.get("tag_founders"):
        out.append("founder")
    # de-dupe preserving order
    seen = set()
    return [x for x in out if not (x in seen or seen.add(x))]


def main():
    state = json.loads(STATE.read_text())["people"]
    blurbs = json.loads(BLURBS.read_text()) if BLURBS.exists() else {}

    rows = []
    for slug, e in state.items():
        if not (PEOPLE / f"{slug}.html").exists():
            continue  # only clickable rows
        b = blurbs.get(slug, {})
        role = b.get("role") or e.get("one_liner") or ""
        spike = b.get("spike") or ""
        rows.append({
            "slug": slug,
            "name": e.get("name") or slug,
            "tier": e.get("tier"),                       # 0..3 or null
            "role": role,
            "spike": spike,
            "tags": e.get("tags") or [],
            "cluster": e.get("cluster"),
            "signals": signal_list(e.get("signals")),
            "status": e.get("status") or "not-contacted",
            "last_contacted": e.get("last_contacted"),
            "next_action_date": e.get("next_action_date"),
            "updated": (e.get("last_git_touch") or "")[:10],   # YYYY-MM-DD (last edit)
            "added": added_date(slug, (e.get("last_git_touch") or "")[:10]),  # researched date
            "channel": e.get("channel"),
            "twitter": e.get("twitter_handle"),
            "linkedin": e.get("linkedin_slug"),
            "email": e.get("email_primary"),
            "gmail_url": e.get("gmail_url"),
            "indian": bool(e.get("indian")),
            "delta": bool(e.get("delta")),
            "needs_triage": bool(e.get("needs_triage")),
            "urgency": bool(e.get("urgency_reason")),
        })

    # stable default order: tier asc (T0 first, untiered last), then updated desc
    def sort_key(r):
        t = r["tier"]
        t = t if isinstance(t, int) else 9
        return (t, "" if not r["updated"] else _neg_date(r["updated"]))
    rows.sort(key=sort_key)

    payload = {
        "generated": _today(),
        "count": len(rows),
        "people": rows,
    }
    # Atomic write: a browser fetching directory.json mid-rebuild must never
    # see a half-written file (caused a transient partial-table render).
    _tmp = OUT.with_name(OUT.name + ".tmp")
    _tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=1))
    _tmp.replace(OUT)

    # quick console summary
    from collections import Counter
    tiers = Counter("T" + str(r["tier"]) if isinstance(r["tier"], int) else "—" for r in rows)
    print(f"directory.json: {len(rows)} clickable people")
    print("  tiers:", dict(sorted(tiers.items())))
    print("  with urgency:", sum(1 for r in rows if r["urgency"]))


def _neg_date(d: str) -> str:
    # invert a YYYY-MM-DD so ascending sort puts newest first
    try:
        y, m, day = d.split("-")
        return f"{9999-int(y):04d}{99-int(m):02d}{99-int(day):02d}"
    except Exception:
        return "99999999"


def _today() -> str:
    # build_outreach_state stamps dates; reuse the state file's mtime-free
    # approach by reading the newest 'last_git_touch'. Falls back to empty.
    try:
        state = json.loads(STATE.read_text())["people"]
        ds = sorted((e.get("last_git_touch") or "")[:10] for e in state.values())
        return ds[-1] if ds and ds[-1] else ""
    except Exception:
        return ""


if __name__ == "__main__":
    main()
