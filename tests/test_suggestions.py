from __future__ import annotations

import unittest

from small_practice_security_kit.suggestions import create_profile_from_preset, rebuild_profile_suggestions, suggest_flows
from small_practice_security_kit.validation import validate_profile


class SuggestionTests(unittest.TestCase):
    def test_create_profile_from_preset_is_valid_and_useful(self) -> None:
        profile = create_profile_from_preset("Test Dental Practice", "dental", "small")
        validate_profile(profile)
        self.assertEqual(profile["intake"]["preset"], "dental")
        self.assertGreaterEqual(len(profile["systems"]), 10)
        self.assertGreaterEqual(len(profile["vendors"]), 8)
        self.assertGreaterEqual(len(profile["flows"]), 5)
        self.assertGreaterEqual(len(profile["evidence"]), 3)
        self.assertTrue(any(workflow["decision"] == "prohibited" for workflow in profile["ai_workflows"]))

    def test_flow_suggestions_follow_selected_systems(self) -> None:
        flows = suggest_flows(["ehr", "billing", "clearinghouse", "email"])
        keys = {flow["key"] for flow in flows}
        self.assertIn("ehr_to_billing", keys)
        self.assertIn("billing_to_clearinghouse", keys)
        self.assertIn("email_referral", keys)

    def test_rebuild_profile_suggestions_refreshes_flows_and_evidence(self) -> None:
        profile = create_profile_from_preset("Test Practice", "telehealth", "solo")
        profile["flows"] = []
        profile["evidence"] = []
        rebuilt = rebuild_profile_suggestions(profile)
        self.assertGreater(len(rebuilt["flows"]), 0)
        self.assertGreater(len(rebuilt["evidence"]), 0)


if __name__ == "__main__":
    unittest.main()
