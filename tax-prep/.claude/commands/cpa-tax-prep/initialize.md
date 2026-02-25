---
description: Set up a new tax year — create folder structure and show document checklist
argument-hint: [year]
allowed-tools: Read, Write, Bash, AskUserQuestion, Glob
---

# Tax Prep Initialize

Set up the folder structure for a new tax year and guide the user on what documents to gather.

## Skill Reference

- Skill: `.claude/skills/cpa-tax-prep/SKILL.md`
- Checklist: `.claude/skills/cpa-tax-prep/references/cpa-checklist.md`

## Variables

```
$1 = tax year (e.g., "2025"). If empty, prompt for it.
TAXES_DIR = {$1} Taxes
```

## Instructions

### Step 1: Get Tax Year and Name

1. If `$1` is empty, ask the user: "What tax year are we setting up?"
2. Ask for the filer's name (unless resuming an existing session where intake.md already has it)

### Step 2: Run Init Script

```bash
python3 .claude/skills/cpa-tax-prep/scripts/init-session.py --year "$1" --name "{name}"
```

This creates:
- `{year} Taxes/` — Top-level year folder
- `{year} Taxes/{year} taxes write up/` — Working directory
- `{year} Taxes/{year} taxes write up/output/` — Deliverables directory
- `{year} Taxes/{year} taxes write up/intake.md` — Intake file from template
- `{year} Taxes/source-documents/` — Document drop zone with subdirectories

### Step 3: Show Document Checklist

Read `.claude/skills/cpa-tax-prep/references/cpa-checklist.md` and present it to the user.

Tell the user:

```
Your tax year folder is ready. Drop your documents into the folders inside source-documents/:

  source-documents/
  ├── bank-statements/      ← Monthly PDFs, organized by account
  ├── quarterly-estimates/   ← Federal + state payment receipts
  ├── income/               ← 1099s, income summaries
  ├── health-insurance/     ← Coverage docs, 1095-A forms
  └── other/                ← Home office notes, receipts, anything else
```

### Step 4: Show Next Steps

Tell the user:

1. Drop your documents into the folders above
2. For bank statements, create a subfolder per account (e.g., `bank-statements/Business Account/`)
3. When your documents are in place, run `/cpa-tax-prep:intake {year}` to start the interview

## Behavior

- If the year folder already exists with an intake.md, report the existing session status instead of creating a new one
- Keep it brief — this is setup, not the interview
- If `source-documents/` already exists, don't recreate it — just confirm it's there
