from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DashboardTests(unittest.TestCase):
    def test_build_only_creates_local_dashboard(self) -> None:
        subprocess.run(
            [
                sys.executable,
                "scripts/serve_dashboard.py",
                "--profile",
                "samples/family_dental_clinic.yaml",
                "--build-only",
            ],
            cwd=ROOT,
            check=True,
        )
        dashboard = ROOT / "out" / "family_dental_clinic" / "dashboard.html"
        text = dashboard.read_text(encoding="utf-8")
        self.assertIn("Owner dashboard", text)
        self.assertIn("ePHI flow map", text)
        self.assertIn("Vendor and BAA review", text)
        self.assertIn("AI workflow review", text)
        self.assertIn("Incident evidence timeline", text)
        self.assertIn("Evidence lifecycle and closeout", text)
        self.assertIn("Evidence closeout", text)
        self.assertIn("Needs evidence", text)
        self.assertIn("Local only", text)
        self.assertIn("review-packet.html", text)
        self.assertIn("30-60-90-roadmap.html", text)
        self.assertIn("incident-evidence-timeline.html", text)
        self.assertIn("incident-after-action-report.html", text)
        self.assertIn("evidence-binder-index.html", text)
        self.assertTrue((ROOT / "out" / "family_dental_clinic" / "30-60-90-roadmap.html").exists())
        self.assertTrue((ROOT / "out" / "family_dental_clinic" / "incident-evidence-timeline.html").exists())
        self.assertTrue((ROOT / "out" / "family_dental_clinic" / "incident-after-action-report.html").exists())
        self.assertTrue((ROOT / "out" / "family_dental_clinic" / "evidence-binder-index.html").exists())

    def test_serve_refuses_non_loopback_host(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "scripts/serve_dashboard.py",
                "--profile",
                "samples/family_dental_clinic.yaml",
                "--host",
                "0.0.0.0",
                "--port",
                "8766",
                "--no-open",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=20,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("loopback", result.stderr.lower())


if __name__ == "__main__":
    unittest.main()
