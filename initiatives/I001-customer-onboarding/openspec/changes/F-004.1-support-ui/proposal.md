# Proposal — F-004.1: Support UI

**As a** support agent,
**I want** to view onboarding state and retry steps,
**so that** I can resolve failures quickly.

**Requirement:** FR-005
**Acceptance criteria:** Support agent can search by onboarding ID and view status and failure reason

## Why now

Verification flow is live (F-002.1). Failures will occur in staging and production — support agents need tooling to diagnose and act on them. RBAC is added in F-004.2 immediately after.

## What changes

- New `GET /support/onboarding/{id}` endpoint — returns onboarding state for support view (no raw PII)
- New `POST /support/onboarding/{id}/retry` endpoint — triggers new IDP verification
- Support UI web view — search by onboarding ID, display state, retry button
- `failure_reason` column added to `verification_records`

## Dependencies

| Relationship | Story ID | Reason |
|---|---|---|
| Depends on | F-002.1 | Reads `verification_records` table; retry calls IDP B client |
| Can run in parallel with | F-003.1 | No shared schema or API |
| Blocks | F-004.2 | RBAC and audit added to support endpoints created here |
| Blocks | F-002.2 | Failure details surfaced through support UI |

## Acceptance criteria

| AC | Criterion | How to verify | Evidence expected |
|---|---|---|---|
| AC-001 | `GET /support/onboarding/{id}` returns status and failure_reason | Integration test | Response contains status, verification_status, failure_reason; no email/phone |
| AC-002 | `POST /support/onboarding/{id}/retry` creates new verification record | Integration test | New `verification_records` row; IDP call made |
| AC-003 | Support UI displays result of GET and allows retry | Staging walkthrough | UI shows state; retry button triggers POST |

## Constraints inherited from upstream

| Constraint | Source artifact |
|---|---|
| PII (email, phone) not exposed in support API response | `quality-gates/security-review.md` |
| All support actions audit-logged | `architecture/architecture-rules.md` AR-SEC-002 |

## Reference artifacts

| Artifact | Path | What to read there |
|---|---|---|
| Security review | `quality-gates/security-review.md` | PII exposure rules for support endpoints |
| Data contract | `quality-gates/data-contract.md` | `verification_records` schema |
| API contract | `quality-gates/api-contract.md` | IDP B client reuse for retry |
