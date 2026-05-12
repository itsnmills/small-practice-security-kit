# ePHI Data Flow Mapper Integration

This integration imports CSV flow rows into a practice profile.

Command:

```bash
python scripts/import_ephi_flows.py examples/imports/ephi-data-flow-mapper/flows.csv --base samples/family_dental_clinic.yaml --output out/family_dental_clinic/imported-ephi-profile.yaml
```

Required columns:

- `id`
- `source`
- `destination`
- `ephi_type`
- `vendor`
- `transmission`
- `baa_needed`
- `risk`
- `evidence_needed`

Imported flows appear in `ephi-flow-map.md` after building the imported profile.

