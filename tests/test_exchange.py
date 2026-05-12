from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from small_practice_security_kit.exchange import EXCHANGE_FIELDS, ExchangeRecord, records_from_csv, records_to_csv


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


if __name__ == "__main__":
    unittest.main()
