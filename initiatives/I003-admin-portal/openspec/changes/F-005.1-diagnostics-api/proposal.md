# Proposal — F-005.1 Diagnostics API (backend)

User story (verbatim):

As an IT Operator, I want a diagnostics probe that returns health and a quick link to Log Analytics, so I can investigate issues.

Requirement: FR-005

What changes:
- Implement diagnostics probe endpoints and generator for Log Analytics deep links per resource.

Dependencies:
- depends-on: F-001.1 (inventory)

Acceptance Criteria:
- AC-003

BDD scenarios (from `quality-gates/bdd-scenarios.md`):
| SCN | Type | One-line summary |
|---:|---|---|
| SCN-033 | Happy path | diagnostics probe returns health and link |
| SCN-034 | Link correctness | diagnostics include correct deep-link |
| SCN-035 | Boundary | query size handling |
| SCN-036 | Authorization | 403 when unauthorized |
