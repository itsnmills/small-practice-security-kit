from __future__ import annotations

import copy
import unittest
from pathlib import Path

from small_practice_security_kit.profile import load_profile
from small_practice_security_kit.validation import ValidationError, validate_profile


ROOT = Path(__file__).resolve().parents[1]


class ProfileValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.profile = load_profile(ROOT / "samples" / "family_dental_clinic.yaml")

    def test_valid_sample_profile_passes(self) -> None:
        validate_profile(self.profile)

    def test_missing_top_level_section_fails(self) -> None:
        profile = copy.deepcopy(self.profile)
        del profile["flows"]
        with self.assertRaisesRegex(ValidationError, "flows"):
            validate_profile(profile)

    def test_missing_nested_field_fails(self) -> None:
        profile = copy.deepcopy(self.profile)
        del profile["vendors"][0]["baa_status"]
        with self.assertRaisesRegex(ValidationError, "baa_status"):
            validate_profile(profile)

    def test_invalid_risk_fails(self) -> None:
        profile = copy.deepcopy(self.profile)
        profile["flows"][0]["risk"] = "spicy"
        with self.assertRaisesRegex(ValidationError, "risk"):
            validate_profile(profile)

    def test_invalid_ai_decision_fails(self) -> None:
        profile = copy.deepcopy(self.profile)
        profile["ai_workflows"][0]["decision"] = "maybe"
        with self.assertRaisesRegex(ValidationError, "decision"):
            validate_profile(profile)


if __name__ == "__main__":
    unittest.main()
