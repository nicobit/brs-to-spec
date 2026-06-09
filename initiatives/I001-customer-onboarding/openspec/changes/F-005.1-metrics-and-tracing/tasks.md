# Tasks — F-005.1: Metrics and Tracing

> Wave 3 — parallel with F-002.1. Coordinate signal names before starting.

## Implementation tasks

- [ ] OS-F005.1-001: Add tracing middleware — W3C trace context and span creation
  - Requirement: NFR-005
  - Acceptance: AC-002 — end-to-end trace visible; AC-003 — no PII in spans
  - Architecture constraint: AR-OBS-001 — W3C `traceparent` propagated; sampling 100% errors / 10% success
  - Data: none
  - API: middleware added to all Onboarding API handlers — no new endpoints
  - Events to emit: spans `onboarding.request`, `idp.request`, `idp.webhook`, `email.send`
  - Evidence expected: staging trace showing all spans linked under one `traceparent`; no PII in attributes

- [ ] OS-F005.1-002: Wire all counter and histogram signals
  - Requirement: NFR-005
  - Acceptance: AC-001 — all signals emit in staging
  - Data: none
  - API: none — instrumentation added to existing handlers
  - Events to emit: `onboarding_start`, `onboarding_success`, `onboarding_failure` (labels `reason`, `stage`), `verification_latency_ms`, `idp_requests_total`, `idp_errors_total`, `idp_webhook_received` (label `status`)
  - Evidence expected: run 5 test flows; all counters increment; histogram shows p50/p95/p99

- [ ] OS-F005.1-003: Configure staging dashboard
  - Requirement: NFR-005
  - Acceptance: AC-004 — all panels populated
  - Data: none
  - API: none
  - Events to emit: none
  - Evidence expected: screenshot of staging dashboard with all SLO panels populated

## Done criteria

- [ ] All tasks merged and passing CI
- [ ] End-to-end trace confirmed in staging
- [ ] All signals visible in staging dashboard
- [ ] No PII confirmed absent from trace attributes
- [ ] F-005.2 team notified — runbooks and alert hardening (Wave 5) can start after F-005.1 and F-004.1
