from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

from small_practice_security_kit.profile import load_profile
from small_practice_security_kit.sprint import STAGE_ORDER, build_sprint


ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "samples" / "family_dental_clinic.yaml"
PHI_PLACEHOLDER_PATTERNS = [
    re.compile(r"Patient Name\s*:", re.IGNORECASE),
    re.compile(r"\bMRN\s*:", re.IGNORECASE),
    re.compile(r"\bDOB\s*:", re.IGNORECASE),
    re.compile(r"diagnosis\s*:", re.IGNORECASE),
    re.compile(r"Jane Doe", re.IGNORECASE),
]
OVERCLAIM_PATTERNS = [
    re.compile(r"\bHIPAA[- ]" + r"compliant\b", re.IGNORECASE),
    re.compile(r"\bcertified " + r"HIPAA " + r"compliant\b", re.IGNORECASE),
    re.compile(r"\bguaranteed " + r"compliance\b", re.IGNORECASE),
    re.compile(r"\bguaranteed " + r"HIPAA " + r"compliance\b", re.IGNORECASE),
    re.compile(r"\bcertifies " + r"compliance\b", re.IGNORECASE),
    re.compile(r"\blegal " + r"determination\b", re.IGNORECASE),
    re.compile(r"\bapproved for " + r"PHI\b", re.IGNORECASE),
    re.compile(r"\bAI tool " + r"approved for PHI\b", re.IGNORECASE),
    re.compile(r"\bvendor " + r"approved\b", re.IGNORECASE),
    re.compile(r"\baudit-ready " + r"guarantee\b", re.IGNORECASE),
    re.compile(r"\bbreach " + r"determination\b", re.IGNORECASE),
]


class SprintModeTests(unittest.TestCase):
    def test_sprint_command_creates_required_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            output_root = Path(temp)
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "small_practice_security_kit",
                    "sprint",
                    "samples/family_dental_clinic.yaml",
                    "--output-root",
                    str(output_root),
                ],
                cwd=ROOT,
                check=True,
            )
            out_dir = output_root / "family_dental_clinic"
            for name in [
                "sprint-index.md",
                "sprint-client-readout.md",
                "sprint-command-center.html",
                "sprint-offering-readout.md",
                "owner-action-plan.md",
                "msp-remediation-brief.md",
                "vendor-baa-ai-questionnaire.md",
                "evidence-collection-checklist.md",
                "day-one-workshop-agenda.md",
                "source-map.md",
                "sprint-summary.json",
                "risk-register.csv",
                "evidence-index.json",
                "handoff-actions.csv",
                "connector-evidence-summary.json",
                "control-evidence-matrix.csv",
                "control-evidence-matrix.json",
                "evidence-freshness-report.md",
                "msp-evidence-request.md",
                "vendor-evidence-request.md",
                "insurance-evidence-packet.md",
                "review-packet.md",
                "review-packet.html",
                "owner-msp-handoff.md",
                "connected-device-inventory.md",
                "portal-api-flow-review.md",
                "incident-decision-log.md",
                "30-60-90-roadmap.md",
                "packet-manifest.json",
                "evidence-binder-export/evidence-binder-index.csv",
            ]:
                path = out_dir / name
                self.assertTrue(path.exists(), name)
                self.assertGreater(path.stat().st_size, 0, name)

    def test_sprint_summary_has_expected_keys_and_stages(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            out_dir = build_sprint(PROFILE, Path(temp), generated_at="2026-05-16T00:00:00Z").output_dir
            summary = json.loads((out_dir / "sprint-summary.json").read_text(encoding="utf-8"))

        self.assertEqual(summary["schema_version"], "2026-05-19")
        self.assertEqual(summary["generator"]["mode"], "velari_sprint_mode_public_runner")
        self.assertEqual(summary["practice"]["label"], "Family Dental Clinic")
        self.assertFalse(summary["data_boundary"]["phi_allowed"])
        self.assertIn("outputs", summary)
        self.assertIn("counts", summary)
        self.assertIn("stage_statuses", summary)
        self.assertIn("readiness_signal", summary)
        self.assertIn("target_delivery_signal", summary)
        self.assertIn("evidence_gap_summary", summary)
        self.assertIn("handoff_lanes", summary)
        self.assertIn("connector_evidence_summary", summary)
        self.assertIn("offering_summary", summary)
        self.assertIn("control_evidence_summary", summary)
        self.assertIn("top_risks", summary)
        self.assertIn("contract_artifacts", summary)
        self.assertEqual(summary["contract_artifacts"]["answer_standard_schema"], "schemas/velari-answer-standard.schema.json")
        self.assertEqual(summary["contract_artifacts"]["normalized_evidence_schema"], "schemas/normalized-evidence.schema.json")
        self.assertEqual(summary["contract_artifacts"]["connector_run_schema"], "schemas/connector-run.schema.json")
        self.assertEqual(summary["contract_artifacts"]["control_evidence_matrix_schema"], "schemas/control-evidence-matrix.schema.json")
        self.assertEqual(summary["connector_evidence_summary"]["total_items"], 0)
        self.assertGreaterEqual(summary["control_evidence_summary"]["total_controls"], 25)
        self.assertGreater(summary["control_evidence_summary"]["mapped_controls"], 0)
        self.assertEqual([stage["id"] for stage in summary["stage_statuses"]], STAGE_ORDER)
        self.assertTrue(any(stage["status"] == "needs_evidence" for stage in summary["stage_statuses"]))
        self.assertEqual(summary["target_delivery_signal"]["next_artifact"], "sprint-command-center.html")
        self.assertGreater(summary["evidence_gap_summary"]["needs_attention"], 0)
        self.assertIn("stale", summary["evidence_gap_summary"]["by_status"])
        self.assertIn("blocked", summary["evidence_gap_summary"]["by_status"])
        self.assertTrue(summary["handoff_lanes"])
        self.assertTrue(summary["top_risks"])
        self.assertEqual(
            summary["offering_summary"]["name"],
            "Velari Cyber Readiness Sprint for Small Healthcare Practices",
        )
        self.assertGreaterEqual(len(summary["offering_summary"]["audience_lanes"]), 4)
        self.assertGreaterEqual(len(summary["offering_summary"]["source_anchors"]), 4)
        self.assertGreaterEqual(len(summary["offering_summary"]["first_7_days_actions"]), 7)
        self.assertGreaterEqual(len(summary["offering_summary"]["artifact_list"]), 7)
        self.assertTrue(summary["offering_summary"]["boundary_statements"])
        self.assertEqual(summary["offering_summary"]["private_app_import"]["contract_key"], "offering_summary")
        for stage in summary["stage_statuses"]:
            self.assertIn("next_action", stage)
            self.assertTrue(stage["artifact_refs"])
        for risk in summary["top_risks"]:
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
                self.assertTrue(risk[field], field)

    def test_sprint_output_contracts_validate_against_schemas_when_jsonschema_available(self) -> None:
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema not installed")

        with tempfile.TemporaryDirectory() as temp:
            out_dir = build_sprint(PROFILE, Path(temp), generated_at="2026-05-16T00:00:00Z").output_dir
            summary = json.loads((out_dir / "sprint-summary.json").read_text(encoding="utf-8"))
            evidence = json.loads((out_dir / "evidence-index.json").read_text(encoding="utf-8"))

        summary_schema = json.loads((ROOT / "schemas" / "sprint-summary.schema.json").read_text(encoding="utf-8"))
        evidence_schema = json.loads((ROOT / "schemas" / "evidence-index.schema.json").read_text(encoding="utf-8"))
        answer_schema = json.loads((ROOT / "schemas" / "velari-answer-standard.schema.json").read_text(encoding="utf-8"))
        jsonschema.validate(summary, summary_schema)
        jsonschema.validate(evidence, evidence_schema)
        for risk in summary["top_risks"]:
            jsonschema.validate(risk, answer_schema)

    def test_risk_handoff_and_evidence_exports_are_reference_only(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            out_dir = build_sprint(PROFILE, Path(temp), generated_at="2026-05-16T00:00:00Z").output_dir
            with (out_dir / "risk-register.csv").open(encoding="utf-8") as handle:
                risk_rows = list(csv.DictReader(handle))
            evidence = json.loads((out_dir / "evidence-index.json").read_text(encoding="utf-8"))
            with (out_dir / "handoff-actions.csv").open(encoding="utf-8") as handle:
                handoff_rows = list(csv.DictReader(handle))
            combined = "\n".join(
                [
                    (out_dir / "sprint-index.md").read_text(encoding="utf-8"),
                    (out_dir / "sprint-client-readout.md").read_text(encoding="utf-8"),
                    (out_dir / "sprint-command-center.html").read_text(encoding="utf-8"),
                    (out_dir / "sprint-offering-readout.md").read_text(encoding="utf-8"),
                    (out_dir / "owner-action-plan.md").read_text(encoding="utf-8"),
                    (out_dir / "msp-remediation-brief.md").read_text(encoding="utf-8"),
                    (out_dir / "vendor-baa-ai-questionnaire.md").read_text(encoding="utf-8"),
                    (out_dir / "evidence-collection-checklist.md").read_text(encoding="utf-8"),
                    (out_dir / "day-one-workshop-agenda.md").read_text(encoding="utf-8"),
                    (out_dir / "source-map.md").read_text(encoding="utf-8"),
                    (out_dir / "review-packet.md").read_text(encoding="utf-8"),
                    json.dumps(evidence, sort_keys=True),
                    json.dumps(risk_rows, sort_keys=True),
                    json.dumps(handoff_rows, sort_keys=True),
                    (out_dir / "evidence-freshness-report.md").read_text(encoding="utf-8"),
                    (out_dir / "msp-evidence-request.md").read_text(encoding="utf-8"),
                    (out_dir / "vendor-evidence-request.md").read_text(encoding="utf-8"),
                    (out_dir / "insurance-evidence-packet.md").read_text(encoding="utf-8"),
                    (out_dir / "connector-evidence-summary.json").read_text(encoding="utf-8"),
                    (out_dir / "control-evidence-matrix.csv").read_text(encoding="utf-8"),
                ]
            )

        self.assertTrue(risk_rows)
        self.assertTrue(evidence["evidence_references"])
        self.assertIn("connector_evidence", evidence)
        self.assertTrue(handoff_rows)
        self.assertFalse(evidence["data_boundary"]["raw_evidence_allowed"])
        self.assertEqual(evidence["binder_export"]["share_safety"], "reference_only_no_phi_no_secret")
        for field in ["audience", "recipient", "owner", "stage_id", "priority", "artifact_ref", "roadmap_bucket"]:
            self.assertTrue(all(row[field] for row in handoff_rows), field)
        for field in ["audience", "recipient", "owner", "stage_id", "priority", "artifact_ref", "roadmap_bucket"]:
            self.assertTrue(all(row[field] for row in risk_rows), field)
        action_packet_fields = [
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
            "owner_view",
            "msp_view",
            "vendor_view",
            "legal_compliance_view",
        ]
        for field in action_packet_fields:
            self.assertTrue(all(row[field] for row in risk_rows), field)
            self.assertTrue(all(row[field] for row in handoff_rows), field)
        for pattern in PHI_PLACEHOLDER_PATTERNS:
            self.assertIsNone(pattern.search(combined), pattern.pattern)
        for pattern in OVERCLAIM_PATTERNS:
            self.assertIsNone(pattern.search(combined), pattern.pattern)

    def test_real_offering_artifacts_include_practical_sections(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            out_dir = build_sprint(PROFILE, Path(temp), generated_at="2026-05-16T00:00:00Z").output_dir

            offering_readout = (out_dir / "sprint-offering-readout.md").read_text(encoding="utf-8")
            owner_plan = (out_dir / "owner-action-plan.md").read_text(encoding="utf-8")
            msp_brief = (out_dir / "msp-remediation-brief.md").read_text(encoding="utf-8")
            questionnaire = (out_dir / "vendor-baa-ai-questionnaire.md").read_text(encoding="utf-8")
            evidence_checklist = (out_dir / "evidence-collection-checklist.md").read_text(encoding="utf-8")
            workshop = (out_dir / "day-one-workshop-agenda.md").read_text(encoding="utf-8")
            source_map = (out_dir / "source-map.md").read_text(encoding="utf-8")
            command_center = (out_dir / "sprint-command-center.html").read_text(encoding="utf-8")
            connected_devices = (out_dir / "connected-device-inventory.md").read_text(encoding="utf-8")
            portal_api = (out_dir / "portal-api-flow-review.md").read_text(encoding="utf-8")
            incident_log = (out_dir / "incident-decision-log.md").read_text(encoding="utf-8")

        self.assertIn("## First 7 Days", offering_readout)
        self.assertIn("## Questions To Send", offering_readout)
        self.assertIn("## What This Does Not Prove", offering_readout)
        self.assertIn("Do Not Upload Or Send PHI To This Public Tool", owner_plan)
        self.assertIn("Questions To Send To The MSP", owner_plan)
        self.assertIn("Expected proof", msp_brief)
        self.assertIn("Stage reference", msp_brief)
        self.assertIn("AI training-use", questionnaire)
        self.assertIn("retention, deletion", questionnaire)
        self.assertIn("MFA status screenshot", evidence_checklist)
        self.assertIn("backup restore test note", evidence_checklist)
        self.assertIn("Discovery Questions", workshop)
        self.assertIn("Evidence Safety Boundaries", workshop)
        self.assertIn("HHS Cyber Gateway", source_map)
        self.assertIn("CISA Cybersecurity Performance Goals", source_map)
        self.assertIn("Offering Mode", command_center)
        self.assertIn("## Connected Device Worksheet", connected_devices)
        self.assertIn("Firmware / patch owner", connected_devices)
        self.assertIn("Default credential status", connected_devices)
        self.assertIn("## Portal And API Flows", portal_api)
        self.assertIn("Patient identity workflow", portal_api)
        self.assertIn("FHIR/app/API connections", portal_api)
        self.assertIn("## Decision Log Template", incident_log)
        self.assertIn("Technical containment", incident_log)
        self.assertIn("Qualified legal/compliance decision", incident_log)

    def test_control_evidence_matrix_maps_packets_to_owner_scoped_requests(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            out_dir = build_sprint(PROFILE, Path(temp), generated_at="2026-05-16T00:00:00Z").output_dir
            matrix = json.loads((out_dir / "control-evidence-matrix.json").read_text(encoding="utf-8"))
            msp_request = (out_dir / "msp-evidence-request.md").read_text(encoding="utf-8")
            vendor_request = (out_dir / "vendor-evidence-request.md").read_text(encoding="utf-8")
            insurance_packet = (out_dir / "insurance-evidence-packet.md").read_text(encoding="utf-8")

        self.assertGreaterEqual(len(matrix), 25)
        self.assertTrue(any(row["linked_answer_packet_ids"] for row in matrix))
        for row in matrix:
            for field in ["control_id", "evidence_id", "evidence_owner", "evidence_status", "freshness_status", "cadence", "acceptable_evidence", "unsafe_inputs", "next_action"]:
                self.assertTrue(row[field], field)
            self.assertIn("PHI or patient identifiers", row["unsafe_inputs"])
        self.assertIn("Do Not Send", msp_request)
        self.assertIn("PHI", msp_request)
        self.assertIn("Vendor Evidence Request", vendor_request)
        self.assertIn("without treating any vendor as approved", vendor_request.lower())
        self.assertIn("not insurance advice", insurance_packet.lower())

    def test_sprint_blocks_high_confidence_sensitive_profile_data(self) -> None:
        profile = load_profile(PROFILE)
        profile["handoff_questions"][0]["question"] = "MRN: A1234567"
        with tempfile.TemporaryDirectory() as temp:
            profile_path = Path(temp) / "bad.yaml"
            profile_path.write_text(yaml.safe_dump(profile, sort_keys=False), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "blocked sensitive data"):
                build_sprint(profile_path, Path(temp) / "out")


if __name__ == "__main__":
    unittest.main()
