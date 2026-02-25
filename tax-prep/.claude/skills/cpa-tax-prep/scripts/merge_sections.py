#!/usr/bin/env python3
"""
Merge per-section JSON files into the monolithic tax data JSON.

Reads 7 section JSONs from a directory, aggregates _cpa_items into
summary.cpa_notes, generates meta block, validates structure, and
outputs the combined JSON that build_xlsx.py expects.

Usage:
    python merge_sections.py --sections-dir DIR --filer-json JSON_STRING \
        --year YEAR --source-files FILE1,FILE2,... --output PATH
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

EXPECTED_SECTIONS = {
    "income": "income.json",
    "business_expenses": "business_expenses.json",
    "personal_deductions": "personal_deductions.json",
    "home_office": "home_office.json",
    "estimated_taxes": "estimated_taxes.json",
    "health_insurance": "health_insurance.json",
    "retirement": "retirement.json",
}


def load_section(sections_dir: Path, filename: str) -> dict:
    """Load a section JSON file and return its parsed contents."""
    path = sections_dir / filename
    if not path.exists():
        raise FileNotFoundError(f"Missing section file: {path}")
    with open(path) as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"{filename}: expected JSON object, got {type(data).__name__}")
    return data


def validate_currency_values(obj, path=""):
    """Recursively check that currency-like fields are numbers, not strings."""
    errors = []
    currency_fields = {
        "amount", "annual_total", "monthly_amount", "monthly_premium",
        "monthly_rent", "monthly_deduction", "subtotal", "office_sqft",
        "home_sqft", "office_pct",
    }
    # monthly_amount is allowed to be a string when amount varied
    string_ok_fields = {"monthly_amount"}

    if isinstance(obj, dict):
        for key, val in obj.items():
            current_path = f"{path}.{key}" if path else key
            if key in currency_fields and isinstance(val, str):
                if key not in string_ok_fields:
                    errors.append(f"{current_path}: expected number, got string '{val}'")
            errors.extend(validate_currency_values(val, current_path))
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            errors.extend(validate_currency_values(item, f"{path}[{i}]"))
    return errors


def merge(sections_dir: Path, filer: dict, year: int,
          source_files: list[str], output: Path) -> dict:
    """Merge all section files into the final JSON structure."""
    all_cpa_items = []
    merged = {}

    # Load each section, extract _cpa_items, store section data
    for section_key, filename in EXPECTED_SECTIONS.items():
        section_data = load_section(sections_dir, filename)

        # Collect and remove _cpa_items
        cpa_items = section_data.pop("_cpa_items", [])
        if isinstance(cpa_items, list):
            all_cpa_items.extend(cpa_items)

        # The section data should have one key matching the section name
        if section_key in section_data:
            merged[section_key] = section_data[section_key]
        else:
            # Fallback: if the file has a single key, use its value
            remaining_keys = [k for k in section_data if not k.startswith("_")]
            if len(remaining_keys) == 1:
                merged[section_key] = section_data[remaining_keys[0]]
            else:
                raise ValueError(
                    f"{filename}: expected key '{section_key}', "
                    f"found keys: {list(section_data.keys())}"
                )

    # Validate currency values across all sections
    validation_errors = validate_currency_values(merged)
    if validation_errors:
        print("WARNING: Currency validation issues:", file=sys.stderr)
        for err in validation_errors:
            print(f"  - {err}", file=sys.stderr)

    # Separate CPA items into questions (ASK CPA) and notes
    cpa_questions = [item for item in all_cpa_items if "ASK CPA" in item.upper()]
    cpa_notes = [item for item in all_cpa_items if "ASK CPA" not in item.upper()]

    # Build the final structure
    result = {
        "meta": {
            "year": year,
            "generated_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "source_files": source_files,
        },
        "summary": {
            "filer": filer,
            "cpa_questions": cpa_questions,
            "cpa_notes": cpa_notes,
        },
        "income": merged["income"],
        "business_expenses": merged["business_expenses"],
        "personal_deductions": merged["personal_deductions"],
        "home_office": merged["home_office"],
        "estimated_taxes": merged["estimated_taxes"],
        "health_insurance": merged["health_insurance"],
        "retirement": merged["retirement"],
    }

    # Write output
    output.parent.mkdir(parents=True, exist_ok=True)
    with open(output, "w") as f:
        json.dump(result, f, indent=2)

    return result


def main():
    parser = argparse.ArgumentParser(description="Merge section JSONs into tax data JSON")
    parser.add_argument("--sections-dir", required=True, help="Directory containing section JSON files")
    parser.add_argument("--filer-json", required=True, help="JSON string with filer info")
    parser.add_argument("--year", required=True, type=int, help="Tax year")
    parser.add_argument("--source-files", required=True, help="Comma-separated list of source files")
    parser.add_argument("--output", required=True, help="Output JSON file path")
    args = parser.parse_args()

    sections_dir = Path(args.sections_dir)
    if not sections_dir.is_dir():
        print(f"ERROR: Sections directory does not exist: {sections_dir}", file=sys.stderr)
        sys.exit(1)

    filer = json.loads(args.filer_json)
    source_files = [f.strip() for f in args.source_files.split(",")]
    output = Path(args.output)

    # Check all section files exist before merging
    missing = []
    for filename in EXPECTED_SECTIONS.values():
        if not (sections_dir / filename).exists():
            missing.append(filename)
    if missing:
        print(f"ERROR: Missing section files: {', '.join(missing)}", file=sys.stderr)
        sys.exit(1)

    result = merge(sections_dir, filer, args.year, source_files, output)

    # Print summary
    summary = {
        "status": "success",
        "output": str(output),
        "sections": list(EXPECTED_SECTIONS.keys()),
        "cpa_questions_count": len(result["summary"]["cpa_questions"]),
        "cpa_notes_count": len(result["summary"]["cpa_notes"]),
        "source_files_count": len(source_files),
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
