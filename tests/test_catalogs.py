from __future__ import annotations

import unittest
from pathlib import Path

from small_practice_security_kit.catalogs import evidence_types, flow_templates, presets, size_tiers, systems, vendors
from small_practice_security_kit.control_evidence import load_control_evidence_catalog, validate_control_evidence_row


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

    def test_control_evidence_matrix_regulatory_citations(self) -> None:
        controls = load_control_evidence_catalog()
        self.assertEqual(len(controls), 30)

        valid_nist_sections = {"§ 3", "§ 4", "§ 5.1", "§ 5.2", "§ 5.3", "§ 5.4", "§ 5.5"}

        for control in controls:
            cid = control["control_id"]
            with self.subTest(control_id=cid):
                validate_control_evidence_row(control)
                refs = control.get("control_refs", [])
                self.assertGreaterEqual(len(refs), 3, f"{cid} has fewer than 3 citations")

                # Verify 45 CFR citation with Required / Addressable designation
                has_cfr = any("45 CFR § 164." in ref and ("(Required)" in ref or "(Addressable)" in ref) for ref in refs)
                self.assertTrue(has_cfr, f"{cid} missing required/addressable 45 CFR § 164 citation in {refs}")

                # Specifically verify Termination Procedures is marked Addressable (H2 finding)
                if cid == "VEL-OFFBOARDING-001":
                    offboarding_cfr = [r for r in refs if "45 CFR § 164.308(a)(3)(ii)(C)" in r][0]
                    self.assertIn("(Addressable)", offboarding_cfr)
                    self.assertNotIn("(Required)", offboarding_cfr)

                # Verify Workforce Training includes Addressable specifications
                if cid == "VEL-WORKFORCE-TRAIN-001":
                    training_cfr = [r for r in refs if "45 CFR § 164.308(a)(5)" in r][0]
                    self.assertIn("(Addressable)", training_cfr)

                # Verify NIST SP 800-66r2 sections align with Publication Structure (H3 finding)
                nist_refs = [r for r in refs if "NIST SP 800-66r2" in r]
                for n_ref in nist_refs:
                    has_valid_sec = any(sec in n_ref for sec in valid_nist_sections)
                    self.assertTrue(has_valid_sec, f"{cid} has invalid NIST SP 800-66r2 section: {n_ref}")

                # Verify HHS 405(d) HICP references align with 10 Core Practices (H4 finding)
                has_hicp = any("HHS 405(d) HICP" in ref for ref in refs)
                self.assertTrue(has_hicp, f"{cid} missing HHS 405(d) HICP reference in {refs}")


if __name__ == "__main__":
    unittest.main()
