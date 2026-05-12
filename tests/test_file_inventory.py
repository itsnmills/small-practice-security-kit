from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from small_practice_security_kit.file_inventory import FileInventoryError, inventory_folder


class FileInventoryTests(unittest.TestCase):
    def test_inventory_folder_imports_metadata_without_contents(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            evidence = root / "EHR_BAA.pdf"
            evidence.write_text("contract contents should not be copied", encoding="utf-8")
            result = inventory_folder(root)
            self.assertEqual(len(result["evidence"]), 1)
            item = result["evidence"][0]
            self.assertEqual(item["reference"], "EHR_BAA.pdf")
            self.assertIn("size_bytes", item["metadata"])
            self.assertNotIn("contract contents", str(item))

    def test_inventory_skips_sensitive_looking_filename(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "MRN_A1234567.pdf").write_text("x", encoding="utf-8")
            result = inventory_folder(root)
            self.assertEqual(result["evidence"], [])
            self.assertEqual(result["skipped"][0]["reason"], "sensitive-looking filename")

    def test_inventory_requires_directory(self) -> None:
        with self.assertRaises(FileInventoryError):
            inventory_folder(Path("/definitely/not/a/real/evidence/folder"))


if __name__ == "__main__":
    unittest.main()
