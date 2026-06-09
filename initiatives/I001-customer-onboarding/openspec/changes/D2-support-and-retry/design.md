# Design — D2: Support Tools and Retry Flows

> Self-contained technical context for this increment.
> An engineer implements from this file + `tasks.md` + `specs/` without opening any other artifact.
> **Prerequisite:** D1 DB schema and API are live in the target environment.

## System context

D2 adds an operator-facing layer on top of D1's onboarding engine. The support UI is a new internal web application (or admin panel) that reads from the existing `profiles` and `verification_records` tables. Two new API endpoints are added to the Onboarding API: a retry endpoint and a support query endpoint. RBAC is introduced via a `support_agent` role — enforced at the API layer with audit logging for every action.

## API surface

| Method | Path | Purpose | Auth | Request body | Response | Contract artifact |
|---|---|---|---|---|---|---|
| GET | `/support/onboarding/{id}` | Return full onboarding state for support view | API key + `support_agent` role | — | `{ id, status, verification_status, failure_reason, created_at, updated_at }` | `specs/api.md#get-support-view` |
| POST | `/support/onboarding/{id}/retry` | Trigger new IDP verification for a failed onboarding | API key + `support_agent` role | `{ reason: string }` | `202 { verification_id }` | `specs/api.md#post-retry` |

Full schemas, error codes, and RBAC enforcement details: `specs/api.md`.

## Data model changes

| Table | Change | Key columns | PII | Encryption | Notes |
|---|---|---|---|---|---|
| `verification_records` | Add column | `failure_reason: string (nullable)` | No | — | Populated on IDP `result = failed`; surfaced to support UI |
| `audit_logs` | Existing table — new action types | `action`: add `support_view`, `support_retry` | No | — | Every support endpoint call writes an audit row |

No new tables in D2. Full schema: `quality-gates/data-contract.md`.

## Integration points

| Integration | Protocol | Auth | Async? | Notes |
|---|---|---|---|---|
| Identity Provider B (retry) | Same as D1 | API key from Key Vault | Yes — webhook callback | Retry creates a new `verification_records` row with new `idp_request_id`; D1 webhook handler processes the callback unchanged |

## Architecture constraints applied

| Rule ID | Constraint | How applied in D2 |
|---|---|---|
| AR-SEC-001 | Secrets in Azure Key Vault | No new secrets in D2 — reuse D1 Key Vault references |
| AR-SEC-002 | RBAC: least-privilege for support agent role | Support endpoints check `support_agent` role claim; reject with 403 otherwise; all actions audit-logged |
| AR-OBS-001 | Distributed tracing | Correlation ID propagated through support endpoints; span names `support.view`, `support.retry` |

## Security decisions

| Concern | Decision | Accepted risk | Gate reference |
|---|---|---|---|
| Support UI access to PII | Support agents can view `status` and `failure_reason` — not raw `email` or `phone` | PII fields not exposed in support API response | `quality-gates/security-review.md` |
| Retry authorisation | Only `support_agent` role can trigger retry; logged with `reason` field | None | `quality-gates/security-review.md` |
| Audit trail | Every support action writes to `audit_logs` with actor, entity, action, timestamp | None | AR-SEC-002 |

## Observability requirements

| Signal | Type | Emitted by | When | Labels |
|---|---|---|---|---|
| `support_retries_total` | Counter | Support API | On every `POST /support/onboarding/{id}/retry` — 202 response | — |
| `support_views_total` | Counter | Support API | On every `GET /support/onboarding/{id}` — 200 response | — |

Tracing: spans `support.view` and `support.retry` added to Onboarding API. Correlation ID propagated. Sampling: 100% for all support actions (low volume, high audit value).

Full telemetry catalog and alert rules: `quality-gates/observability-plan.md`.

## Open questions

| # | Question | Owner | Needed before |
|---|---|---|---|
| 1 | Is the support UI a standalone web app or integrated into an existing admin panel? | Product | OS-D2-030 (UI task) |
| 2 | RBAC identity source — existing IdP, or new role claim in API key? | Security / Architecture | OS-D2-010 (RBAC task) |
