---
description: Generate the final CPA deliverables — xlsx spreadsheet with tabs and a summary document
argument-hint: [year]
allowed-tools: Read, Write, Edit, Glob, Bash, Task, AskUserQuestion
---

# Tax Prep Package

Produce the final CPA-ready deliverables: an xlsx spreadsheet with tabs for each section and a markdown summary document.

## Skill Reference

- Output templates: `.claude/skills/cpa-tax-prep/references/output-templates.md`
- JSON schema: `.claude/skills/cpa-tax-prep/references/tax-data-schema.md`
- Subagent prompt template: `.claude/skills/cpa-tax-prep/references/package-subagent-prompt.md`
- Merge script: `.claude/skills/cpa-tax-prep/scripts/merge_sections.py`
- Build script: `.claude/skills/cpa-tax-prep/scripts/build_xlsx.py`
- Validation script: `.claude/skills/cpa-tax-prep/scripts/validate_xlsx.py`

## Variables

```
$1 = tax year (e.g., "2025"). If empty, detect from existing files.
TAXES_DIR = {$1} Taxes
WRITEUP_DIR = {TAXES_DIR}/{$1} taxes write up
INTAKE = {WRITEUP_DIR}/intake.md
FINAL_DIR = {WRITEUP_DIR}/final
OUTPUT_DIR = {WRITEUP_DIR}/output
SECTIONS_DIR = {OUTPUT_DIR}/sections
```

## Prerequisites

- Review must be complete: finalized files should exist in `{FINAL_DIR}/`
- If `{FINAL_DIR}/` is empty or doesn't exist (but `{WRITEUP_DIR}/raw/` has files), tell the user to run `/cpa-tax-prep:review` first

## Instructions

### Step 1: Load Data

1. Read `{INTAKE}` for filer info
2. List all finalized files from `{FINAL_DIR}/` — note their exact filenames
3. Read `.claude/skills/cpa-tax-prep/references/tax-data-schema.md` for the exact JSON schema
4. Read `.claude/skills/cpa-tax-prep/references/package-subagent-prompt.md` for the subagent prompt template

### Step 2: Build Section Manifest

Create a manifest of 6 subagents to spawn. Each entry maps a section to its source file(s) and output path(s):

| Subagent | Section Key(s) | Source File(s) | Output File(s) |
|----------|---------------|----------------|-----------------|
| income | `income` | `{FINAL_DIR}/Income {year}.md` | `{SECTIONS_DIR}/income.json` |
| business_expenses | `business_expenses` | `{FINAL_DIR}/Expenses * {year}.md` | `{SECTIONS_DIR}/business_expenses.json` |
| personal_deductions | `personal_deductions` | `{FINAL_DIR}/Personal Deductions {year}.md` | `{SECTIONS_DIR}/personal_deductions.json` |
| home_office | `home_office` | `{FINAL_DIR}/Personal Deductions {year}.md` + `{INTAKE}` | `{SECTIONS_DIR}/home_office.json` |
| est_taxes_and_retirement | `estimated_taxes` + `retirement` | `{FINAL_DIR}/Estimated Taxes {year}.md` | `{SECTIONS_DIR}/estimated_taxes.json` + `{SECTIONS_DIR}/retirement.json` |
| health_insurance | `health_insurance` | `{FINAL_DIR}/Health Insurance {year}.md` | `{SECTIONS_DIR}/health_insurance.json` |

**Resume support**: Check if `{SECTIONS_DIR}/` already has valid section JSONs. If any exist and are valid JSON with the correct top-level key, skip those subagents and only spawn the missing ones. Report which sections are being reused vs regenerated.

Create the sections directory:

```bash
mkdir -p "{SECTIONS_DIR}"
```

### Step 3: Spawn Parallel Subagents

For each subagent in the manifest, build a prompt from the template by filling in:
- `{SECTION_NAME}` — the section key (e.g., `income`)
- `{PRIMARY_SOURCE_FILE}` — the absolute path to the source file(s)
- `{OUTPUT_PATH}` — the absolute path to the output JSON file
- `{YEAR}` — the tax year
- `{INTAKE_CONTEXT}` — the filer info section from intake.md (for home_office, include full intake; for others, just filer basics)
- `{SECTION_SCHEMA}` — the relevant section from tax-data-schema.md (copy the exact schema for this section)
- `{TYPE_SPECIFIC_INSTRUCTIONS}` — the matching type-specific block from the template

**Spawn all 6 subagents in parallel** using the Task tool with `subagent_type: "general-purpose"` and `model: "sonnet"`. Each subagent gets:
- `allowed-tools: Read, Write, Glob` in its prompt
- The filled-in prompt template
- A description like "Package {section_name} section"

Example Task call pattern (repeat for each subagent):
```
Task(
  description: "Package income section",
  subagent_type: "general-purpose",
  model: "sonnet",
  prompt: <filled template>
)
```

**Important**: Launch all 6 Task calls in a single message so they run in parallel.

### Step 4: Verify Section JSONs

After all subagents complete, verify each of the 7 expected section files:

1. Check all 7 files exist in `{SECTIONS_DIR}/`: `income.json`, `business_expenses.json`, `personal_deductions.json`, `home_office.json`, `estimated_taxes.json`, `retirement.json`, `health_insurance.json`
2. Read each file and verify it's valid JSON with the correct top-level key
3. Check that currency values are numbers, not strings

If any file is missing or invalid, retry that specific subagent (re-spawn just the failed one). After retry, verify again.

### Step 5: Merge into Monolithic JSON

Run the merge script to combine all section JSONs:

```bash
python3 .claude/skills/cpa-tax-prep/scripts/merge_sections.py \
  --sections-dir "{SECTIONS_DIR}" \
  --filer-json '<filer JSON from intake>' \
  --year {year} \
  --source-files "final/Income {year}.md,final/Expenses ... {year}.md,..." \
  --output "{OUTPUT_DIR}/{year}_tax_data.json"
```

The `--filer-json` argument should be a JSON string with the filer object extracted from intake.md (name, business, entity, states, filing_status, address, address_change, phone, email).

The `--source-files` argument should be a comma-separated list of the finalized files (relative paths from the writeup dir).

Review the merge script's JSON output summary to confirm success.

### Step 6: Build the Spreadsheet

Run the deterministic builder:

```bash
python3 .claude/skills/cpa-tax-prep/scripts/build_xlsx.py "{OUTPUT_DIR}/{year}_tax_data.json" "{OUTPUT_DIR}/{year} CPA Tax Package.xlsx"
```

This script:
- Creates an 8-tab workbook with proper formatting (blue headers, currency formatting, bold totals)
- Uses SUM formulas for totals (not hardcoded sums)
- Wires Summary tab totals to other tabs via cross-sheet formulas
- Runs recalc.py automatically
- Prints a JSON result summary with computed totals

**Do NOT write any openpyxl code.** The builder script handles all spreadsheet creation deterministically.

If the builder fails, read the error output and fix the JSON file — do not modify the builder script.

### Step 7: Validate

Run the validation script:

```bash
python3 .claude/skills/cpa-tax-prep/scripts/validate_xlsx.py "{OUTPUT_DIR}/{year}_tax_data.json" "{OUTPUT_DIR}/{year} CPA Tax Package.xlsx"
```

This checks:
- Every data cell in the xlsx matches the JSON
- Row counts match (no missing or extra rows)
- Totals from SUM formulas match expected sums
- All 8 tabs exist

If validation fails, review the error details. Fix the JSON (either edit it directly or re-run the failing subagent + merge) and re-run steps 6–7.

### Step 8: Build the Summary

Create `{OUTPUT_DIR}/{year} CPA Summary.md`:

```markdown
# {YEAR} Tax Preparation — {NAME} / {BUSINESS}

## Filing Info
- Entity: {type}
- State(s): {states}
- Address: {address}
- Address changes: {if any}

## Annual Totals
| Category | Amount |
|----------|--------|
| Gross Income | ${total} |
| Business Expenses | ${total} |
| Home Office Deduction | ${total} |
| Health Insurance | ${total} |
| Est. Taxes (Federal) | ${total} |
| Est. Taxes (State) | ${total} |
| Retirement Contributions | ${total} |

## Attached Documents
- {year} CPA Tax Package.xlsx — Full detailed breakdown
- Bank statements: {count} files
- Quarterly estimate receipts: {count} files
- Health insurance docs: {count} files
- {other supporting docs}

## Questions for CPA
{numbered list from summary.cpa_questions — items needing CPA input}

## Notes
{numbered list from summary.cpa_notes — informational context for CPA}
```

Use the totals from the JSON (or from the builder's output) to populate the summary — don't re-derive them from the source files. The questions/notes split comes from the JSON `summary.cpa_questions` and `summary.cpa_notes` arrays (separated automatically by the merge script based on "ASK CPA" prefix).

### Step 9: Final Checklist

Present to the user:

```markdown
## CPA Package Complete

### Deliverables (in {OUTPUT_DIR}/)
- **{year}_tax_data.json** — Structured data (source of truth)
- **{year} CPA Tax Package.xlsx** — Spreadsheet with 8 tabs
- **{year} CPA Summary.md** — One-page overview

### Validation
- [ ] `validate_xlsx.py` passed: {checks} checks, {errors} errors
- [ ] Income total: ${X}
- [ ] Expenses total: ${X}
- [ ] All 8 tabs populated
- [ ] ASK CPA items listed
- [ ] Supporting PDFs organized

### What to Send Your CPA
1. {year} CPA Tax Package.xlsx
2. {year} CPA Summary.md
3. All bank statement PDFs (in {TAXES_DIR}/source-documents/bank-statements/)
4. Income summary/1099s
5. Quarterly estimate receipts
6. Health insurance documentation
7. Any other supporting documents

Everything is in: {WRITEUP_DIR}/
```

### Step 10: Cleanup (Optional)

Ask the user if they want to:
- Remove the `raw/`, `extractions/`, and `output/sections/` working directories (keep only `final/` and `output/` deliverables)
- Keep everything as-is for records

## Behavior

- Read tax-data-schema.md carefully before filling template — each subagent gets only its relevant schema section
- Never write openpyxl code directly — always use build_xlsx.py
- If any data is missing, note it in `_cpa_items` rather than omitting the field
- If validation fails, fix the JSON and re-run — don't modify the builder script
- The JSON file is the source of truth — the xlsx is derived from it deterministically
- Section JSONs in `output/sections/` are intermediate artifacts — the monolithic JSON is the deliverable
