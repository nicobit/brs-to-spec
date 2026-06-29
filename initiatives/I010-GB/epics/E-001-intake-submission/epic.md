# E-001 — Intake & Submission

## Metadata

| Field | Value |
|---|---|
| Epic ID | E-001 |
| Initiative ID | I010-GB |
| Wave | Wave 1 |
| Priority | Must |
| Increment | D1 |
| Created at | 2026-06-28 |
| Created by | delivery-lead |
| Status | Draft |

---

## Business Objective

Provide a secure, validated public intake channel to capture applicant data, create an application record (ARN), and trigger downstream scoring and notification workflows. Delivering Intake enables all downstream decisioning, compliance, and disbursement flows; failure to deliver prevents any customer onboarding.

---

## Scope

**In scope:**
- Public application submission form and API endpoint to persist applications and return ARN.
- Submission confirmation and email notification.
- Status lookup API for applicants (ARN + DOB).

**Out of scope:**
- Offer generation and acceptance flows (covered by E-004).
- Underwriter UI and casework (covered by E-003).

---

## High-Level Acceptance Criteria

- AC-E-001: Applicants can submit a valid application and receive a 201 response with an ARN.
- AC-E-002: Applicant can lookup status by ARN+DOB and receive current application status.
- AC-E-003: Submission triggers a scoring request and an email confirmation within configured SLA.

---

## Source Traceability

| Source | Reference | Notes |
|---|---|---|
| BRS | §Application Intake | Intake fields and validation rules originate from the BRS and FR-001..FR-005 |
| Requirement | FR-001 | Loan application submission |
| Requirement | FR-002 | Inline validation before submission |
| Requirement | FR-003 | Assign Application Reference Number (ARN) |
| Requirement | FR-004 | Email confirmation within 2 minutes |
| Requirement | FR-005 | Retrieve status by ARN and DOB |
| Non-functional | NFR-001 | Intake form load time ≤2s |
| Constraint | ARCH-C-001 | UK data residency for stored PII |

---

## Impacted Systems

| System / Module | Change Type | Notes |
|---|---|---|
| Applicant Portal (frontend) | Integration | New submission UI and status lookup routes; partial spec in UI spec. |
| Intake API | New | New service for ingesting applications and returning ARN. |
| Scoring pipeline | Integration | Will receive submission events for decisioning (E-002). |
| Email subsystem | Integration | Send submission confirmation (FR-004). |

---

## Dependencies

| Dependency | Type | Blocking? | Notes |
|---|---|---|---|
| E-005 (Platform & Observability) | Epic | No | Audit store and monitoring must be available for production rollout but not required for initial POC. |
| Experian adapter | External | No | Optional downstream credit enrichment for scoring; not blocking intake. |

---

## Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Missing repository mapping (GAP-UI-001) prevents CI scaffolding | Medium | Medium | Provide `input/repository-context.md` early; prototype using mono-repo default. |
| Data residency violation if storage configured outside UK | Low | High | Ensure hosting and storage default to UK-region environments per ARCH-C-001. |

---

## Foundation / Setup

Provision Intake API service scaffolding, CI pipeline, and a staging environment with UK-region data storage. Configure test harnesses and mock adapters for scoring and email to allow end-to-end validation without real vendor contracts.

---

## Stories

| Story ID | Title | Layers | Priority | Increment | Readiness |
|---|---|---|---|---|---|
| S-001.0 | Intake end-to-end POC | frontend / backend / infrastructure / integration | Must | D1 | Not Ready |
| S-001.1 | Application form UI | Frontend | Must | D1 | Not Ready |
| S-001.2 | Intake API: submit application | Backend API | Must | D1 | Not Ready |
| S-001.3 | ARN generation and persistence | Backend API | Must | D1 | Not Ready |
| S-001.4 | Status lookup API | Backend API | Must | D1 | Not Ready |
| S-001.5 | Confirmation email integration | Integrations | Must | D1 | Not Ready |
| S-001.6 | CI/CD and infra provisioning | Infrastructure | Must | D1 | Not Ready |

---

## Advisory Reviews

*Status: Draft — set to Accepted only after epic review gate.*
