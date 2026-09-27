from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from small_practice_security_kit.adapters.vendor_risk import import_vendors, read_vendor_csv
from small_practice_security_kit.profile import load_profile
from small_practice_security_kit.validation import ValidationError


ROOT = Path(__file__).resolve().parents[1]


class VendorImportTests(unittest.TestCase):
    def test_valid_import_replaces_vendors(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "profile.yaml"
            import_vendors(
                ROOT / "examples" / "imports" / "vendor-risk-manager" / "vendor_register.csv",
                ROOT / "samples" / "family_dental_clinic.yaml",
                output,
            )
            profile = load_profile(output)
            self.assertEqual(len(profile["vendors"]), 3)
            self.assertEqual(profile["vendors"][0]["name"], "Example EHR Vendor")
            self.assertTrue((output.parent / "vendor-register-import" / "exchange-records.csv").exists())

    def test_append_mode_keeps_existing_vendors(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "profile.yaml"
            import_vendors(
                ROOT / "examples" / "imports" / "vendor-risk-manager" / "vendor_register.csv",
                ROOT / "samples" / "family_dental_clinic.yaml",
                output,
                append=True,
            )
            profile = load_profile(output)
            self.assertGreater(len(profile["vendors"]), 3)

    def test_import_blocks_sensitive_data_in_csv(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "leaky.csv"
            path.write_text(
                "name,service,touches_ephi,baa_status,ai_training_use,subcontractors_known,incident_notification_terms,risk\n"
                "Billing Vendor,Billing SSN 123-45-6789,yes,unknown,unknown,unknown,unknown,high\n",
                encoding="utf-8",
            )
            output = Path(temp) / "profile.yaml"
            with self.assertRaisesRegex(ValueError, "blocked sensitive data"):
                import_vendors(path, ROOT / "samples" / "family_dental_clinic.yaml", output)
            self.assertFalse(output.exists())

    def test_missing_column_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "bad.csv"
            path.write_text("name,service\nVendor,Service\n", encoding="utf-8")
            with self.assertRaisesRegex(ValidationError, "missing required column"):
                read_vendor_csv(path)

    def test_import_defaults_missing_attestation_columns_to_not_provided(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "legacy.csv"
            path.write_text(
                "name,service,touches_ephi,baa_status,ai_training_use,subcontractors_known,incident_notification_terms,risk\n"
                "Legacy Vendor,Claims,yes,unknown,unknown,unknown,unknown,high\n",
                encoding="utf-8",
            )

            vendors = read_vendor_csv(path)

        self.assertEqual(vendors[0]["soc2_status"], "not provided")
        self.assertEqual(vendors[0]["hitrust_status"], "not provided")


if __name__ == "__main__":
    unittest.main()
