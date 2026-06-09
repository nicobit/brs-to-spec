# Identity Provider B — API Contract (Vendor-ready Draft)

> Owner: Integration
> Status: Draft — fill vendor URLs and examples, then sign-off

## Summary
This document defines the concrete API contract between the Onboarding Service and Identity Provider B for identity verification used in the onboarding flow. It captures endpoint URLs, request/response schemas, webhook semantics, error handling, security, SLAs, and test vectors.

## Endpoints
- POST /v1/verify
  - Description: Submit an identity verification request for a subject.
  - Auth: `Authorization: Bearer <API_KEY>` (API key token)
  - Content-Type: `application/json`
  - Responses:
    - 200 OK — verification result (synchronous)
    - 202 Accepted — verification accepted and processing (async)
    - 400 Bad Request — invalid input
    - 401 Unauthorized — invalid credentials
    - 429 Too Many Requests — rate limited
    - 5xx — transient server error

- GET /v1/verification/{verificationId}
  - Description: Retrieve current status and detailed result.
  - Auth: same as above
  - Responses: 200 OK with result payload, 404 Not Found if id unknown.

- Webhook (server-to-server)
  - POST /webhooks/verification
  - Description: Identity Provider B posts verification outcome when async processing completes.
  - Security: HMAC-SHA256 signature header `X-Idp-Signature` over raw body using shared secret. Timestamp header `X-Idp-Timestamp` recommended to avoid replay.

## Request/Response Schemas
- Verify request (POST /v1/verify)
```json
{
  "requestId": "string", // client-generated UUID
  "subject": {
    "firstName": "string",
    "lastName": "string",
    "email": "string",
    "phone": "string",
    "document": {
      "type": "passport|id_card|driver_license",
      "number": "string",
      "country": "ISO-3166-1-alpha-2"
    }
  },
  "callbackUrl": "https://onboarding.example.com/webhooks/verification" // optional if async
}
```

- Verify response (200 OK)
```json
{
  "verificationId": "string",
  "status": "verified|failed|pending",
  "score": 0.0,
  "reason": "string (optional, failure reason)",
  "issuedAt": "2026-06-09T12:00:00Z"
}
```

- Webhook payload (POST /webhooks/verification)
```json
{
  "verificationId": "string",
  "requestId": "string",
  "status": "verified|failed",
  "score": 0.0,
  "reason": "string (optional)",
  "issuedAt": "ISO-8601",
  "metadata": { }
}
```

## Error Handling & Retry
- Client behavior:
  - 400: do not retry; surface to support and log detail.
  - 401: fix credentials; do not retry.
  - 429: honor `Retry-After` header if present; exponential backoff with jitter.
  - 5xx: retry with exponential backoff; circuit-breaker around repeated failures.
- Idempotency:
  - Client should send `requestId` to help vendor deduplicate.

## SLAs & Performance Targets
- Target availability to request from vendor: >= 99.9% monthly.
- Latency target (for synchronous path): 95th percentile < 30s.
- Rate limits: vendor to provide concrete limits. Client will implement reasonable throttling.

## Security & Data Protection
- Transport: TLS 1.2+.
- Authentication: Bearer API key token stored in org secret store.
- Webhook security: HMAC signature verification; include timestamp and nonce to mitigate replay.
- PII minimization: send only required fields; avoid sending raw document images unless required and agreed.
- Residency: vendor must confirm data storage regions and support deletion requests; contract must confirm Italy residency if storing PII.

## Acceptance Tests (minimum)
1. Happy-path synchronous verification: POST /v1/verify returns 200 with `verified` and expected fields; system creates customer record.
2. Async verification: POST /v1/verify returns 202 and vendor posts webhook to callback URL; webhook signature verified and record updated.
3. Failure handling: vendor returns `failed` with reason; support ticket created and failure trace captured.
4. Rate limiting: vendor responds with 429 and `Retry-After`; client respects header.
5. Security: webhook signature validated; replay attempts rejected.

## Operational Notes
- Provisioning: vendor to provide staging and production credentials.
- Vendor must provide sample payloads and a sandbox endpoint.
- Monitoring: emit metrics `idp.request.count`, `idp.request.latency`, `idp.request.errors`.

## Open items
- Vendor concrete URLs and example responses for edge cases.
- Vendor-provided rate limits and SLA document.
- Confirm whether document-image uploads are required and the secure transfer mechanism.

