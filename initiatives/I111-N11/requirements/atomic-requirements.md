# Atomic Requirements

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I111-N11 |
| Created at | 2026-06-22 |
| Created by | product-owner |
| Status | Draft |

---

## Summary

| Metric | Value |
|---|---|
| Total requirements | 35 |
| Functional | 22 |
| Non-functional | 6 |
| Data | 2 |
| Integration | 3 |
| Security | 1 |
| Operational | 1 |
| Reporting | 0 |
| Blocking questions | 3 |

---

## Source References

| FR-001 | REQ-001 |
| FR-002 | REQ-002 |
| FR-003 | REQ-001 |
| FR-004 | REQ-003 |
| FR-005 | REQ-004 |
| FR-006 | REQ-005 |
| FR-007 | REQ-006 |
| FR-008 | REQ-006 |
| FR-009 | REQ-007 |
| FR-010 | REQ-008 |
| FR-011 | REQ-009 |
| FR-012 | REQ-010 |
| FR-013 | REQ-011 |
| FR-014 | REQ-010 |
| FR-015 | REQ-012 |
| FR-016 | REQ-012 |
| FR-017 | REQ-013 |
| FR-018 | REQ-013 |
| FR-019 | REQ-013 |
| FR-020 | REQ-014 |
| FR-021 | REQ-014 |
| FR-022 | REQ-015 |
| FR-023 | REQ-015 |
| FR-024 | REQ-016 |
| FR-025 | REQ-016 |
| FR-026 | REQ-017 |
| FR-027 | REQ-017 |
| FR-028 | REQ-018 |
| FR-029 | REQ-019 |
| FR-030 | REQ-019 |

| NFR-001 | REQ-020 |
| NFR-002 | REQ-020 |
| NFR-003 | REQ-021 |
| NFR-004 | REQ-022 |
| NFR-005 | REQ-018 |
| NFR-006 | REQ-021 |
| NFR-007 | REQ-023 |

---

## Requirement Catalogue

### REQ-001 — Application submission UI

| Field | Value |
|---|---|
| Requirement ID | REQ-001 |
| Type | functional |
| Source Section | FR-001 — Epic 1 — Loan Application Intake |
| Actor | Applicant (external user) |
| Business Object | Application |
| Trigger / Event | Applicant submits application form |
| Expected Outcome | Application accepted or rejected immediately with validation feedback; ARN assigned on success |
| Dependencies | None |
| Ambiguities | None |
| Assumptions | Applicant can provide NI number and DOB |
| Blocking Questions | None |

#### Requirement Text

The system shall allow an applicant to submit a personal loan application online with required fields; on successful submission the system shall assign a unique ARN and present it to the applicant. (FR-001, FR-003)

---

### REQ-002 — Inline validation on submission

| Field | Value |
|---|---|
| Requirement ID | REQ-002 |
| Type | functional |
| Source Section | FR-002 |
| Actor | Applicant, Client UI |
| Business Object | Application form |
| Trigger / Event | User attempts to submit incomplete form |
| Expected Outcome | Inline validation errors shown; incomplete submissions blocked |
| Dependencies | UI validation library |
| Ambiguities | Validation rules for optional fields |
| Assumptions | Standard field validation suffices |
| Blocking Questions | None |

#### Requirement Text

The system shall validate all mandatory fields and display inline validation errors before submission; incomplete applications shall not be submitted. (FR-002)

---

### REQ-003 — ARN email confirmation

| Field | Value |
|---|---|
| Requirement ID | REQ-003 |
| Type | functional |
| Source Section | FR-004 |
| Actor | System (Notification service) |
| Business Object | Application confirmation email |
| Trigger / Event | Successful application submission |
| Expected Outcome | Email sent within 2 minutes containing ARN and estimated timeline |
| Dependencies | Notification Service, Email provider |
| Ambiguities | Email deliverability SLAs |
| Assumptions | Email address provided is valid |
| Blocking Questions | None |

#### Requirement Text

The system shall send an email confirmation to the applicant within 2 minutes of submission containing the ARN and an estimated decision timeline. (FR-004)

---

### REQ-004 — Status retrieval by ARN

| Field | Value |
|---|---|
| Requirement ID | REQ-004 |
| Type | functional |
| Source Section | FR-005 |
| Actor | Applicant |
| Business Object | Application status |
| Trigger / Event | Applicant queries status with ARN + DOB |
| Expected Outcome | System returns current status without account registration |
| Dependencies | Authentication via ARN + DOB matching |
| Ambiguities | Rate limiting for lookups |
| Assumptions | ARN + DOB sufficient for identity check |
| Blocking Questions | None |

#### Requirement Text

The system shall allow an applicant to retrieve the status of their application using ARN and date of birth without requiring account registration. (FR-005)

---

### REQ-005 — AI pre-screening trigger

| Field | Value |
|---|---|
| Requirement ID | REQ-005 |
| Type | functional |
| Source Section | FR-006 |
| Actor | Loan Origination API / AI Scoring Service |
| Business Object | Application submission event |
| Trigger / Event | Application submitted (ARN assigned) |
| Expected Outcome | AI pre-screening triggered within 60 seconds |
| Dependencies | Service Bus, Scoring Service |
| Ambiguities | Message ordering under retries |
| Assumptions | Message bus available |
| Blocking Questions | OQ-001 (model vendor) |

#### Requirement Text

The system shall automatically trigger an AI pre-screening assessment for every submitted application within 60 seconds of submission. (FR-006)

---

### REQ-006 — AI scoring outputs

| Field | Value |
|---|---|
| Requirement ID | REQ-006 |
| Type | functional |
| Source Section | FR-007 |
| Actor | AI Scoring Service |
| Business Object | Risk score and recommendation |
| Trigger / Event | Pre-screening invocation completes |
| Expected Outcome | Produce risk score (0–1000) and recommendation label (AUTO_APPROVE|REFER_TO_UNDERWRITER|AUTO_DECLINE) |
| Dependencies | Model endpoint, Experian data (FR-009) |
| Ambiguities | Score calibration thresholds |
| Assumptions | Model returns numeric score and label |
| Blocking Questions | OQ-001 |

#### Requirement Text

The AI pre-screening shall produce a risk score (0–1000) and a recommendation label: AUTO_APPROVE, REFER_TO_UNDERWRITER, or AUTO_DECLINE. (FR-007)

---

### REQ-007 — Experian integration

| Field | Value |
|---|---|
| Requirement ID | REQ-007 |
| Type | integration |
| Source Section | FR-009 |
| Actor | AI Scoring Service, Integration layer |
| Business Object | Credit report |
| Trigger / Event | Scoring pipeline requests credit data |
| Expected Outcome | Credit report retrieved within 30s; fallback to REFER_TO_UNDERWRITER if unavailable |
| Dependencies | Experian API contract, circuit-breaker |
| Ambiguities | Retry policy tuning |
| Assumptions | Experian contract available |
| Blocking Questions | None |

#### Requirement Text

The system shall integrate with Experian CreditExpert API to retrieve a credit report for every application; integration shall complete within 30 seconds and fallback to REFER_TO_UNDERWRITER if Experian is unavailable. (FR-009)

---

### REQ-008 — Auto-approve routing

| Field | Value |
|---|---|
| Requirement ID | REQ-008 |
| Type | functional |
| Source Section | FR-010 |
| Actor | Loan Origination API |
| Business Object | Offer generation flow |
| Trigger / Event | Recommendation= AUTO_APPROVE and loan amount ≤ £10,000 |
| Expected Outcome | Proceed to offer generation subject to AML/KYC clearance |
| Dependencies | AML/KYC services |
| Ambiguities | Edge case for co-applicants |
| Assumptions | AML/KYC passed |
| Blocking Questions | None |

#### Requirement Text

Applications with recommendation AUTO_APPROVE and loan amount ≤ £10,000 shall proceed directly to offer generation without underwriter review, subject to AML/KYC clearance. (FR-010)

---

### REQ-009 — Auto-decline handling

| Field | Value |
|---|---|
| Requirement ID | REQ-009 |
| Type | functional |
| Source Section | FR-011 |
| Actor | Notification Service |
| Business Object | Applicant notification |
| Trigger / Event | Recommendation = AUTO_DECLINE |
| Expected Outcome | Notify applicant within 5 minutes with decline reason category; enforce 30-day cooling-off |
| Dependencies | Notification service |
| Ambiguities | Decline reason categories mapping |
| Assumptions | Cooling-off enforcement implemented |
| Blocking Questions | None |

#### Requirement Text

Applications with recommendation AUTO_DECLINE shall be notified within 5 minutes with a decline reason category and a 30-day cooling-off period enforced. (FR-011)

---

### REQ-010 — AML screening

| Field | Value |
|---|---|
| Requirement ID | REQ-010 |
| Type | functional |
| Source Section | FR-012 |
| Actor | Compliance Service |
| Business Object | AML screening result |
| Trigger / Event | Before offer generation |
| Expected Outcome | AML screening completes within 60s; failures flagged as COMPLIANCE_HOLD |
| Dependencies | HM Treasury sanctions API |
| Ambiguities | Additional provider inclusion (OQ-004) |
| Assumptions | HM Treasury provider used |
| Blocking Questions | None |

#### Requirement Text

The system shall perform AML screening against HM Treasury sanctions and PEP lists before any offer is generated; screening shall complete within 60 seconds. (FR-012)

---

### REQ-011 — KYC verification

| Field | Value |
|---|---|
| Requirement ID | REQ-011 |
| Type | functional |
| Source Section | FR-013 |
| Actor | Compliance Service |
| Business Object | Identity verification result |
| Trigger / Event | Prior to offer generation |
| Expected Outcome | Cross-reference NI number/name/DOB against HMRC API; failures routed to compliance team |
| Dependencies | HMRC API |
| Ambiguities | Fallback behaviour (OQ-003) |
| Assumptions | HMRC API available |
| Blocking Questions | OQ-003 |

#### Requirement Text

The system shall perform KYC identity verification by cross-referencing applicant NI, name, and DOB against HMRC identity verification API. (FR-013)

---

### REQ-012 — Underwriter queue presentation

| Field | Value |
|---|---|
| Requirement ID | REQ-012 |
| Type | functional |
| Source Section | FR-015 |
| Actor | Loan Origination API, Underwriter Dashboard |
| Business Object | Underwriter queue item |
| Trigger / Event | Recommendation REFER_TO_UNDERWRITER or AUTO_APPROVE > £10,000 |
| Expected Outcome | Present application in underwriter queue within 2 minutes of scoring completion |
| Dependencies | Application DB, Dashboard service |
| Ambiguities | Queue sizing under load |
| Assumptions | Scoring completes within SLA |
| Blocking Questions | None |

#### Requirement Text

The system shall present applications with REFER_TO_UNDERWRITER or AUTO_APPROVE above £10,000 to the underwriter queue within 2 minutes of scoring completion. (FR-015)

---

### REQ-013 — Underwriter action recording

| Field | Value |
|---|---|
| Requirement ID | REQ-013 |
| Type | functional |
| Source Section | FR-018 |
| Actor | Underwriter, Loan Origination API |
| Business Object | Underwriter action record |
| Trigger / Event | Underwriter takes action (approve/decline/request info) |
| Expected Outcome | Record action with ID, timestamp, reason, and AI recommendation; immutable |
| Dependencies | Audit Log Store (append-only) |
| Ambiguities | Retention policy for audit snapshots |
| Assumptions | Audit store write-once enabled |
| Blocking Questions | None |

#### Requirement Text

The system shall record every underwriter action with underwriter ID, timestamp, action, reason/conditions, and the AI recommendation presented; this record shall be immutable. (FR-018, FR-028)

---

### REQ-014 — Offer document generation

| Field | Value |
|---|---|
| Requirement ID | REQ-014 |
| Type | functional |
| Source Section | FR-020 |
| Actor | Loan Origination API, Offer generator |
| Business Object | Loan offer document |
| Trigger / Event | Application approved and AML/KYC cleared |
| Expected Outcome | Generate offer containing amount, APR, monthly repayment, total repayable, terms |
| Dependencies | Offer template, pricing service |
| Ambiguities | Interest rounding rules |
| Assumptions | Pricing inputs available |
| Blocking Questions | None |

#### Requirement Text

The system shall generate a loan offer document for every approved application containing approved amount, APR, monthly repayment, total repayable, term, and key terms. (FR-020)

---

### REQ-015 — E-signature acceptance

| Field | Value |
|---|---|
| Requirement ID | REQ-015 |
| Type | integration |
| Source Section | FR-022 |
| Actor | Applicant, DocuSign integration |
| Business Object | Digital acceptance record |
| Trigger / Event | Applicant accepts offer via e-signature |
| Expected Outcome | Acceptance logged with timestamp and IP; DocuSign integration validated |
| Dependencies | DocuSign API |
| Ambiguities | DocuSign callback reliability |
| Assumptions | DocuSign contract in place |
| Blocking Questions | None |

#### Requirement Text

The applicant shall be able to digitally accept the loan offer using DocuSign; acceptance shall be logged with timestamp and IP address. (FR-022)

---

### REQ-016 — Disbursement trigger

| Field | Value |
|---|---|
| Requirement ID | REQ-016 |
| Type | functional |
| Source Section | FR-024 |
| Actor | Loan Origination API, Payment Gateway Adapter |
| Business Object | Disbursement instruction |
| Trigger / Event | Acceptance and cooling-off expiry or waiver |
| Expected Outcome | Trigger disbursement to T24 with required fields |
| Dependencies | Payment Gateway adapter, T24 API |
| Ambiguities | Retry/backoff behavior for T24 failures |
| Assumptions | T24 API contract defined |
| Blocking Questions | OQ-005 |

#### Requirement Text

Upon digital acceptance and cooling-off expiry (or waiver), the system shall trigger a disbursement instruction to the core banking system via the payment gateway API. (FR-024)

---

### REQ-017 — Disbursement confirmation handling

| Field | Value |
|---|---|
| Requirement ID | REQ-017 |
| Type | functional |
| Source Section | FR-026 |
| Actor | Payment Gateway Adapter |
| Business Object | Disbursement confirmation |
| Trigger / Event | T24 returns confirmation |
| Expected Outcome | Update application status to DISBURSED; retry once if not received within 2 minutes then alert ops |
| Dependencies | T24 API, alerting subsystem |
| Ambiguities | Alerting thresholds |
| Assumptions | Network reliability sufficient |
| Blocking Questions | None |

#### Requirement Text

The system shall receive disbursement confirmation from the core banking system and update application status to DISBURSED; if not received within 2 minutes retry once then alert operations. (FR-026)

---

### REQ-018 — Immutable audit log

| Field | Value |
|---|---|
| Requirement ID | REQ-018 |
| Type | security |
| Source Section | FR-028 |
| Actor | Any system actor |
| Business Object | Audit record |
| Trigger / Event | Any state transition or key action |
| Expected Outcome | Immutable append-only audit record with snapshot, actor, timestamp |
| Dependencies | Cosmos DB append-only container |
| Ambiguities | Snapshot granularity |
| Assumptions | Cosmos DB append-only pattern supported |
| Blocking Questions | None |

#### Requirement Text

The system shall maintain an immutable audit log of every state transition including previous state, new state, triggering actor, timestamp, and relevant snapshot. (FR-028)

---

### REQ-019 — Observability events

| Field | Value |
|---|---|
| Requirement ID | REQ-019 |
| Type | operational |
| Source Section | FR-030 |
| Actor | All services |
| Business Object | Observability events |
| Trigger / Event | Submission, scoring completion, AML/KYC result, underwriter decision, offer acceptance, disbursement |
| Expected Outcome | Structured events emitted with ARN, timestamp, status, actor |
| Dependencies | Metrics and logging platform |
| Ambiguities | Event retention policies |
| Assumptions | CorrelationId included in events |
| Blocking Questions | None |

#### Requirement Text

The system shall emit structured observability events for key lifecycle milestones including ARN and actor metadata. (FR-030)

---

### REQ-020 — Performance requirement: scoring latency

| Field | Value |
|---|---|
| Requirement ID | REQ-020 |
| Type | non-functional |
| Source Section | NFR-002 |
| Actor | System |
| Business Object | Scoring pipeline latency |
| Trigger / Event | Scoring invocation |
| Expected Outcome | End-to-end scoring completes within 90 seconds under normal load |
| Dependencies | Model endpoint, Experian availability |
| Ambiguities | Definition of normal load |
| Assumptions | Adequate infra resources provisioned |
| Blocking Questions | None |

#### Requirement Text

AI scoring pipeline shall complete end-to-end within 90 seconds under normal load. (NFR-002)

---

### REQ-021 — Scalability requirement

| Field | Value |
|---|---|
| Requirement ID | REQ-021 |
| Type | non-functional |
| Source Section | NFR-003 |
| Actor | System |
| Business Object | Throughput |
| Trigger / Event | Concurrent submissions |
| Expected Outcome | System supports 500 concurrent submissions |
| Dependencies | Autoscaling, queueing |
| Ambiguities | Definition of concurrent submission handling |
| Assumptions | Load testing will validate |
| Blocking Questions | None |

#### Requirement Text

The system shall support 500 concurrent application submissions. (NFR-003)

---

### REQ-022 — Encryption requirement

| Field | Value |
|---|---|
| Requirement ID | REQ-022 |
| Type | security |
| Source Section | NFR-004 |
| Actor | System |
| Business Object | PII and data at rest/in transit |
| Trigger / Event | Any data storage or transfer |
| Expected Outcome | AES-256 at rest; TLS 1.3 in transit |
| Dependencies | Cloud provider encryption features |
| Ambiguities | Key management policy |
| Assumptions | Azure-managed keys used |
| Blocking Questions | None |

#### Requirement Text

All PII shall be encrypted at rest (AES-256) and in transit (TLS 1.3). (NFR-004)

---

### REQ-023 — Circuit-breaker requirement for integrations

| Field | Value |
|---|---|
| Requirement ID | REQ-023 |
| Type | integration |
| Source Section | NFR-007 |
| Actor | Integration layer |
| Business Object | External API calls |
| Trigger / Event | External API failures or latency spikes |
| Expected Outcome | Circuit-breaker and defined fallback behavior for Experian, HMRC, DocuSign, and T24 |
| Dependencies | Resilience libraries |
| Ambiguities | Threshold tuning |
| Assumptions | Standard resilience patterns applied |
| Blocking Questions | None |

#### Requirement Text

All API integrations shall implement circuit-breakers with defined fallback behaviour. (NFR-007)

---

### REQ-024 — Explainability requirement

| Field | Value |
|---|---|
| Requirement ID | REQ-024 |
| Type | non-functional |
| Source Section | Constraints (FCA) |
| Actor | AI Scoring Service |
| Business Object | Scoring result metadata |
| Trigger / Event | Each scoring decision |
| Expected Outcome | Explainability metadata and model card available for each decision |
| Dependencies | Model instrumentation |
| Ambiguities | Level of explanation required by regulator |
| Assumptions | Model supports explanation hooks |
| Blocking Questions | OQ-001 |

#### Requirement Text

AI model decisions must be explainable and include metadata sufficient for regulatory traceability. (Constraints / FCA)

---

## Open Questions

| OQ-NNN | Question | Source REQ | Blocking? | Owner | Status |
|---|---|---|---|---|---|
| OQ-001 | What is the approved AI model vendor/approach (in-house vs third-party)? | REQ-005 / REQ-006 / REQ-024 | Yes | Head of AI | Open |
| OQ-002 | Does cooling-off waiver require separate legal sign-off flow? | FR-021 | Medium | Legal | Answered: Not required |
| OQ-003 | HMRC KYC fallback: manual verification or auto-refer? | REQ-011 | Yes | Compliance | Open |
| OQ-004 | AML providers list: HM Treasury only or additional providers? | REQ-010 | High | Compliance | Open |
| OQ-005 | Is T24 payment gateway contract defined or needs negotiation? | REQ-016 | Yes | IT Architecture | Open |

---

## Assumptions

| ASM-NNN | Assumption | Source REQ | Risk if Wrong | Validation Approach | Status |
|---|---|---|---|---|---|
| ASM-001 | Experian contract and API stability | REQ-007 | High | Integration test in staging | Open |
| ASM-002 | DocuSign contract in place | REQ-015 | Medium | Confirm with commercial team | Open |
| ASM-003 | T24 API contract will be available for integration | REQ-016 | High | Confirm with IT Architecture | Open |

---

## Traceability Notes

All functional requirements above are extracted directly from the BRS sections (Epic 1..7). Non-functional requirements map to the BRS NFR section. Open questions align with the BRS `Open questions` table and must be resolved prior to readiness for impacted stories.

---
*Set Status: Accepted only after human review. Never self-accept.*

---
## Source Requirements (FR headings)

<!-- Minimal FR canonical sections to support traceability mapping -->

### FR-001 — Loan Application Intake: Submission

| Field | Value |
|---|---|
| Requirement ID | FR-001 |
| Type | functional |
| Source Section | BRS FR-001 |

#### Requirement Text

Applicant can submit a personal loan application via the online form. (source FR-001)

### FR-002 — Inline validation on submission

| Field | Value |
|---|---|
| Requirement ID | FR-002 |
| Type | functional |
| Source Section | BRS FR-002 |

#### Requirement Text

Inline validation must prevent incomplete submissions. (source FR-002)

### FR-003 — ARN assignment

| Field | Value |
|---|---|
| Requirement ID | FR-003 |
| Type | functional |
| Source Section | BRS FR-003 |

#### Requirement Text

System assigns ARN on successful submission. (source FR-003)

### FR-004 — ARN email confirmation

| Field | Value |
|---|---|
| Requirement ID | FR-004 |
| Type | functional |
| Source Section | BRS FR-004 |

#### Requirement Text

Email confirmation with ARN sent within SLA. (source FR-004)

### FR-005 — Status retrieval by ARN

| Field | Value |
|---|---|
| Requirement ID | FR-005 |
| Type | functional |
| Source Section | BRS FR-005 |

#### Requirement Text

Applicant can retrieve status using ARN and DOB. (source FR-005)

### FR-006 — AI pre-screening trigger

| Field | Value |
|---|---|
| Requirement ID | FR-006 |
| Type | functional |
| Source Section | BRS FR-006 |

#### Requirement Text

Trigger AI pre-screening within SLA. (source FR-006)

### FR-007 — AI scoring outputs

| Field | Value |
|---|---|
| Requirement ID | FR-007 |
| Type | functional |
| Source Section | BRS FR-007 |

#### Requirement Text

Scoring returns numeric score and recommendation. (source FR-007)

### FR-008 — Scoring inputs

| Field | Value |
|---|---|
| Requirement ID | FR-008 |
| Type | functional |
| Source Section | BRS FR-008 |

#### Requirement Text

Model uses applicant data and credit bureau inputs. (source FR-008)

### FR-009 — Experian integration

| Field | Value |
|---|---|
| Requirement ID | FR-009 |
| Type | integration |
| Source Section | BRS FR-009 |

#### Requirement Text

Integrate with Experian API for credit reports. (source FR-009)

### FR-010 — Auto-approve routing

| Field | Value |
|---|---|
| Requirement ID | FR-010 |
| Type | functional |
| Source Section | BRS FR-010 |

#### Requirement Text

Auto-approve routing for eligible low-value loans. (source FR-010)

### FR-011 — Auto-decline handling

| Field | Value |
|---|---|
| Requirement ID | FR-011 |
| Type | functional |
| Source Section | BRS FR-011 |

#### Requirement Text

Handle auto-decline notifications and cooling-off. (source FR-011)

### FR-012 — AML screening

| Field | Value |
|---|---|
| Requirement ID | FR-012 |
| Type | functional |
| Source Section | BRS FR-012 |

#### Requirement Text

Perform AML screening before offer generation. (source FR-012)

### FR-013 — KYC verification

| Field | Value |
|---|---|
| Requirement ID | FR-013 |
| Type | functional |
| Source Section | BRS FR-013 |

#### Requirement Text

Perform KYC via HMRC identity API. (source FR-013)

### FR-014 — AML failure handling

| Field | Value |
|---|---|
| Requirement ID | FR-014 |
| Type | functional |
| Source Section | BRS FR-014 |

#### Requirement Text

Flag applications as COMPLIANCE_HOLD on AML/KYC failure. (source FR-014)

### FR-015 — Underwriter queue presentation

| Field | Value |
|---|---|
| Requirement ID | FR-015 |
| Type | functional |
| Source Section | BRS FR-015 |

#### Requirement Text

Present refer/over-limit applications to underwriter queue. (source FR-015)

### FR-016 — Underwriter dashboard contents

| Field | Value |
|---|---|
| Requirement ID | FR-016 |
| Type | functional |
| Source Section | BRS FR-016 |

#### Requirement Text

Dashboard shows applicant summary and AI recommendation. (source FR-016)

### FR-017 — Underwriter actions

| Field | Value |
|---|---|
| Requirement ID | FR-017 |
| Type | functional |
| Source Section | BRS FR-017 |

#### Requirement Text

Underwriter may approve, decline, or request information. (source FR-017)

### FR-018 — Underwriter action immutability

| Field | Value |
|---|---|
| Requirement ID | FR-018 |
| Type | functional |
| Source Section | BRS FR-018 |

#### Requirement Text

Record underwriter actions immutably in audit store. (source FR-018)

### FR-019 — Underwriter escalation

| Field | Value |
|---|---|
| Requirement ID | FR-019 |
| Type | operational |
| Source Section | BRS FR-019 |

#### Requirement Text

Escalate unactioned queue items after threshold. (source FR-019)

### FR-020 — Offer generation

| Field | Value |
|---|---|
| Requirement ID | FR-020 |
| Type | functional |
| Source Section | BRS FR-020 |

#### Requirement Text

Generate loan offer document for approved applications. (source FR-020)

### FR-021 — Offer presentation

| Field | Value |
|---|---|
| Requirement ID | FR-021 |
| Type | functional |
| Source Section | BRS FR-021 |

#### Requirement Text

Present offer via portal and email; validity period enforced. (source FR-021)

### FR-022 — E-signature acceptance

| Field | Value |
|---|---|
| Requirement ID | FR-022 |
| Type | integration |
| Source Section | BRS FR-022 |

#### Requirement Text

Allow digital acceptance via DocuSign with audit metadata. (source FR-022)

### FR-023 — Cooling-off period

| Field | Value |
|---|---|
| Requirement ID | FR-023 |
| Type | functional |
| Source Section | BRS FR-023 |

#### Requirement Text

Enforce 14-day cooling-off with reminders and withdrawal handling. (source FR-023)

### FR-024 — Disbursement trigger

| Field | Value |
|---|---|
| Requirement ID | FR-024 |
| Type | functional |
| Source Section | BRS FR-024 |

#### Requirement Text

Trigger disbursement to T24 upon acceptance and cooling-off expiry. (source FR-024)

### FR-025 — Disbursement content

| Field | Value |
|---|---|
| Requirement ID | FR-025 |
| Type | functional |
| Source Section | BRS FR-025 |

#### Requirement Text

Include account details and reference in disbursement instruction. (source FR-025)

### FR-026 — Disbursement confirmation

| Field | Value |
|---|---|
| Requirement ID | FR-026 |
| Type | functional |
| Source Section | BRS FR-026 |

#### Requirement Text

Handle disbursement confirmation updates and retries. (source FR-026)

### FR-027 — Disbursement notification

| Field | Value |
|---|---|
| Requirement ID | FR-027 |
| Type | functional |
| Source Section | BRS FR-027 |

#### Requirement Text

Notify applicant of disbursement via email and portal. (source FR-027)

### FR-028 — Immutable audit log

| Field | Value |
|---|---|
| Requirement ID | FR-028 |
| Type | security |
| Source Section | BRS FR-028 |

#### Requirement Text

Maintain append-only audit records for all state transitions. (source FR-028)

### FR-029 — Admin dashboard metrics

| Field | Value |
|---|---|
| Requirement ID | FR-029 |
| Type | operational |
| Source Section | BRS FR-029 |

#### Requirement Text

Provide admin metrics and dashboards refreshed regularly. (source FR-029)

### FR-030 — Observability events

| Field | Value |
|---|---|
| Requirement ID | FR-030 |
| Type | operational |
| Source Section | BRS FR-030 |

#### Requirement Text

Emit structured events for key lifecycle milestones. (source FR-030)
