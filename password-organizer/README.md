# Password Organizer

Organize a 1Password CSV export into separate vault-specific CSVs. If you've got personal, business, and old client passwords all mixed together, this agent helps you sort them out.

## What It Does

- Interviews you to understand your emails, business, and how you want vaults organized
- Parses your 1Password CSV export
- Auto-categorizes entries using email matching, domain matching, and AI knowledge of what services are
- Flags ambiguous items for you to decide on
- Outputs per-vault CSVs you can import directly into 1Password

## Requirements

- Python 3.10+
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code)

## Quick Start

```bash
cd password-organizer
claude
```

Then run the commands in order:

```
/pw-organize:initialize my-passwords
```

Export your 1Password data as CSV into the `source-files/` folder, then:

```
/pw-organize:intake my-passwords
/pw-organize:categorize my-passwords
/pw-organize:review my-passwords
/pw-organize:export my-passwords
```

## Workflow

### 1. Initialize

Creates the session folder structure. You'll get:
- `source-files/` — drop your 1Password CSV export here
- `working/` — intermediate files (intake notes, categorized data)
- `output/` — final per-vault CSVs

### 2. Intake

Conversational interview. The agent reads your CSV first, then leads with what it found:
- "I found these email addresses: X, Y, Z — which are personal vs. business?"
- You define your vault categories (Personal, Business, Clients, etc.)
- You set any explicit rules ("everything from clientdomain.com goes to Clients")

### 3. Categorize

Two-phase classification:
1. **Deterministic rules** — email matching, domain matching, your explicit rules (catches ~70-80%)
2. **AI knowledge** — knows that Netflix is personal, AWS is business, GitHub could be either (handles the rest)

Ambiguous items are flagged for the next step.

### 4. Review

Walk through results vault by vault:
- Confirm each vault's contents look right
- Resolve flagged items (shared services, ambiguous, unknown)
- Move misplaced entries

### 5. Export

Generates one CSV per vault in `output/`:
- Preserves the exact 1Password CSV format
- Validates no entries were lost or duplicated
- Includes import instructions

## Folder Structure

```
my-passwords/
├── source-files/
│   └── export.csv              ← Your 1Password export
├── working/
│   ├── intake.md               ← Interview notes
│   ├── parsed_entries.json     ← Parsed CSV data
│   ├── categorized.json        ← After classification
│   └── reviewed.json           ← After review
└── output/
    ├── personal.csv            ← Import into Personal vault
    ├── business.csv            ← Import into Business vault
    ├── clients.csv             ← Import into Clients vault
    └── summary.md              ← What went where
```

## Tips

- **Export everything** — better to have too many entries than miss some
- **Multiple exports** — if you have multiple existing vaults, export each one separately; the tool merges them
- **Name your vaults first** — think about what vault categories you want before starting
- **Be honest about clients** — the more client domains you identify, the cleaner the sort

## Limitations

- CSV format only (not `.1pux`)
- Won't modify your 1Password vaults — you import the CSVs manually
- AI classification is best-effort for ambiguous services
- Large exports (5000+ entries) may take longer during the review phase
