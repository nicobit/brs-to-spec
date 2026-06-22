# Atomic Requirements

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I011-N2 |
| Created at | 2026-06-21 |
| Created by | product-owner |
| Status | Draft |

---

## Summary

| Metric | Value |
|---|---|
| Total requirements | 15 |
| Functional | 10 |
| Non-functional | 3 |
| Data | 1 |
| Integration | 3 |
| Security | 3 |
| Operational | 2 |
| Reporting | 1 |
| Blocking questions | 3 |

---

## Reference IDs

| ID | Notes |
|---|---|
| FR-001 | Loan Application Intake (maps to REQ-001) |
| NFR-002 | AI scoring latency requirement (maps to REQ-012) |


## Requirement Catalogue

### FR-001 — Online application submission

#### Requirement Text

See BRS: applicant submits personal loan application (fields, validations, ARN assignment).

---

### FR-002 — Form validation

#### Requirement Text

See BRS: mandatory fields validated with inline errors; incomplete applications prevented.

---

### FR-003 — Application reference assignment

#### Requirement Text

See BRS: assign unique Application Reference Number (ARN) on submission.

---

### FR-004 — Email confirmation

#### Requirement Text

See BRS: send email confirmation with ARN within 2 minutes.

---

### FR-005 — Status retrieval by ARN

#### Requirement Text

See BRS: applicants can retrieve status using ARN and DOB without registration.

---

### FR-006 — Trigger AI pre-screening

#### Requirement Text

See BRS: automatically trigger AI pre-screening within 60 seconds of submission.

---

### FR-007 — AI recommendation labels

#### Requirement Text

See BRS: produce risk score and recommendation labels (AUTO_APPROVE, REFER_TO_UNDERWRITER, AUTO_DECLINE).

---

### FR-008 — AI scoring inputs

#### Requirement Text

See BRS: scoring uses applicant data, Experian, ratios, employment stability, and credit history.

---

### FR-009 — Experian integration

#### Requirement Text

See BRS: integrate with Experian CreditExpert, retrieve credit report within 30s.

---

### FR-010 — Auto-approve flow

#### Requirement Text

See BRS: AUTO_APPROVE & <=£10,000 proceed to offer generation subject to AML/KYC.

---

### FR-011 — Auto-decline notification

#### Requirement Text

See BRS: AUTO_DECLINE notifications within 5 minutes; cooling-off period applied.

---

### FR-012 — AML screening

#### Requirement Text

See BRS: perform AML screening against HM Treasury sanctions list within 60 seconds.

---

### FR-013 — KYC identity verification

#### Requirement Text

See BRS: perform KYC via HMRC identity verification API.

---

### FR-014 — Compliance hold routing

#### Requirement Text

See BRS: route failing AML/KYC to COMPLIANCE_HOLD and notify applicant.

---

### FR-015 — Underwriter queue presentation

#### Requirement Text

See BRS: present REFER_TO_UNDERWRITER applications to underwriter queue within 2 minutes.

---

### FR-016 — Underwriter dashboard contents

#### Requirement Text

See BRS: dashboard displays applicant summary, AI score, credit summary, ratios, verification status.

---

### FR-017 — Underwriter actions

#### Requirement Text

See BRS: underwriter can approve, decline, or request additional information.

---

### FR-018 — Underwriter action logging

#### Requirement Text

See BRS: record underwriter actions immutably with details and AI recommendation presented.

---

### FR-019 — Underwriter escalation

#### Requirement Text

See BRS: unactioned items escalate after 4 business hours.

---

### FR-020 — Offer document generation

#### Requirement Text

See BRS: generate loan offer document with required fields and terms.

---

### FR-021 — Offer presentation

#### Requirement Text

See BRS: present offer via self-service portal and email; valid for 14 days.

---

### FR-022 — Digital acceptance via e-signature

#### Requirement Text

See BRS: allow e-signature/DocuSign acceptance; log timestamp and IP.

---

### FR-023 — Cooling-off reminders

#### Requirement Text

See BRS: enforce 14-day cooling-off and reminders at day 7 and day 13.

---

### FR-024 — Disbursement trigger

#### Requirement Text

See BRS: trigger disbursement instruction to T24 after acceptance and cooling-off expiry.

---

### FR-025 — Disbursement instruction content

#### Requirement Text

See BRS: include account number, sort code, loan amount, reference, value date in instruction.

---

### FR-026 — Disbursement confirmation handling

#### Requirement Text

See BRS: receive confirmation, update to DISBURSED; retry once then alert on failure.

---

### FR-027 — Disbursement notifications

#### Requirement Text

See BRS: notify applicant of disbursement via email and portal.

---

### FR-028 — Immutable audit log

#### Requirement Text

See BRS: maintain immutable audit log of state transitions with snapshots.

---

### FR-029 — Admin dashboard metrics

#### Requirement Text

See BRS: admin dashboard shows volume, average decision time, AI distribution, rates.

---

### FR-030 — Observability events

#### Requirement Text

See BRS: emit structured observability events for key lifecycle milestones.

---

### NFR-001 — Frontend load performance

#### Requirement Text

See BRS: application intake form shall load within 2 seconds on standard broadband.

---

### NFR-002 — Scoring latency

#### Requirement Text

See BRS: AI scoring pipeline shall complete end-to-end within 90 seconds under normal load.

---

### NFR-003 — Concurrency

#### Requirement Text

See BRS: system shall support 500 concurrent application submissions.

---

### NFR-004 — Encryption

#### Requirement Text

See BRS: all PII encrypted at rest (AES-256) and in transit (TLS 1.3).

---

### NFR-005 — Audit log properties

#### Requirement Text

See BRS: audit log shall be write-once and tamper-evident.

---

### NFR-006 — Uptime

#### Requirement Text

See BRS: system shall achieve 99.9% uptime during business hours.

---

### NFR-007 — Integration circuit breakers

#### Requirement Text

See BRS: API integrations shall implement circuit breakers with defined fallback behavior.

---

### REQ-001 — Online Application Submission

| Field | Value |
|---|---|
| Type | Functional |
| Source Section | Epic 1 — Loan Application Intake (FR-001) |
| Actor | Applicant |
| Business Object | Loan Application |
| Trigger / Event | Applicant submits application form |
| Expected Outcome | Application accepted and ARN assigned |
| Dependencies | REQ-002 (validation) |
| Ambiguities | None |
| Assumptions | Input form fields are as specified in BRS |
| Blocking Questions | None |
| Open Questions | OQ-REQ-001 |

#### Requirement Text

The system shall allow an applicant to submit a personal loan application online with required fields (name, DOB, NI, employment, income, loan amount, purpose, term) and assign a unique Application Reference Number (ARN) immediately upon submission.

#### Notes

See FR-001 and FR-003 for confirmation and ARN display behavior.

---

### REQ-002 — Client-side and Server-side Validation

| Field | Value |
|---|---|
| Type | Functional |
| Source Section | FR-002 |
| Actor | Applicant / System |
| Business Object | Loan Application |
| Trigger / Event | Form entry / submission |
| Expected Outcome | Incomplete forms prevented from submission; clear inline errors shown |
| Dependencies | REQ-001 |
| Ambiguities | None |
| Assumptions | Standard validation rules apply |
| Blocking Questions | None |
| Open Questions | OQ-REQ-002 |

#### Requirement Text

The system shall validate mandatory fields and display inline validation errors; incomplete applications shall not be submitted.

---

### REQ-003 — Email Confirmation with ARN

| Field | Value |
|---|---|
| Type | Functional |
| Source Section | FR-004 |
| Actor | System |
| Business Object | Notification / Application |
| Trigger / Event | Successful submission |
| Expected Outcome | Email sent within 2 minutes containing ARN and estimated timeline |
| Dependencies | REQ-001 |
| Ambiguities | Email delivery SLAs outside system scope |
| Assumptions | Notification service functioning |
| Blocking Questions | None |

#### Requirement Text

The system shall send an email confirmation to the applicant within 2 minutes of submission containing the ARN and an estimated decision timeline.

---

### REQ-004 — AI Pre-Screening Trigger and Output

| Field | Value |
|---|---|
| Type | Functional |
| Source Section | Epic 2 — AI Pre-Screening and Risk Scoring (FR-006, FR-007) |
| Actor | System / AI Scoring Service |
| Business Object | Scoring Result |
| Trigger / Event | Application submission completion |
| Expected Outcome | Risk score (0–1000) and recommendation produced within 60 seconds |
| Dependencies | REQ-001, Integration with Experian (REQ-006) |
| Ambiguities | Score scale interpretation documented elsewhere |
| Assumptions | Experian data available or fallback route exists |
| Blocking Questions | OQ-001 (model vendor / approach) |

#### Requirement Text

The system shall automatically trigger an AI pre-screening assessment for every submitted application within 60 seconds, producing a risk score (0–1000) and a recommendation (`AUTO_APPROVE`, `REFER_TO_UNDERWRITER`, `AUTO_DECLINE`).

---

### REQ-005 — Auto-Approve Criteria and Offer Flow

| Field | Value |
|---|---|
| Type | Functional |
| Source Section | FR-010, FR-015, FR-020 |
| Actor | System |
| Business Object | Loan Offer |
| Trigger / Event | AI recommendation `AUTO_APPROVE` and amount ≤ £10,000 and AML/KYC clear |
| Expected Outcome | Direct offer generation and delivery to applicant |
| Dependencies | REQ-004, REQ-007 (AML/KYC) |
| Ambiguities | Edge cases for borderline amounts |
| Assumptions | AML/KYC integration available |
| Blocking Questions | None |

#### Requirement Text

Applications recommended `AUTO_APPROVE` with loan amount ≤ £10,000 shall proceed to offer generation (subject to AML/KYC clearance) without underwriter review.

---

### REQ-006 — Experian Integration for Credit Reports

| Field | Value |
|---|---|
| Type | Integration |
| Source Section | FR-009 |
| Actor | System / Experian |
| Business Object | Credit Report |
| Trigger / Event | AI scoring initiation |
| Expected Outcome | Credit report retrieved within 30 seconds or route to underwriter on failure |
| Dependencies | Network/integration availability |
| Ambiguities | Retry strategy specifics |
| Assumptions | Enterprise contract in place |
| Blocking Questions | None |

#### Requirement Text

The system shall integrate with Experian CreditExpert API to retrieve a credit report for every application within 30 seconds; if Experian is unavailable, the application shall be routed to `REFER_TO_UNDERWRITER`.

---

### REQ-007 — AML and KYC Screening

| Field | Value |
|---|---|
| Type | Security / Functional |
| Source Section | FR-012, FR-013 |
| Actor | Compliance Service |
| Business Object | Applicant Screening Result |
| Trigger / Event | Before offer generation |
| Expected Outcome | AML/KYC completed within 60 seconds; failures route to `COMPLIANCE_HOLD` |
| Dependencies | HM Treasury and HMRC integrations |
| Ambiguities | Additional AML providers (OQ-004) |
| Assumptions | HM Treasury provider only |
| Blocking Questions | OQ-003, OQ-004 |

#### Requirement Text

The system shall perform AML screening and KYC identity verification before any offer is generated; failures shall route the application to `COMPLIANCE_HOLD` and notify the compliance team.

---

### REQ-008 — Underwriter Queue Presentation and Actions

| Field | Value |
|---|---|
| Type | Functional |
| Source Section | FR-015, FR-016, FR-017 |
| Actor | Underwriter |
| Business Object | Underwriter Queue Item |
| Trigger / Event | AI recommendation `REFER_TO_UNDERWRITER` or `AUTO_APPROVE` > £10,000 |
| Expected Outcome | Underwriter can approve/decline/request info; actions are immutably logged |
| Dependencies | Audit log (REQ-011) |
| Ambiguities | Escalation SLAs |
| Assumptions | Underwriter identities via Azure AD |
| Blocking Questions | None |

#### Requirement Text

The system shall present applications requiring underwriter review in a queue, display required data (AI score, credit summary, AML/KYC status), and allow underwriters to approve, decline, or request information; all actions shall be immutably recorded.

---

### REQ-009 — Offer Generation and Digital Acceptance

| Field | Value |
|---|---|
| Type | Functional |
| Source Section | FR-020, FR-021, FR-022 |
| Actor | System / Applicant |
| Business Object | Loan Offer Document |
| Trigger / Event | Approval (auto or underwriter) and AML/KYC clear |
| Expected Outcome | Offer generated, presented, and can be accepted via e-signature; acceptance logged |
| Dependencies | DocuSign integration, Notification service |
| Ambiguities | Cooling-off handling specifics |
| Assumptions | DocuSign contract available |
| Blocking Questions | None |

#### Requirement Text

On approval and AML/KYC clearance, the system shall generate a loan offer document and present it to the applicant; the applicant may accept via DocuSign and acceptance shall be logged.

---

### REQ-010 — Disbursement Trigger and Confirmation

| Field | Value |
|---|---|
| Type | Functional / Integration |
| Source Section | FR-024, FR-025, FR-026 |
| Actor | System / Core Banking (T24) |
| Business Object | Disbursement Instruction |
| Trigger / Event | Acceptance + cooling-off expiry |
| Expected Outcome | Disbursement instruction sent; confirmation updates application to `DISBURSED` |
| Dependencies | T24 integration, retry strategy |
| Ambiguities | Retry and alerting thresholds |
| Assumptions | Payment gateway API available |
| Blocking Questions | OQ-005 |

#### Requirement Text

The system shall trigger a disbursement instruction to Temenos T24 after acceptance and cooling-off handling; on confirmation the application state becomes `DISBURSED`.

---

### REQ-011 — Immutable Audit Log

| Field | Value |
|---|---|
| Type | Operational / Security |
| Source Section | FR-028 |
| Actor | System |
| Business Object | Audit Entry |
| Trigger / Event | Every state transition and significant action |
| Expected Outcome | Immutable, tamper-evident audit entries for each event |
| Dependencies | Audit store (Cosmos DB) |
| Ambiguities | Retention policies |
| Assumptions | Cosmos DB append-only container available |
| Blocking Questions | None |

#### Requirement Text

The system shall write an immutable audit entry for every state transition and significant action, recording actor, timestamp, previous and new state, and relevant snapshot data.

---

### REQ-012 — Performance and Scalability NFRs

| Field | Value |
|---|---|
| Type | Non-functional |
| Source Section | NFR-002, NFR-003 |
| Actor | System |
| Business Object | Scoring pipeline / intake |
| Trigger / Event | Normal operation |
| Expected Outcome | Scoring completes within 90 seconds; supports 500 concurrent submissions |
| Dependencies | Infrastructure sizing |
| Ambiguities | Exact load shape |
| Assumptions | Reasonable traffic patterns |
| Blocking Questions | None |

#### Requirement Text

The system shall ensure the AI scoring pipeline completes end-to-end within 90 seconds under normal load and support 500 concurrent application submissions.

---

### REQ-013 — Encryption and Data Residency

| Field | Value |
|---|---|
| Type | Security / Non-functional |
| Source Section | NFR-004, Constraints |
| Actor | System |
| Business Object | All PII and persistent data |
| Trigger / Event | Storage and transport of data |
| Expected Outcome | AES-256 at rest and TLS 1.3 in transit; all data in UK regions |
| Dependencies | Cloud tenancy and key management |
| Ambiguities | Key rotation policy |
| Assumptions | Azure-managed keys available |
| Blocking Questions | None |

#### Requirement Text

All PII shall be encrypted at rest (AES-256) and in transit (TLS 1.3); all storage and processing shall remain within UK data centres.

---

### REQ-014 — Observability and Reporting

| Field | Value |
|---|---|
| Type | Reporting / Operational |
| Source Section | FR-029, FR-030 |
| Actor | Admin / Ops |
| Business Object | Metrics and events |
| Trigger / Event | Ongoing operation |
| Expected Outcome | Admin dashboard shows volumes, decision times, distributions; events emitted for key milestones |
| Dependencies | Event bus and metrics pipeline |
| Ambiguities | Dashboard refresh interval (default 5 minutes) |
| Assumptions | Metric collectors in place |
| Blocking Questions | None |

#### Requirement Text

The admin dashboard shall show application volumes, average decision time, AI recommendation distribution, and approval rates; system shall emit structured events for key lifecycle milestones.

---

### REQ-015 — Escalation and SLA for Underwriter Queue

| Field | Value |
|---|---|
| Type | Operational |
| Source Section | FR-019 |
| Actor | System / Team Lead |
| Business Object | Queue items |
| Trigger / Event | Unactioned items for 4 business hours |
| Expected Outcome | Escalation notification to team lead |
| Dependencies | Notification service and calendar/business hours config |
| Ambiguities | Business hours config specifics |
| Assumptions | Team lead contact configured |
| Blocking Questions | None |

#### Requirement Text

Unactioned applications in the underwriter queue shall trigger an escalation notification to the team lead after 4 business hours.

---

## Open Questions

| OQ-NNN | Question | Source REQ | Blocking? | Owner | Status |
|---|---|---|---|---|---|
| OQ-001 | What is the approved AI model vendor / approach (in-house vs third-party)? | REQ-004 | Yes | Head of AI | Open |
| OQ-003 | HMRC KYC fallback behaviour — manual verification or auto-refer? | REQ-007 | Yes | Compliance | Open |
| OQ-004 | Additional AML data providers required (Dow Jones)? | REQ-007 | Yes | Compliance | Open |
| OQ-REQ-001 | Clarify definitive list of mandatory vs optional application fields and exact formats (e.g., NI format) | REQ-001 | No | Product Owner | Open |
| OQ-REQ-002 | Clarify edge cases for field value boundaries (amounts, DOB validation) | REQ-002 | No | Product Owner | Open |

---

## Assumptions

| ASM-NNN | Assumption | Source REQ | Risk if Wrong | Validation Approach | Status |
|---|---|---|---|---|---|
| ASM-001 | Experian enterprise contract available | REQ-006 | High | Confirm procurement contract | Open |
| ASM-002 | DocuSign enterprise contract available | REQ-009 | Medium | Confirm procurement contract | Open |

---

## Traceability Notes

All major BRS sections (Intake, Scoring, AML/KYC, Underwriter workflow, Offer, Disbursement, Observability) are covered by REQ-001..REQ-015. Blocking open questions OQ-001, OQ-003, and OQ-004 must be resolved before certain integrations and model deployment.

---
*Set Status: Accepted only after human review. Never self-accept.*

---
## Source FR → REQ Mapping

| Source FR | Canonical REQ |
|---|---|
| FR-001 | REQ-001 |
| FR-002 | REQ-002 |
| FR-003 | REQ-001 |
| FR-004 | REQ-003 |
| FR-005 | REQ-001 |
| FR-006 | REQ-004 |
| FR-007 | REQ-004 |
| FR-008 | REQ-004 |
| FR-009 | REQ-006 |
| FR-010 | REQ-005 |
| FR-011 | REQ-004 |
| FR-012 | REQ-007 |
| FR-013 | REQ-007 |
| FR-014 | REQ-007 |
| FR-015 | REQ-005 |
| FR-016 | REQ-008 |
| FR-017 | REQ-008 |
| FR-018 | REQ-008 |
| FR-019 | REQ-015 |
| FR-020 | REQ-009 |
| FR-021 | REQ-009 |
| FR-022 | REQ-009 |
| FR-023 | REQ-009 |
| FR-024 | REQ-010 |
| FR-025 | REQ-010 |
| FR-026 | REQ-010 |
| FR-027 | REQ-010 |
| FR-028 | REQ-011 |
| FR-029 | REQ-014 |
| FR-030 | REQ-014 |

This mapping is authoritative for traceability between the original BRS `FR-` identifiers and the canonical `REQ-` identifiers used across planning artifacts.
