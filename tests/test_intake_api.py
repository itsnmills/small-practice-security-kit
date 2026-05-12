from __future__ import annotations

import json
import threading
import unittest
import urllib.error
import urllib.request

from small_practice_security_kit.local_api import AppState, LocalIntakeServer, make_handler
from small_practice_security_kit.packet import build_packet
from small_practice_security_kit.suggestions import create_profile_from_preset
from small_practice_security_kit.workspaces import atomic_write_profile, safe_profile_path


class IntakeApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        profile = create_profile_from_preset("API Seed Clinic", "dental", "small")
        cls.profile_path = safe_profile_path(profile["practice"]["name"])
        atomic_write_profile(profile, cls.profile_path, action="api-seed")
        cls.out_dir = build_packet(cls.profile_path)
        cls.state = AppState(profile_path=cls.profile_path, out_dir=cls.out_dir)
        cls.server = LocalIntakeServer(("127.0.0.1", 0), make_handler(cls.state))
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.server.server_address[1]}"

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()
        cls.thread.join(timeout=5)
        cls.server.server_close()

    def get_json(self, path: str) -> dict:
        with urllib.request.urlopen(self.base + path, timeout=5) as response:
            return json.loads(response.read().decode("utf-8"))

    def post_json(self, path: str, payload: dict, token: str | None = None) -> dict:
        data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            self.base + path,
            data=data,
            method="POST",
            headers={"Content-Type": "application/json", "X-SPSK-Token": token or self.state.csrf_token},
        )
        with urllib.request.urlopen(request, timeout=5) as response:
            return json.loads(response.read().decode("utf-8"))

    def test_status_catalogs_profile_and_build_loop(self) -> None:
        status = self.get_json("/api/status")
        self.assertTrue(status["local_only"])
        self.assertEqual(status["network_status"], "offline/local only")
        catalogs = self.get_json("/api/catalogs")
        self.assertIn("dental", catalogs["catalogs"]["practice_presets"]["presets"])
        created = self.post_json(
            "/api/workspaces",
            {"practice_name": "API Intake Test Clinic", "preset": "dental", "size_tier": "small"},
            status["csrf_token"],
        )
        self.assertTrue(created["ok"])
        self.assertGreater(len(created["profile"]["flows"]), 0)
        built = self.post_json("/api/build", {}, status["csrf_token"])
        self.assertEqual(built["links"]["dashboard"], "/dashboard.html")
        with urllib.request.urlopen(self.base + "/dashboard.html", timeout=5) as response:
            self.assertIn("Owner dashboard", response.read().decode("utf-8"))

    def test_sensitive_data_blocks_profile_save(self) -> None:
        profile = self.get_json("/api/profile")["profile"]
        profile["practice"]["security_owner"] = "MRN: A1234567"
        with self.assertRaises(urllib.error.HTTPError) as raised:
            self.post_json("/api/profile", {"profile": profile}, self.state.csrf_token)
        self.assertEqual(raised.exception.code, 422)
        raised.exception.close()

    def test_write_requires_csrf_token(self) -> None:
        with self.assertRaises(urllib.error.HTTPError) as raised:
            self.post_json("/api/build", {}, "wrong-token")
        self.assertEqual(raised.exception.code, 403)
        raised.exception.close()


if __name__ == "__main__":
    unittest.main()
