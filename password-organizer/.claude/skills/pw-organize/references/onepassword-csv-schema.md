# 1Password CSV Export Schema

1Password exports vary by version and item type. The parser must handle any column layout dynamically.

## Common Login Export Columns

The most common 1Password CSV export for Login items:

```
Title,Url,Username,Password,Notes,OTPAuth
```

| Column | Description | Always Present |
|--------|-------------|----------------|
| Title | Display name of the entry | Yes |
| Url | Website URL | Usually (may be empty) |
| Username | Login username or email | Usually (may be empty) |
| Password | The password value | Yes |
| Notes | Free-text notes field | Sometimes |
| OTPAuth | TOTP seed URI | Sometimes |

## Extended Export Columns

Some exports include additional fields:

| Column | Description |
|--------|-------------|
| Type | Item type: Login, Secure Note, Credit Card, Identity, etc. |
| Tags | Comma-separated tags |
| Vault | Original vault name in 1Password |
| Created | Creation timestamp |
| Modified | Last modified timestamp |
| Favorite | Boolean favorite flag |

## Non-Login Item Types

- **Secure Note** — Title, Notes (no URL/Username/Password)
- **Credit Card** — Title, card fields as extra columns
- **Identity** — Title, name/address fields as extra columns

## Parsing Rules

1. **Read the header row first** — Never assume fixed column positions
2. **Preserve all columns** — Even unknown/custom columns must survive round-trip
3. **Handle empty fields** — Many entries have blank URLs, usernames, or notes
4. **UTF-8 encoding** — 1Password exports use UTF-8
5. **Standard CSV quoting** — Fields containing commas, quotes, or newlines are double-quoted
6. **Multiple CSVs** — A user may export from multiple existing vaults, producing multiple CSV files

## Categorization-Relevant Fields

For categorization, the key fields are:
- **Username** — If it's an email, matches against known personal/business emails
- **Url** — Domain reveals what the service is
- **Title** — Service name when URL is missing
- **Type** — Non-Login items may need different handling
