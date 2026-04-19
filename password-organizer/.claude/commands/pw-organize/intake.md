---
description: Conversational interview to understand the user's identity, accounts, and desired vault categories
argument-hint: [session-name]
allowed-tools: Read, Write, Edit, Glob, Bash, AskUserQuestion
---

# Password Organizer Intake

Conversational interview to understand who the user is, what emails they use, what their business is, and how they want their vaults organized. Pre-reads the CSV export to lead with findings so the user confirms rather than recites from scratch.

## Skill Reference

- Skill: `.claude/skills/pw-organize/SKILL.md`
- CSV schema: `.claude/skills/pw-organize/references/onepassword-csv-schema.md`
- Service knowledge: `.claude/skills/pw-organize/references/service-knowledge.md`

## Variables

```
$1 = session name. If empty, detect from existing session folders.
SESSION_DIR = {$1}
WORKING_DIR = {SESSION_DIR}/working
SOURCE_DIR = {SESSION_DIR}/source-files
INTAKE = {WORKING_DIR}/intake.md
```

## Prerequisites

- Session must be initialized: `{WORKING_DIR}/intake.md` must exist
- At least one CSV file should be in `{SOURCE_DIR}/`

## Instructions

### Step 1: Initialize

1. If `$1` is empty, look for existing session folders and ask the user which one
2. Verify `{SOURCE_DIR}/` has at least one CSV file. If not, tell the user to export and drop their CSV first.

### Step 2: Discovery Scan

Before asking any questions, parse the CSV(s) to pre-populate answers.

```bash
python3 .claude/skills/pw-organize/scripts/parse_csv.py \
  --source-dir "{SOURCE_DIR}" \
  --output "{WORKING_DIR}/parsed_entries.json"
```

Read the output JSON and note:
- Total entry count
- Unique email addresses found (these will drive the identity questions)
- Unique domains (top services)
- Entry type breakdown

**Hold all findings in context** — Use findings to drive the interview in Step 4.

### Step 3: Resume Check

Read the existing `{INTAKE}` and check `<!-- STATUS: -->` markers:

- **All `complete`** → Intake is done. Tell the user what's captured and suggest running `/pw-organize:categorize {session}`. Stop here.
- **Mix of `complete` and `pending`** → Resuming a broken session. Summarize what's already captured, then continue from the first `pending` section in Step 4.
- **All `pending`** → Fresh start. Proceed to Step 4 from the beginning.

### Step 4: Interview

6 sections, each following this pattern:
1. **Lead with findings** — Present what you discovered from the CSV ("I found these emails...")
2. **Confirm or correct** — Let the user confirm, adjust, or add details
3. **Fall back to questions** — Only ask from scratch when no data was found
4. **Save immediately** — After the user confirms, `Edit` that section in `{INTAKE}`:
   - Replace the section content with confirmed data
   - Flip `<!-- STATUS: pending -->` to `<!-- STATUS: complete -->`
   - Update the header's `Sections Completed` count
   - Update the `Last Updated` date

Ask one section at a time. Wait for the user's response before moving to the next.

#### Section 1: Identity

Lead with the unique emails found in the CSV:
- "I found {N} unique email addresses in your passwords: {list}. Which are personal and which are business?"
- Full name
- Personal email(s)
- Business email(s)
- Business name(s)
- Business domain(s) (e.g., yourbusiness.com)

Save in this format:
```markdown
- **Name**: {name}
- **Personal Emails**: {email1}, {email2}
- **Business Emails**: {email1}
- **Business Name**: {name}
- **Business Domains**: {domain1}, {domain2}
```

#### Section 2: Past Clients

- "Do you have passwords from past client work?"
- Client names
- Client domains (e.g., clientname.com)
- Client-specific email addresses you used
- If none: note "No past client accounts" and move on

Save in this format:
```markdown
- **Has Client Accounts**: Yes/No
- **Client Names**: {name1}, {name2}
- **Client Domains**: {domain1}, {domain2}
- **Client Emails**: {email1}
```

#### Section 3: Vault Categories

This is the critical section. Lead with a suggestion based on what was learned:
- "Based on your info, I'd suggest these vaults: Personal, Business, Clients, Unknown — would you like to adjust?"
- Let the user define/rename/add/remove categories freely
- Each vault category gets a name (user-facing) and a key (kebab-case)

Save as a table:
```markdown
| Key | Display Name | Description |
|-----|-------------|-------------|
| personal | Personal | Personal accounts, entertainment, social media |
| business | Business | SaaS tools, dev tools, business finance |
| clients | Clients | Past client accounts to archive |
| unknown | Unknown | Items needing manual sorting |
```

#### Section 4: Categorization Rules

- "Are there any rules you already know?"
- Examples: "Anything with @gmail.com is personal", "Anything on clientdomain.com is a client password"
- "Should streaming services (Netflix, Spotify) always be personal?"
- "Should dev tools (GitHub, AWS) always be business?"

Save as a list of rules:
```markdown
- {pattern} → {vault-key}
```

If no explicit rules: note "No additional rules — rely on email/domain matching and AI classification"

#### Section 5: Handling Preferences

- What to do with truly ambiguous items? (Flag for review — this is always the default)
- Should shared services (e.g., Amazon used for both) be duplicated or assigned to one vault?
- Any passwords to exclude entirely? (e.g., test accounts, throwaway accounts)
- What about entries with no URL and no username — just a title?

Save preferences as bullet points.

#### Section 6: Confirmation

Summarize everything back to the user:
- Identity (emails, business)
- Vault categories defined
- Rules in place
- CSV stats (total entries, emails found)
- Ask: "Does this all look right?"

After confirmation, also update the Statistics section in intake.md with the CSV stats from the discovery scan.

### Step 5: Wrap Up

1. Set the header `Status` to `Complete`
2. Set `Sections Completed` to `6/6`
3. Update `Last Updated` date
4. Tell the user:
   - What's captured in intake.md
   - Next step: run `/pw-organize:categorize {session}` to classify the passwords

## Behavior

- **Lead with findings** — Always present what you discovered from the CSV before asking. Confirm rather than interrogate.
- **Save incrementally** — Write to intake.md after EACH section. Do not batch saves to the end.
- **Update STATUS markers** — Flip `<!-- STATUS: pending -->` to `<!-- STATUS: complete -->` per section for resume support.
- **Keep it conversational** — This should feel like talking to a helpful organizer, not filling out a form.
- **No passwords in output** — Never display or log actual password values. Title, URL, and username are fine.
- **If a section is skipped** — Write "Skipped — will revisit" and mark as `complete` so the interview can move forward.
- **On resume** — Summarize what's already captured before continuing with pending sections.
