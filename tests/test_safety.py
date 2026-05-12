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


if __name__ == "__main__":
    unittest.main()
