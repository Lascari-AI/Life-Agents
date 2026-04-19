#!/usr/bin/env python3
"""
Parse 1Password CSV export(s) into structured JSON.

Reads all CSV files from the source directory, auto-detects headers,
and produces a unified JSON with all entries and summary statistics.

Usage:
    python parse_csv.py --source-dir "session/source-files/" --output "session/working/parsed_entries.json"
"""

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse


def extract_domain(url: str) -> str:
    """Extract the base domain from a URL."""
    if not url:
        return ""
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    try:
        parsed = urlparse(url)
        domain = parsed.netloc or parsed.path.split("/")[0]
        # Strip www. prefix
        domain = re.sub(r"^www\.", "", domain.lower())
        return domain
    except Exception:
        return ""


def extract_email(username: str) -> str:
    """Extract email from username field if it is an email."""
    if not username:
        return ""
    username = username.strip().lower()
    if "@" in username and "." in username.split("@")[-1]:
        return username
    return ""


def parse_csv_file(csv_path: Path) -> tuple[list[str], list[dict]]:
    """Parse a single CSV file and return (headers, rows)."""
    entries = []
    headers = []

    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        headers = list(reader.fieldnames or [])

        for row_num, row in enumerate(reader, start=2):  # row 1 is header
            entry = {
                "_source_file": csv_path.name,
                "_row_number": row_num,
                "_parsed_domain": "",
                "_parsed_email": "",
            }

            # Preserve all original fields
            original_row = {}
            for key in headers:
                original_row[key] = row.get(key, "")
            entry["original_row"] = original_row

            # Extract domain from URL-like fields
            for url_field in ["Url", "URL", "url", "Website", "website"]:
                if url_field in original_row and original_row[url_field]:
                    entry["_parsed_domain"] = extract_domain(original_row[url_field])
                    break

            # Extract email from username-like fields
            for user_field in ["Username", "username", "User", "Login", "Email", "email"]:
                if user_field in original_row and original_row[user_field]:
                    entry["_parsed_email"] = extract_email(original_row[user_field])
                    break

            entries.append(entry)

    return headers, entries


def main():
    parser = argparse.ArgumentParser(description="Parse 1Password CSV exports")
    parser.add_argument("--source-dir", required=True, help="Directory containing CSV file(s)")
    parser.add_argument("--output", required=True, help="Output JSON path")

    args = parser.parse_args()

    source_dir = Path(args.source_dir)
    output_path = Path(args.output)

    csv_files = sorted(source_dir.glob("*.csv"))
    if not csv_files:
        print("Error: No CSV files found in source directory", file=sys.stderr)
        sys.exit(1)

    all_entries = []
    all_headers = []
    source_files = []

    for csv_path in csv_files:
        print(f"Parsing: {csv_path.name}")
        headers, entries = parse_csv_file(csv_path)

        # Use the first file's headers as the canonical set
        if not all_headers:
            all_headers = headers
        else:
            # Merge any new headers not seen before
            for h in headers:
                if h not in all_headers:
                    all_headers.append(h)

        all_entries.extend(entries)
        source_files.append(csv_path.name)
        print(f"  Found {len(entries)} entries")

    # Build statistics
    unique_emails = set()
    unique_domains = set()
    entry_types = {}

    for entry in all_entries:
        if entry["_parsed_email"]:
            unique_emails.add(entry["_parsed_email"])
        if entry["_parsed_domain"]:
            unique_domains.add(entry["_parsed_domain"])

        # Count by type if the field exists
        orig = entry["original_row"]
        entry_type = orig.get("Type") or orig.get("type") or "Login"
        entry_types[entry_type] = entry_types.get(entry_type, 0) + 1

    result = {
        "stats": {
            "total_entries": len(all_entries),
            "unique_emails": sorted(unique_emails),
            "unique_domains": sorted(unique_domains),
            "entry_types": entry_types,
            "source_files": source_files,
            "headers": all_headers,
        },
        "entries": all_entries,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\nParsed {len(all_entries)} entries from {len(csv_files)} file(s)")
    print(f"Unique emails: {len(unique_emails)}")
    print(f"Unique domains: {len(unique_domains)}")
    print(f"Entry types: {entry_types}")
    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()
