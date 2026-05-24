#!/usr/bin/env python3
"""
mark.py
=======
Fast status update for outreach entries. One-line command, no editing JSON.

Usage:
    python3 scripts/mark.py <slug> <status> [note]
    python3 scripts/mark.py <slug> snooze <days>

Status vocabulary:
    sent       → status=contacted, last_contacted=today, next_action_date=+14d
    replied    → status=replied, last_contacted=today
    meeting    → status=replied + notes "meeting booked"
    passed     → status=passed (drops out of all queues)
    snooze N   → next_action_date = today + N days (status unchanged)
    unsnooze   → next_action_date = None
    reset      → status=not-contacted, last_contacted=None
    email ADDR → set email_override (beats auto-extracted)
    subject S  → set outreach_subject_override

Examples:
    python3 scripts/mark.py alex-shan sent
    python3 scripts/mark.py alex-shan replied "wants to chat next week"
    python3 scripts/mark.py mayank-mishra snooze 7
    python3 scripts/mark.py kawin-ethayarajh passed
    python3 scripts/mark.py devvrit-khatri email devvrit@reflection.ai
    python3 scripts/mark.py alex-shan subject "Quick Q on Judgment"
"""
from __future__ import annotations
import json
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
STATE = REPO / "data" / "outreach_state.json"
BUILD_VIEW = REPO / "data" / "build_outreach_view.py"

FOLLOWUP_DAYS_AFTER_SEND = 14


def rerender_panel():
    """Auto-rebuild the index.html outreach panel after status changes.

    Silent on success; surfaces errors. Skip with MARK_NO_RENDER=1.
    """
    import os
    if os.environ.get("MARK_NO_RENDER") == "1":
        return
    try:
        subprocess.run(
            ["python3", str(BUILD_VIEW)],
            cwd=REPO, capture_output=True, text=True, check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"WARN: index re-render failed: {e.stderr[:200]}", file=sys.stderr)
    except FileNotFoundError:
        pass  # build_outreach_view.py missing — silently skip


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
        p["status"] = "contacted"
        p["last_contacted"] = today
        p["next_action_date"] = (date.today() + timedelta(days=FOLLOWUP_DAYS_AFTER_SEND)).isoformat()
        if extra:
            p["notes"] = (p.get("notes") or "") + f"\n[{today}] sent: {extra}"
        print(f"✓ {slug} marked sent. Follow up by {p['next_action_date']}.")

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

    else:
        print(f"ERROR: unknown action '{action}'.")
        usage()

    STATE.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n")
    rerender_panel()


if __name__ == "__main__":
    main()
