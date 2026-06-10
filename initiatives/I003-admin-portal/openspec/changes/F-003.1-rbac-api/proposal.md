# Proposal — F-003.1 RBAC API (backend)

User story (verbatim):

As a Platform Engineer, I want to assign `Operator` role to a user scoped to a tenant/stage, so they can perform allowed actions.

Requirement: FR-003

What changes:
- Add RBAC APIs to read Azure AD group mappings, assign roles, and validate effective permissions.

Dependencies:
- depends-on: F-002.1 (tenant mapping)

Acceptance Criteria:
- AC-001

Constraints:
- Follow least-privilege rules in `architecture/architecture-rules.md` and use service principal role guidance.

BDD scenarios (from `quality-gates/bdd-scenarios.md`):
| SCN | Type | One-line summary |
|---:|---|---|
| SCN-017 | Happy path | Assign Operator role and resolve membership |
| SCN-018 | Invalid group | handles invalid group input |
| SCN-019 | Nested roles | supports nested group role resolution |
| SCN-020 | Audit linkage | assignment writes audit entries |
