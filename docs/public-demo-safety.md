# Public Demo Safety

Public demos must be fictional and PHI-avoidant.

Before publishing:

- Run `python scripts/build.py samples/family_dental_clinic.yaml`.
- Run `python scripts/export_binder_index.py samples/family_dental_clinic.yaml`.
- Run both import scripts against example CSVs.
- Run `python scripts/validate_content.py`.
- Confirm examples do not include patient names, MRNs, DOBs, diagnoses, claim contents, passwords, API keys, tokens, private keys, or real incident details.

