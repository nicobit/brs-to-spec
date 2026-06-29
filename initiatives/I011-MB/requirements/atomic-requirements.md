## Requirement Catalogue

### OBJ-001 — Reduce average decision time

**Source:** input/brs.md | **Actor:** Product | **Deps:** None

WHEN measuring decision times for straight-through cases, THE SYSTEM SHALL achieve an average decision time of under 30 minutes for ≥70% of applications.

### OBJ-002 — Improve underwriter consistency

**Source:** input/brs.md | **Actor:** Product | **Deps:** None

WHEN comparing approval rates across underwriters, THE SYSTEM SHALL reduce variance in approval rates by ≥50% relative to baseline.

### OBJ-003 — Regulatory audit trail

**Source:** input/brs.md | **Actor:** Product | **Deps:** None

THE SYSTEM SHALL ensure 100% of loan decisions have an immutable audit trail recorded within 24 hours of decision.

### OBJ-004 — Compliance targets

**Source:** input/brs.md | **Actor:** Product | **Deps:** None

THE SYSTEM SHALL operate in compliance with AML, KYC, and GDPR requirements such that the first post-launch compliance audit yields zero findings.

### OBJ-005 — Digital end-to-end

**Source:** input/brs.md | **Actor:** Product | **Deps:** None

WHEN measuring post-launch disbursements, THE SYSTEM SHALL support ≥60% of approved loans being disbursed without human intervention.

---

### FR-001 — Application submission

**Source:** input/brs.md | **Actor:** Applicant | **Deps:** None

WHEN an applicant submits an application, THE SYSTEM SHALL accept personal loan applications with full name, date of birth, national insurance number, employment status, annual income, loan amount requested (£1,000–£50,000), loan purpose, and repayment term (12–84 months).

---

## Open Questions

| ID | Question | Source ID | Blocking? | Owner | Status |
|---|---|---|---|---|---|
| OQ-001 | What is the approved AI model vendor / approach for risk scoring? | FR-007 | Yes | Head of AI | Answered: Azure Foundry |
| OQ-002 | Does the cooling-off period waiver require a separate legal sign-off flow? | FR-023 | No | Legal | Answered: Not required |
| OQ-003 | What is the fallback for HMRC KYC API when unavailable? | FR-013 | Yes | Compliance | Answered: manual verification |
| OQ-004 | What are the exact AML database providers? | FR-012 | Yes | Compliance | Answered: HM Treasury only |
| OQ-005 | Is the T24 payment gateway contract defined or needs negotiation? | C-003 | Yes | IT Architecture | Answered: Can define ours |

---

## Assumptions

| ID | Assumption | Source ID | Risk if Wrong | Validation Approach | Status |
|---|---|---|---|---|---|
| ASM-001 | Experian API contract and endpoints are available as specified | FR-009 / C-003 | Integration delays | Confirm with Experian integration team | Open |
| ASM-002 | HMRC identity verification covers required NI matching | FR-013 | Manual verification increases workload | Confirm with HMRC integration team | Open |
| ASM-003 | DocuSign integration supports logging of IP and timestamp | FR-022 | Legal evidence gaps | Validate DocuSign contract | Open |

---

## Source ID Mapping

### FR-002 — Inline validation

**Source:** input/brs.md | **Actor:** Applicant | **Deps:** FR-001

WHEN an applicant fills mandatory fields, THE SYSTEM SHALL validate mandatory fields and display inline validation errors before submission; incomplete applications shall not be submitted.

### FR-003 — Application Reference Number

**Source:** input/brs.md | **Actor:** System | **Deps:** FR-001

WHEN an application is submitted, THE SYSTEM SHALL assign a unique Application Reference Number (ARN) and display it to the applicant immediately after submission.

### FR-004 — Confirmation email

**Source:** input/brs.md | **Actor:** System | **Deps:** FR-003

WHEN an application is submitted, THE SYSTEM SHALL send an email confirmation to the applicant within 2 minutes containing the ARN and an estimated decision timeline.

### FR-005 — Status retrieval

**Source:** input/brs.md | **Actor:** Applicant | **Deps:** FR-003

WHEN an applicant provides ARN and date of birth, THE SYSTEM SHALL allow the applicant to retrieve the status of their application without requiring account registration.

### FR-006 — Trigger AI pre-screening

**Source:** input/brs.md | **Actor:** System | **Deps:** FR-001

WHEN an application is submitted, THE SYSTEM SHALL automatically trigger an AI pre-screening assessment within 60 seconds of submission.

### FR-007 — Risk score and recommendation

**Source:** input/brs.md | **Actor:** System | **Deps:** FR-006

WHEN the AI pre-screening runs, THE SYSTEM SHALL produce a risk score (0–1000) and a recommendation value in {AUTO_APPROVE, REFER_TO_UNDERWRITER, AUTO_DECLINE}.

### FR-008 — Scoring inputs

**Source:** input/brs.md | **Actor:** System | **Deps:** FR-006

THE SYSTEM SHALL use applicant-provided data, credit bureau data, debt-to-income ratio, loan-to-income ratio, employment stability, and credit history length as inputs to the AI scoring model.

### FR-009 — Experian integration

**Source:** input/brs.md | **Actor:** System | **Deps:** FR-006

WHEN the system requests a credit report, THE SYSTEM SHALL integrate with Experian CreditExpert API and complete retrieval within 30 seconds; if Experian is unavailable, THEN the application SHALL be routed to REFER_TO_UNDERWRITER.

### FR-010 — Auto-approve flow

**Source:** input/brs.md | **Actor:** System | **Deps:** FR-007

IF the AI recommendation is AUTO_APPROVE AND loan amount ≤ £10,000, THEN THE SYSTEM SHALL proceed directly to offer generation without underwriter review, subject to AML/KYC clearance.

### FR-011 — Auto-decline notification

**Source:** input/brs.md | **Actor:** System | **Deps:** FR-007

IF the AI recommendation is AUTO_DECLINE, THEN THE SYSTEM SHALL notify the applicant within 5 minutes with a decline reason category and enforce a 30-day cooling-off period before the same applicant can reapply.

### FR-012 — AML screening

**Source:** input/brs.md | **Actor:** System | **Deps:** FR-006

WHEN preparing to generate an offer, THE SYSTEM SHALL perform AML screening against HM Treasury sanctions list and PEP database and complete within 60 seconds.

### FR-013 — KYC verification

**Source:** input/brs.md | **Actor:** System | **Deps:** FR-006

WHEN identity verification is required, THE SYSTEM SHALL perform KYC by cross-referencing NI number, name, and date of birth against HMRC identity verification API.

### FR-014 — Compliance hold routing

**Source:** input/brs.md | **Actor:** System | **Deps:** FR-012, FR-013

IF AML screening or KYC verification fails, THEN THE SYSTEM SHALL flag the application as COMPLIANCE_HOLD and route it to the compliance team; no offer shall be generated while in COMPLIANCE_HOLD.

### FR-015 — Underwriter queue

**Source:** input/brs.md | **Actor:** System | **Deps:** FR-006, FR-010

WHEN the AI recommendation is REFER_TO_UNDERWRITER OR an AUTO_APPROVE above £10,000, THE SYSTEM SHALL present the application to the underwriter queue within 2 minutes of AI scoring completion.

### FR-016 — Underwriter dashboard contents

**Source:** input/brs.md | **Actor:** Underwriter | **Deps:** FR-015

THE SYSTEM SHALL display for each application: applicant summary, AI risk score and recommendation, credit bureau summary, debt-to-income ratio, loan-to-income ratio, employment verification status, and AML/KYC status on the underwriter dashboard.

### FR-017 — Underwriter actions

**Source:** input/brs.md | **Actor:** Underwriter | **Deps:** FR-015

THE SYSTEM SHALL allow the underwriter to approve (with optional conditions), decline (with mandatory reason), or request additional information from the applicant.

### FR-018 — Underwriter audit record

**Source:** input/brs.md | **Actor:** System | **Deps:** FR-017

WHEN an underwriter takes action, THE SYSTEM SHALL record underwriter ID, timestamp, action taken, reason/conditions, and the AI recommendation presented; this record shall be immutable.

### FR-019 — Escalation for unactioned apps

**Source:** input/brs.md | **Actor:** System | **Deps:** FR-015

IF an application remains unactioned in the underwriter queue for 4 business hours, THEN THE SYSTEM SHALL trigger an escalation notification to the team lead.

### FR-020 — Loan offer contents

**Source:** input/brs.md | **Actor:** System | **Deps:** FR-010, FR-012

THE SYSTEM SHALL generate a loan offer document containing approved loan amount, interest rate (APR), monthly repayment amount, total repayable amount, repayment term, and key terms and conditions.

### FR-021 — Offer presentation

**Source:** input/brs.md | **Actor:** System | **Deps:** FR-020

WHEN an offer is generated, THE SYSTEM SHALL present it via the self-service portal and email, and the offer shall be valid for 14 days.

### FR-022 — E-signature acceptance

**Source:** input/brs.md | **Actor:** Applicant | **Deps:** FR-021

WHEN an applicant accepts an offer, THE SYSTEM SHALL allow digital acceptance via e-signature (DocuSign) and log acceptance with timestamp and IP address.

### FR-023 — Cooling-off period

**Source:** input/brs.md | **Actor:** System | **Deps:** FR-022

WHEN an offer is accepted, THE SYSTEM SHALL enforce a 14-day cooling-off period during which the applicant may withdraw without penalty and send reminders at day 7 and day 13.

### FR-024 — Disbursement trigger

**Source:** input/brs.md | **Actor:** System | **Deps:** FR-023

WHEN cooling-off expires or applicant waives it, THE SYSTEM SHALL trigger a disbursement instruction to Temenos T24 via internal payment gateway API including account number, sort code, loan amount, reference number, and value date.

### FR-025 — Disbursement instruction contents

**Source:** input/brs.md | **Actor:** System | **Deps:** FR-024

THE SYSTEM SHALL include applicant account number, sort code, loan amount, reference number, and value date in the disbursement instruction.

### FR-026 — Disbursement confirmation handling

**Source:** input/brs.md | **Actor:** System | **Deps:** FR-024

IF disbursement confirmation is not received within 2 minutes, THEN THE SYSTEM SHALL retry once and then alert the operations team.

### FR-027 — Disbursement notification

**Source:** input/brs.md | **Actor:** System | **Deps:** FR-026

WHEN disbursement is confirmed, THE SYSTEM SHALL notify the applicant by email and portal with the expected value date.

### FR-028 — Immutable audit log

**Source:** input/brs.md | **Actor:** System | **Deps:** All FRs

THE SYSTEM SHALL maintain an immutable audit log for every state transition including previous state, new state, triggering actor, timestamp, and relevant data snapshot.

### FR-029 — Admin dashboard metrics

**Source:** input/brs.md | **Actor:** Admin | **Deps:** FR-028

THE SYSTEM SHALL provide admin dashboard metrics: application volume by status, average decision time, AI recommendation distribution, approval/decline rates by underwriter, and AML/KYC hold rates, refreshed every 5 minutes.

### FR-030 — Observability events

**Source:** input/brs.md | **Actor:** System | **Deps:** FR-028

THE SYSTEM SHALL emit structured observability events for submission, AI scoring completion, AML/KYC result, underwriter decision, offer acceptance, and disbursement including ARN, timestamp, status, and actor.

---

### NFR-001 — Intake performance

**Source:** input/brs.md | **Actor:** System | **Deps:** FR-001

THE SYSTEM SHALL render the application intake form within 2 seconds on a standard broadband connection.

### NFR-002 — Scoring pipeline latency

**Source:** input/brs.md | **Actor:** System | **Deps:** FR-006

THE SYSTEM SHALL complete the AI scoring pipeline end-to-end within 90 seconds under normal load.

### NFR-003 — Concurrency

**Source:** input/brs.md | **Actor:** System | **Deps:** FR-006

THE SYSTEM SHALL support 500 concurrent application submissions.

### NFR-004 — Encryption

**Source:** input/brs.md | **Actor:** System | **Deps:** FR-028

THE SYSTEM SHALL encrypt all PII at rest using AES-256 and in transit using TLS 1.3.

### NFR-005 — Audit log properties

**Source:** input/brs.md | **Actor:** System | **Deps:** FR-028

THE SYSTEM SHALL ensure the audit log is write-once and tamper-evident.

### NFR-006 — Uptime

**Source:** input/brs.md | **Actor:** System | **Deps:** All services

THE SYSTEM SHALL achieve 99.9% uptime during business hours (08:00–20:00 GMT).

### NFR-007 — Integration resilience

**Source:** input/brs.md | **Actor:** System | **Deps:** Experian, HMRC, DocuSign, T24 integrations

THE SYSTEM SHALL implement circuit breakers with defined fallback behaviour for all external API integrations.

---

### C-001 — FCA Consumer Duty compliance

**Source:** input/brs.md Constraints | **Actor:** Compliance | **Deps:** None

THE SYSTEM SHALL comply with FCA Consumer Duty requirements as applicable to loan origination.

### C-002 — Data residency

**Source:** input/brs.md Constraints | **Actor:** Architecture | **Deps:** None

THE SYSTEM SHALL store and process all personal data within UK data centres only.

### C-003 — Experian contract

**Source:** input/brs.md Constraints | **Actor:** Integration | **Deps:** None

THE SYSTEM SHALL use Experian CreditExpert API for credit reports as specified by existing enterprise contract.

### C-004 — Explainability requirement

**Source:** input/brs.md Constraints | **Actor:** AI/Product | **Deps:** None

THE SYSTEM SHALL use explainable models for scoring; black-box models without explainability are not permitted.

---

## Source ID Mapping

All output entries preserve original BRS IDs as headings. No REQ-* aliases introduced in this run.
