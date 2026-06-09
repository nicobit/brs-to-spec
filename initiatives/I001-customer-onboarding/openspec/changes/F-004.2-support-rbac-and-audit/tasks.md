# Tasks — F-004.2: Support RBAC and Audit

> Wave 5 — starts after F-004.1 deployed. Parallel with F-002.2, F-003.2, F-005.2.

## Implementation tasks

- [ ] OS-F004.2-001: Implement RBAC middleware for /support/ routes
  - Requirement: FR-005, AR-SEC-002
  - Acceptance: AC-001, AC-002 — 403 without role; 200/202 with role
  - Architecture constraint: AR-SEC-002 — least-privilege; `support_agent` role only
  - Data: none
  - API: middleware applied to `GET /support/onboarding/{id}` and `POST /support/onboarding/{id}/retry`
  - Events to emit: none
  - Evidence expected: tests — without role → 403; with role → passes through

- [ ] OS-F004.2-002: Ensure audit_log rows written for all support actions
  - Requirement: AR-SEC-002
  - Acceptance: AC-003 — audit rows present for view and retry
  - Data: `audit_logs` rows with `action = support_view` and `support_retry`
  - API: none — audit writes added to existing handlers in F-004.1
  - Events to emit: none
  - Evidence expected: DB query after staging test — rows present with correct actor and entity_id

## Done criteria

- [ ] RBAC enforcement tested (with and without role)
- [ ] Audit log confirmed for all support actions
- [ ] No admin-level access possible via support endpoints
