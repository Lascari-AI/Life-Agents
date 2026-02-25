---
description: Start a tax prep intake interview — understand the filer's situation, accounts, and special considerations before processing
argument-hint: [year]
allowed-tools: Read, Write, Edit, Glob, Bash, AskUserQuestion, Skill
---

# Tax Prep Intake

Conversational interview to understand the filer's situation before touching any documents. Pre-reads available documents and leads with findings so the user confirms rather than recites from scratch.

## Skill Reference

Read the cpa-tax-prep skill for templates and full documentation:
- Skill: `.claude/skills/cpa-tax-prep/SKILL.md`
- Checklist: `.claude/skills/cpa-tax-prep/references/cpa-checklist.md`

## Variables

```
$1 = tax year (e.g., "2025"). If empty, prompt for it.
TAXES_DIR = {$1} Taxes
WRITEUP_DIR = {TAXES_DIR}/{$1} taxes write up
PRIOR_YEAR = {$1 - 1}
PRIOR_DIR = {PRIOR_YEAR} Taxes
PRIOR_WRITEUP = {PRIOR_DIR}/{PRIOR_YEAR} taxes write up
```

## Instructions

### Step 1: Initialize

1. If `$1` is empty, ask the user for the tax year
2. Run the init script:
   ```bash
   python3 .claude/skills/cpa-tax-prep/scripts/init-session.py --year "$1" --name "TBD"
   ```
3. Read `.claude/skills/cpa-tax-prep/references/cpa-checklist.md` for the full document checklist

### Step 2: Discovery Scan

Before asking any questions, scan all available documents to pre-populate answers.

**Inventory the folder** — Use `Glob` and `ls` to map out everything in `{TAXES_DIR}/source-documents/`:
- Bank statement folders in `source-documents/bank-statements/`: note each account name and how many monthly PDFs
- Quarterly estimate files in `source-documents/quarterly-estimates/`: note which quarters have PDFs
- Health insurance documents in `source-documents/health-insurance/`
- Income documents in `source-documents/income/`
- Other documents in `source-documents/other/` (home office notes, receipts, etc.)
- Also check `{TAXES_DIR}/` root for any documents not yet moved into `source-documents/`

**Read non-bank-statement documents** — Use the `pdf` skill to extract key data from:
- Health insurance PDFs → provider name, monthly premium, coverage dates, form type
- Quarterly estimate PDFs (each quarter) → federal amount, state amount, confirmation numbers
- Income summary PDFs → total income, source breakdown
- Do NOT read bank statement PDFs (that's the extract phase)

**Read non-PDF documents:**
- Home office markdown files → sq ft, rent, percentage, move details

**Check prior year** — If `{PRIOR_DIR}/` exists:
- Read `{PRIOR_DIR}/intake.md` if it exists (for name, business, entity type, accounts, categories)
- Read any write-up files in `{PRIOR_WRITEUP}/` for baseline context
- This gives you the filer's name, business details, account structure, and recurring patterns

**Hold all findings in context** — Do not write a discovery file. Use findings to drive the interview in Step 4.

### Step 3: Resume Check

Read the existing `{WRITEUP_DIR}/intake.md` and check `<!-- STATUS: -->` markers:

- **All `complete`** → Intake is done. Tell the user what's captured and suggest running `/cpa-tax-prep:extract {year}`. Stop here.
- **Mix of `complete` and `pending`** → Resuming a broken session. Summarize what's already captured, then continue from the first `pending` section in Step 4.
- **All `pending`** → Fresh start. Proceed to Step 4 from the beginning.
- **No STATUS markers** → Legacy intake file. Ask the user if they want to redo the intake or keep the existing file.

### Step 4: Interview

9 sections, each following this pattern:
1. **Lead with findings** — Present what you discovered from documents and prior year ("I found X — is that correct?")
2. **Confirm or correct** — Let the user confirm, adjust, or add details
3. **Fall back to questions** — Only ask from scratch when no data was found for a section
4. **Save immediately** — After the user confirms, `Edit` that section in `{WRITEUP_DIR}/intake.md`:
   - Replace the section content with confirmed data
   - Flip `<!-- STATUS: pending -->` to `<!-- STATUS: complete -->`
   - Update the header's `Sections Completed` count (e.g., `1/9`, `2/9`, etc.)
   - Update the `Last Updated` date

Ask one section at a time. Wait for the user's response before moving to the next.

#### Section 1: Filer
Pre-fill from prior year if available: name, business name, entity type, address, states.
- Full name
- What do you do? (freelance, LLC, sole prop, S-corp)
- Business name (if applicable)
- Current address
- Did you move during the year?
- What state(s) did you live/work in?
- Phone, email
- Filing status, dependents

#### Section 2: Accounts
Lead with bank statement folder names found during discovery scan.
- For each folder found: confirm the account name, type (business/personal/savings), and treatment
- For mixed accounts: what specific business transactions should we look for?
- How are things paid? (direct, Venmo, Zelle)
- Any accounts NOT represented by a folder?

#### Section 3: Home Office
Lead with home office write-up file if found (sq ft, rent, percentage, move details).
- If write-up exists: "I found your home office calculation showing X — is this correct?"
- If not: office sq ft, home sq ft, rent, any mid-year moves

#### Section 4: Health Insurance
Lead with PDF extraction if a health insurance document was found.
- Provider, monthly premium, coverage period
- Any changes mid-year?
- Paid through which account/method?

#### Section 5: Internet / Utilities
Lead with prior year data or context from home office section.
- Internet provider and monthly cost
- Utilities (if claiming home office)
- Home office percentage applies to these

#### Section 6: Quarterly Estimated Taxes
Lead with PDF extractions from each quarter's folder.
- Federal amounts per quarter
- State amounts per quarter (which state?)
- Confirmation numbers if extracted

#### Section 7: Retirement
Lead with prior year data if found.
- Any retirement contributions? (Roth IRA, SEP, 401k)
- Amount and when funded
- If none, note "No contributions for {year}"

#### Section 8: Income
Lead with income summary PDF if found.
- Sole source or multiple?
- Total amount if extracted
- Any W-2 income?

#### Section 9: Special Considerations + Documents
Catch-all section. Two parts:

**Special Considerations:**
- Anything unusual this year?
- Items the user is unsure about deducting → flag as "ASK CPA"
- Vehicle use for business?
- Large or unusual purchases?

**Documents Provided & Missing:**
- Walk through what's in the folder vs. the CPA checklist
- Update the Documents Provided checklist with what's confirmed
- Flag what's missing

After completing this section, also update the `## Documents Provided` and `## Missing Documents` sections in intake.md.

### Step 5: Wrap Up

1. Set the header `Status` to `Complete`
2. Set `Sections Completed` to `9/9`
3. Update `Last Updated` date
4. Tell the user:
   - What's captured in intake.md
   - What documents are still missing (if any)
   - Next step: run `/cpa-tax-prep:extract {year}` to process the bank statements

## Behavior

- **Lead with findings** — Always present what you discovered before asking. Confirm rather than interrogate.
- **Save incrementally** — Write to intake.md after EACH section. Do not batch saves to the end.
- **Update STATUS markers** — Flip `<!-- STATUS: pending -->` to `<!-- STATUS: complete -->` per section for resume support.
- **Keep it conversational** — This should feel like talking to a helpful preparer, not filling out a form.
- **Don't read bank statements** — Transaction extraction belongs to the extract phase.
- **If a section is skipped** — Write "Skipped — will revisit" and mark as `complete` so the interview can move forward. The user can re-run intake later if needed.
- **On resume** — Summarize what's already captured before continuing with pending sections.
- **If the user mentions something unclear** — Ask follow-up questions.
- **Don't assume** — If you're unsure about something, ask.
- **No tax advice** — This prepares documents; the CPA does the rest.
