# Business Rules

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I013-NEXT13 |
| Created at | 2026-06-16 |
| Created by | product-owner |
| Status | Draft |

## Business Rules Catalog

| BR-NNN | Category | Rule Statement | BRS Source | Affected Requirements | Affected Actors | Notes |
|---|---|---|---|---|---|---|
| BR-001 | Validation | Application submission must include full name, DOB, NI, income and contact details; reject incomplete submissions. | FR-001, FR-002 | FR-001, FR-002 | Applicant, System | Inline validation enforced client-side and server-side |
| BR-002 | Identification | Assign a unique ARN on successful submission and persist as primary identifier. | FR-003 | FR-003 | System | ARN format: alphanumeric 12 chars |
| BR-003 | Timing | Confirmation email must be sent within 2 minutes of successful submission. | FR-004 | FR-004 | Notification Service | Retry policy 3 attempts with exponential backoff |
| BR-004 | Scoring trigger | AI pre-screening must start within 60 seconds of submission. | FR-006 | FR-006 | System, AI Scoring Service | Use async event bus to start scoring pipeline |
| BR-005 | Experian fallback | If Experian lookup fails or times out, route application to REFER_TO_UNDERWRITER. | FR-009 | FR-009 | System | Circuit breaker timeout: 30s |
| BR-006 | AML/KYC gating | Applications failing AML or KYC must be set to COMPLIANCE_HOLD and not proceed to offer generation. | FR-012, FR-013, FR-014 | FR-012, FR-013, FR-014 | Compliance, System | Notify applicant with hold status |

## Coverage Note

| FR-NNN | Business rule(s) | Status |
|---|---|---|
| FR-001 | BR-001 | Covered |
| FR-003 | BR-002 | Covered |
| FR-004 | BR-003 | Covered |
| FR-006 | BR-004 | Covered |
| FR-009 | BR-005 | Covered |
| FR-012 | BR-006 | Covered |

---

*Set Status: Draft — review with product and compliance.*
