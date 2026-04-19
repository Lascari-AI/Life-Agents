#!/usr/bin/env python3
"""
Apply deterministic categorization rules to parsed password entries.

Reads the parsed entries JSON and the intake.md, applies email-match,
domain-match, and user-defined rules in priority order.

Usage:
    python apply_rules.py --entries "working/parsed_entries.json" \
                          --intake "working/intake.md" \
                          --output "working/rules_result.json"
"""

import argparse
import json
import re
import sys
from pathlib import Path


def parse_intake(intake_path: Path) -> dict:
    """Parse intake.md to extract rules data."""
    content = intake_path.read_text()
    data = {
        "personal_emails": [],
        "business_emails": [],
        "client_emails": [],
        "business_domains": [],
        "client_domains": [],
        "vault_categories": [],
        "user_rules": [],
        "email_to_vault": {},
        "domain_to_vault": {},
    }

    # Parse vault categories table
    vault_section = re.search(
        r"## Vault Categories\n<!-- STATUS: complete -->\n(.*?)(?=\n## |\Z)",
        content, re.DOTALL
    )
    if vault_section:
        for match in re.finditer(r"\|\s*(\S+)\s*\|\s*([^|]+)\s*\|\s*([^|]*)\s*\|", vault_section.group(1)):
            key = match.group(1).strip()
            if key == "Key" or key.startswith("-"):
                continue
            data["vault_categories"].append({
                "key": key,
                "display_name": match.group(2).strip(),
                "description": match.group(3).strip(),
            })

    # Parse identity section for emails and domains
    identity_section = re.search(
        r"## Identity\n<!-- STATUS: complete -->\n(.*?)(?=\n## |\Z)",
        content, re.DOTALL
    )
    if identity_section:
        section = identity_section.group(1)
        # Look for personal emails
        for match in re.finditer(r"[Pp]ersonal [Ee]mail[s]?:\s*(.+)", section):
            emails = [e.strip().lower() for e in re.split(r"[,;]", match.group(1)) if "@" in e]
            data["personal_emails"].extend(emails)
        # Look for business emails
        for match in re.finditer(r"[Bb]usiness [Ee]mail[s]?:\s*(.+)", section):
            emails = [e.strip().lower() for e in re.split(r"[,;]", match.group(1)) if "@" in e]
            data["business_emails"].extend(emails)
        # Look for business domains
        for match in re.finditer(r"[Bb]usiness [Dd]omain[s]?:\s*(.+)", section):
            domains = [d.strip().lower() for d in re.split(r"[,;]", match.group(1)) if "." in d]
            data["business_domains"].extend(domains)

    # Parse past clients section
    clients_section = re.search(
        r"## Past Clients\n<!-- STATUS: complete -->\n(.*?)(?=\n## |\Z)",
        content, re.DOTALL
    )
    if clients_section:
        section = clients_section.group(1)
        for match in re.finditer(r"[Cc]lient [Ee]mail[s]?:\s*(.+)", section):
            emails = [e.strip().lower() for e in re.split(r"[,;]", match.group(1)) if "@" in e]
            data["client_emails"].extend(emails)
        for match in re.finditer(r"[Cc]lient [Dd]omain[s]?:\s*(.+)", section):
            domains = [d.strip().lower() for d in re.split(r"[,;]", match.group(1)) if "." in d]
            data["client_domains"].extend(domains)

    # Parse user-defined rules section
    rules_section = re.search(
        r"## Categorization Rules\n<!-- STATUS: complete -->\n(.*?)(?=\n## |\Z)",
        content, re.DOTALL
    )
    if rules_section:
        for match in re.finditer(r"[-*]\s+(.+?)→\s*(\S+)", rules_section.group(1)):
            data["user_rules"].append({
                "pattern": match.group(1).strip().lower(),
                "vault": match.group(2).strip(),
            })

    # Build email→vault mapping
    # Determine vault keys for personal/business/clients by finding
    # vault categories that match those concepts
    vault_keys = {vc["key"]: vc for vc in data["vault_categories"]}

    for email in data["personal_emails"]:
        # Find a vault key that matches "personal"
        for key in vault_keys:
            if "personal" in key.lower():
                data["email_to_vault"][email] = key
                break

    for email in data["business_emails"]:
        for key in vault_keys:
            if "business" in key.lower():
                data["email_to_vault"][email] = key
                break

    for email in data["client_emails"]:
        for key in vault_keys:
            if "client" in key.lower():
                data["email_to_vault"][email] = key
                break

    # Build domain→vault mapping
    for domain in data["business_domains"]:
        for key in vault_keys:
            if "business" in key.lower():
                data["domain_to_vault"][domain] = key
                break

    for domain in data["client_domains"]:
        for key in vault_keys:
            if "client" in key.lower():
                data["domain_to_vault"][domain] = key
                break

    return data


def match_domain(entry_domain: str, known_domains: dict) -> str | None:
    """Check if entry domain matches any known domain (including subdomains)."""
    if not entry_domain:
        return None
    entry_domain = entry_domain.lower()
    for domain, vault in known_domains.items():
        if entry_domain == domain or entry_domain.endswith("." + domain):
            return vault
    return None


def apply_user_rules(entry: dict, user_rules: list) -> str | None:
    """Check if entry matches any user-defined rules."""
    original = entry.get("original_row", {})
    title = (original.get("Title") or original.get("title") or "").lower()
    url = (original.get("Url") or original.get("URL") or original.get("url") or "").lower()
    username = (original.get("Username") or original.get("username") or "").lower()
    domain = entry.get("_parsed_domain", "").lower()

    for rule in user_rules:
        pattern = rule["pattern"]
        # Check if pattern matches title, url, username, or domain
        if pattern in title or pattern in url or pattern in username or pattern in domain:
            return rule["vault"]
    return None


def main():
    parser = argparse.ArgumentParser(description="Apply categorization rules")
    parser.add_argument("--entries", required=True, help="Path to parsed_entries.json")
    parser.add_argument("--intake", required=True, help="Path to intake.md")
    parser.add_argument("--output", required=True, help="Output path for rules_result.json")

    args = parser.parse_args()

    entries_path = Path(args.entries)
    intake_path = Path(args.intake)
    output_path = Path(args.output)

    with open(entries_path, "r", encoding="utf-8") as f:
        parsed = json.load(f)

    intake_data = parse_intake(intake_path)
    entries = parsed["entries"]

    matched = 0
    unmatched = 0
    method_counts = {}

    for entry in entries:
        vault = None
        method = None

        # Priority 1: User-defined rules
        vault = apply_user_rules(entry, intake_data["user_rules"])
        if vault:
            method = "rule:user-defined"

        # Priority 2: Email match
        if not vault:
            email = entry.get("_parsed_email", "").lower()
            if email and email in intake_data["email_to_vault"]:
                vault = intake_data["email_to_vault"][email]
                method = "rule:email-match"

        # Priority 3: Domain match
        if not vault:
            domain = entry.get("_parsed_domain", "")
            vault_key = match_domain(domain, intake_data["domain_to_vault"])
            if vault_key:
                vault = vault_key
                method = "rule:domain-match"

        entry["vault"] = vault
        entry["method"] = method
        entry["confidence"] = "high" if vault else None
        entry["flag"] = None
        entry["notes"] = None

        if vault:
            matched += 1
            method_counts[method] = method_counts.get(method, 0) + 1
        else:
            unmatched += 1

    result = {
        "stats": parsed["stats"],
        "vault_categories": intake_data["vault_categories"],
        "entries": entries,
        "rule_summary": {
            "matched": matched,
            "unmatched": unmatched,
            "by_method": method_counts,
        },
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\nRule application complete:")
    print(f"  Matched: {matched}")
    print(f"  Unmatched: {unmatched}")
    print(f"  By method: {method_counts}")
    print(f"  Output: {output_path}")


if __name__ == "__main__":
    main()
