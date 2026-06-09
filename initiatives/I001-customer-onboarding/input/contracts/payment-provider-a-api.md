# Payment Provider A — API Contract (Vendor-ready Draft)

> Owner: Integration
> Status: Draft — fill vendor URLs and examples, then sign-off

## Summary
Defines API contract for payment validation calls required during onboarding (e.g., card verification, billing validation). Emphasizes PCI scope, tokenization, synchronous validation behavior, error semantics, and test vectors.

## Endpoints
- POST /v1/validate-payment
  - Description: Validate payment instrument (card/bank) for onboarding path.
  - Auth: `Authorization: Bearer <API_KEY>`
  - Content-Type: `application/json`
  - Responses:
    - 200 OK — validation result (synchronous)
    - 400 Bad Request — invalid input
    - 401 Unauthorized
    - 402 Payment Required (or vendor-specific decline code)
    - 429 Too Many Requests
    - 5xx — transient error

- GET /v1/validation/{validationId}
  - Retrieve status and details.

## Request/Response Schemas
- Validate request (POST /v1/validate-payment)
```json
{
  "requestId": "string",
  "customerId": "string (optional)",
  "paymentInstrument": {
    "type": "card|bank_transfer",
    "card": {
      "brand": "visa|mastercard",
      "last4": "string",
      "expiryMonth": 1,
      "expiryYear": 2028,
      "token": "string (if using tokenization)"
    }
  }
}
```

- Validate response (200 OK)
```json
{
  "validationId": "string",
  "status": "valid|invalid|requires_action",
  "reason": "string (if invalid)",
  "timestamp": "ISO-8601"
}
```

## Security & PCI
- Minimize card PAN exposure: prefer tokenization; do not store full PAN in onboarding DB unless PCI scope handling is approved.
- Use vendor tokenization where possible; onboard token via secure PCI-compliant flows (e.g., hosted fields or client-side tokenization).
- Encryption in transit (TLS 1.2+).

## Error Handling & Retry
- 400: fix request; do not retry.
- 402 / decline: surface to support; do not retry automatically.
- 429 / 5xx: exponential backoff with jitter. Implement circuit-breaker for persistent failures.

## SLAs & Performance Targets
- Vendor to provide availability SLA and latency expectations; client target is 95th percentile < 30s for validation calls used in onboarding happy-path.

## Acceptance Tests
1. Happy-path validation returns `valid` and client proceeds to next onboarding step.
2. Decline path returns `invalid` or specific decline codes; system surfaces reason and offers retry.
3. Rate-limited response includes `Retry-After`; client honors header.
4. Tokenized flow: client exchanges card details for vendor token; token accepted in validation request.

## Operational Notes
- Provision separate staging and production credentials.
- Confirm PCI responsibilities and ensure documentation of who is in-scope.
- Emit metrics `payment.validation.count`, `payment.validation.latency`, `payment.validation.errors`.

## Open items
- Vendor concrete rate limits and error code list.
- Tokenization options and sample integration patterns.

