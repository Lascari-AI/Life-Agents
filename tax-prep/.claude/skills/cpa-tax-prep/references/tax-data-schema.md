# Tax Data JSON Schema

This document defines the exact JSON structure for `{year}_tax_data.json`. The LLM generates this file during packaging; deterministic scripts then convert it to xlsx.

## Rules

1. **Currency amounts must be numbers** — `7369.87` not `"$7,369.87"`. Preserve exact cents.
2. **Strings for narrative content** — notes, descriptions, source details, varied monthly amounts.
3. **`monthly_amount` can be a number OR string** — use a string only when the amount varied (e.g., `"$20→$200 (varied)"`).
4. **`annual_total` is always a number** — the builder script decides whether to use a SUM formula or the provided value.
5. **No `null` values** — omit optional fields instead. Use empty arrays `[]` for empty lists.
6. **Dates** — use the format found in source documents (typically `"M/D"` for transactions, `"Month Day, Year"` for tax payments).
7. **All top-level keys are required** — even if a section is empty, include it with empty arrays/objects.

## File Location

```
{year} Taxes/{year} taxes write up/output/{year}_tax_data.json
```

## Schema

```json
{
  "meta": { ... },
  "summary": { ... },
  "income": { ... },
  "business_expenses": { ... },
  "personal_deductions": [ ... ],
  "home_office": { ... },
  "estimated_taxes": { ... },
  "health_insurance": [ ... ],
  "retirement": { ... }
}
```

---

### `meta` (required)

Metadata about the generation.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `year` | integer | yes | Tax year (e.g., `2025`) |
| `generated_at` | string | yes | ISO 8601 timestamp |
| `source_files` | string[] | yes | List of final/ files used |

```json
{
  "year": 2025,
  "generated_at": "2026-02-25T14:30:00",
  "source_files": ["final/Income 2025.md", "final/Expenses Acme LLC 2025.md"]
}
```

---

### `summary` (required)

Filer info and CPA notes. Annual totals are NOT stored here — the builder computes them from other tabs.

#### `summary.filer`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | yes | Filer's full name |
| `business` | string | yes | Business name |
| `entity` | string | yes | Entity type (e.g., "Single-member LLC") |
| `states` | string | yes | State(s) of operation |
| `filing_status` | string | no | Filing status |
| `address` | string | yes | Current address |
| `address_change` | string | no | Details if address changed during the year |
| `phone` | string | no | Phone number |
| `email` | string | no | Email address |

#### `summary.cpa_questions`

Array of strings. Items requiring CPA input or confirmation — those containing "ASK CPA". Aggregated from all finalized files and separated automatically by the merge script.

#### `summary.cpa_notes`

Array of strings. Informational notes and context for the CPA — items that do NOT contain "ASK CPA". Aggregated from all finalized files and separated automatically by the merge script.

```json
{
  "filer": {
    "name": "Jane Smith",
    "business": "Acme LLC",
    "entity": "Single-member LLC",
    "states": "Texas (no state income tax)",
    "filing_status": "Single, no dependents",
    "address": "123 Main St, Austin, TX 78701",
    "address_change": "Moved Sep 1, 2025 from 456 Oak Ave, Unit A, Austin, TX 78702",
    "phone": "512-555-0100",
    "email": "jane@example.com"
  },
  "cpa_questions": [
    "ASK CPA: Can the LLC provide personal training as a company benefit?..."
  ],
  "cpa_notes": [
    "NOTE: Q4 estimated tax ($4,840) paid Jan 7, 2026 — applies to 2025 tax year."
  ]
}
```

---

### `income` (required)

#### `income.monthly`

Array of 12 objects (one per month, January–December).

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `month` | string | yes | Full month name ("January", "February", ...) |
| `amount` | number | yes | Total income for the month |
| `sources` | string | yes | Description of income sources |

#### `income.by_source`

Array of objects — annual totals broken down by income source.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `source` | string | yes | Source name (e.g., "Gusto deposits") |
| `annual_total` | number | yes | Total from this source |

#### `income.interest`

Array of objects — interest income (1099-INT, etc.).

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `source` | string | yes | Source description |
| `amount` | number | yes | Interest amount |

```json
{
  "monthly": [
    {"month": "January", "amount": 7369.87, "sources": "Stripe ($2,888.42 + $241.45), ..."}
  ],
  "by_source": [
    {"source": "Gusto deposits", "annual_total": 114685.00}
  ],
  "interest": [
    {"source": "Amex High-Yield Savings (1099-INT)", "amount": 33.03}
  ]
}
```

---

### `business_expenses` (required)

#### `business_expenses.recurring`

Array of recurring expense objects.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `vendor` | string | yes | Vendor/service name |
| `monthly_amount` | number or string | yes | Per-charge amount. String if varied (e.g., `"$20→$200 (varied)"`) |
| `months_charged` | string | yes | Dates or description (e.g., `"1/23, 2/24, ..."` or `"1/3–12/3 (12 months)"`) |
| `annual_total` | number | yes | Total for the year |
| `category` | string | yes | Expense category |

#### `business_expenses.one_time`

Array of one-time expense objects.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `date` | string | yes | Transaction date (M/D format) |
| `vendor` | string | yes | Vendor name |
| `amount` | number | yes | Transaction amount |
| `category` | string | yes | Expense category |
| `description` | string | no | Brief description |

#### `business_expenses.excluded`

Array of items excluded from expense totals (tax payments, owner draws, etc.).

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `date` | string | yes | Transaction date |
| `payee` | string | yes | Payee name |
| `amount` | number | yes | Amount |
| `notes` | string | yes | Why excluded |

```json
{
  "recurring": [
    {
      "vendor": "Claude.ai (Anthropic)",
      "monthly_amount": "$20→$200 (varied)",
      "months_charged": "1/23, 2/24, 3/24, ...",
      "annual_total": 1586.23,
      "category": "Software & Subscriptions"
    }
  ],
  "one_time": [
    {
      "date": "1/2",
      "vendor": "Lex.page",
      "amount": 18.00,
      "category": "Software & Subscriptions",
      "description": "AI writing tool"
    }
  ],
  "excluded": [
    {
      "date": "1/3",
      "payee": "IRS (USATAXPYMT)",
      "amount": 1760.00,
      "notes": "Prior-year federal tax payment"
    }
  ]
}
```

---

### `personal_deductions` (required)

Array of deduction objects.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | yes | Deduction type (Rent, Utilities, Health Insurance, etc.) |
| `vendor` | string | yes | Vendor/payee |
| `monthly_amount` | number or null | no | Monthly amount if recurring. Omit if not applicable. |
| `annual_total` | number | yes | Annual total |
| `payment_method` | string | yes | How it was paid |
| `notes` | string | no | Additional notes |

```json
[
  {
    "type": "Rent (Jan-Aug)",
    "vendor": "Old house — 456 Oak Ave",
    "monthly_amount": 3350.00,
    "annual_total": 26800.00,
    "payment_method": "Stripe/ZG Rental ACH",
    "notes": "8 months × $3,350"
  }
]
```

---

### `home_office` (required)

#### `home_office.locations`

Array of location objects. One per location; handle mid-year moves with multiple entries.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `description` | string | yes | Full address |
| `months` | string | yes | Coverage period description |
| `months_count` | integer | yes | Number of months |
| `office_sqft` | number | yes | Office square footage |
| `home_sqft` | number | yes | Total home square footage |
| `office_pct` | number | yes | Office percentage (e.g., 8.95 for 8.95%) |
| `monthly_rent` | number | yes | Monthly rent amount |
| `monthly_deduction` | number | yes | Monthly deduction amount |
| `subtotal` | number | yes | Subtotal deduction for this location |

#### `home_office.notes`

Array of strings — notes about the home office calculation.

```json
{
  "locations": [
    {
      "description": "456 Oak Ave, Unit A, Austin, TX 78702",
      "months": "January — August (8 months)",
      "months_count": 8,
      "office_sqft": 115,
      "home_sqft": 1285,
      "office_pct": 8.95,
      "monthly_rent": 3350.00,
      "monthly_deduction": 299.83,
      "subtotal": 2398.60
    }
  ],
  "notes": ["Actual rent at old house was $3,350/mo..."]
}
```

---

### `estimated_taxes` (required)

#### `estimated_taxes.payments`

Array of estimated tax payment objects for the current tax year.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `authority` | string | yes | "IRS" or state name |
| `quarter` | string | yes | "Q1", "Q2", "Q3", or "Q4" |
| `date_paid` | string | yes | Payment date |
| `amount` | number | yes | Payment amount |
| `confirmation` | string | no | Confirmation number |

#### `estimated_taxes.prior_year_payments`

Array of prior-year tax payments made during this calendar year.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `authority` | string | yes | "IRS" or state name |
| `date_paid` | string | yes | Payment date |
| `amount` | number | yes | Payment amount |
| `notes` | string | no | Explanation |

#### `estimated_taxes.notes`

Array of strings — general notes about estimated tax payments.

```json
{
  "payments": [
    {
      "authority": "IRS",
      "quarter": "Q1",
      "date_paid": "April 14, 2025",
      "amount": 3340.00,
      "confirmation": "000000000000000"
    }
  ],
  "prior_year_payments": [
    {
      "authority": "IRS",
      "date_paid": "January 3, 2025",
      "amount": 1760.00,
      "notes": "Likely 2024 Q4 or balance due"
    }
  ],
  "notes": ["Q4 payment dated Jan 7, 2026 applies to tax year 2025"]
}
```

---

### `health_insurance` (required)

Array of health insurance objects.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `provider` | string | yes | Insurance provider |
| `monthly_premium` | number | yes | Monthly premium amount |
| `start_month` | string | yes | Coverage start month |
| `end_month` | string | yes | Coverage end month |
| `months` | integer | yes | Number of months covered |
| `annual_total` | number | yes | Total premiums paid |
| `payment_method` | string | yes | How premiums were paid |
| `notes` | string[] | no | Additional notes (1095-A info, deduction type, etc.) |

```json
[
  {
    "provider": "Blue Cross Blue Shield of TX",
    "monthly_premium": 420.35,
    "start_month": "January",
    "end_month": "December",
    "months": 12,
    "annual_total": 5044.20,
    "payment_method": "ACH Bill Pay (personal acct)",
    "notes": [
      "Form 1095-A provided — policy #171271037",
      "No APTC received — full premium paid out-of-pocket",
      "Deductible as self-employed health insurance (Schedule 1, Form 1040)"
    ]
  }
]
```

---

### `retirement` (required)

#### `retirement.contributions`

Array of retirement contribution objects. May be empty if no contributions were made.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `account_type` | string | yes | "Roth IRA", "SEP IRA", "Solo 401(k)", etc. |
| `institution` | string | yes | Where the account is held |
| `amount` | number | yes | Contribution amount |
| `date` | string | yes | Date of contribution |
| `tax_year` | string | yes | Tax year the contribution applies to |

#### `retirement.notes`

Array of strings.

```json
{
  "contributions": [],
  "notes": [
    "Filer plans to make retirement contributions — type and amount TBD.",
    "ASK CPA: Recommend account type (SEP-IRA, Solo 401k, Roth IRA) and contribution limits."
  ]
}
```
