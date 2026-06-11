# Open Decisions — I004 IT Portal

This register lists architecture and delivery decisions surfaced during routing, drafting, and architecture review. Resolved decisions must be updated here and referenced from their home artifacts.

| Decision ID | Question | Options | Recommended | Owner | Blocking? | Home artifact | Required action |
|---|---|---|---|---:|:---:|---|---|
| D-001 | Which CI/CD provider for MVP? | GitHub Actions / Azure DevOps / Other | Select per Platform preference (recommend GitHub Actions if org uses GH) | Product Owner / Platform | No | `architecture/architecture-review.md` | Platform to confirm provider and run integration spike. |
| D-002 | Will portal own any asset types or is ServiceNow authoritative? | ServiceNow authoritative / Portal owns subset | ServiceNow authoritative for MVP (recommended) | Product Owner / Platform | Yes | `architecture/architecture-review.md`, `architecture/architecture-rules.md` | Product Owner to confirm and document contract; update integration design. |
| D-003 | Audit retention policy and storage choice | Short (1 year) / Long (3+ years) / Configurable | Start with 1 year (BRS default) and confirm with Security | Security / Compliance | Yes | `architecture/architecture-review.md`, `engineering-readiness/readiness-check.md` | Security to define retention and storage (WORM/append-only) before handoff. |
| D-004 | Claim-to-role mapping approach for Azure AD | Map groups to roles / Use custom claims | Map groups to roles (simpler) | Platform / Identity | No | `architecture/architecture-review.md`, `input/architecture.md` | Platform to validate in Auth PoC and document mapping table. |

## Summary

- Blocking decisions: 2 (D-002, D-003) — these must be resolved before connector implementation and before handoff respectively.
- Non-blocking decisions: 2 (D-001, D-004).

## Notes

- When a decision is marked Resolved, update the Home artifact(s) listed above to remove any placeholders or DRAFT notices referencing the decision.
- The orchestrator will re-run the stale-artifact check after decisions are resolved.
