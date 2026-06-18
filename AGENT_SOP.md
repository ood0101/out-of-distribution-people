# Agent SOP: Out of Distribution People Research System

## Purpose
This document defines the standard operating procedure for research agents that build dossiers for an inception-stage VC identifying the most talented people who are truly out of distribution — BEFORE they're obvious to the market.

## Core Principle
**Every dossier must answer one question: what is the *alpha* — the specific, rare, hard-to-replicate edge in this person's actual work, and is it genuinely special *measured against the closest comparable work*?** That is the judgment, and it is what the dossier is organized around.

Whether someone is "building right now," just reached out, or just started a company is an **actionability filter** — it sets the tier and decides whether to reach out — it is **NOT a measure of the person.** Lots of people start companies and are reachable; that alone is not signal. Do not let the tier/inflection question become the spine of the dossier (the historical failure mode: the whole document drifts into justifying a tier, and "are they founding" stands in for "are they exceptional"). **Center the alpha. Demote tier/timing to a quiet tag and a one-line factual status.** Everything else is supporting evidence for the alpha.

---

## Agent Architecture: 6 Parallel Agents Per Person

When researching a new person, launch ALL SIX agents simultaneously. Total time = slowest agent (~5 min), not sum of all agents.

### Agent 1: The Alpha (Technical Deep Dive)
**Mission:** Find, articulate, and STRESS-TEST the *alpha* — the one specific, rare, hard-to-replicate edge in their actual work — and prove (or disprove) it's special by benchmarking against the closest comparable work. This is the most important agent; its output is the spine of the dossier.

**Instructions:**
- **State the alpha in one sentence:** the non-obvious thing they can do / have done that the 20 people who look similar on paper cannot. Then back it with evidence.
- **Benchmark it.** Name the 2–3 closest comparable works/methods/people. Is their contribution actually first / SOTA / structurally novel, or incremental dressed up? Be specific about the mechanism of the edge (the "closed-form Bayesian update," the "single causal assumption," etc.), not just that it's "impressive."
- What did they specifically build? Find benchmark numbers, model sizes, SWE-bench scores, citation counts, GitHub stars
- What was their EXACT role? Architect? Team lead? One of many contributors? Find evidence (commit history, paper authorship position, press quotes) — credit by authorship position; do not over-credit middle/last authorship
- **Calibrate honestly, in this section:** what about the alpha is validated vs. unproven? A thin or early-career alpha must read as thin — the alpha-first frame should EXPOSE when the answer is "not much special yet," not paper over it.
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

## Synthesis: Alpha-First Format

After the agents return, synthesize into this structure. The dossier is organized to answer **what's special about the work, vs. the field** — NOT to justify a tier. Gold-standard example: `people/toon-van-de-maele.html`.

### Page Structure (in order)

1. **One-liner** — Lead with the **alpha** (the rare edge in the work), stated densely. Put role/status as a short *trailing* clause (e.g. *"Status: co-founder & Head of AI of X (stealth, pre-funding)"*) — never as the headline.
2. **The Alpha** (the lead section) — The single most differentiated thing about their work, stated precisely and **benchmarked against the 2–3 closest comparables**: actually first / SOTA / structurally novel, or incremental? Name the comparable work; name the *mechanism* of the edge. Put the honest calibration (validated vs. not) **here**, not as an afterthought. The section the whole dossier exists to support.
3. **How it stacks up** — A tight table: *their work │ closest comparable │ the edge that's actually theirs.* Makes "vs. things which are similar" explicit. (Fold into prose only if there's genuinely a single comparison.)
4. **The Spike — the evidence behind the alpha** — Authorship-precise: papers with position (1st/2nd/middle/last), venue, year, cites. Numbers, not adjectives. This *feeds* the alpha; it is not the headline.
5. **Origin & Trajectory** — Dated milestones, education/lineage, the root of the spike (see Human Layers).
6. **Status & timing** (demoted, factual) — One short block: current role, founding/stealth status (verified vs. reported), reachability, the outreach angle. **NO tier-justification prose.** The tier rides along only as a quiet tag for the table (see Tier Assignment).
7. **Network Map & Recursive Discoveries** — Collaborators, likely co-founders, advisor lineage, recursive leads with priority.
8. **Notes** — Verification + calibration bullets (what's confirmed, what's hedged, what's NOT padded).

Plus the **Human Layers** (Origin-Spike + Life-Texture) per their section below.

### What to EXCLUDE
- Coursework projects (every Stanford MS student does these)
- High school activities (debate, robotics, scouts) unless truly exceptional
- Routine honors (Dean's List, cum laude) — only include if top-of-class or national
- LinkedIn-style role descriptions
- Any fact that is baseline for their peer group
- Vague superlatives ("one of the best", "exceptional talent") — replace with evidence

---

## Tier Assignment

Tier is a **quiet triage/sorting tag for the directory table — it is NOT the dossier's organizing principle.** Assign it, store it in the canonical `tier-N` tag span (the table reads it), and otherwise keep it out of the dossier prose: a one-line factual "Status & timing" block replaces every "T0 because…" paragraph. Tier answers *when/whether to act*; the dossier answers *how special the work is*. The two are orthogonal — a thin-alpha person can be T0 (about to found) and a world-class alpha can be T3 (settled, no inflection); say both honestly and never let the tier inflate or deflate the alpha read.

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

## Discovery Queue & Triage Pipeline

### How It Works
Every deep dive dossier generates recursive discoveries (Agent 6). Those discoveries accumulate in `data/discovery_queue.json`. A daily briefing presents ALL pending people for the owner's yes/no decision.

### Queue File: `data/discovery_queue.json`
Each entry includes: name, one-liner, source dossier, spike signal, Indian-origin flag, departure signal, current company, status (`pending` / `approved` / `researched` / `rejected` / `deferred`).

### Daily Triage Briefing
Format the pending queue grouped by signal type:

```
🔴 DEPARTURE SIGNALS (left non-negotiable company):
  → Guodong Zhang — xAI co-founder, led Grok Code/Imagine, departed Mar 2026
    Spike: Led two flagship xAI products. Active founding signal.
    [yes / no / later]

🇮🇳 INDIAN PIPELINE:
  → Shubham Goel — IIT Bombay + Malik PhD + xAI. 3D reconstruction.
    Spike: Same team as Ravishankar/Patel. Watch for departure.
    [yes / no / later]

🔬 RESEARCH FRONTIER:
  → Charlie Snell — THE paper on test-time compute scaling (ICLR 2025 Oral)
    Spike: Most-cited work in the paradigm. Berkeley PhD.
    [yes / no / later]
```

### Owner's Decision
- **yes** → Full 6-agent SOP. Dossier page. Index card. Their recursive discoveries feed back into queue.
- **no** → Marked `rejected`. Won't resurface unless new signal emerges.
- **later** → Marked `deferred`. Resurfaces in 30 days or when new signal detected.

### What the Owner Scans For (from their own words)
1. **Early spike** — is there something that stands out?
2. **Paper credibility** — has the research they've done shown real impact?
3. **Entrepreneurial potential** — signals they could start something
4. **Rate of change** — is their growth curve significantly steeper than peers?

### The Flywheel
Every "yes" generates ~5-10 new discoveries → queue grows → next triage → more "yes" → more discoveries. The pipeline self-compounds. The owner only spends 5 minutes/day on triage. The system does everything else.

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


---

## The Human Layers: Origin-Spike + Life-Texture

Two research layers, run alongside the 6-agent investment dive. The investment dive finds the *spike*. These two layers find the *root of the spike* and the *person around it*. Run both for every Tier 0/1 dossier; run Layer A at minimum for Tier 2.

---

### Layer A — Origin & Early Spike

**WHY:** The investment spike (papers, departures, funding) tells you the person is extraordinary now. Layer A tells you *why they were always going to be* — the causal root, the "you could see it early" story. It is the single most convincing thing in an outreach email and the best predictor of whether the current spike is a fluke or the latest point on a 15-year line. Critically, it is where the owner's Indian-sourcing thesis lives: the highest-signal version is **achievement despite no scaffolding** — a teenager running a global research community from Chandigarh, a 14-year-old winning a 200-team hackathon with no accelerator behind them. Do not let this layer collapse into "prodigy won a competition." Weight the *absence of advantage* as heavily as the achievement.

**WHAT TO FIND (checklist):**
- [ ] Earliest dated achievement (the floor — "first email at 5," "programming at 8," "led a 15-person company at 16")
- [ ] The conceptual ancestor of their current work (does today's company trace to a teenage project?)
- [ ] Upbringing/context, especially scaffolding-or-not (Tier-2/3 city, no lab access, immigrant/first-gen, self-funded on a small grant)
- [ ] Community-building before it was professional (ran a Discord/club/workshop, wrote curriculum, curated a resource list for others)
- [ ] Polymath / clarity-of-thought signals (quantifies the un-quantified, cross-domain fluency, an unusual deliberate choice)
- [ ] Lineage echoes (2nd-gen fellow, parent in the field, advisor they cold-emailed at 16)
- [ ] Video/talk/podcast presence — the literal "see it early" artifact
- [ ] Persistent online identity (a handle carried from a teen repo into professional work)

**WHERE TO LOOK (source-type playbook):**
- **Hometown / school student newspapers** → the richest single source for the pre-fame arc; names the teenage project, the motivation, the team. (saratogafalcon.org, Horace Mann news, school alumni notes)
- **Competition archives** → ISEF/STS, FRC/FTC Dean's List, IOI/IMO/Putnam, regional science fairs — and reconcile the *exact* prize/category (these are routinely garbled across summaries).
- **Old GitHub (scroll to first repos) + Wayback on personal sites** → raw-CUDA-CNN-with-no-framework, teen tool repos, the handle that persists.
- **arXiv / Nature Methods / lab reprints under their teen name** → real systems papers written at 16-17, not school projects.
- **YouTube / podcasts** → science-fair explainer videos (often later set Private — note existence + title even if gated), long-form lab podcasts where you can *hear* the thinking.
- **Niche-community founding posts** → LessWrong/Discord/forum threads that timestamp who actually founded vs. co-built a community (credit precisely — see Evidence Discipline).
- **Music-school / arts / debate archives, religious-community press** → cross-domain and "despite/alongside" signals.

**WORKED EXAMPLE — Mason Wang (Origin & Early Spike).**
The gem: at ~14, freshman Mason led **Archiscape to 1st of 200+ submissions at LA Hacks (March 2020)**, a virtual-house-tour tool "inspired by Mason's mother, a realtor" — the literal conceptual ancestor of **Hazel**, the realtor-AI company he raised $2M from Pear VC for at 17, three years later. The source-type that surfaced it: a **hometown student newspaper** (saratogafalcon.org) — not Crunchbase, not his site. The causal arc (mother's profession → teen hackathon win → funded company) only exists in the local-press record. *Teaching point: the student paper is the first place to look and the last place agents think to check.*

---

### Layer B — Life & Texture

**WHY (both halves — neither alone is enough):** (1) **Outreach.** A note that knows the person plays cello recitals or walked the full length of Manhattan lands as written by someone who actually paid attention, not a fund running a template. (2) **Network intelligence.** Who they live with, train with, and hang out with are *mappable edges*. A 5am workout club is a co-founder relationship; a roommate is a warm intro. Texture is not small talk — it is the social graph rendered in human terms. Capture both or the layer is half-done.

**WHAT TO FIND (checklist):**
- [ ] Hobbies pursued seriously (instrument + level, sport, a 30-mile walk, turtle conservation)
- [ ] Where / with whom they live — **only where publicly disclosed** (see Privacy Boundary)
- [ ] Co-located relationships that are also professional edges (co-founder who's also a brother / roommate / workout partner; a club member who's also a VC)
- [ ] Hangouts/communities (running club, founder house, a recurring hackathon crew)
- [ ] Fitness footprint (Strava club/route, a race result) — *if public*
- [ ] Online personality (bio location jokes, in-group humor, scrape-warnings) — quote it
- [ ] Media/taste tells (Letterboxd, Goodreads, the tools they unwind with — Geoguessr, Radio Garden)

**WHERE TO LOOK (source-type playbook):**
- **Music-school recital archives / arts-org pages** → instrument, years of training, *and* who they perform with (often a family member or future co-founder).
- **Club / community sites + their team/about pages** → the workout club or founder house, and crucially the *other members* (cross-reference each against VC/founder rolls).
- **Their own "about" / "now" / personal-essay pages** → the 30-mile-walk, the unwind tools, the rare vulnerable line — quote verbatim.
- **Strava / Letterboxd / Goodreads** → fitness and taste; expect login-gating — record only what's genuinely public, never fabricate a route or race time.
- **Instagram / X bios and pinned content** → personality and location jokes; many are gated — note the handle, mark content unverified if you can't load it.
- **Friends'/co-founders' public posts and podcasts** → texture about the person that they don't post themselves (origin of a friendship, a gap-year story).

**WORKED EXAMPLE — Ben Spector (Life & Texture).**
The gem: Ben has played serious **cello since age 4**, performing chamber music with his brother **Asher** as "The Spector Trio" — and Asher is now his **co-founder at Flapping Airplanes**. The source-type that surfaced it: a **music-school recital archive** (Hoff-Barthelson). This is pure texture (a decade-plus of cello, recital-level at the New England Conservatory) that simultaneously delivers the single most important network fact in his dossier — his co-founder is his brother, and the relationship predates the company by ~20 years. *Teaching point: the arts archive is where the deepest network edge was hiding in plain sight.* (Compare Mason Wang's Victory Club, a 5am workout club whose co-member Sam Beskind is a Floodgate Associate and Chief of Staff to Mike Maples Jr. — a warm founder↔VC bridge found via the club's own team page.)

---

### PRIVACY BOUNDARY (strict — read before writing either layer)

The governing heuristic: **include only the texture a warm acquaintance would already know.** If a stranger shouldn't know it, neither should the dossier.

- **Public-only.** Every fact must trace to a public, citable source (their site, a news piece, a public club page). If it required gating, guessing, or inference about a private detail, it is out.
- **Hard NO — never include, even if findable:** home addresses or precise location; phone/email/PII; financial details (personal net worth, exact equity, salary, undisclosed valuations); health, medical, or family-private matters; religious/political specifics beyond what *they* have made public; anything harm-enabling or that aids stalking/doxxing.
- **The "where/with-whom they live" tension — resolved, not waved away.** This is both Layer B's network ask *and* its highest privacy risk. Rule: a **publicly disclosed** arrangement involving public figures is OK (a named, press-covered founder house; a co-founder who has publicly stated they're roommates). **Inferred private cohabitation is NOT** — e.g., "Ben lives with ~3 others including Cursor's first hire" was plausible from density alone but had no public source; it stays **flagged, not stated**. Likewise "eats at Mahalo" could not be sourced to him and is left out.
- **Flag-don't-include.** When something is borderline-private or merely plausible, do not assert it. Note it in internal research notes as "unconfirmed / borderline-private — not for dossier" and move on. The bar for Layer B facts is *higher* than for the investment spike, not lower.

### EVIDENCE DISCIPLINE (these layers embellish the easiest — verify the juicy stuff)

Origin and texture gems are the most repeated and the least sourced. The juicier the gem, the harder you verify it.

- **Quotes, dates, links over adjectives.** "Walked Met Cloisters to Battery Park; unwinds with Geoguessr and Radio Garden (his about page)" beats "an interesting, curious person." Every gem carries its source-type.
- **Flag the unverified explicitly — don't launder it into fact.** Cautionary cases from the first run: Ben Spector's **"Cofactory AI co-founder"** is asserted as fact in three places in the live file off a single thin link — mark it *plausible, unconfirmed*, not fact. The **"~10% equity / ~$2.5B Cursor offer"** is widely repeated lore with no primary source. The **"~$50B combined ecosystem valuation"** conflates portfolio valuation with money he raised (~$25M per Hertz). State each as exactly what it is.
- **Attribute community/founding claims with precision.** Kunvar Thaman did **not** found the mech-interp Discord — Victor Levoso did (founding LessWrong post, Mar 12 2023); Thaman was a co-builder. And ~512 of his ~549 Scholar citations are HLE *contributor* credit, not his own papers. Get the role right; "co-built" and "founded" are different facts.
- **Distinguish self-description from independent verification.** "Principal developer of ESM-1b" (Josh Meier's own bio) vs. "2nd author on Rives et al. 2019" (the paper) — cite the verifiable one. "CEO of Chai" is unconfirmed; "co-founder, one of four" is sourced.
- **Beware the namesake.** Common names (Benjamin Spector, Kunvar Thaman) attract false-positive papers and profiles. Confirm identity via place/time/co-author/handle before attaching a claim. The "fuzzy-logic interpretability" Neurocomputing paper is a different Thaman — do not cite.
- **Gated ≠ confirmed.** Private YouTube videos, login-walled Strava/Instagram, rate-limited Manifund pages: record the title/handle and the fact that it exists, mark the *content* unverified, and never invent the inside.

---

### Transcript Mining — the highest-yield, most-missed source

**The failure mode this fixes (observed, real):** a research agent correctly found the single best video on Ben Spector (Stanford Hidden Layer Podcast #103) and even labeled it "the best 'you can hear it' asset" — then **could not extract a single fact from it**, because it had no way to listen. The richest intel about exceptional people is *said out loud and never written down*. The gap is never discovery; it is **extraction**.

**The fix — a standing capability.** `scripts/transcript.py <youtube_url>` (yt-dlp under the hood) turns any YouTube/podcast video into a clean, timestamped, deduplicated transcript in ~2 seconds. Mine it with `--grep "term1,term2"` or `--around <seconds>`.

```
python3 scripts/transcript.py "https://youtube.com/watch?v=XXXX" --out /tmp/p.txt
python3 scripts/transcript.py "<url>" --grep "grew up,founded,my brother,new lab"
```

**MANDATORY for every Tier-0/1 dossier:** after the origin/texture agents name the best 1–3 video/podcast appearances, PULL THE TRANSCRIPTS and mine them before writing. Do not file a high-conviction dossier with an un-listened-to flagship interview sitting in the sources.

**What only the tape gives you (worked example — the SAME video the agent couldn't use):**
- The Cursor founding story in his own words: *"I was actually on the original founding team of Cursor, although I left very early."* (text-only had only "early contributor")
- The "Cursor wanted him back" lore, sourced: Cursor's President on record — *"We've tried to get him back multiple times."*
- The network edge, said openly: he lives in a 4-person house on the Filbert Steps with **Cursor's President + a Cursor co-founder + his brother** — the exact roommate-graph that was previously "borderline-private, no public source."
- The cello hobby, corroborated by a housemate: *"He plays cello at midnight."*

**WHERE THE SPOKEN WORD LIVES:**
- **YouTube** (podcasts, conference talks, lab channels, "fireside chats") → `transcript.py` directly.
- **Podcasts not on YouTube** (Latent Space, No Priors, the Hidden Layer, a16z, Lightcone) → most mirror to YouTube (find that URL); many also publish transcripts on their own site — check first.
- **Substack / newsletters** → `site:substack.com "<name>"`, plus The Information / Stratechery / personal newsletters where founder profiles and asides live.
- **Twitter/X Spaces, Discord stages, livestreams** → often archived to YouTube afterward.

**LORE TOLERANCE — calibrated.** The owner is fine with lore, *because some of the best signal only exists in spoken/social form and no one writes it on a profile.* But distinguish sharply:
- **Spoken-word self-statement on a recorded podcast = PRIMARY SOURCE**, not lore. Cite it as *"his own words, [podcast], [timestamp]."* This is the strongest tier of human-layer evidence.
- **Genuine unsourced rumor** (e.g., a specific "~10% / $2.5B offer" figure with no recording or document) = **flag as lore**, include if useful but never launder into fact. The tape may source the *qualitative* claim ("they tried to get him back") while the *specific number* stays lore — state each as exactly what it is.

---

### The Read — calibrated inference (a third human layer)

Facts tell you what someone did. **The Read** tells you what it means — a falsifiable thesis about what actually drives them (ambition, values, what they're optimizing for, what they'll do next). This is the highest-value, highest-risk layer; it is where a VC's judgment lives, and where bullshit lives if you're sloppy.

**RULES:**
- **Flag it as interpretation, always.** A dossier section titled "The Read — interpretation, not fact." Never blend inference into the factual record.
- **Ground every claim in declined/chosen evidence.** The strongest reads come from what someone *turned down*. Worked example (Ben Spector): "optimizing for the highest-ceiling problem, not the biggest outcome" — evidenced by *passing on Cursor* (founding team, asked back "multiple times" per its President, said no as it hit tens of billions) + *leaving the PhD to start a research lab* (not a product company) on a fundamental anti-scale thesis. The read is the line connecting the choices.
- **State the falsifiers.** End every Read with "what would prove this wrong" (e.g., "if Flapping Airplanes pivots to an applied product; if he rejoins Cursor"). A read without falsifiers is a horoscope.
- **Keep lore lore.** If the read leans on an unverified claim (the "~10% offer"), say the qualitative part is sourced and the number isn't.
- **It changes outreach.** The Read tells you the *way in*: for Ben, lead with the problem (data-efficiency, anti-scale), never the money or the logo.

### Pedigree Pools — mine the filters, not just the people

Exceptional people cluster in a handful of high-precision selection filters. When a pool keeps recurring across the people you already rate, the *pool itself* is a sourcing vein — pull the full roster, cross-reference the index, surface the un-indexed names + their "vicinity" (cohort-mates, the people one hop away).

**Pools that recur in OUR index (count = people already indexed who hold it) — mine these:**
- **Hertz Fellowship** (6) — tiny annual cohort (~15), extreme technical density. Ben, Ishaan Javali, Kunvar Thaman, Vikram Sundar, Galen Mead, Devansh Pandey.
- **RSI / Research Science Institute** (6) — ~80 high-schoolers/yr, the most selective summer research program.
- **FRC / FIRST Robotics Dean's List** (4) — Ben was 1 of ~4 worldwide/yr; a tiny, builder-flavored filter.
- **Coolidge Scholars** (1), **Davidson Fellows** (3), **Knight-Hennessy** (7), **Coca-Cola Scholars** (4), **Cutler-Bell ACM** (4), **Soros New Americans** (2), **Schmidt Science** (3).
- **DEPRIORITIZED (owner call): Neo Scholars** — ~30 strong CS students/yr; less rarefied than Hertz/RSI and a talent-program rather than an outcome filter. Skip as a primary mining pool; a Neo signal counts only when paired with a sharper one (competition pedigree, Hertz/RSI).
- (Already in the SOP as competition pools: IMO 28, IOI 27, Putnam 15, ISEF 13, Regeneron STS 11.)

**MINING METHOD (per pool):** (1) get the public roster (foundation site, Wikipedia, press); (2) cross-reference against the index (slug/name match); (3) for un-indexed names, run a Depth-0 triage (worth-tracking?); (4) capture cohort-mates of our best people as recursive discoveries — the person who shared a Hertz year or an RSI summer with someone we love is "in the vicinity."

### Video Census — find ALL of them, not one

When pulling video intel (see Transcript Mining), do a CENSUS first: `yt-dlp "ytsearch10:<name> <topic>"` across 3-4 query phrasings to enumerate every substantive appearance, then transcribe the high-value ones. We initially mined 1 of Ben Spector's 3 substantive videos and missed a 4.5-hour live session and a 75-min AMA. One flagship interview is a start, not coverage. Beware namesakes in search results (SNL/Minecraft/luthier hits were not him).
