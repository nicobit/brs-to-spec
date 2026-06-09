# Proposal — F-002.2: Verification Failure Handling

**As a** support agent,
**I want** to see failure details and retry verification,
**so that** users can complete onboarding after a failure.

**Requirement:** FR-005
**Acceptance criteria:** Support UI shows failure reason; retry creates new verification attempt

## Why now

Both the verification flow (F-002.1) and the support UI (F-004.1) are live. This story enriches failure handling — ensuring failure reasons are captured and surfaced clearly, and that retry semantics are correct (rate limiting, audit).

## What changes

- `failure_reason` populated on IDP `failed` callback (webhook handler updated)
- Retry rate limiting added to `POST /support/onboarding/{id}/retry`
- Support UI updated to display failure reason clearly

## Dependencies

| Relationship | Story ID | Reason |
|---|---|---|
| Depends on | F-002.1 | Webhook handler must exist; `verification_records` must have `failure_reason` column |
| Depends on | F-004.1 | Support UI and retry endpoint must exist to enhance |
| Can run in parallel with | F-004.2, F-003.2, F-005.2 | No shared schema changes |
| Blocks | none | Terminal for verification track |

## Acceptance criteria

| AC | Criterion | How to verify | Evidence expected |
|---|---|---|---|
| AC-001 | `failure_reason` populated on IDP failed callback | Send failed webhook; query DB | `verification_records.failure_reason` contains IDP error code |
| AC-002 | Support UI displays failure reason | Staging walkthrough | UI shows failure_reason for failed onboarding |
| AC-003 | Retry rate limited — max 3 per onboarding ID per hour | Send 4 retries | 4th returns 429 |

## Reference artifacts

| Artifact | Path | What to read there |
|---|---|---|
| API contract | `quality-gates/api-contract.md` | IDP error codes for failure_reason population |
| Data contract | `quality-gates/data-contract.md` | `verification_records` schema |
