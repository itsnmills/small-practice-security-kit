# Evidence Connector Standard

## Purpose

The Evidence Connector Standard turns the kit from a manual intake workflow into a local-first evidence operations workflow. A practice owner should connect or import what already exists, then the kit should ask only for the gaps that require an owner, MSP, vendor, or qualified reviewer.

Connectors collect metadata and summaries. They do not collect PHI, credentials, mailbox contents, Drive or SharePoint file contents, raw logs, patient screenshots, raw contracts, or incident-sensitive source details.

The product filter is security, simplicity, and time saving:

- Security: safe metadata first, no PHI expected, no secrets, no raw logs, no screenshots, and no raw contract uploads.
- Simplicity: the shortest command should be the safe command.
- Time saving: every observed gap should become an owner, MSP, vendor, or qualified-reviewer action.

## Product Modes

1. Owner Mode: show what is known, what is missing, who owns the answer, and what unsafe data must stay out.
2. MSP Partner Mode: generate exact evidence requests, remediation questions, and client-ready proof packets that help the MSP show its work.
3. Local Collector Mode: run read-only collectors or import safe exports on the practice-owned or MSP-owned machine.

## New Rule

Manual input is only required when the system cannot observe the answer, an owner must approve it, a vendor must answer it, an MSP must confirm it, or a qualified reviewer must assess it.

## Connector Contract

Every connector output is a JSON evidence bundle with:

- `run`: connector name, version, mode, timestamps, input reference, warnings, and safety manifest.
- `evidence`: normalized evidence items with source, status, confidence, observations, owner lane, recommended question, acceptable evidence, unsafe inputs, recommended action, next action, timeframe, reviewer-needed, owner/MSP/vendor/reviewer views, stage, and priority.

Normalized evidence shape:

```json
{
  "evidence_id": "CONN-DNS-DMARC-001",
  "source_system": "dns",
  "source_type": "public_lookup",
  "collected_at": "2026-05-19T00:00:00Z",
  "phi_expected": false,
  "confidence": "observed_from_public_dns",
  "control_area": "email_authentication",
  "subject": "dmarc_policy",
  "summary": "DMARC policy for exampleclinic.test: none.",
  "plain_english_summary": "The practice has DMARC monitoring, but enforcement still needs an MSP review.",
  "why_it_matters": "Email-authentication evidence helps the owner and MSP reduce spoofing risk without collecting mailbox contents.",
  "observations": {
    "dmarc_record_count": 1,
    "dmarc_monitoring_only": 1
  },
  "unsafe_inputs_excluded": [
    "raw email contents",
    "mailbox contents",
    "private DNS provider credentials"
  ],
  "recommended_action": "Review DMARC posture with the MSP and document whether monitoring-only is intentional.",
  "owner_lane": "msp",
  "recommended_question": "Can the MSP confirm whether DMARC should move from monitoring to quarantine or reject after sender alignment is reviewed?",
  "acceptable_evidence": [
    "DMARC lookup date",
    "policy value",
    "aggregate report owner",
    "authorized sender review",
    "MSP confirmation"
  ],
  "priority": "medium",
  "timeframe": "60_days",
  "reviewer_needed": ["msp", "office_manager"],
  "owner_view": "Ask the MSP whether DMARC can safely move beyond monitoring.",
  "msp_view": "Review sender alignment and return a dated DMARC evidence summary.",
  "vendor_view": "No direct vendor ask unless a sender vendor must be validated.",
  "legal_compliance_view": "No legal conclusion is made; route formal compliance questions to a qualified reviewer.",
  "next_action": "Review DMARC posture with the MSP and document whether monitoring-only is intentional."
}
```

Evidence confidence values:

- `observed_from_public_dns`
- `observed_from_public_web`
- `observed_from_api`
- `imported_from_client_export`
- `imported_from_msp_export`
- `self_attested`
- `derived_from_packet`
- `unknown`

Evidence statuses:

- `observed`
- `current`
- `missing`
- `stale`
- `needs_review`
- `requested`
- `not_applicable`

## Safety Manifest

Each connector must declare:

- default mode,
- whether PHI is expected,
- allowed data,
- forbidden data,
- required scopes if any,
- unsafe scopes,
- human approval requirements.

Default connectors use official read-only APIs when the practice/MSP can authorize them, with CSV imports as a fallback. Official Google Workspace and Microsoft 365 connectors store OAuth tokens in the macOS Keychain when available, fall back to a local `0600` token file only when Keychain is unavailable, and collect only aggregated metadata.

Official Google Workspace evidence currently translates API metadata into action-ready MFA, admin-role, and account-lifecycle evidence. Official Microsoft 365 evidence translates Graph metadata into MFA, account-status, self-service password reset, guest-access, and account-lifecycle evidence. These connectors store aggregate counts and evidence questions; they do not store user identities, mailbox contents, Drive/SharePoint/OneDrive contents, raw sign-in logs, screenshots, credentials, or private admin URLs.

## Practice-Owner Workflow

1. Open the connector wizard or run a connect command.
2. Generate a connector bundle.
3. Run Sprint Mode with `--evidence`.
4. Open `sprint-command-center.html`.
5. Send only the generated MSP/vendor/reviewer questions that apply.

Example:

```bash
python -m small_practice_security_kit connect wizard --out out/connector-wizard.html
python -m small_practice_security_kit connect google-workspace --client-id "$VELARI_GOOGLE_CLIENT_ID" --client-secret "$VELARI_GOOGLE_CLIENT_SECRET"
python -m small_practice_security_kit collect google-workspace --out evidence/google-workspace.json
python -m small_practice_security_kit connect microsoft-365 --client-id "$VELARI_MICROSOFT_CLIENT_ID"
python -m small_practice_security_kit collect microsoft-365 --out evidence/microsoft-365.json
python -m small_practice_security_kit import csv users samples/connectors/google_workspace_users.csv --out evidence/users.json
python -m small_practice_security_kit collect dns --domain exampleclinic.test --out evidence/dns.json
python -m small_practice_security_kit collect vendor-public --vendor "Example AI Scribe Vendor" --domain example.com --out evidence/vendor-public.json
python -m small_practice_security_kit generate msp-request --profile samples/family_dental_clinic.yaml --evidence evidence/*.json --out out/msp-request.md
python -m small_practice_security_kit import msp-response samples/connectors/msp_response.yaml --out evidence/msp-response.json
python -m small_practice_security_kit evidence refresh --current evidence/*.json --out out/evidence-refresh.json
python -m small_practice_security_kit generate views --profile samples/family_dental_clinic.yaml --evidence evidence/*.json --out out/views
python -m small_practice_security_kit build samples/family_dental_clinic.yaml --evidence evidence/*.json --output-root out
```

## Claims Boundary

Connector evidence supports readiness, evidence collection, workflow review, and owner/MSP/vendor handoff. It does not make legal, breach, HIPAA, vendor approval, AI production-use, cyber insurance, or formal Security Risk Analysis determinations.
