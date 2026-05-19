from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PacketManifestTests(unittest.TestCase):
    def test_build_writes_canonical_packet_manifest(self) -> None:
        subprocess.run([sys.executable, "scripts/build.py", "samples/family_dental_clinic.yaml"], cwd=ROOT, check=True)
        manifest_path = ROOT / "out" / "family_dental_clinic" / "packet-manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

        self.assertEqual(manifest["schema_version"], "2026-05-19")
        self.assertEqual(manifest["packet_id"], "pkt_family_dental_clinic_2026_q2")
        self.assertEqual(manifest["generator"]["name"], "small-practice-security-kit")
        self.assertFalse(manifest["data_boundary"]["phi_allowed"])
        self.assertFalse(manifest["data_boundary"]["secrets_allowed"])
        self.assertFalse(manifest["data_boundary"]["raw_evidence_allowed"])

        section_ids = {section["id"] for section in manifest["sections"]}
        self.assertIn("executive_scorecard", section_ids)
        self.assertIn("ai_findings", section_ids)
        self.assertIn("vendor_baa_exposure", section_ids)
        self.assertIn("evidence_index", section_ids)
        self.assertIn("limitations_appendix", section_ids)
        for section in manifest["sections"]:
            if section["id"] in {"owner_msp_handoff", "limitations_appendix"}:
                self.assertEqual(section["status"], "generated")
                self.assertTrue(section["artifact_refs"])

        artifact_paths = {artifact["path"] for artifact in manifest["artifacts"]}
        self.assertIn("review-packet.md", artifact_paths)
        self.assertIn("review-packet.html", artifact_paths)
        self.assertIn("evidence-binder-index.md", artifact_paths)
        self.assertIn("owner-msp-handoff.md", artifact_paths)
        self.assertIn("limitations-appendix.md", artifact_paths)
        self.assertTrue(all(len(artifact["sha256"]) == 64 for artifact in manifest["artifacts"]))
        self.assertTrue(manifest["evidence_references"])
        self.assertTrue(manifest["findings"])
        for finding in manifest["findings"]:
            for field in [
                "plain_english_summary",
                "why_it_matters",
                "owner_lane",
                "recommended_question",
                "acceptable_evidence",
                "unsafe_inputs",
                "priority",
                "timeframe",
                "reviewer_needed",
                "next_action",
                "output_views",
            ]:
                self.assertTrue(finding[field], field)
        self.assertTrue(manifest["roadmap_items"])

    def test_manifest_schema_is_valid_json(self) -> None:
        schema_path = ROOT / "schemas" / "packet-manifest.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        self.assertEqual(schema["title"], "Velari Packet Manifest")
        self.assertEqual(schema["properties"]["generated_at"]["format"], "date-time")
        self.assertIn("allOf", schema["properties"]["sections"])
        self.assertIn("(?!/)", schema["$defs"]["artifact"]["properties"]["path"]["pattern"])
        answer_schema = json.loads((ROOT / "schemas" / "velari-answer-standard.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(answer_schema["title"], "Velari Answer Standard Action Packet")
        self.assertIn("plain_english_summary", answer_schema["required"])

    def test_generated_manifest_validates_against_schema_when_jsonschema_available(self) -> None:
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema not installed")

        subprocess.run([sys.executable, "scripts/build.py", "samples/family_dental_clinic.yaml"], cwd=ROOT, check=True)
        schema = json.loads((ROOT / "schemas" / "packet-manifest.schema.json").read_text(encoding="utf-8"))
        answer_schema = json.loads((ROOT / "schemas" / "velari-answer-standard.schema.json").read_text(encoding="utf-8"))
        manifest = json.loads((ROOT / "out" / "family_dental_clinic" / "packet-manifest.json").read_text(encoding="utf-8"))
        jsonschema.validate(manifest, schema)
        for finding in manifest["findings"]:
            jsonschema.validate(finding, answer_schema)
        self.assertFalse(manifest["source_profile"]["path"].startswith("/"))
        self.assertFalse(".." in Path(manifest["source_profile"]["path"]).parts)

    def test_build_blocks_high_confidence_sensitive_profile_data(self) -> None:
        import copy
        import tempfile
        import yaml

        from small_practice_security_kit.packet import build_packet
        from small_practice_security_kit.profile import load_profile

        profile = copy.deepcopy(load_profile(ROOT / "samples" / "family_dental_clinic.yaml"))
        profile["systems"][0]["evidence_needed"] = "Patient ID: ABCD1234"
        profile["evidence"] = [{"id": "EV-URL", "title": "private link", "reference": "https://example.com/evidence?X-Amz-Signature=abc123"}]
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            profile_path = tmp_path / "profile.yaml"
            profile_path.write_text(yaml.safe_dump(profile, sort_keys=False), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "blocked sensitive data"):
                build_packet(profile_path, output_root=tmp_path / "out")


if __name__ == "__main__":
    unittest.main()
