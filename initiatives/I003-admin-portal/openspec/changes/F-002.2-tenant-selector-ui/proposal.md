# Proposal — F-002.2 Tenant selector UI (frontend)

User story (verbatim):

As a Support Engineer, I want free-text search and tag filters, so I can find environments by tags and names.

Requirement: FR-002

What changes:
- Implement tenant and stage selector in the UI and free-text search controls.

Dependencies:
- depends-on: F-002.1

Acceptance Criteria:
- AC-002

BDD scenarios (from `quality-gates/bdd-scenarios.md`):
| SCN | Type | One-line summary |
|---:|---|---|
| SCN-013 | Happy path | Tenant selector persists selection |
| SCN-014 | No results UX | shows appropriate no-results state |
| SCN-015 | Performance | search returns within target |
| SCN-016 | Authorization | 403 when unauthorized |
