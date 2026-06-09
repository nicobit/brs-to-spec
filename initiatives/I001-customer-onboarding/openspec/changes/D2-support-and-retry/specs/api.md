# API Spec — D2: Support Tools and Retry Flows

> Distilled from `quality-gates/api-contract.md` for this increment only.
> D1 endpoints (`POST /onboarding`, `GET /onboarding/{id}/status`, `POST /webhook/idp`) are unchanged — see D1 `specs/api.md`.

## GET /support/onboarding/{id}

**Purpose:** Return full onboarding state for support agent view
**Auth:** API key (`X-API-Key`) + `support_agent` role claim
**Consumer:** Support UI

Response — 200 OK:
```json
{
  "id": "uuid",
  "status": "pending | verified | failed | complete",
  "verification_status": "pending | verified | failed | retrying",
  "failure_reason": "string | null",
  "created_at": "ISO 8601",
  "updated_at": "ISO 8601"
}
```

**PII policy:** `email` and `phone` are NOT included in this response — support agents do not need raw PII to diagnose flow state.

Response — errors:

| HTTP status | Code | Meaning |
|---|---|---|
| 401 | `UNAUTHORIZED` | Missing or invalid API key |
| 403 | `FORBIDDEN` | Valid API key but missing `support_agent` role |
| 404 | `NOT_FOUND` | Unknown onboarding ID |

**Audit:** every call writes an `audit_logs` row with `action: support_view`, `actor: <service/user id>`, `entity_id: <onboarding id>`.

---

## POST /support/onboarding/{id}/retry

**Purpose:** Operator-triggered IDP verification retry for a failed onboarding
**Auth:** API key (`X-API-Key`) + `support_agent` role claim
**Consumer:** Support UI retry button

Request:
```json
{
  "reason": "string (required) — operator note explaining why retry was triggered"
}
```

Response — 202 Accepted:
```json
{
  "verification_id": "uuid — new verification_records row ID"
}
```

Response — errors:

| HTTP status | Code | Meaning | Retry? |
|---|---|---|---|
| 400 | `INVALID_STATE` | Onboarding is not in a retryable state (e.g. already verified) | No |
| 401 | `UNAUTHORIZED` | Missing or invalid API key | No |
| 403 | `FORBIDDEN` | Missing `support_agent` role | No |
| 404 | `NOT_FOUND` | Unknown onboarding ID | No |
| 429 | `RATE_LIMITED` | Too many retries for this onboarding ID | No |

**Side effects:**
1. Inserts new `verification_records` row (status: `pending`, new `idp_request_id`)
2. Calls IDP B outbound (same as D1 OS-010 — reuses client and Key Vault secret)
3. Writes `audit_logs` row: `action: support_retry`, `actor`, `entity_id`, `details: { reason }`

**Idempotency:** not idempotent — each call creates a new verification attempt. Rate limiting recommended to prevent abuse.

**Audit:** `reason` field stored in `audit_logs.details` (non-PII jsonb field).
