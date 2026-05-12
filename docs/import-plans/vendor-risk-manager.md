# Vendor Risk Manager Integration

This integration imports a lightweight vendor register into a practice profile.

Command:

```bash
python scripts/import_vendor_register.py examples/imports/vendor-risk-manager/vendor_register.csv --base samples/family_dental_clinic.yaml --output out/family_dental_clinic/imported-vendor-profile.yaml
```

Required columns:

- `name`
- `service`
- `touches_ephi`
- `baa_status`
- `ai_training_use`
- `subcontractors_known`
- `incident_notification_terms`
- `risk`

Imported vendors appear in `vendor-baa-review.md` after building the imported profile.

