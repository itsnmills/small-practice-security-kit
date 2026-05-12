# Security Model

The local intake workspace is secure-first and PHI-avoidant by design.

## Local-only defaults

- The server binds to `127.0.0.1` by default.
- The UI displays local-only status.
- There is no telemetry.
- There is no analytics.
- There is no cloud sync.
- There are no model calls.
- There are no hidden update checks.

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

## PHI avoidance

The intake warns users not to enter:

- patient names,
- medical record numbers,
- dates of birth,
- clinical notes,
- claim narratives,
- passwords,
- API keys,
- private keys,
- real incident details that identify patients.

The system is meant to store evidence references, not sensitive evidence content.

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

## Future local AI boundary

Local AI-assisted discovery is intentionally not part of v1.

If added later, it must be:

- opt-in,
- local-only,
- no-PHI by default,
- review-before-import,
- provenance-labeled,
- treated as suggestions, not facts.
