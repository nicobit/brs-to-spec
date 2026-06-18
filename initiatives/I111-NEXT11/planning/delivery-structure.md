# Delivery Structure

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I111-NEXT11 |
| Delivery mode | OpenSpec |
| Execution mode | Enterprise+Modular |
| Created at | 2026-06-18 |
| Created by | delivery-lead |
| Status | Draft |

## Story Count Assertion

**Total stories:** 12  
**Must:** 8 | **Should:** 3 | **Could:** 1  
**Delivery increments:** D1 (8 stories), D2 (4 stories)

---

## E-001: Application Intake and Decisioning

*Deliver a complete loan application intake, decisioning, and handoff flow with audit and integrations.*

### F-001: Intake & Validation

| Story | User Story | AC-NNN | Priority | Increment |
|---|---|---|---|---|
| F-001.1 | As an Applicant, I want to submit a loan application with required fields so that I receive an ARN and confirmation. | AC-001 | Must | D1 |
| F-001.2 | As an Applicant, I want to receive a confirmation email with ARN so that I have a record of my submission. | AC-002 | Should | D1 |
| F-001.3 | As an Applicant, I want to look up my application status using ARN + DOB so that I can track progress. | AC-003 | Should | D1 |

#### F-001.1 — Story Detail

| Field | Value |
|---|---|
| Actor | Applicant |
| Linked requirements | FR-001, FR-002, FR-003 |
| Linked business rules | BR-001 (thresholds) |
| Primary component | Application Backend |
| Out of scope | Bulk batch import of legacy applications |

#### F-001.2 — Story Detail

| Field | Value |
|---|---|
| Actor | Applicant |
| Linked requirements | FR-004 |
| Linked business rules |  |
| Primary component | Notification Service |
| Out of scope | Third-party email deliverability monitoring |

#### F-001.3 — Story Detail

| Field | Value |
|---|---|
| Actor | Applicant |
| Linked requirements | FR-005 |
| Linked business rules |  |
| Primary component | Application Backend |
| Out of scope | Full account registration and login flows |

### F-002: Scoring & Decisioning

| Story | User Story | AC-NNN | Priority | Increment |
|---|---|---|---|---|
| F-002.1 | As the system, I want to trigger AI pre-screening within 60s of submission so that initial routing is available. | AC-004 | Must | D1 |
| F-002.2 | As the system, I want to produce a risk score and recommendation (AUTO_APPROVE/REFER_TO_UNDERWRITER/AUTO_DECLINE) so that downstream flows can act. | AC-005 | Must | D1 |
| F-002.3 | As the system, I want to call Experian and handle fallback routes so that credit decisions are resilient. | AC-006 | Must | D1 |

#### F-002.1 — Story Detail

| Field | Value |
|---|---|
| Actor | System (AI Scoring Service) |
| Linked requirements | FR-006, NFR-002 |
| Linked business rules |  |
| Primary component | AI Scoring Service |
| Out of scope | Model training and offline experiments |

#### F-002.2 — Story Detail

| Field | Value |
|---|---|
| Actor | System (AI Scoring Service) |
| Linked requirements | FR-007 |
| Linked business rules | BR-001 |
| Primary component | AI Scoring Service |
| Out of scope | Human-in-the-loop decisioning workflows beyond referral |

#### F-002.3 — Story Detail

| Field | Value |
|---|---|
| Actor | System (Integrations Layer) |
| Linked requirements | FR-009 |
| Linked business rules | BR-002 |
| Primary component | Integrations Layer |
| Out of scope | Procurement and contract sign-off activities |

### F-003: Underwriter & Operations

| Story | User Story | AC-NNN | Priority | Increment |
|---|---|---|---|---|
| F-003.1 | As an Underwriter, I want a queue of REFER_TO_UNDERWRITER items so that I can take action. | AC-007 | Must | D1 |
| F-003.2 | As an Underwriter, I want a dashboard showing applicant summary, score, and evidence so that I can decide quickly. | AC-008 | Must | D1 |
| F-003.3 | As an Underwriter, I want to record actions immutably so that audit requirements are met. | AC-009 | Must | D1 |

#### F-003.1 — Story Detail

| Field | Value |
|---|---|
| Actor | Underwriter |
| Linked requirements | FR-015 |
| Linked business rules | BR-005 |
| Primary component | Underwriter UI + Queue |
| Out of scope | SLA-driven case reassignment automation |

#### F-003.2 — Story Detail

| Field | Value |
|---|---|
| Actor | Underwriter |
| Linked requirements | FR-016, FR-018 |
| Linked business rules | BR-005 |
| Primary component | Underwriter Dashboard |
| Out of scope | Full analytics workspace for long-term trends |

#### F-003.3 — Story Detail

| Field | Value |
|---|---|
| Actor | Underwriter |
| Linked requirements | FR-017, FR-018 |
| Linked business rules | BR-005 |
| Primary component | Audit Log / Immutable Store |
| Out of scope | Legal-grade archival beyond retention policy |

### F-004: Offer & Disbursement

| Story | User Story | AC-NNN | Priority | Increment |
|---|---|---|---|---|
| F-004.1 | As the system, I want to generate loan offers for approved applications so that applicants can accept terms. | AC-010 | Must | D1 |
| F-004.2 | As an Applicant, I want to sign offers via DocuSign so that acceptance is recorded. | AC-011 | Must | D2 |
| F-004.3 | As the system, I want to trigger disbursement to Temenos T24 and confirm status so that funds are released. | AC-012 | Must | D2 |

#### F-004.1 — Story Detail

| Field | Value |
|---|---|
| Actor | System |
| Linked requirements | FR-020, FR-021 |
| Linked business rules |  |
| Primary component | Offer Service |
| Out of scope | Long-term loan servicing flows |

#### F-004.2 — Story Detail

| Field | Value |
|---|---|
| Actor | Applicant |
| Linked requirements | FR-022 |
| Linked business rules |  |
| Primary component | DocuSign Integration |
| Out of scope | In-house signature mechanisms |

#### F-004.3 — Story Detail

| Field | Value |
|---|---|
| Actor | System (Integrations) |
| Linked requirements | FR-024, FR-025, FR-026 |
| Linked business rules | BR-006 |
| Primary component | Disbursement Integration (Temenos T24) |
| Out of scope | Bank reconciliation automation beyond first retry |

---

## FR Coverage

| FR-NNN | Stories | Status |
|---|---|---|
| FR-001 | F-001.1 | Covered |
| FR-002 | F-001.1 | Covered |
| FR-003 | F-001.1 | Covered |
| FR-004 | F-001.2 | Covered |
| FR-005 | F-001.3 | Covered |
| FR-006 | F-002.1 | Covered |
| FR-007 | F-002.2 | Covered |
| FR-009 | F-002.3 | Covered |
| FR-010 | F-002.2 | Covered |
| FR-011 | F-002.2 | Covered |
| FR-012 | F-002.3 | Covered |
| FR-013 | F-002.3 | Covered |
| FR-014 | F-003.3 | Covered |
| FR-015 | F-003.1 | Covered |
| FR-016 | F-003.2 | Covered |
| FR-017 | F-003.3 | Covered |
| FR-018 | F-003.2, F-003.3 | Covered |
| FR-019 | F-003.1 | Covered |
| FR-020 | F-004.1 | Covered |
| FR-021 | F-004.1 | Covered |
| FR-022 | F-004.2 | Covered |
| FR-023 | F-004.1 | Covered |
| FR-024 | F-004.3 | Covered |
| FR-025 | F-004.3 | Covered |
| FR-026 | F-004.3 | Covered |
| FR-027 | F-004.1 | Covered |
| FR-028 | F-003.3 | Covered |
| FR-029 | F-003.2 | Covered |
| FR-030 | F-002.2, F-003.2 | Covered |

---

*Set Status: Confirmed only after review and readiness progression. Never self-accept.*
