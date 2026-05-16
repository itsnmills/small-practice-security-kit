from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

from small_practice_security_kit.profile import load_profile
from small_practice_security_kit.sprint import STAGE_ORDER, build_sprint


ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "samples" / "family_dental_clinic.yaml"
PHI_PLACEHOLDER_PATTERNS = [
    re.compile(r"Patient Name\s*:", re.IGNORECASE),
    re.compile(r"\bMRN\s*:", re.IGNORECASE),
    re.compile(r"\bDOB\s*:", re.IGNORECASE),
    re.compile(r"diagnosis\s*:", re.IGNORECASE),
    re.compile(r"Jane Doe", re.IGNORECASE),
]


class SprintModeTests(unittest.TestCase):
    def test_sprint_command_creates_required_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            output_root = Path(temp)
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "small_practice_security_kit",
                    "sprint",
                    "samples/family_dental_clinic.yaml",
                    "--output-root",
                    str(output_root),
                ],
                cwd=ROOT,
                check=True,
            )
            out_dir = output_root / "family_dental_clinic"
            for name in [
                "sprint-index.md",
                "sprint-summary.json",
                "risk-register.csv",
                "evidence-index.json",
                "handoff-actions.csv",
                "review-packet.md",
                "review-packet.html",
                "owner-msp-handoff.md",
                "30-60-90-roadmap.md",
                "packet-manifest.json",
                "evidence-binder-export/evidence-binder-index.csv",
            ]:
                path = out_dir / name
                self.assertTrue(path.exists(), name)
                self.assertGreater(path.stat().st_size, 0, name)

    def test_sprint_summary_has_expected_keys_and_stages(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            out_dir = build_sprint(PROFILE, Path(temp), generated_at="2026-05-16T00:00:00Z").output_dir
            summary = json.loads((out_dir / "sprint-summary.json").read_text(encoding="utf-8"))

        self.assertEqual(summary["schema_version"], "2026-05-16")
        self.assertEqual(summary["generator"]["mode"], "velari_sprint_mode_public_runner")
        self.assertEqual(summary["practice"]["label"], "Family Dental Clinic")
        self.assertFalse(summary["data_boundary"]["phi_allowed"])
        self.assertIn("outputs", summary)
        self.assertIn("counts", summary)
        self.assertIn("stage_statuses", summary)
        self.assertEqual([stage["id"] for stage in summary["stage_statuses"]], STAGE_ORDER)
        self.assertTrue(any(stage["status"] == "needs_evidence" for stage in summary["stage_statuses"]))
        for stage in summary["stage_statuses"]:
            self.assertIn("next_action", stage)
            self.assertTrue(stage["artifact_refs"])

    def test_risk_and_evidence_exports_are_reference_only(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            out_dir = build_sprint(PROFILE, Path(temp), generated_at="2026-05-16T00:00:00Z").output_dir
            with (out_dir / "risk-register.csv").open(encoding="utf-8") as handle:
                risk_rows = list(csv.DictReader(handle))
            evidence = json.loads((out_dir / "evidence-index.json").read_text(encoding="utf-8"))
            with (out_dir / "handoff-actions.csv").open(encoding="utf-8") as handle:
                handoff_rows = list(csv.DictReader(handle))
            combined = "\n".join(
                [
                    (out_dir / "sprint-index.md").read_text(encoding="utf-8"),
                    json.dumps(evidence, sort_keys=True),
                    json.dumps(risk_rows, sort_keys=True),
                    json.dumps(handoff_rows, sort_keys=True),
                ]
            )

        self.assertTrue(risk_rows)
        self.assertTrue(evidence["evidence_references"])
        self.assertTrue(handoff_rows)
        self.assertFalse(evidence["data_boundary"]["raw_evidence_allowed"])
        self.assertEqual(evidence["binder_export"]["share_safety"], "reference_only_no_phi_no_secret")
        for pattern in PHI_PLACEHOLDER_PATTERNS:
            self.assertIsNone(pattern.search(combined), pattern.pattern)

    def test_sprint_blocks_high_confidence_sensitive_profile_data(self) -> None:
        profile = load_profile(PROFILE)
        profile["handoff_questions"][0]["question"] = "MRN: A1234567"
        with tempfile.TemporaryDirectory() as temp:
            profile_path = Path(temp) / "bad.yaml"
            profile_path.write_text(yaml.safe_dump(profile, sort_keys=False), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "blocked sensitive data"):
                build_sprint(profile_path, Path(temp) / "out")


if __name__ == "__main__":
    unittest.main()
