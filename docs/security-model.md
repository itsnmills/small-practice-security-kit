# Security Model and Data Boundary

Small Practice Security Kit is designed for **local-first, PHI-avoidant evidence organization**. It helps a practice prepare a packet of references, owners, review dates, and next actions. It is not designed to store patient-level data, secrets, raw incident records, or full private evidence archives.

## Design goals

- Keep the default workflow on the user's machine.
- Store evidence references instead of sensitive evidence content.
- Make the PHI/secrets boundary visible in the UI, docs, generated packet, and manifest.
- Generate artifacts that can be reviewed by a practice owner, MSP, consultant, attorney, insurer, or security reviewer without pretending to certify compliance.
- Block high-confidence sensitive values before they are saved.

## Local-only defaults

- The local server binds to `127.0.0.1` by default.
- The UI displays local-only status.
- There is no telemetry.
- There is no analytics.
- There is no cloud sync.
- There are no model calls.
- There are no hidden update checks.

## Accepted data types

Use non-sensitive operational references:

- practice type and approximate size,
- system names,
- vendor names,
- role/group names,
- workflow descriptions,
- BAA/review status summaries,
- ticket IDs or evidence reference IDs,
- evidence folder references,
- review dates,
- owner names by role, not patient identifiers,
- non-sensitive summary notes.

## Prohibited data types

Do not enter or commit:

- patient names,
- medical record numbers,
- dates of birth,
- diagnoses,
- clinical notes,
- claim narratives,
- patient images,
- real incident details that identify patients or staff,
- passwords,
- API keys,
- MFA recovery codes,
- private keys,
- tokens,
- session cookies,
- private URLs,
- presigned links,
- full private contracts, BAAs, screenshots, logs, or raw evidence exports.

## Evidence-reference model

The kit should answer:

> What evidence should exist, who owns it, where is it referenced, and what gap does it support?

It should not store the evidence itself. Good examples:

- `EVID-BACKUP-RESTORE-Q2` — backup restore test record exists in the MSP ticket system.
- `EVID-BAA-BILLING-2026` — billing vendor BAA review date needs confirmation.
- `EVID-ACCESS-QTR` — quarterly user access review needs export and owner signoff.

Bad examples:

- pasted patient charts,
- raw screenshots containing patient names,
- full contracts with private terms,
- access tokens or admin URLs,
- incident timelines with identifiable patient or employee details.

## Write endpoint controls

Write endpoints require:

- localhost client address,
- same-origin request,
- JSON content type,
- request body under the local size limit,
- per-session `X-SPSK-Token`,
- schema-valid profile data.

## Profile write safety

Profiles are saved under:

```text
profiles/
```

The app:

- refuses writes outside `profiles/`,
- writes atomically through a temporary file,
- creates timestamped backups,
- appends a local change log,
- never stores sensitive warning values in the log.

## Metadata-only folder inventory

The evidence screen can optionally scan a local folder for evidence references.

This inventory:

- records filename-derived titles,
- records relative paths,
- records extension,
- records size,
- records modified timestamp,
- does not read file contents,
- skips unsupported file types,
- skips hidden files and folders,
- blocks sensitive-looking filenames before import.

## Sensitive data detection

Before saving, the app scans profile content locally for:

- SSN-like patterns,
- MRN / patient identifier labels,
- DOB labels,
- private keys,
- API tokens,
- password-like values,
- payment card-like values,
- long clinical-note-like text.

High-confidence sensitive data blocks the save. Medium-confidence findings are returned as warnings without logging the sensitive values.

## Public demo boundary

Public demos must be synthetic. Demo practices, vendors, system names, risk findings, and evidence references should be fictional or generic. Public packet artifacts should be safe to publish in a GitHub repo.

The current checked-in demo lives in [`docs/demo/`](demo/) and uses `Family Dental Clinic` as a fictional sample.

## Future local AI boundary

Local AI-assisted discovery is intentionally not part of v1.

If added later, it must be:

- opt-in,
- local-only by default,
- no-PHI by default,
- review-before-import,
- provenance-labeled,
- treated as suggestions, not facts,
- logged with provider/model/prompt-template metadata when applicable.

Cloud AI should remain outside the default workflow unless a practice has a reviewed vendor relationship, a clear BAA/contract boundary where required, explicit PHI restrictions, human review, and audit logging.

## What this does not prove

Generated packets do not prove:

- HIPAA compliance,
- legal sufficiency,
- formal Security Risk Analysis completion,
- breach status,
- vendor safety,
- AI tool safety,
- backup restorability,
- access control correctness,
- insurer acceptance,
- that all real evidence exists.

Bring the packet to qualified legal, compliance, MSP/IT, security, incident response, and/or insurance reviewers before relying on it for operational decisions.
