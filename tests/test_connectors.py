from __future__ import annotations

import csv
import json
import tempfile
import unittest
from pathlib import Path

from small_practice_security_kit.cli import main as cli_main
from small_practice_security_kit.connectors import (
    collect_csv_import,
    collect_dns_email_auth,
    collect_google_workspace,
    collect_microsoft_365,
    collect_msp_response,
    collect_vendor_public,
    write_connector_bundle,
)
from small_practice_security_kit.evidence_refresh import build_refresh_report
from small_practice_security_kit.sprint import build_sprint
from small_practice_security_kit.view_exports import export_practice_views


ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "samples" / "family_dental_clinic.yaml"


class ConnectorTests(unittest.TestCase):
    def test_csv_import_creates_normalized_evidence_without_row_identities(self) -> None:
        bundle = collect_csv_import(
            "google-users",
            ROOT / "samples" / "connectors" / "google_workspace_users.csv",
            generated_at="2026-05-19T00:00:00Z",
        )
        payload = json.dumps(bundle, sort_keys=True)

        self.assertEqual(bundle["run"]["connector"], "csv_google_users")
        self.assertEqual(bundle["run"]["safety_manifest"]["phi_expected"], False)
        self.assertEqual(len(bundle["evidence"]), 2)
        self.assertNotIn("@exampleclinic.test", payload)
        self.assertIn("mailbox contents", payload)
        self.assertTrue(any(item["evidence_id"] == "CONN-GW-MFA-001" for item in bundle["evidence"]))
        mfa = next(item for item in bundle["evidence"] if item["evidence_id"] == "CONN-GW-MFA-001")
        self.assertEqual(mfa["status"], "missing")
        self.assertEqual(mfa["counts"]["mfa_missing"], 1)
        self.assertEqual(mfa["observations"]["mfa_missing"], 1)
        self.assertEqual(mfa["phi_expected"], False)
        self.assertEqual(mfa["recommended_action"], mfa["next_action"])
        self.assertEqual(mfa["unsafe_inputs_excluded"], mfa["unsafe_fields_excluded"])
        self.assertGreater(mfa["confidence_score"], 0)
        self.assertEqual(mfa["owner_lane"], "msp")

    def test_users_csv_alias_infers_google_or_microsoft_exports(self) -> None:
        google_bundle = collect_csv_import(
            "users",
            ROOT / "samples" / "connectors" / "google_workspace_users.csv",
            generated_at="2026-05-19T00:00:00Z",
        )
        microsoft_bundle = collect_csv_import(
            "users",
            ROOT / "samples" / "connectors" / "microsoft_users.csv",
            generated_at="2026-05-19T00:00:00Z",
        )

        self.assertEqual(google_bundle["run"]["connector"], "csv_google_users")
        self.assertEqual(microsoft_bundle["run"]["connector"], "csv_microsoft_users")

    def test_all_supported_csv_imports_create_safe_evidence(self) -> None:
        imports = {
            "google-users": "google_workspace_users.csv",
            "microsoft-users": "microsoft_users.csv",
            "devices": "device_inventory.csv",
            "backup-report": "backup_report.csv",
            "vendor-register": "vendor_register.csv",
        }
        for import_type, filename in imports.items():
            with self.subTest(import_type=import_type):
                bundle = collect_csv_import(
                    import_type,
                    ROOT / "samples" / "connectors" / filename,
                    generated_at="2026-05-19T00:00:00Z",
                )
                payload = json.dumps(bundle, sort_keys=True)
                self.assertGreaterEqual(len(bundle["evidence"]), 1)
                self.assertEqual(bundle["run"]["safety_manifest"]["phi_expected"], False)
                self.assertNotIn("@exampleclinic.test", payload)
                self.assertTrue(all(item["phi_status"] == "metadata_only_no_phi_expected" for item in bundle["evidence"]))
                self.assertTrue(all(item["recommended_question"] for item in bundle["evidence"]))

    def test_dns_collector_summarizes_email_auth_without_private_records(self) -> None:
        records = {
            ("exampleclinic.test", "MX"): ["10 mail.exampleclinic.test."],
            ("exampleclinic.test", "TXT"): ["v=spf1 include:_spf.example.test -all"],
            ("_dmarc.exampleclinic.test", "TXT"): ["v=DMARC1; p=none; rua=mailto:dmarc@example.test"],
            ("selector1._domainkey.exampleclinic.test", "TXT"): ["v=DKIM1; k=rsa; p=abc"],
        }

        def resolver(name: str, record_type: str) -> list[str]:
            return records.get((name, record_type), [])

        bundle = collect_dns_email_auth("exampleclinic.test", generated_at="2026-05-19T00:00:00Z", resolver=resolver)
        payload = json.dumps(bundle, sort_keys=True)
        dmarc = next(item for item in bundle["evidence"] if item["evidence_id"] == "CONN-DNS-DMARC-001")
        dkim = next(item for item in bundle["evidence"] if item["evidence_id"] == "CONN-DNS-DKIM-001")

        self.assertEqual(bundle["run"]["connector"], "dns_email_auth")
        self.assertEqual(len(bundle["evidence"]), 4)
        self.assertEqual(dmarc["status"], "needs_review")
        self.assertEqual(dkim["status"], "observed")
        self.assertNotIn("mailto:dmarc", payload)
        self.assertIn("metadata_only_no_phi_expected", payload)

    def test_vendor_public_collector_stores_triage_not_raw_pages(self) -> None:
        pages = {
            "/": "Abridge helps healthcare organizations with security and privacy.",
            "/security": "Security program, SOC 2, encryption, and incident response overview.",
            "/privacy": "HIPAA business associate information and customer data use terms.",
            "/subprocessors": "Subprocessors list for service providers.",
            "/terms": "Artificial intelligence and model training terms are described here.",
        }

        def fetcher(url: str) -> tuple[int, str]:
            path = "/" + url.split("/", 3)[3] if "/" in url[8:] else "/"
            return (200, pages.get(path, ""))

        bundle = collect_vendor_public(
            "Abridge",
            "abridge.com",
            generated_at="2026-05-19T00:00:00Z",
            fetcher=fetcher,
        )
        payload = json.dumps(bundle, sort_keys=True)
        item = bundle["evidence"][0]

        self.assertEqual(bundle["run"]["connector"], "vendor_public_web")
        self.assertEqual(item["evidence_id"], "CONN-VENDOR-PUBLIC-001")
        self.assertEqual(item["source_type"], "public_lookup")
        self.assertEqual(item["status"], "needs_review")
        self.assertEqual(item["observations"]["raw_page_text_stored"], False)
        self.assertTrue(item["observations"]["hipaa_baa_terms_found"])
        self.assertNotIn("Security program, SOC 2", payload)

    def test_google_workspace_official_connector_aggregates_api_metadata(self) -> None:
        requested_urls: list[str] = []

        def fetcher(url: str, token: str) -> dict[str, object]:
            requested_urls.append(url)
            return {
                "users": [
                    {
                        "primaryEmail": "owner@exampleclinic.test",
                        "isAdmin": True,
                        "suspended": False,
                        "isEnrolledIn2Sv": True,
                        "isEnforcedIn2Sv": True,
                        "lastLoginTime": "2026-05-10T00:00:00.000Z",
                        "creationTime": "2024-01-01T00:00:00.000Z",
                    },
                    {
                        "primaryEmail": "staff@exampleclinic.test",
                        "isAdmin": False,
                        "suspended": False,
                        "isEnrolledIn2Sv": False,
                        "isEnforcedIn2Sv": False,
                        "lastLoginTime": "2025-01-10T00:00:00.000Z",
                        "creationTime": "2024-01-01T00:00:00.000Z",
                    },
                    {
                        "primaryEmail": "former@exampleclinic.test",
                        "isAdmin": False,
                        "suspended": True,
                        "isEnrolledIn2Sv": False,
                        "isEnforcedIn2Sv": False,
                        "lastLoginTime": "1970-01-01T00:00:00.000Z",
                        "creationTime": "2023-01-01T00:00:00.000Z",
                    },
                ]
            }

        bundle = collect_google_workspace(generated_at="2026-05-19T00:00:00Z", fetcher=fetcher)
        payload = json.dumps(bundle, sort_keys=True)
        mfa = next(item for item in bundle["evidence"] if item["evidence_id"] == "CONN-GW-API-MFA-001")
        lifecycle = next(item for item in bundle["evidence"] if item["evidence_id"] == "CONN-GW-API-LIFECYCLE-001")

        self.assertEqual(bundle["run"]["connector"], "google_workspace_api")
        self.assertEqual(len(bundle["evidence"]), 3)
        self.assertIn("lastLoginTime", requested_urls[0])
        self.assertEqual(mfa["confidence"], "observed_from_api")
        self.assertEqual(mfa["counts"]["mfa_missing"], 1)
        self.assertEqual(mfa["counts"]["active_users"], 2)
        self.assertEqual(lifecycle["counts"]["inactive_90_day_active_users"], 1)
        self.assertEqual(lifecycle["counts"]["suspended_users"], 1)
        self.assertIn("msp", lifecycle["reviewer_needed"])
        self.assertNotIn("@exampleclinic.test", payload)

    def test_microsoft_365_official_connector_aggregates_graph_metadata(self) -> None:
        requested_urls: list[str] = []

        def fetcher(url: str, token: str, headers: dict[str, str] | None = None) -> dict[str, object]:
            requested_urls.append(url)
            if "/users?" in url:
                return {
                    "value": [
                        {
                            "id": "1",
                            "userPrincipalName": "owner@exampleclinic.test",
                            "accountEnabled": True,
                            "userType": "Member",
                            "createdDateTime": "2024-01-01T00:00:00Z",
                            "signInActivity": {"lastSuccessfulSignInDateTime": "2026-05-18T00:00:00Z"},
                        },
                        {
                            "id": "2",
                            "userPrincipalName": "guest@exampleclinic.test",
                            "accountEnabled": True,
                            "userType": "Guest",
                            "createdDateTime": "2026-05-01T00:00:00Z",
                            "signInActivity": {},
                        },
                    ]
                }
            return {
                "value": [
                    {"isMfaRegistered": True, "isMfaCapable": True, "isSsprRegistered": True, "isSsprEnabled": True},
                    {"isMfaRegistered": False, "isMfaCapable": False, "isSsprRegistered": False, "isSsprEnabled": False},
                ]
            }

        bundle = collect_microsoft_365(generated_at="2026-05-19T00:00:00Z", fetcher=fetcher)
        payload = json.dumps(bundle, sort_keys=True)
        mfa = next(item for item in bundle["evidence"] if item["evidence_id"] == "CONN-M365-API-MFA-001")
        users = next(item for item in bundle["evidence"] if item["evidence_id"] == "CONN-M365-API-USERS-001")
        sspr = next(item for item in bundle["evidence"] if item["evidence_id"] == "CONN-M365-API-SSPR-001")
        guests = next(item for item in bundle["evidence"] if item["evidence_id"] == "CONN-M365-API-GUESTS-001")
        lifecycle = next(item for item in bundle["evidence"] if item["evidence_id"] == "CONN-M365-API-LIFECYCLE-001")

        self.assertEqual(bundle["run"]["connector"], "microsoft_365_api")
        self.assertEqual(len(bundle["evidence"]), 5)
        self.assertIn("signInActivity", requested_urls[0])
        self.assertEqual(mfa["counts"]["mfa_missing"], 1)
        self.assertEqual(users["counts"]["enabled_users"], 2)
        self.assertEqual(sspr["counts"]["sspr_missing"], 1)
        self.assertEqual(guests["counts"]["enabled_guest_users"], 1)
        self.assertEqual(lifecycle["counts"]["never_signed_in_enabled_users"], 1)
        self.assertIn("msp", guests["reviewer_needed"])
        self.assertNotIn("@exampleclinic.test", payload)

    def test_msp_response_import_and_refresh_report_are_safe(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            temp_path = Path(temp)
            bundle = collect_msp_response(
                ROOT / "samples" / "connectors" / "msp_response.yaml",
                generated_at="2026-05-19T00:00:00Z",
            )
            bundle_path = write_connector_bundle(bundle, temp_path / "msp-response.json")
            report = build_refresh_report([bundle_path], generated_at="2026-05-19T00:00:00Z")

        payload = json.dumps(bundle, sort_keys=True)
        self.assertEqual(bundle["run"]["connector"], "msp_response_import")
        self.assertEqual(bundle["evidence"][0]["confidence"], "imported_from_msp_response")
        self.assertNotIn("password", payload.lower())
        self.assertEqual(report["total_items"], 1)
        self.assertEqual(report["new_items"], 1)

    def test_sprint_accepts_connector_evidence_and_generates_action_packets(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            temp_path = Path(temp)
            google_bundle = collect_csv_import(
                "google-users",
                ROOT / "samples" / "connectors" / "google_workspace_users.csv",
                generated_at="2026-05-19T00:00:00Z",
            )
            vendor_bundle = collect_csv_import(
                "vendor-register",
                ROOT / "samples" / "connectors" / "vendor_register.csv",
                generated_at="2026-05-19T00:00:00Z",
            )
            google_path = write_connector_bundle(google_bundle, temp_path / "google-users.json")
            vendor_path = write_connector_bundle(vendor_bundle, temp_path / "vendor-register.json")
            out_dir = build_sprint(
                PROFILE,
                temp_path / "out",
                generated_at="2026-05-19T00:00:00Z",
                evidence_paths=[google_path, vendor_path],
            ).output_dir

            summary = json.loads((out_dir / "sprint-summary.json").read_text(encoding="utf-8"))
            evidence_index = json.loads((out_dir / "evidence-index.json").read_text(encoding="utf-8"))
            connector_summary = json.loads((out_dir / "connector-evidence-summary.json").read_text(encoding="utf-8"))
            with (out_dir / "risk-register.csv").open(encoding="utf-8") as handle:
                risk_rows = list(csv.DictReader(handle))

        self.assertEqual(summary["counts"]["connector_evidence_items"], 3)
        self.assertEqual(summary["connector_evidence_summary"]["total_items"], 3)
        self.assertEqual(connector_summary["by_connector"]["csv_google_users"], 2)
        self.assertIn("by_priority", connector_summary)
        self.assertGreaterEqual(len(connector_summary["attention_items"]), 1)
        self.assertEqual(len(evidence_index["connector_evidence"]), 3)
        self.assertTrue(any(row["finding_id"] == "CONN-GW-MFA-001" for row in risk_rows))
        self.assertTrue(any(row["finding_id"] == "CONN-VENDOR-BAA-001" for row in risk_rows))
        self.assertTrue(all("PHI" in row["unsafe_inputs"] for row in risk_rows if row["finding_id"].startswith("CONN-")))
        try:
            import jsonschema
        except ImportError:
            return
        summary_schema = json.loads((ROOT / "schemas" / "sprint-summary.schema.json").read_text(encoding="utf-8"))
        evidence_schema = json.loads((ROOT / "schemas" / "evidence-index.schema.json").read_text(encoding="utf-8"))
        jsonschema.validate(summary, summary_schema)
        jsonschema.validate(evidence_index, evidence_schema)

    def test_cli_owner_friendly_connector_commands(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            temp_path = Path(temp)
            evidence_dir = temp_path / "evidence"
            out_dir = temp_path / "out"
            evidence_dir.mkdir()
            users_path = evidence_dir / "users.json"
            dns_path = evidence_dir / "dns.json"
            msp_request_path = temp_path / "msp-request.md"

            self.assertEqual(
                cli_main(
                    [
                        "import",
                        "csv",
                        "users",
                        str(ROOT / "samples" / "connectors" / "google_workspace_users.csv"),
                        "--out",
                        str(users_path),
                    ]
                ),
                0,
            )
            self.assertEqual(
                cli_main(["collect", "dns", "--domain", "exampleclinic.test", "--out", str(dns_path)]),
                0,
            )
            self.assertEqual(
                cli_main(["generate", "msp-request", "--profile", str(PROFILE), "--evidence", str(users_path), "--out", str(msp_request_path)]),
                0,
            )
            self.assertEqual(
                cli_main(["build", str(PROFILE), "--evidence", str(users_path), str(dns_path), "--output-root", str(out_dir)]),
                0,
            )

            packet_dir = out_dir / "family_dental_clinic"
            summary = json.loads((packet_dir / "sprint-summary.json").read_text(encoding="utf-8"))
            self.assertTrue(users_path.exists())
            self.assertTrue(dns_path.exists())
            self.assertIn("MSP Evidence Request", msp_request_path.read_text(encoding="utf-8"))
            self.assertEqual(summary["counts"]["connector_evidence_items"], 6)

    def test_cli_generates_wizard_refresh_and_practice_views(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            temp_path = Path(temp)
            evidence_dir = temp_path / "evidence"
            views_dir = temp_path / "views"
            evidence_dir.mkdir()
            users_path = evidence_dir / "users.json"
            refresh_path = temp_path / "refresh.json"
            wizard_path = temp_path / "wizard.html"

            self.assertEqual(
                cli_main(["import", "csv", "users", str(ROOT / "samples" / "connectors" / "google_workspace_users.csv"), "--out", str(users_path)]),
                0,
            )
            self.assertEqual(cli_main(["connect", "wizard", "--out", str(wizard_path)]), 0)
            self.assertEqual(cli_main(["evidence", "refresh", "--current", str(users_path), "--out", str(refresh_path)]), 0)
            self.assertEqual(cli_main(["generate", "views", "--profile", str(PROFILE), "--evidence", str(users_path), "--out", str(views_dir)]), 0)

            refresh = json.loads(refresh_path.read_text(encoding="utf-8"))
            self.assertIn("Google Workspace", wizard_path.read_text(encoding="utf-8"))
            self.assertEqual(refresh["total_items"], 2)
            self.assertTrue((views_dir / "owner-view.md").exists())

    def test_export_practice_views_writes_lane_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            temp_path = Path(temp)
            bundle = collect_csv_import(
                "vendor-register",
                ROOT / "samples" / "connectors" / "vendor_register.csv",
                generated_at="2026-05-19T00:00:00Z",
            )
            evidence_path = write_connector_bundle(bundle, temp_path / "vendor.json")
            paths = export_practice_views(PROFILE, temp_path / "views", evidence_paths=[evidence_path])

        self.assertEqual(len(paths), 4)
        self.assertTrue(any(path.name == "vendor-view.md" for path in paths))

    def test_connector_schemas_validate_when_jsonschema_available(self) -> None:
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema not installed")

        bundle = collect_csv_import(
            "backup-report",
            ROOT / "samples" / "connectors" / "backup_report.csv",
            generated_at="2026-05-19T00:00:00Z",
        )
        bundle_schema = json.loads((ROOT / "schemas" / "connector-run.schema.json").read_text(encoding="utf-8"))
        evidence_schema = json.loads((ROOT / "schemas" / "normalized-evidence.schema.json").read_text(encoding="utf-8"))
        msp_bundle = collect_msp_response(
            ROOT / "samples" / "connectors" / "msp_response.yaml",
            generated_at="2026-05-19T00:00:00Z",
        )
        google_bundle = collect_google_workspace(
            generated_at="2026-05-19T00:00:00Z",
            fetcher=lambda url, token: {"users": [{"isAdmin": True, "suspended": False, "isEnrolledIn2Sv": True, "isEnforcedIn2Sv": True}]},
        )
        microsoft_bundle = collect_microsoft_365(
            generated_at="2026-05-19T00:00:00Z",
            fetcher=lambda url, token, headers=None: {
                "value": [{"accountEnabled": True, "userType": "Member", "isMfaRegistered": True, "isMfaCapable": True, "isSsprRegistered": True, "isSsprEnabled": True}]
            },
        )
        for candidate in [bundle, msp_bundle, google_bundle, microsoft_bundle]:
            jsonschema.validate(candidate, bundle_schema)
            for item in candidate["evidence"]:
                jsonschema.validate(item, evidence_schema)


if __name__ == "__main__":
    unittest.main()
