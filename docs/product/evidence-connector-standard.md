# Velari Evidence Connector Standard

## Purpose

The Evidence Connector Standard turns Velari from a manual intake workflow into a local-first evidence operations workflow. A practice owner should connect or import what already exists, then Velari should ask only for the gaps that require an owner, MSP, vendor, or qualified reviewer.

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
- `evidence`: normalized evidence items with source, status, confidence, observations, owner lane, recommended question, acceptable evidence, unsafe inputs, recommended action, next action, stage, and priority.

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

Default Velari connectors use CSV imports, public DNS metadata, and public vendor-page triage. Live API connectors should start read-only and metadata-first.

## Practice-Owner Workflow

1. Export a safe admin CSV or run a local collector.
2. Generate a connector bundle.
3. Run Sprint Mode with `--evidence`.
4. Open `sprint-command-center.html`.
5. Send only the generated MSP/vendor/reviewer questions that apply.

Example:

```bash
python -m small_practice_security_kit import csv users samples/connectors/google_workspace_users.csv --out evidence/users.json
python -m small_practice_security_kit collect dns --domain exampleclinic.test --out evidence/dns.json
python -m small_practice_security_kit collect vendor-public --vendor "Example AI Scribe Vendor" --domain example.com --out evidence/vendor-public.json
python -m small_practice_security_kit generate msp-request --profile samples/family_dental_clinic.yaml --evidence evidence/*.json --out out/msp-request.md
python -m small_practice_security_kit build samples/family_dental_clinic.yaml --evidence evidence/*.json --output-root out
```

## Claims Boundary

Connector evidence supports readiness, evidence collection, workflow review, and owner/MSP/vendor handoff. It does not make legal, breach, HIPAA, vendor approval, AI production-use, cyber insurance, or formal Security Risk Analysis determinations.
