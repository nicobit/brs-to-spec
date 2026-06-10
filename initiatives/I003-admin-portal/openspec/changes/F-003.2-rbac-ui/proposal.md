# Proposal — F-003.2 RBAC UI (frontend)

User story (verbatim):

As an Auditor, I want to view role assignment history, so I can see who changed roles and when.

Requirement: FR-003

What changes:
- UI to manage and view role mappings and history per tenant.

Dependencies:
- depends-on: F-003.1

Acceptance Criteria:
- AC-001

BDD scenarios (from `quality-gates/bdd-scenarios.md`):
| SCN | Type | One-line summary |
|---:|---|---|
| SCN-021 | Happy path | Auditor views role assignment history |
| SCN-022 | Validation error | UI handles invalid input |
| SCN-023 | Authorization | RBAC enforcement in UI |
| SCN-024 | History paging | paging through history works |
