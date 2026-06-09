# Proposal — F-001.2 Inventory UI (frontend)

User story (verbatim):

As a Platform Engineer, I want exportable inventory CSV for selected tenant/stage, so that I can analyze inventory offline.

Requirement: FR-001

Why now: provides operator/engineer tooling for offline analysis and supports audits.

What changes:
- Add inventory list UI with pagination, filters (tenant, stage), and CSV export action.

Dependencies:
- depends-on: F-001.1 (Inventory API)
- parallel-with: none
- blocks: none

Acceptance Criteria (verbatim from BRS):

- AC-004: APIs return inventory and action status with proper auth and role checks.

BDD scenarios: not triggered

Out of scope:
- Implementing backend ingestion (covered by F-001.1)

Constraints:
- Must enforce Azure AD auth and tenant scoping in UI calls.

Reference:
- `input/brs.md` (FR-001)
