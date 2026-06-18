# Delivery Structure

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I013-NEXT13 |
| Delivery mode | OpenSpec |
| Execution mode | Enterprise+Modular |
| Created at | 2026-06-16 |
| Created by | delivery-lead |
| Status | Draft |

## Story Count Assertion

**Total stories:** 12  
**Must:** 8 | **Should:** 3 | **Could:** 1  
**Delivery increments:** D1 (8 stories), D2 (3 stories), D3 (1 story)

---

## E-001: Application Intake

*Capture applicant data, validate, and persist application with ARN.*

### F-001: Online Application Submission

| Story | User Story | AC-NNN | Priority | Increment |
|---|---|---|---|---|
| F-001.1 | As an Applicant, I want to submit an online application, so that I can apply for a personal loan. | AC-001 | Must | D1 |
| F-001.2 | As an Applicant, I want inline field validation, so that I cannot submit incomplete applications. | AC-002 | Must | D1 |
| F-001.3 | As the System, I want to generate a unique ARN on submission, so that applications are traceable. | AC-003 | Must | D1 |

---

## E-002: Decisioning and Scoring

*Score applications using explainable models and produce recommendations.*

### F-002: AI Scoring Pipeline

| Story | User Story | AC-NNN | Priority | Increment |
|---|---|---|---|---|
| F-002.1 | As the System, I want to trigger AI pre-screening within 60s of submission, so that scoring starts promptly. | AC-004 | Must | D1 |
| F-002.2 | As the Scoring Service, I want to produce a 0–1000 risk score and recommendation with explainability outputs, so that decisions are auditable. | AC-005 | Must | D1 |
| F-002.3 | As the System, I want Experian integrations for credit lookups with fallback to refer-to-underwriter, so that scoring is robust. | AC-006 | Must | D2 |

---

## E-003: Compliance Screening

*Ensure AML and KYC screening before any offer generation.*

### F-003: AML / KYC Pipeline

| Story | User Story | AC-NNN | Priority | Increment |
|---|---|---|---|---|
| F-003.1 | As the System, I want to run AML screening and KYC verification before offer generation, so that offers are compliant. | AC-007 | Must | D1 |
| F-003.2 | As the System, I want to flag COMPLIANCE_HOLD and route to a human queue, so that exceptions are managed safely. | AC-008 | Must | D1 |

---

## E-004: Human Underwriter Workflow

*Provide underwriter dashboard and actions for referred cases.*

### F-004: Underwriter Queue and Dashboard

| Story | User Story | AC-NNN | Priority | Increment |
|---|---|---|---|---|
| F-004.1 | As an Underwriter, I want to see applicant summary, AI result, bureau summary, and AML/KYC status, so that I can make consistent decisions. | AC-009 | Must | D1 |
| F-004.2 | As an Underwriter, I want to record my action immutably with rationale, so that audit trails capture decisions. | AC-010 | Must | D1 |

---

## E-005: Offer Generation & Disbursement

*Generate offers and orchestrate disbursement to core banking.*

### F-005: Offer & Disbursement Orchestration

| Story | User Story | AC-NNN | Priority | Increment |
|---|---|---|---|---|
| F-005.1 | As the System, I want to generate loan offers with required financial fields, so that customers receive valid offers. | AC-011 | Should | D2 |
| F-005.2 | As the System, I want to orchestrate disbursement to Temenos T24 via internal payment gateway with idempotency, so that funds are disbursed reliably. | AC-012 | Must | D2 |
| F-005.3 | As the System, I want retries and alerting for disbursement confirmation failures, so that operations can intervene. | AC-013 | Should | D2 |

---

## E-006: Observability & Audit

*Emit structured events and maintain immutable audit store for compliance and operations.*

### F-006: Events, Metrics, and Audit

| Story | User Story | AC-NNN | Priority | Increment |
|---|---|---|---|---|
| F-006.1 | As Ops, I want structured observability events for submission, scoring, compliance, underwriter actions and disbursement, so that we can monitor and troubleshoot. | AC-014 | Must | D1 |

---

## FR Coverage

| FR-NNN | Stories | Status |
|---|---|---|
| FR-001 | F-001.1 | Covered |
| FR-002 | F-001.2 | Covered |
| FR-003 | F-001.3 | Covered |
| FR-004 | F-001.1 | Covered |
| FR-005 | F-001.1 | Covered |
| FR-006 | F-002.1 | Covered |
| FR-007 | F-002.2 | Covered |
| FR-008 | F-002.2 | Covered |
| FR-009 | F-002.3 | Covered |
| FR-012 | F-003.1 | Covered |
| FR-013 | F-003.1 | Covered |
| FR-024 | F-005.2 | Covered |

---
*Set Status: Draft — ready for delivery planning and sizing review.*
