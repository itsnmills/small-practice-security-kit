from __future__ import annotations

import json
import secrets
from dataclasses import dataclass
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from socketserver import ThreadingMixIn
from typing import Any
from urllib.parse import urlparse

import yaml

from .catalogs import load_catalogs
from .connectors import (
    collect_dns_email_auth,
    collect_google_workspace,
    collect_microsoft_365,
    collect_msp_response,
    collect_vendor_public,
    connect_google_workspace,
    connect_microsoft_365,
    load_connector_bundles,
    summarize_connector_evidence,
    write_connector_bundle,
    write_connector_wizard,
)
from .dashboard import build_dashboard
from .evidence_refresh import build_refresh_report, write_refresh_report
from .file_inventory import FileInventoryError, default_evidence_roots, inventory_folder, resolve_allowed_path
from .incident_runner import enrich_incident_timeline, safety_findings, scenario_options, scenario_template
from .packet import build_packet
from .profile import load_profile
from .sensitive_data import blocking_findings, find_sensitive_data
from .sprint import build_sprint
from .suggestions import create_profile_from_preset, rebuild_profile_suggestions
from .validation import ValidationError, validate_profile
from .view_exports import export_practice_views
from .workspaces import ROOT, atomic_write_profile, ensure_workspace_dirs, safe_profile_path


STATIC_DIR = Path(__file__).resolve().parent / "static"
MAX_BODY_BYTES = 512 * 1024
LOOPBACK_HOSTNAMES = frozenset({"127.0.0.1", "localhost", "::1"})


def is_loopback_bind_host(host: str) -> bool:
    value = host.strip().lower()
    if value.startswith("[") and value.endswith("]"):
        value = value[1:-1]
    return value in LOOPBACK_HOSTNAMES


def parse_http_host(host: str) -> tuple[str, int | None] | None:
    value = host.strip()
    if not value:
        return None
    if value.startswith("["):
        end = value.find("]")
        if end <= 1:
            return None
        hostname = value[1:end]
        rest = value[end + 1 :]
        if not rest:
            return hostname, None
        if not rest.startswith(":"):
            return None
        try:
            return hostname, int(rest[1:])
        except ValueError:
            return None
    if value.count(":") == 1:
        hostname, port_text = value.rsplit(":", 1)
        if not hostname or not port_text.isdigit():
            return None
        return hostname, int(port_text)
    if ":" in value:
        return None
    return value, None


def host_header_is_allowed(host: str, bound_port: int) -> bool:
    parsed = parse_http_host(host)
    if parsed is None:
        return False
    hostname, port = parsed
    if hostname.lower() not in LOOPBACK_HOSTNAMES:
        return False
    if port is None:
        return bound_port == 80
    return port == bound_port


def origin_matches_host(origin: str, host: str) -> bool:
    parsed = urlparse(origin)
    if parsed.scheme != "http" or not parsed.netloc:
        return False
    if parsed.username or parsed.password:
        return False
    if parsed.path not in {"", "/"}:
        return False
    if parsed.params or parsed.query or parsed.fragment:
        return False
    return parsed.netloc.lower() == host.strip().lower()


def _import_msp_response(response_path: Path) -> dict[str, Any]:
    try:
        return collect_msp_response(response_path)
    except (OSError, UnicodeError, ValueError, yaml.YAMLError) as exc:
        raise ValueError("Could not import MSP response file.") from exc


def _connector_dir(out_dir: Path) -> Path:
    return out_dir / "connector-evidence"


def _connector_paths(out_dir: Path) -> list[Path]:
    evidence_dir = _connector_dir(out_dir)
    if not evidence_dir.exists():
        return []
    return sorted(evidence_dir.glob("*.json"))


def _connector_status(out_dir: Path) -> dict[str, Any]:
    evidence_dir = _connector_dir(out_dir)
    paths = _connector_paths(out_dir)
    bundles = load_connector_bundles(paths)
    summary = summarize_connector_evidence(bundles)
    items: list[dict[str, Any]] = []
    for path, bundle in zip(paths, bundles):
        run = bundle.get("run", {})
        evidence = bundle.get("evidence", [])
        items.append(
            {
                "file": path.name,
                "path": str(path),
                "connector": str(run.get("connector", "unknown")),
                "mode": str(run.get("mode", "")),
                "status": str(run.get("status", "")),
                "evidence_count": int(run.get("evidence_count", len(evidence))),
                "phi_expected": bool(run.get("safety_manifest", {}).get("phi_expected", False)),
                "warnings": list(run.get("warnings", [])),
            }
        )
    return {
        "directory": str(evidence_dir),
        "items": items,
        "summary": summary,
        "build_uses_connectors": bool(paths),
    }


@dataclass
class AppState:
    profile_path: Path
    out_dir: Path
    host: str = "127.0.0.1"
    csrf_token: str = ""

    def __post_init__(self) -> None:
        if not is_loopback_bind_host(self.host):
            raise ValueError(
                f"Local intake server host must be loopback (127.0.0.1, localhost, or ::1), not {self.host!r}."
            )
        if not self.csrf_token:
            self.csrf_token = secrets.token_urlsafe(24)

    def evidence_roots(self) -> list[Path]:
        return default_evidence_roots(self.out_dir)


class LocalIntakeServer(ThreadingMixIn, HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


def make_handler(state: AppState) -> type[BaseHTTPRequestHandler]:
    class LocalIntakeHandler(BaseHTTPRequestHandler):
        server_version = "SmallPracticeSecurityKit/1.0"

        def log_message(self, format: str, *args: object) -> None:
            return

        def _send(self, status: int, body: bytes, content_type: str) -> None:
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.end_headers()
            self.wfile.write(body)

        def _json(self, status: int, payload: dict[str, Any]) -> None:
            self._send(status, json.dumps(payload, sort_keys=True).encode("utf-8"), "application/json; charset=utf-8")

        def _error(self, status: int, message: str, **extra: Any) -> None:
            payload = {"ok": False, "error": message}
            payload.update(extra)
            self._json(status, payload)

        def _is_local(self) -> bool:
            client = self.client_address[0]
            if client in {"127.0.0.1", "::1", "localhost"}:
                return True
            return client == "::ffff:127.0.0.1"

        def _check_local_request(self) -> bool:
            if not self._is_local():
                self._error(HTTPStatus.FORBIDDEN, "This service is localhost-only.")
                return False
            host = self.headers.get("Host", "")
            if not host_header_is_allowed(host, self.server.server_address[1]):
                self._error(HTTPStatus.FORBIDDEN, "Invalid Host header.")
                return False
            origin = self.headers.get("Origin")
            if origin and not origin_matches_host(origin, host):
                self._error(HTTPStatus.FORBIDDEN, "Same-origin check failed.")
                return False
            return True

        def _check_post_security(self) -> bool:
            if not self._check_local_request():
                return False
            if self.headers.get("X-SPSK-Token") != state.csrf_token:
                self._error(HTTPStatus.FORBIDDEN, "Missing or invalid local session token.")
                return False
            return True

        def _read_json(self) -> dict[str, Any]:
            length = int(self.headers.get("Content-Length", "0") or "0")
            if length > MAX_BODY_BYTES:
                raise ValueError("Request body too large.")
            content_type = self.headers.get("Content-Type", "")
            if "application/json" not in content_type:
                raise ValueError("JSON content type required.")
            raw = self.rfile.read(length)
            return json.loads(raw.decode("utf-8") or "{}")

        def do_GET(self) -> None:
            if not self._check_local_request():
                return
            request_path = urlparse(self.path).path
            if request_path in {"/", "/intake.html"}:
                self._serve_file(STATIC_DIR / "intake.html", "text/html; charset=utf-8")
                return
            if request_path.startswith("/static/"):
                requested = STATIC_DIR / request_path.removeprefix("/static/")
                self._serve_static(requested)
                return
            if request_path == "/api/status":
                self._json(
                    HTTPStatus.OK,
                    {
                        "ok": True,
                        "local_only": True,
                        "network_status": "offline/local only",
                        "csrf_token": state.csrf_token,
                        "profile": str(state.profile_path),
                    },
                )
                return
            if request_path == "/api/catalogs":
                self._json(HTTPStatus.OK, {"ok": True, "catalogs": load_catalogs()})
                return
            if request_path == "/api/profile":
                self._json(HTTPStatus.OK, {"ok": True, "profile": load_profile(state.profile_path)})
                return
            if request_path == "/api/incident-runner":
                profile = load_profile(state.profile_path)
                incident = profile.get("incident_timeline") or scenario_template(profile, "suspicious_login")
                self._json(
                    HTTPStatus.OK,
                    {
                        "ok": True,
                        "scenarios": scenario_options(),
                        "incident_timeline": enrich_incident_timeline(profile, incident),
                    },
                )
                return
            if request_path == "/api/evidence":
                self._json(HTTPStatus.OK, {"ok": True, "evidence": load_profile(state.profile_path).get("evidence", [])})
                return
            if request_path == "/api/connectors":
                self._json(HTTPStatus.OK, {"ok": True, "connectors": _connector_status(state.out_dir)})
                return
            if request_path == "/api/packet-links":
                self._json(
                    HTTPStatus.OK,
                    {
                        "ok": True,
                        "links": {
                            "dashboard": "/dashboard.html",
                            "packet": "/review-packet.html",
                            "roadmap": "/30-60-90-roadmap.html",
                            "evidence": "/evidence-binder-index.html",
                            "incident_timeline": "/incident-evidence-timeline.html",
                            "incident_after_action": "/incident-after-action-report.html",
                        },
                    },
                )
                return
            output_path = (state.out_dir / request_path.lstrip("/")).resolve()
            if state.out_dir.resolve() in output_path.parents and output_path.exists() and output_path.is_file():
                self._serve_file(output_path, self._content_type(output_path))
                return
            self._error(HTTPStatus.NOT_FOUND, "Not found.")

        def do_POST(self) -> None:
            if not self._check_post_security():
                return
            try:
                payload = self._read_json()
            except Exception as exc:
                self._error(HTTPStatus.BAD_REQUEST, str(exc))
                return
            try:
                if self.path == "/api/workspaces":
                    profile = create_profile_from_preset(
                        payload.get("practice_name") or "My Practice",
                        payload.get("preset") or "dental",
                        payload.get("size_tier") or "small",
                    )
                    path = safe_profile_path(profile["practice"]["name"])
                    atomic_write_profile(profile, path, action="create")
                    state.profile_path = path
                    state.out_dir = build_packet(path)
                    build_dashboard(path, state.out_dir)
                    self._json(HTTPStatus.OK, {"ok": True, "profile": profile, "profile_path": str(path), "links": self._links()})
                    return
                if self.path == "/api/profile":
                    profile = payload.get("profile")
                    if not isinstance(profile, dict):
                        raise ValueError("profile object required")
                    findings = [finding.to_dict() for finding in find_sensitive_data(profile)]
                    blocked = [finding.to_dict() for finding in blocking_findings(profile)]
                    if blocked:
                        self._json(HTTPStatus.UNPROCESSABLE_ENTITY, {"ok": False, "error": "Sensitive data detected.", "findings": blocked})
                        return
                    validate_profile(profile)
                    profiles_root = (ROOT / "profiles").resolve()
                    if profiles_root not in state.profile_path.resolve().parents:
                        state.profile_path = safe_profile_path(profile["practice"]["name"])
                    atomic_write_profile(profile, state.profile_path, action="save", warnings=findings)
                    self._json(HTTPStatus.OK, {"ok": True, "profile": profile, "findings": findings})
                    return
                if self.path == "/api/suggestions/rebuild":
                    profile = payload.get("profile") or load_profile(state.profile_path)
                    profile = rebuild_profile_suggestions(profile)
                    findings = [finding.to_dict() for finding in find_sensitive_data(profile)]
                    self._json(HTTPStatus.OK, {"ok": True, "profile": profile, "findings": findings})
                    return
                if self.path == "/api/evidence":
                    profile = load_profile(state.profile_path)
                    evidence = payload.get("evidence")
                    if not isinstance(evidence, list):
                        raise ValueError("evidence list required")
                    profile["evidence"] = evidence
                    blocked = [finding.to_dict() for finding in blocking_findings(evidence)]
                    if blocked:
                        self._json(HTTPStatus.UNPROCESSABLE_ENTITY, {"ok": False, "error": "Sensitive data detected.", "findings": blocked})
                        return
                    atomic_write_profile(profile, state.profile_path, action="evidence-save")
                    self._json(HTTPStatus.OK, {"ok": True, "evidence": evidence})
                    return
                if self.path == "/api/evidence/inventory-folder":
                    folder = payload.get("path")
                    if not isinstance(folder, str) or not folder.strip():
                        raise ValueError("path is required")
                    allowed_roots = state.evidence_roots()
                    inventory_path = resolve_allowed_path(folder.strip(), allowed_roots)
                    inventory = inventory_folder(inventory_path, allowed_roots=allowed_roots)
                    self._json(HTTPStatus.OK, {"ok": True, "inventory": inventory})
                    return
                if self.path == "/api/incident-runner/template":
                    scenario_key = str(payload.get("scenario_key") or "suspicious_login")
                    incident = scenario_template(load_profile(state.profile_path), scenario_key)
                    self._json(HTTPStatus.OK, {"ok": True, "incident_timeline": incident})
                    return
                if self.path == "/api/incident-runner":
                    incident = payload.get("incident_timeline")
                    if not isinstance(incident, dict):
                        raise ValueError("incident_timeline object required")
                    findings = [finding.to_dict() for finding in safety_findings(incident)]
                    if findings:
                        self._json(
                            HTTPStatus.UNPROCESSABLE_ENTITY,
                            {
                                "ok": False,
                                "error": "Incident runner text must stay sanitized. Use categories and private evidence references only.",
                                "findings": findings,
                            },
                        )
                        return
                    profile = load_profile(state.profile_path)
                    incident = enrich_incident_timeline(profile, incident)
                    profile["incident_timeline"] = incident
                    validate_profile(profile)
                    atomic_write_profile(profile, state.profile_path, action="incident-runner-save")
                    if payload.get("build", True):
                        state.out_dir = build_packet(state.profile_path)
                        build_dashboard(state.profile_path, state.out_dir)
                    self._json(
                        HTTPStatus.OK,
                        {"ok": True, "profile": profile, "incident_timeline": incident, "links": self._links()},
                    )
                    return
                if self.path == "/api/connectors/wizard":
                    path = write_connector_wizard(state.out_dir / "connector-wizard.html")
                    self._json(HTTPStatus.OK, {"ok": True, "path": str(path), "href": "/connector-wizard.html", "connectors": _connector_status(state.out_dir)})
                    return
                if self.path == "/api/connectors/dns":
                    domain = str(payload.get("domain") or "").strip()
                    if not domain:
                        raise ValueError("domain is required")
                    path = write_connector_bundle(collect_dns_email_auth(domain), _connector_dir(state.out_dir) / "dns.json")
                    self._json(HTTPStatus.OK, {"ok": True, "path": str(path), "connectors": _connector_status(state.out_dir)})
                    return
                if self.path == "/api/connectors/vendor-public":
                    vendor = str(payload.get("vendor") or "").strip()
                    domain = str(payload.get("domain") or "").strip()
                    if not vendor or not domain:
                        raise ValueError("vendor and domain are required")
                    safe_name = "".join(ch if ch.isalnum() or ch in {"-", "_"} else "-" for ch in vendor.lower()).strip("-") or "vendor"
                    path = write_connector_bundle(collect_vendor_public(vendor, domain), _connector_dir(state.out_dir) / f"vendor-{safe_name}.json")
                    self._json(HTTPStatus.OK, {"ok": True, "path": str(path), "connectors": _connector_status(state.out_dir)})
                    return
                if self.path == "/api/connectors/msp-response":
                    response_path = str(payload.get("path") or "").strip()
                    if not response_path:
                        raise ValueError("path is required")
                    safe_path = resolve_allowed_path(response_path, state.evidence_roots())
                    if not safe_path.is_file():
                        raise FileInventoryError("MSP response path must be a file inside the workspace.")
                    path = write_connector_bundle(
                        _import_msp_response(safe_path),
                        _connector_dir(state.out_dir) / "msp-response.json",
                    )
                    self._json(HTTPStatus.OK, {"ok": True, "path": str(path), "connectors": _connector_status(state.out_dir)})
                    return
                if self.path == "/api/connectors/google-workspace/connect":
                    client_id = str(payload.get("client_id") or "").strip()
                    client_secret = str(payload.get("client_secret") or "").strip() or None
                    if not client_id:
                        raise ValueError("client_id is required")
                    result = connect_google_workspace(client_id=client_id, client_secret=client_secret)
                    self._json(HTTPStatus.OK, {"ok": True, "connection": result, "connectors": _connector_status(state.out_dir)})
                    return
                if self.path == "/api/connectors/google-workspace/collect":
                    path = write_connector_bundle(collect_google_workspace(domain=payload.get("domain") or None), _connector_dir(state.out_dir) / "google-workspace.json")
                    self._json(HTTPStatus.OK, {"ok": True, "path": str(path), "connectors": _connector_status(state.out_dir)})
                    return
                if self.path == "/api/connectors/microsoft-365/connect":
                    client_id = str(payload.get("client_id") or "").strip()
                    tenant = str(payload.get("tenant") or "organizations").strip()
                    if not client_id:
                        raise ValueError("client_id is required")
                    result = connect_microsoft_365(client_id=client_id, tenant=tenant)
                    self._json(HTTPStatus.OK, {"ok": True, "connection": result, "connectors": _connector_status(state.out_dir)})
                    return
                if self.path == "/api/connectors/microsoft-365/collect":
                    path = write_connector_bundle(collect_microsoft_365(), _connector_dir(state.out_dir) / "microsoft-365.json")
                    self._json(HTTPStatus.OK, {"ok": True, "path": str(path), "connectors": _connector_status(state.out_dir)})
                    return
                if self.path == "/api/connectors/refresh":
                    paths = _connector_paths(state.out_dir)
                    report = build_refresh_report(paths) if paths else build_refresh_report([])
                    path = write_refresh_report(report, state.out_dir / "evidence-refresh.json")
                    self._json(HTTPStatus.OK, {"ok": True, "path": str(path), "href": "/evidence-refresh.json", "report": report})
                    return
                if self.path == "/api/connectors/views":
                    paths = export_practice_views(state.profile_path, state.out_dir / "views", evidence_paths=_connector_paths(state.out_dir))
                    self._json(HTTPStatus.OK, {"ok": True, "paths": [str(path) for path in paths], "hrefs": [f"/views/{path.name}" for path in paths]})
                    return
                if self.path == "/api/build":
                    evidence_paths = _connector_paths(state.out_dir)
                    if evidence_paths:
                        result = build_sprint(state.profile_path, state.out_dir.parent, evidence_paths=evidence_paths)
                        state.out_dir = result.output_dir
                    else:
                        state.out_dir = build_packet(state.profile_path)
                    dashboard = build_dashboard(state.profile_path, state.out_dir)
                    self._json(HTTPStatus.OK, {"ok": True, "dashboard": str(dashboard), "links": self._links()})
                    return
                self._error(HTTPStatus.NOT_FOUND, "Not found.")
            except (ValidationError, ValueError, KeyError, FileInventoryError, TimeoutError, OSError) as exc:
                self._error(HTTPStatus.BAD_REQUEST, str(exc))

        def _links(self) -> dict[str, str]:
            return {
                "dashboard": "/dashboard.html",
                "packet": "/review-packet.html",
                "command_center": "/sprint-command-center.html",
                "connector_summary": "/connector-evidence-summary.json",
                "evidence_refresh": "/evidence-refresh.json",
                "views": "/views/owner-view.md",
                "roadmap": "/30-60-90-roadmap.html",
                "evidence": "/evidence-binder-index.html",
                "incident_timeline": "/incident-evidence-timeline.html",
                "incident_after_action": "/incident-after-action-report.html",
            }

        def _serve_static(self, path: Path) -> None:
            resolved = path.resolve()
            if STATIC_DIR.resolve() not in resolved.parents or not resolved.exists() or not resolved.is_file():
                self._error(HTTPStatus.NOT_FOUND, "Static file not found.")
                return
            self._serve_file(resolved, self._content_type(resolved))

        def _serve_file(self, path: Path, content_type: str) -> None:
            self._send(HTTPStatus.OK, path.read_bytes(), content_type)

        def _content_type(self, path: Path) -> str:
            if path.suffix == ".html":
                return "text/html; charset=utf-8"
            if path.suffix == ".css":
                return "text/css; charset=utf-8"
            if path.suffix == ".js":
                return "application/javascript; charset=utf-8"
            if path.suffix in {".md", ".txt"}:
                return "text/plain; charset=utf-8"
            if path.suffix == ".json":
                return "application/json; charset=utf-8"
            return "application/octet-stream"

    ensure_workspace_dirs(ROOT)
    return LocalIntakeHandler
