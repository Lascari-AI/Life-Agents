---
description: Review auto-categorization results and resolve flagged items
argument-hint: [session-name]
allowed-tools: Read, Write, Edit, Glob, AskUserQuestion
---

# Password Organizer Review

Walk through the categorized entries with the user, confirm vault assignments look right, and resolve all flagged items.

## Variables

```
$1 = session name. If empty, detect from existing session folders.
SESSION_DIR = {$1}
WORKING_DIR = {SESSION_DIR}/working
CATEGORIZED = {WORKING_DIR}/categorized.json
REVIEWED = {WORKING_DIR}/reviewed.json
```

## Prerequisites

- Categorization must be complete: `{CATEGORIZED}` must exist with all entries having a vault assigned
- If `{CATEGORIZED}` doesn't exist, tell the user to run `/pw-organize:categorize` first

## Instructions

### Step 1: Load and Resume Check

1. If `{REVIEWED}` already exists, show summary and ask: "Review is already done. Re-review or proceed to export?"
2. Read `{CATEGORIZED}`
3. Separate entries into:
   - **Confident entries** — no flag, high confidence
   - **Flagged entries** — grouped by flag type

### Step 2: Per-Vault Summary

For each vault category, show a brief summary:

```markdown
## {Vault Display Name} — {count} entries

### Sample entries:
| Title | URL | Username | Method |
|-------|-----|----------|--------|
| {first 10 entries} | ... | ... | ... |

{If more than 10: "+ {N} more entries"}
```

After showing each vault, ask: "Does this vault look right? Any entries that shouldn't be here?"

If the user identifies a misplaced entry:
- Update its vault assignment in the working data
- Note the change

Go vault by vault. Wait for confirmation before moving to the next.

**Important**: Never show password values in any table or display.

### Step 3: Flagged Items — Shared Services

If there are `shared-service` flagged items, present them in a batch:

```markdown
## Shared Services — {count} entries

These services are often used for both personal and business:

1. **{Title}** — {domain}, {username}
   Suggested: {vault}
   
2. ...
```

Ask: "For each of these, which vault should they go in? Or should any be duplicated into multiple vaults?"

Process the user's decisions and update vault assignments.

### Step 4: Flagged Items — Ambiguous

Present ambiguous items individually or in smart groups:

```markdown
## Ambiguous Items — {count} entries

1. **{Title}** — {domain}, {username}
   Suggested: {vault} (medium confidence)
   Reason: {notes}
   → Which vault?
```

For similar items (e.g., multiple cloud storage services), group them:
"I flagged 4 cloud storage services — Dropbox, Box, Google Drive, iCloud. Should all go to the same vault?"

### Step 5: Flagged Items — Unknown & No-Data

Present items with minimal information:

```markdown
## Unknown / Minimal Data — {count} entries

1. **{Title}** — no URL, no username
   Currently in: {vault}
   → Keep in {vault}, move elsewhere, or exclude?
```

Options for each:
- Assign to a specific vault
- Keep in Unknown
- Exclude entirely (set vault to `_excluded`)

### Step 6: Cross-Check

Ask the user:
- "Any entries you expected to see but didn't?"
- "Any vault that looks too big or too small?"
- "Anything else to adjust?"

### Step 7: Finalize

After all decisions are made:

1. Write `{REVIEWED}` — same structure as categorized.json but with all flags resolved and vault assignments finalized
2. Present final counts:

```markdown
## Review Complete

| Vault | Entries |
|-------|---------|
| {vault} | {count} |
| ... | ... |
| **Total** | **{total}** |
| Excluded | {count} |

### Next Step
Run `/pw-organize:export {session}` to generate the per-vault CSV files.
```

## Behavior

- **Go vault by vault** — Don't dump everything at once
- **After each section, wait for confirmation** before moving on
- **Group similar flagged items** — Don't ask about 20 similar services one at a time if they can be batched
- **Never show passwords** — Only Title, URL, Username, domain
- **Be concise** — The user has already seen the categorization summary, this is about confirmation and edge cases
- **If a section looks clean** — Don't over-explain. "These {N} entries are in Personal, mostly entertainment and social media. Look good?"
- **Track changes** — Note what was moved, for the summary at the end
