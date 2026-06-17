#!/usr/bin/env python3
"""
build_today.py
==============
Emit data/today.json — the structured feed behind today.html ("The Desk").

WHY THIS EXISTS
---------------
scripts/today.py computes the daily ranking and prints it to a TERMINAL, then
throws it away. The web UI never saw it. This script reuses today.py's exact
scoring (single source of ranking truth — we import it, we don't re-derive it)
and crystallizes the daily action surface into a JSON the static page renders
client-side. No baked staleness: today.html always fetches the latest JSON.

SECTIONS (priority order = the owner's morning sequence, most-perishable first):
  built_at    — wall-clock build time (drives the staleness banner)
  stats       — headline counts
  replies     — status == 'replied', not yet actioned (book the meeting)
  followups   — contacted, no reply, follow-up due (the 2nd touch, currently
                invisible everywhere in the system)
  today5      — top-5 act-now cards (today.py ranking) with why-now / do-this /
                draft / channel links
  signals     — recently-updated dossiers (real "what changed" feed; the richer
                dated/sourced signal-event types land when the signal engine ships)
  triage      — pending-discovery backlog count + the highest-signal names

Usage:
    python3 data/build_today.py
"""
from __future__ import annotations

import json
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
STATE = REPO / "data" / "outreach_state.json"
DISCOVERY = REPO / "data" / "discovery_queue.json"
RECURSIVE = REPO / "data" / "recursive_discoveries.json"
PEOPLE_DIR = REPO / "people"
OUT = REPO / "data" / "today.json"

# Reuse today.py's scoring + link helpers — single source of ranking truth.
sys.path.insert(0, str(REPO / "scripts"))
import today as T  # noqa: E402

FOLLOWUP_DAYS = 7  # contacted N+ days ago with no reply → surface for a 2nd touch
SIGNAL_WINDOW_DAYS = 21  # dossiers touched within this window feed the "fresh" list
SIGNAL_MAX = 8


def slugify(name: str) -> str:
    s = name.lower().strip()
    s = s.replace("&", " and ")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def has_dossier(slug: str) -> bool:
    return (PEOPLE_DIR / f"{slug}.html").exists()


def chips_for(e: dict) -> list[str]:
    """Compress the signals dict + flags into a short, ordered chip list."""
    sigs = e.get("signals") or {}
    tags = set(e.get("tags") or [])
    out: list[str] = []
    if sigs.get("tag_stealth_founder") or sigs.get("phrase_stealth"):
        out.append("stealth")
    if sigs.get("phrase_departed"):
        out.append("departed")
    if sigs.get("tag_founders") or sigs.get("phrase_founded"):
        out.append("founder")
    if sigs.get("phrase_raising"):
        out.append("raising")
    if "yc-s26" in tags:
        out.append("yc-s26")
    if e.get("indian"):
        out.append("indian")
    # de-dupe preserving order
    seen, uniq = set(), []
    for c in out:
        if c not in seen:
            seen.add(c)
            uniq.append(c)
    return uniq[:4]


def window_label(e: dict) -> dict:
    """The 'why-now clock' shown top-right of a card."""
    decay = e.get("urgency_decay_date")
    if decay:
        d = T.days_until(decay)
        if d < 0:
            return {"text": f"window closed {abs(d)}d ago", "kind": "closed"}
        return {"text": f"closes {decay}", "kind": "soon" if d <= 21 else "open"}
    sigs = e.get("signals") or {}
    if sigs.get("phrase_stealth") or sigs.get("tag_stealth_founder"):
        return {"text": "pre-name · open", "kind": "open"}
    if sigs.get("phrase_departed"):
        return {"text": "recently departed", "kind": "open"}
    return {"text": "open", "kind": "open"}


def clamp(s: str | None, n: int) -> str:
    s = (s or "").strip()
    if len(s) <= n:
        return s
    cut = s[:n].rsplit(" ", 1)[0]
    return cut + "…"


def dossier_path(slug: str) -> str | None:
    return f"people/{slug}.html" if has_dossier(slug) else None


def days_ago_date(iso: str | None) -> int:
    """Days since a bare YYYY-MM-DD (today.days_since only handles tz-aware ts)."""
    if not iso:
        return 9999
    try:
        return max(0, (date.today() - date.fromisoformat(iso[:10])).days)
    except ValueError:
        return 9999


def primary_link(e: dict) -> dict | None:
    """The single best reach-out link for the card's channel.
    Label is derived from the actual URL (never assume profile==twitter)."""
    links = T.channel_compose_links("", e, None, None)
    if not links:
        return None
    _label, url = links[0]
    u = url.lower()
    if "twitter.com" in u or "x.com" in u:
        label = f"𝕏 @{e.get('twitter_handle')}" if e.get("twitter_handle") else "𝕏 DM"
    elif "linkedin.com" in u:
        label = f"in/{e.get('linkedin_slug')}" if e.get("linkedin_slug") else "LinkedIn"
    elif "mail.google" in u or u.startswith("mailto"):
        label = "✉ email"
    else:
        label = "reach"
    return {"label": label, "url": url}


def build_card(slug: str, e: dict) -> dict:
    sc = T.score_components(e, slug)
    subject = e.get("outreach_subject_override") or e.get("outreach_subject")
    body = e.get("outreach_body_override") or e.get("outreach_body_preview")
    return {
        "slug": slug,
        "name": e.get("name", slug),
        "tier": e.get("tier"),
        "score": sc["total"],
        "chips": chips_for(e),
        "window": window_label(e),
        "why_now": clamp(e.get("urgency_reason"), 260) or clamp(e.get("one_liner"), 200),
        "do_this": clamp(e.get("next_action"), 200),
        "channel": e.get("channel"),
        "draft": {"subject": subject, "body": body} if (subject or body) else None,
        "link": primary_link(e),
        "twitter": e.get("twitter_handle"),
        "linkedin": e.get("linkedin_slug"),
        "email": T.resolve_email(e)[0],
        "dossier": dossier_path(slug),
    }


def build_followups(people: dict) -> list[dict]:
    today = T.today_iso()
    out = []
    for slug, e in people.items():
        if e.get("status") != "contacted" or e.get("response"):
            continue
        nad = e.get("next_action_date")
        lc = e.get("last_contacted")
        due = (nad and nad <= today) or (lc and T.days_since(lc) >= FOLLOWUP_DAYS)
        if not due:
            continue
        ref = nad or lc
        overdue = T.days_until(nad) * -1 if nad else T.days_since(lc)
        out.append({
            "slug": slug,
            "name": e.get("name", slug),
            "tier": e.get("tier"),
            "channel": e.get("channel") or "?",
            "last_contacted": lc,
            "overdue_days": max(0, overdue),
            "touches": len(e.get("channels_attempted") or []),
            "dossier": dossier_path(slug),
            "link": primary_link(e),
        })
    out.sort(key=lambda x: ((x["tier"] if x["tier"] is not None else 9), -x["overdue_days"]))
    return out


def build_replies(people: dict) -> list[dict]:
    out = []
    for slug, e in people.items():
        if e.get("status") != "replied":
            continue
        out.append({
            "slug": slug,
            "name": e.get("name", slug),
            "tier": e.get("tier"),
            "response": clamp(e.get("response"), 160),
            "channel": e.get("channel"),
            "dossier": dossier_path(slug),
        })
    out.sort(key=lambda x: (x["tier"] if x["tier"] is not None else 9))
    return out


def build_signals(people: dict) -> list[dict]:
    """The fresh-signals feed. Primary source: the signal-events engine
    (data/signal_events.json via scripts/signals.py) — dated, sourced,
    decay-scored events. Fallback filler: recently-updated dossiers."""
    rows: list[dict] = []
    try:
        from signals import load_events, event_score
        for ev in load_events():
            slug = ev.get("slug") or ""
            d = days_ago_date(ev.get("observed") or ev.get("date"))
            if d > SIGNAL_WINDOW_DAYS:
                continue
            p = people.get(slug, {})
            sc = event_score(ev)
            neg = int(ev.get("direction", 1)) < 0
            rows.append({
                "slug": slug,
                "name": p.get("name", slug),
                "tier": p.get("tier"),
                "date": (ev.get("date") or "")[:10],
                "days_ago": d,
                "type": (ev.get("type") or "event").replace("_", " ") + (" (neg)" if neg else ""),
                "text": clamp(ev.get("value"), 150),
                "source_url": ev.get("source_url"),
                "source_kind": ev.get("source_kind"),
                "delta": round(sc),
                "hot": abs(sc) >= 40,
                "has_dossier": has_dossier(slug),
            })
    except Exception:
        pass
    rows.sort(key=lambda x: (x["days_ago"], -abs(x.get("delta") or 0)))

    if len(rows) < SIGNAL_MAX:  # fill with dossier-update recency
        have = {r["slug"] for r in rows}
        fillers = []
        for slug, e in people.items():
            if slug in have or not has_dossier(slug):
                continue
            gt = e.get("last_git_touch")
            d = T.days_since(gt)
            if d > SIGNAL_WINDOW_DAYS:
                continue
            fillers.append({
                "slug": slug, "name": e.get("name", slug), "tier": e.get("tier"),
                "date": (gt or "")[:10], "days_ago": d, "type": "dossier updated",
                "text": clamp(e.get("urgency_reason") or e.get("one_liner"), 150),
                "source_url": None, "source_kind": "git", "delta": None,
                "hot": False,
            })
        fillers.sort(key=lambda x: x["days_ago"])
        rows.extend(fillers[: SIGNAL_MAX - len(rows)])
    return rows[:SIGNAL_MAX]


def build_triage() -> dict:
    pending, p0 = [], []
    seen = set()

    def ingest(items, name_key, status_key, p0_pred):
        for x in items:
            if not isinstance(x, dict):
                continue
            if (x.get(status_key) or "pending") != "pending":
                continue
            name = x.get(name_key) or x.get("name")
            if not name:
                continue
            slug = slugify(name)
            if has_dossier(slug) or slug in seen:
                continue  # reconcile: already researched → not really pending
            seen.add(slug)
            pending.append(name)
            if p0_pred(x):
                ctx = x.get("context") or x.get("one_liner") or x.get("spike_signal") or ""
                p0.append({"name": name, "note": clamp(ctx, 90)})

    try:
        dq = json.loads(DISCOVERY.read_text())
        items = dq if isinstance(dq, list) else dq.get("discoveries", dq.get("queue", []))
        ingest(items, "name", "status", lambda x: bool(x.get("departure_signal")))
    except Exception:
        pass
    try:
        rd = json.loads(RECURSIVE.read_text())["discoveries"]
        ingest(rd, "name", "status", lambda x: str(x.get("priority", "")).upper() in ("P0", "P1"))
    except Exception:
        pass

    return {"pending": len(pending), "highlights": p0[:6]}


def build_pipeline(people: dict) -> dict:
    """The outreach funnel — status counts + the in-flight (contacted, awaiting
    reply) list. Folds the retired queue.html status-board into The Desk."""
    from collections import Counter
    counts = Counter((e.get("status") or "not-contacted") for e in people.values())
    in_flight = []
    for slug, e in people.items():
        if e.get("status") == "contacted" and not e.get("response"):
            lc = e.get("last_contacted")
            in_flight.append({
                "slug": slug, "name": e.get("name", slug), "tier": e.get("tier"),
                "channel": e.get("channel"), "last_contacted": lc,
                "days_since": days_ago_date(lc) if lc else None,
                "dossier": dossier_path(slug),
            })
    in_flight.sort(key=lambda x: ((x["tier"] if x["tier"] is not None else 9),
                                  -(x["days_since"] or 0)))
    order = ["not-contacted", "queued", "contacted", "replied", "passed", "indexed"]
    funnel = [{"status": s, "n": counts.get(s, 0)} for s in order if counts.get(s, 0)]
    for s, n in counts.items():
        if s not in order:
            funnel.append({"status": s, "n": n})
    return {"funnel": funnel, "in_flight": in_flight, "total": len(people)}


def main():
    state = json.loads(STATE.read_text())
    people = state["people"]

    eligible = [(s, e) for s, e in people.items() if T.is_eligible(e)]
    ranked = sorted(eligible, key=lambda x: T.priority(x[1], x[0]), reverse=True)
    today5 = [build_card(s, e) for s, e in ranked[:5]]

    n_t0 = sum(1 for e in people.values() if e.get("tier") == 0)
    n_t1 = sum(1 for e in people.values() if e.get("tier") == 1)
    in_flight = sum(1 for e in people.values() if e.get("status") in ("queued", "contacted"))

    out = {
        "built_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "date": date.today().isoformat(),
        "stats": {"t0": n_t0, "t1": n_t1, "in_flight": in_flight,
                  "pool": len(ranked)},
        "pipeline": build_pipeline(people),
        "replies": build_replies(people),
        "followups": build_followups(people),
        "today5": today5,
        "signals": build_signals(people),
        "triage": build_triage(),
    }
    # Atomic write (temp + rename) so The Desk never fetches a half-written file.
    _tmp = OUT.with_name(OUT.name + ".tmp")
    _tmp.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    _tmp.replace(OUT)
    fu = len(out["followups"])
    print(f"today.json: {len(today5)} act-now · {fu} follow-ups due · "
          f"{len(out['replies'])} replies · {out['triage']['pending']} triage pending")


if __name__ == "__main__":
    main()
