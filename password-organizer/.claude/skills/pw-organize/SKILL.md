---
name: pw-organize
description: >
  Organizes a 1Password CSV export into multiple vault-specific CSVs.
  Session-based flow with slash commands for each phase: intake interview,
  auto-categorization, human review, and export. Parses 1Password CSV exports,
  applies deterministic rules (email matching, domain matching) and AI service
  knowledge to categorize each entry into user-defined vault categories,
  then generates per-vault CSV files importable back into 1Password.
  Use when: organizing passwords into vaults, splitting a 1Password export,
  separating personal from business passwords, cleaning up a password manager.
---

# Password Organizer

Organize a 1Password CSV export into separate vault-specific CSVs. Walks through five phases via slash commands, producing importable CSVs for each vault.

This is password organization, not password management.

## Session Lifecycle

```
/pw-organize:initialize ──▶ /pw-organize:intake ──▶ /pw-organize:categorize ──▶ /pw-organize:review ──▶ /pw-organize:export
       (SETUP)                 (INTERVIEW)            (CLASSIFY)                  (CONFIRM)              (OUTPUT)
```

## Commands

| Command | Phase | What It Does |
|---------|-------|--------------|
| `/pw-organize:initialize [session]` | 0. Setup | Creates the session folder, source-files directory, and intake template. |
| `/pw-organize:intake [session]` | 1. Intake | Conversational interview: who you are, your emails, your business, desired vault categories. Saves to `{session}/working/intake.md`. |
| `/pw-organize:categorize [session]` | 2. Categorize | Parses the CSV, applies deterministic rules and AI service knowledge to categorize every entry. Flags ambiguous items. |
| `/pw-organize:review [session]` | 3. Review | Walks through categorized entries vault by vault. Resolves flagged items. Finalizes assignments. |
| `/pw-organize:export [session]` | 4. Export | Generates per-vault CSV files importable into 1Password, plus a summary report. |

## File Structure

```
{session}/
├── source-files/                      ← User drops 1Password CSV export(s) here
│   └── *.csv
│
├── working/                           ← All intermediate files
│   ├── intake.md                      ← Created by initialize command
│   ├── parsed_entries.json            ← Structured parse of CSV(s)
│   ├── rules_result.json             ← After deterministic rule pass
│   ├── categorized.json              ← After AI classification pass
│   └── reviewed.json                 ← After human review
│
└── output/                            ← Final deliverables
    ├── {vault-key}.csv               ← One CSV per vault category
    └── summary.md                    ← Report of what went where
```

## Important Rules

- **Interview first** — Never categorize without understanding the user's emails, business, and vault preferences
- **Preserve all fields** — Output CSVs must contain every column from the original export, in the same order
- **Don't guess on ambiguous items** — Flag them for user review
- **No passwords in logs** — Never print or display password values during processing
- **Source files are read-only** — Never modify the original CSV exports
- **Ask before overwriting** — Check before writing to any existing file
- **Dynamic vaults** — Vault categories are defined by the user during intake, never hardcoded
