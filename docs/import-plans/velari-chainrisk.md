# Velari ChainRisk Import Plan

`velari-chainrisk` is the attack-chain prioritization add-on for this kit. It answers a different question than the baseline readiness packet:

- the kit asks what evidence the practice has and what gaps should be organized;
- ChainRisk asks which fixes break the most realistic attack chains across vulnerabilities, controls, ePHI proximity, exposure, vendor/BAA gaps, and recovery weakness.

## Source Artifacts

Expected ChainRisk artifacts:

- `chainrisk-workspace.json` - metadata-only JSON workspace export.
- `chainrisk-brief.md` - owner/MSP-ready Markdown brief.
- `chainrisk-kit-adapter.json` - normalized chain/action rows for kit import or manual copy.

Both artifacts must stay non-PHI. Do not import patient identifiers, medical records, credentials, raw logs, raw forensic notes, legal conclusions, or breach determinations.

## Kit Landing Points

Map ChainRisk output into the public kit packet as follows:

| ChainRisk field | Kit destination | Use |
|---|---|---|
| Top chains | `risk-register.csv` and `readiness-review.md` | Explain why combined conditions matter more than isolated severity. |
| Chain-breaking actions | `owner-action-plan.md`, `msp-remediation-brief.md`, `30-60-90-roadmap.md` | Prioritize owner/MSP work by chain reduction. |
| Evidence gaps | `evidence-index.json`, `evidence-binder-index.md`, `evidence-collection-checklist.md` | Track missing proof needed to validate fixes. |
| Source register | `source-map.md` | Preserve external source anchors for CISA KEV, EPSS, HHS, NIST, and related references. |
| JSON workspace | evidence reference path or packet manifest attachment | Keep the full metadata source available without mixing it into prose. |
| Adapter rows | `risk-register.csv`, `owner-action-plan.md`, `msp-remediation-brief.md` | Use normalized ChainRisk rows as the first wired import shape. |

## Manual Import Workflow

1. Generate ChainRisk artifacts:

   ```bash
   npm run export:sample
   ```

2. Copy `chainrisk-workspace.json` into the practice packet evidence-reference folder or list it as a source artifact in `packet-manifest.json`.
3. Use `chainrisk-kit-adapter.json` as the normalized row source for `risk-register.csv`, `owner-action-plan.md`, and `msp-remediation-brief.md`.
4. Copy any remaining evidence gaps into `evidence-collection-checklist.md` and `evidence-binder-index.md`.
5. Link `chainrisk-brief.md` from the packet index as an optional prioritization appendix.

## Future Wired Import

Add a kit command after the JSON schema stabilizes:

```bash
python3 -m small_practice_security_kit import chainrisk chainrisk-workspace.json --profile samples/family_dental_clinic.yaml --out evidence/chainrisk.json
```

The command should validate the ChainRisk workspace, reject sensitive patterns, normalize top chains into the kit evidence model, and produce owner/MSP action rows without overwriting existing packet files.
