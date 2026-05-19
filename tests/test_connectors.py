from __future__ import annotations

import csv
import json
import tempfile
import unittest
from pathlib import Path

from small_practice_security_kit.cli import main as cli_main
from small_practice_security_kit.connectors import collect_csv_import, collect_dns_email_auth, collect_vendor_public, write_connector_bundle
from small_practice_security_kit.sprint import build_sprint


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
        jsonschema.validate(bundle, bundle_schema)
        for item in bundle["evidence"]:
            jsonschema.validate(item, evidence_schema)


if __name__ == "__main__":
    unittest.main()
