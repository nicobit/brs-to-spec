# Tasks — F-001.1: Onboarding Submission

> Scoped to this story only. See `dependency-graph.md` for ordering between stories.

## Implementation tasks

- [ ] OS-F001.1-001: Create `profiles` DB table with field-level encryption
  - Requirement: FR-001, FR-003
  - Acceptance: AC-002 — `profiles` row created with encrypted email/phone
  - Architecture constraint: AR-SEC-002 — email/phone field-level encrypted via KMS; AR-DATA-001 — DB in `eu-south`
  - Data: creates `profiles` table — see `specs/data.md` for full column list
  - API: none
  - Events to emit: none
  - Evidence expected: migration runs cleanly; DB schema matches `specs/data.md`; encryption confirmed via Key Vault key reference in column definition

- [ ] OS-F001.1-002: Implement `POST /onboarding` endpoint
  - Requirement: FR-001
  - Acceptance: AC-001 — returns `202 { id, status: "pending" }`; AC-004 — duplicate email returns 409
  - Architecture constraint: AR-SEC-001 — API key from Key Vault; AR-OBS-001 — W3C trace context, span `onboarding.request`
  - Data: writes to `profiles` — `profile_id`, encrypted `email`, `email_hash`, `phone`, `residency_region = IT`, `status = pending`
  - API: `POST /onboarding` — see `specs/api.md`
  - Events to emit: `onboarding_start` Counter on 202 response
  - Evidence expected: integration test — valid POST returns 202 with UUID; duplicate POST returns 409; `onboarding_start` incremented in staging; `profiles` row present with encrypted columns

## Validation tasks

- [ ] OS-F001.1-V01: Verify `onboarding_start` metric in staging
  - Acceptance source: AC-003, `quality-gates/observability-plan.md`
  - How to validate: POST 5 valid requests; query `onboarding_start` counter in staging
  - Evidence expected: counter value = 5; metric visible in dashboard

- [ ] OS-F001.1-V02: Verify PII encryption in DB
  - Acceptance source: AR-SEC-002, `quality-gates/security-review.md`
  - How to validate: inspect `profiles` row directly — `email` and `phone` columns must not be plaintext
  - Evidence expected: DB query result showing encrypted values; Key Vault key reference present

## Done criteria

- [ ] All implementation tasks merged and passing CI
- [ ] All validation tasks executed with evidence attached
- [ ] `onboarding_start` visible in staging dashboard
- [ ] Key Vault provisioned in `eu-south` (resolves open question #1)
- [ ] F-001.2 team notified — `profiles` table is live, Wave 2 can start
