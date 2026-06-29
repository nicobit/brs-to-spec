# Atomic Requirements

## Source Inventory

- FR-001 — Loan Application Intake
- FR-002 — Inline field validation
- FR-003 — Assign Application Reference Number (ARN)
- FR-004 — Email confirmation within 2 minutes
- FR-005 — Status retrieval by ARN and DOB
- FR-006 — Trigger AI pre-screening within 60 seconds
- FR-007 — AI risk score and recommendation outputs
- FR-008 — AI scoring inputs (applicant data, credit bureau, ratios)
- FR-009 — Experian integration within 30 seconds, fallback to refer
- FR-010 — AUTO_APPROVE flow for ≤£10,000 subject to AML/KYC
- FR-011 — AUTO_DECLINE notification within 5 minutes and cooling-off
- FR-012 — AML screening within 60 seconds
- FR-013 — KYC identity verification via HMRC API
- FR-014 — COMPLIANCE_HOLD routing and notification
- FR-015 — Underwriter queue presentation within 2 minutes
- FR-016 — Underwriter dashboard data display
- FR-017 — Underwriter actions (approve/decline/request info)
- FR-018 — Immutable underwriter action record
- FR-019 — Escalation after 4 business hours
- FR-020 — Loan offer generation contents
- FR-021 — Offer presentation via portal and email
- FR-022 — Digital acceptance via DocuSign logged with timestamp and IP
- FR-023 — 14-day cooling-off with reminders
- FR-024 — Trigger core banking disbursement upon acceptance
- FR-025 — Disbursement instruction contents
- FR-026 — Disbursement confirmation and retry logic
- FR-027 — Disbursement notifications to applicant
- FR-028 — Immutable audit log of state transitions
- FR-029 — Admin dashboard metrics
- FR-030 — Structured observability events

## Requirement Catalogue

| ID | Type | Short Title |
|---|---|---|
| OBJ-001 | objective | Reduce decision time to ≤30 minutes for straight-through cases |
| OBJ-002 | objective | Improve underwriter consistency |
| OBJ-003 | objective | Achieve full regulatory audit trail |
| OBJ-004 | objective | Comply with AML, KYC, and GDPR requirements |
| OBJ-005 | objective | Enable digital end-to-end for eligible applicants |
| FR-001 | functional | Loan Application Intake |
| FR-002 | functional | Inline field validation |
| FR-003 | functional | Assign Application Reference Number (ARN) |
| FR-004 | functional | Email confirmation within 2 minutes |
| FR-005 | functional | Status retrieval by ARN and DOB |
| FR-006 | functional | Trigger AI pre-screening within 60 seconds |
| FR-007 | functional | AI risk score and recommendation outputs |
| FR-008 | functional | AI scoring inputs |
| FR-009 | functional | Experian integration with fallback |
| FR-010 | functional | AUTO_APPROVE flow for ≤£10,000 |
| FR-011 | functional | AUTO_DECLINE notification and cooling-off |
| FR-012 | functional | AML screening within 60 seconds |
| FR-013 | functional | KYC identity verification via HMRC API |
| FR-014 | functional | COMPLIANCE_HOLD routing and notification |
| FR-015 | functional | Underwriter queue presentation |
| FR-016 | functional | Underwriter dashboard data display |
| FR-017 | functional | Underwriter actions (approve/decline/request info) |
| FR-018 | functional | Immutable underwriter action record |
| FR-019 | functional | Escalation after 4 business hours |
| FR-020 | functional | Loan offer generation contents |
| FR-021 | functional | Offer presentation via portal and email |
| FR-022 | functional | Digital acceptance via DocuSign logged |
| FR-023 | functional | 14-day cooling-off with reminders |
| FR-024 | functional | Trigger core banking disbursement upon acceptance |
| FR-025 | functional | Disbursement instruction contents |
| FR-026 | functional | Disbursement confirmation and retry logic |
| FR-027 | functional | Disbursement notifications to applicant |
| FR-028 | functional | Immutable audit log of state transitions |
| FR-029 | functional | Admin dashboard metrics |
| FR-030 | functional | Structured observability events |
| NFR-001 | non-functional | Application intake form performance |
| NFR-002 | non-functional | AI scoring pipeline latency |
| NFR-003 | non-functional | Concurrency support (500 concurrent submissions) |
| NFR-004 | non-functional | PII encryption at rest and in transit |
| NFR-005 | non-functional | Audit log write-once and tamper-evident |
| NFR-006 | non-functional | 99.9% uptime during business hours |
| NFR-007 | non-functional | Circuit breakers for external APIs |

## Extracted Requirements (EARS)

### FR-001 — Loan Application Intake
**Source:** input/brs.md | **Actor:** Applicant | **Deps:** None

WHEN an applicant submits a personal loan application online,
THE SYSTEM SHALL capture full name, date of birth, national insurance number, employment status, annual income, loan amount requested (£1,000–£50,000), loan purpose, and repayment term (12–84 months).

### FR-002 — Inline field validation
**Source:** input/brs.md | **Actor:** Applicant | **Deps:** FR-001

WHEN an applicant fills the application form,
THE SYSTEM SHALL validate mandatory fields and display inline validation errors so that incomplete applications are not submitted.

### FR-003 — Assign Application Reference Number (ARN)
**Source:** input/brs.md | **Actor:** System | **Deps:** FR-001

WHEN an application is submitted,
THE SYSTEM SHALL assign a unique Application Reference Number (ARN) and display it to the applicant immediately after submission.

### FR-004 — Email confirmation within 2 minutes
**Source:** input/brs.md | **Actor:** System | **Deps:** FR-003

WHEN an application is submitted,
THE SYSTEM SHALL send an email confirmation containing the ARN and an estimated decision timeline within 2 minutes of submission.

### FR-005 — Status retrieval by ARN and DOB
**Source:** input/brs.md | **Actor:** Applicant | **Deps:** FR-003

WHEN an applicant provides ARN and date of birth,
THE SYSTEM SHALL allow retrieval of application status without requiring account registration.

### FR-006 — Trigger AI pre-screening within 60 seconds
**Source:** input/brs.md | **Actor:** System | **Deps:** FR-001

WHEN an application is submitted,
THE SYSTEM SHALL automatically trigger an AI pre-screening assessment within 60 seconds.

### FR-007 — AI risk score and recommendation outputs
**Source:** input/brs.md | **Actor:** AI Scoring Service | **Deps:** FR-006

WHEN the AI pre-screening runs,
THE SYSTEM SHALL produce a risk score (0–1000) and a recommendation value of AUTO_APPROVE, REFER_TO_UNDERWRITER, or AUTO_DECLINE.

### FR-008 — AI scoring inputs
**Source:** input/brs.md | **Actor:** AI Scoring Service | **Deps:** FR-006

WHEN generating a score,
THE SYSTEM SHALL use applicant-provided data, credit bureau data, debt-to-income ratio, loan-to-income ratio, employment stability, and credit history length as inputs.

### FR-009 — Experian integration within 30 seconds
**Source:** input/brs.md | **Actor:** System | **Deps:** FR-001

WHEN requesting a credit report from Experian CreditExpert API,
THE SYSTEM SHALL complete the integration within 30 seconds, and IF Experian is unavailable, THEN route the application to REFER_TO_UNDERWRITER.

### FR-010 — AUTO_APPROVE flow for ≤£10,000
**Source:** input/brs.md | **Actor:** System | **Deps:** FR-007, FR-012

WHEN AI recommendation is AUTO_APPROVE and loan amount ≤ £10,000,
THE SYSTEM SHALL proceed directly to offer generation subject to successful AML/KYC clearance.

### FR-011 — AUTO_DECLINE notification and cooling-off
**Source:** input/brs.md | **Actor:** System | **Deps:** FR-007

WHEN AI recommendation is AUTO_DECLINE,
THE SYSTEM SHALL notify the applicant within 5 minutes with a decline reason category and enforce a 30-day cooling-off period before the same applicant can reapply.

### FR-012 — AML screening within 60 seconds
**Source:** input/brs.md | **Actor:** System | **Deps:** FR-001

WHEN an application reaches the AML screening step,
THE SYSTEM SHALL perform AML screening against HM Treasury sanctions list and PEP database and complete within 60 seconds.

### FR-013 — KYC identity verification
**Source:** input/brs.md | **Actor:** System | **Deps:** FR-001

WHEN performing KYC,
THE SYSTEM SHALL verify identity by cross-referencing NI number, name, and date of birth against the HMRC identity verification API.

### FR-014 — COMPLIANCE_HOLD routing and notification
**Source:** input/brs.md | **Actor:** System | **Deps:** FR-012, FR-013

IF AML screening or KYC verification fails,
THEN THE SYSTEM SHALL flag the application as COMPLIANCE_HOLD, route it to the compliance team, and notify the applicant that their application is under review; no offer shall be generated while in COMPLIANCE_HOLD.

### FR-015 — Underwriter queue presentation
**Source:** input/brs.md | **Actor:** System | **Deps:** FR-007

WHEN an application requires underwriter review,
THE SYSTEM SHALL present it to the underwriter queue within 2 minutes of AI scoring completion.

### FR-016 — Underwriter dashboard data display
**Source:** input/brs.md | **Actor:** System | **Deps:** FR-015

WHEN an underwriter views an application,
THE SYSTEM SHALL display applicant summary, AI risk score and recommendation, credit bureau summary, debt-to-income ratio, loan-to-income ratio, employment verification status, and AML/KYC status.

### FR-017 — Underwriter actions
**Source:** input/brs.md | **Actor:** Underwriter | **Deps:** FR-016

WHEN reviewing an application,
THE UNDERWRITER SHALL be able to approve with optional conditions, decline with mandatory reason, or request additional information from the applicant.

### FR-018 — Immutable underwriter action record
**Source:** input/brs.md | **Actor:** System | **Deps:** FR-017

WHEN an underwriter takes an action,
THE SYSTEM SHALL record underwriter ID, timestamp, action taken, reason or conditions, and the AI recommendation presented in an immutable record.

### FR-019 — Escalation after 4 business hours
**Source:** input/brs.md | **Actor:** System | **Deps:** FR-015

IF an application remains unactioned in the underwriter queue for 4 business hours,
THEN THE SYSTEM SHALL send an escalation notification to the team lead.

### FR-020 — Loan offer generation contents
**Source:** input/brs.md | **Actor:** System | **Deps:** FR-010, FR-015

WHEN generating a loan offer,
THE SYSTEM SHALL include approved loan amount, interest rate (APR), monthly repayment amount, total repayable amount, repayment term, and key terms and conditions.

### FR-021 — Offer presentation
**Source:** input/brs.md | **Actor:** System | **Deps:** FR-020

WHEN an offer is generated,
THE SYSTEM SHALL present it via the applicant portal and email, with validity for 14 days.

### FR-022 — Digital acceptance logging
**Source:** input/brs.md | **Actor:** System | **Deps:** FR-021

WHEN an applicant digitally accepts an offer via DocuSign,
THE SYSTEM SHALL log acceptance with timestamp and IP address.

### FR-023 — Cooling-off reminders
**Source:** input/brs.md | **Actor:** System | **Deps:** FR-022

WHEN an offer is accepted,
THE SYSTEM SHALL enforce a 14-day cooling-off period and send reminders at day 7 and day 13.

### FR-024 — Trigger disbursement
**Source:** input/brs.md | **Actor:** System | **Deps:** FR-022

WHEN cooling-off expires or applicant waives it,
THE SYSTEM SHALL trigger a disbursement instruction to the core banking system.

### FR-025 — Disbursement instruction contents
**Source:** input/brs.md | **Actor:** System | **Deps:** FR-024

WHEN sending a disbursement instruction,
THE SYSTEM SHALL include applicant account number, sort code, loan amount, reference number, and value date.

### FR-026 — Disbursement confirmation and retry
**Source:** input/brs.md | **Actor:** System | **Deps:** FR-024

WHEN a disbursement instruction is sent,
THE SYSTEM SHALL await confirmation from core banking; IF no confirmation within 2 minutes, THEN retry once and alert operations if still unconfirmed.

### FR-027 — Disbursement notifications
**Source:** input/brs.md | **Actor:** System | **Deps:** FR-026

WHEN disbursement is confirmed,
THE SYSTEM SHALL notify the applicant via email and portal with the expected value date.

### FR-028 — Immutable audit log
**Source:** input/brs.md | **Actor:** System | **Deps:** multiple

WHEN state transitions occur,
THE SYSTEM SHALL write an immutable audit log entry including previous state, new state, triggering actor, timestamp, and data snapshot.

### FR-029 — Admin dashboard metrics
**Source:** input/brs.md | **Actor:** System | **Deps:** FR-028

WHEN the admin dashboard is viewed,
THE SYSTEM SHALL provide application volume by status, average decision time, AI recommendation distribution, approval/decline rates by underwriter, and AML/KYC hold rates, refreshing data every 5 minutes.

### FR-030 — Observability events
**Source:** input/brs.md | **Actor:** System | **Deps:** multiple

WHEN key events occur (submission, scoring completion, AML/KYC result, underwriter decision, offer acceptance, disbursement),
THE SYSTEM SHALL emit structured observability events including ARN, timestamp, status, and actor.

## Open Questions

| ID | Question | Owner | Priority | Answer |
|---|---|---|---|---|
| OQ-001 | What is the approved AI model vendor / approach for risk scoring? | Head of AI | High | Azure Foundry |
| OQ-002 | Does the cooling-off period waiver require a separate legal sign-off flow? | Legal | Medium | Not required |
| OQ-003 | What is the fallback for HMRC KYC API when unavailable — manual verification or auto-refer? | Compliance | High | manual verification |
| OQ-004 | What are the exact AML database providers — HM Treasury only, or also Dow Jones Watchlist? | Compliance | High | HM Treasury only |
| OQ-005 | Is the T24 payment gateway contract already defined, or does it need API contract negotiation? | IT Architecture | High | We can define ours |

## Assumptions

- All production systems and storage will be deployed within UK data centres to satisfy GDPR data residency.\
- Experian, HMRC, DocuSign, and Temenos T24 integrations are available via enterprise contracts or will be negotiated prior to implementation.\
- AI model decisions will be explainable to satisfy FCA requirements.
