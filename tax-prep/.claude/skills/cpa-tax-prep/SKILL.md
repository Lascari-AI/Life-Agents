---
name: cpa-tax-prep
description: >
  Compiles and organizes all financial documents for a self-employed individual
  to send to a CPA. Session-based flow with slash commands for each phase:
  intake interview, document extraction, review, and final packaging.
  Reads bank statement PDFs, extracts transactions, categorizes expenses,
  summarizes income, identifies deductions, and produces a CPA-ready
  spreadsheet (xlsx with tabs) plus a summary document.
  Use when: preparing tax documents for an accountant, organizing bank statements
  for taxes, compiling self-employment income and expenses, building a CPA tax
  packet, or any end-of-year tax document preparation for a sole proprietor or LLC.
---

# CPA Tax Prep

Tax document preparation for self-employed individuals. Walks through four phases via slash commands, producing a CPA-ready package.

This is document preparation, not tax filing.

## Session Lifecycle

```
/cpa-tax-prep:initialize ──▶ /cpa-tax-prep:intake ──▶ /cpa-tax-prep:extract ──▶ /cpa-tax-prep:review ──▶ /cpa-tax-prep:package
       (SETUP)                  (INTERVIEW)              (SCAN + PROCESS)           (CONFIRM)               (OUTPUT)
```

## Commands

| Command | Phase | What It Does |
|---------|-------|--------------|
| `/cpa-tax-prep:initialize [year]` | 0. Setup | Creates the year folder, source-documents directory, and intake template. |
| `/cpa-tax-prep:intake [year]` | 1. Intake | Conversational interview: who you are, your accounts, special deductions, documents provided. Saves to `{year} taxes write up/intake.md`. |
| `/cpa-tax-prep:extract [year]` | 2. Extract | Inventories documents, reads bank statement PDFs, extracts and categorizes all transactions. Saves raw working files. |
| `/cpa-tax-prep:review [year]` | 3. Review | Walks through extracted data section by section for confirmation. Resolves flagged items. Finalizes working files. |
| `/cpa-tax-prep:package [year]` | 4. Package | Generates the xlsx spreadsheet (8 tabs) and CPA summary markdown. |
| `/cpa-tax-prep:add-vertical [name]` | Utility | Adds a new document type and/or packaging section (spreadsheet tab) to the system. Interactive interview, then edits all touchpoint files. |

## File Structure

```
{year} Taxes/
├── source-documents/                  ← User drops source docs here
│   ├── bank-statements/
│   │   ├── Business Account/
│   │   ├── Personal Account/
│   │   └── ...
│   ├── quarterly-estimates/
│   ├── income/
│   ├── health-insurance/
│   └── other/
│
└── {year} taxes write up/             ← All working files & outputs
    ├── intake.md                      ← Created by initialize command
    ├── extractions/                   ← Per-file subagent outputs
    │   ├── business-{year}-01.md
    │   ├── personal-{year}-01.md
    │   ├── savings-{account}.md
    │   ├── income-summary.md
    │   ├── quarterly-q1.md
    │   └── health-insurance.md
    ├── raw/                           ← Aggregated from extractions
    │   ├── Income {year}.md
    │   ├── Expenses {biz} {year}.md
    │   └── Personal Deductions {year}.md
    ├── final/                         ← Reviewed & finalized versions
    │   └── (copies of raw files after review)
    └── output/                        ← CPA deliverables
        ├── sections/                  ← Per-section JSON (intermediate)
        │   ├── income.json
        │   ├── business_expenses.json
        │   ├── personal_deductions.json
        │   ├── home_office.json
        │   ├── estimated_taxes.json
        │   ├── health_insurance.json
        │   └── retirement.json
        ├── {year}_tax_data.json       ← Structured data (source of truth)
        ├── {year} CPA Tax Package.xlsx ← Spreadsheet with 8 tabs
        └── {year} CPA Summary.md      ← One-page overview
```

## Expense Categories

Standard categories for business expenses:

| Category | Examples |
|----------|----------|
| Software & Subscriptions | SaaS, AI tools, dev tools |
| Education & Courses | Online courses, books, conferences |
| Office Supplies & Equipment | Desk, chair, monitors, supplies |
| Hardware & Technology | Computers, cameras, headphones |
| Professional Services | Consulting, legal, accounting |
| Business Filing & Legal | LLC filing, registered agent |
| Meals & Entertainment | Business meals (note context) |
| Travel | Flights, hotels, rideshare |
| Other | Anything else |

## Spreadsheet Output

The final xlsx has 8 tabs. See [references/output-templates.md](references/output-templates.md) for exact column layouts:

| Tab | Contents |
|-----|----------|
| Summary | Filer info, annual totals, CPA notes |
| Income | Monthly breakdown with SUM total |
| Business Expenses | Recurring + one-time, categorized |
| Personal Deductions | Flagged personal items with notes |
| Home Office | Sq ft calculation, handles mid-year moves |
| Estimated Taxes | Federal + state with confirmation numbers |
| Health Insurance | Provider, premium, coverage dates |
| Retirement | Account type, amount, date |

## Important Rules

- **Interview first** — Never process documents without understanding the user's situation
- **Don't guess** — Flag ambiguous transactions for user or CPA with "ASK CPA:" prefix
- **Preserve originals** — Never modify or move source PDFs
- **Venmo/Zelle** — Note the platform; payee names are often unclear
- **Cents matter** — Use exact amounts, don't round to dollars
- **No tax advice** — This prepares documents; the CPA does the rest
- **Ask before overwriting** — Check before writing to any existing file
- **Uses other skills** — pdf skill for reading statements, xlsx skill for spreadsheet output
