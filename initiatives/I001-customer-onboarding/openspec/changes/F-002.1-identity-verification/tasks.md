# Tasks — F-002.1: Identity Verification Request

> See `dependency-graph.md` — starts after F-001.2 deployed. Coordinate with F-005.1 on span/signal names.

## Implementation tasks

- [ ] OS-F002.1-001: Create `verification_records` DB table
  - Requirement: FR-002
  - Acceptance: AC-001 — table present with correct schema
  - Data: creates `verification_records` — see `specs/data.md`
  - Events to emit: none
  - Evidence expected: migration runs cleanly; unique index on `idp_request_id`

- [ ] OS-F002.1-002: Implement IDP B outbound client
  - Requirement: FR-002, NFR-001
  - Acceptance: AC-001 — IDP request sent; `verification_records` row created with `status = pending`
  - Architecture constraint: AR-SEC-001 — IDP API key from Key Vault
  - Data: inserts `verification_records` row
  - API: outbound to IDP B — see `specs/api.md#idp-outbound`
  - Events to emit: `idp_requests_total` Counter per attempt; `idp_errors_total` Counter on error with `error_code` label
  - Evidence expected: integration test against IDP sandbox — request sent; row created; error metric fires on simulated timeout

- [ ] OS-F002.1-003: Implement `POST /webhook/idp` handler
  - Requirement: FR-002
  - Acceptance: AC-002, AC-003, AC-004 — valid webhook updates record; invalid rejected; duplicates deduplicated
  - Architecture constraint: AR-SEC-001 — signing secret from Key Vault; HMAC-SHA256 + 5-min window
  - Data: updates `verification_records.status`, `completed_at`; writes `audit_logs`
  - API: `POST /webhook/idp` — see `specs/api.md#webhook`
  - Events to emit: `idp_webhook_received` Counter (label `status: valid/invalid`); `verification_latency_ms` Histogram; `onboarding_success` Counter on verified; `onboarding_failure` Counter on failed (labels `reason`, `stage`)
  - Evidence expected: integration tests for all AC-002–004; metrics visible in staging

- [ ] OS-F002.1-004: Implement `GET /onboarding/{id}/status` endpoint
  - Requirement: FR-001
  - Acceptance: returns current status and verification_status; 404 for unknown id
  - Architecture constraint: AR-SEC-001 — API key auth
  - Data: reads `profiles`, `verification_records`
  - API: `GET /onboarding/{id}/status` — see `specs/api.md#get-status`
  - Events to emit: none
  - Evidence expected: integration test — known id returns status; unknown id returns 404

## Validation tasks

- [ ] OS-F002.1-V01: Verify HMAC signature rejection in staging
  - Acceptance source: AC-003, `quality-gates/security-review.md`
  - How to validate: send webhook with invalid signature → 400; send replay outside 5-min window → 400
  - Evidence expected: test results

- [ ] OS-F002.1-V02: Verify IDP p95 latency measurement available
  - Acceptance source: NFR-001 — p95 < 30 000 ms
  - How to validate: run 20 IDP flows; query `verification_latency_ms` histogram in staging
  - Evidence expected: histogram visible with p95 value recorded

## Done criteria

- [ ] All tasks merged and passing CI
- [ ] Signature validation tested (valid, invalid, replay, duplicate)
- [ ] IDP sandbox integration confirmed
- [ ] All telemetry signals visible in staging
- [ ] F-003.1 and F-004.1 teams notified — Wave 4 can start
