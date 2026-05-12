from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from small_practice_security_kit.adapters.ephi_mapper import import_flows, read_flow_csv
from small_practice_security_kit.profile import load_profile
from small_practice_security_kit.validation import ValidationError


ROOT = Path(__file__).resolve().parents[1]


class EphiImportTests(unittest.TestCase):
    def test_valid_import_replaces_flows(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "profile.yaml"
            import_flows(
                ROOT / "examples" / "imports" / "ephi-data-flow-mapper" / "flows.csv",
                ROOT / "samples" / "family_dental_clinic.yaml",
                output,
            )
            profile = load_profile(output)
            self.assertEqual(len(profile["flows"]), 3)
            self.assertEqual(profile["flows"][0]["id"], "FLOW-101")
            self.assertTrue((output.parent / "ephi-flow-import" / "exchange-records.csv").exists())

    def test_append_mode_keeps_existing_flows(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "profile.yaml"
            import_flows(
                ROOT / "examples" / "imports" / "ephi-data-flow-mapper" / "flows.csv",
                ROOT / "samples" / "family_dental_clinic.yaml",
                output,
                append=True,
            )
            profile = load_profile(output)
            self.assertGreater(len(profile["flows"]), 3)

    def test_missing_column_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "bad.csv"
            path.write_text("id,source\nFLOW-1,A\n", encoding="utf-8")
            with self.assertRaisesRegex(ValidationError, "missing required column"):
                read_flow_csv(path)


if __name__ == "__main__":
    unittest.main()
