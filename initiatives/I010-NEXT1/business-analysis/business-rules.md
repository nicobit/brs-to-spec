# Business Rules Catalog

## Metadata

| Field | Value |
|---|---|
| Initiative | I010-NEXT1 |
| Version | 1.0 |
| Status | Draft |
| Created at | 2026-06-16 |
| Created by | product-owner |

## Business Rules

| BR-ID | Category | Rule statement | Source | Affected FRs |
|---|---|---|---:|---|
| BR-001 | Validation | Application must include all mandatory applicant fields before submission; block and show inline errors | input/brs.md, FR-002 | FR-002 |
| BR-002 | Identifier | System must assign a unique ARN at successful submission and return it to the applicant | input/brs.md, FR-003 | FR-003 |
| BR-003 | Timing | Send email confirmation with ARN within 2 minutes of successful submission | input/brs.md, FR-004 | FR-004 |
| BR-004 | Screening | Trigger AI pre-screening within 60 seconds of submission; store score and recommendation | input/brs.md, FR-006, FR-007 | FR-006, FR-007 |
| BR-005 | Credit | Retrieve Experian credit report within 30 seconds when required for scoring | input/brs.md, FR-009 | FR-009 |
| BR-006 | Decisioning | AUTO_APPROVE applies to applications ≤ £10,000 if AML/KYC clear; otherwise REFER_TO_UNDERWRITER | input/brs.md, FR-010, FR-015 | FR-010, FR-015 |
| BR-007 | Compliance | Applications failing AML/KYC must be labeled COMPLIANCE_HOLD and routed to compliance queue | input/brs.md, FR-012, FR-013, FR-014 | FR-012, FR-013, FR-014 |
| BR-008 | Underwriter | Underwriter actions (approve/decline/request-info) must be recorded immutably with user, timestamp, and reason | input/brs.md, FR-016, FR-017, FR-018 | FR-016, FR-017, FR-018 |
| BR-009 | Escalation | Escalate unactioned underwriter items after 4 business hours to a supervisor queue | input/brs.md, FR-019 | FR-019 |
| BR-010 | Offer | Generated loan offer must include required fields and remain valid for 14 days; acceptance recorded with timestamp and IP | input/brs.md, FR-020, FR-021, FR-022 | FR-020, FR-021, FR-022 |

## Coverage Notes

- Rules extracted from the requirements catalog; if additional decision points are found in the BRS, record as new `BR-` entries.

---

*Status: Draft — ready for AI validation.*