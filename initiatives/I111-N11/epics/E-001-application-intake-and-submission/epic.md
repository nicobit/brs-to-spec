# E-001 — Application Intake and Submission

## Metadata

| Field | Value |
|---|---|
| Epic ID | E-001 |
| Initiative ID | I111-N11 |
| Wave | Wave 1 |
| Priority | Must |
| Increment | D1 |
| Created at | 2026-06-22 |
| Created by | delivery-lead |
| Status | Draft |

---

## Business Objective

Enable applicants to submit complete applications through the applicant portal, validate required identity and contact details, and emit a canonical submission event (ARN) for downstream processing. Early delivery reduces manual intake and improves processing SLAs.

---

## Scope

**In scope:**
- Applicant submission form (web) with validation, document upload, and submission confirmation.

**Out of scope:**
- Underwriter decisioning and offer generation (handled in separate epics).

---

## High-Level Acceptance Criteria

- AC-E-001: Applicants can submit an application and receive a confirmation ARN within 30 seconds.
- AC-E-002: Submission payload conforms to the event contract required by scoring and compliance services.

---

## Source Traceability

| Source | Reference | Notes |
|---|---|---|
| BRS | input/brs.md | Applicant flow and data fields |
| Requirement | REQ-001, REQ-002, REQ-003, REQ-004 | See stories for trace links |

---

## Impacted Systems

| System / Module | Change Type | Notes |
|---|---|---|
| Applicant Portal | New | React frontend, new forms and file upload |
| Loan Origination API | Changed | New submission endpoint, validation rules |
| Event Bus (Service Bus) | Integration | Publish `application.submitted` domain event |

---

## Dependencies

| Dependency | Type | Blocking? | Notes |
|---|---|---|---|
| E-007 Observability | Epic | No | CorrelationId and audit patterns must be integrated |

---

## Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Missing required identity fields from applicants | Medium | Medium | Surface field-level validation and guidance; capture as open questions in stories |

---

## Foundation / Setup

Provision frontend static app, backend API scaffold, and event bus topic for `application.submitted`. Configure UK-only storage for uploaded documents.

---

## Stories

| Story ID | Title | Layers | Priority | Increment | Readiness |
|---|---|---|---|---|---|
| F-001.1 | Applicant submission form | Frontend / Backend / Integration | Must | D1 | Ready |
| F-001.2 | Submission confirmation and email | Backend / Integration / Infrastructure | Must | D1 | Ready |
| F-001.3 | Validation and ARN status retrieval | Backend / API / Infrastructure | Must | D1 | Ready |

---
*Status: Draft — set to Accepted only after epic review gate.*
