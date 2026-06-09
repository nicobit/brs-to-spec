# Tasks — F-002.2: Verification Failure Handling

> Wave 5 — starts after F-002.1 and F-004.1 deployed. Parallel with F-004.2, F-003.2, F-005.2.

## Implementation tasks

- [ ] OS-F002.2-001: Populate failure_reason on IDP failed callback
  - Requirement: FR-005
  - Acceptance: AC-001 — failure_reason set from IDP errorCode on failed webhook
  - Data: updates `verification_records.failure_reason` in webhook handler
  - API: no endpoint changes — webhook handler logic update
  - Events to emit: `onboarding_failure` already emitted by F-002.1; ensure `reason` label populated from `failure_reason`
  - Evidence expected: staging test — send failed webhook with errorCode; DB row shows failure_reason

- [ ] OS-F002.2-002: Add retry rate limiting to POST /support/onboarding/{id}/retry
  - Requirement: FR-005
  - Acceptance: AC-003 — 429 after 3 retries per hour per onboarding ID
  - Data: none (rate limit state in cache/counter)
  - API: rate limiting middleware on `POST /support/onboarding/{id}/retry`
  - Events to emit: none
  - Evidence expected: staging test — 4th retry within 1 hour returns 429

- [ ] OS-F002.2-003: Update support UI to display failure reason clearly
  - Requirement: FR-005
  - Acceptance: AC-002 — failure_reason visible in UI for failed onboarding
  - Data: reads via `GET /support/onboarding/{id}` — no schema changes
  - API: no new endpoints
  - Events to emit: none
  - Evidence expected: staging walkthrough — failed onboarding shows failure_reason in UI

## Done criteria

- [ ] All tasks merged and passing CI
- [ ] Failure reason populated and visible in UI
- [ ] Rate limiting tested (3 retries pass; 4th returns 429)
