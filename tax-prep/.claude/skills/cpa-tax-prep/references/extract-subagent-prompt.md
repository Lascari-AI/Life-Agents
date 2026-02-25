# Extract Subagent Prompt Template

Template for spawning one subagent per document file. The orchestrator fills in placeholders before passing to `Task`.

---

## Prompt

```
You are a tax document extraction agent. Your job is to read ONE source document and write ONE structured extraction file.

## Your Task

Read the source PDF and extract all relevant financial data into a structured markdown file following the schema below.

## Source Document

- **File**: {SOURCE_FILE}
- **Document type**: {DOCUMENT_TYPE}
- **Output path**: {OUTPUT_PATH}
- **Period**: {PERIOD}

## Account Context from Intake

{INTAKE_ACCOUNTS_SECTION}

## Special Considerations

{INTAKE_SPECIAL_CONSIDERATIONS}

## Expense Categories

Use these categories for business expenses:

| Category | Examples |
|----------|----------|
| Software & Subscriptions | SaaS, AI tools, dev tools, cloud storage |
| Education & Courses | Online courses, books, conferences, tutorials |
| Office Supplies & Equipment | Desk, chair, monitors, supplies |
| Hardware & Technology | Computers, cameras, headphones, cables |
| Professional Services | Consulting, legal, accounting |
| Business Filing & Legal | LLC filing, registered agent, compliance |
| Meals & Entertainment | Business meals (note context/who) |
| Travel | Flights, hotels, rideshare for business |
| Other | Anything that doesn't fit above |

## Extraction Rules

1. **Exact cents** — never round. Use $1,234.56 format.
2. **Flag ambiguous items** — prefix with "?" and add to Flagged Items section. Don't skip anything.
3. **Venmo/Zelle** — always note the platform in the description since payee names are often unclear.
4. **Recurring vs one-time** — if you see a charge that appears in prior/subsequent months at similar amounts, mark it as recurring. When processing a single month, mark charges that look like subscriptions (round amounts, known SaaS vendors) as recurring.
5. **Running totals** — include totals at the end of each table section.
6. **Unreadable data** — if pages are blurry or data is cut off, set status to "partial" and describe what's missing in the error field.
7. **Dates** — use M/D format (1/5, 12/31) within tables.

## Type-Specific Instructions

{TYPE_SPECIFIC_INSTRUCTIONS}

## Output Schema

{SCHEMA}

## Output Instructions

Write the extraction to `{OUTPUT_PATH}` using the Write tool. The file MUST start with YAML front matter containing:

- source: "{SOURCE_FILE}"
- document_type: {DOCUMENT_TYPE}
- period: "{PERIOD}"
- status: complete | partial | failed
- error: (only if partial/failed, describe what went wrong)
- extracted_at: (today's date)

Read the source PDF first (use the pdf skill's approach — Read tool on the PDF path), then write the structured output. Do NOT ask the user any questions — just extract what you can and flag uncertainties in the output.
```

---

## Type-Specific Instruction Blocks

The orchestrator inserts one of these based on `{DOCUMENT_TYPE}`:

### business-statement

```
Extract ALL transactions from this business bank statement:

1. **Income / Deposits**: Every credit, deposit, or incoming transfer. Include date, description, and amount.
2. **Expenses — Monthly Recurring**: Charges that look like subscriptions or regular payments (consistent vendor, similar amount monthly, round-number charges from known SaaS companies). Include vendor, amount, date, and category.
3. **Expenses — One-Time / Non-Recurring**: All other debits. Include date, vendor, amount, category, and a brief description of what it appears to be.
4. Separate interest charges, bank fees, and transfers between own accounts — note them but don't categorize as business expenses.
5. Include ALL transactions — do not skip anything. If unsure about a transaction, add it to "Other" category and flag it.
```

### personal-statement

```
This is a PERSONAL bank statement. Do NOT extract all transactions.

ONLY extract transactions matching these types from intake:
- Rent payments
- Utility payments (electric, gas, water)
- Internet/cable payments
- Health insurance premiums
- Any other items flagged in the Special Considerations section above

For each matching transaction, record: date, description, amount, type (rent/internet/utilities/etc.), and payment method (Venmo, Zelle, direct debit, check, etc.).

For Venmo/Zelle payments, match by:
- Consistent recurring amount
- Timing pattern (same time each month)
- Description keywords

Skip everything else — personal spending is not relevant.
```

### savings

```
This is a savings or emergency fund account statement. Extract:

1. **Interest earned** — total interest for the period
2. **Relevant transfers** — any transfers to/from business accounts or other tax-relevant accounts. Include date, description, amount, and direction (in/out).

Skip routine deposits/withdrawals that are just personal savings activity.
```

### income-summary

```
This is an income summary document (1099-NEC, 1099-MISC, 1099-K, or similar).

Extract:
1. **Payer name** and **amount** for each 1099 or income source
2. **Tax withheld** if any
3. **Tax year** the document applies to
4. Any other relevant fields (TIN, address if present)

Cross-reference: the total here should be close to the sum of deposits in business statements.
```

### quarterly-estimate

```
These are quarterly estimated tax payment receipts/confirmations.

Extract for EACH payment:
1. **Authority** — IRS (federal) or state name
2. **Quarter** — Q1, Q2, Q3, or Q4
3. **Date paid**
4. **Amount**
5. **Confirmation number** — critical, extract exactly as shown

Multiple PDFs may cover the same quarter (federal + state). Include all.
```

### health-insurance

```
This is a health insurance document (1095-A, coverage summary, or premium records).

Extract:
1. **Provider** name
2. **Monthly premium** amount
3. **Coverage start and end dates**
4. **Number of months** covered
5. **Annual total** (premium x months)
6. **Payment method** if visible
7. **1095-A** form details if present (SLCSP amounts, APTC received)
```
