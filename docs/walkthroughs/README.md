# Walkthrough Posts

These are recruiter/client-facing walkthrough drafts that turn the checked-in synthetic demo into practical proof of work.

## Output and publishing notes

- Posts live in this folder and should stay synthetic, safe to publish, and consistent with the repository safety model.
- Each post links to checked-in artifacts under `docs/demo/` and uses only non-PHI references from the synthetic sample.
- Before publishing:
  - Run `python scripts/validate_content.py`.
  - Run the repo test suite (`python -m unittest discover -s tests`) and confirm green.
  - Do a manual overclaim scan for compliance/legal conclusions.

## Draft index

1. [How a Small Clinic Can Inventory ePHI Flows Without Uploading PHI](post-1-ephi-flow-map-local-first.md)
2. [Why Healthcare AI Governance Starts With Vendors, BAAs, and Evidence](post-2-ai-governance-vendors-baa.md)
3. [A Local-First Security Review Packet for Small Healthcare Practices](post-3-local-first-review-packet.md)

## Reuse checklist

Each post should retain:

- practical framing for owners/MSPs,
- a clear “what this does not prove” section,
- no legal guarantees or audit/compliance certificates,
- no client-specific details, PHI, credentials, incident stories, or unverifiable claims.
