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

BDD scenarios: not triggered
