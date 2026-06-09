# Proposal — F-004.1 Actions API (backend)

User story (verbatim):

As an IT Operator, I want to start/stop an environment and receive immediate status, so I know the action succeeded or failed.

Requirement: FR-004

What changes:
- Implement `POST /actions/{actionId}/run` supporting sync/async pattern and `GET /jobs/{jobId}` status endpoint.

Dependencies:
- depends-on: F-002.1 (tenant mapping), F-001.1 (inventory context)

Acceptance Criteria:
- AC-002, AC-004

Constraints:
- Follow API contract in `quality-gates/api-contract.md` (2026-06-09)

BDD scenarios: not triggered
