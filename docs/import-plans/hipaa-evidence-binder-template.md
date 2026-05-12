# HIPAA Evidence Binder Template Integration

This integration exports evidence needs from the Small Practice Security Kit into files that can be copied into or reviewed alongside `hipaa-evidence-binder-template`.

Command:

```bash
python scripts/export_binder_index.py samples/family_dental_clinic.yaml
```

Outputs:

- `evidence-binder-index.csv`
- `evidence-binder-index.md`
- `binder-import-notes.md`
- `exchange-records.csv`
- `exchange-records.md`

The export contains evidence references and expected evidence items. It does not include PHI, secrets, credentials, or raw evidence files.

