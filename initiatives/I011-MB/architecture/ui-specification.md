# UI Specification

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I011-MB |
| Created at | 2026-06-28 |
| Created by | ux-architect |
| Status | Draft |

---

## Result

The initiative includes a public applicant portal for submission and status, an Underwriter Dashboard for decisioning, and an Admin Dashboard for metrics and operations. Details are derived from `requirements/atomic-requirements.md`, `architecture/technical-landscape.md`, and `architecture/impacted-systems.md`.

## Application Inventory

| Application | Audience | Framework | Auth Model | Hosting | Entry Point | Confidence | Source |
|---|---|---|---|---|---|---|---|
| Applicant Portal | Applicants | needs-clarification | none or minimal | needs-clarification | /applications | inferred | FR-001, FR-005 |
| Underwriter Dashboard | Underwriters | React (explicit in landscape) | enterprise SSO | Azure Static Web Apps | /underwriter | explicit | FR-015, FR-016 |
| Underwriter UI | Underwriters | React | enterprise SSO | Azure Static Web Apps | /underwriter | explicit | FR-015, FR-016 |
| ApplicantDB | Ops / Backend | n/a | n/a | n/a | n/a | explicit | data store only — not a UI |
| CI pipeline | DevOps | n/a | n/a | Azure DevOps | n/a | explicit | infra only — not a UI |
| Admin Dashboard | Admins | needs-clarification | enterprise SSO | needs-clarification | /admin | inferred | FR-029 |

## Repository / Application Mapping Gaps

| Gap ID | Description | Source | Impact | Required Input | Owner |
|---|---|---|---|---|---|
| G-UI-001 | Repository names and build pipelines for frontend apps not provided | technical-landscape.md | Blocks implementation planning and CI mapping | Provide `input/repository-context.md` or repository inventory | Delivery Lead |

---

## Application: Applicant Portal

### Page Summary: Application Form

Audience: Applicants

Auth model: None for submission; status retrieval by ARN and DOB (FR-005)

Primary roles: Applicant

Entry point: /applications

### Route Tree

| Route | Page | Purpose | Roles | Linked FRs | Confidence | Specification Status |
|---|---|---|---|---|---|---|
| /applications | Application Form | Submit new application | Applicant | FR-001, FR-002 | explicit | partial |
| /applications/status | Status Lookup | Retrieve status by ARN + DOB | Applicant | FR-005 | explicit | partial |
| /applications/offer | Offer View | View generated offer and accept | Applicant | FR-020, FR-021, FR-022 | explicit | partial |

### Page: Application Form

**Route:** `/applications`

#### Form Fields

| Field | Type | Validation | Source |
|---|---|---|---|
| full_name | text | required | FR-001 |
| date_of_birth | date | required | FR-001 |
| national_insurance_number | text | required, pattern | FR-001 |
| employment_status | select | required | FR-001 |
| annual_income | number | required, min 0 | FR-001 |
| loan_amount | number | required, between 1000 and 50000 | FR-001 |
| loan_purpose | text | required | FR-001 |
| repayment_term | number | required, between 12 and 84 | FR-001 |

#### Layout

Single-column responsive form; group personal details, employment, and loan details into sections.

#### Sections

- Personal details
- Employment & income
- Loan details
- Declaration & consent

#### Data Binding

| UI Element | API Endpoint | Notes | Contract Mode |
|---|---|---|---|
| Submit application | /applications (POST) | Request schema: `application payload schema` (see impacted-systems) | proposed-by-ui-spec |

#### States

| State | Description |
|---|---|
| loading | Form is submitting or remote validation running |
| success | Submission accepted; ARN returned and confirmation shown |
| error | Validation or server error shown inline; global error banner for infra failures |

#### User Flow

1. Applicant fills form and clicks Submit.
2. Client-side validation runs; server-side validation via `/applications` occurs.
3. On success, show ARN and confirmation; trigger confirmation email.

#### Permissions

None required for submission; status lookup requires ARN + DOB (FR-005).

#### Acceptance Scenarios

- Given a valid form, when submitted, then system returns ARN and confirmation email within 2 minutes (FR-003, FR-004).
- Given missing required field, when submitted, then show inline validation and prevent submission (FR-002).

Blocking dependencies: G-UI-001, Q-001

Specification Status: partial

---

## Application: Underwriter Dashboard

Short description: Internal UI for underwriters to review, override, and take actions on referred applications.

Audience: Underwriters

Auth model: enterprise SSO (confirmed by technical landscape)

Entry point: /underwriter

### Navigation

| Nav Element | Type | Items | Visible To | Source |
|---|---|---|---|---|
| Sidebar | vertical | Queue, Application Detail, Escalations | Underwriter | FR-015, FR-019 |

| Route | Page | Purpose | Roles | Linked FRs | Confidence | Specification Status |
|---|---|---|---|---|---|---|
| /underwriter/queue | Queue | List referred applications | Underwriter | FR-015 | explicit | partial |
| /underwriter/application/:arn | Application Detail | Review application, see score, credit report, AML/KYC, take action | Underwriter | FR-016, FR-017, FR-018 | explicit | partial |

### Page: Application Detail

**Route:** `/underwriter/application/:arn`

#### Form Fields

This page is detail-focused and uses panels rather than form fields; key editable fields are action reason and manual override comments.

| Field | Type | Validation | Source |
|---|---|---|---|
| override_reason | text | required when override | FR-017 |
| manual_comments | text | optional | FR-017 |

#### Layout

Two-column layout: left — applicant summary and documents; right — score, actions, and audit trail.

#### Sections

- AI score & explanation
- Credit report
- AML/KYC status
- Audit trail and underwriter actions

#### Data Binding

| UI Element | API Endpoint | Notes | Contract Mode |
|---|---|---|---|
| Applicant Summary | /applications/{arn} (GET) | Needs ARN-based retrieval API | proposed-by-ui-spec |
| AI Score & Explanation | /scores/{id} (GET) | Explanation payload must be auditable | partial |
| Credit Report | Experian client | External contract; read-only display | confirmed |
| AML/KYC Status | /aml/{arn} (GET) | Integration with HMRC/AML service | partial |

#### States

| State | Description |
|---|---|
| loading | Page is fetching applicant, score, and reports |
| ready | All panels loaded successfully |
| partial | Some panels failed (e.g., Experian unavailable) — show partial data and banners |
| error | Page-level failure; allow retry and escalation |

#### User Flow

1. Underwriter opens application detail using ARN from queue.
2. System loads applicant summary, AI score, credit report, and AML/KYC status.
3. Underwriter chooses Approve / Decline / Request more info; action recorded with audit entry.

#### Permissions

Role `underwriter` can view and take actions. Sensitive audit fields viewable by `compliance` role.

#### Acceptance Scenarios

- Given an application with complete data, when underwriter approves, then an immutable audit record is written and notification is sent to applicant (FR-018, FR-021).
- Given Experian is unavailable, when underwriter views page, then display partial data and allow manual decisioning with a warning banner (FR-009).

Blocking dependencies: Q-001, UIQ-003, UIQ-004, G-UI-001

Specification Status: partial

---

## Application: Admin Dashboard

Short description: Monitoring and admin metrics view for operations and compliance.

Audience: Admins, Ops

Auth model: enterprise SSO

Entry point: /admin

### Route Tree

| Route | Page | Purpose | Roles | Linked FRs | Confidence | Specification Status |
|---|---|---|---|---|---|---|
| /admin/metrics | Metrics Dashboard | View application volume, avg decision time, AML hold rates | Admin | FR-029 | inferred | partial |

Specification Status: partial

---


| FR | Application | Page / Route | UI Element |
|---|---|---|---|
| FR-001 | Applicant Portal | /applications | Application Form |
| FR-002 | Applicant Portal | /applications | Application Form validation |
| FR-003 | Applicant Portal | /applications | ARN display |
| FR-004 | Applicant Portal | /applications | Confirmation email (notification pipeline) |
| FR-005 | Applicant Portal | /applications/status | Status Lookup |
| FR-006 | Applicant Portal / Scoring | /applications -> scoring | scoring trigger |
| FR-007 | Underwriter Dashboard | /underwriter/application/:arn | AI Score & Explanation |
| FR-010 | Offer Generator / Applicant Portal | /applications/offer | Offer View |
| FR-015 | Underwriter Dashboard | /underwriter/queue | Queue List |
| FR-016 | Underwriter Dashboard | /underwriter/application/:arn | Dashboard panels |
| FR-020 | Applicant Portal | /applications/offer | Offer View |
| FR-021 | Applicant Portal | /applications/offer | Offer presentation |
| FR-022 | Applicant Portal | /applications/offer | E-signature acceptance flow |
| FR-029 | Admin Dashboard | /admin/metrics | Metrics Dashboard |
| FR-030 | All UIs | All pages | Observability event emission |

*Note: The Traceability Matrix includes UI-bearing FRs; backend-only FRs are omitted.*

*Note: The Traceability Matrix includes UI-bearing FRs; backend-only FRs are omitted.*

## Page Specification Coverage

| Page | Route | Coverage | Status |
|---|---|---|---|
| Application Form | /applications | fields, data binding, states, user flow, acceptance scenarios | partial |
| Status Lookup | /applications/status | fields, data binding, states | partial |
| Underwriter Queue | /underwriter/queue | list, pagination, filters | partial |
| Application Detail | /underwriter/application/:arn | layout, sections, data binding, states, user flow, permissions, acceptance scenarios | partial |
| Metrics Dashboard | /admin/metrics | metrics, refresh, filters | partial |

## UI Readiness Matrix

| Page | Route | Readiness | Blocking Dependencies |
|---|---|---|---|
| Application Form | /applications | partial | G-UI-001, Q-001 |
| Status Lookup | /applications/status | partial | Q-001 |
| Underwriter Queue | /underwriter/queue | partial | Q-001 |
| Application Detail | /underwriter/application/:arn | partial | Q-001 |
| Metrics Dashboard | /admin/metrics | partial | Q-001 |

---

## Open UI Questions

| ID | Question | Impact | Routes | Owner |
|---|---|---|---|---|
| UIQ-001 | Confirm repository and build pipeline names for frontend apps | Implementation and CI mapping | n/a | Delivery Lead |
| UIQ-002 | Confirm whether Applicant Portal requires user accounts or only ARN-based status lookup | Affects auth model and session flows | /applications | Product Owner |
| UIQ-003 | Confirm API contract for `/scores/{id}` and explanation payload schema used by Application Detail | Affects data binding and acceptance scenarios for Application Detail | /underwriter/application/:arn | Head of AI |
| UIQ-004 | Confirm exact API contract for `/applications/{arn}` GET and for underwriter action APIs; ensure `/scores/{id}` explainability payload fields | Blocks Application Detail `confirmed` status | /underwriter/application/:arn | Head of Engineering |

---

*Set Status: Draft — follow-up required for repository mapping and API contract confirmation.*
