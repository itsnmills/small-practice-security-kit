# GOAL - Velari Official Connectors Sprint

## Objective

Move Velari beyond CSV fallback into official, owner-simple connector flows that reduce manual entry while preserving the security boundary.

The product rule is:

`click/connect -> collect metadata -> normalize evidence -> assign owner/MSP/vendor/reviewer action`

## Seven Delivery Items

1. Google Workspace official OAuth connector for Admin SDK user metadata.
2. Microsoft 365 official OAuth connector for Graph user and MFA-registration metadata.
3. MSP response import loop for evidence requests and ticket/reference responses.
4. Local connector wizard HTML so practices can see the exact connect/collect path.
5. Evidence refresh report for stale, changed, new, and removed evidence.
6. Connector confidence scoring on every normalized evidence item.
7. Practice-ready lane exports for owner, MSP, vendor, and reviewer views.

## Safety Boundary

Official connectors are read-only metadata collectors. They must not request or store:

- PHI or patient identifiers,
- mailbox contents,
- Drive, OneDrive, SharePoint, or Teams content,
- raw sign-in logs,
- credentials,
- private admin URLs,
- patient screenshots,
- raw contracts,
- incident-sensitive details.

## Official Connector Scopes

Google Workspace:

- `https://www.googleapis.com/auth/admin.directory.user.readonly`

Microsoft 365:

- `offline_access`
- `https://graph.microsoft.com/User.Read.All`
- `https://graph.microsoft.com/AuditLog.Read.All`

## Acceptance Criteria

- Official connectors aggregate rows immediately and do not store user emails or user principal names.
- OAuth tokens are stored in macOS Keychain when available, or a local `0600` file fallback outside the repo.
- `connect wizard` creates a local setup page.
- `import msp-response` normalizes MSP ticket/reference responses.
- `evidence refresh` reports freshness and changes.
- `generate views` writes owner, MSP, vendor, and reviewer Markdown views.
- Connector schemas validate with confidence scores.
- Full tests pass.

## Non-Goals

- No EHR/FHIR connector in this sprint.
- No email, file, chat, or raw sign-in log collection.
- No automatic remediation.
- No legal, breach, HIPAA, vendor approval, insurance, or formal Security Risk Analysis conclusions.
