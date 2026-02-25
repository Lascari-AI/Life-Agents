#!/usr/bin/env python3
"""
Initialize a CPA tax prep session directory.

Creates the session folder structure under the tax year directory
and writes an empty intake.md ready for the interview phase.

Usage:
    python init-session.py --year 2025 --name "Jane Smith"
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path


def get_project_root() -> Path:
    """Find project root by looking for .claude directory."""
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / ".claude").is_dir():
            return parent
    raise RuntimeError("Could not find project root (.claude directory)")


def main():
    parser = argparse.ArgumentParser(description="Initialize a CPA tax prep session")
    parser.add_argument("--year", required=True, help="Tax year (e.g. 2025)")
    parser.add_argument("--name", required=True, help="Filer name")

    args = parser.parse_args()

    try:
        root = get_project_root()
        year_dir = root / f"{args.year} Taxes"

        if not year_dir.exists():
            year_dir.mkdir(parents=True)
            print(f"Created: {year_dir}")

        # Create write-up directory first (intake.md goes inside it)
        writeup_dir = year_dir / f"{args.year} taxes write up"
        if not writeup_dir.exists():
            writeup_dir.mkdir()
            print(f"Created: {writeup_dir}")

        # Create output directory for deliverables
        output_dir = writeup_dir / "output"
        if not output_dir.exists():
            output_dir.mkdir()
            print(f"Created: {output_dir}")

        # Create source-documents directory with subdirectories
        source_dir = year_dir / "source-documents"
        if not source_dir.exists():
            source_dir.mkdir()
            print(f"Created: {source_dir}")
            subdirs = [
                "bank-statements",
                "quarterly-estimates",
                "income",
                "health-insurance",
                "other",
            ]
            for subdir in subdirs:
                sub_path = source_dir / subdir
                sub_path.mkdir()
                print(f"Created: {sub_path}")

        # Create intake.md inside write-up directory
        intake_path = writeup_dir / "intake.md"

        # Check for legacy intake.md at top level and migrate
        legacy_intake = year_dir / "intake.md"
        if legacy_intake.exists() and not intake_path.exists():
            legacy_intake.rename(intake_path)
            print(f"Migrated: {legacy_intake} -> {intake_path}")

        if intake_path.exists():
            # Report progress from existing file
            content = intake_path.read_text()
            complete = content.count("<!-- STATUS: complete -->")
            pending = content.count("<!-- STATUS: pending -->")
            total = complete + pending
            print(f"intake.md already exists at {intake_path}")
            if total > 0:
                print(f"  Progress: {complete}/{total} sections complete")
                if complete == total:
                    print("  Intake is fully complete.")
                else:
                    print(f"  {pending} section(s) still pending — resume available.")
            else:
                print("  No STATUS markers found (legacy format).")
        else:
            today = datetime.now().strftime("%Y-%m-%d")
            template_path = root / ".claude/skills/cpa-tax-prep/references/intake-template.md"
            template = template_path.read_text()
            content = (
                template
                .replace("{{YEAR}}", args.year)
                .replace("{{NAME}}", args.name)
                .replace("{{DATE}}", today)
            )
            intake_path.write_text(content)
            print(f"Created: {intake_path}")

        print(f"\nSession initialized for {args.year} tax prep.")
        print(f"  Year folder: {year_dir}")
        print(f"  Write-up folder: {writeup_dir}")
        print(f"  Intake file: {intake_path}")
        print(f"  Output folder: {output_dir}")
        print(f"  Source documents: {source_dir}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
