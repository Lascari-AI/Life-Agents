---
description: Set up a new password organization session — create folder structure and intake template
argument-hint: [session-name]
allowed-tools: Read, Write, Bash, AskUserQuestion, Glob
---

# Password Organizer Initialize

Set up the folder structure for a new password organization session and guide the user on what to prepare.

## Skill Reference

- Skill: `.claude/skills/pw-organize/SKILL.md`

## Variables

```
$1 = session name (e.g., "my-passwords"). If empty, prompt for it.
SESSION_DIR = {$1}
```

## Instructions

### Step 1: Get Session Name

1. If `$1` is empty, ask the user: "What should we call this session?" (suggest something like "passwords-cleanup" or "vault-reorganize")

### Step 2: Run Init Script

```bash
python3 .claude/skills/pw-organize/scripts/init_session.py --session "$1"
```

This creates:
- `{session}/` — Top-level session folder
- `{session}/source-files/` — Drop zone for 1Password CSV export(s)
- `{session}/working/` — Working directory for intermediate files
- `{session}/working/intake.md` — Intake file from template
- `{session}/output/` — Final per-vault CSVs go here

### Step 3: Guide the User

Tell the user:

```
Your session folder is ready. Export your passwords from 1Password as CSV and drop the file(s) into:

  {session}/source-files/

To export from 1Password:
  1. Open 1Password
  2. Go to File → Export (or the vault menu → Export)
  3. Choose CSV format
  4. Save the file into the source-files/ folder above

If you have multiple vaults to consolidate, export each one separately —
the tool will merge them automatically.
```

### Step 4: Show Next Steps

Tell the user:

1. Export your 1Password data as CSV into `source-files/`
2. When the CSV is in place, run `/pw-organize:intake {session}` to start the interview

## Behavior

- If the session folder already exists with an intake.md, report the existing session status instead of creating a new one
- Keep it brief — this is setup, not the interview
- If `source-files/` already has CSVs in it, note that and move to next steps
