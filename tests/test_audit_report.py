from __future__ import annotations

import argparse
import json
import tempfile
import unittest
from pathlib import Path

from small_practice_security_kit.audit_report import (
    generate_audit_gap_report,
    render_audit_report_csv,
    render_audit_report_json,
    render_audit_report_markdown,
    render_audit_report_text,
)
from small_practice_security_kit.cli import audit_report_command, matrix_check_command
from small_practice_security_kit.profile import load_profile
from small_practice_security_kit.suggestions import create_profile_from_preset


class AuditReportTests(unittest.TestCase):
    def setUp(self) -> None:
        self.sample_profile_path = Path("samples/family_dental_clinic.yaml")
        self.sample_profile = load_profile(self.sample_profile_path)

    def test_generate_audit_gap_report_evaluates_all_30_controls(self) -> None:
        report = generate_audit_gap_report(self.sample_profile)
        summary = report["summary"]
        controls = report["controls"]

        self.assertEqual(summary["total_controls"], 30)
        self.assertEqual(len(controls), 30)
        self.assertEqual(
            summary["addressed_count"] + summary["partial_count"] + summary["gap_count"] + summary["not_applicable_count"],
            30,
        )
        self.assertGreater(summary["readiness_percentage"], 0)
        self.assertIn("/", summary["required_addressed_ratio"])
        self.assertIn("/", summary["addressable_addressed_ratio"])
        self.assertGreater(len(summary["by_family"]), 0)
        self.assertGreater(len(summary["by_hicp_practice"]), 0)

    def test_audit_gap_report_identifies_unaddressed_gaps(self) -> None:
        report = generate_audit_gap_report(self.sample_profile)
        gaps_map = {c["control_id"]: c for c in report["unaddressed_gaps"]}

        # Family Dental Clinic has mfa_ehr: false, tested_backups: false, baa_register: false
        self.assertIn("VEL-MFA-REMOTE-001", gaps_map)
        self.assertEqual(gaps_map["VEL-MFA-REMOTE-001"]["status"], "partial")
        self.assertEqual(gaps_map["VEL-MFA-REMOTE-001"]["severity"], "critical")

        self.assertIn("VEL-BACKUP-RESTORE-001", gaps_map)
        self.assertEqual(gaps_map["VEL-BACKUP-RESTORE-001"]["status"], "gap")
        self.assertEqual(gaps_map["VEL-BACKUP-RESTORE-001"]["severity"], "critical")

        # 3 ePHI vendors lack signed BAAs, so BAA status is partial and critical
        self.assertIn("VEL-BAA-STATUS-001", gaps_map)
        self.assertEqual(gaps_map["VEL-BAA-STATUS-001"]["status"], "partial")
        self.assertEqual(gaps_map["VEL-BAA-STATUS-001"]["severity"], "critical")

        # Termination procedures should be addressable
        offboarding = next(c for c in report["controls"] if c["control_id"] == "VEL-OFFBOARDING-001")
        self.assertEqual(offboarding["cfr_designation"], "Addressable")

    def test_baa_register_flag_does_not_override_unsigned_vendors(self) -> None:
        profile = create_profile_from_preset("Preset Clinic", "dental", "solo")
        profile["readiness"]["baa_register"] = True
        # Vendors in preset default to unknown/unsigned BAAs
        report = generate_audit_gap_report(profile)
        baa_eval = next(c for c in report["controls"] if c["control_id"] == "VEL-BAA-STATUS-001")
        self.assertIn(baa_eval["status"], {"gap", "partial"})
        self.assertEqual(baa_eval["severity"], "critical")

    def test_audit_gap_report_with_compliant_profile(self) -> None:
        profile = create_profile_from_preset("Compliant Clinic", "dental", "solo")
        for k, v in [
            ("mfa_email", True),
            ("mfa_ehr", True),
            ("tested_backups", True),
            ("baa_register", True),
            ("quarterly_access_review", True),
            ("downtime_plan", True),
            ("log_review_cadence", True),
            ("security_training_current", True),
            ("vendor_inventory", True),
            ("unique_accounts", True),
            ("risk_analysis", True),
            ("security_policies_current", True),
            ("termination_procedures", True),
            ("breakglass_procedure", True),
            ("endpoint_protection", True),
            ("device_encryption", True),
            ("facility_access_controls", True),
            ("media_disposal", True),
            ("privileged_account_inventory", True),
            ("incident_contact_list", True),
        ]:
            profile["readiness"][k] = v

        for v in profile.get("vendors", []):
            v["baa_status"] = "signed"
            v["incident_notification_terms"] = "24 hours notice"
            v["soc2_status"] = "current"
            v["hitrust_status"] = "current"

        for w in profile.get("ai_workflows", []):
            w["decision"] = "allowed"

        report = generate_audit_gap_report(profile)
        summary = report["summary"]
        self.assertEqual(summary["critical_gaps_count"], 0)
        self.assertGreaterEqual(summary["readiness_percentage"], 90.0)

    def test_render_formats_and_gaps_only_filtering(self) -> None:
        report = generate_audit_gap_report(self.sample_profile)

        # Text
        text_out = render_audit_report_text(report, gaps_only=True)
        self.assertIn("SMALL PRACTICE SECURITY AUDIT GAP REPORT", text_out)
        self.assertIn("EXECUTIVE SUMMARY", text_out)
        self.assertIn("VEL-MFA-REMOTE-001", text_out)

        # Markdown
        md_out = render_audit_report_markdown(report, gaps_only=False)
        self.assertIn("# Security Audit Gap Report:", md_out)
        self.assertIn("## Executive Scorecard", md_out)
        self.assertIn("| Control ID | Control Name |", md_out)

        # JSON with gaps_only
        json_all = json.loads(render_audit_report_json(report, gaps_only=False))
        json_gaps = json.loads(render_audit_report_json(report, gaps_only=True))
        self.assertEqual(len(json_all["controls"]), 30)
        self.assertEqual(len(json_gaps["controls"]), len(report["unaddressed_gaps"]))

        # CSV with gaps_only and formula escaping
        csv_all = render_audit_report_csv(report, gaps_only=False)
        csv_gaps = render_audit_report_csv(report, gaps_only=True)
        self.assertIn("control_id,control_name,control_family", csv_all)
        self.assertIn("VEL-GOV-OWNER-001", csv_all)
        # gaps only has fewer rows than all controls
        self.assertLess(csv_gaps.count("\n"), csv_all.count("\n"))

    def test_cli_audit_report_and_matrix_check(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            temp_dir = Path(temp)
            out_file = temp_dir / "report.md"

            # 1. audit-report without strict returns 0
            args = argparse.Namespace(
                profile=self.sample_profile_path,
                format="markdown",
                out=str(out_file),
                evidence=[],
                gaps_only=True,
                strict=False,
            )
            code = audit_report_command(args)
            self.assertEqual(code, 0)
            self.assertTrue(out_file.exists())
            self.assertIn("# Security Audit Gap Report", out_file.read_text(encoding="utf-8"))

            # 2. matrix-check sets strict=True and fails when gaps exist
            args_strict = argparse.Namespace(
                profile=self.sample_profile_path,
                format="text",
                out=None,
                evidence=[],
                gaps_only=True,
            )
            code_strict = matrix_check_command(args_strict)
            self.assertEqual(code_strict, 1)


if __name__ == "__main__":
    unittest.main()
