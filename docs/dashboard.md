# Local Intake Workspace and Dashboard

The kit includes an owner-friendly local intake workspace and HTML dashboard.

The intake workspace is designed for practice owners, office managers, MSPs, and consultants who need a clear workflow instead of a command-line packet generator.

## Open it without using the CLI

On macOS, double-click:

```text
open_dashboard.command
```

That launcher:

- creates `.venv` if needed,
- installs the local requirements,
- builds the review packet,
- builds `dashboard.html`,
- starts a local server at `127.0.0.1:8765`,
- opens the intake workspace in the default browser.

## Open it from a terminal

```bash
.venv/bin/python scripts/serve_dashboard.py --profile samples/family_dental_clinic.yaml
```

Build only:

```bash
.venv/bin/python scripts/serve_dashboard.py --profile samples/family_dental_clinic.yaml --build-only
```

Generated dashboard:

```text
out/family_dental_clinic/dashboard.html
```

## Dashboard sections

The local app is organized around the real practice workflow:

- Intake start and practice presets
- Practice basics
- Systems used
- Vendors and BAAs
- Suggested ePHI flows
- Readiness checklist
- AI workflow safety
- Downtime and incident prep
- Evidence references
- Overview and next best actions
- Readiness review
- ePHI flow map
- Vendor and BAA review
- AI workflow review
- Evidence queue
- Downtime and ransomware tabletop
- Links to generated packet outputs
- HTML companion pages for the roadmap and evidence index

## Safety model

The dashboard is local-first and PHI-avoidant.

Do not enter patient names, MRNs, DOBs, diagnoses, claim details, clinical notes, passwords, private keys, API keys, or real incident contents.

The intended pattern is to reference evidence locations and review decisions, not store sensitive content inside the profile.
