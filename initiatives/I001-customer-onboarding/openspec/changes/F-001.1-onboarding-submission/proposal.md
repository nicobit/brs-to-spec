# Proposal — F-001.1: Onboarding Submission

> OpenSpec change proposal for one user story. Drive implementation with `/opsx:apply` against this folder.
> Copy this folder into the target code repository before applying.

## User story

**As a** new retail customer,
**I want** to submit my email or phone to create an account,
**so that** I can start onboarding.

**Requirement:** FR-001
**Acceptance criteria:** AC-001 in `input/brs.md`

## Why now

This is the entry point of the entire onboarding flow — nothing else can start until this endpoint exists and the profile record is created. Wave 1: no dependencies.

## What changes

- New `POST /onboarding` REST endpoint — accepts email/phone, returns `202 { id, status: "pending" }`
- New `profiles` DB table — stores profile ID, encrypted email/phone, residency region, status
- `onboarding_start` Counter metric emitted on every successful submission

## Dependencies

| Relationship | Story ID | Reason |
|---|---|---|
| Depends on (must be deployed first) | none | Wave 1 — no dependencies |
| Can run in parallel with | none | First story |
| Blocks (cannot start until this is done) | F-001.2 | F-001.2 persists consent records linked to the profile created here |

## Acceptance criteria

| AC | Criterion | How to verify | Evidence expected |
|---|---|---|---|
| AC-001 | `POST /onboarding` returns `202 { id, status: "pending" }` for valid input | Integration test — POST with valid email | Test result showing 202 response with UUID |
| AC-002 | `profiles` row created with encrypted email/phone | DB query after POST | Row present; email/phone columns encrypted via KMS key reference |
| AC-003 | `onboarding_start` counter incremented | Query metric in staging | Counter value increases by 1 per successful POST |
| AC-004 | Duplicate email returns 409 | Integration test — POST same email twice | Second POST returns 409 `ALREADY_EXISTS` |

## Constraints inherited from upstream

| Constraint | Source artifact |
|---|---|
| PII (email, phone) encrypted at rest via Azure Key Vault KMS | `architecture/architecture-rules.md` AR-SEC-002 |
| No hardcoded credentials — API key from Key Vault | `architecture/architecture-rules.md` AR-SEC-001 |
| Italy residency — DB provisioned in `eu-south` | `quality-gates/data-contract.md` |
| W3C trace context header injected at entry point | `architecture/architecture-rules.md` AR-OBS-001 |

## Reference artifacts

| Artifact | Path | What to read there |
|---|---|---|
| Architecture rules | `architecture/architecture-rules.md` | AR-SEC-001, AR-SEC-002, AR-OBS-001 |
| Data contract | `quality-gates/data-contract.md` | Full `profiles` table DDL, PII mapping, encryption approach |
| API contract | `quality-gates/api-contract.md` | Full endpoint spec, error codes, rate limits |
| Security review | `quality-gates/security-review.md` | PII and encryption checklist |
| Observability plan | `quality-gates/observability-plan.md` | `onboarding_start` signal definition |
