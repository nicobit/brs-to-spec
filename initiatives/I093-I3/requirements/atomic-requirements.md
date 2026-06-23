# Atomic Requirements

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I093-I3 |
| Created at | 2026-06-22 |
| Created by | product-owner |
| Status | Draft |

---

## Summary

| Metric | Value |
|---|---|
| Total requirements | 37 |
| Functional | 30 |
| Non-functional | 7 |
| Data | 4 |
| Integration | 4 |
| Security | 4 |
| Operational | 3 |
| Reporting | 1 |
| Blocking questions | 5 |

---

## Requirement Catalogue

| ID | Title |
|---|---|
| FR-001 | Online application intake fields |
| NFR-001 | Page load performance |
| C-001 | UK data residency constraint |

### FR-001 — Online application intake fields

| Field | Value |
|---|---|
| ID | FR-001 |
| Type | Functional |
| Source Section | Epic 1 — Loan Application Intake (FR-001) |
| Actor | Applicant, Frontend UI |
| Business Object | Loan application |
| Trigger / Event | Applicant submits application form |
| Expected Outcome | Application accepted when mandatory fields provided; returns ARN |
| Dependencies | REQ-002, REQ-003 |
| Ambiguities | Edge cases for optional fields formatting |
| Assumptions | NI number format available from HMRC checks |
| Blocking Questions | OQ-003, OQ-004 |

| Propagated To Stories | S-003.1, S-003.2, S-003.3 |

#### Requirement Text

The system shall allow an applicant to submit a personal loan application online with full name, date of birth, national insurance number, employment status, annual income, loan amount requested (£1,000–£50,000), loan purpose, and repayment term (12–84 months).\

---

### FR-002 — Inline validation before submission

| Field | Value |
|---|---|
| ID | FR-002 |
| Type | Functional |
| Source Section | FR-002 |
| Actor | Frontend UI |
| Business Object | Loan application form |
| Trigger / Event | User input prior to submit |
| Expected Outcome | Inline validation prevents incomplete submission |
| Dependencies | REQ-001 |
| Ambiguities | Validation messages localization |
| Assumptions | Standard validation library used |
| Blocking Questions | None |

#### Requirement Text

The system shall validate all mandatory fields and display inline validation errors before submission; incomplete applications shall not be submitted.

---

### FR-003 — Assign Application Reference Number

| Field | Value |
|---|---|
| ID | FR-003 |
| Type | Functional |
| Source Section | FR-003 |
| Actor | System |
| Business Object | Application Reference Number (ARN) |
| Trigger / Event | On successful submission |
| Expected Outcome | Unique ARN assigned and displayed to applicant |
| Dependencies | REQ-001 |
| Ambiguities | ARN format constraints |
| Assumptions | ARN uniqueness guaranteed by central service |
| Blocking Questions | None |

#### Requirement Text

The system shall assign a unique Application Reference Number (ARN) to every submitted application and display it to the applicant immediately after submission.

---

### FR-004 — Submission confirmation email

| Field | Value |
|---|---|
| ID | FR-004 |
| Type | Functional |
| Source Section | FR-004 |
| Actor | System, Email Service |
| Business Object | Confirmation email |
| Trigger / Event | After submission |
| Expected Outcome | Email sent within 2 minutes containing ARN and timeline |
| Dependencies | REQ-003 |
| Ambiguities | Email deliverability SLAs |
| Assumptions | Email provider available |
| Blocking Questions | None |

#### Requirement Text

The system shall send an email confirmation to the applicant within 2 minutes of submission, containing the ARN and an estimated decision timeline.

---

### FR-005 — Application status retrieval by ARN

| Field | Value |
|---|---|
| ID | FR-005 |
| Type | Functional |
| Source Section | FR-005 |
| Actor | Applicant |
| Business Object | Application status |
| Trigger / Event | Applicant query with ARN and DOB |
| Expected Outcome | Status returned without requiring account registration |
| Dependencies | REQ-003 |
| Ambiguities | Rate limiting for anonymous queries |
| Assumptions | ARN + DOB sufficiently secure for status lookup |
| Blocking Questions | None |

#### Requirement Text

The system shall allow an applicant to retrieve the status of their application using their ARN and date of birth, without requiring account registration.

---

### FR-006 — AI pre-screening trigger

| Field | Value |
|---|---|
| ID | FR-006 |
| Type | Functional |
| Source Section | FR-006 |
| Actor | System, AI scoring pipeline |
| Business Object | Scoring job |
| Trigger / Event | On application submission (or within 60s) |
| Expected Outcome | AI pre-screening runs within 60s of submission |
| Dependencies | REQ-001, REQ-003 |
| Ambiguities | Queueing behaviour under load |
| Assumptions | Asynchronous processing supported |
| Blocking Questions | None |

#### Requirement Text

The system shall automatically trigger an AI pre-screening assessment for every submitted application within 60 seconds of submission.

---

### FR-007 — AI scoring model output

| Field | Value |
|---|---|
| ID | FR-007 |
| Type | Functional |
| Source Section | FR-007 |
| Actor | AI model |
| Business Object | Risk score and recommendation |
| Trigger / Event | After scoring completes |
| Expected Outcome | Produce risk score (0–1000) and recommendation `AUTO_APPROVE`/`REFER_TO_UNDERWRITER`/`AUTO_DECLINE` |
| Dependencies | REQ-006 |
| Ambiguities | Score calibration and thresholds |
| Assumptions | Model explainability attached to result |
| Blocking Questions | OQ-001 (model vendor) |

#### Requirement Text

The AI pre-screening shall produce a risk score (0–1000) and a recommendation: `AUTO_APPROVE`, `REFER_TO_UNDERWRITER`, or `AUTO_DECLINE`.

---

### FR-008 — AI model inputs

| Field | Value |
|---|---|
| ID | FR-008 |
| Type | Functional/Data |
| Source Section | FR-008 |
| Actor | AI scoring pipeline |
| Business Object | Scoring inputs |
| Trigger / Event | Before scoring |
| Expected Outcome | Inputs include applicant data, credit bureau, debt-to-income, loan-to-income, employment stability, credit history length |
| Dependencies | REQ-009 |
| Ambiguities | Weighting of each input |
| Assumptions | Required fields present in BRS |
| Blocking Questions | None |

#### Requirement Text

The AI scoring model shall use applicant-provided data, credit bureau data, debt-to-income ratio, loan-to-income ratio, employment stability, and credit history length as inputs.

---

### FR-009 — Experian integration for credit report

| Field | Value |
|---|---|
| ID | FR-009 |
| Type | Integration |
| Source Section | FR-009 |
| Actor | System, Experian API |
| Business Object | Credit report |
| Trigger / Event | On scoring request |
| Expected Outcome | Credit report retrieved within 30s or route to underwriter if unavailable |
| Dependencies | Integration contract (Doc) |
| Ambiguities | Retry/backoff policy specifics |
| Assumptions | Enterprise contract with Experian exists |
| Blocking Questions | None |

#### Requirement Text

The system shall integrate with Experian CreditExpert API to retrieve a credit report for every application; the integration shall complete within 30 seconds, and if Experian is unavailable the application shall be routed to `REFER_TO_UNDERWRITER`.

---

### FR-010 — Auto-approve flow for low loans

| Field | Value |
|---|---|
| ID | FR-010 |
| Type | Functional |
| Source Section | FR-010 |
| Actor | System |
| Business Object | Offer generation flow |
| Trigger / Event | AI recommendation `AUTO_APPROVE` and loan ≤ £10,000 |
| Expected Outcome | Proceed to offer generation without underwriter subject to AML/KYC |
| Dependencies | REQ-012 |
| Ambiguities | Compound conditions for exceptions |
| Assumptions | AML/KYC must pass first |
| Blocking Questions | None |

#### Requirement Text

Applications with recommendation `AUTO_APPROVE` and loan amount ≤£10,000 shall proceed directly to offer generation without underwriter review, subject to AML/KYC clearance.

---

### FR-011 — Auto-decline notifications and cooling-off

| Field | Value |
|---|---|
| ID | FR-011 |
| Type | Functional |
| Source Section | FR-011 |
| Actor | System, Applicant |
| Business Object | Decline notification |
| Trigger / Event | Recommendation `AUTO_DECLINE` |
| Expected Outcome | Applicant notified within 5 minutes; 30-day cooling-off enforced |
| Dependencies | REQ-003 |
| Ambiguities | Decline reason categories mapping |
| Assumptions | Communication channels available |
| Blocking Questions | None |

#### Requirement Text

Applications with recommendation `AUTO_DECLINE` shall be notified within 5 minutes with a decline reason category (not the score). A cooling-off period of 30 days shall be enforced before the same applicant can reapply.

---

### FR-012 — AML screening before offer generation

| Field | Value |
|---|---|
| ID | FR-012 |
| Type | Security/Functional |
| Source Section | FR-012 |
| Actor | System, AML service |
| Business Object | AML screening result |
| Trigger / Event | Before any offer generation |
| Expected Outcome | AML screening against HM Treasury lists completes within 60s; failures flagged as `COMPLIANCE_HOLD` |
| Dependencies | Integration with AML provider |
| Ambiguities | Additional sanction lists scope |
| Assumptions | HM Treasury list sufficient per BRS |
| Blocking Questions | None |

#### Requirement Text

The system shall perform AML screening on every applicant against HM Treasury sanctions list and PEP database before any offer is generated; AML screening shall complete within 60 seconds.

---

### FR-013 — KYC identity verification via HMRC

| Field | Value |
|---|---|
| ID | FR-013 |
| Type | Integration/Security |
| Source Section | FR-013 |
| Actor | System, HMRC API |
| Business Object | Identity verification result |
| Trigger / Event | Before offer generation |
| Expected Outcome | Cross-reference NI, name, DOB against HMRC; failures flagged `COMPLIANCE_HOLD` |
| Dependencies | HMRC availability |
| Ambiguities | Fallback when HMRC unavailable (OQ-003) |
| Assumptions | HMRC API contract exists |
| Blocking Questions | OQ-003 |

#### Requirement Text

The system shall perform KYC identity verification by cross-referencing the applicant's NI number, name, and date of birth against the HMRC identity verification API.

---

### FR-014 — Compliance hold routing

| Field | Value |
|---|---|
| ID | FR-014 |
| Type | Functional/Operational |
| Source Section | FR-014 |
| Actor | System, Compliance team |
| Business Object | Application status |
| Trigger / Event | AML/KYC failure |
| Expected Outcome | Flag as `COMPLIANCE_HOLD` and notify applicant; no offer generated |
| Dependencies | REQ-012, REQ-013 |
| Ambiguities | Notification wording; HMRC KYC fallback; AML provider list |
| Assumptions | Compliance team reachable for manual review |
| Blocking Questions | None |

#### Requirement Text

Any application that fails AML screening or KYC verification shall be flagged as `COMPLIANCE_HOLD` and routed to the compliance team; the applicant shall receive a notification and no offer shall be generated.

---

### FR-015 — Underwriter queue presentation

| Field | Value |
|---|---|
| ID | FR-015 |
| Type | Functional |
| Source Section | FR-015 |
| Actor | System, Underwriter |
| Business Object | Underwriter queue item |
| Trigger / Event | Recommendation `REFER_TO_UNDERWRITER` or `AUTO_APPROVE` above £10k |
| Expected Outcome | Application appears in underwriter queue within 2 minutes of scoring completion |
| Dependencies | REQ-007, REQ-009 |
| Ambiguities | Queue prioritization rules |
| Assumptions | Real-time messaging available |
| Blocking Questions | None |

#### Requirement Text

The system shall present applications with `REFER_TO_UNDERWRITER` recommendation, or any `AUTO_APPROVE` application above £10,000, to the underwriter queue within 2 minutes of AI scoring completion.

---

### FR-016 — Underwriter dashboard fields

| Field | Value |
|---|---|
| ID | FR-016 |
| Type | Functional |
| Source Section | FR-016 |
| Actor | Underwriter |
| Business Object | Dashboard view |
| Trigger / Event | Underwriter opens application |
| Expected Outcome | Dashboard shows applicant summary, AI score, credit summary, ratios, employment and AML/KYC status |
| Dependencies | REQ-009, REQ-012, REQ-013 |
| Ambiguities | UI layout specifics |
| Assumptions | Data aggregation service available |
| Blocking Questions | None |

#### Requirement Text

The underwriter dashboard shall display for each application: applicant summary, AI risk score and recommendation, credit bureau summary, debt-to-income ratio, loan-to-income ratio, employment verification status, and AML/KYC status.

---

### FR-017 — Underwriter actions recorded immutably

| Field | Value |
|---|---|
| ID | FR-017 |
| Type | Functional/Security |
| Source Section | FR-018 |
| Actor | Underwriter, System |
| Business Object | Audit record |
| Trigger / Event | Underwriter decision/action |
| Expected Outcome | Record underwriter ID, timestamp, action, reason, AI recommendation immutably |
| Dependencies | Audit log store |
| Ambiguities | Immutability mechanism (append-only ledger) |
| Assumptions | Tamper-evident store available |
| Blocking Questions | None |

#### Requirement Text

The system shall record every underwriter action with underwriter ID, timestamp, action taken, reason or conditions, and the AI recommendation presented; this record shall be immutable.

---

### FR-018 — Underwriter action options

| Field | Value |
|---|---|
| ID | FR-018 |
| Type | Functional |
| Source Section | FR-017 |
| Actor | Underwriter |
| Business Object | Underwriter decision |
| Trigger / Event | Underwriter review |
| Expected Outcome | Underwriter can approve (with conditions), decline (with reason), or request more info |
| Dependencies | REQ-016 |
| Ambiguities | Workflow for requests for info |
| Assumptions | Communication channel to applicant exists |
| Blocking Questions | None |

#### Requirement Text

The underwriter shall be able to approve the application (with optional conditions), decline the application (with mandatory reason), or request additional information from the applicant.

---

### FR-019 — Underwriter queue escalation

| Field | Value |
|---|---|
| ID | FR-019 |
| Type | Operational |
| Source Section | FR-019 |
| Actor | System, Team lead |
| Business Object | Escalation notification |
| Trigger / Event | Unactioned application in queue for 4 business hours |
| Expected Outcome | Escalation notification sent to team lead |
| Dependencies | Work hours calendar |
| Ambiguities | Business hours timezone handling |
| Assumptions | Notification routing available |
| Blocking Questions | None |

#### Requirement Text

Unactioned applications in the underwriter queue shall trigger an escalation notification to the team lead after 4 business hours.

---

### FR-020 — Loan offer generation content

| Field | Value |
|---|---|
| ID | FR-020 |
| Type | Functional |
| Source Section | FR-020 |
| Actor | System |
| Business Object | Loan offer document |
| Trigger / Event | Approval/Auto-approve completion |
| Expected Outcome | Offer contains approved amount, APR, monthly repayment, total repayable, term, T&Cs |
| Dependencies | REQ-010, REQ-012 |
| Ambiguities | Legal text versioning |
| Assumptions | Doc generation service available |
| Blocking Questions | None |

#### Requirement Text

The system shall generate a loan offer document for every approved application containing approved loan amount, interest rate (APR), monthly repayment amount, total repayable amount, repayment term, and key terms and conditions.

---

### FR-021 — Offer presentation and validity

| Field | Value |
|---|---|
| ID | FR-021 |
| Type | Functional |
| Source Section | FR-021 |
| Actor | System, Applicant |
| Business Object | Offer validity |
| Trigger / Event | Offer created |
| Expected Outcome | Offer presented via portal and email; valid for 14 days |
| Dependencies | REQ-020 |
| Ambiguities | Timezone on validity period |
| Assumptions | Email deliverability |
| Blocking Questions | None |

#### Requirement Text

The loan offer shall be presented to the applicant via their self-service portal and via email. The offer shall be valid for 14 days.

---

### FR-022 — E-signature acceptance logging

| Field | Value |
|---|---|
| ID | FR-022 |
| Type | Integration/Operational |
| Source Section | FR-022 |
| Actor | System, DocuSign |
| Business Object | Acceptance record |
| Trigger / Event | Applicant signs offer |
| Expected Outcome | Acceptance logged with timestamp and IP address |
| Dependencies | DocuSign integration |
| Ambiguities | IP capture under privacy rules |
| Assumptions | DocuSign integration exists |
| Blocking Questions | None |

#### Requirement Text

The applicant shall be able to digitally accept the loan offer using e-signature (DocuSign integration); acceptance shall be logged with timestamp and IP address.

---

### FR-023 — Cooling-off period enforcement and reminders

| Field | Value |
|---|---|
| ID | FR-023 |
| Type | Functional/Operational |
| Source Section | FR-023 |
| Actor | System |
| Business Object | Cooling-off workflow |
| Trigger / Event | Offer acceptance |
| Expected Outcome | 14-day cooling-off enforced; reminders sent at day 7 and day 13 |
| Dependencies | Notification service |
| Ambiguities | Reminder channels |
| Assumptions | Applicant contact details valid |
| Blocking Questions | None |

#### Requirement Text

The system shall enforce a 14-day cooling-off period after digital acceptance during which the applicant may withdraw without penalty; the system shall send reminders at day 7 and day 13.

---

### FR-024 — Disbursement trigger to core banking

| Field | Value |
|---|---|
| ID | FR-024 |
| Type | Integration/Functional |
| Source Section | FR-024 |
| Actor | System, Core banking (T24) |
| Business Object | Disbursement instruction |
| Trigger / Event | Cooling-off expiry or waiver |
| Expected Outcome | Disbursement instruction sent to T24 via internal payment gateway API |
| Dependencies | Integration contract with T24 |
| Ambiguities | Retry/backoff policy specifics |
| Assumptions | Internal payment gateway available |
| Blocking Questions | OQ-005 |

#### Requirement Text

Upon digital acceptance and cooling-off expiry (or applicant waiver), the system shall trigger a disbursement instruction to the core banking system (Temenos T24) via the internal payment gateway API.

---

### FR-025 — Disbursement instruction content

| Field | Value |
|---|---|
| ID | FR-025 |
| Type | Functional |
| Source Section | FR-025 |
| Actor | System |
| Business Object | Disbursement message |
| Trigger / Event | Disbursement instruction creation |
| Expected Outcome | Include account number, sort code, amount, reference, value date |
| Dependencies | REQ-024 |
| Ambiguities | Sensitive data handling in logs |
| Assumptions | Bank account verification in place |
| Blocking Questions | None |

#### Requirement Text

The disbursement instruction shall include applicant account number, sort code, loan amount, reference number, and value date.

---

### FR-026 — Disbursement confirmation handling

| Field | Value |
|---|---|
| ID | FR-026 |
| Type | Functional/Operational |
| Source Section | FR-026 |
| Actor | System, Core banking |
| Business Object | Disbursement confirmation |
| Trigger / Event | T24 confirmation receipt |
| Expected Outcome | Update application to `DISBURSED`; retry once if no confirmation within 2 minutes then alert operations |
| Dependencies | REQ-024 |
| Ambiguities | Alerting channel specifics |
| Assumptions | Core banking responds to API calls |
| Blocking Questions | None |

#### Requirement Text

The system shall receive a disbursement confirmation from the core banking system and update the application status to `DISBURSED`. If confirmation is not received within 2 minutes, the system shall retry once and then alert the operations team.

---

### FR-027 — Disbursement notification to applicant

| Field | Value |
|---|---|
| ID | FR-027 |
| Type | Functional |
| Source Section | FR-027 |
| Actor | System, Applicant |
| Business Object | Notification |
| Trigger / Event | Disbursement confirmation |
| Expected Outcome | Applicant receives email and portal notification confirming disbursement and expected value date |
| Dependencies | REQ-026 |
| Ambiguities | Notification formatting |
| Assumptions | Contact details valid |
| Blocking Questions | None |

#### Requirement Text

The applicant shall receive an email and portal notification confirming disbursement with the expected value date.

---

### FR-028 — Immutable audit log of state transitions

| Field | Value |
|---|---|
| ID | FR-028 |
| Type | Reporting/Security |
| Source Section | FR-028 |
| Actor | System |
| Business Object | Audit log |
| Trigger / Event | Every state transition or action |
| Expected Outcome | Immutable audit log with previous/new state, actor, timestamp, snapshot |
| Dependencies | Audit storage solution |
| Ambiguities | Retention policy specifics |
| Assumptions | WORM or append-only store available |
| Blocking Questions | None |

#### Requirement Text

The system shall maintain an immutable audit log of every state transition for every application, including previous state, new state, triggering actor, timestamp, and relevant data snapshot.

---

### FR-029 — Admin dashboard metrics

| Field | Value |
|---|---|
| ID | FR-029 |
| Type | Reporting |
| Source Section | FR-029 |
| Actor | Admin user |
| Business Object | Dashboard |
| Trigger / Event | Dashboard view refresh |
| Expected Outcome | Provide volume by status, average decision time, AI distribution, approval rates, AML/KYC hold rates; refresh every 5 minutes |
| Dependencies | Observability pipeline |
| Ambiguities | Time window selection |
| Assumptions | Metrics pipeline in place |
| Blocking Questions | None |

#### Requirement Text

The admin dashboard shall provide application volume by status, average decision time, AI recommendation distribution, approval/decline rates by underwriter, and AML/KYC hold rates; data shall refresh every 5 minutes.

---

### FR-030 — Observability event emission

| Field | Value |
|---|---|
| ID | FR-030 |
| Type | Operational |
| Source Section | FR-030 |
| Actor | System |
| Business Object | Observability events |
| Trigger / Event | Key lifecycle events (submission, scoring, AML/KYC, decision, acceptance, disbursement) |
| Expected Outcome | Emit structured events including ARN, timestamp, status, actor |
| Dependencies | Event pipeline |
| Ambiguities | Event schema versioning |
| Assumptions | Event bus available |
| Blocking Questions | None |

#### Requirement Text

The system shall emit structured observability events for application submission, AI scoring completion, AML/KYC result, underwriter decision, offer acceptance, and disbursement; events must include ARN, timestamp, status, and actor.

---

### NFR-001 — Page load performance

| Field | Value |
|---|---|
| ID | NFR-001 |
| Type | Non-functional |
| Source Section | NFR-001 |
| Actor | System |
| Business Object | Application intake page |
| Trigger / Event | Page load |
| Expected Outcome | Intake form loads within 2 seconds on standard broadband |
| Dependencies | Frontend performance optimizations |
| Ambiguities | Definition of standard broadband |
| Assumptions | CDN in use |
| Blocking Questions | None |

#### Requirement Text

The application intake form shall load within 2 seconds on a standard broadband connection.

---

### NFR-002 — AI scoring pipeline latency

| Field | Value |
|---|---|
| ID | NFR-002 |
| Type | Non-functional |
| Source Section | NFR-002 |
| Actor | System |
| Business Object | Scoring pipeline |
| Trigger / Event | Scoring request |
| Expected Outcome | End-to-end scoring completes within 90 seconds under normal load |
| Dependencies | Infrastructure sizing |
| Ambiguities | Definition of normal load |
| Assumptions | Load testing will define thresholds |
| Blocking Questions | None |

#### Requirement Text

The AI scoring pipeline shall complete end-to-end within 90 seconds under normal load.

---

### NFR-003 — Concurrency

| Field | Value |
|---|---|
| ID | NFR-003 |
| Type | Non-functional |
| Source Section | NFR-003 |
| Actor | System |
| Business Object | Submission throughput |
| Trigger / Event | Peak concurrent submissions |
| Expected Outcome | Support 500 concurrent application submissions |
| Dependencies | Autoscaling |
| Ambiguities | Measurement of concurrency |
| Assumptions | Horizontal scaling available |
| Blocking Questions | None |

#### Requirement Text

The system shall support 500 concurrent application submissions.

---

### NFR-004 — Encryption and data protection

| Field | Value |
|---|---|
| ID | NFR-004 |
| Type | Security/Non-functional |
| Source Section | NFR-004 |
| Actor | System |
| Business Object | PII data stores and transport |
| Trigger / Event | Data at rest/in transit |
| Expected Outcome | PII encrypted at rest (AES-256) and in transit (TLS 1.3) |
| Dependencies | Key management service |
| Ambiguities | Key rotation policy |
| Assumptions | KMS available in UK region |
| Blocking Questions | None |

#### Requirement Text

All PII shall be encrypted at rest (AES-256) and in transit (TLS 1.3).

---

### NFR-005 — Audit log tamper-evidence

| Field | Value |
|---|---|
| ID | NFR-005 |
| Type | Non-functional/Security |
| Source Section | NFR-005 |
| Actor | System |
| Business Object | Audit log |
| Trigger / Event | Log writes |
| Expected Outcome | Audit log is write-once and tamper-evident |
| Dependencies | Storage solution |
| Ambiguities | Retention policy |
| Assumptions | WORM or append-only storage available |
| Blocking Questions | None |

#### Requirement Text

Audit log shall be write-once and tamper-evident.

---

### NFR-006 — Availability

| Field | Value |
|---|---|
| ID | NFR-006 |
| Type | Non-functional |
| Source Section | NFR-006 |
| Actor | System |
| Business Object | Platform uptime |
| Trigger / Event | Operational monitoring |
| Expected Outcome | 99.9% uptime during business hours (08:00–20:00 GMT) |
| Dependencies | High-availability architecture |
| Ambiguities | Measurement window |
| Assumptions | SLO monitoring configured |
| Blocking Questions | None |

#### Requirement Text

System shall achieve 99.9% uptime during business hours (08:00–20:00 GMT).

---

### NFR-007 — Integration resilience

| Field | Value |
|---|---|
| ID | NFR-007 |

---

### C-001 — UK data residency constraint

| Field | Value |
|---|---|
| ID | C-001 |
| Type | Constraint |
| Source Section | Constraints |
| Actor | System, Data Platform |
| Business Object | PII and production data |
| Trigger / Event | Any data storage or processing |
| Expected Outcome | All PII remains within UK-hosted data centres; no cross-border replication without explicit ADR and legal approval |
| Dependencies | Cloud region configuration |
| Ambiguities | DR replication strategy for cross-region resilience |
| Assumptions | UK-region KMS available |
| Blocking Questions | None |

#### Requirement Text

All production PII and related audit data must remain within UK-hosted data centres unless a documented ADR and legal approval allow otherwise.
| Type | Non-functional/Integration |
| Source Section | NFR-007 |
| Actor | System |
| Business Object | External API integrations |
| Trigger / Event | External API calls (Experian, HMRC, DocuSign, T24) |
| Expected Outcome | Implement circuit breakers and defined fallback behaviours |
| Dependencies | Resilience libraries |
| Ambiguities | Fallback routes for each provider |
| Assumptions | Provider SLAs known |
| Blocking Questions | None |

#### Requirement Text

All API integrations (Experian, HMRC, DocuSign, T24) shall implement circuit breakers with defined fallback behaviour.

---

## Open Questions

| OQ-NNN | Question | Source REQ | Blocking? | Owner | Status |
|---|---|---|---|---|---|
| OQ-001 | What is the approved AI model vendor / approach for risk scoring? | REQ-007 | Yes | Head of AI | Open |
| OQ-002 | Does the cooling-off period waiver require a separate legal sign-off flow? | REQ-023 | No | Legal | Open |
| OQ-003 | What is the fallback for HMRC KYC API when unavailable — manual verification or auto-refer? | REQ-013; FR-014 | Yes | Compliance | Closed — see `input/checklists/hmrc-kvc-fallback.md` |
| OQ-004 | What AML database providers beyond HM Treasury are required (Dow Jones, others)? | REQ-012; FR-014 | Yes | Compliance | Closed — see `input/decisions/aml-provider-decision.md` |
| OQ-005 | Is the T24 payment gateway contract already defined or does it need API negotiation? | REQ-024 | Yes | IT Architecture | Open |

---

## Assumptions

| ASM-NNN | Assumption | Source REQ | Risk if Wrong | Validation Approach | Status |
|---|---|---|---|---|---|
| ASM-001 | Enterprise contract exists with Experian | REQ-009 | High | Verify contract documents | Open |
| ASM-002 | DocuSign integration available under enterprise contract | REQ-022 | Medium | Verify contract | Open |
| ASM-003 | Core banking integration details can be defined | REQ-024 | High | Confirm with T24 owners | Open |

---

## Traceability Notes

This catalogue maps the primary functional and non-functional requirements described in the BRS into atomic, testable entries. Each REQ references the BRS section that motivated it. Additional BRS subsections or later clarifications may produce further REQs.

---
*Set Status: Accepted only after human review. Never self-accept.*
