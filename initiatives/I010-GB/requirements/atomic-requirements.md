# Atomic Requirements

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I010-GB |
| Created at | 2026-06-28 |
| Created by | product-owner |
| Status | Draft |

---

## Summary

| Metric | Value |
|---|---|
| Total requirements | 42 |
| Business objectives | 5 |
| Functional | 30 |
| Non-functional | 7 |
| Data | 0 |
| Integration | 4 |
| Security | 4 |
| Operational | 1 |
| Reporting | 1 |
| Constraints | 4 |
| Blocking questions | 5 |

---

## Source Inventory

| Source ID | Type | Title / Summary | Preserved In |
|---|---|---|---|
| OBJ-001 | Objective | Reduce decision time to ≤30 minutes for straight-through cases | OBJ-001 |
| OBJ-002 | Objective | Improve underwriter consistency | OBJ-002 |
| OBJ-003 | Objective | Achieve full regulatory audit trail | OBJ-003 |
| OBJ-004 | Objective | Comply with AML, KYC, GDPR | OBJ-004 |
| OBJ-005 | Objective | Enable digital end-to-end for eligible applicants | OBJ-005 |
| FR-001 | Functional | Loan application submission fields and flow | FR-001 |
| FR-002 | Functional | Inline validation before submission | FR-002 |
| FR-003 | Functional | Assign ARN on submission | FR-003 |
| FR-004 | Functional | Email confirmation within 2 minutes | FR-004 |
| FR-005 | Functional | Retrieve status by ARN and DOB | FR-005 |
| FR-006 | Functional | Trigger AI pre-screening within 60s | FR-006 |
| FR-007 | Functional | Produce risk score and recommendation | FR-007 |
| FR-008 | Functional | Model inputs for scoring | FR-008 |
| FR-009 | Functional | Integrate with Experian CreditExpert | FR-009 |
| FR-010 | Functional | AUTO_APPROVE flow for ≤£10,000 | FR-010 |
| FR-011 | Functional | AUTO_DECLINE notification and cooling-off | FR-011 |
| FR-012 | Functional | AML screening before offer generation | FR-012 |
| FR-013 | Functional | KYC identity verification via HMRC | FR-013 |
| FR-014 | Functional | COMPLIANCE_HOLD routing | FR-014 |
| FR-015 | Functional | Underwriter queue rules | FR-015 |
| FR-016 | Functional | Underwriter dashboard contents | FR-016 |
| FR-017 | Functional | Underwriter actions (approve/decline/request info) | FR-017 |
| FR-018 | Functional | Immutable underwriter action record | FR-018 |
| FR-019 | Functional | Escalation after 4 business hours | FR-019 |
| FR-020 | Functional | Loan offer content requirements | FR-020 |
| FR-021 | Functional | Present offer via portal and email | FR-021 |
| FR-022 | Functional | Digital acceptance via DocuSign | FR-022 |
| FR-023 | Functional | 14-day cooling-off enforcement | FR-023 |
| FR-024 | Functional | Trigger disbursement to T24 after acceptance | FR-024 |
| FR-025 | Functional | Disbursement instruction fields | FR-025 |
| FR-026 | Functional | Disbursement confirmation handling and retries | FR-026 |
| FR-027 | Functional | Applicant notification on disbursement | FR-027 |
| FR-028 | Functional | Immutable audit log of state transitions | FR-028 |
| FR-029 | Functional | Admin dashboard metrics and refresh | FR-029 |
| FR-030 | Functional | Emit structured observability events | FR-030 |
| NFR-001 | Non-functional | Intake form load time ≤2s | NFR-001 |
| NFR-002 | Non-functional | AI scoring pipeline ≤90s under normal load | NFR-002 |
| NFR-003 | Non-functional | Support 500 concurrent submissions | NFR-003 |
| NFR-004 | Non-functional | Encrypt PII at rest/in transit | NFR-004 |
| NFR-005 | Non-functional | Audit log write-once, tamper-evident | NFR-005 |
| NFR-006 | Non-functional | 99.9% uptime during business hours | NFR-006 |
| NFR-007 | Non-functional | API integrations implement circuit breakers | NFR-007 |
| C-001 | Constraint | Comply with FCA Consumer Duty | C-001 |
| C-002 | Constraint | UK GDPR and UK-only data residency | C-002 |
| C-003 | Constraint | Integrate with Temenos T24 (internal gateway) | C-003 |
| C-004 | Constraint | Use Experian CreditExpert and DocuSign per contracts | C-004 |

---

## Requirement Catalogue

### OBJ-001 — Reduce average decision time to ≤30 minutes for straight-through cases

**Source:** Business objectives | **Actor:** Product Owner | **Deps:** None

WHEN the initiative is in operation,
THE SYSTEM SHALL enable ≥70% of eligible applications to reach a decision in ≤30 minutes.

> **Ambiguities:** Eligibility criteria for "straight-through" cases must be defined in architecture inputs.

---

### OBJ-002 — Improve underwriter consistency

**Source:** Business objectives | **Actor:** Product Owner | **Deps:** None

WHEN measuring approval variance,
THE SYSTEM SHALL reduce variance in approval rates across underwriters by ≥50% compared to baseline.

---

### OBJ-003 — Achieve full regulatory audit trail

**Source:** Business objectives | **Actor:** Product Owner | **Deps:** FR-028

WHEN decisions occur,
THE SYSTEM SHALL record an immutable audit trail for every decision accessible within 24 hours.

---

### OBJ-004 — Comply with AML, KYC, and GDPR

**Source:** Business objectives | **Actor:** Product Owner | **Deps:** FR-012, FR-013, C-002

WHEN processing personal data,
THE SYSTEM SHALL comply with AML, KYC, and UK GDPR requirements and maintain evidence for audits.

---

### OBJ-005 — Enable digital end-to-end for eligible applicants

**Source:** Business objectives | **Actor:** Product Owner | **Deps:** FR-020, FR-022, FR-024

WHEN an applicant is eligible and accepts an offer,
THE SYSTEM SHALL allow end-to-end digital processing including e-signature and disbursement without human intervention.

---

### FR-001 — Loan application submission

**Source:** Epic 1 — Loan Application Intake | **Actor:** Applicant | **Deps:** None

WHEN an applicant submits an application,
THE SYSTEM SHALL accept and store applicant-provided fields: full name, date of birth, national insurance number, employment status, annual income, loan amount requested (£1,000–£50,000), loan purpose, and repayment term (12–84 months).

IF mandatory fields are missing,
THEN THE SYSTEM SHALL prevent submission and display inline validation errors (see FR-002).

---

### FR-002 — Inline validation before submission

**Source:** Epic 1 — Loan Application Intake | **Actor:** Applicant | **Deps:** FR-001

WHEN an applicant fills the form,
THE SYSTEM SHALL validate mandatory fields inline and prevent submission if any required field is incomplete.

---

### FR-003 — Assign Application Reference Number (ARN)

**Source:** Epic 1 — Loan Application Intake | **Actor:** System | **Deps:** FR-001

WHEN an application is submitted successfully,
THE SYSTEM SHALL assign a unique Application Reference Number (ARN) and display it to the applicant immediately.

---

### FR-004 — Email confirmation within 2 minutes

**Source:** Epic 1 — Loan Application Intake | **Actor:** System | **Deps:** FR-003

WHEN an application is submitted,
THE SYSTEM SHALL send an email confirmation containing the ARN and estimated decision timeline within 2 minutes of submission.

---

### FR-005 — Retrieve status by ARN and DOB

**Source:** Epic 1 — Loan Application Intake | **Actor:** Applicant | **Deps:** FR-003

WHEN an applicant provides ARN and date of birth,
THE SYSTEM SHALL return the current status of the application without requiring account registration.

---

### FR-006 — Trigger AI pre-screening within 60s

**Source:** Epic 2 — AI Pre-Screening | **Actor:** System | **Deps:** FR-001

WHEN an application is submitted,
THE SYSTEM SHALL automatically trigger an AI pre-screening assessment within 60 seconds.

---

### FR-007 — Produce risk score and recommendation

**Source:** Epic 2 — AI Pre-Screening | **Actor:** AI Scoring Service | **Deps:** FR-006, FR-008

WHEN pre-screening completes,
THE SYSTEM SHALL produce a risk score (0–1000) and a recommendation: `AUTO_APPROVE`, `REFER_TO_UNDERWRITER`, or `AUTO_DECLINE`.

---

### FR-008 — Model inputs for scoring

**Source:** Epic 2 — AI Pre-Screening | **Actor:** System | **Deps:** FR-006

WHEN preparing model input,
THE SYSTEM SHALL include applicant-provided data, credit bureau data, debt-to-income ratio, loan-to-income ratio, employment stability, and credit history length.

---

### FR-009 — Experian integration

**Source:** Epic 2 — AI Pre-Screening | **Actor:** Integration Service | **Deps:** FR-006, C-004

WHEN a credit report is required,
THE SYSTEM SHALL call Experian CreditExpert API and complete the integration within 30 seconds; IF Experian is unavailable, THEN route the application to `REFER_TO_UNDERWRITER`.

---

### FR-010 — AUTO_APPROVE flow for ≤£10,000

**Source:** Epic 2 — AI Pre-Screening | **Actor:** System | **Deps:** FR-007, FR-012

WHEN recommendation is `AUTO_APPROVE` AND loan amount ≤£10,000,
THE SYSTEM SHALL proceed to offer generation without underwriter review, subject to AML/KYC clearance.

---

### FR-011 — AUTO_DECLINE notification and cooling-off

**Source:** Epic 2 — AI Pre-Screening | **Actor:** System | **Deps:** FR-007

WHEN recommendation is `AUTO_DECLINE`,
THE SYSTEM SHALL notify the applicant within 5 minutes with a decline reason category and enforce a 30-day cooling-off period before reapplication.

---

### FR-012 — AML screening before offer generation

**Source:** Epic 3 — AML / KYC | **Actor:** Compliance Service | **Deps:** FR-009

WHEN an offer is about to be generated,
THE SYSTEM SHALL perform AML screening against HM Treasury sanctions list and PEP database and complete within 60 seconds.

IF AML screening fails, THEN THE SYSTEM SHALL flag the application as `COMPLIANCE_HOLD` and route to compliance team.

---

### FR-013 — KYC identity verification

**Source:** Epic 3 — AML / KYC | **Actor:** Identity Verification Service | **Deps:** FR-001

WHEN identity verification is required,
THE SYSTEM SHALL verify NI number, name, and date of birth via HMRC identity verification API.

IF verification fails, THEN THE SYSTEM SHALL flag `COMPLIANCE_HOLD` and notify applicant.

---

### FR-014 — COMPLIANCE_HOLD routing

**Source:** Epic 3 — AML / KYC | **Actor:** System | **Deps:** FR-012, FR-013

WHEN AML/KYC fails,
THE SYSTEM SHALL set application status to `COMPLIANCE_HOLD` and route to the compliance team; NO offer shall be generated for such applications.

---

### FR-015 — Underwriter queue rules

**Source:** Epic 4 — Underwriter Review | **Actor:** System | **Deps:** FR-007, FR-010

WHEN an application requires underwriter review,
THE SYSTEM SHALL place it in the underwriter queue within 2 minutes of AI scoring completion.

---

### FR-016 — Underwriter dashboard contents

**Source:** Epic 4 — Underwriter Review | **Actor:** System | **Deps:** FR-015

WHEN an underwriter views an application,
THE SYSTEM SHALL display applicant summary, AI risk score and recommendation, credit bureau summary, debt-to-income ratio, loan-to-income ratio, employment verification status, and AML/KYC status.

---

### FR-017 — Underwriter actions

**Source:** Epic 4 — Underwriter Review | **Actor:** Underwriter | **Deps:** FR-016

WHEN reviewing an application,
THE SYSTEM SHALL allow the underwriter to approve (with optional conditions), decline (with mandatory reason), or request additional information.

---

### FR-018 — Immutable underwriter action record

**Source:** Epic 4 — Underwriter Review | **Actor:** System | **Deps:** FR-017

WHEN an underwriter takes action,
THE SYSTEM SHALL record underwriter ID, timestamp, action taken, reason or conditions, and the AI recommendation immutably.

---

### FR-019 — Escalation after 4 business hours

**Source:** Epic 4 — Underwriter Review | **Actor:** System | **Deps:** FR-015

WHILE an application is unactioned in the underwriter queue for 4 business hours,
THE SYSTEM SHALL trigger an escalation notification to the team lead.

---

### FR-020 — Loan offer content

**Source:** Epic 5 — Loan Offer | **Actor:** System | **Deps:** FR-010, FR-012

WHEN generating an offer,
THE SYSTEM SHALL include approved loan amount, interest rate (APR), monthly repayment, total repayable, repayment term, and key terms and conditions.

---

### FR-021 — Present offer via portal and email

**Source:** Epic 5 — Loan Offer | **Actor:** System | **Deps:** FR-020

WHEN an offer is generated,
THE SYSTEM SHALL present it via the self-service portal and send it by email; the offer shall be valid for 14 days.

---

### FR-022 — Digital acceptance via DocuSign

**Source:** Epic 5 — Loan Offer | **Actor:** System | **Deps:** FR-021, C-004

WHEN an applicant accepts an offer,
THE SYSTEM SHALL record acceptance via DocuSign e-signature and log timestamp and IP address.

---

### FR-023 — 14-day cooling-off enforcement

**Source:** Epic 5 — Loan Offer | **Actor:** System | **Deps:** FR-022

WHEN an offer is accepted,
THE SYSTEM SHALL enforce a 14-day cooling-off period and send reminders at day 7 and day 13.

---

### FR-024 — Trigger disbursement to T24

**Source:** Epic 6 — Disbursement | **Actor:** System | **Deps:** FR-023, C-003

WHEN cooling-off expires or applicant waives it,
THE SYSTEM SHALL trigger a disbursement instruction to Temenos T24 via the internal payment gateway.

---

### FR-025 — Disbursement instruction fields

**Source:** Epic 6 — Disbursement | **Actor:** System | **Deps:** FR-024

WHEN sending disbursement instruction,
THE SYSTEM SHALL include applicant account number, sort code, loan amount, reference number, and value date.

---

### FR-026 — Disbursement confirmation handling and retries

**Source:** Epic 6 — Disbursement | **Actor:** System | **Deps:** FR-024

WHEN waiting for confirmation from the core banking system,
THE SYSTEM SHALL retry once if confirmation is not received within 2 minutes and then alert operations if still missing.

---

### FR-027 — Applicant notification on disbursement

**Source:** Epic 6 — Disbursement | **Actor:** System | **Deps:** FR-026

WHEN disbursement is confirmed,
THE SYSTEM SHALL notify the applicant via email and portal with expected value date.

---

### FR-028 — Immutable audit log of state transitions

**Source:** Epic 7 — Observability | **Actor:** System | **Deps:** OBJ-003

WHEN any state transition occurs for an application,
THE SYSTEM SHALL append an immutable audit entry including previous state, new state, triggering actor, timestamp, and relevant data snapshot.

---

### FR-029 — Admin dashboard metrics and refresh

**Source:** Epic 7 — Observability | **Actor:** System | **Deps:** FR-028

WHEN rendering admin dashboard,
THE SYSTEM SHALL provide application volume by status, average decision time, AI recommendation distribution, approval/decline rates by underwriter, and AML/KYC hold rates, refreshing data every 5 minutes.

---

### FR-030 — Emit structured observability events

**Source:** Epic 7 — Observability | **Actor:** System | **Deps:** FR-028

WHEN key events occur (submission, scoring, AML/KYC, underwriter decision, offer acceptance, disbursement),
THE SYSTEM SHALL emit structured observability events including ARN, timestamp, status, and actor.

---

### NFR-001 — Intake form load time

**Source:** Non-functional | **Actor:** System | **Deps:** FR-001

WHEN the intake page is requested,
THE SYSTEM SHALL render the form within 2 seconds on a standard broadband connection.

---

### NFR-002 — AI scoring pipeline latency

**Source:** Non-functional | **Actor:** System | **Deps:** FR-006

WHEN scoring is executed under normal load,
THE SYSTEM SHALL complete the AI scoring pipeline end-to-end within 90 seconds.

---

### NFR-003 — Concurrency support

**Source:** Non-functional | **Actor:** System | **Deps:** FR-001

WHEN under normal operational conditions,
THE SYSTEM SHALL support 500 concurrent application submissions.

---

### NFR-004 — PII encryption

**Source:** Non-functional | **Actor:** System | **Deps:** C-002

WHEN storing or transmitting PII,
THE SYSTEM SHALL encrypt data at rest using AES-256 and in transit using TLS 1.3.

---

### NFR-005 — Audit log durability

**Source:** Non-functional | **Actor:** System | **Deps:** FR-028

WHEN writing audit logs,
THE SYSTEM SHALL ensure write-once, tamper-evident storage for audit entries.

---

### NFR-006 — Uptime

**Source:** Non-functional | **Actor:** System | **Deps:** Operational planning

WHILE in production,
THE SYSTEM SHALL achieve 99.9% uptime during business hours (08:00–20:00 GMT).

---

### NFR-007 — Integration resilience

**Source:** Non-functional | **Actor:** System | **Deps:** FR-009, FR-012

WHEN interacting with external APIs (Experian, HMRC, DocuSign, T24),
THE SYSTEM SHALL implement circuit breakers with defined fallback behavior.

---

### C-001 — FCA Consumer Duty compliance

**Source:** Constraints | **Actor:** Organisation | **Deps:** Regulatory review

WHEN designing features,
THE SYSTEM SHALL comply with FCA Consumer Duty principles and record decisions for audit.

---

### C-002 — UK GDPR and data residency

**Source:** Constraints | **Actor:** Organisation | **Deps:** Legal

WHEN handling PII,
THE SYSTEM SHALL ensure all production personal data resides in UK datacenters and follows UK GDPR obligations.

---

### C-003 — Temenos T24 integration

**Source:** Constraints | **Actor:** System | **Deps:** Integration contracts

WHEN disbursing funds,
THE SYSTEM SHALL integrate with the Temenos T24 core banking system via the internal payment gateway as specified in integration contracts.

---

### C-004 — Experian and DocuSign mandated integrations

**Source:** Constraints | **Actor:** System | **Deps:** Supplier contracts

WHEN credit reports or e-signatures are required,
THE SYSTEM SHALL use Experian CreditExpert and DocuSign according to existing enterprise contracts.

---

## Source ID Mapping

| Source ID | Optional REQ Alias | Mapping Type | Notes |
|---|---|---|---|
| FR-* | — | Direct | All FR- entries preserved with EARS text |
| NFR-* | — | Direct | All NFR- entries preserved |
| OBJ-* | — | Context | Objectives preserved as top-level entries |
| C-* | — | Direct | Constraints preserved as C- entries |

---

## Open Questions

| ID | Question | Source ID | Blocking? | Owner | Status |
|---|---|---|---|---|---|
| OQ-001 | What is the approved AI model vendor / approach for risk scoring? | FR-008 / OBJ-001 | Yes | Head of AI | Answered: Azure Foundry (architecture input) |
| OQ-002 | Does the cooling-off waiver require legal sign-off? | FR-023 | No | Legal | Answered: Not required |
| OQ-003 | Fallback for HMRC KYC when unavailable? | FR-013 | Yes | Compliance | Answered: manual verification (architecture input) |
| OQ-004 | Exact AML database providers required | FR-012 | Yes | Compliance | Answered: HM Treasury only |
| OQ-005 | Is the T24 payment gateway API contract defined? | C-003 | Yes | IT Architecture | Answered: Can be defined by team |

---

## Assumptions

| ID | Assumption | Source ID | Risk if Wrong | Validation Approach | Status |
|---|---|---|---|---|---|
| ASM-001 | Experian, HMRC, DocuSign integrations are available under enterprise contracts | C-004 | High | Verify contracts and test endpoints | Open |
| ASM-002 | Test data and environments will be provided for NFR verification | NFR-002, NFR-003 | Medium | Provision test environments | Open |

---

## Traceability Notes

Every `FR-`, `NFR-`, and `OBJ-` from the provided `input/brs.md` has been preserved as an atomic requirement entry above. Constraints have been assigned `C-` identifiers and preserved.

## Loss Check

| Check | Result | Notes |
|---|---|---|
| Every `FR-` from BRS preserved | Yes | 30 FR entries preserved |
| Every `NFR-` from BRS preserved | Yes | 7 NFR entries preserved |
| Every `OBJ-` from BRS preserved | Yes | 5 OBJ entries preserved |
| Every explicit constraint preserved | Yes | 4 C- entries preserved |
| Every optional `REQ-` alias has source mapping | N/A | No REQ aliases used |
| Any intentionally postponed items explained | Yes | Open assumptions and questions documented |

---

*Set Status: Accepted only after human review. Never self-accept.*
