---
description: Scan documents and extract transactions from bank statements based on intake notes
argument-hint: [year]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion, Task
---

# Tax Prep Extract

Inventory all documents in the tax year folder, then spawn parallel subagents to read bank statement PDFs and extract/categorize every relevant transaction using the intake notes as a guide.

## Skill Reference

- Skill: `.claude/skills/cpa-tax-prep/SKILL.md`
- Output templates: `.claude/skills/cpa-tax-prep/references/output-templates.md`
- Extraction schema: `.claude/skills/cpa-tax-prep/references/extraction-schema.md`
- Subagent prompt: `.claude/skills/cpa-tax-prep/references/extract-subagent-prompt.md`
- Checklist: `.claude/skills/cpa-tax-prep/references/cpa-checklist.md`

## Variables

```
$1 = tax year (e.g., "2025"). If empty, detect from existing intake.md files.
TAXES_DIR = {$1} Taxes
WRITEUP_DIR = {TAXES_DIR}/{$1} taxes write up
INTAKE = {WRITEUP_DIR}/intake.md
EXTRACTIONS_DIR = {WRITEUP_DIR}/extractions
RAW_DIR = {WRITEUP_DIR}/raw
```

## Prerequisites

- Intake must be complete: `{WRITEUP_DIR}/intake.md` must exist with status "Complete"
- Bank statement PDFs should be in `{TAXES_DIR}/source-documents/bank-statements/`

## Instructions

### Step 1: Load Intake

1. Read `{WRITEUP_DIR}/intake.md` to understand:
   - Which accounts exist and how to treat each one
   - What to look for in personal accounts
   - Special considerations and flagged items
2. If intake.md doesn't exist or is incomplete, tell the user to run `/cpa-tax-prep:intake` first
3. Extract two key sections for subagent context:
   - **Accounts section** — everything about what accounts exist, their names, and how to treat them
   - **Special considerations** — flagged items, unusual situations, things to watch for

### Step 2: Inventory

Scan `{TAXES_DIR}/source-documents/` recursively. Report:

```markdown
## Document Inventory

### Bank Statements
- Business Account: {count} files ({date range})
- Personal Account: {count} files ({date range})
- {Other accounts}: {count} files

### Other Documents
- Income: {list files found}
- Quarterly Estimates: {list files found}
- Health Insurance: {list files found}
- {etc.}

### Missing
- {anything from checklist not found}
```

Ask the user to confirm this looks right before proceeding.

### Step 3: Create Working Directories

```bash
mkdir -p "{EXTRACTIONS_DIR}" "{RAW_DIR}"
```

### Step 4: Build Manifest

Create a manifest mapping each source file to its extraction output. For each document found in the inventory:

1. Determine the **document type**: `business-statement`, `personal-statement`, `savings`, `income-summary`, `quarterly-estimate`, `health-insurance`
2. Determine the **output filename**:
   - Business statements: `business-{year}-{MM}.md` (one per month)
   - Personal statements: `personal-{year}-{MM}.md` (one per month)
   - Savings: `savings-{account-name}.md` (one per account)
   - Income summaries: `income-summary.md`
   - Quarterly estimates: `quarterly-q{N}.md` (one per quarter, NOT per PDF)
   - Health insurance: `health-insurance.md`
3. Set **output path**: `{EXTRACTIONS_DIR}/{output filename}`
4. **Check for existing extractions** (resume support): Read any existing output file and check the YAML front matter. If `status: complete`, mark this file as **skip** in the manifest.

**Quarterly estimate grouping**: If multiple PDFs exist for the same quarter (e.g., federal + state), group them into a single subagent that reads all PDFs for that quarter.

Report the manifest to the user:

```markdown
## Extraction Plan

### To Extract ({count} files)
- {source file} -> {output file} ({document type})
- ...

### Skipping ({count} already complete)
- {output file} — already extracted
- ...
```

### Step 5: Spawn Subagents

1. Read the subagent prompt template from `.claude/skills/cpa-tax-prep/references/extract-subagent-prompt.md`
2. Read the extraction schema from `.claude/skills/cpa-tax-prep/references/extraction-schema.md`
3. For each file in the manifest that is NOT skipped, build a subagent prompt by filling in the template placeholders:
   - `{SOURCE_FILE}` — the source PDF path
   - `{DOCUMENT_TYPE}` — from the manifest
   - `{OUTPUT_PATH}` — from the manifest
   - `{PERIOD}` — the month/quarter/year
   - `{INTAKE_ACCOUNTS_SECTION}` — from Step 1
   - `{INTAKE_SPECIAL_CONSIDERATIONS}` — from Step 1
   - `{TYPE_SPECIFIC_INSTRUCTIONS}` — the matching block from the template
   - `{SCHEMA}` — the matching schema example from extraction-schema.md

4. **Spawn all subagents in parallel** using the Task tool:
   - Use `subagent_type: "general-purpose"` for each
   - Each subagent gets a description like `"Extract {document_type} {period}"`
   - Each subagent reads ONE PDF (or a small group for quarterly estimates) and writes ONE output file
   - Use `model: "sonnet"` for each subagent to balance speed and cost

5. Wait for all subagents to complete.

**Important**: Launch all Task calls in a single message to maximize parallelism. Each subagent operates independently — they don't need each other's results.

### Step 6: Verify Extractions

After all subagents return:

1. Read each expected output file in `{EXTRACTIONS_DIR}/`
2. Check the YAML front matter `status` field
3. Report results:

```markdown
## Extraction Results

### Successful ({count})
- {output file} — {document type}, {period}

### Partial ({count}) — data extracted but with gaps
- {output file} — {error description}

### Failed ({count})
- {output file} — {error description}
```

If any files failed:
- Ask the user if they want to retry the failed files (spawn new subagents for just those)
- Or skip them and note gaps in the aggregated output

### Step 7: Aggregate into Raw Files

Read all complete/partial extraction files and merge them into the monolithic raw files that the review command expects:

- **`Income {year}.md`** — Combine deposit tables from all `business-statement` extractions into monthly totals. Cross-reference with `income-summary` extraction if it exists.

- **`Expenses {business name} {year}.md`** — Combine expense tables from all `business-statement` extractions. Deduplicate recurring vendors across months (group into one recurring entry with all dates). List one-time purchases sorted by date.

- **`Personal Deductions {year}.md`** — Combine flagged transactions from all `personal-statement` extractions. Group by type (rent, internet, utilities, etc.) with monthly breakdown.

- **`Estimated Taxes {year}.md`** — Directly from `quarterly-estimate` extractions. Organize by quarter, then by authority.

- **`Health Insurance {year}.md`** — Directly from `health-insurance` extraction.

Use the business name from intake.md for the expenses filename. Write all files to `{RAW_DIR}/`.

### Step 8: Present Summary

Show the user a high-level summary:

```markdown
## Extraction Complete

### Income
- Annual total: ${amount}
- Months covered: {count}/12

### Business Expenses
- Total: ${amount}
- Categories: {count} categories, {count} transactions
- Top categories: {list top 3 by amount}

### Personal Deductions Found
- Rent: ${amount}/month x {months}
- Internet: ${amount}/month x {months}
- {other items}

### Flagged Items
- {anything uncertain or ambiguous}

### Next Step
Run `/cpa-tax-prep:review` to walk through these findings.
```

## Behavior

- Process statements in chronological order within aggregated files (January first)
- When a transaction is ambiguous, subagents add it with a "?" flag — nothing is skipped
- If a bank statement is unreadable or partially readable, the subagent sets status to "partial" and notes gaps
- For Venmo/Zelle, subagents note the platform in the description
- Use exact cents — don't round
- If a subagent finds something unexpected (large transfer, unusual charge), it flags it for the review phase
- On resume: existing `status: complete` extractions are skipped, only incomplete/missing files are re-extracted
