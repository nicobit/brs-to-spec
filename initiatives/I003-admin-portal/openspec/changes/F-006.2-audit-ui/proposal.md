# Proposal — F-006.2 Audit UI (frontend)

User story (verbatim):

As an IT Operator, I want to see the last actor and timestamp for environment actions, so I can understand recent changes.

Requirement: FR-006

What changes:
- UI components to view audit entries and export reports.

Dependencies:
- depends-on: F-006.1

Acceptance Criteria:
- AC-006

BDD scenarios (from `quality-gates/bdd-scenarios.md`):
| SCN | Type | One-line summary |
|---:|---|---|
| SCN-045 | UI happy path | audit UI shows append-only entries |
| SCN-046 | Authorization | UI enforces access control |
| SCN-047 | No-results negative | handles empty state |
| SCN-048 | Observability correlation | audit links to observability traces |
