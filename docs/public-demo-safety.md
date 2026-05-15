# Public Demo Safety

Public demos must be fictional, PHI-avoidant, and safe to publish.

## Before publishing or refreshing `docs/demo/`

- Run `python -m small_practice_security_kit validate samples/family_dental_clinic.yaml`.
- Run `python -m small_practice_security_kit build samples/family_dental_clinic.yaml`.
- Run `python -m small_practice_security_kit export-binder samples/family_dental_clinic.yaml`.
- Run `python -m small_practice_security_kit export-demo --profile samples/family_dental_clinic.yaml --output docs/demo`.
- Run both import scripts against example CSVs if they changed.
- Run `python scripts/validate_content.py`.
- Run `python -m unittest discover -s tests`.
- Confirm examples do not include patient names, MRNs, DOBs, diagnoses, claim contents, clinical notes, passwords, API keys, tokens, private keys, private URLs, presigned links, full contracts, or real incident details.

## Checked-in demo artifacts

The checked-in public snapshot lives in [`docs/demo/`](docs/demo/). It should include:

- `README.md`
- `review-packet.md`
- `review-packet.html`
- `packet-manifest.json`
- generated section markdown files
- `screenshots/review-packet.png`

## Safe demo language

Use:

- fictional practice names,
- generic vendor names,
- evidence reference IDs,
- owner roles,
- review dates,
- synthetic gaps,
- clear limitations.

Avoid:

- implying certification,
- claiming legal sufficiency,
- using real client anecdotes,
- publishing private operational details,
- turning the demo into a fake audit opinion.

The demo export writes packet files and binder export files into `docs/demo/` after schema validation and sensitive-content scanning. It attempts a Linux Chrome/Chromium screenshot when available and skips with a warning when the browser is missing. Use `--pdf` only for optional PDF rendering; CI and unit tests do not require system Chrome.

CI uploads the generated demo packet as an Actions artifact for pull requests and pushes to `main`. The workflow does not publish GitHub releases automatically.
