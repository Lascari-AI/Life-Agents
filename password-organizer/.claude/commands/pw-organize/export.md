---
description: Generate per-vault CSV files importable into 1Password
argument-hint: [session-name]
allowed-tools: Read, Write, Glob, Bash, AskUserQuestion
---

# Password Organizer Export

Generate the final per-vault CSV files from the reviewed data, validate them, and provide import instructions.

## Skill Reference

- Skill: `.claude/skills/pw-organize/SKILL.md`

## Variables

```
$1 = session name. If empty, detect from existing session folders.
SESSION_DIR = {$1}
WORKING_DIR = {SESSION_DIR}/working
REVIEWED = {WORKING_DIR}/reviewed.json
OUTPUT_DIR = {SESSION_DIR}/output
```

## Prerequisites

- Review must be complete: `{REVIEWED}` must exist
- If `{REVIEWED}` doesn't exist, tell the user to run `/pw-organize:review` first

## Instructions

### Step 1: Resume Check

If output CSVs already exist in `{OUTPUT_DIR}/`:
1. Run the validation script to check them
2. If valid, show the summary and ask if the user wants to regenerate or is done
3. If invalid or the user wants to regenerate, continue

### Step 2: Generate CSVs

```bash
python3 .claude/skills/pw-organize/scripts/build_export_csvs.py \
  --reviewed "{REVIEWED}" \
  --output-dir "{OUTPUT_DIR}"
```

### Step 3: Validate

```bash
python3 .claude/skills/pw-organize/scripts/validate_export.py \
  --reviewed "{REVIEWED}" \
  --output-dir "{OUTPUT_DIR}"
```

Check the JSON output:
- If `status: "pass"` — all good, proceed to Step 4
- If `status: "fail"` — show the errors, investigate, and fix. Re-run Steps 2-3.

### Step 4: Present Results

```markdown
## Export Complete

### Generated Files (in {OUTPUT_DIR}/)

| File | Vault | Entries |
|------|-------|---------|
| {vault-key}.csv | {Display Name} | {count} |
| ... | ... | ... |
| **summary.md** | Report | — |

### Validation
- Total entries: {count} (matches source)
- No duplicates found
- No entries missing
- CSV format: 1Password compatible

### How to Import into 1Password

1. Open 1Password
2. Create a vault for each category above (if not already existing):
   {list vault display names}
3. For each CSV file:
   - Go to **File → Import**
   - Choose **CSV** as the format
   - Select the CSV file
   - Choose the matching target vault
4. After importing, verify the entries look correct in each vault

### Files are in:
{OUTPUT_DIR}/
```

### Step 5: Cleanup (Optional)

Ask the user:
- "Want to remove the working files (parsed JSON, intermediate data)? The source CSVs and output CSVs will be kept."
- If yes, remove `{WORKING_DIR}/parsed_entries.json`, `{WORKING_DIR}/rules_result.json`, `{WORKING_DIR}/categorized.json` (keep `reviewed.json` and `intake.md` as records)
- If no, keep everything

## Behavior

- **Validate before presenting** — Always run validation before telling the user it's done
- **If validation fails** — Show the specific errors and investigate. Don't just re-run blindly.
- **Never display passwords** — The export CSVs contain passwords, but don't print them to the console
- **Clear import instructions** — The user needs to know exactly how to get these CSVs into 1Password
