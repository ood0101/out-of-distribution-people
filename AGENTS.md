# Out of Distribution People — Project Memory

## What This Is
A persistent deep research system (static HTML digital garden) for an inception-stage VC.
Each person gets a dedicated HTML dossier page. A master index links all pages.
Repository: github.com/ood0101/out-of-distribution-people (public, GitHub Pages)

## Owner Preferences (Non-Negotiable)

### What the owner cares about
- Deeply technical, research-focused people at the frontier of AI/ML
- People at inflection points: about to start a company, just left a frontier lab, stealth mode
- The RATE OF CHANGE matters more than current state — acceleration is the signal
- Indian/Indian-origin people are a specific sourcing thesis — always flag with `indian` tag
- Network intelligence: who collaborates with whom, advisor lineages, co-author maps

### What the owner does NOT care about
- Forbes 30U30 ("pretty much a scam")
- TIME 100 AI ("pretty shit")
- MIT TR 35 Under 35 (questionable signal)
- YC / a16z / South Park Commons cohorts ("too late for us" — they invest at inception)
- Stanford coursework projects (every Stanford MS student does these — it's filler)
- High school activities (debate, robotics, scouts) unless truly exceptional
- LinkedIn-style role descriptions
- Vague superlatives ("one of the best", "exceptional talent") — replace with evidence

### Outreach Email Style (Non-Negotiable)
- Ultra-high substance. Must make the person feel the sender genuinely understands their specific problem/belief
- Structure: Who am I → Why reaching out (show landscape: 3-5 companies/approaches) → Intrinsic insight about THEM (specific paper finding, metric, technical decision) → Next steps
- Short: 4-6 sentences after greeting. Conversational, not corporate
- Sign as "Vansh" (no formal sign-off)
- Always name specific companies and approaches in their space to prove market understanding
- End with specific offer: "I can write $500K-$1M and move fast" or similar
- NO generic compliments, NO fund thesis paragraphs, NO "pick your brain" language
- See AGENT_SOP.md for full template and anti-patterns

### Signal sources the owner DOES value
- Competition results: IOI, IMO, ICPC, Putnam, IPhO, USAMO, USABO, ISEF, Regeneron STS
- Lab alumni pages: Chris Ré, Percy Liang, Pieter Abbeel, Kaiming He, Song Han, Tri Dao, etc.
- Departure signals from frontier labs (the 20 non-negotiable companies)
- Credential intersections (IOI + quant, physics olympiad + CS PhD, etc.)
- Codeforces International Grandmaster (2600+)
- Exceptional Capital Exceptional 100

## Research SOP
Read `AGENT_SOP.md` for the full 6-agent research architecture.

Key points:
- Launch 6 parallel agents per person (technical, social, market, background, trajectory, recursive)
- Investment-thesis-first output format
- Evidence over claims. Numbers over adjectives. Quotes over summaries
- Must include at least 2 direct quotes from the person's own words
- Must include competitive landscape with at least 3 comparables
- Must include growth trajectory with dated milestones
- Recursive discovery: context-dependent expansion (startup → team, researcher → lab, departure → cohort)
- After synthesis, assign a tier (0 = active pursuit, 1 = high conviction, 2 = tracking, 3 = indexed)

## Tier System
- **Tier 0:** Active pursuit. Likely starting a company within 6 months. Reach out now.
- **Tier 1:** High conviction. Would back if they started today. Build relationship, check monthly.
- **Tier 2:** Tracking. Worth watching. Check quarterly.
- **Tier 3:** Indexed. Part of a cohort or competition result. Re-evaluate if they surface again.

## 20 Non-Negotiable Departure-Tracking Companies
OpenAI, Anthropic, Google DeepMind, Meta FAIR / Meta Superintelligence Labs, xAI, Mistral AI,
Cursor/Anysphere, Runway, Midjourney, Character AI, Perplexity, Scale AI, Databricks (Mosaic ML),
Together AI, Physical Intelligence, NVIDIA Research, Tesla AI/Optimus, Apple MLR, Anduril Lattice, Palantir AIP

## Critical Labs for Alumni Tracking
Chris Ré (Stanford), Percy Liang (Stanford), Pieter Abbeel (Berkeley), Kaiming He (MIT),
Song Han (MIT), Tri Dao (Princeton), Christopher Manning (Stanford), Sanjit Seshia / Ion Stoica (Berkeley),
Sergey Levine (Berkeley), Chelsea Finn (Stanford), Tengyu Ma (Stanford), Stefano Ermon (Stanford),
Ludwig Schmidt (UW/Stanford)

## Tech Stack
- Static HTML/CSS, no JS frameworks. Max-width 920px
- CSS: `--bg: #fafaf8`, `--accent: #c43d2e` (red for spikes), Georgia serif headings, monospace labels, Inter sans-serif body
- Person pages follow the template in existing hand-curated dossiers (see people/ronak-malde.html as gold standard)
- Data files in /data/ directory (Delta fellows JSON, build scripts)
- .nojekyll file for GitHub Pages compatibility

## Current State (as of March 2026)
- 28 hand-curated dossier pages + 142 Delta fellow pages = 170 total
- 144 Delta fellows indexed with photos, profiles, company research
- IOI gold medalists (2018-2024) and IPhO gold medalists mapped but not yet indexed in repo
- Competition medal pipeline established
- Background monitoring not yet scheduled (planned: Tier 0 weekly, Tier 1 monthly)
- Clay MCP tool available for email lookups
- Twitter MCP tools available for engagement analysis
