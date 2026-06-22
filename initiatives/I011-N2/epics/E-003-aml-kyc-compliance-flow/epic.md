# E-003 — AML/KYC & Compliance Flow

## Summary

Epic E-003 performs AML screening and KYC identity verification, routing failing checks to a compliance hold and notifying applicants and compliance teams.

## Business Objective

Prevent sanctioned or high-risk applicants from receiving offers and ensure regulatory compliance through timely screening and clear routing.

## In Scope

- AML screening against HM Treasury sanctions list
- KYC identity verification via HMRC API
- Routing to `COMPLIANCE_HOLD` and compliance notifications
- Underwriter referral where automated checks are inconclusive

## Out of Scope

- Manual investigation playbooks (handled by Compliance operations)

## Traceability (requirements)

- REQ-007 — AML and KYC Screening
- REQ-014 — Observability and Reporting
- REQ-013 — Encryption and Data Residency

## Stories

| Story | Title | Linked Requirements |
|---|---|---|
| F-004.1 | AML Screening Integration | REQ-007 |
| F-004.2 | KYC Identity Verification | REQ-007 |
| F-004.3 | Compliance Hold Routing & Notifications | REQ-014, REQ-007 |

---
