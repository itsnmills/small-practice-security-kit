# Adapter Contract

All import and export adapters normalize records into one exchange contract so companion repos can plug into the same packet workflow.

Required fields:

- `source_repo`
- `source_artifact`
- `item_id`
- `module`
- `title`
- `status`
- `risk`
- `owner`
- `evidence_needed`
- `evidence_reference`
- `source_mapping`
- `next_review_due`
- `notes`

Adapters should write evidence references, not raw PHI, credentials, incident details, or production evidence files.

