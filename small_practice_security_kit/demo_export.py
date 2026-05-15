from __future__ import annotations

import platform
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

from .adapters.evidence_binder import export_binder_index
from .packet import build_packet
from .profile import load_profile
from .safety import assert_safe_tree
from .sensitive_data import blocking_findings


DEMO_GENERATED_AT = "2026-05-15T00:00:00Z"
PACKET_ARTIFACTS = [
    "readiness-review.md",
    "ephi-flow-map.md",
    "vendor-baa-review.md",
    "ai-workflow-review.md",
    "downtime-ransomware-tabletop.md",
    "evidence-binder-index.md",
    "owner-msp-handoff.md",
    "30-60-90-roadmap.md",
    "limitations-appendix.md",
    "review-packet.md",
    "review-packet.html",
    "packet-manifest.json",
]
BINDER_ARTIFACTS = [
    "evidence-binder-index.csv",
    "evidence-binder-index.md",
    "binder-import-notes.md",
    "exchange-records.csv",
    "exchange-records.md",
]
BROWSER_CANDIDATES = [
    "chromium-browser",
    "chromium",
    "google-chrome",
    "google-chrome-stable",
    "chrome",
]


@dataclass(frozen=True)
class DemoExportResult:
    output_dir: Path
    artifacts: list[Path]
    warnings: list[str]


def find_browser() -> str | None:
    for candidate in BROWSER_CANDIDATES:
        browser = shutil.which(candidate)
        if browser:
            return browser
    return None


def _browser_base_command(browser: str) -> list[str]:
    return [browser, "--headless", "--disable-gpu", "--no-sandbox"]


def render_screenshot(html_path: Path, output_path: Path) -> str | None:
    if platform.system() != "Linux":
        return "screenshot skipped: headless browser rendering is only attempted on Linux"
    browser = find_browser()
    if not browser:
        return "screenshot skipped: Chrome/Chromium was not found"
    command = [
        *_browser_base_command(browser),
        "--hide-scrollbars",
        "--window-size=1440,1200",
        f"--screenshot={output_path}",
        html_path.resolve().as_uri(),
    ]
    completed = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
    if completed.returncode != 0 or not output_path.exists():
        return "screenshot skipped: headless browser rendering failed"
    return None


def render_pdf(html_path: Path, output_path: Path) -> str | None:
    browser = find_browser()
    if not browser:
        return "PDF skipped: Chrome/Chromium was not found"
    command = [
        *_browser_base_command(browser),
        f"--print-to-pdf={output_path}",
        html_path.resolve().as_uri(),
    ]
    completed = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
    if completed.returncode != 0 or not output_path.exists():
        return "PDF skipped: headless browser rendering failed"
    return None


def _sensitive_error(profile: dict) -> ValueError | None:
    findings = blocking_findings(profile)
    if not findings:
        return None
    joined = "; ".join(f"{finding.path}: {finding.message}" for finding in findings[:5])
    return ValueError(f"profile contains blocked sensitive data; use references only ({joined})")


def _copy_file(source: Path, destination: Path, artifacts: list[Path]) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    artifacts.append(destination)


def _remove_previous_outputs(output_dir: Path) -> None:
    for name in PACKET_ARTIFACTS:
        path = output_dir / name
        if path.exists():
            path.unlink()
    for name in ["review-packet.png", "review-packet.pdf"]:
        path = output_dir / name
        if path.exists():
            path.unlink()
    binder_dir = output_dir / "evidence-binder-export"
    if binder_dir.exists():
        shutil.rmtree(binder_dir)


def _validate_demo_output(output_dir: Path, artifacts: list[Path]) -> None:
    missing = [path for path in artifacts if not path.exists() or path.stat().st_size == 0]
    if missing:
        names = ", ".join(path.name for path in missing)
        raise ValueError(f"demo export missing generated artifact(s): {names}")
    assert_safe_tree(output_dir)


def export_demo(
    profile_path: Path,
    output_dir: Path,
    *,
    include_pdf: bool = False,
    include_screenshot: bool = True,
) -> DemoExportResult:
    profile = load_profile(profile_path)
    sensitive_error = _sensitive_error(profile)
    if sensitive_error:
        raise sensitive_error

    output_dir.mkdir(parents=True, exist_ok=True)
    _remove_previous_outputs(output_dir)

    artifacts: list[Path] = []
    warnings: list[str] = []
    with tempfile.TemporaryDirectory(prefix="spsk-demo-export-") as temp:
        temp_root = Path(temp)
        packet_dir = build_packet(profile_path, temp_root / "packet", generated_at=DEMO_GENERATED_AT)
        binder_dir = export_binder_index(profile_path, packet_dir / "evidence-binder-export")

        for name in PACKET_ARTIFACTS:
            _copy_file(packet_dir / name, output_dir / name, artifacts)
        for name in BINDER_ARTIFACTS:
            _copy_file(binder_dir / name, output_dir / "evidence-binder-export" / name, artifacts)

    html_path = output_dir / "review-packet.html"
    if include_screenshot:
        screenshot_path = output_dir / "review-packet.png"
        warning = render_screenshot(html_path, screenshot_path)
        if warning:
            warnings.append(warning)
        else:
            artifacts.append(screenshot_path)

    if include_pdf:
        pdf_path = output_dir / "review-packet.pdf"
        warning = render_pdf(html_path, pdf_path)
        if warning:
            warnings.append(warning)
        else:
            artifacts.append(pdf_path)

    _validate_demo_output(output_dir, artifacts)
    return DemoExportResult(output_dir=output_dir, artifacts=artifacts, warnings=warnings)
