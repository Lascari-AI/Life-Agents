# Output Templates

Two deliverables: an xlsx spreadsheet (primary) and a markdown summary.

> **Data source of truth:** The JSON file (`{year}_tax_data.json`) is the canonical data source. See [`tax-data-schema.md`](tax-data-schema.md) for the exact JSON structure. The xlsx is built deterministically from the JSON by `build_xlsx.py` — the templates below describe the *layout* the builder produces. Do not manually construct xlsx files; generate JSON and run the builder.

## Spreadsheet: `{year} CPA Tax Package.xlsx`

Use the **xlsx skill** to create this workbook. Each tab below is a separate sheet.

### Tab: Summary

Row-based key-value layout, not a table. This is the CPA's landing page.

```
Row 1: {YEAR} Tax Preparation — {NAME} / {BUSINESS}
Row 3: FILER INFO
Row 4: Name          | {name}
Row 5: Business      | {business name}
Row 6: Entity        | {LLC, sole prop, etc.}
Row 7: State(s)      | {states}
Row 8: Address       | {address}
Row 9: Address Change| {details if applicable}
Row 11: ANNUAL TOTALS
Row 12: Gross Income           | ${total}
Row 13: Business Expenses      | ${total}
Row 14: Home Office Deduction  | ${total}
Row 15: Health Insurance       | ${total}
Row 16: Est. Taxes (Federal)   | ${total}
Row 17: Est. Taxes (State)     | ${total}
Row 18: Retirement             | ${total}
Row 20: QUESTIONS FOR CPA
Row 21+: {ASK CPA items, one per row}
Row N+1: (blank)
Row N+2: NOTES
Row N+3+: {Informational notes, one per row}
```

### Tab: Income

| Column | Description |
|--------|-------------|
| A: Month | January, February, ... December |
| B: Amount | Monthly income total |
| C: Notes | Source details if relevant |
| Last row | **TOTAL** with SUM formula |

### Tab: Business Expenses

Two sections separated by an empty row.

**Section 1: Monthly Recurring**

| Column | Description |
|--------|-------------|
| A: Vendor | Service/vendor name |
| B: Monthly Amount | Per-charge amount |
| C: Months Charged | "1/15, 2/13, 3/15..." |
| D: Annual Total | Amount x count of charges |
| E: Category | software, storage, internet, etc. |

**Section 2: One-Time / Non-Recurring**

| Column | Description |
|--------|-------------|
| A: Date | Transaction date (M/D format) |
| B: Vendor | Vendor/payee name |
| C: Amount | Transaction amount |
| D: Category | software, education, office supplies, hardware, etc. |
| E: Description | Brief note on what it is |

**Last row**: **TOTAL** summing both sections.

### Tab: Personal Deductions

| Column | Description |
|--------|-------------|
| A: Type | Rent, Utilities, Internet, Health Insurance, Other |
| B: Vendor/Payee | Company or person |
| C: Monthly Amount | If recurring |
| D: Annual Total | Monthly x 12 (or actual count) |
| E: Payment Method | Venmo, Zelle, direct, etc. |
| F: Notes | "potential write-off", "ASK CPA", etc. |

### Tab: Home Office

Row-based layout per location. For mid-year moves, repeat the block.

```
Row 1: HOME OFFICE DEDUCTION — {YEAR}
Row 3: LOCATION 1: {description}
Row 4: Months        | {start} — {end} ({count} months)
Row 5: Office Sq Ft  | {number}
Row 6: Home Sq Ft    | {number}
Row 7: Office %      | {percentage}
Row 8: Monthly Rent  | ${amount}
Row 9: Monthly Deduction | ${amount}
Row 10: Subtotal     | ${amount}
Row 12: (repeat for additional locations)
Row N: TOTAL DEDUCTION | ${combined total}
```

### Tab: Estimated Taxes

| Column | Description |
|--------|-------------|
| A: Authority | IRS or {State Name} |
| B: Quarter | Q1, Q2, Q3, Q4 |
| C: Date Paid | Payment date |
| D: Amount | Payment amount |
| E: Confirmation # | Confirmation number |

Last rows: subtotals per authority, grand total.

### Tab: Health Insurance

| Column | Description |
|--------|-------------|
| A: Provider | Insurance company |
| B: Monthly Premium | Amount |
| C: Start Month | Coverage start |
| D: End Month | Coverage end |
| E: Months | Count |
| F: Annual Total | Premium x months |
| G: Payment Method | How premiums were paid |

### Tab: Retirement

| Column | Description |
|--------|-------------|
| A: Account Type | Roth IRA, SEP IRA, 401(k) |
| B: Institution | Where the account is held |
| C: Amount | Contribution amount |
| D: Date | When contributed |
| E: Tax Year | Tax year the contribution applies to |

---

## Summary Document: `{year} CPA Summary.md`

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
- {other docs}

## Questions for CPA
- {ASK CPA flagged items, one per line}

## Notes
- {Informational notes, one per line}
```
