---
description: Auto-categorize all password entries into vault categories using rules and AI knowledge
argument-hint: [session-name]
allowed-tools: Read, Write, Edit, Glob, Bash, AskUserQuestion
---

# Password Organizer Categorize

Apply deterministic rules first, then use AI service knowledge to categorize remaining entries. Flag truly ambiguous items for the review phase.

## Skill Reference

- Skill: `.claude/skills/pw-organize/SKILL.md`
- Categorization rules: `.claude/skills/pw-organize/references/categorization-rules.md`
- Service knowledge: `.claude/skills/pw-organize/references/service-knowledge.md`

## Variables

```
$1 = session name. If empty, detect from existing session folders.
SESSION_DIR = {$1}
WORKING_DIR = {SESSION_DIR}/working
INTAKE = {WORKING_DIR}/intake.md
PARSED = {WORKING_DIR}/parsed_entries.json
RULES_RESULT = {WORKING_DIR}/rules_result.json
CATEGORIZED = {WORKING_DIR}/categorized.json
```

## Prerequisites

- Intake must be complete: `{INTAKE}` must exist with status "Complete"
- Parsed entries must exist: `{PARSED}` must exist (created during intake)
- If either is missing, tell the user to run the appropriate prior command

## Instructions

### Step 1: Resume Check

If `{CATEGORIZED}` already exists:
1. Read it and check if all entries have a vault assigned
2. If complete, show the summary and suggest `/pw-organize:review {session}`
3. If partial (some entries have no vault), continue from the AI classification step

### Step 2: Load Context

1. Read `{INTAKE}` to understand:
   - Email/domain mappings
   - Vault categories
   - User-defined rules
   - Handling preferences
2. Read `{PARSED}` for entry count and stats
3. Read `.claude/skills/pw-organize/references/categorization-rules.md`
4. Read `.claude/skills/pw-organize/references/service-knowledge.md`

### Step 3: Apply Deterministic Rules

Run the rules engine:

```bash
python3 .claude/skills/pw-organize/scripts/apply_rules.py \
  --entries "{PARSED}" \
  --intake "{INTAKE}" \
  --output "{RULES_RESULT}"
```

Read the output and report:
```markdown
## Rules Engine Results

- **Matched**: {count} entries classified by rules
  - Email match: {count}
  - Domain match: {count}
  - User-defined rules: {count}
- **Unmatched**: {count} entries need AI classification

Proceeding to AI classification...
```

### Step 4: AI Classification

Read `{RULES_RESULT}`. For each entry where `vault` is `null`:

1. Look at the entry's Title, URL/domain, and Username
2. Using the service knowledge framework, determine:
   - What service is this?
   - Is it clearly personal, clearly business, or ambiguous?
3. Assign:
   - `vault` — the vault key from the user's defined categories
   - `method` — `"ai:service-knowledge"`
   - `confidence` — `"high"`, `"medium"`, or `"low"`
   - `flag` — set based on confidence:
     - `null` if high confidence
     - `"ambiguous"` if medium confidence and could go either way
     - `"shared-service"` if the service is known to be used for both personal and business (check service-knowledge.md)
     - `"unknown-service"` if you can't identify what the service is
     - `"no-data"` if the entry has minimal identifying information (no URL, no username)
   - `notes` — brief explanation for medium/low confidence entries

**Processing approach**:
- Work through entries in batches. You don't need to present each one individually.
- For obvious classifications (Netflix=personal, AWS=business), assign silently.
- For entries you're unsure about, still assign your best guess but flag them.
- Entries with absolutely no identifying data (no URL, no username, just a generic title) → assign to the "unknown" vault with `flag: "no-data"`.

After classifying all entries, write the complete result to `{CATEGORIZED}`:

The JSON structure should be:
```json
{
  "stats": { ... (from parsed) },
  "vault_categories": [ ... (from intake) ],
  "entries": [
    {
      "original_row": { ... },
      "_source_file": "...",
      "_row_number": 1,
      "_parsed_domain": "...",
      "_parsed_email": "...",
      "vault": "personal",
      "method": "rule:email-match",
      "confidence": "high",
      "flag": null,
      "notes": null
    },
    ...
  ]
}
```

### Step 5: Present Summary

Show the user a summary:

```markdown
## Categorization Complete

| Vault | Count | By Rules | By AI |
|-------|-------|----------|-------|
| {vault} | {total} | {rules} | {ai} |
| ... | ... | ... | ... |

### Flagged for Review: {count}
- {N} ambiguous (could go either way)
- {N} shared services (used for both personal/business)
- {N} unknown services (unrecognizable)
- {N} no data (minimal identifying info)

### Next Step
Run `/pw-organize:review {session}` to review the results and resolve flagged items.
```

## Behavior

- **Never display passwords** — Only use Title, URL, Username, and domain for classification
- **Be consistent** — If you classify Dropbox as business for one entry, classify all Dropbox entries the same way (unless different emails are used)
- **When truly uncertain, flag it** — Better to flag and ask than to silently miscategorize
- **Batch processing** — Don't present every entry individually. Work through them programmatically and present the summary.
- **Respect user rules** — User-defined rules from intake always override AI judgment
