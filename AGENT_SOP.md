# Agent SOP: Out of Distribution People Research System

## Purpose
This document defines the standard operating procedure for research agents that build dossiers for an inception-stage VC identifying the most talented people who are truly out of distribution — BEFORE they're obvious to the market.

## Core Principle
**Every dossier must answer one question: should I build a relationship with this person right now, and if so, what's my angle?** Everything else is supporting evidence for that answer.

---

## Agent Architecture: 6 Parallel Agents Per Person

When researching a new person, launch ALL SIX agents simultaneously. Total time = slowest agent (~5 min), not sum of all agents.

### Agent 1: Technical Deep Dive
**Mission:** Find the specific, evidence-backed reason this person is extraordinary.

**Instructions:**
- What did they specifically build? Find benchmark numbers, model sizes, SWE-bench scores, citation counts, GitHub stars
- What was their EXACT role? Architect? Team lead? One of many contributors? Find evidence (commit history, paper authorship position, press quotes)
- How does their work compare to the top 5 competitors on specific metrics?
- Find papers, code repos, technical blog posts
- NO CLAIMS WITHOUT NUMBERS. If you can't find a benchmark, say "benchmark not publicly available" — don't substitute a vague superlative

**Quality bar:** A technical co-founder reading this section should learn something they didn't know. If it reads like a LinkedIn summary, it's failed.

### Agent 2: Primary Source / Social Signal
**Mission:** Read their actual public voice to understand what they'd build and when.

**Instructions:**
- Search Twitter/X for their recent tweets (last 3-6 months)
- Find their 5-10 highest-engagement tweets. QUOTE them verbatim (short quotes only)
- What topics generate the most engagement? This reveals their thesis
- Who replies to them? Flag: VCs, founders of known companies, researchers at specific labs
- Who do they reply to / retweet most? This reveals their intellectual community
- Read their blog/personal website if it exists. What do they write about unprompted?
- Check if their Twitter bio has changed recently (compare to cached versions if available)
- Look for conviction signals: "I believe...", "the future is...", "building...", "leaving...", "excited to..."

**Quality bar:** This section should contain at least 3 direct quotes from the person's own words. If it contains zero quotes, it's failed.

### Agent 3: Investment Context & Market
**Mission:** Frame this person as an investment opportunity, not a biography.

**Instructions:**
- What would they build if they started a company? What's the market? TAM?
- Name the 5 closest competitors or comparable companies. How would this person's approach differ?
- Which VCs are active in this space? Who would likely lead a round?
- What's the likely valuation range based on comparable raises? (e.g., "Windsurf alumni + frontier model training experience → comparable to [X] who raised $Y at $Z valuation")
- Timeline: How long have they been at current company? What's the typical tenure before departure? Any non-compete considerations?
- Risk factors: What could make this person NOT interesting? (stays at big co forever, goes back to academia, thesis doesn't pan out)
- Network: Who would they recruit? Who are their most likely co-founders?

**Quality bar:** A partner at a VC firm should be able to use this section to write an investment memo. If it reads like a Wikipedia article, it's failed.

### Agent 4: Background & Credentials
**Mission:** Compressed biographical context.

**Instructions:**
- Education (school, degree, advisor — ONE line each)
- Work history (company, role, dates — ONE line each)
- Competitions/awards (ONLY if exceptional — IOI gold, Putnam Fellow, etc. Skip routine honors)
- Demographic flags: Note if Indian/Indian-origin
- Photo URL: Find from Twitter profile, personal website, or other source
- Social links: Twitter, GitHub, LinkedIn, personal site, Google Scholar

**Quality bar:** This entire section should be 8-12 bullet points max. If it's longer, you're including filler. Kill anything that's baseline for their peer group (Stanford coursework projects, standard honors, club memberships).

### Agent 5: Growth Trajectory
**Mission:** Map the rate of change, not the current state.

**Instructions:**
- Find DATED milestones. Every achievement needs a month/year
- Build a chronological list and compute:
  - Is the gap between achievements shrinking? (acceleration)
  - Is the magnitude of achievements increasing? (escalation)
  - How does their pace compare to peer group? (a Stanford MS grad who trained a frontier model within 6 months of graduating is faster than normal)
- Specific metrics to track over time if available:
  - Citation count by year
  - GitHub stars/followers growth
  - Twitter follower growth rate
  - Revenue/funding trajectory (for founders)
  - Paper publication velocity

**Output format:**
```
GROWTH TRAJECTORY: [Name]
[Year]: [milestone]
[Year]: [milestone]
...
PACE: [X] career-defining events in [Y] months
ACCELERATION: [Clear/Moderate/Linear/Unclear]. [1-2 sentence explanation]
PEER COMPARISON: [How does this pace compare to others at their level?]
```

### Agent 6: Context-Dependent Recursive Discovery
**Mission:** Identify the highest-signal people connected to this person who should be researched next.

**Instructions — choose expansion direction based on context:**

**If the person is at a startup:**
→ Map the founding team and first 10 employees. Find names from team pages, LinkedIn, press releases. For each: name, role, background in ONE line.
→ If the startup was acquired: find every named person from the acquisition. Who stayed? Who left? Where did they go?

**If the person is a researcher / PhD student:**
→ Find the advisor. Find the advisor's lab page. List every current student and every graduate from the last 3 years. For each: name, current role, any notable work.
→ Find co-authors on their top 3 cited papers. Where are those co-authors now?

**If the person just left a company:**
→ Search for who else left the same company within 6 months. Coordinated departures signal new ventures forming.
→ Check if any of the co-departures have announced new companies or changed their Twitter bios.

**If the person is a professor / lab lead:**
→ Map all PhD graduates from the last 5 years. Where did they go? (startup, frontier lab, quant, academia)
→ Which graduates show founder signals? (left academia, active Twitter, started something)

**If the person is a founder:**
→ Map the first 5-10 employees. Early employees at breakout startups are often next-gen founders.
→ Check the investor list. Who else did those investors back? (portfolio-level pattern matching)

**Output format:**
For each person surfaced, provide:
- Name
- Current role
- Relationship to the person being researched
- ONE sentence on why they might be interesting
- Signal strength: HIGH (should research immediately) / MEDIUM (worth tracking) / LOW (context only)

**Do not cap at a fixed number.** For a Windsurf acquisition, there might be 12 people. For a solo PhD student, maybe 2. Let the context determine the expansion.

---

## Synthesis: Investment-Thesis-First Format

After all 6 agents return, I (the orchestrator) synthesize into this structure:

### Page Structure (in order)

1. **One-liner** — Who they are in one dense sentence
2. **Investment Thesis** (2-3 sentences) — Why this person, why now, what's the angle
3. **The Spike** — The specific, evidence-backed thing that makes them extraordinary. Must contain numbers/benchmarks, not adjectives
4. **Growth Trajectory** — Dated milestones with acceleration analysis
5. **What They'd Build** — Market thesis, competitive landscape, likely approach
6. **Primary Sources** — Direct quotes from their tweets/blog/talks
7. **Network Map** — Key collaborators, likely co-founders, advisor lineage
8. **Timeline & Signals** — When might they be in market? What to watch for?
9. **Risks** — What could make this not work out?
10. **Background** — Compressed to 3-5 sentences
11. **Notes** — Raw intelligence bullets for reference

### What to EXCLUDE
- Coursework projects (every Stanford MS student does these)
- High school activities (debate, robotics, scouts) unless truly exceptional
- Routine honors (Dean's List, cum laude) — only include if top-of-class or national
- LinkedIn-style role descriptions
- Any fact that is baseline for their peer group
- Vague superlatives ("one of the best", "exceptional talent") — replace with evidence

---

## Tier Assignment

After synthesis, assign a tier:

- **Tier 0 (Active Pursuit):** Person is likely to start a company within 6 months. Evidence: departure signals, active thesis development, VC engagement, bio changes. ACTION: Reach out now.
- **Tier 1 (High Conviction):** Extraordinary person who would be backable if they started today, but no immediate signal they're about to. ACTION: Build relationship, check monthly.
- **Tier 2 (Tracking):** Interesting trajectory, worth watching. Not yet at inflection point. ACTION: Index, check quarterly.
- **Tier 3 (Indexed):** Part of a cohort or competition result. Minimal individual research. ACTION: Store, re-evaluate if they surface again.

---

## Background Monitoring (Scheduled)

### Tier 0: Weekly
- Pull last 20 tweets. Flag: keywords ("announcing", "building", "leaving", "stealth", "raising", "hiring"), engagement spikes (>3x avg), VC interactions (replies/follows/QTs from known investors)
- News search: "[name] + [company]" for last 7 days
- LinkedIn title/bio change check

### Tier 1: Monthly
- Pull last 30 days of tweets. Keyword + engagement flag
- News search for last 30 days
- LinkedIn/Twitter bio comparison to stored version

### Tier 2: Quarterly
- News search only. Flag major events: departed, raised, published at top venue

### Output: Consolidated Briefing
```
🔴 URGENT: [name] — [what happened]. ACTION: [what to do]
🟠 UPDATE: [name] — [what changed]. SIGNAL: [what it means]
⚪ NO CHANGE: [names] — nothing notable
```

---

## Demographic Flags

- **Indian / Indian-origin:** Flag in tags. Important for the VC's sourcing thesis.
- Detect from: birthplace, undergrad institution (IIT, BITS, NIT, IISC, DA-IICT), JEE/KVPY results, name patterns (use with caution — always verify with institutional evidence)

---

## Outreach Email Guidelines

Every dossier includes an outreach email draft. The email must be **ultra-high substance** — it should make the person feel that the sender has genuinely put in the work and deeply understands the specific problem or belief they are working on. This is the VC's primary differentiator.

### Structure (strict order)

1. **Who am I?** — One sentence. "I'm Vansh, Partner at Boldcap."
2. **Why am I reaching out?** — Demonstrate deep domain knowledge of their specific area. Name companies, approaches, and technical tradeoffs in their space. Show you've done the research.
3. **What do I know about YOU specifically?** — The intrinsic insight. Reference their specific technical thesis, a specific paper finding, a specific metric, or a specific decision they made. This must be something only someone who genuinely studied their work would know. NOT generic ("your impressive background") — SPECIFIC ("your TOTO finding that video models scale at L(C) = 7.32 × C^{-0.0378} vs GPT-3's 0.0480 exponent").
4. **Next steps** — Casual, low-pressure. "Not sure if you're raising — would love to chat." Offer to write a check with a specific range if appropriate.

### Tone
- **Short.** 4-6 sentences max after the greeting. The bio founder example email is the gold standard length.
- **Conversational, not corporate.** Write like a person, not a fund.
- **Personal connection if authentic.** If there's a genuine personal angle (diagnosed with a disease, used their product, etc.), lead with it.
- **Show the landscape.** Name 3-5 companies/approaches in their space to prove you understand the market. Say what's missing or what you believe.
- **End with specificity.** "I can write $500K-$1M and move fast" is better than "we'd love to explore."

### Anti-patterns (DO NOT)
- Generic compliments ("your impressive work", "your exceptional talent")
- Name-dropping the VC's portfolio unless directly relevant
- Long paragraphs about the fund's thesis
- "I'd love to pick your brain" — offer value, don't extract it
- Formal sign-offs ("Best regards", "Sincerely")

### Template

```
hi {{name}}

I'm Vansh, Partner at Boldcap. [Personal connection if authentic, 1 sentence.]

I've been going deep on [their specific area] — [show landscape: name 3-5 companies/approaches, what's working, what's missing]. [Your specific insight or belief about the space.]

[The intrinsic thing you know about THEM — specific paper finding, specific metric, specific technical decision that shows you've done the work.] [Why this matters / what it unlocks.]

Not sure if you're raising — would love to chat either way. [Specific offer: "I can write $X-$Y and move fast" OR "happy to meet in the Bay Area."]

Vansh
```

### Signing
- Always sign as "Vansh" (not "Best, Vansh" or "Sincerely, Vansh")
- No email signature block

---

## Quality Checklist (Before Publishing)

Before any dossier page goes live, verify:

- [ ] Investment thesis is in the first 3 sentences
- [ ] The spike contains at least one specific number or benchmark
- [ ] At least 2 direct quotes from the person's own words
- [ ] Competitive landscape names at least 3 comparables
- [ ] Growth trajectory has dated milestones
- [ ] No coursework projects or LinkedIn filler
- [ ] Background section is ≤5 sentences
- [ ] Tier is assigned with rationale
- [ ] Recursive discovery surfaced at least 2 connected people
- [ ] Indian demographic flag checked
