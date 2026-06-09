# Proposal — F-001.1 Inventory API (backend)

User story (verbatim):

As an IT Operator, I want to see a paginated list of environments by tenant and stage, so that I can find an environment quickly.

Requirement: FR-001

Why now: foundational data surface for inventory-driven features and actions.

What changes:
- Add `GET /inventory` paginated endpoint supporting `tenantId`, `stage`, `page`, and `pageSize`.
- Inventory ingestion pipeline to populate the inventory store for sample subscription IDs.

Dependencies:
- depends-on: F-002.1 (Tenant mapping API) — for tenant->subscription scoping
- parallel-with: none
- blocks: F-001.2 (Inventory UI)

Acceptance Criteria (verbatim from BRS):

- AC-004: APIs return inventory and action status with proper auth and role checks.

BDD scenarios: not triggered

Out of scope:
- UI rendering and pagination controls (covered by F-001.2)

Constraints:
- AR: Authentication: All UI and API traffic MUST use Azure AD. (see `architecture/architecture-rules.md`)
- AR: Idempotency and dry-run rules apply to mutating endpoints (not directly to GET).

Reference:
- `input/brs.md` (FR-001, AC-004)
- `architecture/architecture-rules.md`
