#!/usr/bin/env python3
"""
Initialize a password organizer session directory.

Creates the session folder structure and writes an empty intake.md
ready for the interview phase.

Usage:
    python init_session.py --session "my-passwords"
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
    parser = argparse.ArgumentParser(description="Initialize a password organizer session")
    parser.add_argument("--session", required=True, help="Session name (e.g. my-passwords)")

    args = parser.parse_args()

    try:
        root = get_project_root()
        session_dir = root / args.session

        if not session_dir.exists():
            session_dir.mkdir(parents=True)
            print(f"Created: {session_dir}")

        # Create source-files directory
        source_dir = session_dir / "source-files"
        if not source_dir.exists():
            source_dir.mkdir()
            print(f"Created: {source_dir}")

        # Create working directory
        working_dir = session_dir / "working"
        if not working_dir.exists():
            working_dir.mkdir()
            print(f"Created: {working_dir}")

        # Create output directory
        output_dir = session_dir / "output"
        if not output_dir.exists():
            output_dir.mkdir()
            print(f"Created: {output_dir}")

        # Create intake.md inside working directory
        intake_path = working_dir / "intake.md"

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
                print("  No STATUS markers found.")
        else:
            today = datetime.now().strftime("%Y-%m-%d")
            template_path = root / ".claude/skills/pw-organize/references/intake-template.md"
            template = template_path.read_text()
            content = (
                template
                .replace("{{SESSION}}", args.session)
                .replace("{{NAME}}", "TBD")
                .replace("{{DATE}}", today)
            )
            intake_path.write_text(content)
            print(f"Created: {intake_path}")

        print(f"\nSession initialized for password organization.")
        print(f"  Session folder: {session_dir}")
        print(f"  Source files: {source_dir}")
        print(f"  Working dir: {working_dir}")
        print(f"  Output dir: {output_dir}")
        print(f"  Intake file: {intake_path}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
