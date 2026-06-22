# Delivery Skeleton (Light)

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I111-N11 |
| Created at | 2026-06-22 |
| Created by | delivery-lead |
| Status | Draft |

## Application Layers

| Layer | Present? | Components | Notes |
|---|---|---|---|
| Frontend | Yes | Applicant Portal, Underwriter Dashboard, Admin Dashboard | React/Next.js — Azure Static Web Apps |
| Backend API | Yes | Loan Origination API, Compliance Service, Notification Service | .NET 8 / FastAPI for AI scoring |
| Infrastructure | Yes | Azure Service Bus, Cosmos DB, Azure SQL, Container Apps | UK regions only; CI/CD required |
| Integrations | Yes | Experian, HMRC, DocuSign, Temenos T24 | Circuit-breakers required |

## Epics

### E-001 — Application Intake and Submission (Priority: Must, Risk: Low-Medium)
Objective: Enable applicants to submit complete applications and receive ARN and confirmation.

### E-002 — AI Pre-Screening & Risk Scoring (Priority: Must, Risk: Medium-High)
Objective: Automatically produce risk scores and recommendations for submitted applications.

### E-003 — AML / KYC Compliance and Screening (Priority: Must, Risk: High)
Objective: Perform AML and KYC checks prior to offer generation; route to compliance when required.

### E-004 — Underwriter Review Workflow (Priority: Should, Risk: Medium)
Objective: Provide queueing, case view, and action recording for underwriters.

### E-005 — Offer Generation and Digital Acceptance (Priority: Must, Risk: Medium)
Objective: Generate offers and acceptances via DocuSign with cooling-off handling.

### E-006 — Disbursement and Core Banking Integration (Priority: Must, Risk: High)
Objective: Trigger and confirm disbursements to Temenos T24.

### E-007 — Observability, Audit and Ops (Priority: Must, Risk: Medium)
Objective: Emit metrics, maintain immutable audit trail, and provide admin dashboards.

## Features (per epic)

E-001 Features:
- F-001 Applicant submission form — covers: REQ-001, REQ-002, REQ-004
- F-002 Submission confirmation and email — covers: REQ-003

E-002 Features:
- F-003 Scoring invocation & event contract — covers: REQ-005, REQ-006, REQ-024
- F-004 Experian integration adapter — covers: REQ-007

E-003 Features:
- F-005 AML screening integration — covers: REQ-010
- F-006 KYC verification integration — covers: REQ-011

E-004 Features:
- F-007 Underwriter queue and case view — covers: REQ-012, REQ-013

E-005 Features:
- F-008 Offer generation — covers: REQ-014
- F-009 E-signature acceptance (DocuSign) — covers: REQ-015

E-006 Features:
- F-010 Disbursement adapter to T24 — covers: REQ-016, REQ-017

E-007 Features:
- F-011 Audit log and immutable storage — covers: REQ-018
 - F-012 Observability events and dashboards — covers: REQ-019
 - F-013 Performance & scalability (scoring infra) — covers: REQ-020, REQ-021
 - F-014 Resilience & integration guardrails — covers: REQ-023
 - F-015 Security: encryption & key management — covers: REQ-022

## Epic and Feature Hierarchy

| Feature ID | Title | Epic | Requirements Covered | Priority |
|---|---|---|---|---|
| F-001 | Applicant submission form | E-001 | REQ-001, REQ-002, REQ-004 | Must |
| F-002 | Submission confirmation and email | E-001 | REQ-003 | Must |
| F-003 | Scoring invocation & event contract | E-002 | REQ-005, REQ-006, REQ-024 | Must |
| F-004 | Experian integration adapter | E-002 | REQ-007 | Must |
| F-005 | AML screening integration | E-003 | REQ-010 | Must |
| F-006 | KYC verification integration | E-003 | REQ-011 | Must |
| F-007 | Underwriter queue and case view | E-004 | REQ-012, REQ-013 | Should |
| F-008 | Offer generation | E-005 | REQ-014 | Must |
| F-009 | E-signature acceptance (DocuSign) | E-005 | REQ-015 | Must |
| F-010 | Disbursement adapter to T24 | E-006 | REQ-016, REQ-017 | Must |
| F-011 | Audit log and immutable storage | E-007 | REQ-018 | Must |
| F-012 | Observability events and dashboards | E-007 | REQ-019 | Must |
| F-013 | Performance & scalability (scoring infra) | E-007 | REQ-020, REQ-021 | Must |
| F-014 | Resilience & integration guardrails | E-007 | REQ-023 | Must |
| F-015 | Security: encryption & key management | E-007 | REQ-022 | Must |

## Requirement Coverage

| Requirement ID | Covered By Feature | Epic |
|---|---|---|
| REQ-001 | F-001 | E-001 |
| REQ-002 | F-001 | E-001 |
| REQ-003 | F-002 | E-001 |
| REQ-004 | F-001 | E-001 |
| REQ-005 | F-003 | E-002 |
| REQ-006 | F-003 | E-002 |
| REQ-007 | F-004 | E-002 |
| REQ-008 | F-003 | E-002 |
| REQ-009 | F-003 | E-002 |
| REQ-010 | F-005 | E-003 |
| REQ-011 | F-006 | E-003 |
| REQ-012 | F-007 | E-004 |
| REQ-013 | F-007 | E-004 |
| REQ-014 | F-008 | E-005 |
| REQ-015 | F-009 | E-005 |
| REQ-016 | F-010 | E-006 |
| REQ-017 | F-010 | E-006 |
| REQ-018 | F-011 | E-007 |
| REQ-019 | F-012 | E-007 |
| REQ-020 | F-013 | E-007 |
| REQ-021 | F-013 | E-007 |
| REQ-022 | F-015 | E-007 |
| REQ-023 | F-014 | E-007 |
| REQ-024 | F-003 | E-002 |

*Note: The table below provides full source-requirement coverage (FR-### entries) mapped to features.*

| Requirement ID | Covered By Feature | Epic |
|---|---|---|
| FR-001 | F-001 | E-001 |
| FR-002 | F-001 | E-001 |
| FR-003 | F-002 | E-001 |
| FR-004 | F-002 | E-001 |
| FR-005 | F-001 | E-001 |
| FR-006 | F-003 | E-002 |
| FR-007 | F-003 | E-002 |
| FR-008 | F-003 | E-002 |
| FR-009 | F-004 | E-002 |
| FR-010 | F-003 | E-002 |
| FR-011 | F-003 | E-002 |
| FR-012 | F-005 | E-003 |
| FR-013 | F-006 | E-003 |
| FR-014 | F-005 | E-003 |
| FR-015 | F-007 | E-004 |
| FR-016 | F-007 | E-004 |
| FR-017 | F-007 | E-004 |
| FR-018 | F-011 | E-007 |
| FR-019 | F-007 | E-004 |
| FR-020 | F-008 | E-005 |
| FR-021 | F-008 | E-005 |
| FR-022 | F-009 | E-005 |
| FR-023 | F-008 | E-005 |
| FR-024 | F-010 | E-006 |
| FR-025 | F-010 | E-006 |
| FR-026 | F-010 | E-006 |
| FR-027 | F-010 | E-006 |
| FR-028 | F-011 | E-007 |
| FR-029 | F-012 | E-007 |
| FR-030 | F-012 | E-007 |

## Epic Dependency Summary

| Epic | Depends On | Risk |
|---|---|---|
| E-002 | E-001 | Medium-High (depends on submission pipeline) |
| E-003 | E-002 | High (compliance requires scoring and data) |
| E-004 | E-002, E-003 | Medium |
| E-005 | E-003 | Medium |
| E-006 | E-005 | High |

---
*Set Status: Draft. Every requirement from `atomic-requirements.md` must be included in the full coverage table before readiness.*
## Non-Functional Requirements Mapping (canonical REQ references)

| REQ ID | Covered By Feature | Epic |
|---|---|---|
| REQ-020 | F-013 | E-007 |
| REQ-021 | F-013 | E-007 |
| REQ-022 | F-015 | E-007 |
| REQ-018 | F-011 | E-007 |
| REQ-021 | F-013 | E-007 |
| REQ-023 | F-014 | E-007 |

## Non-Functional Requirements Mapping (canonical REQ references)

| REQ ID | Covered By Feature | Epic |
|---|---|---|
| REQ-020 | F-013 | E-007 |
| REQ-021 | F-013 | E-007 |
| REQ-022 | F-015 | E-007 |
| REQ-018 | F-011 | E-007 |
| REQ-021 | F-013 | E-007 |
| REQ-023 | F-014 | E-007 |

