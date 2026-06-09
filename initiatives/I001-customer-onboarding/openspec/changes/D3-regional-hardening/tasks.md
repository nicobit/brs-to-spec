# Tasks — D3: Regional Hardening and Ops Readiness

> Implementation checklist for `/opsx:apply`.
> **D1 and D2 must be deployed before any D3 task starts.**

## Implementation tasks

- [ ] OS-D3-001: Confirm and lock data residency in production
  - Requirement: OD-001 resolution, `quality-gates/data-contract.md`
  - Acceptance: DB confirmed in `eu-south`; cross-region replication policy documented and approved by Legal; Legal sign-off attached to `input/input-package.md`
  - Data: no schema changes; verify DB region config
  - Events to emit: none
  - Evidence expected: Legal sign-off document in `input/input-package.md`; infrastructure config showing `eu-south` region

- [ ] OS-D3-002: Implement `DELETE /profiles/{profile_id}` — GDPR subject deletion
  - Requirement: Legal / GDPR, `quality-gates/data-contract.md`
  - Acceptance: soft-delete flag set on `profiles`; physical purge scheduled (background job); consents and verification records purged after retention window; export endpoint for subject access requests
  - Architecture constraint: AR-DATA-001 — delete in `eu-south` region only
  - Data: updates `profiles.deleted_at` (soft-delete); background job purges after retention window; cascades to `consents`, `verification_records` per retention schedule
  - API: `DELETE /profiles/{profile_id}` — authenticated, audit-logged
  - Events to emit: none (audit log entry written)
  - Evidence expected: integration test — DELETE sets soft-delete flag; purge job runs in staging; audit log row present

- [ ] OS-D3-010: CRM sync implementation
  - Requirement: OD-004 resolution
  - Acceptance: profile and consent data synced to CRM; data-sharing contract present in `input/contracts/`; PII fields shared confirmed with Legal; sync is one-way (onboarding → CRM)
  - Architecture constraint: AR-SEC-001 — CRM API credentials in Key Vault
  - Data: reads `profiles`, `consents`; no new tables
  - API: outbound CRM sync call (contract TBD — attach to `input/contracts/` before this task starts)
  - Events to emit: CRM sync success/failure counter (name TBD with Platform)
  - Evidence expected: staging sync confirmed; data-sharing contract in `input/contracts/`; Legal sign-off attached
  - Blocker: OD-004 Legal sign-off and CRM data-sharing contract required before this task starts

- [ ] OS-D3-020: Observability hardening — runbooks tested and alert thresholds tuned
  - Requirement: F-005.2, NFR-005
  - Acceptance: P1 runbooks exercised in staging by SRE; alert thresholds tuned to production traffic baseline; pager drill completed; dashboard links attached to `quality-gates/observability-plan.md`
  - Data: no changes
  - API: no changes
  - Events to emit: no new signals; verify existing signals from D1 are firing correctly in production
  - Evidence expected: SRE sign-off on runbooks; pager drill result; dashboard links filled in observability-plan.md

- [ ] OS-D3-030: Availability hardening — AKS multi-AZ and load test
  - Requirement: NFR-002 — 99.9% monthly availability
  - Acceptance: AKS multi-AZ deployment confirmed; load test at 2× expected pilot traffic passes; chaos test (node failure) shows automatic recovery; availability SLO dashboard configured
  - Data: no changes
  - API: no changes
  - Events to emit: no new signals; availability SLO measured via existing `onboarding_start` / `onboarding_success` counters
  - Evidence expected: load test report; chaos test result; AKS config showing multi-AZ node pools

## Validation tasks

- [ ] OS-D3-V01: GDPR deletion end-to-end in staging
  - Acceptance source: Legal / GDPR, `quality-gates/data-contract.md`
  - How to validate: create profile, submit onboarding, then DELETE — verify soft-delete flag set; run purge job — verify physical deletion; confirm no PII remains in logs or traces
  - Evidence expected: DB query before/after purge; log scan showing no PII

- [ ] OS-D3-V02: Availability SLO — 99.9% over 72-hour staging soak
  - Acceptance source: BRS NFR-002
  - How to validate: run sustained load test for 72 hours; measure uptime via `onboarding_start` counter gaps
  - Evidence expected: availability metric from staging dashboard

## Handoff checklist

- [ ] D1 and D2 deployed in production
- [ ] Legal residency sign-off attached to `input/input-package.md`
- [ ] GDPR deletion endpoint operational and tested
- [ ] CRM sync live (if OD-004 Legal sign-off obtained) or explicitly deferred with Legal approval
- [ ] All P1 runbooks tested by SRE and linked to alert rules
- [ ] Alert thresholds tuned and pager drill completed
- [ ] Dashboard links filled in `quality-gates/observability-plan.md`
- [ ] Load test and chaos test results attached
- [ ] Availability SLO confirmed over 72-hour staging soak
