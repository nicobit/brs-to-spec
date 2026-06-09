# Integration Acceptance Tests — IDP & Payment

> Purpose: provide runnable acceptance test vectors and pass/fail criteria for Integration, Security, and QA to validate vendor integrations in staging.

## Metadata
- Initiative: I001 — Customer Onboarding
- Owners: Integration / QA
- Test environment: Staging sandbox endpoints provided in `input/contracts/`

## Test 1 — Identity Provider B (async webhook flow)

Objective: validate verification request/response and webhook signature verification and replay protection.

Preconditions:
- Staging API credentials provisioned and available in `input/contracts/`
- Webhook endpoint registered in IDP sandbox and reachable from vendor
- Shared secret or signing key exchanged and configured in staging

Steps:
1. Submit `POST /onboarding` with a test profile in staging (use correlation id `test-idp-001`).
2. Confirm `verification_records` created with `status = pending` and `idp_request_id` present.
3. From vendor sandbox, send webhook callback to the registered webhook with `requestId` and verification result `verified`.
   - Include signature header `X-Idp-Signature` (HMAC-SHA256) computed over the raw payload using shared secret.
4. Verify the onboarding service accepts the webhook only when signature validates; rejects when signature is invalid (401/403).
5. Verify replay protection: re-sending the same webhook with same `requestId` is idempotent and does not create duplicate `verification_records` or double transitions.
6. Verify `verification_records` updated to `verified` and `onboarding_success` event emitted.

Pass criteria:
- Webhook accepted when signature valid and rejected when invalid.
- Replay attempts detected and rejected or idempotent.
- `verification_records` show correct timestamps and `idp_payload` redacted as per data model.
- Integration owner records test logs and attaches evidence to this artifact.

## Test 2 — Payment Provider A (synchronous validation)

Objective: validate synchronous payment validation endpoint and error handling.

Preconditions:
- Staging sandbox credentials present in `input/contracts/`

Steps:
1. Submit `POST /onboarding` that triggers payment validation with a test card token in staging.
2. Confirm the onboarding API calls Payment Provider A synchronous validation endpoint and returns appropriate verdict.
3. Validate handling of success, transient failure (5xx), and permanent failure (card declined) scenarios.
4. Confirm retry/backoff behavior for transient errors and correct user-facing status for permanent failures.

Pass criteria:
- Successful validation leads to `onboarding_success` flow.
- Transient errors result in retries according to documented backoff and do not mark user as verified incorrectly.
- Permanent failures surfaced to support UI with actionable error codes.

## Observability Acceptance

- Ensure traces include correlation ids from frontend→API→IDP webhook flow (W3C traceparent or similar).
- Confirm `verification_latency_ms` metric emitted and p95 measured in staging for the test flows.
- Check dashboards: Onboarding Health Overview shows the test flows and metrics.

## Security Acceptance

- Security to run webhook signature verification tests and confirm HMAC verification code path is exercised.
- Ensure logs redact PII as per data model; sample logs to be attached as evidence.

## Evidence to attach
- Request/response logs (redacted) showing correlation ids
- Webhook raw payload and signature header (for validation only; redact secrets)
- Test run summary with pass/fail status

## Owner actions
- Integration/QA: execute tests and update this file with results and links to logs/results.
- Security: confirm webhook tests and update `quality-gates/security-review.md` with their sign-off.
- Delivery: confirm acceptance tests meet Product acceptance criteria and record acceptance in `engineering-readiness/readiness-check.md`.
