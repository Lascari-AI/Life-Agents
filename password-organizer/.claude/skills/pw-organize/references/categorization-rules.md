# Categorization Rules

Rules are applied in priority order. The first matching rule wins.

## Rule Priority

1. **User-defined explicit rules** (from intake Section 4)
   - Exact matches the user specified during interview
   - Example: "Anything from clientdomain.com → Clients"
   - These override all other rules

2. **Email-match rules** (from intake Section 1)
   - If the entry's Username field is an email address that matches a known email:
     - Personal email match → Personal vault
     - Business email match → Business vault
     - Client email match → Clients vault
   - Confidence: `high` (deterministic identity match)

3. **Domain-match rules** (from intake Sections 1 & 2)
   - If the entry's URL domain matches a known domain:
     - Business domain(s) → Business vault
     - Client domain(s) → Clients vault
   - Confidence: `high` (deterministic domain match)

4. **AI service knowledge** (handled by agent, not script)
   - For entries not matched by rules 1-3
   - Agent uses service-knowledge.md as a framework
   - Assigns confidence: `high`, `medium`, or `low`
   - Low confidence → flagged for review

## Rule Application Details

### Email Matching
- Extract the email from the Username field
- Normalize: lowercase, trim whitespace
- Compare against known emails from intake
- Only match if the Username IS an email (contains @)

### Domain Matching
- Extract domain from the Url field
- Normalize: lowercase, strip www., strip trailing paths
- Compare against known business/client domains
- Subdomain matching: `admin.clientdomain.com` matches `clientdomain.com`

### Conflict Resolution
- If email says "personal" but domain says "business" → flag as ambiguous
- If multiple rules match different vaults → flag as ambiguous
- User-defined rules always win over email/domain rules

## Entry Structure After Categorization

```json
{
  "original_row": { "Title": "...", "Url": "...", ... },
  "vault": "personal",
  "method": "rule:email-match",
  "confidence": "high",
  "flag": null,
  "notes": null
}
```

### Method Values
- `rule:user-defined` — matched a user-specified explicit rule
- `rule:email-match` — username email matched a known email
- `rule:domain-match` — URL domain matched a known domain
- `ai:service-knowledge` — classified by AI based on service type

### Confidence Values
- `high` — certain classification (rule match or obvious service)
- `medium` — likely correct but could go either way
- `low` — uncertain, flagged for review

### Flag Values
- `null` — no flag, confident assignment
- `ambiguous` — could reasonably go to multiple vaults
- `shared-service` — known to be used for both personal and business
- `unknown-service` — unrecognizable, no URL, minimal data
- `no-data` — entry has almost no identifying information
