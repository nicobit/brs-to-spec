# Input Package

## Source Metadata

| Field | Value |
|---|---|
| Source name | Bug report — password reset email delay |
| Source version / date | 2026-06-09 |
| Extracted by | Backend team |
| Extraction date | 2026-06-09 |

## Problem Statement

Password reset emails are delayed by 3–5 minutes in production.

Root cause identified: the `POST /auth/password-reset` handler calls the email service synchronously before returning the HTTP response. Under load, the email service queue backs up and the HTTP request blocks.

Expected behavior: the response returns immediately after creating the reset token. Email delivery happens asynchronously.

## Scope

| Item | In scope | Out of scope |
|---|---|---|
| Move email send to background queue | Yes | |
| Change reset token logic | | Yes |
| Change email template | | Yes |
| Change password reset UI | | Yes |
| Add new API endpoints | | Yes |

## Architecture context

- Existing background queue: `job-queue` service (Redis-backed, already used for notification emails)
- Existing email service: `email-service` (internal, HTTP API)
- Affected component: `auth-service` → `POST /auth/password-reset` handler
- No new service boundaries introduced
- No schema changes required

## Success criteria

- `POST /auth/password-reset` returns HTTP 200 within 200ms under normal load
- Reset email is delivered within 30 seconds of the request
- Existing reset flow tests continue to pass
- No change to the reset token validity or expiry behavior
