# Atomic Requirements

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I001-GIO |
| Created at | 2026-07-02 |
| Created by | product-owner |
| Status | Draft |

---

## Summary

| Metric | Value |
|---|---|
| Total requirements | 49 |
| Business objectives | 5 |
| Functional | 30 |
| Non-functional | 7 |
| Constraints | 7 |
| Blocking questions | 0 |

---

## Source Inventory

| Source ID | Type | Title / Summary | Preserved In |
|---|---|---|---|
| OBJ-001 | Objective | Reduce average decision time to under 30 minutes for ≥70% of applications | OBJ-001 |
| OBJ-002 | Objective | Improve underwriter consistency — variance reduced ≥50% | OBJ-002 |
| OBJ-003 | Objective | 100% of decisions have immutable audit trail within 24h of go-live | OBJ-003 |
| OBJ-004 | Objective | Zero regulatory findings in first post-launch compliance audit | OBJ-004 |
| OBJ-005 | Objective | ≥60% of approved loans disbursed without human intervention | OBJ-005 |
| FR-001 | Functional | Online loan application submission with required fields | FR-001 |
| FR-002 | Functional | Mandatory field validation before submission | FR-002 |
| FR-003 | Functional | Unique ARN assignment on submission | FR-003 |
| FR-004 | Functional | Email confirmation within 2 minutes of submission | FR-004 |
| FR-005 | Functional | Application status retrieval by ARN + date of birth | FR-005 |
| FR-006 | Functional | AI pre-screening triggered within 60 seconds of submission | FR-006 |
| FR-007 | Functional | AI scoring produces risk score (0–1000) and recommendation | FR-007 |
| FR-008 | Functional | AI scoring inputs: applicant data, credit bureau, ratios, employment, credit history | FR-008 |
| FR-009 | Functional | Experian CreditExpert API integration; fallback to REFER_TO_UNDERWRITER | FR-009 |
| FR-010 | Functional | AUTO_APPROVE ≤£10,000 proceeds to offer without underwriter review (pending AML/KYC) | FR-010 |
| FR-011 | Functional | AUTO_DECLINE notification within 5 minutes; 30-day cooling-off enforced | FR-011 |
| FR-012 | Functional | AML screening against HM Treasury sanctions and PEP database before any offer | FR-012 |
| FR-013 | Functional | KYC identity verification via HMRC identity API | FR-013 |
| FR-014 | Functional | COMPLIANCE_HOLD flag for failed AML/KYC; no offer generated | FR-014 |
| FR-015 | Functional | REFER_TO_UNDERWRITER and AUTO_APPROVE >£10,000 routed to underwriter queue within 2 minutes | FR-015 |
| FR-016 | Functional | Underwriter dashboard displays full application summary | FR-016 |
| FR-017 | Functional | Underwriter can approve, decline, or request additional information | FR-017 |
| FR-018 | Functional | Immutable record of every underwriter action | FR-018 |
| FR-019 | Functional | Escalation notification to team lead after 4 business hours without action | FR-019 |
| FR-020 | Functional | Loan offer document generated for every approved application | FR-020 |
| FR-021 | Functional | Loan offer presented via portal and email; valid for 14 days | FR-021 |
| FR-022 | Functional | Digital acceptance via DocuSign e-signature; acceptance logged | FR-022 |
| FR-023 | Functional | 14-day cooling-off period with reminders at day 7 and day 13 | FR-023 |
| FR-024 | Functional | Disbursement instruction to Temenos T24 after acceptance and cooling-off | FR-024 |
| FR-025 | Functional | Disbursement instruction fields: account number, sort code, amount, reference, value date | FR-025 |
| FR-026 | Functional | Disbursement confirmation received; retry and ops alert on failure | FR-026 |
| FR-027 | Functional | Applicant email and portal notification of disbursement with value date | FR-027 |
| FR-028 | Functional | Immutable audit log for every application state transition | FR-028 |
| FR-029 | Functional | Admin dashboard metrics refreshed every 5 minutes | FR-029 |
| FR-030 | Functional | Structured observability events for key lifecycle milestones | FR-030 |
| NFR-001 | Non-functional | Application intake form loads within 2 seconds | NFR-001 |
| NFR-002 | Non-functional | AI scoring pipeline completes end-to-end within 90 seconds | NFR-002 |
| NFR-003 | Non-functional | System supports 500 concurrent application submissions | NFR-003 |
| NFR-004 | Non-functional | All PII encrypted at rest (AES-256) and in transit (TLS 1.3) | NFR-004 |
| NFR-005 | Non-functional | Audit log is write-once and tamper-evident | NFR-005 |
| NFR-006 | Non-functional | 99.9% uptime during business hours (08:00–20:00 GMT) | NFR-006 |
| NFR-007 | Non-functional | All external API integrations implement circuit breakers with fallback behaviour | NFR-007 |
| C-001 | Constraint | Must comply with FCA Consumer Duty regulations | C-001 |
| C-002 | Constraint | Must comply with UK GDPR; data residency UK only | C-002 |
| C-003 | Constraint | Must integrate with Temenos T24 via internal payment gateway API (REST) | C-003 |
| C-004 | Constraint | Must use Experian CreditExpert API (existing enterprise contract) | C-004 |
| C-005 | Constraint | AI model decisions must be explainable; black-box models are not permitted | C-005 |
| C-006 | Constraint | All data must remain within UK data centres | C-006 |
| C-007 | Constraint | E-signature must use DocuSign (existing enterprise contract) | C-007 |

---

## Requirement Catalogue

### OBJ-001 — Reduce decision time

**Source:** BRS Business Objectives | **Actor:** System / Applicant | **Deps:** FR-006, FR-007, FR-010

THE SYSTEM SHALL deliver a loan decision within 30 minutes for at least 70% of submitted personal loan applications, measured across all completed decisions.

---

### OBJ-002 — Improve underwriter consistency

**Source:** BRS Business Objectives | **Actor:** Underwriter | **Deps:** FR-016, FR-017, FR-018

THE SYSTEM SHALL reduce the variance in approval rate across individual underwriters by at least 50% compared to the pre-launch baseline, measured over rolling monthly cohorts.

---

### OBJ-003 — Full regulatory audit trail

**Source:** BRS Business Objectives | **Actor:** System | **Deps:** FR-028

THE SYSTEM SHALL produce an immutable audit trail for 100% of loan decisions within 24 hours of the platform going live.

---

### OBJ-004 — Regulatory compliance at all stages

**Source:** BRS Business Objectives | **Actor:** System / Compliance Team | **Deps:** FR-012, FR-013, FR-014, C-001, C-002

THE SYSTEM SHALL satisfy all AML, KYC, and GDPR requirements at every stage of the loan lifecycle such that the first post-launch compliance audit produces zero regulatory findings.

---

### OBJ-005 — Digital end-to-end disbursement

**Source:** BRS Business Objectives | **Actor:** System | **Deps:** FR-010, FR-024, FR-025, FR-026

THE SYSTEM SHALL disburse at least 60% of approved loans without any human intervention in the loan processing workflow.

---

### FR-001 — Online loan application submission

**Source:** BRS Epic 1 — Loan Application Intake | **Actor:** Applicant | **Deps:** None

WHEN an applicant submits a personal loan application online,
THE SYSTEM SHALL collect and store: full name, date of birth, national insurance number, employment status, annual income, loan amount requested (£1,000–£50,000), loan purpose, and repayment term (12–84 months).

---

### FR-002 — Mandatory field validation

**Source:** BRS Epic 1 | **Actor:** Applicant | **Deps:** FR-001

WHEN an applicant attempts to submit an application with one or more mandatory fields missing or invalid,
THE SYSTEM SHALL display inline validation errors identifying each invalid field and SHALL NOT submit the application.

---

### FR-003 — ARN assignment

**Source:** BRS Epic 1 | **Actor:** System | **Deps:** FR-001

WHEN an applicant successfully submits a loan application,
THE SYSTEM SHALL assign a unique Application Reference Number (ARN) to that application and display the ARN to the applicant immediately after submission.

---

### FR-004 — Submission email confirmation

**Source:** BRS Epic 1 | **Actor:** System | **Deps:** FR-003

WHEN a loan application is successfully submitted,
THE SYSTEM SHALL send an email confirmation to the applicant within 2 minutes containing the ARN and an estimated decision timeline.

---

### FR-005 — Application status retrieval

**Source:** BRS Epic 1 | **Actor:** Applicant | **Deps:** FR-003

WHEN an applicant provides a valid ARN and date of birth,
THE SYSTEM SHALL return the current status of the corresponding loan application without requiring account registration.

IF the ARN and date of birth combination does not match any application,
THEN THE SYSTEM SHALL return an error indicating no matching application was found.

---

### FR-006 — AI pre-screening trigger

**Source:** BRS Epic 2 — AI Pre-Screening and Risk Scoring | **Actor:** System | **Deps:** FR-001, FR-003

WHEN a loan application is submitted,
THE SYSTEM SHALL automatically trigger an AI pre-screening assessment for that application within 60 seconds of submission.

---

### FR-007 — AI risk score and recommendation

**Source:** BRS Epic 2 | **Actor:** AI Scoring Service | **Deps:** FR-006, FR-008, FR-009

WHEN the AI pre-screening assessment completes,
THE SYSTEM SHALL produce a risk score between 0 and 1000 and a recommendation of exactly one of: `AUTO_APPROVE`, `REFER_TO_UNDERWRITER`, or `AUTO_DECLINE`.

---

### FR-008 — AI scoring inputs

**Source:** BRS Epic 2 | **Actor:** AI Scoring Service | **Deps:** FR-001, FR-009

WHEN computing the AI risk score,
THE SYSTEM SHALL use the following inputs: applicant-provided data (FR-001), credit bureau data retrieved from Experian (FR-009), debt-to-income ratio, loan-to-income ratio, employment stability, and credit history length.

---

### FR-009 — Experian CreditExpert integration

**Source:** BRS Epic 2 | **Actor:** System / Experian API | **Deps:** FR-001, C-004

WHEN an application enters the AI scoring pipeline,
THE SYSTEM SHALL retrieve a credit report for the applicant from the Experian CreditExpert API within 30 seconds.

IF the Experian CreditExpert API is unavailable or does not respond within 30 seconds,
THEN THE SYSTEM SHALL automatically route the application to `REFER_TO_UNDERWRITER` and SHALL NOT block or fail the application.

---

### FR-010 — Auto-approve straight-through path

**Source:** BRS Epic 2 | **Actor:** System | **Deps:** FR-007, FR-012, FR-013

WHEN an application receives an AI recommendation of `AUTO_APPROVE` and the requested loan amount is £10,000 or less,
THE SYSTEM SHALL route the application directly to offer generation (FR-020) without underwriter review, provided AML screening (FR-012) and KYC verification (FR-013) have both cleared.

WHILE an AML or KYC check is pending or has failed for an `AUTO_APPROVE` application,
THE SYSTEM SHALL NOT route the application to offer generation.

---

### FR-011 — Auto-decline notification and cooling-off

**Source:** BRS Epic 2 | **Actor:** System | **Deps:** FR-007

WHEN an application receives an AI recommendation of `AUTO_DECLINE`,
THE SYSTEM SHALL notify the applicant within 5 minutes with a decline reason category, without disclosing the risk score or detailed scoring rationale.

WHEN an applicant who was previously declined attempts to reapply,
THE SYSTEM SHALL enforce a 30-day cooling-off period from the date of the most recent decline and SHALL reject reapplication attempts within that period.

---

### FR-012 — AML screening

**Source:** BRS Epic 3 — AML / KYC Compliance | **Actor:** Compliance Service | **Deps:** FR-001, C-001

WHEN processing a loan application prior to generating any offer,
THE SYSTEM SHALL perform AML screening of the applicant against the HM Treasury sanctions list and PEP (Politically Exposed Persons) database, completing the screening within 60 seconds.

> **Ambiguities:** OQ-004 resolved: AML database is HM Treasury only (no Dow Jones Watchlist).

---

### FR-013 — KYC identity verification

**Source:** BRS Epic 3 | **Actor:** Compliance Service | **Deps:** FR-001, C-002

WHEN processing a loan application,
THE SYSTEM SHALL perform KYC identity verification by cross-referencing the applicant's national insurance number, full name, and date of birth against the HMRC identity verification API.

IF the HMRC identity verification API is unavailable,
THEN THE SYSTEM SHALL route the application to a manual verification queue for human review, without blocking or auto-declining the application.

> **Ambiguities:** OQ-003 resolved: HMRC fallback is manual verification queue.

---

### FR-014 — COMPLIANCE_HOLD status

**Source:** BRS Epic 3 | **Actor:** System | **Deps:** FR-012, FR-013

WHEN an application fails AML screening or KYC verification,
THE SYSTEM SHALL set the application status to `COMPLIANCE_HOLD` and route it to the compliance team queue.

WHILE an application is in `COMPLIANCE_HOLD`,
THE SYSTEM SHALL NOT generate a loan offer and SHALL notify the applicant that their application is under review.

---

### FR-015 — Underwriter queue routing

**Source:** BRS Epic 4 — Underwriter Review Workflow | **Actor:** System | **Deps:** FR-007, FR-010, FR-012, FR-013

WHEN an application receives a `REFER_TO_UNDERWRITER` AI recommendation,
THE SYSTEM SHALL present the application to the underwriter queue within 2 minutes of AI scoring completion.

WHEN an application receives an `AUTO_APPROVE` recommendation and the requested loan amount exceeds £10,000,
THE SYSTEM SHALL present the application to the underwriter queue within 2 minutes of AI scoring completion.

---

### FR-016 — Underwriter dashboard application display

**Source:** BRS Epic 4 | **Actor:** Underwriter | **Deps:** FR-015

WHEN an underwriter views an application in the queue,
THE SYSTEM SHALL display: applicant summary, AI risk score and recommendation, credit bureau summary, debt-to-income ratio, loan-to-income ratio, employment verification status, and AML/KYC status.

---

### FR-017 — Underwriter decision actions

**Source:** BRS Epic 4 | **Actor:** Underwriter | **Deps:** FR-016

WHILE reviewing an application in the underwriter queue,
THE SYSTEM SHALL allow the underwriter to perform exactly one of: approve the application (with optional conditions), decline the application (with mandatory written reason), or request additional information from the applicant.

---

### FR-018 — Immutable underwriter action record

**Source:** BRS Epic 4 | **Actor:** System | **Deps:** FR-017

WHEN an underwriter performs any action on an application,
THE SYSTEM SHALL create an immutable record containing: underwriter ID, timestamp, action taken, reason or conditions applied, and the AI recommendation that was presented at time of review.

---

### FR-019 — Escalation notification for unactioned applications

**Source:** BRS Epic 4 | **Actor:** System | **Deps:** FR-015

WHEN an application remains unactioned in the underwriter queue for 4 business hours,
THE SYSTEM SHALL send an escalation notification to the underwriter team lead.

---

### FR-020 — Loan offer document generation

**Source:** BRS Epic 5 — Loan Offer and Digital Acceptance | **Actor:** System | **Deps:** FR-010, FR-017

WHEN a loan application is approved (either via auto-approve or underwriter approval),
THE SYSTEM SHALL generate a loan offer document containing: approved loan amount, interest rate (APR), monthly repayment amount, total repayable amount, repayment term, and key terms and conditions.

---

### FR-021 — Loan offer delivery and validity

**Source:** BRS Epic 5 | **Actor:** System | **Deps:** FR-020

WHEN a loan offer is generated,
THE SYSTEM SHALL present the offer to the applicant via the self-service portal and send the offer via email.

THE SYSTEM SHALL enforce a 14-day validity period for every generated loan offer, after which the offer expires automatically.

---

### FR-022 — Digital offer acceptance via e-signature

**Source:** BRS Epic 5 | **Actor:** Applicant | **Deps:** FR-021, C-007

WHEN an applicant accepts a loan offer,
THE SYSTEM SHALL obtain the acceptance via DocuSign e-signature integration and record the acceptance timestamp and the applicant's IP address.

---

### FR-023 — 14-day cooling-off period

**Source:** BRS Epic 5 | **Actor:** System | **Deps:** FR-022

WHEN an applicant digitally accepts a loan offer,
THE SYSTEM SHALL start a 14-day cooling-off period during which the applicant may withdraw from the agreement without penalty.

WHEN the cooling-off period day count reaches 7,
THE SYSTEM SHALL send a reminder notification to the applicant.

WHEN the cooling-off period day count reaches 13,
THE SYSTEM SHALL send a final reminder notification to the applicant.

> **Ambiguities:** OQ-002 resolved: a separate legal sign-off UI step for the cooling-off waiver is not required.

---

### FR-024 — Disbursement instruction to T24

**Source:** BRS Epic 6 — Disbursement | **Actor:** System | **Deps:** FR-022, FR-023, C-003

WHEN the 14-day cooling-off period expires (or the applicant validly waives it),
THE SYSTEM SHALL trigger a disbursement instruction to the Temenos T24 core banking system via the internal payment gateway API.

---

### FR-025 — Disbursement instruction fields

**Source:** BRS Epic 6 | **Actor:** System | **Deps:** FR-024

WHEN generating a disbursement instruction,
THE SYSTEM SHALL include in the instruction: applicant account number, sort code, loan amount, reference number, and value date.

---

### FR-026 — Disbursement confirmation handling

**Source:** BRS Epic 6 | **Actor:** System | **Deps:** FR-024, FR-025

WHEN a disbursement confirmation is received from the T24 core banking system,
THE SYSTEM SHALL update the application status to `DISBURSED`.

IF disbursement confirmation is not received within 2 minutes of the disbursement instruction being sent,
THEN THE SYSTEM SHALL retry the disbursement instruction once and, if confirmation is still not received, SHALL alert the operations team.

---

### FR-027 — Disbursement applicant notification

**Source:** BRS Epic 6 | **Actor:** System | **Deps:** FR-026

WHEN an application status is updated to `DISBURSED`,
THE SYSTEM SHALL send the applicant an email notification and a portal notification confirming disbursement and stating the expected value date.

---

### FR-028 — Immutable audit log for state transitions

**Source:** BRS Epic 7 — Observability, Audit, and Administration | **Actor:** System | **Deps:** All FRs that trigger state changes

WHEN any application state transition occurs,
THE SYSTEM SHALL append an immutable record to the audit log containing: previous state, new state, triggering actor (applicant, AI model, underwriter ID, or system), timestamp, and a relevant data snapshot.

THE SYSTEM SHALL ensure audit log records cannot be updated or deleted under any code path.

---

### FR-029 — Admin dashboard metrics

**Source:** BRS Epic 7 | **Actor:** Admin | **Deps:** FR-028

THE SYSTEM SHALL provide an admin dashboard displaying: application volume by status, average decision time, AI recommendation distribution, approval and decline rates by underwriter, and AML/KYC hold rates.

THE SYSTEM SHALL refresh all admin dashboard data at intervals not exceeding 5 minutes.

---

### FR-030 — Structured observability events

**Source:** BRS Epic 7 | **Actor:** System | **Deps:** FR-003, FR-006, FR-007, FR-012, FR-013, FR-017, FR-022, FR-024

WHEN any of the following milestones occurs — application submission, AI scoring completion, AML/KYC result, underwriter decision, offer acceptance, or disbursement — THE SYSTEM SHALL emit a structured observability event containing: ARN, timestamp, milestone status, and triggering actor.

---

### NFR-001 — Application form load time

**Source:** BRS Non-Functional Requirements | **Actor:** Applicant | **Deps:** None

THE SYSTEM SHALL load the loan application intake form within 2 seconds when accessed on a standard broadband connection under normal operating conditions.

---

### NFR-002 — AI scoring pipeline latency

**Source:** BRS Non-Functional Requirements | **Actor:** System | **Deps:** FR-006, FR-007, FR-008, FR-009

THE SYSTEM SHALL complete the end-to-end AI scoring pipeline within 90 seconds under normal load conditions.

---

### NFR-003 — Concurrent submission capacity

**Source:** BRS Non-Functional Requirements | **Actor:** System | **Deps:** FR-001

THE SYSTEM SHALL support a minimum of 500 concurrent loan application submissions without degradation below defined SLAs.

---

### NFR-004 — PII encryption

**Source:** BRS Non-Functional Requirements | **Actor:** System | **Deps:** C-002, C-006

THE SYSTEM SHALL encrypt all personally identifiable information at rest using AES-256 and in transit using TLS 1.3.

---

### NFR-005 — Tamper-evident audit log

**Source:** BRS Non-Functional Requirements | **Actor:** System | **Deps:** FR-028

THE SYSTEM SHALL implement the audit log as a write-once, tamper-evident store — no update or delete operations shall be possible on any audit record.

---

### NFR-006 — Business hours uptime

**Source:** BRS Non-Functional Requirements | **Actor:** System | **Deps:** None

THE SYSTEM SHALL achieve 99.9% uptime during business hours (08:00–20:00 GMT), measured on a monthly basis.

---

### NFR-007 — Circuit breakers for external APIs

**Source:** BRS Non-Functional Requirements | **Actor:** System | **Deps:** FR-009, FR-012, FR-013, FR-022, FR-024

THE SYSTEM SHALL implement circuit breakers with defined fallback behaviour for all external API integrations: Experian CreditExpert, HMRC identity verification, HM Treasury AML, DocuSign, and Temenos T24 payment gateway.

---

### C-001 — FCA Consumer Duty compliance

**Source:** BRS Constraints | **Actor:** System / All Teams | **Deps:** FR-007, FR-011, C-005

THE SYSTEM SHALL be designed and operated in full compliance with FCA Consumer Duty regulations at every stage of the loan lifecycle.

---

### C-002 — UK GDPR compliance and data residency

**Source:** BRS Constraints | **Actor:** System | **Deps:** NFR-004, C-006

THE SYSTEM SHALL comply with UK GDPR at every stage of data collection, processing, and storage, and all personal data shall be stored and processed exclusively within UK jurisdiction.

---

### C-003 — Temenos T24 integration constraint

**Source:** BRS Constraints | **Actor:** System / IT Architecture | **Deps:** FR-024, FR-025, FR-026

THE SYSTEM SHALL integrate with the existing Temenos T24 core banking system via the internal payment gateway REST API. The API contract is to be defined by this initiative.

> **Ambiguities:** OQ-005 resolved: the T24 API contract will be defined by this initiative.

---

### C-004 — Experian CreditExpert API constraint

**Source:** BRS Constraints | **Actor:** System | **Deps:** FR-009

THE SYSTEM SHALL use the existing Experian CreditExpert enterprise API contract for all credit bureau data retrieval. No alternative credit bureau integration is permitted.

---

### C-005 — Explainable AI requirement

**Source:** BRS Constraints | **Actor:** AI Scoring Service | **Deps:** FR-007, FR-008, C-001

THE SYSTEM SHALL use only explainable AI models for loan scoring decisions. Black-box models that cannot produce human-readable decision rationale are not permitted, in compliance with FCA requirements.

---

### C-006 — UK data centre residency

**Source:** BRS Constraints | **Actor:** System / Infrastructure | **Deps:** C-002, NFR-004

THE SYSTEM SHALL store and process all data exclusively within UK data centres. No data shall traverse, be processed by, or be stored in infrastructure outside the United Kingdom.

---

### C-007 — DocuSign e-signature constraint

**Source:** BRS Constraints | **Actor:** System | **Deps:** FR-022

THE SYSTEM SHALL use the existing DocuSign enterprise contract for all e-signature operations. No alternative e-signature provider is permitted.

---

## Source ID Mapping

| Source ID | Optional REQ Alias | Mapping Type | Notes |
|---|---|---|---|
| OBJ-001 | — | Context | Objective preserved as-is; no REQ alias needed |
| OBJ-002 | — | Context | Objective preserved as-is |
| OBJ-003 | — | Context | Objective preserved as-is |
| OBJ-004 | — | Context | Objective preserved as-is |
| OBJ-005 | — | Context | Objective preserved as-is |
| FR-001 | — | Direct | Alias omitted; FR-001 is the primary ID |
| FR-002 | — | Direct | Alias omitted |
| FR-003 | — | Direct | Alias omitted |
| FR-004 | — | Direct | Alias omitted |
| FR-005 | — | Direct | Alias omitted |
| FR-006 | — | Direct | Alias omitted |
| FR-007 | — | Direct | Alias omitted |
| FR-008 | — | Direct | Alias omitted |
| FR-009 | — | Direct | Alias omitted |
| FR-010 | — | Direct | Alias omitted |
| FR-011 | — | Direct | Alias omitted |
| FR-012 | — | Direct | Alias omitted |
| FR-013 | — | Direct | Alias omitted |
| FR-014 | — | Direct | Alias omitted |
| FR-015 | — | Direct | Alias omitted |
| FR-016 | — | Direct | Alias omitted |
| FR-017 | — | Direct | Alias omitted |
| FR-018 | — | Direct | Alias omitted |
| FR-019 | — | Direct | Alias omitted |
| FR-020 | — | Direct | Alias omitted |
| FR-021 | — | Direct | Alias omitted |
| FR-022 | — | Direct | Alias omitted |
| FR-023 | — | Direct | Alias omitted |
| FR-024 | — | Direct | Alias omitted |
| FR-025 | — | Direct | Alias omitted |
| FR-026 | — | Direct | Alias omitted |
| FR-027 | — | Direct | Alias omitted |
| FR-028 | — | Direct | Alias omitted |
| FR-029 | — | Direct | Alias omitted |
| FR-030 | — | Direct | Alias omitted |
| NFR-001 | — | Direct | Alias omitted |
| NFR-002 | — | Direct | Alias omitted |
| NFR-003 | — | Direct | Alias omitted |
| NFR-004 | — | Direct | Alias omitted |
| NFR-005 | — | Direct | Alias omitted |
| NFR-006 | — | Direct | Alias omitted |
| NFR-007 | — | Direct | Alias omitted |
| C-001 | — | Constraint | FCA Consumer Duty — first-class constraint |
| C-002 | — | Constraint | UK GDPR + data residency |
| C-003 | — | Constraint | T24 integration constraint |
| C-004 | — | Constraint | Experian API constraint |
| C-005 | — | Constraint | Explainable AI (FCA) |
| C-006 | — | Constraint | UK data centre residency |
| C-007 | — | Constraint | DocuSign constraint |

---

## Open Questions

| ID | Question | Source ID | Blocking? | Owner | Status |
|---|---|---|---|---|---|
| OQ-001 | What is the approved AI model vendor / approach for risk scoring? | FR-007, FR-008 | No | Head of AI | Resolved — Azure Foundry |
| OQ-002 | Does the cooling-off period waiver require a separate legal sign-off flow? | FR-023 | No | Legal | Resolved — no separate legal sign-off UI step required |
| OQ-003 | What is the fallback for HMRC KYC API when unavailable? | FR-013 | No | Compliance | Resolved — manual verification queue |
| OQ-004 | What are the exact AML database providers? | FR-012 | No | Compliance | Resolved — HM Treasury only |
| OQ-005 | Is the T24 payment gateway contract already defined? | FR-024, C-003 | No | IT Architecture | Resolved — contract to be defined by this initiative |

---

## Assumptions

| ID | Assumption | Source ID | Risk if Wrong | Validation Approach | Status |
|---|---|---|---|---|---|
| ASM-001 | Azure Foundry is already procured or will be procured within delivery timeline | FR-007, FR-008 | AI Scoring Service design blocked | Confirm with Head of AI before AI Scoring Service stories begin | Open |
| ASM-002 | Experian CreditExpert API contract is already active and authentication credentials are available | FR-009, C-004 | Experian integration stories blocked | Confirm with IT Architecture in Sprint 0 | Open |
| ASM-003 | DocuSign enterprise contract is active and integration credentials are available | FR-022, C-007 | Offer acceptance flow blocked | Confirm with IT Architecture in Sprint 0 | Open |
| ASM-004 | T24 internal payment gateway team will participate in API contract definition | FR-024, C-003 | Disbursement stories blocked | Schedule API contract workshop with IT Architecture | Open |
| ASM-005 | HMRC identity verification API credentials are available for Compliance Service integration | FR-013 | KYC verification stories blocked | Confirm with Compliance team in Sprint 0 | Open |

---

## Traceability Notes

All 30 functional requirements (FR-001 through FR-030), 7 non-functional requirements (NFR-001 through NFR-007), 5 business objectives (OBJ-001 through OBJ-005), and 7 explicit constraint bullets (C-001 through C-007) from the BRS have been extracted and preserved as first-class entries. No REQ aliases are used; all source IDs are the primary catalogue identifiers. All 5 open questions from the BRS are captured with resolved status per the answers provided in the BRS open questions table. No requirements have been excluded, skipped, or silently lost.

## Loss Check

| Check | Result | Notes |
|---|---|---|
| Every `FR-` from BRS preserved | Yes | FR-001 through FR-030, all 30 entries |
| Every `NFR-` from BRS preserved | Yes | NFR-001 through NFR-007, all 7 entries |
| Every `OBJ-` from BRS preserved | Yes | OBJ-001 through OBJ-005, all 5 entries |
| Every explicit constraint preserved | Yes | C-001 through C-007, all 7 constraint bullets |
| Every optional `REQ-` alias has source mapping | Yes | No REQ aliases used; N/A |
| Any intentionally excluded item explained | Yes | No items excluded |

---
*Set Status: Accepted only after human review. Never self-accept.*
