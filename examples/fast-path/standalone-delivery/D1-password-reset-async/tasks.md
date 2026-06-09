# Tasks — D1 Password Reset Async

## Task list

| Task ID | Title | Type | Depends on | Status |
|---|---|---|---|---|
| T01 | Verify job-queue email schema version | Investigation | None | Open |
| T02 | Refactor password reset handler to enqueue job | Implementation | T01 | Open |
| T03 | Update integration tests for async behavior | Test | T02 | Open |

---

## T01 — Verify job-queue email schema version

**Type:** Investigation (complete before coding T02)

**Goal:** Confirm the job-queue message schema used by `email-service` for password reset emails matches the schema used by the existing notification email flow.

**Steps:**

1. Find the current notification email job schema in the `auth-service` or `notification-service` codebase.
2. Find the `email-service` consumer — confirm what schema fields it expects for email jobs.
3. Confirm the password reset email can be sent using the same schema with no new fields.
4. If the schema differs, raise it before starting T02 — an event contract gate may be required.

**Acceptance:** Schema confirmed identical or compatible. No new fields needed. Documented in implementation summary.

---

## T02 — Refactor password reset handler to enqueue job

**Type:** Implementation

**Requires:** T01 complete and schema confirmed compatible.

**Goal:** Move the `email-service` call out of the synchronous HTTP handler and into a `job-queue` background job.

**Steps:**

1. Load `engineering-readiness/initiative-context.md` — confirm constraints before touching code.
2. Locate the `POST /auth/password-reset` handler in `auth-service`.
3. Inspect existing notification email enqueue pattern — follow it exactly.
4. Refactor: after creating the reset token, enqueue the email job and return HTTP 200.
5. Remove the synchronous `email-service` call from the handler.
6. Do not change reset token creation, TTL, format, or validation.

**Acceptance:**

- Handler returns HTTP 200 before email is sent
- Job is enqueued using the existing schema (verified in T01)
- Reset token logic is unchanged
- No new dependencies introduced

---

## T03 — Update integration tests for async behavior

**Type:** Test

**Goal:** Update existing reset flow tests to account for the async email send.

**Steps:**

1. Identify existing integration tests that assert email was sent synchronously (e.g., mock assertions that fire immediately after the HTTP call).
2. Update assertions to account for the async delay — check that the job was enqueued, not that the email was sent immediately.
3. Confirm all other reset flow assertions still pass unchanged.
4. Add a test that asserts the handler returns HTTP 200 before the email job completes.

**Acceptance:**

- All existing `auth-service` integration tests pass
- New async assertion covers the handler return before email send
- No test coverage removed
