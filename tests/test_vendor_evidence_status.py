from __future__ import annotations

import copy
import unittest
from pathlib import Path

from small_practice_security_kit.offering import render_vendor_baa_ai_questionnaire
from small_practice_security_kit.packet import vendor_review
from small_practice_security_kit.profile import load_profile


ROOT = Path(__file__).resolve().parents[1]


class VendorEvidenceStatusTests(unittest.TestCase):
    def setUp(self) -> None:
        self.profile = load_profile(ROOT / "samples" / "family_dental_clinic.yaml")

    def test_vendor_review_includes_explicit_soc2_and_hitrust_statuses(self) -> None:
        profile = copy.deepcopy(self.profile)
        profile["vendors"][0]["soc2_status"] = "provided in private binder"
        profile["vendors"][0]["hitrust_status"] = "absent"

        text = vendor_review(profile)

        self.assertIn("SOC 2 Status", text)
        self.assertIn("HITRUST Status", text)
        self.assertIn("provided in private binder", text)
        self.assertIn("absent", text)

    def test_vendor_review_defaults_missing_attestation_statuses_to_not_provided(self) -> None:
        profile = copy.deepcopy(self.profile)
        del profile["vendors"][0]["soc2_status"]
        del profile["vendors"][0]["hitrust_status"]

        text = vendor_review(profile)

        self.assertIn("not provided", text)

    def test_sprint_questionnaire_includes_soc2_and_hitrust_statuses(self) -> None:
        text = render_vendor_baa_ai_questionnaire(self.profile, {})

        self.assertIn("SOC 2 status", text)
        self.assertIn("HITRUST status", text)
        self.assertIn("not provided", text)


if __name__ == "__main__":
    unittest.main()
