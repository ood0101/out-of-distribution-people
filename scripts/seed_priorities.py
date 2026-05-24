#!/usr/bin/env python3
"""
seed_priorities.py
==================
One-shot script to seed urgency fields for the top-priority entries in
data/outreach_state.json.

Run once: `python3 scripts/seed_priorities.py`

This populates urgency_decay_date, urgency_reason, channel, next_action,
and cluster for the entries you actually want to act on this week. The
build_outreach_state.py script preserves these across rebuilds.

After seeding, re-run `python3 scripts/today.py` to get the daily 5.
"""
from __future__ import annotations
import json
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
STATE = REPO / "data" / "outreach_state.json"

# ---- The seed list. Edit this when priorities change. ----
# Format: slug -> dict of urgency fields. Missing fields stay None.
SEED = {
    # ─── T0 — REACH OUT THIS WEEK (windows actively closing) ──────────────
    "alex-shan": {
        "urgency_reason": "Just raised $32M (May 12). Post-funding window — ~3 weeks before hiring ramp consumes him.",
        "urgency_decay_date": "2026-06-15",
        "channel": "twitter",
        "next_action": "Congrats DM ref Osiris paper as Manning-lab prelude to judgeval",
        "cluster": "agent-infra",
    },
    "mayank-mishra": {
        "urgency_reason": "LinkedIn shows 'Stealth AI Startup' alongside Berkeley PhD — active signal.",
        "urgency_decay_date": "2026-06-21",
        "channel": "twitter",
        "next_action": "DM @MayankMish98 — ask what he's building, ref lm-engine",
        "cluster": "architecture",
    },
    "rohil-badkundri": {
        "urgency_reason": "'Building' stealth post-EvolutionaryScale → CZ Biohub acquisition. Pre-formation mode.",
        "urgency_decay_date": "2026-07-01",
        "channel": "warm-intro",
        "next_action": "Warm intro via Roshan Rao or direct; ref ESM3 clinical-trial angle",
        "cluster": "ai-bio",
    },
    "michael-wornow": {
        "urgency_reason": "Kinetic Systems actively hiring → in build/fundraise mode.",
        "urgency_decay_date": None,
        "channel": "email",
        "next_action": "Send 2-3 specific candidates from pipeline (offer value first)",
        "cluster": "healthcare-ai",
    },
    "devvrit-khatri": {
        "urgency_reason": "Joining Reflection AI ($2B) — vesting cliff begins immediately. Last pre-lockup window.",
        "urgency_decay_date": "2026-06-30",
        "channel": "email",
        "next_action": "Meet before Reflection start date; ref ScaleRL co-authorship pattern",
        "cluster": "scalerl",
    },

    # ─── T1 — RELATIONSHIP-BUILD (open-ended, monthly cadence) ────────────
    "brandon-wang": {
        "urgency_reason": "Recent departure Cartesia → onepot AI. IMO Gold + 3x USAMO + Putnam solo solver.",
        "urgency_decay_date": None,
        "channel": "twitter",
        "next_action": "DM @fluorane — H-Net dynamic chunking question + chemistry SMILES angle",
        "cluster": "architecture",
    },
    "sukjun-hwang": {
        "urgency_reason": "CMU mid-PhD under Albert Gu. Tri Dao reference class. Architecture frontier.",
        "urgency_decay_date": None,
        "channel": "email",
        "next_action": "Cold email ref H-Net robustness gap (42.8 vs 22.2) + EMA smoothing trick",
        "cluster": "architecture",
    },
    "kunvar-thaman": {
        "urgency_reason": "Solo ICML 2026. Indian. Standard Intelligence ML eng + incoming MIT PhD. Rare profile.",
        "urgency_decay_date": None,
        "channel": "email",
        "next_action": "Email kunvar@mechinterp.com ref RHB +13.3pp DeepSeek sibling-comparison",
        "cluster": "mech-interp",
    },
    "kanishk-gandhi": {
        "urgency_reason": "Stanford Goodman lab. Lead researcher on Countdown task R1-Zero used. IIT Kanpur.",
        "urgency_decay_date": None,
        "channel": "twitter",
        "next_action": "DM @gandhikanishk ref Cognitive Behaviors incorrect-priming finding",
        "cluster": "reasoning",
    },
    "lovish-madaan": {
        "urgency_reason": "Meta MSL + UCL PhD. JEE AIR 124. Llama 3 contributor. ScaleRL co-author.",
        "urgency_decay_date": None,
        "channel": "email",
        "next_action": "Email ref ScaleRL recipe + PDR +11% AIME finding",
        "cluster": "scalerl",
    },
    "rishabh-tiwari": {
        "urgency_reason": "Berkeley/Keutzer. QuantSpec on Apple ML Research page. ScaleRL co-author. RS intern Meta.",
        "urgency_decay_date": None,
        "channel": "email",
        "next_action": "Email ref QuantSpec ~2.5x speedup + 90% acceptance rate",
        "cluster": "scalerl",
    },
    "kawin-ethayarajh": {
        "urgency_reason": "Created KTO. UChicago Booth prof. 3,200+ cites. Research collaboration angle.",
        "urgency_decay_date": None,
        "channel": "email",
        "next_action": "Email ref KTO vs DPO commercial deployment question",
        "cluster": "post-training",
    },
    "roshan-rao": {
        "urgency_reason": "Post-EvolutionaryScale acquisition by CZ Biohub. Second-act watch in 12-24 months.",
        "urgency_decay_date": None,
        "channel": "email",
        "next_action": "Email ref ESM3 → what's next in protein foundation models",
        "cluster": "ai-bio",
    },
    "ajay-jain": {
        "urgency_reason": "DDPM co-author. Genmo CTO. Diffusion-to-video cluster anchor. WndrCo connects to Chonghao.",
        "urgency_decay_date": None,
        "channel": "twitter",
        "next_action": "DM @ajayj_ ref Mochi 1 AsymmDiT vs Stable Video Diffusion architecture",
        "cluster": "diffusion-video",
    },
    "akshat-bubna": {
        "urgency_reason": "First Indian IOI Gold ever. Modal CTO ($1.1B, ~$50M ARR). Already running. Relationship.",
        "urgency_decay_date": None,
        "channel": "email",
        "next_action": "Email ref Modal scale + ask for intros to IOI-track founders",
        "cluster": "ioi-pipeline",
    },

    # ─── LP / CAPITAL (separate track from founders) ──────────────────────
    "jessie-jia-guo": {
        "urgency_reason": "Next Legacy Emerging Leaders Fund: exact $1-5M emerging-manager fit.",
        "urgency_decay_date": None,
        "channel": "email",
        "next_action": "Request introductory LP meeting — lead with clarity-of-purpose framing",
        "cluster": "lp",
    },
    "sameer-gandhi": {
        "urgency_reason": "Meeting scheduled. Accel partner with Perplexity board + Anthropic + India bridge.",
        "urgency_decay_date": None,
        "channel": "meeting",
        "next_action": "Prep meeting — lead with Perplexity/Aravind connection + deal flow proof",
        "cluster": "lp",
    },

    # ─── VC PEER / CO-INVESTOR ────────────────────────────────────────────
    "shri-kolanukuduru": {
        "urgency_reason": "Category Ventures pre-seed/seed. Natural follow-on partner. Engineer-founder thesis.",
        "urgency_decay_date": None,
        "channel": "email",
        "next_action": "Deal flow swap email — name 2 pre-seed founders he'd want to see",
        "cluster": "co-investor",
    },
}


def main():
    state = json.loads(STATE.read_text())
    people = state["people"]
    missing = []
    updated = 0

    for slug, fields in SEED.items():
        if slug not in people:
            missing.append(slug)
            continue
        for k, v in fields.items():
            people[slug][k] = v
        updated += 1

    STATE.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n")
    print(f"Seeded {updated} entries.")
    if missing:
        print(f"WARNING: {len(missing)} slugs not found in state: {missing}")
        print("Run `python3 data/build_outreach_state.py` first if dossiers exist.")


if __name__ == "__main__":
    main()
