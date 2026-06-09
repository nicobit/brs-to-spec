# API Spec — F-001.1: Onboarding Submission

## POST /onboarding

**Purpose:** Create onboarding record and profile
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
| 400 | `INVALID_REQUEST` | Missing required field or invalid format | No |
| 401 | `UNAUTHORIZED` | Missing or invalid API key | No |
| 409 | `ALREADY_EXISTS` | Email already has an onboarding record | No |
| 429 | `RATE_LIMITED` | Too many requests | Yes — backoff |
| 500 | `INTERNAL_ERROR` | Unexpected server error | Yes — backoff |

**PII transmitted:** `email` (high), `phone` (high) — do not log; encrypt at DB write
