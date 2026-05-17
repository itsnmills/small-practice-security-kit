from __future__ import annotations

import unittest

from small_practice_security_kit.catalogs import evidence_types, flow_templates, presets, size_tiers, systems, vendors


class CatalogTests(unittest.TestCase):
    def test_catalogs_include_healthcare_defaults(self) -> None:
        self.assertIn("dental", presets())
        self.assertIn("primary_care", presets())
        self.assertIn("behavioral_health", presets())
        self.assertIn("telehealth", presets())
        self.assertIn("small_lab", presets())
        self.assertIn("billing_rcm", presets())
        self.assertIn("small", size_tiers())
        self.assertIn("ehr", systems())
        self.assertIn("billing", systems())
        self.assertIn("public_ai", systems())
        self.assertIn("ehr_vendor", vendors())
        self.assertIn("signed_baa", evidence_types())
        self.assertTrue(any(flow["key"] == "ehr_to_billing" for flow in flow_templates()))

    def test_system_catalog_items_have_required_intake_fields(self) -> None:
        required = {"name", "category", "description", "ephi_role", "vendor_category", "evidence_needed", "baa_likely", "risk"}
        for key, item in systems().items():
            with self.subTest(system=key):
                self.assertTrue(required.issubset(item))
                self.assertIn(item["vendor_category"], vendors())

    def test_vendor_catalog_items_have_explicit_attestation_statuses(self) -> None:
        required = {"soc2_status", "hitrust_status"}
        for key, item in vendors().items():
            with self.subTest(vendor=key):
                self.assertTrue(required.issubset(item))
                self.assertTrue(str(item["soc2_status"]).strip())
                self.assertTrue(str(item["hitrust_status"]).strip())


if __name__ == "__main__":
    unittest.main()
