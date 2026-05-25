#!/usr/bin/env python3
"""
import_exceptional100.py
========================
One-shot import of Exceptional 100 (2025) list into outreach_state.json.

These are INDEXED entries, not full dossiers — they don't pollute the daily
queue. They become discoverable via the index browse page and surface in
triage only when there's a real signal (departure, raising, etc.).

What this does:
  - Adds each person to outreach_state.json with status="indexed"
  - Tags: exceptional100, exceptional100-2025, <company-slug>
  - Auto-flags Indian-origin via name heuristic
  - Cross-references with existing dossiers (e.g., Ronak Malde) — adds
    exceptional100 tag to their existing tag list instead of duplicating
  - High-signal subset (frontier-lab researchers + Indian-origin + ex-founders)
    gets tier=2 and category="indexed-hot" so they surface in triage

Run once:
    python3 scripts/import_exceptional100.py

Re-runs are idempotent (won't duplicate; updates fields in place).
"""
from __future__ import annotations
import json
import re
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SOURCE = REPO / "data" / "exceptional100_2025.json"
STATE = REPO / "data" / "outreach_state.json"
PEOPLE_DIR = REPO / "people"

# Indian last-name heuristic. Compiled from observed patterns in repo + the list.
# Not perfect — flag false positives in notes.
INDIAN_LAST_NAMES = {
    "shah", "patel", "singh", "sharma", "doshi", "mathur", "agarwal", "agrawal",
    "gupta", "kumar", "mehta", "iyer", "iyengar", "rao", "reddy", "raghuvanshi",
    "dahiya", "vangipuram", "rajan", "vaid", "priya", "bose", "chishtie",
    "srivastava", "khanna", "arulraj", "mishra", "tiwari", "verma", "joshi",
    "kapoor", "saxena", "nair", "menon", "krishnan", "pillai", "subramanian",
    "ramachandran", "venkatesh", "narayanan", "chakraborty", "bhattacharya",
    "banerjee", "chatterjee", "mukherjee", "goswami", "vohra", "kapila",
    "ravichandran", "vasudevan", "ranganathan", "raghavan", "rane", "doraiswami",
    "doraiswamy", "balasubramanian", "viswanathan", "krishnamoorthy",
}
INDIAN_FIRST_NAMES = {
    "aditi", "aman", "amit", "anika", "anjali", "ankit", "arjun", "ashwin",
    "chetan", "deepak", "dev", "deval", "gaurav", "kunal", "manish", "nikhil",
    "nirav", "pranav", "priya", "rahul", "rajat", "ravi", "rohit", "sachi",
    "shreya", "sneha", "vikram", "vineet", "vivek", "yash", "adi", "adit",
    "pujaa", "puja", "anika", "abhay", "akshay", "kunvar", "mayank", "rishabh",
    "ritvik", "ishaan", "rohil", "samar", "siddharth", "sai", "tanmay",
    "varun", "yashvi", "krish", "krishi", "asha", "kavya", "naveen",
}

# Companies to tag specially (the 20 non-negotiable from CLAUDE.md + close
# adjacents).
TRACKED_COMPANIES = {
    "anthropic", "openai", "google deepmind", "deepmind", "meta", "xai",
    "mistral ai", "cursor", "anysphere", "runway", "midjourney",
    "character ai", "perplexity", "scale ai", "databricks", "together ai",
    "physical intelligence", "nvidia", "nvidia research", "tesla",
    "apple mlr", "anduril", "palantir",
    # extra high-signal
    "cohere", "thinking machines",
}

# Roles that indicate "research scientist" / leadership / founder-track.
HIGH_SIGNAL_ROLE_KEYWORDS = (
    "research scientist", "senior research", "head of", "vp", "director",
    "founding", "co-founded", "founded", "leading", "ml engineer",
    "research engineer", "principal", "tech lead",
)


def slugify(name: str) -> str:
    s = name.lower().strip()
    s = re.sub(r"[\(\)]", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def is_likely_indian(name: str) -> bool:
    parts = re.split(r"\s+", name.lower())
    if not parts:
        return False
    first = parts[0]
    last = parts[-1] if len(parts) > 1 else ""
    return last in INDIAN_LAST_NAMES or first in INDIAN_FIRST_NAMES


def is_high_signal(person: dict) -> bool:
    """Subset that should surface in triage (not just be indexed)."""
    company = person["company"].lower().strip()
    role = person["role"].lower()
    detail = (person.get("detail") or "").lower()
    # At a tracked frontier company
    is_frontier = company in TRACKED_COMPANIES or any(c in company for c in TRACKED_COMPANIES)
    # Research / leadership / founder-track role
    is_senior = any(kw in role for kw in HIGH_SIGNAL_ROLE_KEYWORDS)
    # Previously founded something or working on something concrete
    has_founder_signal = (
        "founded" in detail or "co-founded" in detail or
        "previously" in detail or "built" in detail
    )
    # Indian-origin always counts as elevated
    indian = is_likely_indian(person["name"])
    # Heuristic: at least 2 of the 4
    score = sum([is_frontier, is_senior, has_founder_signal, indian])
    return score >= 2


def existing_dossier_slug(name: str) -> str | None:
    """Check if a dossier already exists for this person."""
    expected = slugify(name) + ".html"
    if (PEOPLE_DIR / expected).exists():
        return expected[:-5]
    return None


def main():
    data = json.loads(SOURCE.read_text())
    state = json.loads(STATE.read_text())
    people_state = state["people"]

    imported_new = 0
    updated_existing = 0
    cross_referenced = 0
    high_signal = 0

    for person in data["people"]:
        name = person["name"]
        company = person["company"]
        role = person["role"]
        detail = person.get("detail", "")
        rank = person["rank"]

        slug = existing_dossier_slug(name)
        is_existing_dossier = slug is not None
        if not slug:
            slug = slugify(name)

        indian = is_likely_indian(name)
        hot = is_high_signal(person)
        company_tag = slugify(company)
        if hot:
            high_signal += 1

        # Tags to add
        new_tags = ["exceptional100", "exceptional100-2025", company_tag]
        if indian:
            new_tags.append("indian")

        if slug in people_state:
            # Either an existing dossier or already-imported entry
            entry = people_state[slug]
            existing_tags = set(entry.get("tags") or [])
            for t in new_tags:
                existing_tags.add(t)
            entry["tags"] = sorted(existing_tags)
            if is_existing_dossier:
                # Existing full dossier — don't touch tier/status, just add tags
                cross_referenced += 1
            else:
                # Already-imported indexed entry — update with latest fields
                entry["name"] = name
                entry["one_liner"] = f"{role} at {company}. {detail}".strip(". ")
                if indian and not entry.get("indian"):
                    entry["indian"] = True
                if hot and entry.get("tier") is None:
                    entry["tier"] = 2
                updated_existing += 1
        else:
            # New entry — create indexed
            people_state[slug] = {
                "name": name,
                "tier": 2 if hot else None,
                "tier_label": "tier-2: tracking (exceptional100)" if hot else None,
                "category": "indexed-hot" if hot else "indexed",
                "tags": new_tags,
                "indian": indian,
                "delta": False,
                "one_liner": f"{role} at {company}. {detail}".strip(". "),
                "signals": {
                    "tag_stealth_founder": False,
                    "tag_founders": False,
                    "phrase_stealth": False,
                    "phrase_departed": False,
                    "phrase_raising": False,
                    "phrase_founded": "founded" in detail.lower() or "co-founded" in detail.lower(),
                },
                "last_git_touch": None,
                "needs_triage": False,
                "emails": [],
                "email_primary": None,
                "email_primary_kind": None,
                "outreach_subject": None,
                "outreach_body_preview": None,
                "gmail_url": None,
                "twitter_handle": None,
                "linkedin_slug": None,
                "github_handle": None,
                # USER-OWNED
                # Hot entries get status=not-contacted so they surface in suggest_urgency.py
                # Low-signal entries stay "indexed" (silent — searchable but won't appear in queue/triage).
                "status": "not-contacted" if hot else "indexed",
                "last_contacted": None,
                "next_action_date": None,
                "response": None,
                "notes": f"Exceptional Capital Exceptional 100 (2025), rank #{rank}",
                "urgency_decay_date": None,
                "urgency_reason": None,
                "channel": None,
                "next_action": None,
                "cluster": "exceptional100",
                "email_override": None,
                "outreach_subject_override": None,
                "outreach_body_override": None,
                # Source attribution
                "source": "exceptional100_2025",
                "source_rank": rank,
            }
            imported_new += 1

    state["last_built"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    STATE.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n")

    print(f"Exceptional 100 (2025) import complete:")
    print(f"  New indexed entries:     {imported_new}")
    print(f"  Updated existing import: {updated_existing}")
    print(f"  Cross-referenced full dossiers: {cross_referenced}")
    print(f"  High-signal (auto-tier-2): {high_signal}")
    print(f"  Total state entries:     {len(people_state)}")


if __name__ == "__main__":
    main()
