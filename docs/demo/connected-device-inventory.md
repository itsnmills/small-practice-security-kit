# Connected Device Inventory

This worksheet extends the ePHI flow map for small-practice IoMT and medical-device-adjacent systems. It is a readiness worksheet, not a live network scan, penetration test, FDA safety assessment, or compliance determination.

## Connected Device Worksheet

| Device / system | Vendor | Network location or access path | PHI handled | Firmware / patch owner | Default credential status | Downtime fallback | Safety notice review |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Cloud EHR | Example EHR Vendor | browser | creates, receives, maintains, transmits | Practice Owner | unknown - verify default credentials disabled | manual workflow or restore path to confirm | review vendor safety/security notices and patch advisories |
| Billing Portal | Example Billing Vendor | browser | receives, maintains, transmits | Billing Lead | unknown - verify default credentials disabled | manual workflow or restore path to confirm | review vendor safety/security notices and patch advisories |
| Shared Drive | Workspace Provider | managed endpoint and browser | maintains | Office Manager | unknown - verify default credentials disabled | manual workflow or restore path to confirm | review vendor safety/security notices and patch advisories |
| Dental Imaging Workstation | Example Imaging Vendor | local workstation and vendor support session | creates and maintains | Lead Dental Assistant | unknown - verify default credentials disabled | manual workflow or restore path to confirm | review vendor safety/security notices and patch advisories |

## Evidence To Request

- Current device or workstation inventory export, with owner and date observed.
- Vendor support path, remote-access method, and account owner.
- Firmware, patch, or managed endpoint status reference.
- Default credential exception review and compensating-control note.
- Backup/restore or downtime fallback for devices needed during patient care.
- Vendor safety/security notice review cadence and owner.

## Boundary

Record only reference IDs, owners, and short status summaries here. Keep serial numbers, screenshots, network diagrams, private IPs, raw logs, credentials, and patient details in the private/offline evidence binder.
