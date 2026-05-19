from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path

from .adapters.evidence_binder import export_binder_index
from .connectors import (
    collect_csv_import,
    collect_dns_email_auth,
    collect_google_workspace,
    collect_microsoft_365,
    collect_msp_response,
    collect_vendor_public,
    connect_google_workspace,
    connect_microsoft_365,
    write_connector_bundle,
    write_connector_wizard,
)
from .demo_export import export_demo
from .evidence_refresh import build_refresh_report, write_refresh_report
from .packet import OUT, build_packet
from .profile import load_profile
from .sensitive_data import blocking_findings
from .sprint import build_sprint
from .validation import ValidationError
from .view_exports import export_practice_views


def _path(value: str) -> Path:
    return Path(value)


def validate_command(args: argparse.Namespace) -> int:
    profile = load_profile(args.profile)
    findings = blocking_findings(profile)
    if findings:
        joined = "; ".join(f"{finding.path}: {finding.message}" for finding in findings[:5])
        print(f"Sensitive data check failed: {joined}", file=sys.stderr)
        return 2
    print(f"Profile valid: {args.profile}")
    return 0


def build_command(args: argparse.Namespace) -> int:
    if getattr(args, "evidence", None):
        result = build_sprint(args.profile, args.output_root, evidence_paths=args.evidence)
        print(f"Built Sprint Mode packet in {result.output_dir}")
        print(f"Imported connector evidence from {len(args.evidence)} path(s)")
        return 0
    out_dir = build_packet(args.profile, args.output_root)
    print(f"Built review packet in {out_dir}")
    return 0


def sprint_command(args: argparse.Namespace) -> int:
    result = build_sprint(args.profile, args.output_root, evidence_paths=args.evidence)
    print(f"Built Sprint Mode packet in {result.output_dir}")
    print(f"Exported binder-compatible evidence index to {result.binder_dir}")
    return 0


def export_binder_command(args: argparse.Namespace) -> int:
    out_dir = export_binder_index(args.profile, args.output)
    print(f"Exported evidence binder index to {out_dir}")
    return 0


def export_demo_command(args: argparse.Namespace) -> int:
    result = export_demo(
        args.profile,
        args.output,
        include_pdf=args.pdf,
        include_screenshot=not args.no_screenshot,
    )
    for warning in result.warnings:
        print(f"Warning: {warning}", file=sys.stderr)
    print(f"Exported public demo packet to {result.output_dir}")
    return 0


def import_csv_command(args: argparse.Namespace) -> int:
    bundle = collect_csv_import(args.import_type, args.csv_path)
    write_connector_bundle(bundle, args.out)
    print(f"Imported {len(bundle['evidence'])} normalized evidence items to {args.out}")
    return 0


def import_msp_response_command(args: argparse.Namespace) -> int:
    bundle = collect_msp_response(args.response_path)
    write_connector_bundle(bundle, args.out)
    print(f"Imported {len(bundle['evidence'])} MSP response evidence items to {args.out}")
    return 0


def collect_dns_command(args: argparse.Namespace) -> int:
    bundle = collect_dns_email_auth(args.domain)
    write_connector_bundle(bundle, args.out)
    print(f"Collected {len(bundle['evidence'])} DNS/email-auth evidence items to {args.out}")
    return 0


def collect_google_workspace_command(args: argparse.Namespace) -> int:
    bundle = collect_google_workspace(customer=args.customer, domain=args.domain)
    write_connector_bundle(bundle, args.out)
    print(f"Collected {len(bundle['evidence'])} Google Workspace evidence items to {args.out}")
    return 0


def collect_microsoft_365_command(args: argparse.Namespace) -> int:
    bundle = collect_microsoft_365()
    write_connector_bundle(bundle, args.out)
    print(f"Collected {len(bundle['evidence'])} Microsoft 365 evidence items to {args.out}")
    return 0


def collect_vendor_public_command(args: argparse.Namespace) -> int:
    bundle = collect_vendor_public(args.vendor, args.domain)
    write_connector_bundle(bundle, args.out)
    print(f"Collected {len(bundle['evidence'])} public vendor evidence items to {args.out}")
    return 0


def connect_google_workspace_command(args: argparse.Namespace) -> int:
    result = connect_google_workspace(client_id=args.client_id, client_secret=args.client_secret, open_browser=not args.no_open)
    print(f"Connected Google Workspace using {result['token_store_backend']}")
    print("Scopes: " + ", ".join(result["scopes"]))
    return 0


def connect_microsoft_365_command(args: argparse.Namespace) -> int:
    result = connect_microsoft_365(client_id=args.client_id, tenant=args.tenant, open_browser=not args.no_open)
    print(f"Connected Microsoft 365 using {result['token_store_backend']}")
    print("Scopes: " + ", ".join(result["scopes"]))
    return 0


def connect_wizard_command(args: argparse.Namespace) -> int:
    path = write_connector_wizard(args.out)
    print(f"Wrote connector wizard to {path}")
    return 0


def generate_msp_request_command(args: argparse.Namespace) -> int:
    with tempfile.TemporaryDirectory() as temp:
        result = build_sprint(args.profile, Path(temp), evidence_paths=args.evidence)
        source = result.output_dir / "msp-evidence-request.md"
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(source.read_text(encoding="utf-8"), encoding="utf-8", newline="\n")
    print(f"Generated MSP evidence request in {args.out}")
    return 0


def generate_views_command(args: argparse.Namespace) -> int:
    paths = export_practice_views(args.profile, args.out, evidence_paths=args.evidence)
    print(f"Generated {len(paths)} practice-ready views in {args.out}")
    return 0


def evidence_refresh_command(args: argparse.Namespace) -> int:
    report = build_refresh_report(args.current, previous_paths=args.previous, stale_after_days=args.stale_after_days)
    write_refresh_report(report, args.out)
    print(f"Wrote evidence refresh report with {report['total_items']} items to {args.out}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m small_practice_security_kit")
    subcommands = parser.add_subparsers(dest="command", required=True)

    validate = subcommands.add_parser("validate", help="Validate a practice profile schema and safety boundary.")
    validate.add_argument("profile", type=_path)
    validate.set_defaults(func=validate_command)

    build = subcommands.add_parser("build", help="Build a local review packet from a practice profile.")
    build.add_argument("profile", type=_path)
    build.add_argument("--output-root", type=_path, default=OUT)
    build.add_argument(
        "--evidence",
        type=_path,
        nargs="*",
        default=[],
        help="Optional connector evidence bundle JSON files or directories. When provided, build emits a Sprint Mode packet.",
    )
    build.set_defaults(func=build_command)

    sprint = subcommands.add_parser("sprint", help="Build a Velari Sprint Mode packet and owner/MSP runner outputs.")
    sprint.add_argument("profile", type=_path)
    sprint.add_argument("--output-root", type=_path, default=OUT)
    sprint.add_argument(
        "--evidence",
        type=_path,
        nargs="*",
        default=[],
        help="Optional connector evidence bundle JSON files or directories of JSON bundles.",
    )
    sprint.set_defaults(func=sprint_command)

    import_parser = subcommands.add_parser("import", help="Import safe client/MSP exports into normalized evidence.")
    import_subcommands = import_parser.add_subparsers(dest="import_command", required=True)
    import_csv = import_subcommands.add_parser("csv", help="Import a safe CSV export into a connector evidence bundle.")
    import_csv.add_argument(
        "import_type",
        choices=["users", "google-users", "microsoft-users", "devices", "backup-report", "vendor-register"],
        help="Type of CSV export to normalize.",
    )
    import_csv.add_argument("csv_path", type=_path)
    import_csv.add_argument("--out", type=_path, required=True)
    import_csv.set_defaults(func=import_csv_command)
    import_msp = import_subcommands.add_parser("msp-response", help="Import an MSP response YAML into a normalized evidence bundle.")
    import_msp.add_argument("response_path", type=_path)
    import_msp.add_argument("--out", type=_path, required=True)
    import_msp.set_defaults(func=import_msp_response_command)

    collect_parser = subcommands.add_parser("collect", help="Run local metadata-only collectors.")
    collect_subcommands = collect_parser.add_subparsers(dest="collect_command", required=True)
    collect_dns = collect_subcommands.add_parser("dns", help="Collect public DNS/email-auth metadata.")
    collect_dns.add_argument("--domain", required=True)
    collect_dns.add_argument("--out", type=_path, required=True)
    collect_dns.set_defaults(func=collect_dns_command)
    collect_google = collect_subcommands.add_parser("google-workspace", help="Collect official Google Workspace metadata after OAuth connect.")
    collect_google.add_argument("--customer", default="my_customer")
    collect_google.add_argument("--domain")
    collect_google.add_argument("--out", type=_path, required=True)
    collect_google.set_defaults(func=collect_google_workspace_command)
    collect_microsoft = collect_subcommands.add_parser("microsoft-365", help="Collect official Microsoft 365 metadata after OAuth connect.")
    collect_microsoft.add_argument("--out", type=_path, required=True)
    collect_microsoft.set_defaults(func=collect_microsoft_365_command)
    collect_vendor = collect_subcommands.add_parser("vendor-public", help="Collect public vendor evidence without storing raw pages.")
    collect_vendor.add_argument("--vendor", required=True)
    collect_vendor.add_argument("--domain", required=True)
    collect_vendor.add_argument("--out", type=_path, required=True)
    collect_vendor.set_defaults(func=collect_vendor_public_command)

    connect_parser = subcommands.add_parser("connect", help="Connect official read-only metadata connectors.")
    connect_subcommands = connect_parser.add_subparsers(dest="connect_command", required=True)
    connect_google = connect_subcommands.add_parser("google-workspace", help="Open browser OAuth for Google Workspace metadata.")
    connect_google.add_argument("--client-id", required=True)
    connect_google.add_argument("--client-secret")
    connect_google.add_argument("--no-open", action="store_true")
    connect_google.set_defaults(func=connect_google_workspace_command)
    connect_microsoft = connect_subcommands.add_parser("microsoft-365", help="Open browser OAuth for Microsoft 365 metadata.")
    connect_microsoft.add_argument("--client-id", required=True)
    connect_microsoft.add_argument("--tenant", default="organizations")
    connect_microsoft.add_argument("--no-open", action="store_true")
    connect_microsoft.set_defaults(func=connect_microsoft_365_command)
    connect_wizard = connect_subcommands.add_parser("wizard", help="Write a local connector wizard HTML file.")
    connect_wizard.add_argument("--out", type=_path, default=Path("out/connector-wizard.html"))
    connect_wizard.set_defaults(func=connect_wizard_command)

    generate_parser = subcommands.add_parser("generate", help="Generate focused handoff artifacts from a profile and optional evidence.")
    generate_subcommands = generate_parser.add_subparsers(dest="generate_command", required=True)
    generate_msp = generate_subcommands.add_parser("msp-request", help="Generate an MSP evidence request without building a full handoff by hand.")
    generate_msp.add_argument("--profile", type=_path, required=True)
    generate_msp.add_argument("--out", type=_path, required=True)
    generate_msp.add_argument(
        "--evidence",
        type=_path,
        nargs="*",
        default=[],
        help="Optional connector evidence bundle JSON files or directories of JSON bundles.",
    )
    generate_msp.set_defaults(func=generate_msp_request_command)
    generate_views = generate_subcommands.add_parser("views", help="Generate owner, MSP, vendor, and reviewer views.")
    generate_views.add_argument("--profile", type=_path, required=True)
    generate_views.add_argument("--out", type=_path, required=True)
    generate_views.add_argument("--evidence", type=_path, nargs="*", default=[])
    generate_views.set_defaults(func=generate_views_command)

    evidence_parser = subcommands.add_parser("evidence", help="Work with connector evidence bundles.")
    evidence_subcommands = evidence_parser.add_subparsers(dest="evidence_command", required=True)
    evidence_refresh = evidence_subcommands.add_parser("refresh", help="Compare current evidence to previous evidence and mark stale items.")
    evidence_refresh.add_argument("--current", type=_path, nargs="+", required=True)
    evidence_refresh.add_argument("--previous", type=_path, nargs="*", default=[])
    evidence_refresh.add_argument("--stale-after-days", type=int, default=90)
    evidence_refresh.add_argument("--out", type=_path, required=True)
    evidence_refresh.set_defaults(func=evidence_refresh_command)

    export_binder = subcommands.add_parser("export-binder", help="Export binder-compatible evidence index files.")
    export_binder.add_argument("profile", type=_path)
    export_binder.add_argument("--output", type=_path)
    export_binder.set_defaults(func=export_binder_command)

    export_demo_parser = subcommands.add_parser("export-demo", help="Export a safe public demo packet snapshot.")
    export_demo_parser.add_argument("--profile", type=_path, default=Path("samples/family_dental_clinic.yaml"))
    export_demo_parser.add_argument("--output", type=_path, default=Path("docs/demo"))
    export_demo_parser.add_argument("--pdf", action="store_true", help="Optionally render review-packet.pdf if Chrome/Chromium is installed.")
    export_demo_parser.add_argument("--no-screenshot", action="store_true", help="Skip optional Chrome/Chromium screenshot rendering.")
    export_demo_parser.set_defaults(func=export_demo_command)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except ValidationError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
