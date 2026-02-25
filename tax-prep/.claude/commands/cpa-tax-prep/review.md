---
description: Review extracted tax data with the user section by section before packaging
argument-hint: [year]
allowed-tools: Read, Write, Edit, Glob, AskUserQuestion
---

# Tax Prep Review

Walk through the extracted data with the user, confirm accuracy, resolve flagged items, and finalize everything before packaging.

## Variables

```
$1 = tax year (e.g., "2025"). If empty, detect from existing raw files.
TAXES_DIR = {$1} Taxes
WRITEUP_DIR = {TAXES_DIR}/{$1} taxes write up
INTAKE = {WRITEUP_DIR}/intake.md
RAW_DIR = {WRITEUP_DIR}/raw
FINAL_DIR = {WRITEUP_DIR}/final
```

## Prerequisites

- Extraction must be complete: raw files should exist in `{RAW_DIR}/`
- If raw files don't exist, tell the user to run `/cpa-tax-prep:extract` first

## Instructions

### Step 1: Load Context

1. Read `{WRITEUP_DIR}/intake.md` for reference
2. Read all `.md` files from `{RAW_DIR}/`
3. Identify all flagged items (marked with "?", "ASK CPA", or "uncertain")
4. Note: per-file extractions exist in `{WRITEUP_DIR}/extractions/` — use these to drill into specific transactions when a raw file entry needs investigation (each per-file extraction has the original source PDF path in its front matter)

### Step 2: Review Income

Present the monthly income breakdown to the user:

```markdown
## Income Review

| Month | Amount |
|-------|--------|
| January | $X,XXX |
| ... | ... |
| **TOTAL** | **$XX,XXX** |
```

Ask:
- Does this total match your expectations?
- Any months look off?
- Any income sources missing?

If the user has a 1099 or income summary PDF, cross-reference against it.

### Step 3: Review Business Expenses

Present expenses in two sections:

**Monthly Recurring** — Show each recurring charge with the months it appeared

**One-Time Purchases** — Show sorted by date with category

Ask:
- Anything miscategorized?
- Any expenses missing that you remember?
- Any items that are actually personal?

### Step 4: Review Personal Deductions

Present each flagged personal item:

```markdown
## Personal Deductions

| Type | Monthly | Annual | Payment Method |
|------|---------|--------|----------------|
| Rent | $3,300 | $39,600 | Venmo |
| Internet | $72 | $864 | Venmo |
| ... | ... | ... | ... |
```

Ask:
- Are these amounts correct?
- Anything else from personal accounts we should include?
- Any items that are NOT deductible after all? (move to "ASK CPA" if unsure)

### Step 5: Review Home Office

If a home office write-up exists, present it. If not, build it from intake:

```markdown
## Home Office

| Detail | Value |
|--------|-------|
| Office | {X} sq ft |
| Home | {X} sq ft |
| Rent | ${X}/month |
| Office % | {X}% |
| Monthly deduction | ${X} |
| **Annual** | **${X}** |
```

For mid-year moves, show each location separately with subtotals.

Ask: Does this look right?

### Step 6: Review Flagged & Uncertain Items

Present every item that was flagged during extraction:

```markdown
## Items Needing Decision

1. **{description}** — ${amount} on {date}
   - Found in: {account}
   - Question: {why it's flagged}
   - Options: Business expense / Personal / ASK CPA

2. ...
```

Use AskUserQuestion for each flagged item to get a decision:
- Categorize as business expense (which category?)
- Mark as personal (exclude)
- Flag as "ASK CPA" (include with note)

### Step 7: Review Estimated Taxes, Health Insurance, Retirement

Present each briefly — these are usually straightforward but confirm:
- Estimated tax payments: dates, amounts, confirmation numbers
- Health insurance: provider, amounts, coverage dates
- Retirement: type, amount, date

### Step 8: Finalize

After all sections are reviewed:

1. Copy reviewed files from `{RAW_DIR}/` to `{FINAL_DIR}/` with any corrections applied
2. Update intake.md status to "Review Complete"
3. Present final summary:

```markdown
## Review Complete

### Final Totals
| Category | Amount |
|----------|--------|
| Gross Income | ${X} |
| Business Expenses | ${X} |
| Home Office Deduction | ${X} |
| Health Insurance | ${X} |
| Est. Taxes (Federal) | ${X} |
| Est. Taxes (State) | ${X} |
| Retirement | ${X} |

### ASK CPA Items
- {list any items flagged for CPA}

### Next Step
Run `/cpa-tax-prep:package` to generate the CPA spreadsheet and summary.
```

## Behavior

- Go section by section — don't dump everything at once
- After each section, wait for confirmation before moving on
- When the user corrects something, update the file in `{RAW_DIR}/` immediately
- Keep a running list of "ASK CPA" items for the final summary
- Be concise — the user has already seen this data during extraction, this is about confirmation not re-presentation
- If a section looks clean and simple, don't over-explain — just show and ask "look good?"
