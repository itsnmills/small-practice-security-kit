from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from small_practice_security_kit.demo_export import export_demo
from small_practice_security_kit.safety import scan_tree


ROOT = Path(__file__).resolve().parents[1]


class DemoExportTests(unittest.TestCase):
    def test_export_demo_writes_packet_and_binder_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "demo"
            result = export_demo(ROOT / "samples" / "family_dental_clinic.yaml", output, include_screenshot=False)
            names = {path.relative_to(output).as_posix() for path in result.artifacts}
            self.assertIn("review-packet.md", names)
            self.assertIn("review-packet.html", names)
            self.assertIn("packet-manifest.json", names)
            self.assertIn("sprint-summary.json", names)
            self.assertIn("risk-register.csv", names)
            self.assertIn("handoff-actions.csv", names)
            self.assertIn("connector-evidence-summary.json", names)
            self.assertIn("owner-action-plan.md", names)
            self.assertIn("msp-remediation-brief.md", names)
            self.assertIn("vendor-baa-ai-questionnaire.md", names)
            self.assertIn("evidence-collection-checklist.md", names)
            self.assertIn("evidence-binder-export/evidence-binder-index.csv", names)
            self.assertIn("evidence-binder-export/exchange-records.md", names)
            self.assertFalse(scan_tree(output))


if __name__ == "__main__":
    unittest.main()
