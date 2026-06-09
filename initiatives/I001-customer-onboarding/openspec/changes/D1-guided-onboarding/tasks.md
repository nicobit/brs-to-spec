# Tasks — D1: Guided Onboarding (MVP)

> Implementation checklist for `/opsx:apply`.
> Tasks are ordered — complete each before starting the next.
> Each task is independently reviewable (one PR boundary).

## Implementation tasks

- [ ] OS-001: Create DB schema — profiles, verification_records, consents, audit_logs
  - User story: F-001.2 — system persists profile and consent records for audit and legal traceability
  - Requirement: FR-003
  - Acceptance: schema matches `specs/data.md`; PII fields encrypted; indexes present; migration runs cleanly on empty DB
  - Architecture constraint: AR-SEC-002 — email and phone field-level encrypted via Azure Key Vault KMS
  - Architecture constraint: AR-DATA-001 — DB provisioned in `eu-south` region
  - Data: creates `profiles`, `verification_records`, `consents`, `audit_logs`
  - API: none
  - Events to emit: none (schema only)
  - Evidence expected: migration script in repo; DB schema matches `specs/data.md`; encryption confirmed via Key Vault key reference in column definition

- [ ] OS-002: Implement `POST /onboarding` endpoint
  - User story: F-001.1 — customer submits email/phone to create account
  - Requirement: FR-001, AC-001
  - Acceptance: returns `202 { id, status: "pending" }`; persists profile + consent + audit_log; emits `onboarding_start`
  - Architecture constraint: AR-SEC-001 — API key sourced from Key Vault, not hardcoded
  - Data: writes to `profiles`, `consents`, `audit_logs`
  - API: `POST /onboarding` — see `specs/api.md#post-onboarding`
  - Events to emit: `onboarding_start` (Counter) on 202 response
  - Evidence expected: integration test — POST returns 202, DB rows present, `onboarding_start` metric incremented in staging

- [ ] OS-003: Implement `GET /onboarding/{id}/status` endpoint
  - User story: F-001.1 — customer can check onboarding progress
  - Requirement: FR-001
  - Acceptance: returns current status; 404 for unknown id; auth required
  - Architecture constraint: AR-SEC-001 — API key auth
  - Data: reads from `profiles`, `verification_records`
  - API: `GET /onboarding/{id}/status` — see `specs/api.md#get-status`
  - Events to emit: none
  - Evidence expected: integration test — known id returns status; unknown id returns 404

- [ ] OS-010: Implement IDP B client and verification request
  - User story: F-002.1 — system calls IDP B to verify identity
  - Requirement: FR-002, NFR-001
  - Acceptance: POST /onboarding triggers IDP request; `idp_request_id` stored in `verification_records`; retry/backoff on IDP timeout; no hardcoded credentials
  - Architecture constraint: AR-SEC-001 — IDP API key from Key Vault
  - Data: writes `verification_records` row with status `pending`
  - API: outbound call to IDP B — see `specs/api.md#idp-integration`
  - Events to emit: `idp_errors_total` (Counter) on IDP API error or timeout, with `error_code` label
  - Evidence expected: integration test against IDP sandbox — request sent, `verification_records` row created, error metric incremented on simulated IDP failure
  - Blocker: IDP sandbox credentials must be in Key Vault before this task starts (open question #1)

- [ ] OS-011: Implement IDP webhook handler `POST /webhook/idp`
  - User story: F-002.1 — system receives async IDP callback and progresses onboarding
  - Requirement: FR-002
  - Acceptance: validates HMAC-SHA256 signature; rejects replays outside 5-min window; deduplicates by `idp_request_id`; updates `verification_records`; enqueues notification job on success
  - Architecture constraint: AR-SEC-001 — webhook signing secret from Key Vault
  - Data: updates `verification_records.status`, writes `audit_logs`
  - API: `POST /webhook/idp` — see `specs/api.md#webhook-idp`
  - Events to emit: `idp_webhook_received` (Counter, label `status`); `onboarding_success` on verified; `onboarding_failure` on failed (labels `reason`, `stage`); `verification_latency_ms` Histogram
  - Evidence expected: integration test — valid signed payload updates record and increments `idp_webhook_received`; invalid signature returns 400; duplicate payload deduplicated

- [ ] OS-020: Implement SendGrid notification — onboarding success email
  - User story: F-003.1 — customer receives confirmation email on onboarding success
  - Requirement: FR-004
  - Acceptance: email sent on IDP verification success; template present in SendGrid staging; SendGrid API key from Key Vault; failure logged but does not fail the onboarding flow
  - Architecture constraint: AR-SEC-001 — SendGrid API key from Key Vault
  - Data: no new tables; writes `audit_logs` row for email send action
  - API: outbound SendGrid API call
  - Events to emit: none required for D1 (email delivery tracking is D2)
  - Evidence expected: staging test — IDP success triggers email delivery; template renders correctly; Key Vault key reference confirmed
  - Blocker: SendGrid account and template IDs needed (open question #2)

- [ ] OS-030: Add distributed tracing and correlation ID propagation
  - User story: F-005.1 — SRE can trace a flow end-to-end
  - Requirement: NFR-005
  - Acceptance: W3C trace context header injected at API gateway; propagated to IDP client, webhook handler, job queue; span names match `design.md#observability-requirements`; PII redacted from trace attributes
  - Architecture constraint: AR-OBS-001 — W3C trace context required
  - Data: no schema changes
  - API: no new endpoints; tracing middleware added to existing handlers
  - Events to emit: spans `onboarding.request`, `idp.request`, `idp.webhook`, `email.send`; 100% error sampling, 10% success sampling
  - Evidence expected: staging trace — end-to-end trace visible in tracing tool; correlation ID present on all spans; no PII in span attributes

## Validation tasks

- [ ] OS-V01: Verify conversion rate instrumentation in staging
  - Acceptance source: BRS NFR-005 — conversion ≥ 25%
  - How to validate: run 20 staged onboarding flows; confirm `onboarding_start` and `onboarding_success` counters increment correctly; calculate rate
  - Evidence expected: screenshot of staging dashboard showing counter values and computed rate

- [ ] OS-V02: Verify IDP p95 latency measurement in staging
  - Acceptance source: BRS NFR-001 — verification p95 < 30 000 ms
  - How to validate: run 50 IDP flows against sandbox; query `histogram_quantile(0.95, verification_latency_ms_bucket)` in staging
  - Evidence expected: p95 value recorded; confirm metric is flowing before go-live

- [ ] OS-V03: Verify HMAC-SHA256 webhook signature rejection
  - Acceptance source: `quality-gates/security-review.md` — replay protection
  - How to validate: send webhook with invalid signature → 400; send duplicate payload → 200 but no duplicate DB row
  - Evidence expected: test results attached to OS-011 PR

## Handoff checklist

- [ ] All implementation tasks merged and passing CI
- [ ] All validation tasks executed with evidence attached
- [ ] `onboarding_start`, `onboarding_success`, `onboarding_failure` visible in staging dashboard
- [ ] `verification_latency_ms` histogram flowing in staging
- [ ] IDP webhook: signature validation tested (valid + invalid + replay)
- [ ] Secrets confirmed in Key Vault (`eu-south`): IDP API key, webhook signing secret, SendGrid API key
- [ ] DB: PII encryption confirmed (email, phone field-level encrypted via KMS)
- [ ] Data residency: DB confirmed in `eu-south` region
- [ ] SendGrid: confirmation email delivered in staging; template rendered correctly
- [ ] Open questions 1–3 resolved before coding starts (see `design.md#open-questions`)
- [ ] `specs/` folder copied into code repository alongside this folder
