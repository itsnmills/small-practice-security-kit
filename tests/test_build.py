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
        self.assertIn("Vendor and BAA Review", text)
        self.assertIn("AI Workflow Review", text)
        self.assertIn("30-60-90 Roadmap", text)
        html = (ROOT / "out" / "family_dental_clinic" / "review-packet.html").read_text(encoding="utf-8")
        self.assertIn("Velari Security Kit", html)
        self.assertIn("#050a10", html.lower())
        self.assertIn("#c9a84c", html.lower())
        self.assertIn("#dcc076", html.lower())
        self.assertIn("<table>", html)
        self.assertIn("print", html)

    def test_validate_content_passes(self) -> None:
        subprocess.run([sys.executable, "scripts/build.py", "samples/family_dental_clinic.yaml"], cwd=ROOT, check=True)
        subprocess.run([sys.executable, "scripts/validate_content.py"], cwd=ROOT, check=True)

    def test_docs_describe_existing_repo_imports(self) -> None:
        text = (ROOT / "docs" / "import-plans" / "existing-repos.md").read_text(encoding="utf-8")
        self.assertIn("hipaa-evidence-binder-template", text)
        self.assertIn("ephi-data-flow-mapper", text)
        self.assertIn("vendor-risk-manager", text)
        self.assertIn("health-ai-governance-auditor", text)


if __name__ == "__main__":
    unittest.main()
