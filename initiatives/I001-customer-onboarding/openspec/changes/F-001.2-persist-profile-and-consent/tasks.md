# Tasks — F-001.2: Persist Profile and Consent

> See `dependency-graph.md` — starts after F-001.1 is deployed.

## Implementation tasks

- [ ] OS-F001.2-001: Create `consents` and `audit_logs` DB tables
  - Requirement: FR-003
  - Acceptance: AC-001, AC-002 — tables present with correct schema
  - Data: creates `consents`, `audit_logs` — see `specs/data.md`
  - Events to emit: none
  - Evidence expected: migration runs cleanly; schema matches `specs/data.md`

- [ ] OS-F001.2-002: Extend `POST /onboarding` to write consent and audit records in same transaction
  - Requirement: FR-003
  - Acceptance: AC-001, AC-002, AC-003 — consent and audit created atomically with profile
  - Architecture constraint: no PII in `audit_logs.details`
  - Data: writes to `consents` and `audit_logs` in same DB transaction as `profiles` insert
  - API: `POST /onboarding` — no response change; internal logic change only
  - Events to emit: none (telemetry handled in F-001.1 and F-005.1)
  - Evidence expected: integration test — POST creates all three rows; forced rollback creates none

## Validation tasks

- [ ] OS-F001.2-V01: Verify no PII in audit_logs.details
  - Acceptance source: `quality-gates/data-contract.md`
  - How to validate: inspect `audit_logs` rows after POST — `details` field must contain no email or phone
  - Evidence expected: DB query result showing non-PII details only

## Done criteria

- [ ] All tasks merged and passing CI
- [ ] Atomicity test passing — no partial writes on rollback
- [ ] No PII confirmed absent from audit_logs.details
- [ ] F-002.1 and F-005.1 teams notified — Wave 3 can start
