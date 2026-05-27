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
        "urgency_reason": "Co-founder of rekursiv.ai (stealth, Mountain View, 'Autonomously Create Knowledge') with Joshua V. Dillon (TensorFlow Probability creator, 13,301 Scholar cites). FIRST LUMA RESEARCH-SCIENTIST DEPARTURE INDEXED IN REPO (ex-Luma RS Mar 2024–2025/Q1 2026, ex-Google 4.5y). 1st author VideoPoet (ICML 2024 Best Paper, 1 of 10 from 2,610) + 1st author MoViNets (CVPR 2021) + 1st author UDify (EMNLP 2019). Architectural through-line: ONE general system subsumes a zoo of specialists, now applied to scientific method. Category (AI Scientists): Sakana $2.65B, Edison $70M, Lila $550M — Kondratyuk+Dillon are the only team with a 1st-author ICML Best Paper foundation-model author + 13K-cite probabilistic-infra creator on the founding bench. Site live, recruiting@rekursiv.ai hiring, no public raise = seed window NOW. 1,327 LinkedIn followers (pre-launch). NOT same as Richard Socher's Recursive Superintelligence ($650M, $4.65B). First Charles University node in repo.",
        "urgency_decay_date": None,
        "channel": "linkedin",
        "next_action": "LinkedIn DM (1,327 followers = will read). Subject: 'One decoder, many specialists — the through-line from VideoPoet to rekursiv.' Lead with the architectural through-line across UDify/MoViNets/VideoPoet (one general system subsumes a zoo of specialists), name Sakana hallucination tax + Edison bio lock-in + Lila wet-lab capex, ask architectural question (custom multimodal foundation model substrate vs TFP-wrapper on open base models), $500K-$1M check, warm-intro option via Chenfeng Xu (in-repo T2, Improved Immiscible Diffusion 2025 co-author). Fallback: general@rekursiv.ai. Tertiary: X DM @hyperparticle. Sign Vansh. Reach out alongside Joshua Dillon (rekursiv co-founder) the same week — pairing is the story.",
        "cluster": "ai-scientists",
    },
    "joshua-dillon": {
        "urgency_reason": "Co-founder of rekursiv.ai (stealth, Mountain View, AI Scientists category) with Dan Kondratyuk. CREATOR + ENGINEERING LEAD OF TENSORFLOW PROBABILITY (4.4K GitHub stars, the canonical probabilistic-ML library inside Google + Alphabet research; used by Anthropic / DeepMind / Brain alums). 1st author of TensorFlow Distributions (Nov 2017, 744 cites) — the founding TFP paper. 13,301 Scholar cites, h-25, i10-32. 11,671 of 13,301 cites since 2021 = ACCELERATING slope late in 13+ year career. Three papers over 1,000 cites: DVIB (Alemi+Fischer+Dillon+Murphy 2016, 2,878 cites) — founding paper of info-theoretic deep learning; 'Can You Trust Your Model's Uncertainty' (Ovadia et al. NeurIPS 2019, 2,839 cites) — canonical uncertainty-under-shift benchmark; 'Likelihood Ratios for OOD' (Ren et al. NeurIPS 2019, 1,019 cites). OOD-DETECTION TRILOGY ~3,991 COMBINED CITES = the rekursiv differentiator (AI Scientists hallucinate; Joshua's trilogy is literally the toolkit for catching that). Gemini 2.5 co-author (2025, 3,101 cites). VideoPoet 15th of 27 = bonding-event paper with Dan inside Google before they co-founded. PhD ML Georgia Tech (Guy Lebanon). Declined Marshall Sherfield Postdoc. ~10-15y Google Research probabilistic ML. VERIFIED @rekursiv.ai Scholar email = full-time at company confirmed. recruiting@rekursiv.ai open. THE JOSHUA + DAN PAIRING is the story: foundation-model author + probabilistic-infra creator = strongest AI-Scientist founding bench in May 2026 cohort. No other AI-Scientist team (Sakana $2.65B / Edison $70M / Lila $550M / Periodic / FutureHouse) has this exact combination on the founding bench. 566 LinkedIn followers (lower-profile than Dan, will read DM).",
        "urgency_decay_date": None,
        "channel": "linkedin",
        "next_action": "LinkedIn DM https://www.linkedin.com/in/jvdillon/ (566 followers, will read). Subject: 'OOD detection for autonomous discovery — your TFP + DVIB lineage applied to AI Scientists.' DIFFERENT ANGLE FROM DAN: lead with category-level hallucination problem (Sakana v1 peer-review critique on hallucinated numerical results) and connect directly to Joshua's own OOD trilogy (DVIB + Ovadia + Ren). Name Alex Alemi (now Anthropic) + Dustin Tran (DeepMind) as legitimate reference paths — his closest co-authors. Ask probabilistic-programming substrate question (TFP-style vs ensemble-only). $500K-$1M check. Reach out alongside Dan Kondratyuk same week — pairing is the story. Fallback: general@rekursiv.ai. Tertiary: X DM @dfacto82.",
        "cluster": "ai-scientists",
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

    # ─── T1 FALLOW — full dossiers already exist, seeded May 26 batch ────
    "ritvik-kapila": {
        "urgency_reason": "NeoSigma co-founder w/ Gauri Gupta. Essential AI under Vaswani (24T token dataset). IIT Delhi + UCSD 4.0. Indian.",
        "urgency_decay_date": None,
        "channel": "twitter",
        "next_action": "DM @ritvikkapila — ref NeoSigma + Essential AI dataset scale",
        "cluster": "post-training",
    },
    "gauri-gupta": {
        "urgency_reason": "NeoSigma founder & CEO. MIT PhD dropout. IIT Delhi. Pre-seed. Indian female founder.",
        "urgency_decay_date": None,
        "channel": "twitter",
        "next_action": "DM @gauri__gupta — ref NeoSigma eval + post-training wedge",
        "cluster": "post-training",
    },
    "ally-nakamura": {
        "urgency_reason": "Catapult Technologies (PearX S24) founder — AI agents for medical device workflows. Masason Scholar. Stanford AI.",
        "urgency_decay_date": None,
        "channel": "email",
        "next_action": "Email ally@trycatapult.ai — ref Pear S24 + medical device workflow wedge",
        "cluster": "healthcare-ai",
    },
    "ritvik-singh": {
        "urgency_reason": "Built NVIDIA ORBIT/Isaac Lab (6.8k stars). First RGB-only dexterous grasping (93% real-world). Berkeley PhD Abbeel+Malik. 855 cites. Indian.",
        "urgency_decay_date": None,
        "channel": "email",
        "next_action": "Email ritviksingh9@gmail.com — ref Dexgrasp + ORBIT/Isaac Lab adoption",
        "cluster": "robotics",
    },
    "sijun-tan": {
        "urgency_reason": "rLLM lead (5.3K stars). DeepScaleR beats o1-preview. Co-lead went stealth. Berkeley.",
        "urgency_decay_date": None,
        "channel": "email",
        "next_action": "Email or Twitter — ref rLLM + DeepScaleR co-lead departure pattern",
        "cluster": "post-training",
    },
    "niklas-muennighoff": {
        "urgency_reason": "23.5K citations. MTEB creator. s1 author. Knight-Hennessy Scholar. Stanford. Reference class for Tanishq Kumar (recursive discovery).",
        "urgency_decay_date": None,
        "channel": "email",
        "next_action": "Email or Twitter — ref s1 + MTEB commercial deployment angle",
        "cluster": "post-training",
    },
    "tanishq-kumar": {
        "urgency_reason": "1st-year Stanford CS PhD (Sep 2025) co-advised by Percy Liang + Tatsu Hashimoto. 6 pre-PhD ICLR/ICML papers via Pehlevan/Bordelon (Harvard SEAS / Kempner): Grokking ICLR 24 (1st, 109 cites) + No Free Prune ICML 24 (co-1st w/ Sellke) + Scaling Laws for Precision ICLR 2025 ORAL AWARD (co-1st, 112 cites) + Do Mice Grok ICLR 25 (1st) + Overtrained LMs SCOPE Outstanding + ICBINB Best Paper ICLR 25 (4th of 8 w/ Springer + Goyal + Wen + Aditi, 56 cites). Already ICLR 2026 1st-author Speculative Speculative Decoding w/ Tri Dao (CLAUDE.md critical lab) + Avner May. 3 co-authorships with Aditi Raghunathan (CMU). Co-author w/ Niklas Muennighoff (reference class, in repo) + Chris Ré + Ben Spector (in repo). 313 Scholar cites, h-5. Indian-origin (Tanishq Mathew Kumar). Harvard math '25 (with 2019-20 SF gap year, prior boarding school London, Abu Dhabi childhood). Reference class: Niklas Muennighoff (pre-PhD prolific publisher archetype). Recursive discovery from Aditi Raghunathan dossier (her P0 student).",
        "urgency_decay_date": None,
        "channel": "email",
        "next_action": "Email tanishq@stanford.edu — relationship build, NOT pitching. Lead with technical insight on Scaling Laws for Precision (low precision reduces effective parameter count + post-training quantization gets worse with more pretraining data, the cross-finding with Overtrained paper) + ask about Pehlevan/Bordelon DMFT framework prediction for precision floor below FP6. Reference Niklas + Sukjun as in-repo reference classes. Fallback Twitter DM @tanishqkumar07 (5,243 followers, verified).",
        "cluster": "scaling-laws",
    },
    "shreyas-sreenivas": {
        "urgency_reason": "Exa founding engineer — Vector DB in Rust. $12M ARR. Indian (Bangalore). Already at scale — relationship/sourcing angle.",
        "urgency_decay_date": None,
        "channel": "email",
        "next_action": "Email — ref Exa Rust vector DB + ask for intros to next-wave search founders",
        "cluster": "search-infra",
    },
    "aditya-gupta": {
        "urgency_reason": "Chess NM + USACO Plat. 2 acquisitions by 20. Percy Liang advisor. Indian.",
        "urgency_decay_date": None,
        "channel": "twitter",
        "next_action": "DM — ref 2x acquisition pattern + Percy Liang lab connection",
        "cluster": "stanford-pipeline",
    },
    "suvansh-sanjeev": {
        "urgency_reason": "OpenAI GPT-5 team. CMU PhD dropout. Prior founder. Indian. OpenAI is on the 20-tracked list.",
        "urgency_decay_date": None,
        "channel": "twitter",
        "next_action": "DM — ref GPT-5 + prior founder background; departure-watch candidate",
        "cluster": "openai-departure",
    },
    "ameen-patel": {
        "urgency_reason": "INTELLECT-3 co-author (106B SOTA). Prime Intellect. Indian.",
        "urgency_decay_date": None,
        "channel": "twitter",
        "next_action": "DM — ref INTELLECT-3 106B + decentralized training thesis",
        "cluster": "decentralized-training",
    },
    "gashon-hussein": {
        "urgency_reason": "Physical Intelligence researcher. pi-0.6 co-author. Neo Scholar. Physical Intelligence is on the 20-tracked list.",
        "urgency_decay_date": None,
        "channel": "twitter",
        "next_action": "DM — ref pi-0.6 + robot foundation model serving angle",
        "cluster": "robotics",
    },
    "zeyneb-kaya": {
        "urgency_reason": "Topological (YC S25) co-founder/CTO. Physics CAD 1930x faster. Regen STS 5th ($90K). ~19. 3 hackathon wins.",
        "urgency_decay_date": None,
        "channel": "email",
        "next_action": "Email — ref Topological 1930x speedup + young second-time builder pattern",
        "cluster": "physics-cad",
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
