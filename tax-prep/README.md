# Tax Prep Agent

Walks you through preparing your self-employment tax documents for a CPA. You drop in your bank statements and receipts, then the agent interviews you, extracts every transaction, and produces a CPA-ready spreadsheet.

This is document preparation, not tax filing. The CPA does the rest.

## What You Get

An 8-tab xlsx spreadsheet covering:

| Tab | Contents |
|-----|----------|
| Summary | Filer info, annual totals, CPA notes |
| Income | Monthly breakdown with SUM totals |
| Business Expenses | Recurring + one-time, categorized |
| Personal Deductions | Flagged personal items with notes |
| Home Office | Sq ft calculation, handles mid-year moves |
| Estimated Taxes | Federal + state with confirmation numbers |
| Health Insurance | Provider, premium, coverage dates |
| Retirement | Account type, amount, date |

Plus a markdown summary document with everything your CPA needs at a glance.

## Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code)
- Python 3.10+
- `openpyxl` — `pip install openpyxl`
- [LibreOffice](https://www.libreoffice.org/) (optional, for formula recalculation in the xlsx)
- Claude Code skills: **pdf** and **xlsx** (built-in, available to all Claude Code users)

## Quick Start

```bash
git clone https://github.com/your-username/life-agents.git
cd life-agents/tax-prep
claude
```

Then run:

```
/cpa-tax-prep:initialize 2025
```

## The Workflow

Five commands, run in order:

### 1. `/cpa-tax-prep:initialize [year]`

Creates your tax year folder structure and tells you what documents to gather.

```
/cpa-tax-prep:initialize 2025
```

### 2. Drop your documents

Put your files into the `source-documents/` folder it created:

```
2025 Taxes/
└── source-documents/
    ├── bank-statements/      ← Monthly PDFs per account
    ├── quarterly-estimates/   ← Federal + state receipts
    ├── income/               ← 1099s, income summaries
    ├── health-insurance/     ← Coverage docs, 1095-A
    └── other/                ← Anything else
```

### 3. `/cpa-tax-prep:intake [year]`

Conversational interview about your situation — accounts, home office, special deductions. The agent pre-reads your documents and leads with findings so you confirm rather than recite.

### 4. `/cpa-tax-prep:extract [year]`

Reads all your bank statement PDFs in parallel, extracts every transaction, categorizes expenses, and builds working files. Handles resume if interrupted.

### 5. `/cpa-tax-prep:review [year]`

Walks through the extracted data section by section. You confirm, correct, and resolve any flagged items.

### 6. `/cpa-tax-prep:package [year]`

Generates the final xlsx spreadsheet (8 tabs with formulas) and a CPA summary document. All spreadsheet values are derived deterministically from a structured JSON file.

## Folder Structure After Running

```
2025 Taxes/
├── source-documents/
│   ├── bank-statements/
│   │   ├── Business Account/
│   │   │   ├── January 2025.pdf
│   │   │   └── ...
│   │   └── Personal Account/
│   │       └── ...
│   ├── quarterly-estimates/
│   ├── income/
│   ├── health-insurance/
│   └── other/
│
└── 2025 taxes write up/
    ├── intake.md
    ├── extractions/          ← Per-file subagent outputs
    ├── raw/                  ← Aggregated working files
    ├── final/                ← Reviewed & finalized
    └── output/
        ├── sections/         ← Intermediate JSON
        ├── 2025_tax_data.json
        ├── 2025 CPA Tax Package.xlsx
        └── 2025 CPA Summary.md
```

## Expense Categories

The agent uses 9 standard categories for business expenses:

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

## Tips

- **Organize by account** — Create a subfolder per bank account inside `source-documents/bank-statements/`
- **Name files consistently** — "January 2025.pdf", "February 2025.pdf", etc.
- **One PDF per month** — If your bank provides quarterly PDFs, that works too
- **Include everything** — Better to have extra documents than miss something
- **Resume support** — Every command can pick up where it left off if interrupted

## Limitations

- **Not tax advice** — This prepares documents; your CPA does the rest
- **Designed for sole props / LLCs** — Single-member LLC, sole proprietorship, freelancers
- **US-focused** — Federal + state estimated taxes, Schedule C categories
- **PDF quality matters** — Scanned/low-quality PDFs may produce partial extractions
