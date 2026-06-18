# Requirements Catalog

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I013-NEXT13 |
| Created at | 2026-06-16 |
| Created by | product-owner |
| Status | Draft |

---

## Functional Requirements

| ID | Title | User Story | Priority | Status | Source |
|---|---|---|---|---|---|
| FR-001 | Online application submission | As an applicant I can submit a personal loan application with required identity, employment, income, amount, purpose and term fields so that my request can be assessed digitally. | High | Open | input/brs.md |
| FR-002 | Inline field validation | As an applicant I see inline validation errors and cannot submit incomplete applications. | High | Open | input/brs.md |
| FR-003 | Application Reference Number (ARN) | As an applicant I receive a unique ARN immediately after submission for traceability. | High | Open | input/brs.md |
| FR-004 | Confirmation email with ARN | As an applicant I receive an email within 2 minutes containing the ARN and estimated decision timeline. | Medium | Open | input/brs.md |
| FR-005 | Status lookup without account | As an applicant I can retrieve application status using ARN and DOB without registering. | Medium | Open | input/brs.md |
| FR-006 | Trigger AI pre-screening | As the system I trigger AI pre-screening within 60 seconds of submission. | High | Open | input/brs.md |
| FR-007 | Produce risk score and recommendation | As the scoring service I produce a 0–1000 risk score plus recommendation (AUTO_APPROVE, REFER_TO_UNDERWRITER, AUTO_DECLINE). | High | Open | input/brs.md |
| FR-008 | Use defined model inputs | As the scoring process I use applicant data, credit bureau data, debt-to-income, loan-to-income, employment stability and credit history length. | High | Open | input/brs.md |
| FR-009 | Experian integration | As the system I integrate with Experian CreditExpert and complete lookups within 30 seconds or route to underwriter if unavailable. | High | Open | input/brs.md |
| FR-010 | AUTO_APPROVE routing for low amounts | AUTO_APPROVE applications ≤ £10,000 proceed to offer generation after AML/KYC clearance. | High | Open | input/brs.md |
| FR-011 | AUTO_DECLINE notification & cooling-off | AUTO_DECLINE applicants are notified within 5 minutes and cannot reapply for 30 days. | Medium | Open | input/brs.md |
| FR-012 | AML screening | Perform AML screening against HM Treasury sanctions and PEP sources before any offer is generated (<= 60s). | High | Open | input/brs.md |
| FR-013 | KYC identity verification | Perform KYC identity verification against HMRC using NI, name and DOB. | High | Open | input/brs.md |
| FR-014 | Compliance hold handling | Flag failed AML/KYC as COMPLIANCE_HOLD, route to compliance and block offer generation. | High | Open | input/brs.md |
| FR-015 | Underwriter queue routing | Place REFER_TO_UNDERWRITER cases and AUTO_APPROVE > £10,000 into underwriter queue within 2 minutes. | High | Open | input/brs.md |
| FR-016 | Underwriter dashboard context | Underwriter dashboard shows applicant summary, AI result, bureau summary, ratios, employment verification and AML/KYC status. | High | Open | input/brs.md |
| FR-017 | Underwriter actions | Underwriters can approve with conditions, decline with reason, or request more information. | High | Open | input/brs.md |
| FR-018 | Immutable recording of underwriter actions | Record every underwriter action with actor, timestamp, action, rationale and presented AI recommendation immutably. | High | Open | input/brs.md |
| FR-019 | Escalation for unactioned items | Escalate unactioned underwriter queue items to team lead after 4 business hours. | Medium | Open | input/brs.md |
| FR-020 | Loan offer document generation | Generate loan offer with amount, APR, monthly repayment, total repayable, term and key terms. | High | Open | input/brs.md |
| FR-021 | Offer presentation channels | Present offer in portal and email; offer validity 14 days. | Medium | Open | input/brs.md |
| FR-022 | Digital acceptance via DocuSign | Allow digital acceptance via DocuSign and log timestamp and IP address. | Medium | Open | input/brs.md |
| FR-023 | Cooling-off enforcement & reminders | Enforce 14-day cooling-off with reminders at day 7 and day 13. | Medium | Open | input/brs.md |
| FR-024 | Disbursement trigger to T24 | Trigger disbursement to Temenos T24 via internal payment gateway after acceptance and cooling-off or waiver. | High | Open | input/brs.md |
| FR-025 | Disbursement payload completeness | Include account number, sort code, loan amount, reference number and value date in disbursement. | High | Open | input/brs.md |
| FR-026 | Disbursement confirmation handling | On missing confirmation retry once after 2 minutes then alert operations. | Medium | Open | input/brs.md |
| FR-027 | Disbursement notification to applicant | Notify applicant by email and portal when disbursement is confirmed. | Medium | Open | input/brs.md |
| FR-028 | Immutable audit log of state transitions | Maintain immutable audit log for every application state transition including snapshot. | High | Open | input/brs.md |
| FR-029 | Admin dashboard metrics | Provide admin metrics for volume, average decision time, AI recommendation distribution, underwriter rates, AML/KYC hold rates with 5-minute refresh. | Medium | Open | input/brs.md |
| FR-030 | Structured observability events | Emit observability events for submission, scoring, AML/KYC, underwriter decision, acceptance, and disbursement with ARN, timestamp, status, actor. | High | Open | input/brs.md |

---

## Non-Functional Requirements

| ID | Title | Requirement | Category | Priority | Status | Source |
|---|---|---|---|---|---|---|
| NFR-001 | Fast form load | Intake form loads within 2 seconds on standard broadband | Performance | High | Open | input/brs.md |
| NFR-002 | Scoring latency | AI scoring pipeline completes end-to-end within 90 seconds under normal load | Performance | High | Open | input/brs.md |
| NFR-003 | Concurrency | Support 500 concurrent application submissions | Scalability | Medium | Open | input/brs.md |
| NFR-004 | Encryption of PII | Encrypt all PII at rest (AES-256) and in transit (TLS 1.3) | Security | High | Open | input/brs.md |
| NFR-005 | Tamper-evident audit log | Audit log is write-once and tamper-evident | Reliability / Compliance | High | Open | input/brs.md |
| NFR-006 | Availability SLA | Achieve 99.9% uptime during business hours (08:00–20:00 GMT) | Availability | Medium | Open | input/brs.md |
| NFR-007 | Circuit breakers and fallbacks | Implement circuit breakers for Experian, HMRC, DocuSign and T24 with defined fallback behaviour | Resilience | High | Open | input/brs.md |

---

## Constraints

| ID | Title | Constraint | Category | Priority | Status | Source |
|---|---|---|---|---|---|---|
| C-001 | Regulatory compliance | Must comply with FCA Consumer Duty and UK GDPR; data residency in UK-only | Regulatory | High | Open | input/brs.md |
| C-002 | Core banking integration | Must integrate with existing Temenos T24 via internal payment gateway (REST) | Integration | High | Open | input/brs.md |
| C-003 | Credit bureau contract | Must use Experian CreditExpert under existing enterprise contract | Integration | High | Open | input/brs.md |
| C-004 | E-signature provider | Must use DocuSign for e-signature under enterprise contract | Integration | Medium | Open | input/brs.md |
| C-005 | Explainable AI requirement | AI model decisions must be explainable; black-box models not permitted | Regulatory / Architecture | High | Open | input/brs.md |
| C-006 | Data protection | All PII must be encrypted and handled within UK data centres | Security / Regulatory | High | Open | input/brs.md |

---

*Set Status: Accepted only by human approval when required by the workflow. Never self-accept.*
