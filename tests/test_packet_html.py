from __future__ import annotations

import unittest
from pathlib import Path

from small_practice_security_kit.packet import (
    PACKET_KICKER,
    ephi_insight,
    heading_slug,
    joined_findings,
    readiness_insight,
    render_html,
    render_status_cell,
    render_table,
    vendor_insight,
    verdict,
)
from small_practice_security_kit.profile import load_profile


ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "samples" / "family_dental_clinic.yaml"


class PacketHtmlTests(unittest.TestCase):
    def test_heading_slug_is_stable_and_unique(self) -> None:
        used: dict[str, int] = {}
        self.assertEqual(heading_slug("ePHI Flow Map", used), "ephi_flow_map")
        self.assertEqual(heading_slug("ePHI Flow Map", used), "ephi_flow_map_2")

    def test_status_cells_become_chips(self) -> None:
        self.assertIn("chip-blocked", render_status_cell("No"))
        self.assertIn("chip-high", render_status_cell("high"))
        self.assertIn("chip-outside", render_status_cell("Never touches the EHR"))
        self.assertEqual(render_status_cell("Cloud EHR"), "Cloud EHR")

    def test_wide_table_marks_print_hide_columns(self) -> None:
        html = render_table(
            [
                "| Flow | Lane | Lifecycle | Closeout | Evidence Needed |",
                "| --- | --- | --- | --- | --- |",
                "| FLOW-001 | Never touches the EHR | Requested | Needs evidence | BAA |",
            ]
        )
        self.assertIn('class="print-hide"', html)
        self.assertIn("chip-outside", html)
        self.assertIn("chip-review", html)

    def test_insights_name_the_actual_gaps(self) -> None:
        profile = load_profile(SAMPLE)
        self.assertIn("Still open:", readiness_insight(profile))
        self.assertIn("EHR MFA", readiness_insight(profile))
        self.assertIn("email", ephi_insight(profile).casefold())
        self.assertIn("BAA", vendor_insight(profile))
        self.assertIn("cannot show", verdict(profile))
        self.assertIn("Example Billing Vendor", verdict(profile))
        paths = [item["path"] for item in joined_findings(profile)]
        self.assertTrue(any("Staff email" in path for path in paths))
        self.assertTrue(any("Shared Drive" in path or "Imaging" in path for path in paths))

    def test_wide_register_becomes_findings_not_a_table(self) -> None:
        html = render_table(
            [
                "| Vendor | Service | Touches ePHI? | BAA Status | AI Training Use | Incident Terms | Risk |",
                "| --- | --- | --- | --- | --- | --- | --- |",
                "| Example Billing | Claims | Yes | missing | unknown | unknown | high |",
            ]
        )
        self.assertIn('class="findings"', html)
        self.assertNotIn("<table>", html)

    def test_review_packet_cover_uses_honest_kicker(self) -> None:
        profile = load_profile(SAMPLE)
        html = render_html("# Readiness Review\n\nPractice: Family Dental Clinic\n", profile)
        self.assertIn(PACKET_KICKER, html)
        self.assertNotIn("Velari Security Kit", html)
        self.assertIn('class="toc"', html)
        self.assertIn('id="readiness_review"', html)
        self.assertIn("Never touches the EHR", html)
        self.assertIn("This week", html)
        self.assertIn("cannot show", html)
        self.assertIn("print-footer", html)
        self.assertIn("@page", html)
        self.assertIn("--green:", html)
        self.assertIn("--red:", html)


if __name__ == "__main__":
    unittest.main()
