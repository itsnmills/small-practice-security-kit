from __future__ import annotations

import unittest
from pathlib import Path

from small_practice_security_kit.packet import _parse_table, render_html, table
from small_practice_security_kit.profile import load_profile

ROOT = Path(__file__).resolve().parents[1]


class PacketRenderTests(unittest.TestCase):
    def test_table_escapes_pipes_and_newlines(self) -> None:
        markdown = table(["Vendor", "BAA"], [["Evil Corp | signed", "missing\nreview"]])
        row = markdown.splitlines()[2]
        self.assertEqual(row, "| Evil Corp \\| signed | missing review |")

    def test_parse_table_keeps_escaped_pipe_in_one_cell(self) -> None:
        markdown = table(["Vendor", "BAA"], [["Evil Corp | signed", "missing"]])
        parsed = _parse_table(markdown.splitlines())
        self.assertEqual(parsed[1], ["Evil Corp | signed", "missing"])

    def test_parse_table_keeps_dash_data_rows(self) -> None:
        markdown = table(["A", "B"], [["-", ""]])
        parsed = _parse_table(markdown.splitlines())
        self.assertEqual(len(parsed), 2)

    def test_render_html_closes_packet_sections(self) -> None:
        profile = load_profile(ROOT / "samples" / "family_dental_clinic.yaml")
        html_out = render_html("# One\n\ntext\n\n# Two\n\nmore\n", profile)
        self.assertEqual(html_out.count("<section"), html_out.count("</section>"))


if __name__ == "__main__":
    unittest.main()
