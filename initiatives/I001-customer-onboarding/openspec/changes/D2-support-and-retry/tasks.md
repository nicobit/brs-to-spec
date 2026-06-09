# Tasks — D2: Support Tools and Retry Flows

> Implementation checklist for `/opsx:apply`.
> Tasks are ordered — D1 must be deployed before any D2 task starts.
> Each task is independently reviewable (one PR boundary).

## Implementation tasks

- [ ] OS-D2-001: Add `failure_reason` column to `verification_records`
  - User story: F-002.2 — support agent sees failure details
  - Requirement: FR-005
  - Acceptance: column added via zero-downtime migration; populated when IDP webhook delivers `result = failed`
  - Architecture constraint: AR-DATA-001 — migration runs in `eu-south` DB
  - Data: alters `verification_records` — adds `failure_reason string nullable`
  - API: no new endpoints; D1 webhook handler updated to write `failure_reason` on failure
  - Events to emit: none
  - Evidence expected: migration runs cleanly; staging test — failed IDP webhook populates `failure_reason`

- [ ] OS-D2-010: Implement RBAC for support endpoints
  - User story: F-004.2 — operator has role-based access; actions are accountable
  - Requirement: FR-005, AR-SEC-002
  - Acceptance: `support_agent` role claim checked on all `/support/` endpoints; 403 returned if missing; role source confirmed (see open question #2)
  - Architecture constraint: AR-SEC-002 — least-privilege; all actions audit-logged
  - Data: no schema changes
  - API: middleware added to Onboarding API for support routes
  - Events to emit: none
  - Evidence expected: test — request without role → 403; request with role → passes to handler; audit log row written

- [ ] OS-D2-020: Implement `GET /support/onboarding/{id}` endpoint
  - User story: F-004.1 — support agent views onboarding state and verification details
  - Requirement: FR-005
  - Acceptance: returns `status`, `verification_status`, `failure_reason`; does not expose `email` or `phone`; RBAC enforced; audit log written
  - Architecture constraint: AR-SEC-002 — PII not in response; audit log on every call
  - Data: reads `profiles`, `verification_records`
  - API: `GET /support/onboarding/{id}` — see `specs/api.md#get-support-view`
  - Events to emit: `support_views_total` Counter on 200 response
  - Evidence expected: integration test — known id returns correct state; PII fields absent from response; audit_log row present

- [ ] OS-D2-030: Implement `POST /support/onboarding/{id}/retry` endpoint
  - User story: F-002.2 — support agent triggers verification retry
  - Requirement: FR-005
  - Acceptance: creates new `verification_records` row; triggers new IDP request; returns 202; RBAC enforced; audit log written with `reason` field
  - Architecture constraint: AR-SEC-001 — IDP API key from Key Vault (reuse D1); AR-SEC-002 — audit log required
  - Data: inserts new `verification_records` row; writes `audit_logs` row with action `support_retry` and `reason`
  - API: `POST /support/onboarding/{id}/retry` — see `specs/api.md#post-retry`; outbound IDP call same as D1 OS-010
  - Events to emit: `support_retries_total` Counter on 202 response
  - Evidence expected: integration test — retry creates new verification record; IDP call made to sandbox; `support_retries_total` incremented; audit log row present with `reason`

- [ ] OS-D2-040: Implement support UI — onboarding search and retry view
  - User story: F-004.1 — support agent searches by onboarding ID and triggers retries
  - Requirement: FR-005
  - Acceptance: search by onboarding ID; display status, verification status, failure reason; retry button calls `POST /support/onboarding/{id}/retry`; access restricted to `support_agent` role
  - Architecture constraint: AR-SEC-002 — RBAC enforced at UI and API layer
  - Data: reads via support API endpoints (no direct DB access)
  - API: consumes `GET /support/onboarding/{id}` and `POST /support/onboarding/{id}/retry`
  - Events to emit: none (telemetry emitted by API layer)
  - Evidence expected: staging walkthrough — search returns result; retry button triggers retry and shows updated status; blocked when role absent
  - Blocker: open question #1 (standalone app vs admin panel) must be resolved first

- [ ] OS-D2-050: SendGrid template management
  - User story: F-003.2 — operator manages notification templates
  - Requirement: FR-004
  - Acceptance: SendGrid templates configurable without code deploy; template IDs stored in Key Vault or config; staging templates verified
  - Architecture constraint: AR-SEC-001 — SendGrid API key from Key Vault
  - Data: no schema changes
  - API: no new endpoints
  - Events to emit: none
  - Evidence expected: template update without redeploy; staging confirmation email renders correctly after template change

## Validation tasks

- [ ] OS-D2-V01: Verify RBAC enforcement end-to-end in staging
  - Acceptance source: AR-SEC-002, `quality-gates/security-review.md`
  - How to validate: attempt all support endpoints without `support_agent` role → all return 403; with role → all succeed
  - Evidence expected: test results attached to OS-D2-010 PR

- [ ] OS-D2-V02: Verify audit log completeness
  - Acceptance source: AR-SEC-002
  - How to validate: execute one view and one retry action; confirm `audit_logs` has rows for `support_view` and `support_retry` with correct actor, entity_id, and timestamp
  - Evidence expected: DB query result showing audit rows

## Handoff checklist

- [ ] D1 deployed and DB schema live in target environment
- [ ] All D2 implementation tasks merged and passing CI
- [ ] All D2 validation tasks executed with evidence attached
- [ ] RBAC confirmed: 403 without role, 200/202 with role
- [ ] Audit log confirmed for all support actions
- [ ] `support_retries_total` and `support_views_total` visible in staging dashboard
- [ ] SendGrid templates updated and verified in staging
- [ ] Open questions 1–2 resolved before coding starts (see `design.md#open-questions`)
- [ ] `specs/` folder copied into code repository alongside this folder
