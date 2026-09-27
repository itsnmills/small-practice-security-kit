from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from small_practice_security_kit.safety import find_sensitive_patterns, scan_tree


class SafetyTests(unittest.TestCase):
    def test_phi_like_pattern_is_detected(self) -> None:
        self.assertTrue(find_sensitive_patterns("Patient Name: Jane Example"))

    def test_secret_like_pattern_is_detected(self) -> None:
        self.assertTrue(find_sensitive_patterns("api_key = abcdefghijklmnop"))

    def test_scan_tree_reports_sensitive_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "bad.md"
            path.write_text("DOB: 01/02/1970\n", encoding="utf-8")
            self.assertTrue(scan_tree(Path(temp)))

    def test_scan_tree_flags_unscannable_file_types(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "patients.log"
            path.write_text("SSN 123-45-6789\n", encoding="utf-8")
            findings = scan_tree(Path(temp))
            self.assertTrue(any("unscannable file type" in finding for finding in findings))

    def test_scan_tree_allows_rendered_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            (Path(temp) / "review-packet.png").write_bytes(b"\x89PNG\r\n")
            (Path(temp) / "review-packet.pdf").write_bytes(b"%PDF-1.4")
            self.assertEqual(scan_tree(Path(temp)), [])

    def test_scan_tree_flags_undecodable_text_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            (Path(temp) / "notes.txt").write_bytes(b"\xff\xfe\x00bad")
            findings = scan_tree(Path(temp))
            self.assertTrue(any("not valid UTF-8" in finding for finding in findings))


if __name__ == "__main__":
    unittest.main()
