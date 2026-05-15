# Public Demo Safety

Public demos must be fictional, PHI-avoidant, and safe to publish.

## Before publishing or refreshing `docs/demo/`

- Run `python scripts/build.py samples/family_dental_clinic.yaml`.
- Run `python scripts/export_binder_index.py samples/family_dental_clinic.yaml`.
- Run both import scripts against example CSVs if those examples changed.
- Run `python scripts/validate_content.py`.
- Run `python -m unittest discover -s tests`.
- Confirm examples do not include patient names, MRNs, DOBs, diagnoses, claim contents, clinical notes, passwords, API keys, tokens, private keys, private URLs, presigned links, full contracts, or real incident details.

## Checked-in demo artifacts

The checked-in public snapshot lives in [`demo/`](demo/). It should include:

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
