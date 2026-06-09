# Proposal — F-001.2: Persist Profile and Consent

**As the** system,
**I want** to persist profile and consent records for audit and legal traceability,
**so that** all user choices and identity data are stored durably and compliantly.

**Requirement:** FR-003
**Acceptance criteria:** `quality-gates/data-contract.md` — consents and audit_logs table spec

## Why now

Profile record exists after F-001.1. This story adds the consent and audit records that must be created atomically with the profile — required before IDP verification (F-002.1) can proceed.

## What changes

- New `consents` DB table — stores consent type, grant status, timestamp, and source
- New `audit_logs` DB table — stores every system action for compliance
- `POST /onboarding` handler (from F-001.1) extended to write consent and audit records in the same transaction

## Dependencies

| Relationship | Story ID | Reason |
|---|---|---|
| Depends on | F-001.1 | `profiles` table and `POST /onboarding` endpoint must exist |
| Can run in parallel with | none | Sequential with F-001.1 |
| Blocks | F-002.1 | IDP verification reads profile; consent must be persisted first |
| Blocks | F-005.1 | Telemetry instruments the full onboarding_start event including consent |

## Acceptance criteria

| AC | Criterion | How to verify | Evidence expected |
|---|---|---|---|
| AC-001 | `consents` row created on POST with correct type and grant status | DB query after POST | Row present with `consent_type = terms`, `granted = true` |
| AC-002 | `audit_logs` row created for `create` action on profile | DB query | Row with `action = create`, `entity = profile`, no PII in `details` |
| AC-003 | Consent and profile created atomically — neither persists if the other fails | Integration test with forced DB error | Both rows absent on rollback |

## Constraints inherited from upstream

| Constraint | Source artifact |
|---|---|
| No PII in `audit_logs.details` field | `quality-gates/data-contract.md` |
| Audit logs retained minimum 1 year | `quality-gates/data-contract.md` |

## Reference artifacts

| Artifact | Path | What to read there |
|---|---|---|
| Data contract | `quality-gates/data-contract.md` | Full `consents` and `audit_logs` table DDL, retention rules |
| Security review | `quality-gates/security-review.md` | Audit logging requirements |
