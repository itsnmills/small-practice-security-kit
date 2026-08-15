from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from small_practice_security_kit.exchange import EXCHANGE_FIELDS, ExchangeRecord, csv_safe, markdown_cell, records_from_csv, records_to_csv, records_to_markdown


class ExchangeTests(unittest.TestCase):
    def test_exchange_csv_headers_are_stable(self) -> None:
        record = ExchangeRecord(
            source_repo="repo",
            source_artifact="artifact.csv",
            item_id="ITEM-1",
            module="module",
            title="Title",
            status="imported",
            risk="high",
            owner="Owner",
            evidence_needed="Evidence",
            evidence_reference="restricted-evidence/example.md",
            source_mapping="HIPAA Security Rule",
            next_review_due="not_scheduled",
            notes="Notes",
        )
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "records.csv"
            records_to_csv([record], path)
            first_line = path.read_text(encoding="utf-8").splitlines()[0]
            self.assertEqual(first_line.split(","), EXCHANGE_FIELDS)
            loaded = records_from_csv(path)
            self.assertEqual(loaded[0].item_id, "ITEM-1")

    def test_csv_safe_neutralizes_formula_prefixes(self) -> None:
        for payload in ["=HYPERLINK(\"http://evil\")", "+1+1", "-2+3", "@SUM(A1)", "\tcmd", "\rcmd"]:
            self.assertEqual(csv_safe(payload), "'" + payload)
        self.assertEqual(csv_safe("Plain title"), "Plain title")

    def test_exported_csv_and_markdown_neutralize_injection(self) -> None:
        record = ExchangeRecord(
            source_repo="repo",
            source_artifact="artifact.csv",
            item_id="ITEM-1",
            module="module",
            title="=HYPERLINK(\"http://evil\")",
            status="imported",
            risk="high",
            owner="Owner | signed",
            evidence_needed="Evidence",
            evidence_reference="restricted-evidence/example.md",
            source_mapping="HIPAA Security Rule",
            next_review_due="not_scheduled",
            notes="Notes",
        )
        with tempfile.TemporaryDirectory() as temp:
            csv_path = Path(temp) / "records.csv"
            records_to_csv([record], csv_path)
            self.assertIn("'=HYPERLINK", csv_path.read_text(encoding="utf-8"))
            md_path = Path(temp) / "records.md"
            records_to_markdown([record], md_path, "Title")
            self.assertIn("Owner \\| signed", md_path.read_text(encoding="utf-8"))

    def test_markdown_cell_escapes_pipes_and_newlines(self) -> None:
        self.assertEqual(markdown_cell("a|b"), "a\\|b")
        self.assertEqual(markdown_cell("a\nb"), "a b")


if __name__ == "__main__":
    unittest.main()
