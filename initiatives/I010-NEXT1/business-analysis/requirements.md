# Requirements Catalog

> Produced by: product-owner
> Primary consumer: Product Owner, business analyst, delivery lead

## Metadata

| Field | Value |
|---|---|
| Initiative | I010-NEXT1 |
| Version | 1.0 |
| Status | Draft |
| Created at | 2026-06-16 |
| Created by | product-owner |

## Functional Requirements

| Requirement ID | Summary | Source |
|---|---|---|
| FR-001 | Allow applicant to submit personal loan application with required fields | input/brs.md |
| FR-002 | Validate mandatory fields and show inline errors before submission | input/brs.md |
| FR-003 | Assign a unique Application Reference Number (ARN) and display it after submission | input/brs.md |
| FR-004 | Send email confirmation with ARN within 2 minutes of submission | input/brs.md |
| FR-005 | Allow applicant to retrieve status by ARN and DOB without account registration | input/brs.md |
| FR-006 | Trigger AI pre-screening within 60 seconds of submission | input/brs.md |
| FR-007 | Produce risk score (0–1000) and recommendation (AUTO_APPROVE/REFER_TO_UNDERWRITER/AUTO_DECLINE) | input/brs.md |
| FR-008 | AI scoring model uses applicant data, credit bureau, ratios, employment stability | input/brs.md |
| FR-009 | Integrate with Experian CreditExpert API; complete within 30 seconds | input/brs.md |
| FR-010 | AUTO_APPROVE ≤£10,000 proceed to offer generation if AML/KYC clear | input/brs.md |
| FR-011 | AUTO_DECLINE applications notified within 5 minutes with reason category | input/brs.md |
| FR-012 | Perform AML screening against HM Treasury and PEP database within 60 seconds | input/brs.md |
| FR-013 | Perform KYC identity verification via HMRC API | input/brs.md |
| FR-014 | Applications failing AML/KYC flagged as COMPLIANCE_HOLD and routed to compliance | input/brs.md |
| FR-015 | Present REFER_TO_UNDERWRITER and high-value AUTO_APPROVE cases to underwriter queue within 2 minutes | input/brs.md |
| FR-016 | Underwriter dashboard displays applicant summary, AI score, credit bureau summary, ratios, AML/KYC status | input/brs.md |
| FR-017 | Underwriter can approve with conditions, decline with reason, or request info | input/brs.md |
| FR-018 | Record every underwriter action immutably with metadata | input/brs.md |
| FR-019 | Escalate unactioned applications after 4 business hours | input/brs.md |
| FR-020 | Generate loan offer document with required fields | input/brs.md |
| FR-021 | Present loan offer via portal and email; valid for 14 days | input/brs.md |
| FR-022 | Allow digital acceptance via e-signature; log timestamp and IP | input/brs.md |
| FR-023 | Enforce 14-day cooling-off period after acceptance; send reminders | input/brs.md |
| FR-024 | Trigger disbursement to T24 after cooling-off expiry or waiver | input/brs.md |
| FR-025 | Disbursement instruction includes account details and reference | input/brs.md |
| FR-026 | Receive disbursement confirmation; retry once if not received within 2 minutes | input/brs.md |
| FR-027 | Notify applicant of disbursement via email and portal | input/brs.md |
| FR-028 | Maintain immutable audit log of every state transition | input/brs.md |
| FR-029 | Admin dashboard provides metrics and refreshes every 5 minutes | input/brs.md |
| FR-030 | Emit structured observability events for key lifecycle events | input/brs.md |

## Non-Functional Requirements

| ID | Requirement |
|---|---|
| NFR-001 | Application intake form loads within 2 seconds |
| NFR-002 | AI scoring pipeline completes within 90 seconds under normal load |
| NFR-003 | Support 500 concurrent application submissions |
| NFR-004 | PII encrypted at rest (AES-256) and in transit (TLS 1.3) |
| NFR-005 | Audit log is write-once and tamper-evident |
| NFR-006 | Achieve 99.9% uptime during business hours |
| NFR-007 | All API integrations implement circuit breakers with fallbacks |

## Constraints

- Comply with FCA Consumer Duty regulations
- Comply with UK GDPR (data residency: UK only)
- Integrate with Temenos T24, Experian, HMRC, DocuSign
- AI explainability required (no black-box models without explainability)

## Acceptance Criteria

- Requirements traceable to BRS and intake
- Automated tests and integration stubs for Experian and T24
- Security review and compliance sign-off planned
