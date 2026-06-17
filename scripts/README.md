# Daily Outreach Scripts

ADHD-friendly daily ritual for converting the dossier repo into actual outreach.
All scripts read/write `data/outreach_state.json`. UI re-renders into the index
outreach panel after every status change.

---

## Morning ritual (5 min)

```bash
# 1. See today's 5 prioritized names
python3 scripts/today.py

# 2. Click the channel-appropriate compose link inline (Gmail, Twitter DM, LinkedIn)

# 3. After each message sent, mark it
python3 scripts/mark.py alex-shan sent

# 4. Once a week (or when queue feels thin): triage new entries
python3 scripts/suggest_urgency.py

# 5. Check cluster activity (or set as cron — see below)
python3 scripts/cluster_check.py
```

---

## Scripts

### `today.py` — Daily queue
Shows 5 entries max, ranked by `tier × 100 + urgency_decay_proximity`.
- `python3 scripts/today.py` → today's 5
- `python3 scripts/today.py --all` → full ranked debug list
- `python3 scripts/today.py --triage` → tiered entries missing urgency

Each row shows: tier badge · name · cluster · WHY-NOW · ACTION · identifiers
(email/twitter/linkedin) · channel-aware compose link.

### `mark.py` — Status updates
```
python3 scripts/mark.py SLUG sent          # marked contacted, +14d follow-up
python3 scripts/mark.py SLUG replied "note" # marked replied with note
python3 scripts/mark.py SLUG meeting "Tue 3pm" # meeting booked
python3 scripts/mark.py SLUG passed "reason" # drops out forever
python3 scripts/mark.py SLUG snooze 30     # next_action_date = today + 30d
python3 scripts/mark.py SLUG unsnooze      # clear snooze
python3 scripts/mark.py SLUG reset         # back to not-contacted
python3 scripts/mark.py SLUG email ADDR    # override extracted email
python3 scripts/mark.py SLUG subject "..." # override extracted subject
```

After any change, the index outreach panel auto-rebuilds.
Skip with `MARK_NO_RENDER=1 python3 scripts/mark.py ...` in batch mode.

### `suggest_urgency.py` — Triage queue
Surfaces untriaged entries with the strongest signals. Score = tier weight + 
recent-touch + signals (stealth/departed/raising/founded) + Indian flag.

```
python3 scripts/suggest_urgency.py       # top 15
python3 scripts/suggest_urgency.py --top 30
python3 scripts/suggest_urgency.py --json # machine-readable
```

Output gives you slug + suggested urgency_reason + suggested channel —
copy into `scripts/seed_priorities.py`, re-run `seed_priorities.py`.

### `cluster_check.py` — Cluster activity alerts
Detects clusters with recent dossier updates or status changes. Surfaces
under-engaged members of active clusters so you outreach the whole cohort
in the same window.

```
python3 scripts/cluster_check.py
```

Run as cron daily — see below.

### `seed_priorities.py` — Edit + re-run to seed urgency
Hand-curated priority list. Edit the `SEED` dict to add/modify entries, then:
```
python3 scripts/seed_priorities.py
```

User-owned fields (urgency_reason, channel, next_action, urgency_decay_date,
cluster, email_override, subject_override) are preserved across rebuilds of
`build_outreach_state.py`.

---

## Cron setup (recommended)

Add to your crontab (`crontab -e`):

```cron
# 7am daily: refresh state + render directory table + The Desk
0 7 * * * cd "/Users/vansh/out of distribution people repo" && python3 data/build_outreach_state.py > /dev/null && python3 data/build_directory.py > /dev/null && python3 data/build_today.py > /dev/null

# 7:05am daily: cluster activity check (output goes to file you can grep)
5 7 * * * cd "/Users/vansh/out of distribution people repo" && python3 scripts/cluster_check.py > /tmp/cluster_check.log 2>&1

# 7:10am daily: suggest urgency (output goes to file)
10 7 * * * cd "/Users/vansh/out of distribution people repo" && python3 scripts/suggest_urgency.py > /tmp/triage.log 2>&1
```

Then check the log files in the morning:
```bash
cat /tmp/cluster_check.log
cat /tmp/triage.log
```

---

## Gmail draft creation

Two ways to push drafts:

**A. From this terminal (mailto fallback):** Click the 📧 link in `today.py` 
output. Opens Gmail compose in browser with `to` + `subject` prefilled. No 
draft saved; you send directly or close.

**B. From a Claude Code session (real Gmail draft):** Ask Claude "draft emails 
for today's queue" — Claude uses Gmail MCP to push real drafts into your 
Drafts folder with `to` + `subject`. You then open Gmail, customize body, 
hit send.

The MCP path is preferred when you want drafts to persist and accumulate 
across sessions.

---

## Reply detection (workflow)

Gmail MCP only runs inside a Claude Code session. Daily routine:

1. Morning: run `python3 scripts/today.py` to see queue
2. Open Claude Code session in this repo
3. Ask: "check for new replies from anyone in state and update"
4. Claude searches Gmail for any thread with `email_primary` addresses, 
   auto-marks `replied`, re-renders index panel
5. Then run `python3 scripts/today.py` again — replied entries are surfaced 
   at top

For full automation, you'd need a standalone Python script using Google's 
Gmail API directly (OAuth setup required) — not built yet.

---

## Twitter

No Twitter API needed for outreach. The `twitter` channel renders DM 
compose intent URLs (`twitter.com/messages/compose?recipient_screen_name=X`) 
which open the DM box in browser if your account has DM access to the 
recipient.

Twitter API would be needed for **monitoring** (bio changes, recent tweets, 
follower spikes) — that's Phase 2 signal detection, not outreach.
