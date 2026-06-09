# Test Strategy

| Test area | Why | Evidence expected |
|---|---|---|
| integration tests for onboarding submission | validate the happy path for D1 | successful submission and review routing evidence |
| negative tests for unauthorized document access | protect sensitive upload flow | rejection evidence and authorization behavior |
| regression tests for audit event emission | preserve existing auditability guarantees | auditable event evidence after successful submission |

## Notes

- keep D1 validation aligned with BDD scenarios
- verify both functional behavior and operational evidence
