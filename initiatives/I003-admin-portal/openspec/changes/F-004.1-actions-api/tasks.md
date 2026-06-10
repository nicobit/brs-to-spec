# Tasks — F-004.1 Actions API (backend)

OS-F-004.1-001: Implement `POST /actions/{actionId}/run` with sync/async logic
- Requirement: FR-004
- AC: AC-002, AC-004

OS-F-004.1-002: Implement job enqueue and `GET /jobs/{jobId}` status endpoint

OS-F-004.1-003: Add integration tests validating 200 (sync) and 202 (async) flows, and audit entries

Done criteria:
- ACs validated; API contract conformance; Metrics emitted
- BDD scenarios: SCN-025, SCN-026, SCN-027, SCN-028 pass in CI
