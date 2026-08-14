from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class BuildTests(unittest.TestCase):
    def test_build_creates_review_packet(self) -> None:
        subprocess.run([sys.executable, "scripts/build.py", "samples/family_dental_clinic.yaml"], cwd=ROOT, check=True)
        packet = ROOT / "out" / "family_dental_clinic" / "review-packet.md"
        text = packet.read_text(encoding="utf-8")
        self.assertIn("Readiness Review", text)
        self.assertIn("ePHI Flow Map", text)
        self.assertIn("Patient Data Outside the EHR", text)
        self.assertIn("Never touches the EHR", text)
        self.assertIn("Vendor and BAA Review", text)
        self.assertIn("AI Workflow Review", text)
        self.assertIn("External Evidence Pre-Check", text)
        self.assertIn("Incident Evidence Timeline", text)
        self.assertIn("Incident After-Action Report", text)
        self.assertIn("Guided Phase Checklist", text)
        self.assertIn("Owner/MSP Call Sheet", text)
        self.assertIn("Owner Review Agenda", text)
        self.assertIn("Evidence Closeout Queue", text)
        self.assertIn("Still open:", text)
        self.assertIn("Needs attention", text)
        self.assertIn("Evidence Lifecycle", text)
        self.assertIn("30-60-90 Roadmap", text)
        self.assertTrue((ROOT / "out" / "family_dental_clinic" / "incident-evidence-timeline.md").exists())
        self.assertTrue((ROOT / "out" / "family_dental_clinic" / "incident-after-action-report.md").exists())
        self.assertTrue((ROOT / "out" / "family_dental_clinic" / "external-evidence-precheck.md").exists())
        html = (ROOT / "out" / "family_dental_clinic" / "review-packet.html").read_text(encoding="utf-8")
        self.assertIn("Small Practice Security Kit", html)
        self.assertNotIn("Velari Security Kit", html)
        self.assertIn("Incident Evidence Timeline", html)
        self.assertIn("Never touches the EHR", html)
        self.assertIn("This week", html)
        self.assertIn("cannot show", html)
        self.assertIn('class="toc"', html)
        self.assertIn("print-footer", html)
        self.assertIn("@page", html)
        self.assertIn("<table>", html)
        self.assertIn("print", html)

    def test_validate_content_passes(self) -> None:
        subprocess.run([sys.executable, "scripts/build.py", "samples/family_dental_clinic.yaml"], cwd=ROOT, check=True)
        subprocess.run([sys.executable, "scripts/validate_content.py"], cwd=ROOT, check=True)


if __name__ == "__main__":
    unittest.main()
