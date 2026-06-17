#!/usr/bin/env python3
"""
mark.py
=======
Fast status update for outreach entries. One-line command, no editing JSON.

Usage:
    python3 scripts/mark.py <slug> <status> [note]
    python3 scripts/mark.py <slug> snooze <days>

Status vocabulary:
    sent CHANNEL [note] → status=contacted via CHANNEL, +14d follow-up
                          channel: twitter|email|linkedin|slack|whatsapp|warm-intro|meeting
    replied [note]   → status=replied, last_contacted=today
    meeting [note]   → status=replied + notes "meeting booked"
    passed [note]    → status=passed (drops out of all queues)
    snooze N         → next_action_date = today + N days (status unchanged)
    unsnooze         → next_action_date = None
    reset            → status=not-contacted, last_contacted=None
    email ADDR       → set email_override (beats auto-extracted)
    subject S        → set outreach_subject_override
    touch CHANNEL    → record an attempt without changing status (DM bounces, etc.)

Multi-channel tracking: every `sent` and `touch` appends to channels_attempted
list with {channel, date, note}. Lets you see conversion-by-channel later.

Examples:
    python3 scripts/mark.py alex-shan sent twitter "DM'd referencing Osiris"
    python3 scripts/mark.py ronak-malde sent slack "MIT institute channel"
    python3 scripts/mark.py jennifer-zhai sent whatsapp "via Aditya intro"
    python3 scripts/mark.py alex-shan replied "wants to chat next week"
    python3 scripts/mark.py mayank-mishra snooze 7
    python3 scripts/mark.py kawin-ethayarajh passed
    python3 scripts/mark.py devvrit-khatri email devvrit@reflection.ai
    python3 scripts/mark.py shivani-poddar touch twitter "DM bounced, will retry"
"""
from __future__ import annotations
import json
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
STATE = REPO / "data" / "outreach_state.json"
BUILD_TODAY = REPO / "data" / "build_today.py"
BUILD_DIR = REPO / "data" / "build_directory.py"

FOLLOWUP_DAYS_AFTER_SEND = 14


def rerender_panel():
    """Auto-rebuild The Desk (today.json) AND the directory table data
    (directory.json) after status changes, so both views stay live.

    Silent on success; surfaces errors. Skip with MARK_NO_RENDER=1.
    """
    import os
    if os.environ.get("MARK_NO_RENDER") == "1":
        return
    for script, label in ((BUILD_TODAY, "desk"), (BUILD_DIR, "directory")):
        try:
            subprocess.run(
                ["python3", str(script)],
                cwd=REPO, capture_output=True, text=True, check=True,
            )
        except subprocess.CalledProcessError as e:
            print(f"WARN: {label} re-render failed: {e.stderr[:200]}", file=sys.stderr)
        except FileNotFoundError:
            pass  # builder missing — silently skip


def usage():
    print(__doc__)
    sys.exit(1)


def main():
    if len(sys.argv) < 3:
        usage()

    slug = sys.argv[1]
    action = sys.argv[2]
    extra = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else ""

    state = json.loads(STATE.read_text())
    people = state["people"]

    if slug not in people:
        print(f"ERROR: slug '{slug}' not in state. Try: python3 scripts/today.py --all | grep <name>", file=sys.stderr)
        sys.exit(1)

    p = people[slug]
    today = date.today().isoformat()

    if action == "sent":
        # parse: sent CHANNEL [note] — first extra token is channel
        parts = extra.split(maxsplit=1) if extra else []
        channel = parts[0].lower() if parts else (p.get("channel") or "email")
        note = parts[1] if len(parts) > 1 else ""
        VALID_CHANNELS = {"twitter", "email", "linkedin", "slack", "whatsapp", "warm-intro", "meeting", "x", "dm", "telegram", "signal"}
        if channel not in VALID_CHANNELS:
            print(f"WARNING: channel '{channel}' not in {VALID_CHANNELS}. Recording anyway.", file=sys.stderr)
        p["status"] = "contacted"
        p["last_contacted"] = today
        p["next_action_date"] = (date.today() + timedelta(days=FOLLOWUP_DAYS_AFTER_SEND)).isoformat()
        # Multi-channel history
        attempts = p.get("channels_attempted") or []
        attempts.append({"channel": channel, "date": today, "note": note})
        p["channels_attempted"] = attempts
        if note:
            p["notes"] = (p.get("notes") or "") + f"\n[{today}] sent via {channel}: {note}"
        else:
            p["notes"] = (p.get("notes") or "") + f"\n[{today}] sent via {channel}"
        print(f"✓ {slug} marked sent via {channel}. Follow up by {p['next_action_date']}.")

    elif action == "replied":
        p["status"] = "replied"
        p["last_contacted"] = today
        p["response"] = extra or "replied"
        if extra:
            p["notes"] = (p.get("notes") or "") + f"\n[{today}] reply: {extra}"
        print(f"✓ {slug} marked replied.")

    elif action == "meeting":
        p["status"] = "replied"
        p["last_contacted"] = today
        p["notes"] = (p.get("notes") or "") + f"\n[{today}] meeting booked: {extra}"
        print(f"✓ {slug} marked meeting booked.")

    elif action == "passed":
        p["status"] = "passed"
        if extra:
            p["notes"] = (p.get("notes") or "") + f"\n[{today}] passed: {extra}"
        print(f"✓ {slug} marked passed — drops from queue.")

    elif action == "snooze":
        try:
            days = int(extra)
        except ValueError:
            print("ERROR: snooze needs integer days. e.g. `mark.py alex-shan snooze 7`", file=sys.stderr)
            sys.exit(1)
        new_date = (date.today() + timedelta(days=days)).isoformat()
        p["next_action_date"] = new_date
        print(f"✓ {slug} snoozed until {new_date}.")

    elif action == "unsnooze":
        p["next_action_date"] = None
        print(f"✓ {slug} unsnoozed.")

    elif action == "reset":
        p["status"] = "not-contacted"
        p["last_contacted"] = None
        p["next_action_date"] = None
        print(f"✓ {slug} reset to not-contacted.")

    elif action == "email":
        if not extra or "@" not in extra:
            print("ERROR: provide a valid email. e.g. `mark.py alex-shan email alex@stealthco.com`", file=sys.stderr)
            sys.exit(1)
        p["email_override"] = extra.strip()
        print(f"✓ {slug} email override set to {extra.strip()}")

    elif action == "subject":
        if not extra:
            print("ERROR: provide subject. e.g. `mark.py alex-shan subject 'Re: $32M round'`", file=sys.stderr)
            sys.exit(1)
        p["outreach_subject_override"] = extra
        print(f"✓ {slug} subject override set.")

    elif action == "touch":
        # Record an outreach attempt without flipping status (DM bounced, no response yet, etc.)
        parts = extra.split(maxsplit=1) if extra else []
        if not parts:
            print("ERROR: touch requires a channel. e.g. `mark.py SLUG touch twitter \"DM bounced\"`", file=sys.stderr)
            sys.exit(1)
        channel = parts[0].lower()
        note = parts[1] if len(parts) > 1 else ""
        attempts = p.get("channels_attempted") or []
        attempts.append({"channel": channel, "date": today, "note": note, "kind": "touch"})
        p["channels_attempted"] = attempts
        p["notes"] = (p.get("notes") or "") + f"\n[{today}] touch via {channel}: {note}"
        print(f"✓ {slug} touch recorded via {channel}. Status unchanged.")

    else:
        print(f"ERROR: unknown action '{action}'.")
        usage()

    STATE.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n")
    rerender_panel()


if __name__ == "__main__":
    main()
