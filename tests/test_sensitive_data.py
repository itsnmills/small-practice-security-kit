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

    def test_labeled_patient_names_block(self) -> None:
        for text in ["Patient Name: John Smith", "Patient: John Smith", "patient name John"]:
            findings = blocking_findings({"note": text})
            self.assertTrue(any(finding.rule_id == "patient_name_label" for finding in findings), text)

    def test_patient_prose_does_not_block(self) -> None:
        findings = blocking_findings({"note": "No patient data required for the intake portal."})
        self.assertFalse(any(finding.rule_id == "patient_name_label" for finding in findings))

    def test_ssn_variants_block(self) -> None:
        for text in ["123-45-6789", "123 45 6789", "SSN: 123456789", "SSN 123 45 6789"]:
            findings = blocking_findings({"note": text})
            self.assertTrue(any(finding.rule_id in {"ssn", "ssn_label"} for finding in findings), text)

    def test_integer_ssn_and_dict_key_are_scanned(self) -> None:
        self.assertTrue(blocking_findings({"ssn": 123456789}))
        self.assertTrue(blocking_findings({"John Smith DOB: 1/2/1990": {"nested": "x"}}))

    def test_labeled_generic_secret_blocks(self) -> None:
        findings = blocking_findings({"note": "api_key: fake.value.for.test"})
        self.assertTrue(any(finding.rule_id == "labeled_secret" for finding in findings))

    def test_basic_prose_is_not_a_credential(self) -> None:
        findings = blocking_findings({"note": "Staff need a basic understanding of the downtime plan."})
        self.assertFalse(any(finding.rule_id == "bearer_or_basic_auth" for finding in findings))

    def test_bearer_token_still_blocks(self) -> None:
        findings = blocking_findings({"note": "Authorization: Bearer abc123def456ghi789"})
        self.assertTrue(any(finding.rule_id == "bearer_or_basic_auth" for finding in findings))


if __name__ == "__main__":
    unittest.main()
