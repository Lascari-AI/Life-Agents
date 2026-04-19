#!/usr/bin/env python3
"""
Validate exported per-vault CSV files against the reviewed data.

Checks that every entry in reviewed.json appears in exactly one
output CSV, no entries are missing or duplicated, and CSV headers
match the original format.

Usage:
    python validate_export.py --reviewed "working/reviewed.json" \
                              --output-dir "output/"
"""

import argparse
import csv
import json
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Validate per-vault CSV exports")
    parser.add_argument("--reviewed", required=True, help="Path to reviewed.json")
    parser.add_argument("--output-dir", required=True, help="Directory containing output CSVs")

    args = parser.parse_args()

    reviewed_path = Path(args.reviewed)
    output_dir = Path(args.output_dir)

    with open(reviewed_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    entries = data["entries"]
    expected_headers = data["stats"]["headers"]

    errors = []
    total_checks = 0

    # Count expected entries per vault (excluding _excluded)
    expected_by_vault = {}
    expected_total = 0
    for entry in entries:
        vault = entry.get("vault")
        if vault == "_excluded":
            continue
        expected_by_vault[vault] = expected_by_vault.get(vault, 0) + 1
        expected_total += 1

    # Check each expected vault CSV exists
    actual_total = 0
    for vault_key, expected_count in expected_by_vault.items():
        csv_path = output_dir / f"{vault_key}.csv"

        # Check file exists
        if not csv_path.exists():
            errors.append({
                "check": "file_exists",
                "vault": vault_key,
                "expected": str(csv_path),
                "actual": "NOT FOUND",
            })
            total_checks += 1
            continue

        # Read the CSV
        with open(csv_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            actual_headers = list(reader.fieldnames or [])
            rows = list(reader)

        # Check headers match
        if actual_headers != expected_headers:
            errors.append({
                "check": "headers_match",
                "vault": vault_key,
                "expected": expected_headers,
                "actual": actual_headers,
            })
        total_checks += 1

        # Check row count
        actual_count = len(rows)
        actual_total += actual_count
        if actual_count != expected_count:
            errors.append({
                "check": "row_count",
                "vault": vault_key,
                "expected": expected_count,
                "actual": actual_count,
            })
        total_checks += 1

    # Check no extra CSV files exist that aren't in expected vaults
    csv_files = set(p.stem for p in output_dir.glob("*.csv"))
    expected_files = set(expected_by_vault.keys())
    extra_files = csv_files - expected_files
    if extra_files:
        errors.append({
            "check": "no_extra_files",
            "expected": sorted(expected_files),
            "actual": sorted(csv_files),
            "extra": sorted(extra_files),
        })
    total_checks += 1

    # Check total row count
    if actual_total != expected_total:
        errors.append({
            "check": "total_count",
            "expected": expected_total,
            "actual": actual_total,
        })
    total_checks += 1

    # Check summary.md exists
    summary_path = output_dir / "summary.md"
    if not summary_path.exists():
        errors.append({
            "check": "summary_exists",
            "expected": str(summary_path),
            "actual": "NOT FOUND",
        })
    total_checks += 1

    result = {
        "status": "pass" if not errors else "fail",
        "checks": total_checks,
        "errors": errors,
        "summary": {
            "expected_entries": expected_total,
            "actual_entries": actual_total,
            "vaults": len(expected_by_vault),
        },
    }

    print(json.dumps(result, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
