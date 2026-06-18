# Business Requirements Specification
# AI-Powered Loan Origination Platform

## Document metadata

| Field | Value |
|---|---|
| Initiative ID | I005 |
| Title | AI-Powered Loan Origination Platform |
| Version | 1.0 |
| Status | Draft |
| Owner | Head of Retail Lending |
| Date | 2026-06-12 |

## Business context

The bank currently processes personal loan applications through a fully manual workflow. Applications are submitted via paper or email, manually reviewed by underwriters, and decisions take 5–10 business days. Rejection rates are inconsistent across underwriters. Regulatory audit trails are incomplete. The bank faces increasing competition from fintechs offering same-day decisions and digital-first experiences.

The goal of this initiative is to replace the manual process with an AI-assisted digital platform that delivers consistent, auditable, and regulatory-compliant loan decisions within minutes for eligible applications, while preserving human underwriter oversight for complex or borderline cases.

## Business objectives

| ID | Objective | Success measure |
|---|---|---|
| OBJ-001 | Reduce average decision time from 5–10 days to under 30 minutes for straight-through cases | ≥70% of applications reach a decision in ≤30 minutes |
| OBJ-002 | Improve underwriter consistency | Variance in approval rate across underwriters reduced by ≥50% |
| OBJ-003 | Achieve full regulatory audit trail for all loan decisions | 100% of decisions have immutable audit trail within 24h of go-live |
| OBJ-004 | Comply with AML, KYC, and GDPR requirements at all stages | Zero regulatory findings in first post-launch compliance audit |
| OBJ-005 | Enable digital end-to-end for eligible applicants | ≥60% of approved loans disbursed without human intervention |

## Scope

**In scope:**
- Loan application intake (personal loans only, £1,000–£50,000)
- AI pre-screening and risk scoring
- Credit bureau integration (Experian)
- AML/KYC compliance checks
- Underwriter review workflow
- Loan offer generation and digital acceptance (e-signature)
- Core banking disbursement trigger
- Applicant self-service portal
- Underwriter and admin dashboard
- Observability and audit trail

**Out of scope:**
- Mortgage products
- Business loans
- Savings or current account products
- Direct debit setup (Phase 2)
- Mobile native app (Phase 2)

## Functional requirements

### Epic 1 — Loan Application Intake

**FR-001** — The system shall allow an applicant to submit a personal loan application online, providing: full name, date of birth, national insurance number, employment status, annual income, loan amount requested (£1,000–£50,000), loan purpose, and repayment term (12–84 months).

**FR-002** — The system shall validate all mandatory fields and display inline validation errors before submission. Incomplete applications shall not be submitted.

**FR-003** — The system shall assign a unique Application Reference Number (ARN) to every submitted application and display it to the applicant immediately after submission.

**FR-004** — The system shall send an email confirmation to the applicant within 2 minutes of submission, containing the ARN and an estimated decision timeline.

**FR-005** — The system shall allow an applicant to retrieve the status of their application using their ARN and date of birth, without requiring account registration.

### Epic 2 — AI Pre-Screening and Risk Scoring

**FR-006** — The system shall automatically trigger an AI pre-screening assessment for every submitted application within 60 seconds of submission.

**FR-007** — The AI pre-screening shall produce a risk score (0–1000) and a recommendation: `AUTO_APPROVE`, `REFER_TO_UNDERWRITER`, or `AUTO_DECLINE`.

**FR-008** — The AI scoring model shall use the following inputs: applicant-provided data, credit bureau data (FR-009), debt-to-income ratio, loan-to-income ratio, employment stability, and credit history length.

**FR-009** — The system shall integrate with Experian CreditExpert API to retrieve a credit report for every application. The integration shall complete within 30 seconds. If Experian is unavailable, the application shall be automatically routed to `REFER_TO_UNDERWRITER`.

**FR-010** — Applications with recommendation `AUTO_APPROVE` and loan amount ≤£10,000 shall proceed directly to offer generation (FR-015) without underwriter review, subject to AML/KYC clearance (FR-012).

**FR-011** — Applications with recommendation `AUTO_DECLINE` shall be notified to the applicant within 5 minutes with a decline reason category (not the score). A cooling-off period of 30 days shall be enforced before the same applicant can reapply.

### Epic 3 — AML / KYC Compliance

**FR-012** — The system shall perform AML screening on every applicant against HM Treasury sanctions list and PEP (Politically Exposed Persons) database before any offer is generated. AML screening shall complete within 60 seconds.

**FR-013** — The system shall perform KYC identity verification by cross-referencing the applicant's NI number, name, and date of birth against the HMRC identity verification API.

**FR-014** — Any application that fails AML screening or KYC verification shall be flagged as `COMPLIANCE_HOLD` and routed to the compliance team. The applicant shall receive a notification that their application is under review. No offer shall be generated for applications in `COMPLIANCE_HOLD`.

### Epic 4 — Underwriter Review Workflow

**FR-015** — The system shall present applications with `REFER_TO_UNDERWRITER` recommendation, or any `AUTO_APPROVE` application above £10,000, to the underwriter queue within 2 minutes of AI scoring completion.

**FR-016** — The underwriter dashboard shall display for each application: applicant summary, AI risk score and recommendation, credit bureau summary, debt-to-income ratio, loan-to-income ratio, employment verification status, and AML/KYC status.

**FR-017** — The underwriter shall be able to: approve the application (with optional conditions), decline the application (with mandatory reason), or request additional information from the applicant.

**FR-018** — The system shall record every underwriter action with: underwriter ID, timestamp, action taken, reason or conditions, and the AI recommendation that was presented. This record shall be immutable.

**FR-019** — Unactioned applications in the underwriter queue shall trigger an escalation notification to the team lead after 4 business hours.

### Epic 5 — Loan Offer and Digital Acceptance

**FR-020** — The system shall generate a loan offer document for every approved application containing: approved loan amount, interest rate (APR), monthly repayment amount, total repayable amount, repayment term, and key terms and conditions.

**FR-021** — The loan offer shall be presented to the applicant via their self-service portal and via email. The offer shall be valid for 14 days.

**FR-022** — The applicant shall be able to digitally accept the loan offer using e-signature (DocuSign integration). Acceptance shall be logged with timestamp and IP address.

**FR-023** — The system shall enforce a 14-day cooling-off period after digital acceptance during which the applicant may withdraw without penalty. The system shall send a reminder at day 7 and day 13.

### Epic 6 — Disbursement

**FR-024** — Upon digital acceptance and cooling-off period expiry (or applicant waiver), the system shall trigger a disbursement instruction to the core banking system (Temenos T24) via the internal payment gateway API.

**FR-025** — The disbursement instruction shall include: applicant account number, sort code, loan amount, reference number, and value date.

**FR-026** — The system shall receive a disbursement confirmation from the core banking system and update the application status to `DISBURSED`. If confirmation is not received within 2 minutes, the system shall retry once and then alert the operations team.

**FR-027** — The applicant shall receive an email and portal notification confirming disbursement with the expected value date.

### Epic 7 — Observability, Audit, and Administration

**FR-028** — The system shall maintain an immutable audit log of every state transition for every application, including: previous state, new state, triggering actor (applicant, AI model, underwriter ID, system), timestamp, and relevant data snapshot.

**FR-029** — The admin dashboard shall provide: application volume by status, average decision time, AI recommendation distribution, approval/decline rates by underwriter, and AML/KYC hold rates. Data shall refresh every 5 minutes.

**FR-030** — The system shall emit structured observability events for: application submission, AI scoring completion, AML/KYC result, underwriter decision, offer acceptance, and disbursement. Events shall include ARN, timestamp, status, and actor.

## Non-functional requirements

| ID | Requirement |
|---|---|
| NFR-001 | Application intake form shall load within 2 seconds on a standard broadband connection |
| NFR-002 | AI scoring pipeline shall complete end-to-end within 90 seconds under normal load |
| NFR-003 | System shall support 500 concurrent application submissions |
| NFR-004 | All PII shall be encrypted at rest (AES-256) and in transit (TLS 1.3) |
| NFR-005 | Audit log shall be write-once and tamper-evident |
| NFR-006 | System shall achieve 99.9% uptime during business hours (08:00–20:00 GMT) |
| NFR-007 | All API integrations (Experian, HMRC, DocuSign, T24) shall implement circuit breakers with defined fallback behaviour |

## Constraints

- Must comply with FCA Consumer Duty regulations
- Must comply with UK GDPR (data residency: UK only)
- Must integrate with existing Temenos T24 core banking system (internal payment gateway API — REST, existing contract)
- Must use Experian CreditExpert API (existing enterprise contract)
- AI model decisions must be explainable (FCA requirement) — black-box models are not permitted
- All data must remain within UK data centres
- E-signature must use DocuSign (existing enterprise contract)

## Open questions

| ID | Question | Owner | Priority | Answer |
|---|---|---|---|---|
| OQ-001 | What is the approved AI model vendor / approach for risk scoring? In-house model or third-party (e.g. Experian PowerCurve)? | Head of AI | High | Azure Foundry|
| OQ-002 | Does the cooling-off period waiver require a separate legal sign-off flow? | Legal | Medium | Not required|
| OQ-003 | What is the fallback for HMRC KYC API when unavailable — manual verification or auto-refer? | Compliance | High | manual verification |
| OQ-004 | What are the exact AML database providers — HM Treasury only, or also Dow Jones Watchlist? | Compliance | High | HM Treasury only |
| OQ-005 | Is the T24 payment gateway contract already defined, or does it need API contract negotiation? | IT Architecture | High | We can define ours |
