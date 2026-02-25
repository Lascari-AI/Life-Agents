# Tax Prep Agent

Designed for freelancers, sole proprietors, and small LLC owners.

The primary goal is to produce a clean, organized document you can hand directly to your CPA — everything they need to file your taxes, classified and in one place. 

You can also use it for your own reference, but it's built around giving your accountant a single package they can work from alongside any other documents you send them. 

The goal is to reduce back-and-forth between you and your tax advisor, make their job as easy as possible, and help you get the best return you can.

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

Plus a markdown summary document with everything organized at a glance — ready to send to a CPA or use as your own reference when filing.

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

> [!NOTE]
> **Heads up — this takes a while.**
>
> The extract phase reads every page of every bank statement PDF, which can take 30+ minutes depending on how many documents you have.
>
> I personally run it with the `--dangerously-skip-permissions` flag so it can churn through everything in the background without stopping for approval on each file operation:
>
> ```bash
> claude --dangerously-skip-permissions
> ```
>
> This flag bypasses all permission prompts — file reads, writes, shell commands, everything.
>
> **Use at your own risk.** 
> 
> Only run it if you understand what that means and are comfortable with Claude Code operating unsupervised in your directory.

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

- **Not tax advice** — This organizes your documents; a CPA or your own review takes it from there
- **Designed for sole props / LLCs** — Single-member LLC, sole proprietorship, freelancers
- **US-focused** — Federal + state estimated taxes, Schedule C categories
- **PDF quality matters** — Scanned/low-quality PDFs may produce partial extractions

## Disclaimer

**This tool is not tax advice, financial advice, or legal advice.** It is a document preparation assistant only. Lascari AI and its contributors make no guarantees about the accuracy, completeness, or correctness of any output. Transactions may be miscategorized, amounts may be misread from PDFs, and deductions may be missed or incorrectly flagged.

You are solely responsible for reviewing all output before sending it to your CPA or filing anything with the IRS. Lascari AI assumes no responsibility or liability for any errors, omissions, penalties, or damages arising from the use of this tool. Use it entirely at your own risk and always have a qualified tax professional review your documents.
