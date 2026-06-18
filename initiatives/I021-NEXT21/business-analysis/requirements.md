# Requirements Catalog

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I021-NEXT21 |
| Created at | 2026-06-17T17:30:00+00:00 |
| Created by | product-owner |
| Status | Draft |

---

## Functional Requirements

| ID | Title | User Story | Priority | Status | Source |
|---|---|---|---|---|---|
| FR-001 | Application intake form | As an applicant, I can submit a personal loan application with required fields so my request can be processed | High | Open | input/brs.md |
| FR-002 | Inline validation on intake form | As an applicant, I see inline validation errors so I can fix issues before submitting | High | Open | input/brs.md |
| FR-003 | Assign ARN | As the system, assign a unique Application Reference Number on submission so applicants and staff can reference it | High | Open | input/brs.md |
| FR-004 | Email confirmation | As the system, send confirmation email with ARN within 2 minutes of submission | Medium | Open | input/brs.md |
| FR-005 | Status retrieval by ARN | As an applicant, I can retrieve application status with ARN and DOB without registering | Medium | Open | input/brs.md |
| FR-006 | AI pre-screening trigger | As the system, automatically trigger AI pre-screening within 60s of submission | High | Open | input/brs.md |
| FR-007 | Produce risk score and recommendation | As the system, produce a risk score (0–1000) and recommendation (AUTO_APPROVE/REFER_TO_UNDERWRITER/AUTO_DECLINE) | High | Open | input/brs.md |
| FR-008 | AI model input requirements | As the system, use applicant data, credit bureau data, DTI, LTI, employment stability and credit history for scoring | High | Open | input/brs.md |
| FR-009 | Experian integration | As the system, call Experian CreditExpert API and handle fallback to refer-to-underwriter if unavailable | High | Open | input/brs.md |
| FR-010 | Auto-approve rules | As the system, auto-approve loans ≤£10,000 (with AML/KYC clearance) to enable straight-through processing | High | Open | input/brs.md |
| FR-011 | Auto-decline notifications | As the system, notify applicants of auto-decline reasons (category) within 5 minutes and enforce 30-day cooling-off | Medium | Open | input/brs.md |
| FR-012 | AML screening | As the system, perform AML screening against sanctions/PEP lists within 60s | High | Open | input/brs.md |
| FR-013 | KYC identity verification | As the system, verify identity via HMRC API before offer generation | High | Open | input/brs.md |
| FR-014 | Compliance hold routing | As the system, flag applications failing AML/KYC as COMPLIANCE_HOLD and route to compliance team | High | Open | input/brs.md |
| FR-015 | Underwriter queue and actions | As an underwriter, view referred applications and take actions (approve/decline/request info) | High | Open | input/brs.md |
| FR-016 | Underwriter escalation | As the system, escalate unactioned applications after 4 business hours | Medium | Open | input/brs.md |
| FR-017 | Underwriter decision recording | As the system, record every underwriter action immutably with metadata | High | Open | input/brs.md |
| FR-018 | Decision context in dashboard | As an underwriter, see AI score, bureau summary, DTI/LTI, AML/KYC status | Medium | Open | input/brs.md |
| FR-019 | Offer generation | As the system, generate loan offer documents with key terms for approved applications | High | Open | input/brs.md |
| FR-020 | Offer presentation and validity | As the system, present offers via portal and email; offers valid for 14 days | Medium | Open | input/brs.md |
| FR-021 | Digital acceptance via DocuSign | As the applicant, I can accept offers using DocuSign e-signature | High | Open | input/brs.md |
| FR-022 | Acceptance logging | As the system, log acceptance with timestamp and IP | High | Open | input/brs.md |
| FR-023 | Cooling-off reminders | As the system, send 7- and 13-day reminders during cooling-off | Low | Open | input/brs.md |
| FR-024 | Trigger disbursement to T24 | As the system, trigger disbursement instruction to Temenos T24 after acceptance and cooling-off | High | Open | input/brs.md |
| FR-025 | Disbursement payload | As the system, include account number, sort code, loan amount, reference, and value date in disbursement payload | High | Open | input/brs.md |
| FR-026 | Disbursement retry and alert | As the system, retry once on disbursement failure then alert operations | Medium | Open | input/brs.md |
| FR-027 | Disbursement notification | As the system, notify applicant of disbursement confirmation | Medium | Open | input/brs.md |
| FR-028 | Observability events | As the system, emit structured observability events for key lifecycle steps | Medium | Open | input/brs.md |
| FR-029 | Admin metrics dashboard | As admin, view application volumes, decision times, AI distribution | Medium | Open | input/brs.md |
| FR-030 | Append-only audit log | As the system, maintain an immutable, tamper-evident audit log for state transitions | High | Open | input/brs.md |

---

## Non-Functional Requirements

| ID | Title | Requirement | Category | Priority | Status | Source |
|---|---|---|---|---|---|---|
| NFR-001 | Page load | Application intake form loads within 2s on standard broadband | Performance | High | Open | input/brs.md |
| NFR-002 | Scoring latency | AI scoring pipeline completes within 90s under normal load | Performance | High | Open | input/brs.md |
| NFR-003 | Concurrency | System supports 500 concurrent submissions | Scalability | Medium | Open | input/brs.md |
| NFR-004 | Encryption | PII encrypted at rest and in transit (AES-256, TLS1.3) | Security | High | Open | input/brs.md |
| NFR-005 | Audit immutability | Audit log is write-once and tamper-evident | Compliance | High | Open | input/brs.md |
| NFR-006 | Uptime | 99.9% uptime during business hours | Reliability | High | Open | input/brs.md |
| NFR-007 | Circuit breakers | External integrations implement circuit breakers with fallbacks | Reliability | High | Open | input/brs.md |

---

## Constraints

| ID | Title | Constraint | Category | Priority | Status | Source |
|---|---|---|---|---|---|---|
| C-001 | Data residency | All data must remain in UK data centres | Regulatory | High | Open | input/brs.md, input/architecture.md |

---

*Set Status: Accepted only by human approval when required by the workflow. Never self-accept.*
