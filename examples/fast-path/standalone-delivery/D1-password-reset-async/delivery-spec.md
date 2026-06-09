# Delivery Spec — D1 Password Reset Async

## Metadata

| Field | Value |
|---|---|
| Deliverable ID | D1 |
| Deliverable name | Password Reset Async |
| Initiative | Password reset email delay — async fix |
| Delivery mode | Fast Path |
| Execution mode | Standalone |
| Owner | Backend team |
| Status | Ready for implementation |

## Problem

`POST /auth/password-reset` sends the password reset email synchronously inside the HTTP request handler. Under load, this causes 3–5 minute delays before the response is returned to the client.

## Solution

Move the email send to a background job via the existing `job-queue` service. The handler creates the reset token, enqueues the email job, and returns HTTP 200 immediately.

## Requirements

| Req ID | Requirement | Source |
|---|---|---|
| REQ-01 | `POST /auth/password-reset` must return HTTP 200 within 200ms under normal load | input-package.md — success criteria |
| REQ-02 | Reset email must be delivered within 30 seconds of the request | input-package.md — success criteria |
| REQ-03 | Reset token validity and expiry behavior must not change | input-package.md — scope |
| REQ-04 | Existing reset flow tests must continue to pass | input-package.md — success criteria |

## Constraints

| Constraint | Source |
|---|---|
| Use existing `job-queue` service and its current email schema | initiative-context.md R-02 |
| Do not call `email-service` directly from the HTTP handler | initiative-context.md R-01 |
| Do not change reset token logic | initiative-context.md R-03 |
| Verify queue schema version matches current `email-service` expectation before coding | initiative-context.md — open risk R01 |

## Acceptance criteria

- `POST /auth/password-reset` returns HTTP 200 in < 200ms (p95) under normal load
- Password reset email arrives within 30 seconds in staging smoke test
- All existing `auth-service` integration tests pass
- No change to reset token TTL, format, or validation behavior

## Out of scope

- Email template changes
- Reset UI changes
- New API endpoints
- Schema changes

## Validation approach

1. Run existing `auth-service` integration test suite — all tests must pass
2. Manual smoke test in staging: request reset, confirm email arrives within 30 seconds
3. Load test the endpoint at expected peak RPS — confirm p95 < 200ms
