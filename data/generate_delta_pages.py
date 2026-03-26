#!/usr/bin/env python3
"""Generate individual dossier HTML pages for all 144 Delta fellows
using the pre-researched JSON data, in the same template format as
the main repo's hand-curated dossier pages."""
import json
import html as h
import re
import os

REPO = '/Users/vansh/out of distribution people repo'
DATA = f'{REPO}/data'
PEOPLE = f'{REPO}/people'

# Load all data
with open(f'{DATA}/delta_fellows.json') as f:
    base_data = json.load(f)

batches = []
for fname in [
    'delta_fellows_profiles.json',
    'delta_fellows_26_50.json',
    'delta_fellows_51_75.json',
    'delta_fellows_76_100.json',
    'delta_fellows_101_144.json',
]:
    with open(f'{DATA}/{fname}') as f:
        batches.extend(json.load(f))

with open(f'{DATA}/delta_fellows_companies_research.json') as f:
    companies = json.load(f)

# Build lookups
research = {}
for person in batches:
    name = person.get('name', '').strip()
    if '(' in name:
        name = name.split('(')[0].strip()
    research[name] = person

photos = {}
for b in base_data:
    photos[b['name']] = b.get('photo', '')

company_map = {}
for c in companies:
    company_map[c['name'].lower()] = c

def slug(name):
    return re.sub(r'[^a-z0-9-]', '', name.lower().replace(' ', '-').replace('(', '').replace(')', ''))

def esc(s):
    if not s:
        return ''
    return h.escape(str(s))

def make_list_html(items, max_items=8):
    if not items:
        return ''
    if isinstance(items, str):
        return f'<p>{esc(items)}</p>'
    out = '<ul>'
    for item in items[:max_items]:
        out += f'<li>{esc(item)}</li>'
    out += '</ul>'
    return out

def make_links_html(person):
    links = []
    for key, label in [('linkedin_url', 'linkedin'), ('twitter_url', 'twitter/x'),
                        ('website_url', 'website'), ('scholar_url', 'scholar')]:
        url = person.get(key)
        if url and url != 'null' and url != 'None' and str(url).startswith('http'):
            links.append(f'<a href="{esc(url)}">{label}</a>')
    return '\n      '.join(links)

def detect_tags(name, aff, r):
    tags = ['delta']
    companies_founded = r.get('companies_founded', [])
    if isinstance(companies_founded, list) and len(companies_founded) > 0:
        tags.append('founders')
    for lab in ['OpenAI', 'Anthropic', 'DeepMind', 'Meta AI', 'Meta Superintelligence',
                'Physical Intelligence', 'Skild AI', 'NVIDIA', 'Tesla']:
        if lab.lower() in aff.lower():
            tags.append('frontier-labs')
            break
    if 'PhD' in aff or 'Postdoc' in aff:
        tags.append('researchers')
    for firm in ['Jane Street', 'HRT', 'DRW', 'Jump Trading', 'Citadel']:
        if firm.lower() in aff.lower():
            tags.append('quant')
            break
    # Indian detection
    indian_indicators = ['IIT', 'India', 'IISC', 'Chennai', 'Mumbai', 'Delhi', 'Bombay', 'Bangalore']
    for ind in indian_indicators:
        if ind.lower() in aff.lower():
            tags.append('indian')
            break
    return tags

def generate_page(name, base_aff, photo, r):
    s = slug(name)
    aff = r.get('affiliation', base_aff) or base_aff
    problems = r.get('problems_worked_on', [])
    spiky = r.get('what_makes_them_spiky', [])
    key_work = r.get('key_work', [])
    companies_founded = r.get('companies_founded', [])
    current = r.get('current_work', '')
    alpha = r.get('alpha_insight', '')
    links = make_links_html(r)
    tags = detect_tags(name, aff, r)

    # Build spike box content
    spike_content = ''
    if spiky:
        spike_items = '\n'.join(f'      <li>{esc(item)}</li>' for item in spiky)
        spike_content = f'''
    <ul>
{spike_items}
    </ul>'''

    # Build research section
    research_section = ''
    if problems or key_work:
        research_section = '\n  <h2>Research &amp; Key Work</h2>'
        if problems:
            research_section += f'\n  <h3>Problems &amp; Research Areas</h3>\n  {make_list_html(problems)}'
        if key_work:
            research_section += f'\n  <h3>Key Work</h3>\n  {make_list_html(key_work)}'

    # Build companies section
    companies_section = ''
    if companies_founded and isinstance(companies_founded, list) and len(companies_founded) > 0:
        companies_section = '\n  <h2>Companies Founded</h2>\n  ' + make_list_html(companies_founded)

    # Build current work section
    current_section = ''
    if current:
        current_section = f'\n  <h2>Current Work</h2>\n  <p>{esc(current)}</p>'

    # Build alpha insight
    alpha_section = ''
    if alpha:
        alpha_section = f'''
  <div class="spike-box" style="margin-top: 1.5rem;">
    <div class="label">&#9670; Alpha Insight</div>
    <p>{esc(alpha)}</p>
  </div>'''

    # Build tag spans
    tag_spans = '\n      '.join(
        f'<span class="tag{" spike" if t in ["founders"] else ""}">{t}</span>'
        for t in tags
    )

    # Photo HTML
    photo_html = ''
    if photo:
        initials = ''.join(w[0].upper() for w in name.split()[:2])
        photo_html = f'<img src="{esc(photo)}" alt="{esc(name)}" style="width:80px;height:80px;border-radius:50%;object-fit:cover;float:right;margin:0 0 1rem 1rem;" loading="lazy" onerror="this.style.display=\'none\'" />'

    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(name)} &mdash; Out of Distribution People</title>
  <link rel="stylesheet" href="../style.css">
</head>
<body>

  <nav>
    <div class="site-title">Out of Distribution People</div>
    <div class="breadcrumb"><a href="../index.html">/ index</a> / {s}</div>
  </nav>

  <div class="profile-header">
    <h1>{esc(name)}</h1>
    {photo_html}
    <p class="one-liner">{esc(aff)}</p>
    <div class="tags">
      {tag_spans}
    </div>
    <div class="links">
      {links}
    </div>
  </div>

  <!-- THE SPIKE -->
  <div class="spike-box">
    <div class="label">&#9670; What Makes Them Spiky</div>{spike_content}
  </div>
{research_section}
{companies_section}
{current_section}
{alpha_section}

  <footer>
    researched: 2026-03 &middot; delta institute cohort 1 &middot; <a href="../index.html">back to index</a>
  </footer>

</body>
</html>'''
    return page

# Generate all pages
generated = 0
skipped = 0
for base in base_data:
    name = base['name']
    s = slug(name)
    filepath = f'{PEOPLE}/{s}.html'

    # Skip if page already exists (hand-curated pages take precedence)
    if os.path.exists(filepath):
        skipped += 1
        continue

    r = research.get(name, {})
    if not r:
        # Still generate a minimal page
        r = {'affiliation': base.get('affiliation', '')}

    photo = photos.get(name, '')
    page_html = generate_page(name, base.get('affiliation', ''), photo, r)

    with open(filepath, 'w') as f:
        f.write(page_html)
    generated += 1

print(f"Generated {generated} new Delta fellow pages")
print(f"Skipped {skipped} (already existed)")

# Now update index.html to link Delta cards to their pages
index_path = f'{REPO}/index.html'
with open(index_path) as f:
    index_html = f.read()

# Convert no-link divs to linked <a> tags for Delta fellows
linked = 0
for base in base_data:
    name = base['name']
    s = slug(name)
    name_lower = name.lower()

    # Find: <div class="person-card no-link" data-name="name_lower"
    pattern = rf'<div class="person-card no-link" data-name="{re.escape(name_lower)}"'
    if pattern in index_html:
        replacement = f'<a href="people/{s}.html" class="person-card" data-name="{name_lower}"'
        index_html = index_html.replace(pattern, replacement, 1)

        # Also need to close the div -> close the a
        # Find the closing </div> for this card (the outermost one)
        # This is tricky - let's find the card and replace closing tag
        linked += 1

# Also fix closing tags: find </div>\n  </div> patterns that should be </div>\n  </a>
# for the cards we just converted
# Actually, the card structure is:
#   <div class="person-card no-link" ...>
#     <img .../>
#     <div class="card-body">...</div>
#   </div>
# We changed the opening <div to <a, so we need to change the matching </div> to </a>
# Let's do a more targeted replacement

# Re-read and fix closing tags
lines = index_html.split('\n')
new_lines = []
in_linked_card = False
depth = 0

for i, line in enumerate(lines):
    if '<a href="people/' in line and 'class="person-card"' in line and 'data-tags="delta' in line:
        in_linked_card = True
        depth = 0
        new_lines.append(line)
        continue

    if in_linked_card:
        # Count opening/closing divs
        opens = line.count('<div')
        closes = line.count('</div>')
        depth += opens - closes

        if depth < 0:
            # This </div> is the closing of our <a> tag
            line = line.replace('</div>', '</a>', 1)
            in_linked_card = False
            depth = 0

    new_lines.append(line)

index_html = '\n'.join(new_lines)

with open(index_path, 'w') as f:
    f.write(index_html)

print(f"Linked {linked} Delta cards to their pages in index.html")
