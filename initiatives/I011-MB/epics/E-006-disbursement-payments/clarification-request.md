# Epic Clarification Request — E-006 Disbursement & Payments

## Summary

WHEN preparing the Disbursement & Payments epic, THE TEAM REQUIRES CLARIFICATION on payment provider selection, settlement timing, idempotency, and refund/reconciliation rules.

## Blocking Questions

| ID | Route | Page | Question | Why It Matters | Required For |
|---|---|---|---|---|---|
| PAQ-001 | /api/v1/servicing/payments | Servicing API | Which payment provider(s) are supported/approved (internal ledger, Stripe, Adyen, bank rails)? | Implementation depends on provider APIs, credentials, and supported features (refunds, currency, settlement). | Provider integration stories, secrets, deployment
| PAQ-002 | /api/v1/servicing/payments | Servicing API | What is the expected settlement window and currency handling (same-day, T+1, multi-currency)? | Affects retry/backoff, reconciliation, reporting, and liability accounting. | Business rules, scheduled jobs, reconciliation
| PAQ-003 | /api/v1/servicing/payments | Servicing API | What idempotency and retry semantics are required for payment submission and webhooks? | Prevents duplicate charges and ensures safe retries across network failures. | API design (idempotency keys), consumer contracts, tests
| PAQ-004 | webhooks / notifications | N/A | What webhook schema and delivery guarantees are required for payment events and notifications? | Downstream consumers need stable event payloads and retry/backoff expectations. | Event contracts, consumer integration stories
| PAQ-005 | /api/v1/servicing/payments | Servicing API | How should refunds, chargebacks, and failed settlements be represented and linked to original payments? | Affects audit trail, customer communications, and accounting. | API schema, audit entries, reconciliation flows |

## Answer Instructions

Record answers in:

```text
input/clarifications/E-006.yaml
```

Include `id`, `answer`, `rationale`, `answered_at`, and `owner` for each answered question.

*End of clarification request.*
