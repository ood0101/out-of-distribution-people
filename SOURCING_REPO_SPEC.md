# OOD Sourcing Repo — Build Specification

## What This Is
A scouting/lead-generation repository that casts a wide net across competition results, lab alumni, fellowship cohorts, and departure signals to identify exceptional technical people BEFORE they're obvious. This feeds into the main `out-of-distribution-people` repo (the curated investment database) via a promotion flow.

## Relationship to Main Repo
```
ood-sourcing (this repo, 2000+ people, wide net)
    │
    │  User says "Promote [name], Tier X"
    │  or monitoring recommends promotion
    │
    ▼
out-of-distribution-people (curated, 200-500 people, deep dossiers)
```

The sourcing repo is a RESERVOIR. Most people here will never be promoted. The value is in having them indexed so when a name comes up, you can instantly see their competition history, lab affiliation, and current status.

## Tech Stack
- Static HTML, same aesthetic as the main repo
- CSS: `--bg: #fafaf8`, `--accent: #c43d2e`, Georgia serif headings, monospace labels, Inter sans-serif body
- Max-width 920px
- Search + filter across all sections
- Dense table format (not individual dossier pages)
- GitHub Pages for hosting

## Directory Structure
```
ood-sourcing/
├── index.html                    (master search + filter + links to all sections)
├── style.css                     (shared styles)
├── CLAUDE.md                     (project memory)
├── .nojekyll
├── competitions/
│   ├── ioi-gold.html             (IOI gold medalists 2015-2024)
│   ├── ipho-pivots.html          (IPhO gold medalists who pivoted to CS/AI)
│   ├── imo-gold.html             (IMO gold/silver medalists 2015-2024)
│   ├── icpc-finals.html          (ICPC World Finals top 5 teams + individuals)
│   ├── putnam-fellows.html       (Putnam Fellows + top 10, last 10 years)
│   ├── usamo-mop.html            (USAMO winners / MOP participants)
│   ├── sts-finalists.html        (Regeneron STS top 40, last 10 years)
│   ├── isef-grand-awards.html    (ISEF Grand Award + Best of Category)
│   ├── usabo-ibo.html            (Biology Olympiad gold → comp bio pivots)
│   └── icho.html                 (Chemistry Olympiad gold → comp chem pivots)
├── labs/
│   ├── chris-re.html             (Hazy Research alumni, last 5 years)
│   ├── percy-liang.html          (Stanford CRFM alumni)
│   ├── pieter-abbeel.html        (Berkeley BAIR alumni)
│   ├── kaiming-he.html           (MIT, prev FAIR, alumni)
│   ├── song-han.html             (MIT EfficientML alumni)
│   ├── tri-dao.html              (Princeton, prev Stanford, alumni)
│   ├── christopher-manning.html  (Stanford NLP alumni)
│   ├── ion-stoica.html           (Berkeley Systems alumni)
│   ├── sergey-levine.html        (Berkeley RL for robotics alumni)
│   ├── chelsea-finn.html         (Stanford meta-learning alumni)
│   ├── tengyu-ma.html            (Stanford theory alumni)
│   ├── stefano-ermon.html        (Stanford diffusion/generative alumni)
│   └── ludwig-schmidt.html       (UW/Stanford, DataComp alumni)
├── departures/
│   └── log.html                  (monthly departure log from 20 tracked companies)
├── fellowships/
│   ├── thiel-fellows.html        (all cohorts 2011-2025)
│   ├── hertz-fellows.html        (recent Hertz Fellows in CS/ML)
│   ├── knight-hennessy.html      (KH Scholars in STEM)
│   └── neo-scholars.html         (Neo Scholar cohorts)
└── data/
    └── promoted.json             (tracks who's been promoted to main repo)
```

## Page Format: Dense Searchable Tables

Each page should have:
1. A title and one-line description
2. A search input that filters the table
3. A dense HTML table with columns specific to the data type

### Competition Page Format
```html
<table>
  <thead>
    <tr>
      <th>Name</th>
      <th>Country</th>
      <th>Year(s)</th>
      <th>Medal</th>
      <th>Current Affiliation</th>
      <th>Status</th>
      <th>Links</th>
    </tr>
  </thead>
  <tbody>
    <tr data-status="startup" data-country="usa">
      <td><strong>Walden Yan</strong></td>
      <td>USA</td>
      <td>2020</td>
      <td>Gold</td>
      <td>Co-founder & CPO, Cognition AI ($10.2B)</td>
      <td><span class="status-tag startup">at startup</span></td>
      <td><a href="...">Twitter</a> <a href="...">LinkedIn</a></td>
    </tr>
    ...
  </tbody>
</table>
```

Status tags: `at startup`, `frontier lab`, `stealth`, `quant`, `phd`, `undergrad`, `unknown`

Indian-origin people should have an `indian` data attribute for filtering.

### Lab Alumni Page Format
```html
<table>
  <thead>
    <tr>
      <th>Name</th>
      <th>Degree</th>
      <th>Graduated</th>
      <th>Thesis/Focus</th>
      <th>Current Affiliation</th>
      <th>Status</th>
      <th>Links</th>
    </tr>
  </thead>
  ...
</table>
```

### Departure Log Format
```html
<table>
  <thead>
    <tr>
      <th>Name</th>
      <th>Left</th>
      <th>Previous Company</th>
      <th>Previous Role</th>
      <th>Now</th>
      <th>Date</th>
      <th>Links</th>
    </tr>
  </thead>
  ...
</table>
```

## Pre-Researched Data to Populate

### IOI Gold Medalists (2018-2024) — Ready to Index

#### Multi-Gold Medalists
| Name | Country | Gold Years | Current Affiliation |
|------|---------|------------|-------------------|
| Rain Jiang | USA | 2021, 2023, 2024, 2025 | Homeschooled; publishes CS theory with his father. 4 golds — most ever for American |
| Zixiang Zhou | Canada | 2019, 2020, 2021, 2022 | 4 golds. Likely University of Waterloo |
| Patrick Pavic | Croatia | 2020, 2021, 2022 | 3 golds. Unknown current |
| Nikoloz Birkadze | Georgia | 2018, 2019, 2020 | 3 golds. MIT |
| Masataka Yoneda | Japan | 2018, 2019, 2020 | 3 golds. Unknown |
| Daiki Kodama | Japan | 2021, 2022, 2023 | 3 golds. Unknown |
| Daniel Weber | Israel | 2022, 2023, 2024 | 3 golds. Unknown |
| Benjamin Qi | USA | 2018 (1st), 2019 (1st) | MIT BS CS. Creator of USACO Guide |
| Eric Zhang | USA | 2018, 2019 | Modal (engineer, #1 committer 3.5+ years). Also IPhO triple gold |
| Kshitij Sodani | India 🇮🇳 | 2023, 2024 | MIT CS. Founded Algoplanet. Codeforces IGM (2736). Already in main repo (Delta) |
| Agastya Goel | USA (Indian-origin 🇮🇳) | 2023, 2024 | Gunn High School, Palo Alto. Also IPhO 2025 gold. Son of IIT-JEE 1990 topper |
| Ildar Gainullin | Russia | 2019, 2020 | Lives/studies in Canada |
| Dorijan Lendvaj | Croatia | 2021, 2022 | University of Zagreb |

#### At Startups or Frontier Labs (Highest Priority)
| Name | Country | Gold Years | Where Now |
|------|---------|------------|-----------|
| Walden Yan | USA | 2020 | Co-founder & CPO, Cognition AI ($10.2B). Thiel Fellow. Dropped out of Harvard. Prev Cursor |
| William Lin | USA | 2020 (perfect 600/600) | Engineer at Pika (AI video). MIT '24 |
| Eric Zhang | USA | 2018, 2019 | Modal (cloud infra for AI). #1 committer 3.5+ years |
| Ziqian Zhong | China | 2019 | CMU (AI safety research). Previously Research Scientist at Pika, led Pika 2.0 |
| Mingyang Deng | China | 2021 (perfect 600/600) | MIT CSAIL PhD (Kaiming He's group). Already in main repo (Delta) |
| Rohin Garg | USA | 2023 | Character.AI + MIT |
| Spencer Compton | USA | 2018 | Stanford PhD (CS theory) |
| Kasra Mazaheri | Iran | 2020 | Citadel (quant) |

#### Indian IOI Gold (2018-2024)
Only one: Kshitij Sodani (2023, 2024). Already in main repo.
Agastya Goel (2023, 2024) is Indian-origin but competed for USA.

#### Key Pattern: Cognition AI
Cognition (Devin, $10.2B) is the most IOI-dense company: Scott Wu (3x gold, 2013-15), Steven Hao (1x gold, 2014), Walden Yan (1x gold, 2020). Early 10-person team held 10 combined IOI golds.

### IPhO Gold Medalists → CS/AI Pivots — Ready to Index

#### Confirmed Founders
| Name | Country | IPhO Year | Where Now |
|------|---------|-----------|-----------|
| William Huang | USA | 2021 (Rank 40) | CEO & Co-founder, Sylvian (YC F25). Stanford |
| Elias Hohl | Austria | 2021 (Rank 27) | CEO & Co-founder, CryptoSearchTools AG (ETH Zurich AI Center). 7 international medals |

#### At Frontier Labs / Elite AI Research
| Name | Country | IPhO Year | Where Now |
|------|---------|-----------|-----------|
| Rahul Arya | Hong Kong | 2018 (Rank 28) | Google DeepMind |
| Alex Gu | USA | 2022 (Rank 24) | MIT CSAIL PhD (Solar-Lezama). LLMs for code. Already in main repo (Delta) |
| Zhening Li | USA | 2021 (Rank 7) | MIT CSAIL PhD (Solar-Lezama). MIT Presidential Fellow. NeurIPS 2025. Already in main repo (Delta) |
| Zian Shi | USA | 2023 (Rank 16) | MIT — BS in AI + Physics. Also EuPhO gold |

#### Physics → Quant Pipeline
| Name | Country | IPhO Year | Where Now |
|------|---------|-----------|-----------|
| Pawan Goyal | India 🇮🇳 | 2018 (Rank 7) | Two Sigma. MIT CS+Econ. JEE AIR 4 |
| Lay Jain | India 🇮🇳 | 2018 (Rank 12) | Two Sigma. MIT EECS. KVPY AIR 1, JEE AIR 9 |
| Nishant Abhangi | India 🇮🇳 | 2018 + 2019 | Sunrise Futures (quant). Two-time gold |
| Vincent Bian | USA | 2019 (Rank 6) | Citadel Securities. MIT |
| Collin Fan | USA | 2023 (Rank 5, Best Experiment) | Citadel Securities / Harvard Physics+CS |

#### Indian IPhO Gold Complete Map
| Name | Year | Rank | JEE Rank | Where Now |
|------|------|------|----------|-----------|
| Pawan Goyal | 2018 | 7 | AIR 4 | Two Sigma, MIT |
| Lay Jain | 2018 | 12 | AIR 9 | Two Sigma, MIT |
| Nishant Abhangi | 2018+2019 | 31, 9 | — | Sunrise Futures |
| Archit Bubna | 2019 | 22 | AIR 3 | IIT Delhi |
| Deevyanshu Malu | 2022 | 20 | AIR 11 | Likely IIT |
| Mehul Borad | 2023 | — | AIR 25 | IIT Bombay |
| Rhythm Kedia | 2024 | 15 | AIR 4 | IIT Bombay CS |
| Ved Lahoti | 2024 | 17 | AIR 1 | MIT (transferred from IIT Bombay) |

#### Key Pattern: Quant Trap
Indian IPhO gold medalists overwhelmingly follow: IPhO Gold → JEE Top 10 → IIT Bombay CS → MIT → Two Sigma/Citadel. The ones who break this pipeline are highest-alpha.

### Full IOI Gold Lists by Year (2018-2024)

Complete lists with scores available for all 7 years (~210 gold medalists total).
Top scorers per year with exact scores:
- 2024: Kangyang Zhou (China) 600 perfect
- 2023: Tingqiang Xu (China) 580, Siyuan Cheng (China) 579
- 2022: Jiangqi Dai (China) 600 + Shaoxuan Tang (China) 600 (dual perfect)
- 2021: Mingyang Deng (China) 600 perfect
- 2020: William Lin (USA) 600 perfect
- 2019: Benjamin Qi (USA) 547
- 2018: Benjamin Qi (USA) 499

Full year-by-year lists with all 30 gold medalists per year, scores, and countries are available in the research output files at:
- /private/tmp/claude-502/-Users-vansh-out-of-distribution-people-repo/85bfcc60-0677-4d6d-9a23-0371c8d94bf6/tasks/aa165ffd7ac74b5f2.output (IOI full data)
- /private/tmp/claude-502/-Users-vansh-out-of-distribution-people-repo/85bfcc60-0677-4d6d-9a23-0371c8d94bf6/tasks/a6ed312b513a38017.output (IPhO full data)

## Data Still Needed (Research Required)

### Competitions — Not Yet Researched
1. **IMO Gold/Silver (2015-2024)** — ~150 gold medalists. Cross-reference with current CS/AI affiliations
2. **ICPC World Finals (2018-2024)** — top 5 teams per year, identify individuals. Cross-reference
3. **Putnam Fellows + Top 10 (2015-2024)** — ~50 people. Cross-reference
4. **USAMO/MOP participants (2018-2024)** — the IMO pipeline. Cross-reference with who went to CS
5. **Regeneron STS Top 40 (2016-2025)** — ~400 people. Focus on CS/AI projects
6. **ISEF Grand Awards in CS/Math/Physics (2018-2024)** — identify who's now in AI
7. **Codeforces International Grandmasters (2600+)** — ~200 people globally. Where are they?
8. **USABO/IBO gold → comp bio** — emerging signal for bio-AI founders
9. **IChO gold → comp chem/materials AI** — same pattern

### Labs — Not Yet Researched
For each lab, need to scrape the "People" or "Alumni" page and cross-reference:
1. Chris Ré (Stanford, Hazy Research) — hazyresearch.stanford.edu/people
2. Percy Liang (Stanford, CRFM) — crfm.stanford.edu/people
3. Pieter Abbeel (Berkeley, BAIR) — people.eecs.berkeley.edu/~pabbeel/
4. Kaiming He (MIT) — people.csail.mit.edu/kaiming/
5. Song Han (MIT) — songhan.mit.edu/team/
6. Tri Dao (Princeton) — tridao.me/
7. Christopher Manning (Stanford NLP) — nlp.stanford.edu/people/
8. Ion Stoica (Berkeley) — people.eecs.berkeley.edu/~istoica/
9. Sergey Levine (Berkeley) — people.eecs.berkeley.edu/~svlevine/
10. Chelsea Finn (Stanford) — ai.stanford.edu/~cbfinn/
11. Tengyu Ma (Stanford) — tengyuma.github.io/
12. Stefano Ermon (Stanford) — ermon.stanford.edu/
13. Ludwig Schmidt (UW/Stanford) — ludwigschmidt.github.io/

### Fellowships — Not Yet Researched
1. **Thiel Fellows (2011-2025)** — ~300 people. High founder density
2. **Hertz Fellows (recent, in CS/ML)** — very selective
3. **Knight-Hennessy Scholars (STEM)** — Stanford's top fellowship
4. **Neo Scholars** — early-career technologists

### Departures — Not Yet Researched
Weekly monitoring of the 20 tracked companies for departures:
1. OpenAI, 2. Anthropic, 3. Google DeepMind, 4. Meta FAIR / MSL, 5. xAI, 6. Mistral
7. Cursor/Anysphere, 8. Runway, 9. Midjourney, 10. Character AI, 11. Perplexity
12. Scale AI, 13. Databricks (Mosaic), 14. Together AI, 15. Physical Intelligence
16. NVIDIA Research, 17. Tesla AI/Optimus, 18. Apple MLR, 19. Anduril Lattice, 20. Palantir AIP

## Promotion Flow

When a person is promoted from sourcing to main repo:
1. User says: "Promote [name], Tier X"
2. Run full 6-agent SOP (see main repo's AGENT_SOP.md)
3. Create dossier page in out-of-distribution-people/people/
4. Add card to index.html with tier and tags
5. Add to watchlist.json at appropriate monitoring frequency
6. Mark as promoted in ood-sourcing/data/promoted.json:
```json
{
  "walden-yan": {
    "promoted_date": "2026-03-26",
    "promoted_tier": 1,
    "source": "ioi-gold-2020"
  }
}
```

## Monitoring & Refresh

### Competitions: Annual
- After each IOI/IMO/IPhO/ICPC: scrape new results, add to tables
- Quarterly: re-check current affiliations for people already indexed (especially "unknown" status)

### Labs: Quarterly
- Scrape alumni pages for new graduates
- Cross-reference against LinkedIn/Twitter for current status

### Departures: Weekly
- Search "[company] departure" / "[company] leaves" for each of the 20 companies
- Flag anyone not already in either repo

### Recommendations: Quarterly
- Scan the full sourcing repo for status changes
- Surface anyone who went from "phd" → "startup" or "frontier lab" → "stealth"
- Format as promotion recommendations for the user

## Design Notes

- Keep it minimal. Dense tables, not fancy cards. This is a working tool, not a portfolio
- Search bar at the top of every page
- Filter buttons: `at startup`, `frontier lab`, `stealth`, `quant`, `phd`, `indian`
- Each table row should have a subtle indicator if the person is already in the main repo (promoted)
- Mobile-responsive: tables should scroll horizontally on small screens
- No JavaScript frameworks. Plain vanilla JS for search/filter. Same as main repo
