# Delivery Skeleton

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I988-N8 |
| Created at | 2026-06-21 |
| Created by | delivery-lead |
| Status | Draft |

---

## Application Layers

| Layer | Present? | Components | Notes |
|---|---|---|---|
| Frontend | Yes | Applicant Portal, Underwriter Dashboard, Admin Panel | Web UI for applicants and underwriters; react-hosted on CDN |
| Backend API | Yes | Loan Origination API, Scoring Service, Compliance Service, Underwriter Queue | Microservices with managed identities and event bus |
| Infrastructure | Yes | CI/CD pipelines, Key Vault, Monitoring, Regions: UK South/UK West | IaC via Bicep; environments: dev/staging/prod |
| Integrations | Yes | Experian, HMRC, DocuSign, Temenos T24 | External adapters and contract tests required |

---

## Epic Summary

| Metric | Value |
|---|---|
| Total epics | 5 |
| Must | 3 |
| Should | 1 |
| Could | 1 |

---

## Epic and Feature Hierarchy

### E-001 — Intake & Submission

*Enable applicants to submit and track loan applications.*

| Field | Value |
|---|---|
| Priority | Must |
| Risk | Medium |
| Dependencies | None |

| Feature | Feature Title | Requirements Covered | Priority |
|---|---|---|---|
| F-001 | Online application form and ARN generation | REQ-001, REQ-002 | Must |
| F-002 | Submission confirmation and applicant status | REQ-003, REQ-016 | Must |

### E-002 — AI Scoring & Risk Decisions

*Provide automated scoring, explainability, and routing decisions.*

| Field | Value |
|---|---|
| Priority | Must |
| Risk | High |
| Dependencies | E-001 |

| Feature | Feature Title | Requirements Covered | Priority |
|---|---|---|---|
| F-003 | AI scoring pipeline with explainability exports | REQ-004, REQ-017, REQ-018, REQ-014 | Must |
| F-004 | Experian integration for credit data (transient use) | REQ-005, REQ-018 | Should |

### E-003 — Compliance & Underwriter Workflows

*Handle AML/KYC, underwriter review, and audit logging.*

| Field | Value |
|---|---|
| Priority | Must |
| Risk | Medium-High |
| Dependencies | E-002 |

| Feature | Feature Title | Requirements Covered | Priority |
|---|---|---|---|
| F-005 | AML/KYC screening orchestration | REQ-006 | Must |
| F-006 | Underwriter queue, actions, and escalations | REQ-009, REQ-010, REQ-011 | Must |
| F-007 | Observability and audit event emission | REQ-013, REQ-022 | Should |

### E-004 — Offer Generation & Disbursement

*Generate offers, manage acceptance, and execute disbursements.*

| Field | Value |
|---|---|
| Priority | Should |
| Risk | High |
| Dependencies | E-003 |

| Feature | Feature Title | Requirements Covered | Priority |
|---|---|---|---|
| F-008 | Offer generation and DocuSign acceptance | REQ-007, REQ-019, REQ-020 | Should |
| F-009 | Disbursement adapter and reconciliation | REQ-012, REQ-021, REQ-005 | Must |

### E-005 — Platform, Non-functional & Reporting

*Foundation, performance, security, and admin reporting.*

| Field | Value |
|---|---|
| Priority | Could |
| Risk | Medium |
| Dependencies | E-001, E-002, E-003 |

| Feature | Feature Title | Requirements Covered | Priority |
|---|---|---|---|
| F-010 | Performance, residency, encryption, and key management | REQ-014, REQ-015, REQ-024, REQ-029 | Must |
| F-011 | Admin metrics and dashboards | REQ-023 | Could |

---

## Epic Dependency Summary

| Epic | Depends On | Depended On By | Risk |
|---|---|---|---|
| E-001 | None | E-002, E-003 | Medium |
| E-002 | E-001 | E-003 | High |
| E-003 | E-002 | E-004 | Medium-High |
| E-004 | E-003 | None | High |
| E-005 | E-001,E-002,E-003 | None | Medium |

---

## Requirement Coverage


| REQ / FR | Feature | Epic | Status |
|---|---|---|---|
| REQ-001 | F-001 | E-001 | Covered |
| REQ-002 | F-001 | E-001 | Covered |
| REQ-003 | F-002 | E-001 | Covered |
| REQ-004 | F-003 | E-002 | Covered |
| REQ-005 | F-004 | E-002 | Covered |
| REQ-006 | F-005 | E-003 | Covered |
| REQ-007 | F-008 | E-004 | Covered |
| REQ-008 | F-006 | E-003 | Covered |
| REQ-009 | F-006 | E-003 | Covered |
| REQ-010 | F-006 | E-003 | Covered |
| REQ-011 | F-006 | E-003 | Covered |
| REQ-012 | F-009 | E-004 | Covered |
| REQ-013 | F-007 | E-003 | Covered |
| REQ-014 | F-010 | E-005 | Covered |
| REQ-015 | F-010 | E-005 | Covered |
| REQ-016 | F-002 | E-001 | Covered |
| REQ-017 | F-003 | E-002 | Covered |
| REQ-018 | F-003 | E-002 | Covered |
| REQ-019 | F-008 | E-004 | Covered |
| REQ-020 | F-008 | E-004 | Covered |
| REQ-021 | F-009 | E-004 | Covered |
| REQ-022 | F-007 | E-003 | Covered |
| REQ-023 | F-011 | E-005 | Covered |
| REQ-024 | F-010 | E-005 | Covered |

# BRS Functional Requirements
| FR-001 | F-001 | E-001 | Covered |
| FR-002 | F-001 | E-001 | Covered |
| FR-003 | F-001 | E-001 | Covered |
| FR-004 | F-002 | E-001 | Covered |
| FR-005 | F-002 | E-001 | Covered |
| FR-006 | F-003 | E-002 | Covered |
| FR-007 | F-003 | E-002 | Covered |
| FR-008 | F-003 | E-002 | Covered |
| FR-009 | F-004 | E-002 | Covered |
| FR-010 | F-003 | E-002 | Covered |
| FR-011 | F-003 | E-002 | Covered |
| FR-012 | F-005 | E-003 | Covered |
| FR-013 | F-005 | E-003 | Covered |
| FR-014 | F-010 | E-005 | Covered |
| FR-015 | F-006 | E-003 | Covered |
| FR-016 | F-006 | E-003 | Covered |
| FR-017 | F-006 | E-003 | Covered |
| FR-018 | F-006 | E-003 | Covered |
| FR-019 | F-006 | E-003 | Covered |
| FR-020 | F-008 | E-004 | Covered |
| FR-021 | F-008 | E-004 | Covered |
| FR-022 | F-008 | E-004 | Covered |
| FR-023 | F-008 | E-004 | Covered |
| FR-024 | F-009 | E-004 | Covered |
| FR-025 | F-009 | E-004 | Covered |
| FR-026 | F-009 | E-004 | Covered |
| FR-027 | F-009 | E-004 | Covered |
| FR-028 | F-007 | E-003 | Covered |
| FR-029 | F-011 | E-005 | Covered |
| FR-030 | F-007 | E-003 | Covered |

## Non-functional Requirements (NFR)

| NFR-001 | F-010 | E-005 | Covered |
| NFR-002 | F-003 | E-002 | Covered |
| NFR-003 | F-010 | E-005 | Covered |
| NFR-004 | F-010 | E-005 | Covered |
| NFR-005 | F-007 | E-003 | Covered |
| NFR-006 | F-010 | E-005 | Covered |
| NFR-007 | F-004 | E-002 | Covered |

---
*This is a lightweight skeleton. Stories are produced later during epic elaboration. Set Status: Confirmed only after review. Never self-accept.*
