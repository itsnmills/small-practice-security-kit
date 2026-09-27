# Small Practice Security Kit (`spsk`)

[![CI](https://github.com/itsnmills/small-practice-security-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/itsnmills/small-practice-security-kit/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Security: Bandit & pip-audit](https://img.shields.io/badge/security-Bandit%20%7C%20pip--audit-green.svg)](.bandit)
[![Privacy: Zero--PHI Local First](https://img.shields.io/badge/privacy-Zero--PHI%20Local--First-brightgreen.svg)](docs/security-model.md)

**A local-first, privacy-engineered security baseline and readiness packet generator for independent healthcare practices.**

Small healthcare providers—such as dental clinics, physical therapy offices, psychotherapy groups, and ambulatory centers—face increasing ransomware threats, regulatory obligations, and insurance requirements. Enterprise compliance platforms are designed for tech companies and 500-bed hospital networks, burying smaller practices under SaaS subscriptions and compliance theater.

**Small Practice Security Kit** bridges this gap: a practical, offline-first toolkit that maps where electronic Protected Health Information (ePHI) actually travels, audits business associate agreements (BAAs), evaluates AI tool risks, and produces a complete, audit-ready practice assurance packet in minutes.

---

## Key Capabilities

- **Patient Data Outside the EHR Map:** Automatically highlights high-risk "sidecar" data paths—shared inboxes, cloud drives, AI transcribers, billing exports, and local backups—that never enter the chart.
- **Guided Local Web Intake:** Zero-dependency web UI running strictly on `127.0.0.1` with practice presets (Dental, Therapy, Ambulatory), immediate CSRF protection, and Content Security Policy enforcement.
- **Zero-PHI Data Boundary:** Designed strictly for metadata and operational references. Automated safety scanners halt execution if clinical notes, MRNs, SSNs, or credentials are entered.
- **Automated Evidence Connectors:** Evaluates DNS email authentication (SPF, DKIM, DMARC), queries vendor public trust disclosures with SSRF and DNS-rebinding protection, and connects to Google Workspace / Microsoft 365 metadata APIs using secure OS keychain token storage.
- **Practice Assurance Deliverables:** Generates both Markdown and self-contained HTML packets tailored for practice owners, managed service providers (MSPs), insurers, and legal reviewers.

---

## How It Works

```text
┌─────────────────────────────────────────────────────────────┐
│                     1. Local Intake                         │
│  Guided Web UI (open_dashboard.command) or YAML Profile     │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                2. Data Flow & Boundary Mapper               │
│   EHR Sidecars • Shared Drives • Cloud Inboxes • AI Tools   │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                 3. Evidence & Triage Connectors             │
│   DNS Email Auth (SPF/DMARC) • Public Vendor Web Triage     │
│   Google Workspace / M365 Metadata • Folder Inventory       │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│               4. Practice Assurance Packet                  │
│  Readiness Review • Vendor/BAA Matrix • AI Workflow Review  │
│  Ransomware Tabletop • Evidence Binder • 30/60/90 Roadmap   │
└─────────────────────────────────────────────────────────────┘
```

---

## Generated Assurance Deliverables

When a profile is compiled, `spsk` generates an integrated suite of purpose-built review documents in `out/<practice_name>/`:

| Artifact | Purpose & Audience |
|:---|:---|
| [`review-packet.html`](docs/demo/review-packet.html) | **Master Practice Packet:** Standalone, print-ready HTML dossier combining all reviews, maps, and action items. |
| [`readiness-review.md`](docs/demo/review-packet.md) | **Executive Baseline Review:** Plain-English summary of technical, administrative, and physical safeguards. |
| `ephi-flow-map.md` | **Patient Data Outside the EHR:** Detailed map of charts, billing flows, cloud files, inboxes, and AI pipelines. |
| `vendor-baa-review.md` | **Vendor & BAA Register:** BAA execution status, SOC 2 / HITRUST proof points, and AI data-retention terms. |
| `ai-workflow-review.md` | **Clinical AI Governance:** Approved, restricted, and prohibited AI use cases with explicit patient privacy rules. |
| `evidence-binder-index.md` | **Audit Evidence Index:** Date-stamped matrix of policy documents, backup logs, and owner signoffs. |
| `downtime-ransomware-tabletop.md` | **Operational Resilience:** 24–72 hour clinical downtime protocols, paper-charting triggers, and tabletop drills. |
| `incident-evidence-timeline.md` | **Incident Playbook:** Phase-by-phase response timeline with containment checkpoints and forensic handoffs. |
| `owner-msp-handoff.md` | **MSP Coordination Boundary:** Clear division of responsibilities between practice ownership and external IT. |
| `30-60-90-roadmap.md` | **Prioritized Action Plan:** Sequenced milestones to remediate critical gaps without disrupting patient care. |
| `limitations-appendix.md` | **Assurance Scope & Boundaries:** Explicit statement of what the evidence baseline does and does not prove. |

Inspect our sanitized, fictional sample artifacts in [`docs/demo/`](docs/demo/).

---

## Regulatory & Control Foundations

The baseline control matrix in [`catalogs/control_evidence_matrix.yaml`](catalogs/control_evidence_matrix.yaml) structures 30 core controls mapped to authoritative healthcare cybersecurity frameworks:

- **HIPAA Security Rule:** 45 CFR Part 164 Subpart C (Technical, Administrative, and Physical Safeguards).
- **HHS 405(d) HICP:** Health Industry Cybersecurity Practices for Small Healthcare Organizations.
- **HHS HPH & CISA CPGs:** Cross-Sector Cybersecurity Performance Goals for Healthcare and Public Health.
- **NIST SP 800-66r2:** Implementing the Health Insurance Portability and Accountability Act Security Rule.

Every control references an accountable owner lane (`owner`, `msp`, `vendor`, `staff`), acceptable evidence formats, review cadences, and automated status evaluation (`observed`, `needs_review`, `missing`, `stale`).

---

## Quickstart

### Prerequisites

- Python 3.11 or newer
- macOS or Linux

### Installation

```bash
# Clone repository
git clone https://github.com/itsnmills/small-practice-security-kit.git
cd small-practice-security-kit

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 1. Launch the Guided Intake Web Dashboard

On macOS, you can simply double-click `open_dashboard.command`, or start the server via terminal:

```bash
python scripts/serve_dashboard.py --profile samples/family_dental_clinic.yaml
```

Open your browser to `http://127.0.0.1:8765`. The local dashboard allows you to:
- Select a specialized practice preset (e.g., Dental, Family Medicine, Therapy, Ambulatory Surgical).
- Interactively inventory clinical systems, vendor BAAs, and ePHI flow paths.
- Run live DNS and vendor metadata connectors.
- Build, preview, and download the finished assurance packet directly from your browser.

### 2. Build via Command Line

Compile any profile YAML directly to generated packet artifacts:

```bash
python -m small_practice_security_kit build samples/family_dental_clinic.yaml
```

Outputs are written to `out/<profile_slug>/`. Open `out/<profile_slug>/review-packet.html` in any web browser.

### 3. Rapid Assessment ("Sprint Mode")

For a rapid discovery session with an MSP or practice owner:

```bash
python -m small_practice_security_kit sprint samples/family_dental_clinic.yaml --output-root out/sprint
```

Generates a targeted MSP technical inquiry request, an intake summary, and immediate gap flags.

### 4. Automated Audit Gap Evaluation (`audit-report` & `matrix-check`)

Evaluate a practice profile against all 30 controls in the HIPAA, NIST SP 800-66r2, and HHS 405(d) HICP matrix:

```bash
# View human-readable terminal gap summary
python -m small_practice_security_kit audit-report samples/family_dental_clinic.yaml --gaps-only

# Export structured report (markdown, json, or csv)
python -m small_practice_security_kit audit-report samples/family_dental_clinic.yaml --format markdown --out out/audit-report.md

# Enforce strict compliance check in CI/CD (exits with code 1 on high/critical gaps)
python -m small_practice_security_kit matrix-check samples/family_dental_clinic.yaml
```

---

## Security Model & Data Boundary

This project follows an uncompromising **local-first, zero-PHI architecture**:

- **Network Containment:** All intake APIs bind strictly to loopback (`127.0.0.1`). External interfaces are refused.
- **Browser Security:** HTTP responses enforce strict `Content-Security-Policy`, `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, and `Cache-Control: no-store` headers.
- **Cross-Site Request Protection:** All write operations require matching same-origin headers and dynamic per-session CSRF tokens (`X-SPSK-Token`).
- **SSRF & DNS Rebinding Defenses:** Vendor public documentation lookups reject non-HTTP schemes, validate DNS syntax, reject IP literals/internal domains, and resolve target hostnames before connection to block loopback (127.0.0.0/8), RFC 1918 private, link-local, or reserved networks.
- **OS Credential Isolation:** Connector OAuth tokens and API secrets are stored using the native macOS Keychain (streaming credentials via stdin to prevent process argument snooping) or local files restricted to `0600` permissions.
- **Atomic Operations:** Workspace and profile writes use randomized temporary files (`tempfile.NamedTemporaryFile`) with atomic replacement and automatic cleanup on error to avoid partial writes or race conditions.
- **Static Analysis & Supply Chain Verification:** Automated CI tests verify dependencies against the PyPA database with `pip-audit`, execute AST static security scanning with `bandit`, validate secret hygiene with `gitleaks`, and generate CycloneDX SBOMs with `trivy`.

Review our complete [Security Model and Data Boundary Specification](docs/security-model.md).

---

## Development & Testing

Run unit tests, content validation, and security scans locally:

```bash
# Run unit test suite (148 tests)
python -m unittest discover -s tests

# Validate content and safety boundaries
python scripts/validate_content.py

# Run Bandit AST static security analysis
bandit -r small_practice_security_kit -c .bandit

# Audit dependencies for known vulnerabilities
pip-audit
```

---

## Provenance & Engineering Context

`small-practice-security-kit` originated as a hands-on project to translate federal healthcare compliance frameworks (HIPAA Security Rule, HHS 405(d), NIST SP 800-66r2) into an automated, practitioner-friendly evidence engine.

The project blends deep domain research into small-clinic workflows with modern AI-accelerated implementation patterns, backed by automated static analysis, supply chain auditing, and strict security boundaries. Control identifiers within the evidence matrix retain the working prefix `VEL-*` (from the project's early internal codename, *Velari*).

---

## Disclaimer

**Small Practice Security Kit is an operational readiness and documentation toolkit, not legal counsel or certified regulatory advice.** 

Using this kit does not guarantee compliance with the HIPAA Security Rule or state privacy laws, nor does it replace formal Security Risk Analyses (SRAs), independent technical penetration tests, or consultations with qualified healthcare legal and compliance professionals.

---

## License

Released under the [MIT License](LICENSE).
