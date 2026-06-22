# Delivery Skeleton

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I011-N2 |
| Created at | 2026-06-21 |
| Created by | delivery-lead |
| Status | Draft |

---

## Application Layers

| Layer | Present? | Components | Notes |
|---|---|---|---|
| Frontend | Yes | Applicant Portal, Underwriter Dashboard, Admin Dashboard | React / Next.js — Azure Static Web Apps |
| Backend API | Yes | Loan Origination API, Compliance Service, Notification Service | .NET 8 / Azure App Service; AI Scoring service in Container Apps |
| Infrastructure | Yes | CI/CD pipelines, environments (dev, test, stage, prod) | Azure DevOps / GitHub Actions; multi-region UK South/UK West |
| Integrations | Yes | Experian, HMRC, HM Treasury, DocuSign, Temenos T24 | Circuit breakers and fallbacks required |

---

## Epic Summary

| Metric | Value |
|---|---|
| Total epics | 4 |
| Must | 3 |
| Should | 1 |
| Could | 0 |

---

## Epic and Feature Hierarchy

### E-001 — Application Intake and Submission

*Allow applicants to submit personal loan applications and receive an ARN.*

| Field | Value |
|---|---|
| Priority | Must |
| Risk | Medium |
| Dependencies | None |

| Feature | Feature Title | Requirements Covered | Priority |
|---|---|---|---|
| F-001 | Application Form & Validation | REQ-001, REQ-002 | Must |
| F-002 | ARN Assignment & Confirmation | REQ-003 | Must |

### E-002 — AI Pre-Screening & Scoring

*Run scoring pipeline and produce recommendation labels and scores.*

| Field | Value |
|---|---|
| Priority | Must |
| Risk | High |
| Dependencies | E-001, Experian integration (REQ-006) |

| Feature | Feature Title | Requirements Covered | Priority |
|---|---|---|---|
| F-003 | AI Scoring Pipeline | REQ-004, REQ-006, REQ-012 | Must |

### E-003 — AML/KYC & Compliance Flow

*Perform AML and KYC checks and route compliance holds.*

| Field | Value |
|---|---|
| Priority | Must |
| Risk | High |
| Dependencies | Experian, HMRC integrations |

| Feature | Feature Title | Requirements Covered | Priority |
|---|---|---|---|
| F-004 | AML/KYC Screening & Routing | REQ-007, REQ-014, REQ-013 | Must |

### E-004 — Offer Generation, Acceptance, Disbursement

*Generate offers, capture acceptance via e-signature, and trigger disbursement.*

| Field | Value |
|---|---|
| Priority | Should |
| Risk | High |
| Dependencies | DocuSign, T24 integrations |

| Feature | Feature Title | Requirements Covered | Priority |
|---|---|---|---|
| F-005 | Offer Generation & Delivery | REQ-009, REQ-015 | Should |
| F-006 | Disbursement Integration | REQ-010 | Should |

---

## Epic Dependency Summary

| Epic | Depends On | Depended On By | Risk |
|---|---|---|---|
| E-001 | None | E-002, E-003 | Medium |
| E-002 | E-001, Experian | E-004 | High |

---

## Requirement Coverage

| Requirement ID | Source FRs | Feature(s) | Epic | Status |
|---|---|---|---|---|
| REQ-001 | FR-001, FR-003, FR-005, NFR-001 | F-001, F-002 | E-001 | Covered |
| REQ-002 | FR-002 | F-001 | E-001 | Covered |
| REQ-003 | FR-004 | F-002 | E-001 | Covered |
| REQ-004 | FR-006, FR-007, FR-008, FR-011, FR-015 | F-003 | E-002 | Covered |
| REQ-005 | FR-010, FR-015, FR-020 | F-005 | E-004 | Covered |
| REQ-006 | FR-009 | F-003 | E-002 | Covered |
| REQ-007 | FR-012, FR-013, FR-014 | F-004 | E-003 | Covered |
| REQ-008 | FR-016, FR-017, FR-018 | F-003, F-004 | E-002/E-003 | Covered |
| REQ-009 | FR-020, FR-021, FR-022, FR-023 | F-005 | E-004 | Covered |
| REQ-010 | FR-024, FR-025, FR-026, FR-027 | F-006 | E-004 | Covered |
| REQ-011 | FR-028 | F-003 | E-002 | Covered |
| REQ-012 | NFR-002, NFR-003, NFR-005, NFR-006 | F-003 | E-002 | Covered |
| REQ-013 | NFR-004, NFR-007 | F-003 | E-002 | Covered |
| REQ-014 | FR-029, FR-030 | F-004 | E-003 | Covered |
| REQ-015 | FR-019 | F-004 | E-003 | Covered |

---
*This is a lightweight skeleton. Stories are produced later during epic elaboration. Set Status: Confirmed only after review.*
