# Proposal — F-002.1: Identity Verification Request

**As the** onboarding system,
**I want** to call Identity Provider B to verify identity,
**so that** only verified users progress through onboarding.

**Requirement:** FR-002, NFR-001
**Acceptance criteria:** `quality-gates/api-contract.md` — IDP integration spec

## Why now

Profile and consent are persisted (F-001.2). IDP verification is the next step in the onboarding flow — the system must initiate verification immediately after profile creation.

## What changes

- New `verification_records` DB table
- IDP B client — outbound HTTPS call to trigger async verification
- Webhook handler `POST /webhook/idp` — receives async IDP callback, validates HMAC-SHA256 signature, updates verification record
- `GET /onboarding/{id}/status` endpoint — allows polling of current onboarding state
- Background job queue — retries failed IDP calls
- Telemetry: `idp_requests_total`, `idp_errors_total`, `idp_webhook_received`, `verification_latency_ms`, `onboarding_success`, `onboarding_failure`

## Dependencies

| Relationship | Story ID | Reason |
|---|---|---|
| Depends on | F-001.2 | Reads `profiles` table; consent must be persisted before verification starts |
| Can run in parallel with | F-005.1 | Agree span names and signal names before starting — see parallelism notes in dependency-graph.md |
| Blocks | F-003.1 | Notifications sent on IDP verified callback — webhook handler must exist |
| Blocks | F-004.1 | Support UI reads `verification_records` |
| Blocks | F-002.2 | Failure handling needs `failure_reason` populated by this story |

## Acceptance criteria

| AC | Criterion | How to verify | Evidence expected |
|---|---|---|---|
| AC-001 | `POST /onboarding` triggers IDP request; `verification_records` row created with status `pending` | Integration test against IDP sandbox | Row present; `idp_request_id` populated |
| AC-002 | Valid signed IDP webhook updates `verification_records` to `verified` | Send signed webhook payload to staging | Row status = `verified`; `completed_at` set |
| AC-003 | Invalid webhook signature returns 400 — no DB update | Send webhook with bad signature | 400 response; DB row unchanged |
| AC-004 | Duplicate webhook deduplicated by `idp_request_id` | Send identical payload twice | Second call returns 200; only one DB row updated |
| AC-005 | IDP error increments `idp_errors_total` | Simulate IDP timeout | Metric incremented with `error_code` label |

## Constraints inherited from upstream

| Constraint | Source artifact |
|---|---|
| IDP API key from Key Vault | `architecture/architecture-rules.md` AR-SEC-001 |
| HMAC-SHA256 + 5-min timestamp window for webhook | `quality-gates/security-review.md` |
| Webhook signing secret from Key Vault | `architecture/architecture-rules.md` AR-SEC-001 |
| Idempotency via `idp_request_id` | `quality-gates/api-contract.md` |
| Correlation ID propagated to IDP client and webhook handler | `architecture/architecture-rules.md` AR-OBS-001 |

## Reference artifacts

| Artifact | Path | What to read there |
|---|---|---|
| API contract | `quality-gates/api-contract.md` | IDP B integration — outbound and webhook specs |
| Data contract | `quality-gates/data-contract.md` | `verification_records` full DDL, PII handling |
| Security review | `quality-gates/security-review.md` | Webhook signature and replay protection |
| Observability plan | `quality-gates/observability-plan.md` | IDP telemetry signals, alert rules |
