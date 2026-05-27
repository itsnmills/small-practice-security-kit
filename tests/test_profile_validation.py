from __future__ import annotations

import copy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

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

    def test_missing_vendor_attestation_status_fails(self) -> None:
        profile = copy.deepcopy(self.profile)
        del profile["vendors"][0]["soc2_status"]
        with self.assertRaisesRegex(ValidationError, "soc2_status"):
            validate_profile(profile)

    def test_invalid_risk_fails(self) -> None:
        profile = copy.deepcopy(self.profile)
        profile["flows"][0]["risk"] = "spicy"
        with self.assertRaisesRegex(ValidationError, "risk"):
            validate_profile(profile)

    def test_invalid_boolean_fails(self) -> None:
        profile = copy.deepcopy(self.profile)
        profile["readiness"]["mfa_email"] = "yes"
        with self.assertRaisesRegex(ValidationError, "readiness.mfa_email"):
            validate_profile(profile)

    def test_invalid_type_fails(self) -> None:
        profile = copy.deepcopy(self.profile)
        profile["practice"]["staff_count"] = "fourteen"
        with self.assertRaisesRegex(ValidationError, "practice.staff_count"):
            validate_profile(profile)

    def test_invalid_ai_decision_fails(self) -> None:
        profile = copy.deepcopy(self.profile)
        profile["ai_workflows"][0]["decision"] = "maybe"
        with self.assertRaisesRegex(ValidationError, "decision"):
            validate_profile(profile)

    def test_invalid_incident_timeline_item_fails(self) -> None:
        profile = copy.deepcopy(self.profile)
        del profile["incident_timeline"]["timeline"][0]["evidence_ref"]
        with self.assertRaisesRegex(ValidationError, "evidence_ref"):
            validate_profile(profile)

    def test_cli_exits_nonzero_on_invalid_profile(self) -> None:
        profile = copy.deepcopy(self.profile)
        del profile["practice"]
        with tempfile.TemporaryDirectory() as temp:
            invalid_path = Path(temp) / "invalid-profile.yaml"
            invalid_path.write_text(yaml.safe_dump(profile), encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, "-m", "small_practice_security_kit", "validate", str(invalid_path)],
                cwd=ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            )
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("profile", completed.stderr)
        self.assertIn("practice", completed.stderr)


if __name__ == "__main__":
    unittest.main()
