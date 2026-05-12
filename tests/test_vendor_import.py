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

    def test_missing_column_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "bad.csv"
            path.write_text("name,service\nVendor,Service\n", encoding="utf-8")
            with self.assertRaisesRegex(ValidationError, "missing required column"):
                read_vendor_csv(path)


if __name__ == "__main__":
    unittest.main()
