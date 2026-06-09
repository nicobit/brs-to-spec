# Tasks — F-003.1: Transactional Notifications

> Wave 4 — parallel with F-004.1. Starts after F-002.1 deployed.

## Implementation tasks

- [ ] OS-F003.1-001: Implement notification job consumer and SendGrid client
  - Requirement: FR-004
  - Acceptance: AC-001 — email delivered on verified callback; AC-002 — key from Key Vault; AC-003 — failure doesn't break flow
  - Architecture constraint: AR-SEC-001 — SendGrid API key from Key Vault
  - Data: writes `audit_logs` row with `action = email_sent`
  - API: outbound SendGrid Mail Send API v3; uses sandbox mode in staging
  - Events to emit: none (delivery tracking deferred to F-003.2)
  - Evidence expected: staging test — IDP verified webhook triggers email delivery; SendGrid sandbox mode confirms send; Key Vault key reference confirmed; `audit_logs` row present

## Validation tasks

- [ ] OS-F003.1-V01: Verify notification failure isolation
  - Acceptance source: AC-003
  - How to validate: simulate SendGrid 500 error; confirm onboarding status remains `verified` and flow completes
  - Evidence expected: test result showing status unaffected by notification failure

## Done criteria

- [ ] Task merged and passing CI
- [ ] Email delivered in staging on verified callback
- [ ] SendGrid sandbox mode confirmed; no hardcoded credentials
- [ ] F-003.2 team notified — template management (Wave 5) can start
