from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from small_practice_security_kit.file_inventory import FileInventoryError, inventory_folder, resolve_allowed_path


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

    def test_inventory_rejects_path_outside_allowed_roots(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(FileInventoryError):
                inventory_folder(Path("/etc"), allowed_roots=[Path(tmp)])

    def test_inventory_rejects_parent_segments(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaises(FileInventoryError):
                inventory_folder(root / "nested" / ".." / "etc", allowed_roots=[root])

    def test_resolve_allowed_path_rejects_etc_passwd(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(FileInventoryError):
                resolve_allowed_path("/etc/passwd", [Path(tmp)])

    def test_inventory_skips_symlink_escape(self) -> None:
        outside = Path("/etc/passwd")
        if not outside.exists():
            self.skipTest("no /etc/passwd")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "safe.txt").write_text("ok", encoding="utf-8")
            (root / "passwd.txt").symlink_to(outside)
            result = inventory_folder(root)
            self.assertEqual([item["reference"] for item in result["evidence"]], ["safe.txt"])
            self.assertTrue(any(item["reason"] == "outside inventory root" for item in result["skipped"]))


if __name__ == "__main__":
    unittest.main()
