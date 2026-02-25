# Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          CPA Tax Prep — Data Flow                           │
└─────────────────────────────────────────────────────────────────────────────┘


  ┌──────────────┐      ┌───────────────┐      ┌──────────────┐      ┌──────────────┐
  │  1. INTAKE   │ ───▶ │  2. EXTRACT   │ ───▶ │  3. REVIEW   │ ───▶ │  4. PACKAGE  │
  │  Interview   │      │  Parallel I/O │      │  Human-in-   │      │  Parallel    │
  │              │      │               │      │  the-loop    │      │  Assembly    │
  └──────┬───────┘      └──────┬────────┘      └──────┬───────┘      └──────┬───────┘
         │                     │                      │                     │
         ▼                     ▼                      ▼                     ▼
    intake.md           extractions/                final/             xlsx + summary
                         + raw/



═══════════════════════════════════════════════════════════════════════════════
  PHASE 0 — INITIALIZE
═══════════════════════════════════════════════════════════════════════════════

  /cpa-tax-prep:initialize 2025

  Creates the folder scaffold and intake template.
  User then drops source documents into the appropriate folders.

  Output:
  ┌─────────────────────────────┐
  │ 2025 Taxes/                 │
  │ ├── source-documents/       │
  │ │   ├── bank-statements/    │
  │ │   ├── quarterly-estimates/│
  │ │   ├── income/             │
  │ │   ├── health-insurance/   │
  │ │   └── other/              │
  │ └── 2025 taxes write up/    │
  │     └── intake.md (blank)   │
  └─────────────────────────────┘



═══════════════════════════════════════════════════════════════════════════════
  PHASE 1 — INTAKE  (Interview)
═══════════════════════════════════════════════════════════════════════════════

  /cpa-tax-prep:intake 2025

  Conversational interview — 9 sections. The agent pre-reads your
  source documents so it can lead with findings and you confirm
  rather than recite from memory.

  ┌──────────────────────────────────────────────────────────┐
  │                    INTAKE AGENT                          │
  │                                                          │
  │   Scans source-documents/ ──▶ Pre-populates questions    │
  │                                                          │
  │   Sections:                                              │
  │   ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────────┐    │
  │   │ Filer   │ │Accounts │ │Home Off.│ │Health Ins.  │    │
  │   │ Info    │ │         │ │         │ │             │    │
  │   └────┬────┘ └────┬────┘ └────┬────┘ └──────┬──────┘    │
  │   ┌────┴────┐ ┌────┴────┐ ┌────┴────┐ ┌──────┴──────┐    │
  │   │Internet/│ │Quarterly│ │Retire-  │ │  Income     │    │
  │   │Utilities│ │ Taxes   │ │ment     │ │             │    │
  │   └────┬────┘ └────┬────┘ └────┬────┘ └──────┬──────┘    │
  │        └──────┬─────┴─────┬────┘              │          │
  │               ▼           ▼                   ▼          │
  │          ┌───────────────────────────────┐               │
  │          │ Special Considerations (9/9)  │               │
  │          └───────────────────────────────┘               │
  │                                                          │
  │   Each section saved immediately on confirmation         │
  │   STATUS markers enable resume if interrupted            │
  └──────────────────────────────────────────────────────────┘
                         │
                         ▼
                    intake.md
              (populated, all sections
               marked STATUS: complete)



═══════════════════════════════════════════════════════════════════════════════
  PHASE 2 — EXTRACT  (Parallel Subagents)
═══════════════════════════════════════════════════════════════════════════════

  /cpa-tax-prep:extract 2025

  One subagent per source document, all running in parallel.
  Each subagent reads intake.md for context — so extractions are
  tailored to your specific accounts, categories, and situation.

  ┌────────────────────────────────────────────────────────────────────┐
  │                      EXTRACTION ORCHESTRATOR                       │
  │                                                                    │
  │  Reads intake.md ──▶ Builds extraction manifest                    │
  │                      (maps each source file to an output file)     │
  │                                                                    │
  │  Spawns subagents in parallel:                                     │
  │                                                                    │
  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                │
  │  │  Subagent 1  │ │  Subagent 2  │ │  Subagent 3  │  ...           │
  │  │              │ │              │ │              │                │
  │  │ Business     │ │ Business     │ │ Personal     │                │
  │  │ Jan 2025.pdf │ │ Feb 2025.pdf │ │ Jan 2025.pdf │                │
  │  │              │ │              │ │              │                │
  │  │  ┌─────────┐ │ │  ┌─────────┐ │ │  ┌─────────┐ │                │
  │  │  │PDF Skill│ │ │  │PDF Skill│ │ │  │PDF Skill│ │                │
  │  │  └─────────┘ │ │  └─────────┘ │ │  └─────────┘ │                │
  │  └──────┬───────┘ └──────┬───────┘ └──────┬───────┘                │
  │         │                │                │                        │
  │         ▼                ▼                ▼                        │
  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                │
  │  │ business-    │ │ business-    │ │ personal-    │                │
  │  │ 2025-01.md   │ │ 2025-02.md   │ │ 2025-01.md   │                │
  │  │              │ │              │ │              │                │
  │  │ status:      │ │ status:      │ │ status:      │                │
  │  │ complete ✓   │ │ complete ✓   │ │ partial ⚠    │                │
  │  └──────────────┘ └──────────────┘ └──────────────┘                │
  │                                                                    │
  │  Each extraction has YAML front matter:                            │
  │    source, document_type, period, status, extracted_at             │
  │                                                                    │
  │  After all subagents return:                                       │
  │  ┌──────────────────────────────────────────────────────┐          │
  │  │              AGGREGATE INTO RAW FILES                │          │
  │  │                                                      │          │
  │  │  extractions/  ──▶  raw/                             │          │
  │  │                     ├── Income 2025.md               │          │
  │  │                     ├── Expenses Business 2025.md    │          │
  │  │                     ├── Personal Deductions 2025.md  │          │
  │  │                     ├── Estimated Taxes 2025.md      │          │
  │  │                     └── Health Insurance 2025.md     │          │
  │  └──────────────────────────────────────────────────────┘          │
  └────────────────────────────────────────────────────────────────────┘



═══════════════════════════════════════════════════════════════════════════════
  PHASE 3 — REVIEW  (Human-in-the-Loop)
═══════════════════════════════════════════════════════════════════════════════

  /cpa-tax-prep:review 2025

  Walks through extracted data section by section.
  Flags items marked with "?" or "ASK CPA:" for your attention.
  Updates documents as you confirm or correct.

  ┌───────────────────────────────────────────────────────────────┐
  │                       REVIEW AGENT                            │
  │                                                               │
  │   raw/ files ──▶ Present section by section                   │
  │                                                               │
  │   ┌──────────┐    ┌──────────┐    ┌──────────┐                │
  │   │ Income   │───▶│ Expenses │───▶│ Personal │───▶ ...        │
  │   │          │    │          │    │Deductions│                │
  │   └────┬─────┘    └────┬─────┘    └────┬─────┘                │
  │        │               │               │                      │
  │        │   User confirms, corrects,    │                      │
  │        │   resolves flagged items      │                      │
  │        │               │               │                      │
  │        ▼               ▼               ▼                      │
  │   ┌──────────────────────────────────────────┐                │
  │   │              final/                      │                │
  │   │  Reviewed copies with all corrections    │                │
  │   │  applied. Ready for packaging.           │                │
  │   └──────────────────────────────────────────┘                │
  └───────────────────────────────────────────────────────────────┘



═══════════════════════════════════════════════════════════════════════════════
  PHASE 4 — PACKAGE  (Parallel Assembly)
═══════════════════════════════════════════════════════════════════════════════

  /cpa-tax-prep:package 2025

  One subagent per section, all running in parallel.
  Each converts a finalized markdown file into a JSON section.
  Then a deterministic pipeline merges, builds, and validates.

  ┌───────────────────────────────────────────────────────────────────┐
  │                     PACKAGE ORCHESTRATOR                          │
  │                                                                   │
  │  Spawns section subagents in parallel:                            │
  │                                                                   │
  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐              │
  │  │ Income   │ │ Business │ │ Personal │ │Home Off. │              │
  │  │ Agent    │ │ Expenses │ │ Deduct.  │ │ Agent    │              │
  │  │          │ │ Agent    │ │ Agent    │ │          │              │
  │  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘              │
  │  ┌────┴─────┐ ┌────┴─────┐                                        │
  │  │Estimated │ │Health Ins│                                        │
  │  │Taxes Agt │ │+ Retire  │                                        │
  │  │          │ │ Agent    │                                        │
  │  └────┬─────┘ └────┬─────┘                                        │
  │       │            │                                              │
  │       ▼            ▼                                              │
  │  ┌──────────────────────────────────────────────────────┐         │
  │  │            output/sections/                          │         │
  │  │  income.json          personal_deductions.json       │         │
  │  │  business_expenses.json   home_office.json           │         │
  │  │  estimated_taxes.json     health_insurance.json      │         │
  │  │                           retirement.json            │         │
  │  └──────────────────────┬───────────────────────────────┘         │
  │                         │                                         │
  │                         ▼                                         │
  │  ┌──────────────────────────────────────────────────────┐         │
  │  │         merge_sections.py                            │         │
  │  │                                                      │         │
  │  │  Merges 7 section JSONs ──▶ 2025_tax_data.json       │         │
  │  │  Collects ASK CPA / NOTE items                       │         │
  │  │  Generates meta block                                │         │
  │  └──────────────────────┬───────────────────────────────┘         │
  │                         │                                         │
  │                         ▼                                         │
  │  ┌──────────────────────────────────────────────────────┐         │
  │  │         build_xlsx.py                                │         │
  │  │                                                      │         │
  │  │  JSON ──▶ 8-tab xlsx with SUM formulas               │         │
  │  │  Deterministic: same JSON always = same xlsx         │         │
  │  │  Uses openpyxl + LibreOffice for formula recalc      │         │
  │  └──────────────────────┬───────────────────────────────┘         │
  │                         │                                         │
  │                         ▼                                         │
  │  ┌──────────────────────────────────────────────────────┐         │
  │  │         validate_xlsx.py                             │         │
  │  │                                                      │         │
  │  │  Checks: cell values match JSON, row counts,         │         │
  │  │  SUM totals, all 8 tabs present                      │         │
  │  └──────────────────────┬───────────────────────────────┘         │
  │                         │                                         │
  │                         ▼                                         │
  │  ┌──────────────────────────────────────────────────────┐         │
  │  │              FINAL OUTPUT                            │         │
  │  │                                                      │         │
  │  │  output/                                             │         │
  │  │  ├── 2025_tax_data.json     (source of truth)        │         │
  │  │  ├── 2025 CPA Tax Package.xlsx  (8-tab spreadsheet)  │         │
  │  │  └── 2025 CPA Summary.md       (one-page overview)   │         │
  │  └──────────────────────────────────────────────────────┘         │
  └───────────────────────────────────────────────────────────────────┘



═══════════════════════════════════════════════════════════════════════════════
  DATA LINEAGE
═══════════════════════════════════════════════════════════════════════════════

  Source PDFs are never modified. Every piece of data can be traced
  back through this chain:

  source-documents/*.pdf
       │
       ▼  (extract subagents, parallel)
  extractions/*.md           ← per-file, with YAML status
       │
       ▼  (aggregation)
  raw/*.md                   ← grouped by category
       │
       ▼  (human review)
  final/*.md                 ← confirmed and corrected
       │
       ▼  (package subagents, parallel)
  output/sections/*.json     ← per-section structured data
       │
       ▼  (merge_sections.py)
  output/{year}_tax_data.json  ← single source of truth
       │
       ├──▶ build_xlsx.py ──▶ {year} CPA Tax Package.xlsx
       └──▶ summary agent ──▶ {year} CPA Summary.md



═══════════════════════════════════════════════════════════════════════════════
  KEY PATTERNS
═══════════════════════════════════════════════════════════════════════════════

  Parallelism       Subagents run concurrently in Extract and Package.
                    Each gets its own context window and intake context.

  Resume Support    STATUS markers on intake sections, YAML status on
                    extractions. Every command picks up where it left off.

  JSON-First        All data converges to JSON before xlsx generation.
                    The spreadsheet is a deterministic projection of JSON.

  Flagging          "?" = uncertain, "ASK CPA:" = needs professional input,
                    "NOTE:" = informational. Surfaced during Review and
                    carried into the final CPA summary.

  No Mutation       Source documents are read-only. Data flows forward
                    through extractions → raw → final → JSON → xlsx.
```
