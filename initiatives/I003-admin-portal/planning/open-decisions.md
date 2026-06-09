 # Open Decisions

 | Decision ID | Question | Owner | Blocking | Status | Home artifact |
 |---|---|---|---:|---|---|
 | OD-001 | Validate tenant → subscription mapping for target customers | Architect / Product | Yes | Resolved | architecture/architecture-review.md |
 | OD-002 | Action Orchestrator execution model for long-running operations | Architect / Platform | Yes | Resolved | architecture/architecture-review.md |
 | OD-003 | Service principal role set and provisioning guidance | Architecture / Ops | Yes | Resolved | architecture/architecture-review.md |

 Generated from `architecture/architecture-review.md` on 2026-06-09.

 ## Resolutions

 - **OD-001 — Tenant → Subscription mapping**: Resolved to *One-to-one mapping* for MVP. Rationale: reduces complexity and blast radius. Resolved by: Nico (PO). Date: 2026-06-09.
 - **OD-002 — Action Orchestrator model**: Resolved to *Hybrid model* (sync for short ops; async job queue for long ops). Resolved by: Nico (PO). Date: 2026-06-09.
 - **OD-003 — Service principal role & provisioning**: Resolved to *custom `AdminPortalActionRunner` role + per-subscription service principal (MVP)*. Resolved by: Nico (PO). Date: 2026-06-09.
