 # Atomic Requirements

 ## Metadata

 | Field | Value |
 |---|---|
 | Initiative ID | I988-N8 |
 | Created at | 2026-06-21 |
 | Created by | product-owner |
 | Status | Draft |

 ---

 ## Summary

 | Metric | Value |
 |---|---|
 | Total requirements | 9 |
 | Functional | 7 |
 | Non-functional | 2 |
 | Data | 1 |
 | Integration | 3 |
 | Security | 2 |
 | Operational | 1 |
 | Reporting | 1 |
 | Blocking questions | 2 |

 ---

 ## Requirement Catalogue

 ### REQ-001 — Applicant can submit personal loan application online

 | Field | Value |
 |---|---|
 | Type | Functional |
 | Source Section | Epic 1 — Loan Application Intake (FR-001) |
 | Actor | Applicant |
 | Business Object | Loan Application |
 | Trigger / Event | Applicant submits application form |
 | Expected Outcome | Application accepted and ARN assigned |
 | Dependencies | Notification service, Application DB |
 | Ambiguities | None |
 | Assumptions | Applicant provides valid NI number |
 | Blocking Questions | None |

 #### Requirement Text

 The system shall allow an applicant to submit a personal loan application online with required fields (name, DOB, NI number, employment status, income, loan amount, loan purpose, repayment term). The system shall validate mandatory fields and reject incomplete submissions.

 #### Notes

 Derived from FR-001 and FR-002.

 ---

 ### REQ-002 — Assign unique Application Reference Number (ARN)

 | Field | Value |
 |---|---|
 | Type | Functional |
 | Source Section | FR-003 |
 | Actor | System |
 | Business Object | ARN |
 | Trigger / Event | After successful submission |
 | Expected Outcome | ARN generated and shown to applicant |
 | Dependencies | Application DB |
 | Ambiguities | ARN format requirements |
 | Assumptions | ARN uniqueness enforced by DB constraints |
 | Blocking Questions | ARN persistence and format policy |

 #### Requirement Text

 The system shall assign a unique Application Reference Number (ARN) to every submitted application and display it to the applicant immediately after submission.

 ---

 ### REQ-003 — Email confirmation on submission

 | Field | Value |
 |---|---|
 | Type | Functional |
 | Source Section | FR-004 |
 | Actor | System / Notification Service |
 | Business Object | Email Confirmation |
 | Trigger / Event | Successful submission |
 | Expected Outcome | Email sent within 2 minutes containing ARN and estimated timeline |
 | Dependencies | Notification Service, Email Provider |
 | Ambiguities | Retry policy for email failures |
 | Assumptions | Email address format validated in form |
 | Blocking Questions | None |

 #### Requirement Text

 The system shall send an email confirmation to the applicant within 2 minutes of submission, containing the ARN and an estimated decision timeline.

 ---

 ### REQ-004 — AI pre-screening and risk scoring

 | Field | Value |
 |---|---|
 | Type | Functional |
 | Source Section | FR-006, FR-007, FR-008 |
 | Actor | AI Scoring Service |
 | Business Object | Risk Score, Recommendation |
 | Trigger / Event | After application submission |
 | Expected Outcome | Risk score (0–1000) and recommendation produced within 60 seconds |
 | Dependencies | Experian integration, scoring model, input transformations |
 | Ambiguities | Model explainability outputs required |
 | Assumptions | Experian response available within 30s; otherwise route to refer |
 | Blocking Questions | Model vendor and explainability format (OQ-001) |

 #### Requirement Text

 The system shall automatically trigger an AI pre-screening assessment for every submitted application within 60 seconds and produce a risk score and recommendation (AUTO_APPROVE, REFER_TO_UNDERWRITER, AUTO_DECLINE). The AI scoring output must include explainability metadata and input provenance.

 ---

 ### REQ-005 — Experian integration

 | Field | Value |
 |---|---|
 | Type | Integration |
 | Source Section | FR-009 |
 | Actor | Loan Origination API |
 | Business Object | Credit Report |
 | Trigger / Event | During AI scoring pipeline |
 | Expected Outcome | Credit report retrieved within 30s or route to refer |
 | Dependencies | Experian API, circuit breaker implementation |
 | Ambiguities | Retry/backoff policy |
 | Assumptions | Enterprise Experian contract available |
 | Blocking Questions | Fallback policies when Experian unavailable (OQ-003) |

 #### Requirement Text

 The system shall integrate with Experian CreditExpert API to retrieve a credit report for every application, completing within 30 seconds. If Experian is unavailable, the application shall be routed to REFER_TO_UNDERWRITER.

 ---

 ### REQ-006 — AML / KYC screening

 | Field | Value |
 |---|---|
 | Type | Security |
 | Source Section | FR-012, FR-013 |
 | Actor | Compliance Service |
 | Business Object | AML/KYC Result |
 | Trigger / Event | Before offer generation |
 | Expected Outcome | Screening completes within 60 seconds; failures flagged as COMPLIANCE_HOLD |
 | Dependencies | HM Treasury sanctions, HMRC KYC API |
 | Ambiguities | Additional providers scope (OQ-004) |
 | Assumptions | HMRC API available; fallback manual verification |
 | Blocking Questions | Exact fallback behaviour when HMRC unavailable (OQ-003) |

 #### Requirement Text

 The system shall perform AML and KYC checks as defined; failures place application into COMPLIANCE_HOLD and prevent offer generation.

 ---

 ### REQ-007 — Offer generation and acceptance

 | Field | Value |
 |---|---|
 | Type | Functional |
 | Source Section | FR-020, FR-021, FR-022 |
 | Actor | Loan Origination API / DocuSign |
 | Business Object | Loan Offer |
 | Trigger / Event | Application approved and compliance cleared |
 | Expected Outcome | Offer generated; applicant can accept via e-signature; acceptance logged |
 | Dependencies | DocuSign integration, Notification Service |
 | Ambiguities | Offer template variations |
 | Assumptions | DocuSign contract exists |
 | Blocking Questions | None |

 #### Requirement Text

 The system shall generate and present a loan offer; acceptance via DocuSign must be recorded with timestamp and IP address.

 ---

### REQ-008 — Auto-decline notification and cooling-off policy

| Field | Value |
|---|---|
| Type | Functional |
| Source Section | FR-011 |
| Actor | System |
| Business Object | Decline Notification |
| Trigger / Event | AI recommendation = AUTO_DECLINE |
| Expected Outcome | Applicant notified within 5 minutes; 30-day cooling-off enforced |
| Dependencies | Notification Service, Applicant DB |
| Ambiguities | Decline reason categories mapping |
| Assumptions | Applicant contact details available |
| Blocking Questions | None |

#### Requirement Text

Applications with recommendation AUTO_DECLINE shall be notified to the applicant within 5 minutes with a decline reason category; enforce a 30-day cooling-off period before reapply.

---

### REQ-009 — Underwriter queue presentation

| Field | Value |
|---|---|
| Type | Functional |
| Source Section | FR-015 |
| Actor | Underwriter Dashboard |
| Business Object | Underwriter Queue Item |
| Trigger / Event | Recommendation = REFER_TO_UNDERWRITER or AUTO_APPROVE > £10,000 |
| Expected Outcome | Application appears in queue within 2 minutes with full context |
| Dependencies | Application DB, AI Scoring Service, Compliance Service |
| Ambiguities | UI pagination/ordering rules |
| Assumptions | Data aggregation service available |
| Blocking Questions | None |

#### Requirement Text

Applications requiring underwriter review must appear in the underwriter queue within 2 minutes and include applicant summary, AI score and recommendation, credit summary, ratios, and AML/KYC status.

---

### REQ-010 — Underwriter action logging

| Field | Value |
|---|---|
| Type | Functional |
| Source Section | FR-018 |
| Actor | System |
| Business Object | Underwriter Action Record |
| Trigger / Event | Underwriter approval/decline/request info |
| Expected Outcome | Immutable record with ID, timestamp, action, reason, AI recommendation |
| Dependencies | Audit Log Store |
| Ambiguities | Retention policy for action logs |
| Assumptions | Audit store append-only enforced |
| Blocking Questions | None |

#### Requirement Text

The system shall record every underwriter action with underwriter ID, timestamp, action taken, reason/conditions, and presented AI recommendation; records are immutable.

---

### REQ-011 — Underwriter escalation for unactioned items

| Field | Value |
|---|---|
| Type | Operational |
| Source Section | FR-019 |
| Actor | System |
| Business Object | Escalation Notification |
| Trigger / Event | Unactioned > 4 business hours |
| Expected Outcome | Notification to team lead triggered |
| Dependencies | Notification Service, Queue monitoring |
| Ambiguities | Business hours definition and timezone handling |
| Assumptions | Workday calendar available |
| Blocking Questions | None |

#### Requirement Text

Unactioned applications in the underwriter queue shall trigger an escalation notification to the team lead after 4 business hours.

---

### REQ-012 — Disbursement instruction to core banking

| Field | Value |
|---|---|
| Type | Integration |
| Source Section | FR-024, FR-025 |
| Actor | Payment Gateway Adapter |
| Business Object | Disbursement Instruction |
| Trigger / Event | Acceptance and cooling-off expiry |
| Expected Outcome | Disbursement instruction sent with required fields; receive confirmation |
| Dependencies | Temenos T24 adapter, internal payment gateway |
| Ambiguities | Retry policy and reconciliation steps |
| Assumptions | T24 adapter contract available |
| Blocking Questions | None |

#### Requirement Text

Upon acceptance and cooling-off completion, the system shall send a disbursement instruction to Temenos T24 with required payment details and handle confirmation or retries.

---

### REQ-013 — Observability events emission

| Field | Value |
|---|---|
| Type | Reporting |
| Source Section | FR-030 |
| Actor | Various services |
| Business Object | Observability Event |
| Trigger / Event | Key lifecycle events (submission, scoring, AML result, underwriter decision, acceptance, disbursement) |
| Expected Outcome | Structured events emitted with ARN, timestamp, status |
| Dependencies | Event bus, monitoring stack |
| Ambiguities | Event schema evolution rules |
| Assumptions | Service bus and monitoring available in UK region |
| Blocking Questions | None |

#### Requirement Text

The system shall emit structured observability events for key lifecycle milestones including ARN, timestamp, status, and actor.

---

### REQ-014 — Performance and concurrency targets

| Field | Value |
|---|---|
| Type | Non-functional |
| Source Section | NFR-002, NFR-003 |
| Actor | System |
| Business Object | Performance Targets |
| Trigger / Event | Production operation |
| Expected Outcome | Scoring pipeline completes within 90s; support 500 concurrent submissions |
| Dependencies | Infrastructure sizing, autoscaling |
| Ambiguities | Load profile distribution |
| Assumptions | Autoscaling configured |
| Blocking Questions | None |

#### Requirement Text

The system shall meet the non-functional targets: scoring pipeline ≤90 seconds and support 500 concurrent submissions under normal load.

---

### REQ-015 — Data residency and encryption

| Field | Value |
|---|---|
| Type | Non-functional |
| Source Section | NFR-004 |
| Actor | Platform |
| Business Object | PII Storage |
| Trigger / Event | Any storage of PII or audit data |
| Expected Outcome | Data stored only in UK regions; AES-256 at rest and TLS1.3 in transit |
| Dependencies | Cloud resource configuration |
 | Ambiguities | Backup/replication policies |
| Assumptions | UK regions available and configured |
| Blocking Questions | None |

#### Requirement Text

All PII must be stored in UK datacenters and encrypted at rest (AES-256) and in transit (TLS 1.3).

---

## ID Mapping
| FR-001 | REQ-001 |
| NFR-002 | REQ-014 |
| C-001 | REQ-015 |


### REQ-016 — Applicant status retrieval

| Field | Value |
|---|---|
| Type | Functional |
| Source Section | FR-005 |
| Actor | Applicant |
| Business Object | Application Status |
| Trigger / Event | Applicant requests status with ARN and DOB |
| Expected Outcome | Status returned without registration |

#### Requirement Text

Applicants can retrieve application status using ARN and date of birth without registration.

---

### REQ-017 — AI recommendation thresholds

| Field | Value |
|---|---|
| Type | Functional |
| Source Section | FR-010 |
| Actor | AI Scoring Service |
| Business Object | Auto-approval threshold |

#### Requirement Text

Define threshold for AUTO_APPROVE when loan amount ≤ £10,000 and AML/KYC cleared.

---

### REQ-018 — Credit data ephemeral handling

| Field | Value |
|---|---|
| Type | Data |
| Source Section | FR-009 |

#### Requirement Text

Credit bureau data must be used transiently and not persisted beyond scoring pipeline.

---

### REQ-019 — Offer validity window

| Field | Value |
|---|---|
| Type | Functional |
| Source Section | FR-021 |

#### Requirement Text

Offers are valid for 14 days from generation and communicated to applicants.

---

### REQ-020 — Cooling-off reminders

| Field | Value |
|---|---|
| Type | Functional |
| Source Section | FR-023 |

#### Requirement Text

System sends reminder emails at day 7 and day 13 of the 14-day cooling-off period.

---

### REQ-021 — Disbursement retry and alerting

| Field | Value |
|---|---|
| Type | Operational |
| Source Section | FR-026 |

#### Requirement Text

If disbursement confirmation is not received within 2 minutes, retry once and alert operations.

---

### REQ-022 — Audit log structure

| Field | Value |
|---|---|
| Type | Security |
| Source Section | FR-028 |

#### Requirement Text

Audit logs must record previous state, new state, actor, timestamp, and data snapshot for each transition.

---

### REQ-023 — Admin dashboard metrics

| Field | Value |
|---|---|
| Type | Reporting |
| Source Section | FR-029 |

#### Requirement Text

Admin dashboard provides application volume by status, average decision time, recommendation distribution, and underwriter stats; data refresh every 5 minutes.

---

### REQ-024 — Performance and schema versioning

| Field | Value |
|---|---|
| Type | Non-functional |
| Source Section | FR-030 / NFRs |

#### Requirement Text

Event schemas must include versioning and performance targets must be met for critical pipelines.

---

## Open Questions

 | OQ-NNN | Question | Source REQ | Blocking? | Owner | Status |
 |---|---|---|---|---|---|
 | OQ-001 | What is the approved AI model vendor and explainability format? | REQ-004 | Yes | Head of AI | Open |
 | OQ-003 | What is the fallback when HMRC KYC API is unavailable? Manual verification or auto-refer? | REQ-005/006 | Yes | Compliance | Open |

 ---

 ## Assumptions

 | ASM-NNN | Assumption | Source REQ | Risk if Wrong | Validation Approach | Status |
 |---|---|---|---|---|---|
 | ASM-001 | Experian contract is available and supports required queries | REQ-005 | High | Contract check and test calls | Open |

 ---

 ## Traceability Notes

 Requirements were extracted from the BRS sections covering intake, AI scoring, AML/KYC, offer generation, and integrations. Further decomposition will occur during story creation.

 ---
 *Set Status: Accepted only after human review. Never self-accept.*
