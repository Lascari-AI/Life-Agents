# Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     Password Organizer — Data Flow                          │
└─────────────────────────────────────────────────────────────────────────────┘


  ┌──────────────┐      ┌───────────────┐      ┌──────────────┐      ┌──────────────┐
  │  1. INTAKE   │ ───▶ │ 2. CATEGORIZE │ ───▶ │  3. REVIEW   │ ───▶ │  4. EXPORT   │
  │  Interview   │      │  Rules + AI   │      │  Human-in-   │      │  Per-vault   │
  │              │      │               │      │  the-loop    │      │  CSVs        │
  └──────┬───────┘      └──────┬────────┘      └──────┬───────┘      └──────┬───────┘
         │                     │                      │                     │
         ▼                     ▼                      ▼                     ▼
    intake.md           categorized.json          reviewed.json       {vault}.csv



═══════════════════════════════════════════════════════════════════════════════
  PHASE 0 — INITIALIZE
═══════════════════════════════════════════════════════════════════════════════

  /pw-organize:initialize my-passwords

  Creates the folder scaffold and intake template.
  User then exports their 1Password data as CSV into source-files/.

  Output:
  ┌─────────────────────────────┐
  │ my-passwords/               │
  │ ├── source-files/           │
  │ │   └── *.csv (user drops)  │
  │ ├── working/                │
  │ │   └── intake.md (blank)   │
  │ └── output/                 │
  └─────────────────────────────┘



═══════════════════════════════════════════════════════════════════════════════
  PHASE 1 — INTAKE  (Interview)
═══════════════════════════════════════════════════════════════════════════════

  /pw-organize:intake my-passwords

  Conversational interview — 6 sections. The agent pre-reads the CSV
  export to discover emails, domains, and service names, then leads
  with findings so the user confirms rather than recites from memory.

  ┌──────────────────────────────────────────────────────────────┐
  │                    INTAKE AGENT                               │
  │                                                               │
  │   Parses CSV(s) ──▶ Finds unique emails, domains, services   │
  │                                                               │
  │   Sections:                                                   │
  │   ┌──────────┐ ┌────────────┐ ┌────────────────┐              │
  │   │ Identity │ │Past Clients│ │Vault Categories│              │
  │   │ (emails) │ │ (domains)  │ │ (user-defined) │              │
  │   └────┬─────┘ └─────┬──────┘ └───────┬────────┘              │
  │   ┌────┴─────────┐ ┌─┴──────────────┐ ┌┴─────────────┐       │
  │   │Categorization│ │    Handling     │ │ Confirmation │       │
  │   │    Rules     │ │  Preferences   │ │              │       │
  │   └──────────────┘ └────────────────┘ └──────────────┘       │
  │                                                               │
  │   Each section saved immediately on confirmation              │
  │   STATUS markers enable resume if interrupted                 │
  └──────────────────────────────────────────────────────────────┘
                         │
                         ▼
                    intake.md
              (populated, all sections
               marked STATUS: complete)



═══════════════════════════════════════════════════════════════════════════════
  PHASE 2 — CATEGORIZE  (Rules + AI)
═══════════════════════════════════════════════════════════════════════════════

  /pw-organize:categorize my-passwords

  Two-phase classification. Deterministic rules first (catches ~70-80%),
  then AI service knowledge for the remainder.

  ┌────────────────────────────────────────────────────────────────────┐
  │                    CATEGORIZATION ENGINE                           │
  │                                                                    │
  │  ┌──────────────────────────────────────────────────────┐          │
  │  │  Phase 1: Deterministic Rules  (apply_rules.py)      │          │
  │  │                                                      │          │
  │  │  Priority order:                                     │          │
  │  │  1. User-defined explicit rules                      │          │
  │  │  2. Email match (username → known email)             │          │
  │  │  3. Domain match (URL → known domain)                │          │
  │  │                                                      │          │
  │  │  Result: ~70-80% classified with high confidence     │          │
  │  └──────────────────────┬───────────────────────────────┘          │
  │                         │                                          │
  │                         ▼ (unmatched entries)                      │
  │                                                                    │
  │  ┌──────────────────────────────────────────────────────┐          │
  │  │  Phase 2: AI Classification  (agent in conversation) │          │
  │  │                                                      │          │
  │  │  For each unmatched entry:                           │          │
  │  │  - What service is this? (Netflix, AWS, etc.)        │          │
  │  │  - Is it personal, business, or ambiguous?           │          │
  │  │  - Assign vault + confidence + flag                  │          │
  │  │                                                      │          │
  │  │  high confidence  → assigned silently                │          │
  │  │  medium confidence → flagged as "ambiguous"          │          │
  │  │  low confidence   → flagged for review               │          │
  │  └──────────────────────┬───────────────────────────────┘          │
  │                         │                                          │
  │                         ▼                                          │
  │                  categorized.json                                  │
  │           (every entry has vault + method +                        │
  │            confidence + flag)                                      │
  └────────────────────────────────────────────────────────────────────┘



═══════════════════════════════════════════════════════════════════════════════
  PHASE 3 — REVIEW  (Human-in-the-Loop)
═══════════════════════════════════════════════════════════════════════════════

  /pw-organize:review my-passwords

  Walks through categorized entries vault by vault.
  Resolves flagged items with user input.

  ┌───────────────────────────────────────────────────────────────┐
  │                       REVIEW AGENT                            │
  │                                                               │
  │   categorized.json ──▶ Present vault by vault                 │
  │                                                               │
  │   ┌──────────┐    ┌──────────┐    ┌──────────┐                │
  │   │ Personal │───▶│ Business │───▶│ Clients  │───▶ ...        │
  │   │ (confirm)│    │ (confirm)│    │ (confirm)│                │
  │   └────┬─────┘    └────┬─────┘    └────┬─────┘                │
  │        │               │               │                      │
  │        └───────┬───────┘               │                      │
  │                ▼                       │                      │
  │   ┌──────────────────────────┐         │                      │
  │   │  Flagged Items           │         │                      │
  │   │  - Shared services       │         │                      │
  │   │  - Ambiguous             │         │                      │
  │   │  - Unknown / No data     │         │                      │
  │   │                          │         │                      │
  │   │  User assigns each one   │         │                      │
  │   └──────────────┬───────────┘         │                      │
  │                  │                     │                      │
  │                  ▼                     ▼                      │
  │   ┌──────────────────────────────────────────┐                │
  │   │              reviewed.json               │                │
  │   │  All flags resolved, vaults finalized    │                │
  │   └──────────────────────────────────────────┘                │
  └───────────────────────────────────────────────────────────────┘



═══════════════════════════════════════════════════════════════════════════════
  PHASE 4 — EXPORT  (Deterministic Output)
═══════════════════════════════════════════════════════════════════════════════

  /pw-organize:export my-passwords

  Deterministic split of reviewed entries into per-vault CSVs.
  Preserves the original 1Password CSV format exactly.

  ┌───────────────────────────────────────────────────────────────────┐
  │                      EXPORT PIPELINE                              │
  │                                                                   │
  │  reviewed.json                                                    │
  │       │                                                           │
  │       ▼  (build_export_csvs.py)                                   │
  │  ┌──────────────────────────────────────────────────────┐         │
  │  │            output/                                   │         │
  │  │  personal.csv        clients.csv                     │         │
  │  │  business.csv        unknown.csv                     │         │
  │  │  summary.md                                          │         │
  │  └──────────────────────┬───────────────────────────────┘         │
  │                         │                                         │
  │                         ▼  (validate_export.py)                   │
  │  ┌──────────────────────────────────────────────────────┐         │
  │  │  Checks:                                             │         │
  │  │  - Every entry in exactly one CSV                    │         │
  │  │  - No missing or duplicate entries                   │         │
  │  │  - Headers match original 1Password format           │         │
  │  │  - Row counts match expected per vault               │         │
  │  └──────────────────────────────────────────────────────┘         │
  └───────────────────────────────────────────────────────────────────┘



═══════════════════════════════════════════════════════════════════════════════
  DATA LINEAGE
═══════════════════════════════════════════════════════════════════════════════

  Source CSVs are never modified. Every piece of data can be traced
  back through this chain:

  source-files/*.csv
       │
       ▼  (parse_csv.py)
  working/parsed_entries.json    ← per-entry, with source file + row tracking
       │
       ▼  (apply_rules.py)
  working/rules_result.json      ← deterministic rule matches
       │
       ▼  (AI classification)
  working/categorized.json       ← all entries classified
       │
       ▼  (human review)
  working/reviewed.json          ← all flags resolved, final assignments
       │
       ▼  (build_export_csvs.py)
  output/{vault-key}.csv         ← per-vault, 1Password-importable
  output/summary.md              ← what went where



═══════════════════════════════════════════════════════════════════════════════
  KEY PATTERNS
═══════════════════════════════════════════════════════════════════════════════

  Two-Phase         Deterministic rules catch the majority, AI handles
  Classification    the rest. Human review resolves true ambiguity.

  Resume Support    STATUS markers on intake sections, file existence
                    checks for categorize/review/export. Every command
                    picks up where it left off.

  CSV Fidelity      original_row dict preserved through the entire
                    pipeline. Output CSVs use the exact same headers
                    and column order as the input. Import-ready.

  Dynamic Vaults    Vault categories are user-defined during intake,
                    never hardcoded. Can be as simple as 2 vaults
                    or as complex as 10+ subcategories.

  No Mutation       Source CSV files are read-only. Data flows forward
                    through parsed → rules → categorized → reviewed → export.

  No Passwords      Password values are preserved in data files but
  in Logs           never displayed in conversation or log output.
```
