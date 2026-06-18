# Process Flows

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I021-NEXT21 |
| Created at | 2026-06-17T18:05:00+00:00 |
| Created by | product-owner |
| Status | Draft |

## Key Process Flows

### Application Intake -> Pre-screen -> Underwriting -> Offer -> Disbursement

High-level flow:

1. Applicant submits application.
2. System validates and assigns ARN.
3. System triggers AI pre-screening and credit bureau call.
4. If AUTO_APPROVE -> generate offer -> cooling-off -> disburse.
5. If REFER_TO_UNDERWRITER -> enqueue for underwriter actions.

---

*Set Status: Accepted only by human approval when required by the workflow. Never self-accept.*
