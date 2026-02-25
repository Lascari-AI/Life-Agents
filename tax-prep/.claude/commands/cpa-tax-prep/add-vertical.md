---
description: Add a new document type and/or packaging section to the tax-prep system
argument-hint: [vertical-name]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
---

# Add Vertical

Add a new extraction document type and/or packaging section (spreadsheet tab) to the tax-prep system. Conducts an interview to gather requirements, then edits all touchpoint files in a single pass.

## Skill Reference

All files that may need modification:

- Extraction schema: `.claude/skills/cpa-tax-prep/references/extraction-schema.md`
- Extract type instructions: `.claude/skills/cpa-tax-prep/references/extract-type-instructions.md`
- JSON schema: `.claude/skills/cpa-tax-prep/references/tax-data-schema.md`
- Output templates: `.claude/skills/cpa-tax-prep/references/output-templates.md`
- Package type instructions: `.claude/skills/cpa-tax-prep/references/package-type-instructions.md`
- CPA checklist: `.claude/skills/cpa-tax-prep/references/cpa-checklist.md`
- Intake template: `.claude/skills/cpa-tax-prep/references/intake-template.md`
- Merge script: `.claude/skills/cpa-tax-prep/scripts/merge_sections.py`
- Build script: `.claude/skills/cpa-tax-prep/scripts/build_xlsx.py`
- Validate script: `.claude/skills/cpa-tax-prep/scripts/validate_xlsx.py`
- Init session: `.claude/skills/cpa-tax-prep/scripts/init-session.py`
- Extract command: `.claude/commands/cpa-tax-prep/extract.md`
- Package command: `.claude/commands/cpa-tax-prep/package.md`
- Skill doc: `.claude/skills/cpa-tax-prep/SKILL.md`
- Architecture: `ARCHITECTURE.md`

## Variables

```
$1 = vertical name in kebab-case (e.g., "vehicle-mileage"). If empty, ask during interview.
SNAKE = kebab-case converted to snake_case (e.g., "vehicle_mileage")
TITLE = kebab-case converted to Title Case (e.g., "Vehicle Mileage")
```

## Instructions

### Step 1: Load Current State

Read these files to determine current counts and existing names:

1. Read `.claude/skills/cpa-tax-prep/references/extraction-schema.md` — note the `document_type` enum values on the front matter line
2. Read `.claude/skills/cpa-tax-prep/references/tax-data-schema.md` — note all top-level JSON keys in the Schema section
3. Read `.claude/skills/cpa-tax-prep/scripts/merge_sections.py` — note the `EXPECTED_SECTIONS` dict keys
4. Read `.claude/skills/cpa-tax-prep/scripts/validate_xlsx.py` — note the `expected_tabs` list
5. Read `.claude/skills/cpa-tax-prep/scripts/build_xlsx.py` — note the `totals_labels` list and `"tabs"` count
6. Read `.claude/skills/cpa-tax-prep/references/intake-template.md` — note the "Sections Completed: 0/N" count
7. Read `.claude/skills/cpa-tax-prep/SKILL.md` — note the tab count mentioned in the commands table and spreadsheet table

Store these as reference values for collision checking and count incrementing.

### Step 2: Scope

If `$1` was not provided, ask for the vertical name (kebab-case, e.g., `vehicle-mileage`).

Then ask via AskUserQuestion:

**Question 1**: What are you adding?
- Extraction type only (new document type that feeds into an existing packaging section)
- Packaging section only (new spreadsheet tab from already-extracted data)
- Both (new document type AND new spreadsheet tab)

**Question 2**: Confirm the names that will be used:
- Document type (kebab-case): `{$1}` (e.g., `vehicle-mileage`)
- Section key (snake_case): `{SNAKE}` (e.g., `vehicle_mileage`)
- Tab name (Title Case): `{TITLE}` (e.g., `Vehicle Mileage`)

Check for naming conflicts:
- Compare document type against the `document_type` enum values from Step 1
- Compare section key against `EXPECTED_SECTIONS` keys from Step 1
- Compare tab name against `expected_tabs` from Step 1

If any conflict, tell the user and ask for a different name.

### Step 3: Extraction Details (if adding extraction type)

Skip this step if scope is "Packaging section only".

Ask via AskUserQuestion:

1. **Source documents**: What kind of documents will be extracted? (e.g., "Vehicle mileage logs in PDF format", "Charitable donation receipts")
2. **Data fields**: What fields should be extracted from each document? List column names and types. (e.g., "date: string, destination: string, miles: number, purpose: string")
3. **Periodicity**: How many extraction files per year?
   - One per year (like health-insurance, income-summary)
   - One per month (like business-statement, personal-statement)
   - One per quarter (like quarterly-estimate)
   - One per document (like savings)
4. **Output filename pattern**: Based on periodicity, derive the pattern:
   - Per year: `{kebab-name}.md`
   - Per month: `{kebab-name}-{year}-{MM}.md`
   - Per quarter: `{kebab-name}-q{N}.md`
   - Per document: `{kebab-name}-{identifier}.md`
5. **Aggregation target**: Should the raw data:
   - Feed into a NEW raw file (e.g., `Vehicle Mileage {year}.md`)
   - Fold into an existing raw file (ask which one)

From the answers, compose two blocks:
- **Extraction schema block**: A `### {document-type}` section for `extraction-schema.md` following the pattern of existing blocks (YAML front matter example + markdown body with table layout)
- **Extraction instruction block**: A `## {document-type}` section for `extract-type-instructions.md` following the pattern of existing blocks

Present both blocks to the user for confirmation before proceeding.

### Step 4: Packaging Details (if adding packaging section)

Skip this step if scope is "Extraction type only".

Ask via AskUserQuestion:

1. **JSON structure**: What shape should the section's JSON take? Show existing patterns:
   - Object with named arrays (like `income` with `.monthly`, `.by_source`, `.interest`)
   - Object with array + notes (like `estimated_taxes` with `.payments`, `.notes`)
   - Top-level array (like `personal_deductions` or `health_insurance`)
   - Simple object (like `home_office` with `.locations` and `.notes`)
2. **Field definitions**: For each array/object, what fields? Include name, type (string/number/integer), and whether required.
3. **Summary total**: Should this section's total appear on the Summary tab?
   - Yes — provide the label (e.g., "Vehicle Mileage Deduction")
   - No

From the answers, compose two blocks:
- **JSON schema block**: A `### {snake_case}` section for `tax-data-schema.md` following the pattern of existing sections (field table + example JSON)
- **Package instruction block**: A `## {snake_case}` section for `package-type-instructions.md` following the pattern of existing blocks

Present both blocks to the user for confirmation before proceeding.

### Step 5: Spreadsheet Tab (if adding packaging section)

Skip this step if scope is "Extraction type only".

Ask via AskUserQuestion:

1. **Tab name**: Confirm Title Case name (e.g., "Vehicle Mileage")
2. **Column headers**: List columns with types. Example:
   - A: Date (text)
   - B: Destination (text)
   - C: Miles (number)
   - D: Purpose (text)
3. **Sub-sections**: Does the tab have sub-sections? (like Business Expenses has Recurring + One-Time)
   - If yes, what are they?
4. **Total row**: Should the tab have a SUM formula total row?
   - If yes, which column(s) get totals?

From the answers, compose three blocks:
- **Output template block**: A `### Tab: {Title}` section for `output-templates.md`
- **`build_{snake}_tab(wb, data)` function**: A Python function for `build_xlsx.py` following the pattern of existing builder functions. Must return a dict — if the tab has a total that appears on Summary, return `{"total_cell": f"{col}{total_row}"}`, otherwise return `{}`
- **`validate_{snake}(wb, data, errors)` function**: A Python function for `validate_xlsx.py` following the pattern of existing validators

Present all three blocks to the user for confirmation before proceeding.

### Step 6: Intake & Checklist

Ask via AskUserQuestion:

1. **Intake section**: Should a new section be added to the intake interview template?
   - If yes: What questions should the section ask? (e.g., "Do you have vehicle mileage records? Business vs personal use?")
   - If no: skip
2. **Checklist items**: What items should be added to the CPA checklist? (e.g., "Vehicle mileage log", "Vehicle registration")
   - Which existing checklist category do they belong in? Or a new category?
3. **Source documents subfolder**: Should `init-session.py` create a new subfolder under `source-documents/`?
   - If yes: what name? (e.g., `vehicle-records`)
   - If no: skip

### Step 7: Confirmation

Present a complete summary of every file to be created or modified:

```markdown
## Add Vertical: {TITLE}

### Scope
- Extraction type: {yes/no} — `{document-type}`
- Packaging section: {yes/no} — `{snake_case}`
- Spreadsheet tab: {yes/no} — "{Title Case}"

### Files to Modify

#### Reference Files (appends)
- `references/extraction-schema.md` — Append `### {document-type}` schema block
- `references/extract-type-instructions.md` — Append `## {document-type}` instruction block
- `references/tax-data-schema.md` — Append `### {snake_case}` JSON schema section
- `references/output-templates.md` — Append `### Tab: {Title}` layout
- `references/package-type-instructions.md` — Append `## {snake_case}` instruction block
- `references/cpa-checklist.md` — Add {N} checklist items
- `references/intake-template.md` — Add new section, update 0/N counter {if applicable}

#### Python Scripts (surgical edits)
- `scripts/merge_sections.py` — Add to `EXPECTED_SECTIONS` dict + `result` dict
- `scripts/build_xlsx.py` — New `build_{snake}_tab()` function + edit `totals_labels`, `main()`, `wire_summary_formulas()`, totals computation, tab count
- `scripts/validate_xlsx.py` — New `validate_{snake}()` function + edit `expected_tabs`, `main()` dispatch
- `scripts/init-session.py` — Add "{subfolder}" to `subdirs` list {if applicable}

#### Command Files (edit existing steps)
- `commands/cpa-tax-prep/extract.md` — Add to document type list (Step 4) + aggregation rules (Step 7)
- `commands/cpa-tax-prep/package.md` — Add to section manifest (Step 2) + expected file count (Step 4)

#### Documentation
- `skills/cpa-tax-prep/SKILL.md` — Update tab count, add tab to spreadsheet table, update file structure
- `ARCHITECTURE.md` — Update section references
```

Wait for the user to approve before proceeding. If they want changes, loop back to the relevant step.

### Step 8: Execute All Edits

Make all edits in this order. For each file, read it first, then apply the edit.

#### 8a. Reference files (appends — no dependencies)

1. **`extraction-schema.md`** (if adding extraction type):
   - Append the new document type schema block (from Step 3) before the `## Aggregation Rules` section
   - Add the new document type to the `document_type` enum on the front matter line
   - Add a new aggregation rule bullet under `## Aggregation Rules`

2. **`extract-type-instructions.md`** (if adding extraction type):
   - Append the new `## {document-type}` instruction block at the end of the file

3. **`tax-data-schema.md`** (if adding packaging section):
   - Add the new key to the top-level schema overview (the `{ "meta": ..., "summary": ..., ... }` block)
   - Append the new `### {snake_case}` schema section before the file ends

4. **`output-templates.md`** (if adding packaging section):
   - Append the new `### Tab: {Title}` layout block after the last tab section, before the `---` separator above `## Summary Document`
   - If the section has a Summary total, add a new row to the Summary tab's ANNUAL TOTALS section

5. **`package-type-instructions.md`** (if adding packaging section):
   - Append the new `## {snake_case}` instruction block at the end of the file

6. **`cpa-checklist.md`**:
   - Add checklist items under the appropriate category section, or add a new category section

7. **`intake-template.md`** (if adding intake section):
   - Insert a new `## {Section Name}` with `<!-- STATUS: pending -->` marker and `_Not yet discussed._` placeholder — add before the `## Documents Provided` section
   - Update the `Sections Completed: 0/N` counter to `0/{N+1}`
   - Add a new checkbox to the `## Documents Provided` list

#### 8b. Python scripts (surgical edits)

8. **`merge_sections.py`**:
   - Add entry to `EXPECTED_SECTIONS` dict: `"{snake}": "{snake}.json",`
   - Add entry to `result` dict in the `merge()` function: `"{snake}": merged["{snake}"],`
   - If the new section has currency fields not already in `currency_fields`, add them

9. **`build_xlsx.py`**:
   - Write the new `build_{snake}_tab(wb, data)` function — insert it before the `# ── Cross-sheet formula wiring` comment
   - If the section has a Summary total:
     - Add the label to `totals_labels` list in `build_summary_tab()`
     - Add `{snake}_info` parameter to `wire_summary_formulas()` signature
     - Add `elif label == "{Summary Label}" and {snake}_info.get("total_cell"):` branch in `wire_summary_formulas()`
     - Add `{snake}_info = build_{snake}_tab(wb, data)` call in `main()` (before wire_summary_formulas)
     - Pass `{snake}_info` to the `wire_summary_formulas()` call in `main()`
     - Add `{snake}_total = sum(...)` computation in `main()`
     - Add `"{snake}": {snake}_total` to the `"totals"` dict in `main()`
   - If no Summary total:
     - Add `build_{snake}_tab(wb, data)` call in `main()` (no info capture needed)
   - Increment the `"tabs": N` count in `main()`

10. **`validate_xlsx.py`**:
    - Write the new `validate_{snake}(wb, data, errors)` function — insert it before `validate_tab_existence()`
    - Add `"{Title}"` to the `expected_tabs` list in `validate_tab_existence()`
    - Add dispatch block in `main()`: `if "{Title}" in wb.sheetnames: total_checks += validate_{snake}(wb, data, errors)`

11. **`init-session.py`** (if adding source documents subfolder):
    - Add `"{subfolder-name}"` to the `subdirs` list

#### 8c. Command files

12. **`extract.md`** (if adding extraction type):
    - In Step 4 (Build Manifest), add the new document type to the list: `N. Determine the **document type**: ... `{document-type}``
    - Add the output filename pattern for the new type
    - In Step 7 (Aggregate into Raw Files), add a bullet for the new raw file

13. **`package.md`** (if adding packaging section):
    - In Step 2 (Build Section Manifest), add a new row to the subagent table
    - In Step 4 (Verify Section JSONs), add the new filename to the expected files list
    - Update the subagent count in Step 3 and file count in Step 4 if they are mentioned numerically

#### 8d. Documentation

14. **`SKILL.md`**:
    - Update the tab count in the `/cpa-tax-prep:package` row of the Commands table (e.g., "8 tabs" → "9 tabs")
    - Add a new row to the Spreadsheet Output table
    - If adding a new extraction type, add the extraction output to the File Structure tree
    - If adding a new source documents subfolder, add it to the File Structure tree
    - If adding a new section JSON, add it to the File Structure tree under `output/sections/`

15. **`ARCHITECTURE.md`**:
    - If adding a new section JSON, add it to the `output/sections/` listing in the Phase 4 diagram
    - Update any references to section/tab counts (e.g., "7 section JSONs", "8-tab xlsx")

### Step 9: Verification

After all edits are complete, run these checks:

1. **Python syntax check** — verify all modified Python scripts parse cleanly:
   ```bash
   python3 -c "import ast; ast.parse(open('.claude/skills/cpa-tax-prep/scripts/merge_sections.py').read())"
   python3 -c "import ast; ast.parse(open('.claude/skills/cpa-tax-prep/scripts/build_xlsx.py').read())"
   python3 -c "import ast; ast.parse(open('.claude/skills/cpa-tax-prep/scripts/validate_xlsx.py').read())"
   python3 -c "import ast; ast.parse(open('.claude/skills/cpa-tax-prep/scripts/init-session.py').read())"
   ```

2. **Cross-file consistency checks** (use Grep):
   - Verify `{SNAKE}` appears in `merge_sections.py` EXPECTED_SECTIONS
   - Verify `{TITLE}` appears in `validate_xlsx.py` expected_tabs
   - Verify `build_{SNAKE}_tab` function exists in `build_xlsx.py`
   - Verify `validate_{SNAKE}` function exists in `validate_xlsx.py`
   - If extraction type was added: verify `{document-type}` appears in `extraction-schema.md` front matter enum and in `extract-type-instructions.md`

3. **Count consistency**:
   - Count the actual number of tabs in `validate_xlsx.py` `expected_tabs` list
   - Confirm the `"tabs"` number in `build_xlsx.py` matches
   - Confirm the tab count in `SKILL.md` matches
   - If intake section was added: count `<!-- STATUS: pending -->` markers in `intake-template.md` and confirm `0/N` matches

4. **Present final report**:

```markdown
## Vertical Added: {TITLE}

### Files Modified ({count})
- {list each file with a one-line summary of what changed}

### Verification
- [ ] merge_sections.py — syntax OK, {SNAKE} in EXPECTED_SECTIONS
- [ ] build_xlsx.py — syntax OK, build_{SNAKE}_tab() exists, tabs = {N}
- [ ] validate_xlsx.py — syntax OK, validate_{SNAKE}() exists, {TITLE} in expected_tabs
- [ ] init-session.py — syntax OK {if modified}
- [ ] Tab count consistent: {N} across build_xlsx.py, validate_xlsx.py, SKILL.md
- [ ] Intake section count: {M} {if applicable}

### Next Steps
- Run `/cpa-tax-prep:extract` and `/cpa-tax-prep:package` on a test year to verify end-to-end
- If intake section was added, run `/cpa-tax-prep:intake` to test the new interview section
```

## Edge Cases

- **Extraction-only** (new doc type feeding existing section): Skip Steps 4, 5, and all packaging/xlsx edits in Step 8. Only modify extraction-schema.md, extract-type-instructions.md, extract.md, cpa-checklist.md, and optionally intake-template.md + init-session.py.
- **Section-only** (new tab from already-extracted data): Skip Step 3 and all extraction edits in Step 8. Only modify tax-data-schema.md, output-templates.md, package-type-instructions.md, build_xlsx.py, validate_xlsx.py, merge_sections.py, package.md, SKILL.md, ARCHITECTURE.md, and optionally cpa-checklist.md.
- **Naming conflicts**: Detected in Step 2 — loop until a unique name is chosen.
- **Tab count**: Read dynamically from `expected_tabs` in Step 1 — never assume a specific count.
- **Intake section count**: Read the `0/N` counter from `intake-template.md` in Step 1 — increment N by 1 if adding a section.
- **Bundled sections**: If the new vertical produces multiple JSON files (like `estimated_taxes_and_retirement`), handle the one-to-many pattern: one subagent, multiple output files, multiple entries in EXPECTED_SECTIONS.

## Behavior

- Read every file before editing it — never edit blind
- Present generated code blocks to the user for review before writing them
- If any Python syntax check fails, fix the issue immediately and re-verify
- Do not modify files outside the `tax-prep/` directory tree
- Keep the same formatting conventions as existing content in each file (indentation, heading levels, blank lines)
