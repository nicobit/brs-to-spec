# API Spec — D1: Guided Onboarding (MVP)

> Distilled from `quality-gates/api-contract.md` for this increment only.
> Full contract (sandbox credentials, SLA, rate limits) is in `quality-gates/api-contract.md` and `input/contracts/`.

## POST /onboarding

**Purpose:** Create onboarding record, persist profile and consent, trigger async IDP verification
**Auth:** API key — header `X-API-Key` (value from Azure Key Vault)
**Consumer:** Web / mobile frontend shell

Request:
```json
{
  "email": "string (required)",
  "phone": "string (optional)",
  "consent_marketing": "boolean (required)"
}
```

Response — 202 Accepted:
```json
{
  "id": "uuid",
  "status": "pending"
}
```

Response — errors:

| HTTP status | Code | Meaning | Retry? |
|---|---|---|---|
| 400 | `INVALID_REQUEST` | Missing required field or invalid format | No — fix request |
| 401 | `UNAUTHORIZED` | Missing or invalid API key | No |
| 409 | `ALREADY_EXISTS` | Email already has an onboarding record in progress | No |
| 429 | `RATE_LIMITED` | Too many requests | Yes — exponential backoff |
| 500 | `INTERNAL_ERROR` | Unexpected server error | Yes — retry with backoff |

**Idempotency:** not required for initial submission — duplicate email returns 409
**PII transmitted:** `email` (high), `phone` (high) — do not log; encrypt at DB write

---

## GET /onboarding/{id}/status

**Purpose:** Return current state of an onboarding flow
**Auth:** API key — header `X-API-Key`
**Consumer:** Frontend shell (polling), support tooling (D2)

Response — 200 OK:
```json
{
  "id": "uuid",
  "status": "pending | verified | failed | complete",
  "verification_status": "pending | verified | failed | retrying",
  "created_at": "ISO 8601",
  "updated_at": "ISO 8601"
}
```

Response — errors:

| HTTP status | Code | Meaning |
|---|---|---|
| 401 | `UNAUTHORIZED` | Missing or invalid API key |
| 404 | `NOT_FOUND` | Unknown onboarding ID |

---

## POST /webhook/idp

**Purpose:** Receive async Identity Provider B verification callback
**Auth:** HMAC-SHA256 signature — header `X-IDP-Signature: sha256=<hex>`
**Idempotency key:** `requestId` in payload body — deduplicate on receipt

Signature verification:
1. Compute `HMAC-SHA256(raw_body, webhook_signing_secret)` where secret is from Key Vault
2. Compare constant-time to header value
3. Reject if timestamp in payload is outside ±5-minute window (replay protection)
4. Return `400 Bad Request` on any verification failure — do not process payload

Expected payload:
```json
{
  "requestId": "string — IDP request identifier (idempotency key)",
  "result": "verified | failed | pending",
  "timestamp": "ISO 8601",
  "errorCode": "string | null"
}
```

Response — 200 OK: empty body (IDP does not use response content)
Response — 400 Bad Request: invalid signature or replay detected

On success:
- Update `verification_records` row matching `idp_request_id = requestId`
- If `result = verified`: enqueue notification job, update `profiles.status`
- If `result = failed`: update status, log `errorCode` in audit_log

---

## IDP B integration — outbound

**Protocol:** HTTPS REST
**Auth method:** API key (header — confirm header name with vendor; store in Key Vault)
**Sandbox endpoint:** see `input/contracts/identity-provider-b-contract.md` when available
**Retry strategy:** exponential backoff — 3 attempts, 1s / 5s / 30s delays; log `idp_errors_total` on each failure

Outbound request (to IDP B):
```json
{
  "requestId": "uuid — our generated idempotency key",
  "email": "string",
  "phone": "string | null",
  "webhookUrl": "https://<our-domain>/webhook/idp",
  "region": "IT"
}
```

Expected IDP response — 202 Accepted: IDP has accepted the request; callback will follow async.

---

## SendGrid integration — outbound

**Protocol:** HTTPS REST (SendGrid Mail Send API v3)
**Auth method:** API key (Key Vault)
**Async:** fire-and-forget — failure does not fail the onboarding flow in D1
**Sandbox:** use SendGrid sandbox mode (`mail_settings.sandbox_mode.enable: true`) in staging

Outbound request (minimal):
```json
{
  "to": [{ "email": "<customer email>" }],
  "template_id": "<provisioned template ID>",
  "dynamic_template_data": {
    "onboarding_id": "uuid"
  }
}
```
