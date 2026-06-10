# Proposal — F-005.2 Diagnostics UI (frontend)

User story (verbatim):

As a Support Engineer, I want to view recent errors and traces for an environment, so I can triage incidents faster.

Requirement: FR-005

What changes:
- UI to show recent errors, traces, and provide Log Analytics deep links.

Dependencies:
- depends-on: F-005.1

Acceptance Criteria:
- AC-003

BDD scenarios (from `quality-gates/bdd-scenarios.md`):
| SCN | Type | One-line summary |
|---:|---|---|
| SCN-037 | Happy path | recent errors list shows last 50 events |
| SCN-038 | Backend unavailable | UI handles backend failures |
| SCN-039 | Limit/pagination | recent error paging works |
| SCN-040 | Authorization | 403 when unauthorized |
