# Tasks — F-003.2: Notification Template Management

> Wave 5 — parallel with F-004.2, F-002.2, F-005.2.

## Implementation tasks

- [ ] OS-F003.2-001: Move SendGrid template IDs and config to Key Vault / environment config
  - Requirement: FR-004
  - Acceptance: AC-001 — template ID updatable without redeploy
  - Architecture constraint: AR-SEC-001 — config in Key Vault, not hardcoded
  - Data: none
  - API: no new endpoints; notification job consumer updated to read template ID from config at runtime
  - Events to emit: none
  - Evidence expected: update template ID in config; trigger staging notification; email uses updated template

- [ ] OS-F003.2-002: Write operator runbook for SendGrid template management
  - Requirement: FR-004
  - Acceptance: AC-002 — runbook present and reviewed
  - Data: none
  - API: none
  - Events to emit: none
  - Evidence expected: runbook file present in repo; reviewed by Product/Ops

## Done criteria

- [ ] Template ID config change confirmed without redeploy
- [ ] Operator runbook reviewed and merged
