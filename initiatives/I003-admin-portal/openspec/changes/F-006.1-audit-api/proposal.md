# Proposal — F-006.1 Audit API (backend)

User story (verbatim):

As an Auditor, I want an append-only audit view of admin actions, so I can generate compliance reports.

Requirement: FR-006

What changes:
- Implement append-only audit store APIs and export endpoint for CSV/JSON.

Dependencies:
- depends-on: F-004.1 (actions API) to receive audit events

Acceptance Criteria:
- AC-006

BDD scenarios (from `quality-gates/bdd-scenarios.md`):
| SCN | Type | One-line summary |
|---:|---|---|
| SCN-033 | Happy path | probe/link happy path (shared) |
| SCN-041 | Happy path | append-only audit entries written |
| SCN-042 | Immutability negative | ensure audit entries are immutable |
| SCN-043 | Export masking | export respects masking rules |
| SCN-044 | Boundary | export size handling |
