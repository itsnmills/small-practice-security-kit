from __future__ import annotations

import unittest
from pathlib import Path

from small_practice_security_kit.suggestions import create_profile_from_preset
from small_practice_security_kit.workspaces import ROOT, WorkspaceError, atomic_write_profile, safe_profile_path


class WorkspaceWriteTests(unittest.TestCase):
    def test_atomic_write_profile_writes_under_profiles_and_logs_without_values(self) -> None:
        profile = create_profile_from_preset("Workspace Test Clinic", "dental", "solo")
        path = safe_profile_path(profile["practice"]["name"])
        atomic_write_profile(profile, path, action="test", warnings=[{"rule_id": "patient_name_label", "path": "x", "message": "redacted"}])
        self.assertTrue(path.exists())
        log = (ROOT / "profiles" / ".logs" / "profile_changes.jsonl").read_text(encoding="utf-8")
        self.assertIn("patient_name_label", log)
        self.assertNotIn("redacted", log)

    def test_atomic_write_rejects_outside_profiles(self) -> None:
        profile = create_profile_from_preset("Outside Test Clinic", "dental", "solo")
        with self.assertRaises(WorkspaceError):
            atomic_write_profile(profile, Path("/tmp/outside-small-practice-profile.yaml"), action="bad")


if __name__ == "__main__":
    unittest.main()
