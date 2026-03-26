#!/usr/bin/env python3
"""Build the Delta Institute Fellows HTML digital garden page."""
import json
import html as html_mod

# Load all research data
with open('/Users/vansh/Brainstorming/delta_fellows.json') as f:
    base_data = json.load(f)  # name, affiliation, photo

with open('/Users/vansh/Brainstorming/delta_fellows_profiles.json') as f:
    batch1 = json.load(f)  # 1-25

with open('/Users/vansh/Brainstorming/delta_fellows_26_50.json') as f:
    batch2 = json.load(f)  # 26-50

with open('/Users/vansh/Brainstorming/delta_fellows_51_75.json') as f:
    batch3 = json.load(f)  # 51-75

with open('/Users/vansh/Brainstorming/delta_fellows_76_100.json') as f:
    batch4 = json.load(f)  # 76-100

with open('/Users/vansh/Brainstorming/delta_fellows_101_144.json') as f:
    batch5 = json.load(f)  # 101-144

with open('/Users/vansh/Brainstorming/delta_fellows_companies_research.json') as f:
    companies = json.load(f)

# Build name -> research mapping
research = {}
for batch in [batch1, batch2, batch3, batch4, batch5]:
    for person in batch:
        name = person.get('name', '').strip()
        # Normalize name
        if '(' in name:
            name = name.split('(')[0].strip()
        research[name] = person

# Build company name -> data mapping
company_map = {}
for c in companies:
    company_map[c['name']] = c

def esc(s):
    if not s:
        return ''
    return html_mod.escape(str(s))

def make_list(items):
    if not items:
        return ''
    if isinstance(items, str):
        return f'<p>{esc(items)}</p>'
    return '<ul>' + ''.join(f'<li>{esc(i)}</li>' for i in items[:6]) + '</ul>'

def make_links(person):
    links = []
    for key, label in [('linkedin_url', 'LinkedIn'), ('twitter_url', 'X/Twitter'), ('website_url', 'Website'), ('scholar_url', 'Scholar')]:
        url = person.get(key)
        if url and url != 'null' and url != 'None':
            links.append(f'<a href="{esc(url)}" target="_blank">[{label}]</a>')
    return ' '.join(links) if links else ''

def slug(name):
    return name.lower().replace(' ', '-').replace('(', '').replace(')', '').replace('.', '')

# Categorize fellows
founders = []
frontier_lab = []  # OpenAI, Anthropic, DeepMind, Meta AI
researchers = []  # PhD students, postdocs
quant_finance = []  # Jane Street, HRT, DRW, Jump
rising_stars = []  # undergrads doing exceptional things

for i, base in enumerate(base_data):
    name = base['name']
    aff = base.get('affiliation', '')
    r = research.get(name, {})

    companies_founded = r.get('companies_founded', [])
    if isinstance(companies_founded, list) and len(companies_founded) > 0:
        founders.append(name)

    for lab in ['OpenAI', 'Anthropic', 'DeepMind', 'Meta AI', 'Meta Superintelligence']:
        if lab.lower() in aff.lower():
            frontier_lab.append(name)
            break

    if 'PhD' in aff or 'Postdoc' in aff:
        researchers.append(name)

    for firm in ['Jane Street', 'HRT', 'DRW', 'Jump Trading', 'Jump']:
        if firm.lower() in aff.lower():
            quant_finance.append(name)
            break

# Build HTML
fellow_cards = []
for i, base in enumerate(base_data):
    name = base['name']
    aff = base.get('affiliation', '')
    photo = base.get('photo', '')
    r = research.get(name, {})

    # Get research fields
    problems = r.get('problems_worked_on', [])
    spiky = r.get('what_makes_them_spiky', [])
    key_work = r.get('key_work', [])
    companies_founded = r.get('companies_founded', [])
    current = r.get('current_work', '')
    alpha = r.get('alpha_insight', '')
    links = make_links(r)

    # Tags
    tags = []
    if name in founders:
        tags.append('<span class="tag founder">founder</span>')
    if name in frontier_lab:
        tags.append('<span class="tag frontier">frontier lab</span>')
    if name in researchers:
        tags.append('<span class="tag researcher">researcher</span>')
    if name in quant_finance:
        tags.append('<span class="tag quant">quant</span>')

    # Determine affiliation from research if better
    r_aff = r.get('affiliation', '')
    display_aff = r_aff if r_aff and len(r_aff) > len(aff) else aff

    card = f'''
    <article class="fellow" id="{slug(name)}">
      <div class="fellow-header">
        {'<img src="' + esc(photo) + '" alt="' + esc(name) + '" class="fellow-photo" loading="lazy" />' if photo else '<div class="fellow-photo placeholder"></div>'}
        <div class="fellow-meta">
          <h2><a href="#{slug(name)}">{esc(name)}</a></h2>
          <p class="affiliation">{esc(display_aff)}</p>
          <div class="tags">{' '.join(tags)}</div>
          <div class="links">{links}</div>
        </div>
      </div>
      {'<div class="section"><h3>// what makes them spiky</h3>' + make_list(spiky) + '</div>' if spiky else ''}
      {'<div class="section"><h3>// problems &amp; research</h3>' + make_list(problems) + '</div>' if problems else ''}
      {'<div class="section"><h3>// key work</h3>' + make_list(key_work) + '</div>' if key_work else ''}
      {'<div class="section"><h3>// companies founded</h3>' + make_list(companies_founded) + '</div>' if companies_founded and len(companies_founded) > 0 else ''}
      {'<div class="section"><h3>// current work</h3><p>' + esc(current) + '</p></div>' if current else ''}
      {'<div class="alpha"><h3>// alpha insight</h3><p>' + esc(alpha) + '</p></div>' if alpha else ''}
    </article>'''
    fellow_cards.append(card)

# Build index
index_items = []
for i, base in enumerate(base_data):
    name = base['name']
    aff = base.get('affiliation', '')
    index_items.append(f'<li><a href="#{slug(name)}">{esc(name)}</a> <span class="idx-aff">— {esc(aff)}</span></li>')

# Build company cards
company_cards = []
for c in companies:
    card = f'''
    <article class="company" id="company-{slug(c['name'])}">
      <h2>{esc(c['name'])}</h2>
      <p class="company-meta">{esc(c.get('founders', ''))}</p>
      {'<p><strong>What it does:</strong> ' + esc(c.get('what_it_does', '')) + '</p>' if c.get('what_it_does') else ''}
      {'<p><strong>Problem:</strong> ' + esc(c.get('problem_solved', '')) + '</p>' if c.get('problem_solved') else ''}
      {'<p><strong>Funding:</strong> ' + esc(c.get('funding', '')) + '</p>' if c.get('funding') else ''}
      {'<p><strong>Traction:</strong> ' + esc(c.get('traction', '')) + '</p>' if c.get('traction') else ''}
      {'<p><strong>Differentiator:</strong> ' + esc(c.get('differentiator', '')) + '</p>' if c.get('differentiator') else ''}
      {'<p><strong>Delta connection:</strong> ' + esc(c.get('delta_fellow_connection', '')) + '</p>' if c.get('delta_fellow_connection') else ''}
      {'<p><a href="' + esc(c.get('website_url', '')) + '" target="_blank">' + esc(c.get('website_url', '')) + '</a></p>' if c.get('website_url') and 'Unknown' not in c.get('website_url', '') else ''}
    </article>'''
    company_cards.append(card)

# Stats
num_founders = len(set(founders))
num_frontier = len(set(frontier_lab))
num_phd = len(set(researchers))
num_quant = len(set(quant_finance))

html_page = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Delta Institute Fellows — Cohort 1</title>
<style>
:root {{
  --bg: #fafaf8;
  --fg: #1a1a1a;
  --dim: #666;
  --border: #e0e0dd;
  --accent: #2a5a3a;
  --accent-light: #f0f5f1;
  --founder: #8b5cf6;
  --frontier: #0ea5e9;
  --researcher: #f59e0b;
  --quant: #ef4444;
  --mono: 'Berkeley Mono', 'SF Mono', 'Fira Code', 'JetBrains Mono', Menlo, Consolas, monospace;
  --serif: 'Newsreader', 'Georgia', 'Times New Roman', serif;
  --sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}}

@media (prefers-color-scheme: dark) {{
  :root {{
    --bg: #111110;
    --fg: #e8e8e4;
    --dim: #999;
    --border: #2a2a28;
    --accent: #6dba82;
    --accent-light: #1a2a1e;
  }}
}}

* {{ margin: 0; padding: 0; box-sizing: border-box; }}

body {{
  font-family: var(--sans);
  background: var(--bg);
  color: var(--fg);
  line-height: 1.6;
  max-width: 820px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
  font-size: 15px;
}}

header {{
  margin-bottom: 3rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid var(--border);
}}

header h1 {{
  font-family: var(--serif);
  font-size: 1.8rem;
  font-weight: 400;
  margin-bottom: 0.5rem;
  letter-spacing: -0.02em;
}}

header p {{
  color: var(--dim);
  font-size: 0.9rem;
}}

nav {{
  margin-bottom: 3rem;
}}

nav h2 {{
  font-family: var(--mono);
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--dim);
  margin-bottom: 0.75rem;
}}

.nav-links {{
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
  margin-bottom: 1.5rem;
  font-family: var(--mono);
  font-size: 0.85rem;
}}

.nav-links a {{
  color: var(--accent);
  text-decoration: none;
}}

.nav-links a:hover {{
  text-decoration: underline;
}}

.stats {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
  padding: 1rem 0;
}}

.stat {{
  text-align: center;
  padding: 0.75rem;
  border: 1px solid var(--border);
}}

.stat-num {{
  font-family: var(--mono);
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--accent);
}}

.stat-label {{
  font-size: 0.75rem;
  color: var(--dim);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}}

/* Search & Filter */
.controls {{
  margin-bottom: 2rem;
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  align-items: center;
}}

#search {{
  flex: 1;
  min-width: 200px;
  padding: 0.5rem 0.75rem;
  border: 1px solid var(--border);
  background: var(--bg);
  color: var(--fg);
  font-family: var(--mono);
  font-size: 0.85rem;
  outline: none;
}}

#search:focus {{
  border-color: var(--accent);
}}

.filter-btn {{
  padding: 0.35rem 0.75rem;
  border: 1px solid var(--border);
  background: var(--bg);
  color: var(--dim);
  font-family: var(--mono);
  font-size: 0.75rem;
  cursor: pointer;
  transition: all 0.15s;
}}

.filter-btn:hover, .filter-btn.active {{
  background: var(--accent-light);
  color: var(--accent);
  border-color: var(--accent);
}}

/* Index */
.index {{
  margin-bottom: 3rem;
  border: 1px solid var(--border);
  padding: 1.5rem;
}}

.index h2 {{
  font-family: var(--mono);
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--dim);
  margin-bottom: 1rem;
}}

.index ol {{
  list-style: none;
  counter-reset: fellow;
  columns: 2;
  column-gap: 2rem;
  font-size: 0.85rem;
}}

@media (max-width: 600px) {{
  .index ol {{ columns: 1; }}
}}

.index li {{
  counter-increment: fellow;
  padding: 0.15rem 0;
  break-inside: avoid;
}}

.index li::before {{
  content: counter(fellow, decimal-leading-zero) ". ";
  font-family: var(--mono);
  color: var(--dim);
  font-size: 0.75rem;
}}

.index li a {{
  color: var(--fg);
  text-decoration: none;
}}

.index li a:hover {{
  color: var(--accent);
  text-decoration: underline;
}}

.idx-aff {{
  color: var(--dim);
  font-size: 0.8rem;
}}

/* Fellow Cards */
.fellow {{
  margin-bottom: 2.5rem;
  padding-bottom: 2.5rem;
  border-bottom: 1px solid var(--border);
}}

.fellow-header {{
  display: flex;
  gap: 1rem;
  align-items: flex-start;
  margin-bottom: 1rem;
}}

.fellow-photo {{
  width: 64px;
  height: 64px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
  background: var(--border);
}}

.fellow-photo.placeholder {{
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: var(--border);
}}

.fellow-meta h2 {{
  font-family: var(--serif);
  font-size: 1.2rem;
  font-weight: 500;
  margin-bottom: 0.1rem;
}}

.fellow-meta h2 a {{
  color: var(--fg);
  text-decoration: none;
}}

.fellow-meta h2 a:hover {{
  color: var(--accent);
}}

.affiliation {{
  color: var(--dim);
  font-size: 0.85rem;
  margin-bottom: 0.3rem;
}}

.tags {{
  display: flex;
  gap: 0.4rem;
  flex-wrap: wrap;
  margin-bottom: 0.3rem;
}}

.tag {{
  font-family: var(--mono);
  font-size: 0.65rem;
  padding: 0.15rem 0.45rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}}

.tag.founder {{ background: #f3f0ff; color: var(--founder); border: 1px solid #e0d8ff; }}
.tag.frontier {{ background: #f0f9ff; color: var(--frontier); border: 1px solid #bae6fd; }}
.tag.researcher {{ background: #fffbeb; color: #b45309; border: 1px solid #fde68a; }}
.tag.quant {{ background: #fef2f2; color: var(--quant); border: 1px solid #fecaca; }}

@media (prefers-color-scheme: dark) {{
  .tag.founder {{ background: #1e1536; border-color: #3b2970; }}
  .tag.frontier {{ background: #0c1929; border-color: #1e3a5f; }}
  .tag.researcher {{ background: #1f1a0e; border-color: #4a3510; }}
  .tag.quant {{ background: #1f0e0e; border-color: #4a1010; }}
}}

.links {{
  font-family: var(--mono);
  font-size: 0.75rem;
}}

.links a {{
  color: var(--accent);
  text-decoration: none;
  margin-right: 0.5rem;
}}

.links a:hover {{
  text-decoration: underline;
}}

.section {{
  margin-bottom: 0.75rem;
}}

.section h3 {{
  font-family: var(--mono);
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--dim);
  margin-bottom: 0.3rem;
}}

.section ul {{
  list-style: none;
  padding-left: 0;
}}

.section li {{
  padding: 0.1rem 0;
  font-size: 0.88rem;
  padding-left: 1em;
  text-indent: -1em;
}}

.section li::before {{
  content: "— ";
  color: var(--dim);
}}

.section p {{
  font-size: 0.88rem;
}}

.alpha {{
  background: var(--accent-light);
  padding: 0.75rem 1rem;
  border-left: 3px solid var(--accent);
  margin-top: 0.75rem;
}}

.alpha h3 {{
  font-family: var(--mono);
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--accent);
  margin-bottom: 0.3rem;
}}

.alpha p {{
  font-size: 0.88rem;
  color: var(--fg);
}}

/* Companies Section */
.companies-section {{
  margin-top: 4rem;
  padding-top: 3rem;
  border-top: 2px solid var(--border);
}}

.companies-section > h2 {{
  font-family: var(--serif);
  font-size: 1.5rem;
  font-weight: 400;
  margin-bottom: 2rem;
}}

.company {{
  margin-bottom: 2rem;
  padding: 1.25rem;
  border: 1px solid var(--border);
}}

.company h2 {{
  font-family: var(--serif);
  font-size: 1.1rem;
  font-weight: 500;
  margin-bottom: 0.25rem;
}}

.company-meta {{
  color: var(--dim);
  font-size: 0.82rem;
  margin-bottom: 0.75rem;
}}

.company p {{
  font-size: 0.85rem;
  margin-bottom: 0.4rem;
}}

.company a {{
  color: var(--accent);
  font-family: var(--mono);
  font-size: 0.8rem;
}}

/* Footer */
footer {{
  margin-top: 4rem;
  padding-top: 2rem;
  border-top: 1px solid var(--border);
  color: var(--dim);
  font-size: 0.8rem;
  font-family: var(--mono);
}}

/* Responsive */
@media (max-width: 600px) {{
  body {{ padding: 1rem; font-size: 14px; }}
  .fellow-photo {{ width: 48px; height: 48px; }}
  .stats {{ grid-template-columns: repeat(2, 1fr); }}
}}
</style>
</head>
<body>

<header>
  <h1>Delta Institute Fellows — Cohort 1</h1>
  <p>144 researchers and builders. Mapped, profiled, and annotated.</p>
  <p style="margin-top:0.5rem; font-family: var(--mono); font-size: 0.75rem;">
    last updated: march 2026 &middot; <a href="https://deltainstitutes.org/cohort1" target="_blank" style="color:var(--accent)">source</a>
  </p>
</header>

<nav>
  <h2>navigate</h2>
  <div class="nav-links">
    <a href="#index">index</a>
    <a href="#fellows-section">fellows</a>
    <a href="#companies-section">companies</a>
  </div>
</nav>

<div class="stats">
  <div class="stat"><div class="stat-num">144</div><div class="stat-label">fellows</div></div>
  <div class="stat"><div class="stat-num">{num_founders}</div><div class="stat-label">founders</div></div>
  <div class="stat"><div class="stat-num">{num_frontier}</div><div class="stat-label">frontier lab</div></div>
  <div class="stat"><div class="stat-num">{num_phd}</div><div class="stat-label">PhD / postdoc</div></div>
  <div class="stat"><div class="stat-num">{num_quant}</div><div class="stat-label">quant finance</div></div>
</div>

<div class="controls">
  <input type="text" id="search" placeholder="search fellows..." onkeyup="filterFellows()" />
  <button class="filter-btn" onclick="toggleFilter('all')">all</button>
  <button class="filter-btn" onclick="toggleFilter('founder')">founders</button>
  <button class="filter-btn" onclick="toggleFilter('frontier')">frontier labs</button>
  <button class="filter-btn" onclick="toggleFilter('researcher')">researchers</button>
  <button class="filter-btn" onclick="toggleFilter('quant')">quant</button>
</div>

<div class="index" id="index">
  <h2>index — 144 fellows</h2>
  <ol>
    {''.join(index_items)}
  </ol>
</div>

<section id="fellows-section">
  {''.join(fellow_cards)}
</section>

<section class="companies-section" id="companies-section">
  <h2>Companies & Startups</h2>
  {''.join(company_cards)}
</section>

<footer>
  <p>assembled by vansh &middot; research powered by claude &middot; delta institute cohort 1</p>
  <p>this is a research document, not affiliated with delta institute</p>
</footer>

<script>
let currentFilter = 'all';

function filterFellows() {{
  const query = document.getElementById('search').value.toLowerCase();
  document.querySelectorAll('.fellow').forEach(el => {{
    const text = el.textContent.toLowerCase();
    const matchesSearch = !query || text.includes(query);
    const matchesFilter = currentFilter === 'all' || el.querySelector('.tag.' + currentFilter);
    el.style.display = (matchesSearch && matchesFilter) ? '' : 'none';
  }});
}}

function toggleFilter(filter) {{
  currentFilter = filter;
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  event.target.classList.add('active');
  filterFellows();
}}
</script>

</body>
</html>'''

with open('/Users/vansh/Brainstorming/delta_fellows.html', 'w') as f:
    f.write(html_page)

print(f"Generated HTML: {len(html_page)} bytes")
print(f"Fellows: {len(fellow_cards)}")
print(f"Companies: {len(company_cards)}")
print(f"Stats: {num_founders} founders, {num_frontier} frontier lab, {num_phd} researchers, {num_quant} quant")
