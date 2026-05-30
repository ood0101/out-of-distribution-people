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
    "kushal-kedia": {
        "urgency_reason": "Cornell CS PhD candidate GRADUATING MAY 2026 (5 weeks out). Advised by Sanjiban Choudhury (Cornell + Aurora; ONR YIP + OpenAI Superalignment Award + Google Research Award; PoRTaL Lab) + Wei-Chiu Ma (Cornell, MIT/Torralba+Urtasun, ex-Uber ATG/Waabi). CONCURRENT visiting researcher at Stanford under Jeannette Bohg (IPRL, 2023 Sloan) + C. Karen Liu (humanoid + biomechanics, SIGGRAPH Academy; ON PARTIAL LEAVE JAN–JUN 2026 — likely humanoid co sabbatical). 8 top-venue robotics papers in 4 years: X-Sim (CoRL 2025 ORAL + RSS EgoAct Best Paper Runner-Up, co-1st w/ Prithwish Dan) — real-to-sim-to-real training using rewards from human videos, EXACT PI pi-0.5/Figure Helix/1X World Model/Skild Brain wedge. RHyME (ICRA 25, Cornell Chronicle press). MOSAIC (CoRL 24 + Best Paper VLMNM ICRA 24 + Best Poster MoMa ICRA 24, co-1st). X-Diffusion (ICRA 26, co-1st). SimToolReal (Feb 26, 1st w/ Tyler Lum + Bohg + Karen Liu). InteRACT (ICRA 24, 1st), ManiCast (CoRL 23, 1st), Game-Theoretic (IROS 23, 1st). 4 best/oral awards in 18 months. 154 Scholar cites, h-7, i10-5 (verified). IIT KGP undergrad (CSE; advised PP Chakrabarti). Cruise + MSR India interns. Oct 2025 invited talks at NVIDIA Robotics Mobility + RAI Institute + UMich = canonical pre-offer pattern. Shift from academic talk circuit (Oct 24 RPM Lab UMN + RobIn Lab UT Austin) to industry talk circuit (Oct 25 NVIDIA + RAI) = strongest signal he's going industry-side, not faculty. Twitter @kushalk_ 834 followers — research-promo only, no founder signal yet. Modal outcome: research scientist at PI/Figure/1X/Skild within 6 months; non-zero probability of founding (Prithwish Dan, Cornell MS, co-1st on 6 papers, is co-founder candidate). Bridges 3 in-repo nodes: Weiying Wang (T0 stealth humanoid Cambridge), Ritvik Singh (T1 NVIDIA Isaac Lab Berkeley Abbeel+Malik), Himanshu Gaurav Singh (T1 Berkeley Abbeel+Malik JEE AIR 2). Indian. Citation profile mid-tier (closer to Weiying operator-pivot than Tanishq citation-prodigy) — load-bearing claim is award density + timing + dual-lab advising, not raw cites.",
        "urgency_decay_date": "2026-07-15",
        "channel": "email",
        "next_action": "Email kk837@cornell.edu THIS WEEK. Subject: 'X-Sim, Moving Beyond Teleoperation, and what's next post-Cornell.' Lead with X-Sim Oral (CoRL 25) + RSS EgoAct Best Paper Runner-up + the 'real-to-sim-to-real with no teleop' framing. Name 4 humanoid landscape comps with valuations (PI pi-0.5 $2B+, Figure Helix $39B, 1X NEO World Model OpenAI-backed, Skild Brain $300M+). Ask the sim-asset-reconstruction-from-video vs reward-extraction-layer technical question only an X-Sim reader could ask. Offer $500K-$1M check + Weiying Wang in-portfolio intro + Karen Liu cohort market intel + 20 min coffee. Don't pitch capital first — open the channel before he signs. Backup: X DM @kushalk_.",
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
    "augustus-odena": {
        "urgency_reason": "Co-founder of Arda (AI-for-manufacturing) with Bob McGrew (ex-OpenAI CRO) + 2 ex-Palantir leads. Stealth cover blown Feb 25 2026 (Information/Palazzolo). $20M seed closed (Team8 + SignalFire); $70M priced round at $700M post-money reportedly co-led by Founders Fund + Accel (Khosla + XYZ also in) — STAGE PAST FUND'S INCEPTION RULE per CLAUDE.md. Second-time founder: co-founded Adept (Apr 2022, research lead; ACT-1 first Computer Use Agent; Fuyu multimodal models) → Amazon reverse-acquihire Jun 28 2024 → Meta TBD Labs Jun–Nov 19 2025 (5.5 months) → Arda. 23,359 Scholar cites, h-27: SAGAN (5,930), AC-GAN (4,975), Program Synthesis with LLMs (3,999), Deconvolution checkerboard (2,199), Scratchpad/CoT (Nye lead, 1,095) + joint CoT patent US20230244938A1. Columbia Math BA → Five Rings/Millennium trader → Nervana → Google Brain Resident batch 1 → Brain ~5y. Nov 20 2025 resignation tweet (629 likes): 'Founder Mode is real and good… unusually high-leverage time to pursue ambitious new projects at the intersection of AI and other technologies.' DILIGENCE FLAG (CTOL): self-attribution 'invented chain-of-thought' overclaims vs Wei et al.; Scratchpad IS adjacent + patent IS real. ADJACENT INDEXES: David Luan (Adept CEO, left Amazon Feb 2026 'to cook up something new', highest-priority follow-on), Maxwell Nye (Adept co-founder, now Meta MSL, Scratchpad lead inventor), Bob McGrew (OpenAI Mafia hub). T1 not T0: Arda round past inception stage; manufacturing thesis not in fund's 20 tracked categories; Augustus is research-anchor not CEO-narrative-anchor.",
        "urgency_decay_date": None,
        "channel": "twitter",
        "next_action": "Twitter DM @gstsdn (primary, 12.1K followers) OR email augustus.odena@gmail.com (backup). Subject 'Scratchpad → Arda — the factory-video moat question.' Lead with Scratchpad date-precedence vs Wei et al. (Nov 2021 vs Jan 2022) WITHOUT repeating 'invented CoT' overclaim. Frame the Adept ACT-1 → Anthropic Computer Use lesson on data-distribution. Ask the data-licensing-vs-foundation-model question (customer-licensed factory video = Palantir model vs pre-trained corpus = PI model) — answer reveals Arda's moat strategy. NO capital ask (acknowledge $500K-$1M check doesn't fit $700M round). Offer to be useful on cohort intel (continual learning / humanoid robotics / reasoning-RL). Sign Vansh. Goal is relationship for next venture in 5-7y, NOT current Arda round. RECURSIVE DISCOVERIES TO INDEX: David Luan (Adept CEO ex-Amazon Feb 2026), Maxwell Nye (Meta MSL, Scratchpad lead), Bob McGrew (OpenAI Mafia hub @bobmcgrew).",
        "cluster": "founders-pool-adept",
    },
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
    "aryaman-arora": {
        "urgency_reason": "3rd-year Stanford NLP CS PhD (Potts + Jurafsky), mechanistic interpretability + rare researcher-who-builds. Co-first author (w/ Zhengxuan Wu) on ReFT (NeurIPS 2024 Spotlight, 255 cites; LoReFT 15-65x more param-efficient than LoRA) + AxBench (ICML 2025 Spotlight, 153 cites; 'simple baselines beat SAEs'). Sole-led CausalGym -> ACL 2024 Outstanding Paper + SAC Award. Core contributor on pyvene (879 stars, the DAS/intervention library) + pyreft (1.6k stars). ~1,299 Scholar cites, h-14, i10-17 (top-decile for 3rd-year). Already interned at Transluce (Steinhardt) + Redwood + Apple = one step from interp commercialization. Indian-origin (born India, immigrated ~5, Wiktionary admin as teen writing code for South Asian languages). Georgetown CS+Ling '23 (Nathan Schneider; ACL paper as a first-year; Tropaia CS Award). NSF GRFP. mech-interp cluster anchor w/ Kunvar Thaman (T1) + Neel Nanda (T2); Jurafsky-lab bridge to Kawin Ethayarajh (T1, KTO). NO founding signal (only 'startup' mention is a joke tweet); real probability stays academic; if commercial likely a hire (Goodfire/Transluce/Anthropic) not founder. Voice @aryaman2020 active/funny. Higher-priority spinout-watch within his group is Zhengxuan Wu (tooling lead). T2 relationship-build, long fuse, quarterly.",
        "urgency_decay_date": None,
        "channel": "twitter",
        "next_action": "DM @aryaman2020 (active/funny, do NOT pitch). Lead with a genuine question on the AxBench/SAE result (does steering-via-ReFT win, or is the honest answer still 'just finetune'); name the Goodfire/Transluce/Redwood landscape and correctly note he's already been inside Transluce + Redwood. Distinguish 'builds the tooling' vs 'cites it' (pyvene/pyreft). Coffee in SF, no ask. AUTHORSHIP PRECISION: co-first (not sole) on ReFT/AxBench w/ Zhengxuan Wu; lead on CausalGym; core contributor (not principal) on pyvene/pyreft. RECURSIVE DISCOVERIES TO INDEX: Zhengxuan 'Zen' Wu (P1, Stanford NLP, lead author on pyvene/ReFT/AxBench = the interp-tooling principal + higher-priority spinout-watch) + Atticus Geiger (P2, DAS/causal abstraction originator, Pr(Ai)2R Group).",
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
    "vikram-sundar": {
        "urgency_reason": "ML Scientist at Generate:Biomedicines (Flagship, $273M Series C, NVIDIA+Amgen). Just completed MIT CSB PhD (May 7 2025) under Kevin Esvelt; joined Generate full-time Jul 7 2025. Spike is selection not cites (103 cites, h-5): Hertz Fellow 2020 + Churchill Scholar 2018 + Goldwater 2017 + Putnam top-27. Harvard '18 (math, Aspuru-Guzik undergrad research). Built FLIGHTED (denoises high-throughput protein assay data to recover fitness landscapes); engineered TEV protease specificities. Roshan Rao / Sam Stanton reference class (elite bio-ML IC -> founder in 3-5 yrs). NO founding signal, just locked in at Generate -> relationship build, founding watch 2028-2030. Indian (Tamil).",
        "urgency_decay_date": None,
        "channel": "email",
        "next_action": "Email vsundar@generatebiomedicines.com. Subject: 'FLIGHTED — denoising the assay, not the model.' Lead with the noise-model-before-fitness-model read of FLIGHTED; name protein-design landscape (EvolutionaryScale, Cradle, Chai Discovery, Profluent, Latent Labs, Generate); reference Stanton + Rao WITHOUT pushing him to found; offer $500K-$1M only at the end. Backup: X DM @vikramsundar. Relationship build, NOT this-week urgency.",
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
    "cynthia-chen": {
        "urgency_reason": "Agent Software Engineer at Decagon ($4.5B Series D Jan 28 2026; first tender Mar 4 2026). One of first ~10 engineers (joined Sep 2024). Solo-built Trace View agent observability product + sole author of AOP Copilot launch blog. Harvard CS BS+MS '24, Eliot House. Co-author AttentionViz IEEE VIS 2023 (171 cites) under Wattenberg+Viégas at Insight + Interaction Lab. HBS Tech Innovation Fellow Cohort 6. Regeneron STS 2020 Finalist + Davidson Fellow + RSI + Intel ISEF + 2020 U.S. Presidential Scholar candidate (Harker '20 / Cupertino). Founded Startups @ Harvard (Fall 2023, Xfund-backed Member Grants) + runs SF weekend startup discussion group at her place. Founder-curious quote (unprompted): 'a lot of my friends who took big leaps and started companies of their own or joined early stage companies.' No public departure signal — relationship-build window. Decagon first tender likely re-commits her 2-3 years; founder inflection plausible Q1-Q3 2027. Prev: Scale AI (Enterprise Gen AI Platform APIs), HRT quant, LinkedIn.",
        "urgency_decay_date": None,
        "channel": "email",
        "next_action": "Email cynthia9chen@gmail.com (her published contact). Subject: 'Trace View, the SF startup group, and the next agent obs layer.' Lead with Trace View vs LangSmith ($1.1B) / Braintrust ($80M a16z) / Arize Phoenix landscape and the AOP-step-structured-trace differentiator; reference the SF weekend discussion group (NOT Startups @ Harvard — the group she runs *now*); ask for coffee, $500K-$1M check offer. Backup: Twitter DM @chenxcynthia (~850 followers). Avoid LinkedIn.",
        "cluster": "ai-agents",
    },
    "karan-singhal": {
        "urgency_reason": "Head of Health AI + AGI Benefits at OpenAI (one of 20 CLAUDE.md tracked cos) — the FIRST AMIE-cluster departure from Google DeepMind, ~22 months in. Co-equal first author (listed first) on Med-PaLM Nature 2023 (5,747 cites) + Med-PaLM 2 Nature Medicine 2025 (2,428 cites) — combined 8,175 cites; corresponding author on Med-PaLM. 21,541 total Scholar cites, h-26, i10-34 (99.9% post-2021 = pure medical-LLM + frontier-model profile). Stanford BS+MS CS '19 (4.1/4.0 MS GPA), initiated + main instructor of Stanford's first CS+Social Good AI ethics class (Apr 2018). Google Research Jul 2019 → Apr 2024 (~5y; federated learning lead author NeurIPS 2021 → Med-PaLM bottom-up brain moonshot). Departed July 22, 2024 (X tweet 1815444769868574944, 923 likes; Greg Brockman replied 'Welcome!'). Now leads OpenAI's entire health surface: HealthBench (May 2025, 49K rubric items, 250+ physicians, 60 countries) + Penda Health Kenya RCT (first real-world LLM clinical copilot RCT, statistically significant improvement on diagnosis+treatment) + OpenAI for Healthcare (Jan 8 2026 HIPAA-compliant ChatGPT, day-one customers Boston Children's, Cedars-Sinai, Memorial Sloan Kettering, Stanford Children's, UCSF, AdventHealth, Baylor Scott & White, HCA) + ChatGPT Health consumer (Jan 2026, Apple Health/wearables) + ChatGPT for Clinicians + HealthBench Professional (Apr 22 2026, pinned tweet 1.6M impressions, peak engagement). Jan 13 2026: 'we completed that original plan' tweet = founder-voice 'Series A note'. TIME100 Health 2026 (Feb 11). Co-author GPT-4o + o1 + GPT-5 + gpt-oss system cards. Second AMIE departure CONFIRMED via Jan 13 2026 reply: Khaled Saab (Stanford EE PhD under Chris Ré = CLAUDE.md critical lab, Hazy Research alumnus) now on Karan's OpenAI Health team — bridges DeepMind health ↔ Ré cluster ↔ OpenAI Health pipeline. Sam Altman: 'healthcare is one of the defining impacts of AGI' (cited by Karan). Indian-origin (Singhal = North Indian Vaishya/Marwari surname, name-based only — not interview-confirmed). SF-based. @thekaransinghal (9,815 X followers). NOT a founder yet — earliest meaningful departure window Q3 2027 (3-yr vesting milestone). Reference class: Roshan Rao (T1, FAIR → EvolutionaryScale, the bio analogue) + Vivek Natarajan (T1, parallel-track comp who stayed). T1 RELATIONSHIP-BUILD, not pitch. Departure-watch triggers: (1) OpenAI → OpenAI Foundation transition (Yo Shavit May 25 2026 precedent — Karan retweeted), (2) X bio change (currently 'Health AI, AGI benefits, safety @OpenAI'), (3) Vivek Natarajan's next move (most-likely co-founder), (4) Khaled Saab departure inverse signal, (5) OpenAI Health spin-out / acquisition. If he ever founds, Vivek is the canonical co-founder — they were the dosa-lunch project originators together. NEW recursive: Nate Gross (Doximity co-founder, OpenAI healthcare strategy lead) + Ashley Alexander (ex-Instagram product, OpenAI healthcare product) — the operator+product side of the OpenAI Health founding kernel.",
        "urgency_decay_date": None,
        "channel": "email",
        "next_action": "Email karansinghal@google.com (his Nature corresponding-author address, still public) or X DM @thekaransinghal (9,815 followers, will read). Subject: 'Med-PaLM 2 9-axis rubric → HealthBench 49K criteria — the post-training feedback loop you couldn't get at Google.' Lead with the Aug 2023 Rising Stars #4 quote ('the missing piece now is the post-training refinement of these models in the context of specific workflows') as the founder-thesis-before-OpenAI-existed reference; connect to ChatGPT for Healthcare's 8 named hospital systems as the operational realization. Name 5 healthcare-AI landscape comps (Hippocratic $1.6B, Abridge $850M, OpenEvidence $1B, Innovaccer $3.2B, K Health). Ask the model-grader-outperforms-physician-grader question — Khaled Saab cross-reference legitimate. Reference Roshan Rao → EvolutionaryScale + Mira Murati → Thinking Machines as senior-IC-to-founder precedents WITHOUT pitching founding. Frame: peer/thought-partner curiosity. 20 min ask. Sign Vansh, no fund-thesis paragraph. Backup: LinkedIn karan1149 (high inbound, lower hit rate); tertiary contact via personal site karansinghal.com.",
        "cluster": "healthcare-ai",
    },
    "vivek-natarajan": {
        "urgency_reason": "Research Lead at Google DeepMind (one of 20 CLAUDE.md tracked cos) — canonical world-class healthcare AI researcher. Lead researcher on the 4 most-cited medical-LLM papers in history: Med-PaLM (Nature 2023, 5,742 cites, first AI to pass USMLE) + Med-PaLM 2 (Nature Medicine 2025, 2,422 cites, 86.5% MedQA = +19pp) + AMIE conversational (Nature 2025, 733 cites, beat PCPs in OSCE) + AMIE-DDx (Nature 2025). 20,301 total Scholar cites, h-35, i10-50 (99.5% earned since 2021). Co-leads Project AMIE w/ Alan Karthikesalingam. Mar 2026 Beth Israel Deaconess prospective clinical feasibility study (arXiv 2603.08448): 100 patients, 90% top-DDx, ZERO safety stops — first real-world AMIE deployment. Included Health nationwide randomized study underway. Also co-lead AI Co-Scientist (522 cites, US Genesis Mission / 17 DOE National Labs). BS NIT India → MS CS UT Austin → FAIR (won 2018 VQA Challenge, Pythia/MMF; TextVQA 2,285 cites) → Google Health (recruited by Greg Corrado) → Google DeepMind. Harvard T.H. Chan exec-ed faculty; RAAIS 2023+2026 speaker; Harvard SEAS invited talk. Indian-origin (Tamil; grew up where seeing a doctor was not feasible). NO public departure signal as of May 2026 — T1 relationship-build, NOT pitch. Reference class: Roshan Rao (T1 in repo, FAIR → EvolutionaryScale → CZI, the medical analogue). Founder-thesis quote (his own, Pear Healthcare Playbook): 'The companies that became unicorns were concepts that reimagined and rebuilt workflows on the new platform. I don't see anyone doing that yet.' Recursive discoveries surfaced: Karan Singhal (P0, Med-PaLM 1st author, departed Google → OpenAI Health Aug 2024 = first AMIE-cluster departure), Tao Tu (P0, AMIE 1st author CMU PhD), Khaled Saab (P1, Stanford EE PhD under Chris Ré = CLAUDE.md critical lab; Hazy Research alumnus), Anil Palepu (P1, Harvard-MIT HST). Estimated earliest meaningful departure window: 2027-2028.",
        "urgency_decay_date": None,
        "channel": "email",
        "next_action": "Email (institutional vivnat@google.com inferable pattern) or X DM @vivnat. Subject: Beth Israel feasibility paper (90% top-DDx, zero safety stops, 100 patients, arXiv 2603.08448) — 'the moment medical AI stopped being a benchmark game.' Reference 5 specific landscape comps with valuations (Hippocratic $1.6B, Abridge $850M, OpenEvidence $1B, Innovaccer $3.2B, K Health). Quote his own Pear Healthcare Playbook 'unicorn workflow-rebuild' framing back at him. Drop Roshan Rao → EvolutionaryScale reference class. Frame as peer/thought-partner curiosity, NOT pitch — he is not a founder candidate today. 20-min ask. Sign Vansh, no fund-thesis paragraph. Backup: LinkedIn DM (high inbound; lower hit rate).",
        "cluster": "healthcare-ai",
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
