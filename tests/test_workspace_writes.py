from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

from small_practice_security_kit.suggestions import create_profile_from_preset
from small_practice_security_kit.workspaces import WorkspaceError, atomic_write_profile, safe_profile_path


class WorkspaceWriteTests(unittest.TestCase):
    def test_atomic_write_profile_writes_under_profiles_and_logs_without_values(self) -> None:
        profile = create_profile_from_preset("Workspace Test Clinic", "dental", "solo")
        with tempfile.TemporaryDirectory(prefix="spsk-workspace-write-") as temp:
            workspace_root = Path(temp).resolve()
            path = safe_profile_path(profile["practice"]["name"], root=workspace_root)
            atomic_write_profile(
                profile,
                path,
                root=workspace_root,
                action="test",
                warnings=[{"rule_id": "patient_name_label", "path": "x", "message": "redacted"}],
            )
            self.assertTrue(path.exists())
            self.assertEqual(path.parent.resolve(), workspace_root / "profiles")
            log = (workspace_root / "profiles" / ".logs" / "profile_changes.jsonl").read_text(encoding="utf-8")
            self.assertIn("patient_name_label", log)
            self.assertNotIn("redacted", log)

    def test_atomic_write_cleans_up_tmp_file_on_failure(self) -> None:
        profile = create_profile_from_preset("Tmp Cleanup Clinic", "dental", "solo")
        with tempfile.TemporaryDirectory(prefix="spsk-workspace-cleanup-") as temp:
            workspace_root = Path(temp).resolve()
            path = safe_profile_path(profile["practice"]["name"], root=workspace_root)
            with mock.patch("small_practice_security_kit.workspaces.os.replace", side_effect=OSError("disk full")):
                with self.assertRaises(OSError):
                    atomic_write_profile(profile, path, root=workspace_root, action="test")
            self.assertEqual(list((workspace_root / "profiles").glob("*.tmp")), [])
            self.assertEqual(list((workspace_root / "profiles").glob(".*.tmp")), [])
            self.assertFalse(path.exists())

    def test_atomic_write_cleans_up_tmp_file_on_dump_exception(self) -> None:
        profile = create_profile_from_preset("Dump Fail Clinic", "dental", "solo")
        with tempfile.TemporaryDirectory(prefix="spsk-workspace-dump-fail-") as temp:
            workspace_root = Path(temp).resolve()
            path = safe_profile_path(profile["practice"]["name"], root=workspace_root)
            with mock.patch("yaml.safe_dump", side_effect=RuntimeError("serialization aborted")):
                with self.assertRaises(RuntimeError):
                    atomic_write_profile(profile, path, root=workspace_root, action="test")
            self.assertEqual(list((workspace_root / "profiles").glob("*.tmp")), [])
            self.assertEqual(list((workspace_root / "profiles").glob(".*.tmp")), [])
            self.assertFalse(path.exists())

    def test_atomic_write_rejects_outside_profiles(self) -> None:
        profile = create_profile_from_preset("Outside Test Clinic", "dental", "solo")
        with tempfile.TemporaryDirectory(prefix="spsk-workspace-write-") as temp:
            with self.assertRaises(WorkspaceError):
                atomic_write_profile(profile, Path(temp) / "outside.yaml", root=Path(temp) / "workspace", action="bad")

    def test_rapid_sequential_writes_generate_distinct_backups(self) -> None:
        profile = create_profile_from_preset("Rapid Write Clinic", "dental", "solo")
        with tempfile.TemporaryDirectory(prefix="spsk-workspace-rapid-") as temp:
            workspace_root = Path(temp).resolve()
            path = safe_profile_path(profile["practice"]["name"], root=workspace_root)
            atomic_write_profile(profile, path, root=workspace_root, action="seed")
            # Write twice in immediate succession
            atomic_write_profile(profile, path, root=workspace_root, action="update-1")
            atomic_write_profile(profile, path, root=workspace_root, action="update-2")
            backups = list((workspace_root / "profiles" / ".backups").glob("*.yaml"))
            self.assertEqual(len(backups), 2)


if __name__ == "__main__":
    unittest.main()
