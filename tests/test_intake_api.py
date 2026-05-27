from __future__ import annotations

import copy
import json
import threading
import unittest
import urllib.error
import urllib.request
import uuid
from pathlib import Path

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

    def test_connector_center_collects_and_builds_from_evidence(self) -> None:
        status = self.get_json("/api/status")
        practice_name = f"API Connector Center Clinic {uuid.uuid4().hex[:8]}"
        created = self.post_json(
            "/api/workspaces",
            {"practice_name": practice_name, "preset": "dental", "size_tier": "small"},
            status["csrf_token"],
        )
        self.assertTrue(created["ok"])
        empty = self.get_json("/api/connectors")
        self.assertEqual(empty["connectors"]["summary"]["total_items"], 0)

        wizard = self.post_json("/api/connectors/wizard", {}, status["csrf_token"])
        self.assertEqual(wizard["href"], "/connector-wizard.html")

        dns = self.post_json("/api/connectors/dns", {"domain": "exampleclinic.test"}, status["csrf_token"])
        self.assertEqual(dns["connectors"]["summary"]["by_connector"]["dns_email_auth"], 4)
        self.assertFalse(any(item["phi_expected"] for item in dns["connectors"]["items"]))

        msp_path = Path("samples/connectors/msp_response.yaml").resolve()
        msp = self.post_json("/api/connectors/msp-response", {"path": str(msp_path)}, status["csrf_token"])
        self.assertEqual(msp["connectors"]["summary"]["total_items"], 5)
        self.assertEqual(msp["connectors"]["summary"]["data_boundary"], "metadata_only_no_phi_expected")

        refresh = self.post_json("/api/connectors/refresh", {}, status["csrf_token"])
        self.assertEqual(refresh["href"], "/evidence-refresh.json")
        views = self.post_json("/api/connectors/views", {}, status["csrf_token"])
        self.assertIn("/views/owner-view.md", views["hrefs"])

        built = self.post_json("/api/build", {}, status["csrf_token"])
        self.assertEqual(built["links"]["command_center"], "/sprint-command-center.html")
        self.assertEqual(built["links"]["connector_summary"], "/connector-evidence-summary.json")
        with urllib.request.urlopen(self.base + "/connector-evidence-summary.json", timeout=5) as response:
            connector_summary = json.loads(response.read().decode("utf-8"))
        self.assertEqual(connector_summary["total_items"], 5)
        with urllib.request.urlopen(self.base + "/sprint-command-center.html", timeout=5) as response:
            self.assertIn("Command Center", response.read().decode("utf-8"))

    def test_incident_runner_template_save_and_safety_block(self) -> None:
        status = self.get_json("/api/status")
        created = self.post_json(
            "/api/workspaces",
            {"practice_name": f"API Incident Runner Clinic {uuid.uuid4().hex[:8]}", "preset": "dental", "size_tier": "small"},
            status["csrf_token"],
        )
        self.assertTrue(created["ok"])

        runner = self.get_json("/api/incident-runner")
        scenario_keys = {scenario["key"] for scenario in runner["scenarios"]}
        self.assertIn("ransomware_concern", scenario_keys)

        templated = self.post_json("/api/incident-runner/template", {"scenario_key": "ransomware_concern"}, status["csrf_token"])
        incident = templated["incident_timeline"]
        self.assertEqual(incident["scenario_key"], "ransomware_concern")
        self.assertGreaterEqual(len(incident["timeline"]), 5)

        saved = self.post_json("/api/incident-runner", {"incident_timeline": incident, "build": True}, status["csrf_token"])
        self.assertEqual(saved["incident_timeline"]["scenario_key"], "ransomware_concern")
        with urllib.request.urlopen(self.base + "/incident-evidence-timeline.md", timeout=5) as response:
            self.assertIn("Ransomware concern", response.read().decode("utf-8"))

        unsafe = copy.deepcopy(incident)
        unsafe["timeline"][0]["event"] = "Patient Name: Jane Example"
        with self.assertRaises(urllib.error.HTTPError) as raised:
            self.post_json("/api/incident-runner", {"incident_timeline": unsafe}, status["csrf_token"])
        self.assertEqual(raised.exception.code, 422)
        raised.exception.close()

    def test_sensitive_data_blocks_profile_save(self) -> None:
        profile = self.get_json("/api/profile")["profile"]
        profile["practice"]["security_owner"] = "MRN: A1234567"
        with self.assertRaises(urllib.error.HTTPError) as raised:
            self.post_json("/api/profile", {"profile": profile}, self.state.csrf_token)
        self.assertEqual(raised.exception.code, 422)
        raised.exception.close()

    def test_invalid_profile_save_is_rejected(self) -> None:
        profile = self.get_json("/api/profile")["profile"]
        profile["readiness"]["mfa_email"] = "yes"
        with self.assertRaises(urllib.error.HTTPError) as raised:
            self.post_json("/api/profile", {"profile": profile}, self.state.csrf_token)
        self.assertEqual(raised.exception.code, 400)
        body = raised.exception.read().decode("utf-8")
        self.assertIn("readiness.mfa_email", body)
        self.assertNotIn("yes", body)
        raised.exception.close()

    def test_write_requires_csrf_token(self) -> None:
        with self.assertRaises(urllib.error.HTTPError) as raised:
            self.post_json("/api/build", {}, "wrong-token")
        self.assertEqual(raised.exception.code, 403)
        raised.exception.close()


if __name__ == "__main__":
    unittest.main()
