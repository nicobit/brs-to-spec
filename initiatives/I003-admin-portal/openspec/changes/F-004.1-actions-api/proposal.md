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

BDD scenarios (from `quality-gates/bdd-scenarios.md`):
| SCN | Type | One-line summary |
|---:|---|---|
| SCN-025 | Short-op happy path | sync start/stop returns success |
| SCN-026 | Async submission | long op returns 202 + job_id |
| SCN-027 | Job lifecycle | job status transitions recorded |
| SCN-028 | Idempotency | repeated requests are safe |
