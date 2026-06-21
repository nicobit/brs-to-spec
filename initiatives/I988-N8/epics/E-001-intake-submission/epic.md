# E-001 — Intake & Submission

## Business Objective

Enable applicants to submit and track loan applications end-to-end so that originations can start automated scoring and downstream processing with a durable ARN.

## Scope

In scope:
- Public applicant portal form
- ARN generation and persistence
- Submission confirmation and applicant-facing status
- Basic validation and document upload stub

Out of scope:
- AI scoring, compliance screening, disbursement adapters

## High-Level Acceptance Criteria

- Applicants can complete and submit an online application and receive a stable ARN that is retained for all downstream interactions.
- Submission triggers a confirmation to the applicant and an intake event onto the event bus.

## Foundation / Setup

- Requires a persisted `applications` table and an `arn` generator service. CI pipeline must include contract tests for the intake API.

## Stories

| Story ID | Title | Layers | Priority |
|---|---|---|---|
| F-001.1 | Applicant completes online application form | Frontend, Backend, Integration | Must |
| F-001.2 | Generate ARN and persist application record | Backend, Infrastructure | Must |

---

## Epic-level Test Expectations

- Validate ARN uniqueness and idempotent submission behaviour ([integration], [e2e]).
