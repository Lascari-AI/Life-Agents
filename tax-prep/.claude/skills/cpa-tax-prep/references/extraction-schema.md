# Extraction Schema

Per-file output format for subagent extractions. Every file in `extractions/` follows this structure.

## Front Matter

Every extraction file starts with YAML front matter:

```yaml
---
source: "path/to/source-file.pdf"
document_type: business-statement | personal-statement | savings | income-summary | quarterly-estimate | health-insurance
period: "2025-01" | "2025-Q1" | "2025"  # month, quarter, or year as appropriate
status: complete | partial | failed
error: "description of issue"  # only if status is partial or failed
extracted_at: "2025-02-25"
---
```

- `status: complete` — all transactions extracted successfully
- `status: partial` — some data extracted but gaps exist (e.g., unreadable pages)
- `status: failed` — could not extract meaningful data

The orchestrator uses `status` for resume support: files with `status: complete` are skipped on re-run.

## Document Type Schemas

### business-statement

```markdown
---
source: "2025 Taxes/source-documents/bank-statements/Business Account/January 2025.pdf"
document_type: business-statement
period: "2025-01"
status: complete
extracted_at: "2025-02-25"
---

# Business Statement — January 2025

## Income / Deposits

| Date | Description | Amount |
|------|-------------|--------|
| 1/5  | Client ABC — invoice #123 | $5,000.00 |
| 1/20 | Client XYZ — retainer | $3,500.00 |

**Total deposits: $8,500.00**

## Expenses

### Monthly Recurring

| Vendor | Amount | Date | Category |
|--------|--------|------|----------|
| OpenAI | $20.00 | 1/1 | Software & Subscriptions |
| GitHub | $4.00 | 1/4 | Software & Subscriptions |

### One-Time / Non-Recurring

| Date | Vendor | Amount | Category | Description |
|------|--------|--------|----------|-------------|
| 1/12 | Amazon | $149.99 | Hardware & Technology | USB-C hub |
| 1/25 | ? Unclear Charge | $42.50 | Other | Flagged — unrecognized |

## Flagged Items

- **1/25 — ? Unclear Charge — $42.50**: Unrecognized vendor, needs user review
```

### personal-statement

Only flagged transaction types from intake (rent, utilities, internet, etc.).

```markdown
---
source: "2025 Taxes/source-documents/bank-statements/Personal Account/January 2025.pdf"
document_type: personal-statement
period: "2025-01"
status: complete
extracted_at: "2025-02-25"
---

# Personal Statement — January 2025

## Flagged Transactions

| Date | Description | Amount | Type | Payment Method |
|------|-------------|--------|------|----------------|
| 1/1  | Venmo — John Doe | $3,300.00 | Rent | Venmo |
| 1/5  | Venmo — ISP Company | $72.00 | Internet | Venmo |
| 1/15 | Zelle — Electric Co | $85.40 | Utilities | Zelle |

## Notes

- Rent payment confirmed by consistent amount ($3,300) and timing (1st of month)
```

### savings

```markdown
---
source: "2025 Taxes/source-documents/bank-statements/Savings/Amex Savings 2025.pdf"
document_type: savings
period: "2025"
status: complete
extracted_at: "2025-02-25"
---

# Savings — Amex High-Yield 2025

## Interest Earned

| Period | Amount |
|--------|--------|
| Annual total | $1,234.56 |

## Relevant Transfers

| Date | Description | Amount | Direction |
|------|-------------|--------|-----------|
| 6/15 | Transfer to Business | $5,000.00 | Out |
```

### income-summary

```markdown
---
source: "2025 Taxes/source-documents/income/1099-NEC.pdf"
document_type: income-summary
period: "2025"
status: complete
extracted_at: "2025-02-25"
---

# Income Summary — 2025

## 1099-NEC

| Payer | Amount |
|-------|--------|
| Client ABC | $60,000.00 |
| Client XYZ | $42,000.00 |

**Total 1099 income: $102,000.00**
```

### quarterly-estimate

One file per quarter. May aggregate multiple source PDFs.

```markdown
---
source: "2025 Taxes/source-documents/quarterly-estimates/Q1/*.pdf"
document_type: quarterly-estimate
period: "2025-Q1"
status: complete
extracted_at: "2025-02-25"
---

# Quarterly Estimates — Q1 2025

## Payments

| Authority | Date | Amount | Confirmation # |
|-----------|------|--------|----------------|
| IRS | 4/15/2025 | $5,000.00 | 12345678 |
| NY State | 4/15/2025 | $2,500.00 | 87654321 |
```

### health-insurance

```markdown
---
source: "2025 Taxes/source-documents/health-insurance/coverage-summary.pdf"
document_type: health-insurance
period: "2025"
status: complete
extracted_at: "2025-02-25"
---

# Health Insurance — 2025

## Coverage

| Detail | Value |
|--------|-------|
| Provider | Oscar Health |
| Monthly Premium | $450.00 |
| Coverage Start | January 2025 |
| Coverage End | December 2025 |
| Months | 12 |
| Annual Total | $5,400.00 |
| Payment Method | Direct debit |
```

## Aggregation Rules

The orchestrator merges per-file extractions into monolithic raw files:

- **Income raw.md**: Combine all `business-statement` deposit tables + `income-summary` data into monthly totals
- **Expenses raw.md**: Combine all `business-statement` expense tables; deduplicate recurring vendors across months
- **Personal Deductions raw.md**: Combine all `personal-statement` flagged transactions; group by type
- **Estimated Taxes raw.md**: Combine all `quarterly-estimate` files
- **Health Insurance raw.md**: Directly from `health-insurance` extraction
