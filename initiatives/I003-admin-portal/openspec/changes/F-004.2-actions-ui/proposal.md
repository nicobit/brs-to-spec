# Proposal — F-004.2 Actions UI (frontend)

User story (verbatim):

As a Platform Engineer, I want to trigger reprovision and see job status, so I can monitor progress (MVP: synchronous trigger + status link).

Requirement: FR-004

What changes:
- UI flows for action confirmation, dry-run preview, and job status polling.

Dependencies:
- depends-on: F-004.1

Acceptance Criteria:
- AC-002, AC-004

BDD scenarios (from `quality-gates/bdd-scenarios.md`):
| SCN | Type | One-line summary |
|---:|---|---|
| SCN-029 | UI happy path | action UI triggers job and shows status |
| SCN-030 | Cancel job | cancel flow behaves correctly |
| SCN-031 | Progress UI | progress updates shown |
| SCN-032 | Authorization | UI enforces role checks |
