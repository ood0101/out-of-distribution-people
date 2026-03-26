#!/usr/bin/env python3
"""Enrich the main index.html Delta fellows cards with research data and photos."""
import json
import re
import html as html_mod

# Load all research data
with open('/Users/vansh/out of distribution people repo/data/delta_fellows.json') as f:
    base_data = json.load(f)

batches = []
for fname in [
    'delta_fellows_profiles.json',
    'delta_fellows_26_50.json',
    'delta_fellows_51_75.json',
    'delta_fellows_76_100.json',
    'delta_fellows_101_144.json',
]:
    with open(f'/Users/vansh/out of distribution people repo/data/{fname}') as f:
        batches.extend(json.load(f))

# Build name -> research mapping
research = {}
for person in batches:
    name = person.get('name', '').strip()
    if '(' in name:
        name = name.split('(')[0].strip()
    research[name] = person

# Build name -> base data mapping (photos)
photos = {}
for b in base_data:
    photos[b['name']] = b.get('photo', '')

# Read current index.html
with open('/Users/vansh/out of distribution people repo/index.html') as f:
    html = f.read()

# For each Delta fellow card, add photo URL and enriched spike text
updated = 0
for name, r in research.items():
    photo = photos.get(name, '')
    spiky = r.get('what_makes_them_spiky', [])
    alpha = r.get('alpha_insight', '')
    twitter = r.get('twitter_url', '')
    linkedin = r.get('linkedin_url', '')
    website = r.get('website_url', '')
    scholar = r.get('scholar_url', '')

    # Build spike text from first spiky item
    spike_text = ''
    if spiky and isinstance(spiky, list) and len(spiky) > 0:
        spike_text = spiky[0]

    # Find the card for this person in the HTML
    # Match pattern: data-name="name_lower"
    name_lower = name.lower()

    # Try to find and update the card
    # Pattern: person-card with this name, find the card-spike div
    pattern = rf'(data-name="{re.escape(name_lower)}"[^>]*>)'
    match = re.search(pattern, html)
    if not match:
        # Try partial match
        name_parts = name_lower.split()
        if len(name_parts) >= 2:
            pattern2 = rf'(data-name="[^"]*{re.escape(name_parts[0])}[^"]*{re.escape(name_parts[-1])}[^"]*"[^>]*>)'
            match = re.search(pattern2, html)

    if match:
        # Add photo to the avatar div if we have one
        if photo:
            # Find the avatar div after this card opening
            card_start = match.start()
            avatar_pattern = r'(<div class="avatar" data-initials="[A-Z]{2}"></div>)'
            avatar_match = re.search(avatar_pattern, html[card_start:card_start+500])
            if avatar_match:
                old_avatar = avatar_match.group(1)
                initials = re.search(r'data-initials="([A-Z]{2})"', old_avatar).group(1)
                new_avatar = f'<img src="{html_mod.escape(photo)}" alt="{html_mod.escape(name)}" class="avatar" loading="lazy" onerror="this.outerHTML=\'<div class=&quot;avatar&quot; data-initials=&quot;{initials}&quot;></div>\'" />'
                html = html[:card_start] + html[card_start:].replace(old_avatar, new_avatar, 1)
                updated += 1

        # Update spike text if we have better data
        if spike_text:
            card_start = match.start()
            spike_pattern = r'(<div class="card-spike">)(.*?)(</div>)'
            spike_match = re.search(spike_pattern, html[card_start:card_start+1000])
            if spike_match:
                old_spike = spike_match.group(0)
                # Only replace if our new text is longer/better
                if len(spike_text) > len(spike_match.group(2)):
                    new_spike = f'<div class="card-spike">{html_mod.escape(spike_text)}</div>'
                    html = html[:card_start] + html[card_start:].replace(old_spike, new_spike, 1)

# Write updated HTML
with open('/Users/vansh/out of distribution people repo/index.html', 'w') as f:
    f.write(html)

print(f"Updated {updated} Delta fellow cards with photos")
print(f"Total research profiles available: {len(research)}")
print(f"Total photos available: {len([p for p in photos.values() if p])}")
