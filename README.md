# Small Practice Security Kit

**A local-first, PHI-avoidant readiness packet builder for small healthcare practices.**

This is a personal learning project. I built it to teach myself the HIPAA Security Rule and
the practical side of small-practice security by working the problem end to end instead of
just reading about it.

## How this was built, plainly

I lean on AI heavily for the implementation. The part I actually developed here is the
security judgment: deciding what a small practice has to be able to answer, reading the
source material closely enough to know which controls matter, and checking whether the
output holds up. Most of the real work in this repo is domain research, not code.

I would rather say that up front than let a reviewer assume otherwise.

"Velari" appears throughout the source, the control IDs (`VEL-*`), and some doc filenames.
It was a working name I used for this project earlier on. It is not a company, there is no
product, and nothing here is offered as a service. I am leaving the identifiers in place
rather than doing a risky rename across the codebase.

This runs on a fictional `Family Dental Clinic` profile. It has never been run on real
patient data.

## What it does

Small practices usually know they need MFA, backups, BAAs, access reviews, and an incident
plan. The hard part is proving what already exists when the evidence is scattered across
email, vendor portals, tickets, screenshots, and spreadsheets.

This takes intake answers about a practice and produces a readiness packet: where ePHI
actually lives, which vendors need BAAs, which evidence is missing or stale, and a 30/60/90
day action list.

```text
10-minute intake -> patient-data-outside-the-EHR map -> vendor/BAA review
  -> AI workflow review -> downtime/tabletop -> evidence index -> 30/60/90 roadmap
```

The part I think is most useful is the **Patient Data Outside the EHR Map**: inboxes, shared
drives, AI tools, vendor portals, exports, contractors, backups, and billing systems. Once
those flows are visible, the evidence binder, vendor register, and downtime plan stop being
abstract.

## Where the content comes from

The control set lives in [`catalogs/control_evidence_matrix.yaml`](catalogs/control_evidence_matrix.yaml):
30 controls across Technical Safeguards (12), Administrative Safeguards (6),
Vendor/BAA/AI (6), Operational Readiness (4), and Physical Safeguards (2).

Each control maps to an evidence item, an accountable owner, and a freshness state. The
source material is the HIPAA Security Rule (45 CFR Part 164 Subpart C), the HHS 405(d)
Health Industry Cybersecurity Practices, the HHS HPH and CISA Cybersecurity Performance
Goals, and NIST SP 800-66r2.

**Known gap, being worked:** the controls currently reference their source in prose rather
than by citation. I am going through all 30 by hand to add the specific CFR section and
whether each is required or addressable. Until that is finished, treat the mappings as a
reasonable reading rather than an authoritative one.

## Quick start

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/build.py samples/family_dental_clinic.yaml
```

Output lands in `out/family_dental_clinic/`. Open `review-packet.html` to see the result.

Local intake dashboard (macOS: double-click `open_dashboard.command`):

```bash
.venv/bin/python scripts/serve_dashboard.py --profile samples/family_dental_clinic.yaml
```

Tests and content validation:

```bash
.venv/bin/python scripts/validate_content.py
.venv/bin/python -m unittest discover -s tests
```

## Sample output

Checked-in, sanitized artifacts, no PHI:

- [`docs/demo/review-packet.md`](docs/demo/review-packet.md) and [`.html`](docs/demo/review-packet.html)
- [`docs/demo/practice-assurance-packet.md`](docs/demo/practice-assurance-packet.md)
- [`docs/demo/packet-manifest.json`](docs/demo/packet-manifest.json)
- [`docs/security-model.md`](docs/security-model.md) for the safety boundary

## What gets generated

| Output | What it is |
|---|---|
| `readiness-review.md` | Plain-English baseline readiness review |
| `ephi-flow-map.md` | Systems, workflows, vendors, ePHI categories, BAA needs |
| `vendor-baa-review.md` | Vendor and BAA status, SOC 2/HITRUST evidence, AI data-use terms |
| `ai-workflow-review.md` | Allowed, restricted, and prohibited AI workflows |
| `evidence-binder-index.md` | Evidence references, owners, and freshness state |
| `downtime-ransomware-tabletop.md` | Downtime planning and tabletop starter |
| `incident-evidence-timeline.md` | Sanitized incident timeline with decision gates |
| `owner-msp-handoff.md` | Follow-up items, vendor asks, and the handoff boundary |
| `30-60-90-roadmap.md` | Prioritized remediation plan |
| `limitations-appendix.md` | What the packet does and does not prove |

There is also an optional connector layer that imports metadata-only evidence from CSV
exports or read-only Google Workspace and Microsoft 365 APIs. It deliberately avoids
row-level identities, mailbox contents, raw logs, and credentials. See
[`docs/product/evidence-connector-standard.md`](docs/product/evidence-connector-standard.md).

## Safety and data boundary

This repository is **local-first and PHI-avoidant**.

Reasonable inputs: fictional practices, system names, vendor names, role names, ticket
references, evidence folder references, non-sensitive summary notes.

Do **not** enter: patient names, medical record numbers, dates of birth, diagnoses, claim
contents, clinical notes, passwords, API keys, MFA recovery codes, private keys, or real
incident details.

Full boundary: [`docs/security-model.md`](docs/security-model.md).

## What this is not

This does not certify HIPAA compliance, does not constitute legal advice, does not decide
breach-notification duties, and is not a formal Security Risk Analysis, a penetration test,
or a substitute for qualified legal, compliance, security, or incident response
professionals.

It is a learning project and a practical organizer. Nothing more than that.

## License

MIT. See [LICENSE](LICENSE).
