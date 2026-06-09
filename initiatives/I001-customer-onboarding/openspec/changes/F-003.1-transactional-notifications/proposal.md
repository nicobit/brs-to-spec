# Proposal — F-003.1: Transactional Notifications

**As a** user,
**I want** to receive confirmation emails/SMS when onboarding completes,
**so that** I have a record of my successful onboarding.

**Requirement:** FR-004
**Acceptance criteria:** SendGrid template renders correctly in staging; email delivered on IDP verified callback

## Why now

IDP webhook handler exists (F-002.1). Notifications are triggered from the `verified` callback — the webhook handler enqueues a notification job when verification succeeds.

## What changes

- Notification job consumer — reads from background queue, calls SendGrid API
- SendGrid client — sends transactional email using provisioned template
- `audit_logs` row written on email send action

## Dependencies

| Relationship | Story ID | Reason |
|---|---|---|
| Depends on | F-002.1 | Webhook handler must exist to enqueue notification job on `verified` |
| Can run in parallel with | F-004.1 | No shared schema or API changes |
| Blocks | F-003.2 | Template management builds on the SendGrid integration established here |

## Acceptance criteria

| AC | Criterion | How to verify | Evidence expected |
|---|---|---|---|
| AC-001 | Confirmation email delivered in staging on IDP verified callback | Trigger verified webhook; check inbox | Email received with correct template content |
| AC-002 | SendGrid API key loaded from Key Vault | Config inspection | No hardcoded key in code or config files |
| AC-003 | Notification failure does not fail the onboarding flow | Simulate SendGrid error; check onboarding status | Status remains `verified`; error logged |
| AC-004 | `audit_logs` row written for email send action | DB query after notification | Row with `action = email_sent`, no PII in `details` |

## Constraints inherited from upstream

| Constraint | Source artifact |
|---|---|
| SendGrid API key from Key Vault | `architecture/architecture-rules.md` AR-SEC-001 |
| Notification failure must not fail onboarding | `quality-gates/api-contract.md` |
| No PII in audit_logs.details | `quality-gates/data-contract.md` |

## Reference artifacts

| Artifact | Path | What to read there |
|---|---|---|
| API contract | `quality-gates/api-contract.md` | SendGrid integration spec |
| Security review | `quality-gates/security-review.md` | Secrets management |
