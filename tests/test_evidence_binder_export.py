from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

from small_practice_security_kit.adapters.evidence_binder import BINDER_FIELDS, export_binder_index
from small_practice_security_kit.safety import scan_tree


ROOT = Path(__file__).resolve().parents[1]


class EvidenceBinderExportTests(unittest.TestCase):
    def test_export_writes_expected_files_and_rows(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            out = export_binder_index(ROOT / "samples" / "family_dental_clinic.yaml", Path(temp))
            csv_path = out / "evidence-binder-index.csv"
            with csv_path.open(encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(list(rows[0].keys()), BINDER_FIELDS)
            ids = {row["evidence_id"] for row in rows}
            self.assertIn("ACCESS-QTR", ids)
            self.assertIn("BACKUP-RESTORE", ids)
            self.assertIn("AI-POLICY", ids)
            self.assertTrue((out / "evidence-binder-index.md").exists())
            self.assertTrue((out / "binder-import-notes.md").exists())
            self.assertFalse(scan_tree(out))


if __name__ == "__main__":
    unittest.main()
