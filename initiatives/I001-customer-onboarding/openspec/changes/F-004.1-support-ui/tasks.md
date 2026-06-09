# Tasks — F-004.1: Support UI

> Wave 4 — parallel with F-003.1. Starts after F-002.1 deployed.

## Implementation tasks

- [ ] OS-F004.1-001: Add `failure_reason` column to `verification_records`
  - Requirement: FR-005
  - Acceptance: AC-001 — failure_reason surfaced in GET response
  - Data: alters `verification_records` — adds `failure_reason string nullable`; zero-downtime migration
  - Events to emit: none
  - Evidence expected: migration runs cleanly; column present; populated on IDP failed callback

- [ ] OS-F004.1-002: Implement `GET /support/onboarding/{id}` endpoint
  - Requirement: FR-005
  - Acceptance: AC-001 — returns status, verification_status, failure_reason; no PII
  - Data: reads `profiles`, `verification_records`
  - API: `GET /support/onboarding/{id}`
  - Events to emit: `support_views_total` Counter on 200
  - Evidence expected: integration test — response contains correct fields; email/phone absent

- [ ] OS-F004.1-003: Implement `POST /support/onboarding/{id}/retry` endpoint
  - Requirement: FR-005
  - Acceptance: AC-002 — new verification record created; IDP call made
  - Architecture constraint: AR-SEC-001 — IDP key from Key Vault (reuse existing)
  - Data: inserts new `verification_records` row; writes `audit_logs` row
  - API: `POST /support/onboarding/{id}/retry`
  - Events to emit: `support_retries_total` Counter on 202
  - Evidence expected: integration test — new row created; IDP sandbox call made; audit log present

- [ ] OS-F004.1-004: Implement support UI view
  - Requirement: FR-005
  - Acceptance: AC-003 — UI displays state; retry button works
  - Data: reads via support API — no direct DB access
  - API: consumes GET and POST support endpoints
  - Events to emit: none
  - Evidence expected: staging walkthrough — search returns result; retry triggers new verification

## Done criteria

- [ ] All tasks merged and passing CI
- [ ] Support API endpoints tested (happy path + 404)
- [ ] No PII confirmed absent from GET response
- [ ] Audit log rows present for view and retry actions
- [ ] F-004.2 and F-002.2 teams notified — Wave 5 can start
