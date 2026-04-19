#!/usr/bin/env python3
"""
Build per-vault CSV files from reviewed password entries.

Reads the reviewed JSON and produces one CSV per vault category,
preserving the original 1Password CSV format exactly.

Usage:
    python build_export_csvs.py --reviewed "working/reviewed.json" \
                                --output-dir "output/"
"""

import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Build per-vault CSV exports")
    parser.add_argument("--reviewed", required=True, help="Path to reviewed.json")
    parser.add_argument("--output-dir", required=True, help="Output directory for CSVs")

    args = parser.parse_args()

    reviewed_path = Path(args.reviewed)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(reviewed_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    entries = data["entries"]
    headers = data["stats"]["headers"]
    vault_categories = {vc["key"]: vc for vc in data.get("vault_categories", [])}

    # Group entries by vault
    vaults = {}
    excluded = []

    for entry in entries:
        vault = entry.get("vault")
        if vault == "_excluded":
            excluded.append(entry)
            continue
        if vault not in vaults:
            vaults[vault] = []
        vaults[vault].append(entry)

    # Write one CSV per vault
    files_written = []
    total_rows = 0

    for vault_key, vault_entries in sorted(vaults.items()):
        csv_path = output_dir / f"{vault_key}.csv"

        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers, extrasaction="ignore")
            writer.writeheader()

            for entry in vault_entries:
                writer.writerow(entry["original_row"])

        count = len(vault_entries)
        total_rows += count
        display_name = vault_categories.get(vault_key, {}).get("display_name", vault_key)
        files_written.append({
            "file": csv_path.name,
            "vault_key": vault_key,
            "display_name": display_name,
            "entries": count,
        })
        print(f"Written: {csv_path.name} ({count} entries)")

    # Write summary report
    summary_path = output_dir / "summary.md"
    today = datetime.now().strftime("%Y-%m-%d %H:%M")

    summary_lines = [
        "# Password Organization Summary",
        "",
        f"> **Generated**: {today}",
        f"> **Total Entries**: {total_rows}",
        f"> **Vaults**: {len(files_written)}",
        "",
        "## Per-Vault Breakdown",
        "",
        "| File | Vault | Entries |",
        "|------|-------|---------|",
    ]

    method_counts = {}
    for entry in entries:
        m = entry.get("method", "unknown")
        method_counts[m] = method_counts.get(m, 0) + 1

    for fw in files_written:
        summary_lines.append(f"| {fw['file']} | {fw['display_name']} | {fw['entries']} |")

    summary_lines.extend([
        "",
        "## Classification Methods",
        "",
        "| Method | Count |",
        "|--------|-------|",
    ])
    for method, count in sorted(method_counts.items()):
        summary_lines.append(f"| {method} | {count} |")

    if excluded:
        summary_lines.extend([
            "",
            f"## Excluded Entries: {len(excluded)}",
            "",
        ])
        for entry in excluded:
            title = entry.get("original_row", {}).get("Title", "Unknown")
            summary_lines.append(f"- {title}")

    summary_lines.extend([
        "",
        "## How to Import into 1Password",
        "",
        "1. Open 1Password",
        "2. Create a vault for each category (if not already existing)",
        "3. For each CSV file above:",
        "   - Go to **File → Import**",
        "   - Select **CSV** as the format",
        "   - Choose the CSV file",
        "   - Select the target vault",
        "4. Verify the imported entries look correct",
        "",
    ])

    summary_path.write_text("\n".join(summary_lines))
    print(f"\nSummary: {summary_path}")

    # Print result for validation
    result = {
        "files": files_written,
        "total_rows": total_rows,
        "excluded": len(excluded),
    }
    print(f"\nResult: {json.dumps(result)}")


if __name__ == "__main__":
    main()
