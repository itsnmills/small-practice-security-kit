from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class StaticIntakeWorkspaceTests(unittest.TestCase):
    def test_all_non_incident_sections_have_playbooks(self) -> None:
        html = (ROOT / "small_practice_security_kit" / "static" / "intake.html").read_text(encoding="utf-8")
        js = (ROOT / "small_practice_security_kit" / "static" / "intake.js").read_text(encoding="utf-8")

        for section in [
            "start",
            "basics",
            "systems",
            "connectors",
            "vendors",
            "flows",
            "readiness",
            "ai",
            "downtime",
            "evidence",
            "generate",
        ]:
            self.assertIn(f'data-playbook="{section}"', html)
            self.assertIn(f"{section}:", js)

        self.assertIn("SECTION_PLAYBOOKS", js)
        self.assertIn("renderSectionPlaybooks", js)
        self.assertIn("sourceAlignment", js)
        self.assertIn("Do not enter", js)

    def test_high_value_sections_have_live_command_summaries(self) -> None:
        html = (ROOT / "small_practice_security_kit" / "static" / "intake.html").read_text(encoding="utf-8")
        js = (ROOT / "small_practice_security_kit" / "static" / "intake.js").read_text(encoding="utf-8")
        css = (ROOT / "small_practice_security_kit" / "static" / "intake.css").read_text(encoding="utf-8")

        for element_id in [
            "basics-command",
            "systems-command",
            "vendors-command",
            "flows-command",
            "readiness-command",
            "ai-command",
            "downtime-command",
            "evidence-command",
            "packet-command",
        ]:
            self.assertIn(f'id="{element_id}"', html)

        for function_name in [
            "renderBasicsCommand",
            "renderSystemsCommand",
            "renderVendorsCommand",
            "renderFlowsCommand",
            "renderReadinessCommand",
            "renderAICommand",
            "renderDowntimeCommand",
            "renderEvidenceCommand",
            "renderPacketCommand",
        ]:
            self.assertIn(function_name, js)

        self.assertIn(".service-brief", css)
        self.assertIn(".owner-command", css)
        self.assertIn(".command-metric.needs-work", css)

    def test_workspace_standard_document_exists(self) -> None:
        standard = (ROOT / "docs" / "product" / "local-intake-workspace-standard.md").read_text(encoding="utf-8")
        self.assertIn("Section Pattern", standard)
        self.assertIn("Command Summaries", standard)
        self.assertIn("Product Rules", standard)


if __name__ == "__main__":
    unittest.main()
