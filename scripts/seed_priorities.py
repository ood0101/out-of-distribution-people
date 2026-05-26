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
    "shivani-poddar": {
        "urgency_reason": "Stealth AI Startup founder (venture-backed), building agentic AI for commerce. Highest-signal untriaged entry in repo.",
        "urgency_decay_date": None,
        "channel": "twitter",
        "next_action": "DM @shivanipod — ref agentic commerce wedge + ask what she's building",
        "cluster": "agent-commerce",
    },
    "ronak-malde": {
        "urgency_reason": "Stealth founder (prev DeepMind ~7 months). Trained SWE-1 at Windsurf — triggered $2.4B Google acquisition. ~2 months post-departure.",
        "urgency_decay_date": None,
        "channel": "twitter",
        "next_action": "DM @rronak_ — ref continual learning thesis + SWE-1 training-from-scratch story",
        "cluster": "windsurf-cohort",
    },
    "michael-elabd": {
        "urgency_reason": "Trajectory Technologies Co-Founder/Director/CFO (CA filing Nov 3 2025) alongside Ronak Malde + Arjun Karanam. Concurrent DeepMind Foundational Research (verified Gemini Robotics arXiv co-author + Gemini Robotics 1.5 contributor). Apr 14 2026 X 'own the grammar' essay = strongest founder-voice artifact in the continual-learning cluster.",
        "urgency_decay_date": None,
        "channel": "email",
        "next_action": "Email hello@trajectory.ai ATTN Michael — lead with Apr 14 'own the grammar' essay + Policy Dreamer co-authorship as >=14-month team-history proof + SkillRL bitter-lesson question. Fallback Twitter DM @MichaelElabd (he's invited continual-learning DMs since ICLR Rio Apr 22).",
        "cluster": "continual-learning",
    },
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
    "weiying-wang": {
        "urgency_reason": "Stealth humanoid robotics founder, Cambridge MA. Harvard CS PhD (Stephanie Gil/REACT Lab) + ex-Zoox 3D perception/VLM/VLA. ~6 months post-departure window. 786 LinkedIn followers — pre-launch. Category consolidating fast (Figure $39B, PI $2B+).",
        "urgency_decay_date": None,
        "channel": "linkedin",
        "next_action": "LinkedIn DM ref Wi-Closure + MULAN-WC + the pi-0 vs OpenVLA transfer-vs-rebuild question; fallback warm intro via verified Yilun Du (Harvard/Kempner)",
        "cluster": "humanoid-robotics",
    },
    "blanca-villanueva": {
        "urgency_reason": "Stealth Founder & CEO 'autonomous robotics + biomedical AI' (LinkedIn May 2026). Stanford BS CS + MS Biomedical Informatics + Stanford School of Medicine. Nature 2023 co-author (Leskovec lab, 4th of 10) + Apple Hearing Study methods paper (JASA 2022) — shipped Apple Health algorithms. Boldcap mutuals Mo + Samir + 2 others. LinkedIn connection request PENDING. Rare female founder in autonomous medical robotics. CALIBRATION: the 3 arXiv surgical-robotics papers from brief are NOT hers (verified) — robotics half is currently a self-described stealth pitch, not a research record.",
        "urgency_decay_date": None,
        "channel": "warm-intro",
        "next_action": "Warm intro via Mo / Samir (Boldcap mutuals); fallback LinkedIn DM once pending connection accepts — lead with Apple Health -> founder pattern + name 5 surgical-robotics comps + 4 wedge surfaces + $500K-$1M check; final fallback blanca@cs.stanford.edu",
        "cluster": "surgical-robotics",
    },
    "devvrit-khatri": {
        "urgency_reason": "Joining Reflection AI ($2B) — vesting cliff begins immediately. Last pre-lockup window.",
        "urgency_decay_date": "2026-06-30",
        "channel": "email",
        "next_action": "Meet before Reflection start date; ref ScaleRL co-authorship pattern",
        "cluster": "scalerl",
    },
    "dan-kondratyuk": {
        "urgency_reason": "Co-founder of rekursiv.ai (stealth, Mountain View, 'Autonomously Create Knowledge') with Joshua V. Dillon (TensorFlow Probability creator). FIRST LUMA RESEARCH-SCIENTIST DEPARTURE INDEXED IN REPO (ex-Luma RS Mar 2024–2025/Q1 2026, ex-Google 4.5y). 1st author VideoPoet (ICML 2024 Best Paper, 1 of 10 from 2,610) + 1st author MoViNets (CVPR 2021) + 1st author UDify (EMNLP 2019). Architectural through-line: ONE general system subsumes a zoo of specialists, now applied to scientific method. Category (AI Scientists): Sakana $2.65B, Edison $70M, Lila $550M — Kondratyuk+Dillon are the only team with a 1st-author ICML Best Paper foundation-model author on the founding bench. Site live, recruiting@rekursiv.ai hiring, no public raise = seed window NOW. 1,327 LinkedIn followers (pre-launch). NOT same as Richard Socher's Recursive Superintelligence ($650M, $4.65B). First Charles University node in repo.",
        "urgency_decay_date": None,
        "channel": "linkedin",
        "next_action": "LinkedIn DM (1,327 followers = will read). Subject: 'One decoder, many specialists — the through-line from VideoPoet to rekursiv.' Lead with the architectural through-line across UDify/MoViNets/VideoPoet (one general system subsumes a zoo of specialists), name Sakana hallucination tax + Edison bio lock-in + Lila wet-lab capex, ask architectural question (custom multimodal foundation model substrate vs TFP-wrapper on open base models), $500K-$1M check, warm-intro option via Chenfeng Xu (in-repo T2, Improved Immiscible Diffusion 2025 co-author). Fallback: general@rekursiv.ai. Tertiary: X DM @hyperparticle. Sign Vansh.",
        "cluster": "diffusion-video",
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
    "chenfeng-xu": {
        "urgency_reason": "Incoming UT Austin AP (Fall 2026) + Researcher @ Together AI + Aurora project co-lead. 2 MLSys 2026 Best Papers in one week (LEANN + StreamDiffusionV2). Bridges 4 repo clusters (Keutzer/Tiwari, Tri Dao/Wang/Hwang/Mishra, Berkeley SkyLab, Song Han). Network hub.",
        "urgency_decay_date": None,
        "channel": "email",
        "next_action": "Email cxu@utexas.edu ref StreamDiffusionV2 58.28 FPS sink-token rolling KV + Together AI direction at UT Austin; fallback Twitter DM @Chenfeng_X",
        "cluster": "efficient-inference",
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
    "saksham-consul": {
        "urgency_reason": "Training at Black Forest Labs (FLUX models). FLUX.1 Kontext co-author. Stanford ME (Kennedy) + Nvidia + Lamini founding eng. BITS 9.99/10 branch topper. 5th node in diffusion cluster.",
        "urgency_decay_date": None,
        "channel": "twitter",
        "next_action": "DM @TheNoise2Signal ref FLUX.1 Kontext sequence-concat trick + KontextBench question",
        "cluster": "diffusion-video",
    },
    "akshat-bubna": {
        "urgency_reason": "First Indian IOI Gold ever. Modal CTO ($1.1B, ~$50M ARR). Already running. Relationship.",
        "urgency_decay_date": None,
        "channel": "email",
        "next_action": "Email ref Modal scale + ask for intros to IOI-track founders",
        "cluster": "ioi-pipeline",
    },
    "arjun-karanam": {
        "urgency_reason": "Co-Founder, Secretary & Director of Trajectory Technologies, Inc. (Nov 3 2025 CA filing, w/ Ronak Malde CEO + Michael Elabd CFO). Second-time founder — sole co-founder with prior incorporation (Time Flies, USAF AI scheduling). Policy Dreamer NeurIPS 2024 SoLaR co-authored with Michael Elabd + Kanishk Gandhi >14 months before incorporation — public-record proof of pre-Trajectory team collaboration. Stanford AI Lab thesis + 3x Apple Vision Pro + NASA Artemis + Regeneron/Siemens Scholar.",
        "urgency_decay_date": None,
        "channel": "email",
        "next_action": "Email arjun.karanam@stanford.edu or hello@trajectory.ai — ref Time Flies (USAF) + Policy Dreamer + Stanford AI Lab thesis on human-agentic simulation. Reach out alongside Ronak/Michael; team will compare notes. Fallback Twitter DM @QuantumArjun.",
        "cluster": "continual-learning",
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
    "jennifer-zhai": {
        "urgency_reason": "Dual role: Coho Deeptech Co-Founder/GP (Cartesia, Higgsfield, Bland, Sahara AI, Amigo) + stealth founder 'building continual learning' (Twitter bio @jennzhaii). Mei Z. archetype #2. Pending LinkedIn from Boldcap; 55+ mutuals.",
        "urgency_decay_date": None,
        "channel": "warm-intro",
        "next_action": "Warm intro via Alan or Aditya (LinkedIn mutuals); fallback DM @jennzhaii — lead with Cartesia SSM lineage + Ronak Malde continual-learning cluster",
        "cluster": "continual-learning",
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
