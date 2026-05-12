from __future__ import annotations

import unittest

from small_practice_security_kit.sensitive_data import blocking_findings, find_sensitive_data


class SensitiveDataTests(unittest.TestCase):
    def test_blocks_high_confidence_patient_and_secret_patterns(self) -> None:
        payload = {
            "notes": "MRN: A1234567",
            "secret": "-----BEGIN PRIVATE KEY-----",
            "dob": "DOB: 01/02/1980",
            "token": "sk-abcdefghijklmnopqrstuvwxyz123456",
        }
        findings = blocking_findings(payload)
        rule_ids = {finding.rule_id for finding in findings}
        self.assertIn("mrn_label", rule_ids)
        self.assertIn("private_key", rule_ids)
        self.assertIn("dob_label", rule_ids)
        self.assertIn("api_key", rule_ids)

    def test_warns_on_patient_name_label_without_logging_value(self) -> None:
        findings = find_sensitive_data({"note": "patient name John"})
        self.assertTrue(any(finding.rule_id == "patient_name_label" for finding in findings))
        self.assertTrue(all("John" not in finding.to_dict()["message"] for finding in findings))


if __name__ == "__main__":
    unittest.main()
