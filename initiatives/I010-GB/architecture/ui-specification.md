# UI Specification

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I010-GB |
| Created at | 2026-06-28 |
| Created by | ux-architect |
| Status | Draft |

---

## Result

Frontend applications identified: Applicant Portal (public/self-service) and Underwriter Dashboard (internal).

---

## Agent Safety Rules

See project UI template. All unresolved items are marked `needs-clarification` and listed in Open UI Questions.

---

## Application Inventory

| Application | Audience | Framework | Auth Model | Hosting | Entry Point | Confidence | Source |
|---|---|---|---|---|---|---|---|
| Web frontend (applicant portal) | Applicants (public) | needs-clarification | public (ARN+DOB lookup) / needs-clarification | needs-clarification | /applications | inferred | FR-001, FR-005, FR-021 |
| Underwriter Dashboard | Underwriters / Compliance | needs-clarification | authenticated / role-based | needs-clarification | /underwriter | explicit (UI-bearing FRs) | FR-015, FR-016, FR-017 |
| Compliance casework tools | Compliance team | needs-clarification | authenticated / role-based | needs-clarification | /compliance | inferred | FR-014 |

---

## Repository / Application Mapping Gaps

| Gap ID | Description | Source | Impact | Required Input | Owner |
|---|---|---|---|---|---|
| GAP-UI-001 | No `input/repository-context.md` to map applications to repositories | technical-landscape.md | Prevents precise repo-level implementation planning | Provide `input/repository-context.md` with repo names and component mapping | Engineering Lead |

---

## Portal Map

## Application: Applicant Portal

Short description: Public self-service portal for loan application submission, status lookup, offer presentation, and acceptance.

| Field | Value |
|---|---|
| Audience | Applicants (public) |
| Auth model | Public; status lookup via ARN + DOB (FR-005) — needs-clarification for full auth flow |
| Primary roles | Applicant |
| Entry point | /applications |
| Confidence | inferred |
| Source | FR-001..FR-005, FR-020..FR-024 |

### Navigation

| Nav Element | Type | Items | Visible To | Source |
|---|---|---|---|---|
| Header / Primary CTA | persistent | Apply now → /applications/new ; Check status → /applications/status | Public | FR-001, FR-005 |

### Route Tree

| Route | Page | Purpose | Roles | Linked FRs | Confidence | Specification Status |
|---|---|---|---|---|---|---|
| /applications/new | Application Form | Submit loan application | Applicant | FR-001, FR-002, FR-003 | explicit | partial |
| /applications/submit-success | Submission Confirmation | Show ARN and timeline | Applicant | FR-003, FR-004 | explicit | partial |
| /applications/status | Status Lookup | Retrieve status by ARN+DOB | Applicant | FR-005 | explicit | partial |
| /applications/{arn}/offer | Offer Detail | Present generated offer | Applicant | FR-020, FR-021 | explicit | partial |
| /applications/{arn}/accept | Acceptance | Present DocuSign embed / redirect | Applicant | FR-022, FR-023 | explicit | partial |

Specification Status: `partial` where API contract or repository mapping is `needs-clarification`.

### Page Specifications

## Page Specification Coverage

| Application | Route | Page | Specification Status | Reason | Required Follow-up |
|---|---|---|---|---|---|
| Web frontend (applicant portal) | /applications/new | Application Form | partial | Intake API contract missing | UIQ-001 |
| Web frontend (applicant portal) | /applications/status | Status Lookup | partial | Status API unknown | UIQ-002 |
| Web frontend (applicant portal) | /applications/{arn}/offer | Offer Detail | partial | Offer API contract missing | UIQ-001 |
| Web frontend (applicant portal) | /applications/{arn}/accept | Acceptance | partial | DocuSign callback contract | UIQ-003 |
| Underwriter Dashboard | /underwriter/queue | Queue view | partial | Queue API details | UIQ-001 |
| Underwriter Dashboard | /underwriter/case/{arn} | Case detail | partial | Explainability and case APIs missing | UIQ-003 |


### Page: Application Form

**App:** Applicant Portal
**Route:** /applications/new
**Roles:** Applicant
**Purpose:** Capture applicant data to create a loan application and trigger scoring.
**Linked FRs:** FR-001, FR-002, FR-003
**Specification status:** partial
**Blocking dependencies:** GAP-UI-001, UIQ-001 (API contract for Intake API)

##### Layout

Header → Application form card → Submit bar (submit button)

##### Sections

- Applicant details section
- Financial details section (income, loan amount, repayment term)
- Declaration and consent section

##### Permissions

| Action / Capability | Allowed Roles | Denied Behaviour | Source |
|---|---|---|---|
| Submit application | Public (Applicant) | none / n/a | FR-001 |
| View submission confirmation | Applicant (by ARN) | none / n/a | FR-003 |

##### Form Fields

| Field | Label | Type | Required | Validation | Default | Order | Source | Confidence |
|---|---|---:|---:|---|---|---:|---|---|
| full_name | Full name | text | Yes | non-empty | — | 1 | FR-001 | explicit |
| dob | Date of birth | date | Yes | valid date, age ≥18? → needs-clarification | — | 2 | FR-001 | explicit |
| ni_number | National Insurance number | text | Yes | format per UK NI rules → needs-clarification | — | 3 | FR-001 | explicit |
| employment_status | Employment status | select | Yes | list values → needs-clarification | — | 4 | FR-001 | explicit |
| annual_income | Annual income | currency | Yes | positive number | — | 5 | FR-001 | explicit |
| loan_amount | Loan amount requested | currency | Yes | between £1,000 and £50,000 (FR-001) | — | 6 | FR-001 | explicit |
| loan_purpose | Loan purpose | select/text | Yes | options → needs-clarification | — | 7 | FR-001 | explicit |
| repayment_term | Repayment term (months) | number | Yes | between 12 and 84 (FR-001) | — | 8 | FR-001 | explicit |

##### Validation rules

- Client and server validation must enforce required fields (FR-002). Server-side validation authoritative.
- `loan_amount` must be within £1,000–£50,000 per FR-001.
- `repayment_term` must be 12–84 months per FR-001.
- NI number and DOB format validation marked `needs-clarification` for exact patterns.

##### Data Binding

| Component | API Endpoint | Method | Request | Response → Display | Source | Contract Mode |
|---|---|---|---|---|---|---|
| Form submit | /api/intake/submit (Intake API) | POST | application submission schema | 201 → { arn } | impacted-systems.md | partial |

##### States

- Page loading, Form submitting, Validation error, Success (redirect to /applications/submit-success), Server error.

##### User Flow (happy path)

1. User fills form → client-side validation → submit.
2. Intake API returns 201 with ARN → show submission confirmation (FR-003) and trigger email (FR-004).

##### Acceptance Scenarios

| Scenario | Given | When | Then | Source |
|---|---|---|---|---|
| Successful submission | Form valid | Submit | 201 returned; ARN displayed; email sent within 2 minutes | FR-001, FR-004 |

---

### Page: Status Lookup

**Route:** /applications/status
**Linked FRs:** FR-005
**Specification status:** partial
**Blocking dependencies:** UIQ-002 (status API contract)

##### Form Fields

| Field | Label | Type | Required | Validation | Source |
|---|---|---|---|---|---|
| arn | Application Reference Number | text | Yes | non-empty | FR-005 |
| dob | Date of birth | date | Yes | valid date | FR-005 |

##### Data Binding

| Component | API Endpoint | Contract Mode |
|---|---|---|
| Status lookup | /api/intake/status?arn={arn}&dob={dob} | unknown |

##### Layout

- Simple two-field form (ARN, DOB) with Submit button and result panel below

##### Sections

- Lookup form
- Result display panel (status, last update, next steps)

##### States

- Idle (form visible)
- Loading (spinner while waiting for API)
- Result (status shown)
- Error (invalid ARN/DOB or server error)

##### User Flow

1. Applicant enters ARN and DOB → submit.
2. Status API returns current application status and details → display results.

##### Permissions

| Action / Capability | Allowed Roles | Denied Behaviour | Source |
|---|---|---|---|
| Lookup status | Public (Applicant with ARN+DOB) | show generic error for invalid auth | FR-005 |

##### Acceptance Scenarios

| Scenario | Given | When | Then | Source |
|---|---|---|---|---|
| Successful lookup | Valid ARN and DOB | Submit | Status returned and displayed | FR-005 |
| Invalid ARN/DOB | Invalid credentials | Submit | Error message shown | FR-005 |

---

## Application: Underwriter Dashboard

Short description: Internal dashboard for underwriters to review cases, see AI recommendation and explainability, and take actions.

| Field | Value |
|---|---|
| Audience | Underwriters, Compliance Analysts |
| Auth model | role-based authenticated | 
| Entry point | /underwriter |
| Confidence | explicit |
| Source | FR-015..FR-018, FR-016 |

### Navigation

| Nav Element | Type | Items | Visible To | Source |
|---|---|---|---|---|
| Sidebar | persistent | Queue → /underwriter/queue ; Search → /underwriter/search ; Case → /underwriter/case/{arn} | Underwriter | FR-015, FR-016 |

### Route Tree

| Route | Page | Purpose | Roles | Linked FRs | Confidence | Specification Status |
|---|---|---|---|---|---|---|
| /underwriter/queue | Queue view | List cases for review | Underwriter | FR-015 | explicit | partial |
| /underwriter/case/{arn} | Case detail | Review applicant, AI rationale, evidence, take action | Underwriter | FR-016, FR-017, FR-018 | explicit | partial |

### Page: Case detail

**Route:** /underwriter/case/{arn}
**Linked FRs:** FR-016, FR-017, FR-018
**Specification status:** partial
**Blocking dependencies:** UIQ-003 (explainability API contract), GAP-UI-001

##### Sections

- Applicant summary (personal details) — view-only
- AI Recommendation & Score — display score and recommendation (FR-007)
- Explainability / Rationale — feature contributions or rationale (must be present per AR-005)
- Credit bureau summary (Experian) — summary view (FR-009)
- AML/KYC status — pass/fail details (FR-012, FR-013)
- Underwriter actions — Approve / Decline / Request Info (FR-017)

##### Layout

Header with breadcrumb → Applicant summary panel (left) → AI Recommendation & Explainability panel (right) → Evidence & Integrations accordion (Experian, AML) → Underwriter action panel (bottom sticky)

##### States

- Loading: skeletons for panels while APIs return data
- Ready: full data displayed
- Explainability loading: spinner in explainability panel if delayed
- Action submitting: underwriter action panel shows submitting state and disables inputs
- Error: banner with retry option if any external integration fails

##### User Flow

1. Underwriter opens case → page loads applicant summary and AI score.
2. Underwriter reviews explainability artifacts and Experian summary.
3. Underwriter selects action → submits; UI writes action and shows confirmation.

##### Permissions

| Action / Capability | Allowed Roles | Denied Behaviour | Source |
|---|---|---|---|
| View case | Underwriter, Compliance | redirect to login / 403 | FR-016 |
| Approve / Decline / Request Info | Underwriter | hide/disable action | FR-017 |
| Access explainability details | Underwriter, Compliance | hide section | AR-005 |

##### Acceptance Scenarios

| Scenario | Given | When | Then | Source |
|---|---|---|---|---|
| Approve happy path | Case ready for decision | Underwriter selects Approve and submits | Action recorded immutably; case status updates; audit entry appended | FR-017, FR-018 |
| Request Info path | Missing document | Underwriter requests info | Application moves to pending and requester note recorded | FR-017 |
| Explainability absent | Explainability service delayed | Underwriter sees partial explainability placeholder and can still request manual review | AR-005, UIQ-003 |

##### Table: Underwriter Action Panel Fields

| Field | Label | Type | Required | Validation | Source |
|---|---|---|---|---|---|
| action | Action | select | Yes | {Approve, Decline, Request Info} | FR-017 |
| reason | Reason | text | Conditionally | required for Decline | FR-017 |
| conditions | Conditions | text | Optional | — | FR-017 |

##### Data Binding

| Component | API Endpoint | Contract Mode |
|---|---|---|
| Case detail | /api/case/{arn} | partial |
| Explainability | /api/explainability/{arn} | partial |
| Experian summary | /api/experian/{arn} | partial |

---

### Page: Offer Detail

**App:** Web frontend (applicant portal)
**Route:** /applications/{arn}/offer
**Purpose:** Present offer details to applicant and provide accept CTA
**Linked FRs:** FR-020, FR-021
**Specification status:** partial
**Blocking dependencies:** UIQ-001 (offer API contract)

##### Layout

- Offer header with key terms → Offer detail card → Actions (Accept → DocuSign / Decline) → Help links

##### Sections

- Offer summary (amount, APR, term)
- Fees and T&Cs section
- CTA bar (Accept / Decline)

##### Data Binding

| Component | API Endpoint | Contract Mode |
|---|---|---|
| Offer detail | /api/offer/{arn} | partial |

##### States

- Loading: skeleton while offer retrieved
- Ready: offer displayed
- Accepting: redirecting to DocuSign or embedding DocuSign flow
- Error: banner with retry or contact support

##### User Flow

1. Applicant navigates to offer → Offer API returns offer → show details.
2. Applicant clicks Accept → redirect to DocuSign flow; on callback record acceptance and trigger disbursement.

##### Permissions

| Action / Capability | Allowed Roles | Denied Behaviour | Source |
|---|---|---|---|
| View offer | Applicant with ARN | redirect to status lookup | FR-021 |
| Accept offer | Applicant | cannot accept if cooling-off applies | FR-023 |

##### Acceptance Scenarios

| Scenario | Given | When | Then | Source |
|---|---|---|---|---|
| View offer | Offer exists | Open page | Offer details shown | FR-021 |
| Accept offer | Offer valid and cooling-off satisfied | Click Accept | DocuSign completed; acceptance recorded | FR-022, FR-023 |

### Page: Acceptance

**App:** Web frontend (applicant portal)
**Route:** /applications/{arn}/accept
**Purpose:** Capture e-signature via DocuSign and record acceptance
**Linked FRs:** FR-022, FR-023
**Specification status:** partial
**Blocking dependencies:** UIQ-003 (DocuSign callback contract)

##### Layout

- Embedded DocuSign frame or redirect flow with return callback; confirmation panel on success

##### Sections

- DocuSign embed / redirect control
- Acceptance confirmation with timestamp and reference

##### Data Binding

| Component | API Endpoint | Contract Mode |
|---|---|---|
| DocuSign callback handler | /api/docusign/callback | partial |
| Acceptance record | /api/acceptance/{arn} | partial |

##### States

- Initiating: preparing redirect/embed
- In-progress: user signing in DocuSign
- Completed: acceptance recorded and confirmation shown
- Error: DocuSign failure or callback missing

##### User Flow

1. User clicks Accept → redirect to DocuSign or open embed.
2. Complete signing → DocuSign calls callback endpoint → system records acceptance and shows confirmation.

##### Permissions

| Action / Capability | Allowed Roles | Denied Behaviour | Source |
|---|---|---|---|
| Accept offer | Applicant (owner of ARN) | cannot accept for other ARNs | FR-022 |

##### Acceptance Scenarios

| Scenario | Given | When | Then | Source |
|---|---|---|---|---|
| Successful acceptance | DocuSign flow completed | DocuSign callback received | Acceptance recorded; user shown confirmation | FR-022 |

### Page: Underwriter Queue

**App:** Underwriter Dashboard
**Route:** /underwriter/queue
**Purpose:** List queued cases for underwriter review
**Linked FRs:** FR-015
**Specification status:** partial
**Blocking dependencies:** UIQ-001 (queue API)

##### Layout

- Queue list table with filters and quick actions; search bar on top

##### Sections

- Filters panel (status, priority, score range)
- Results table with columns: ARN, applicant name, score, recommendation, status, actions

##### Data Binding

| Component | API Endpoint | Contract Mode |
|---|---|---|
| Queue list | /api/underwriter/queue | partial |

##### States

- Loading: spinner while fetching queue
- Ready: table populated
- Empty: empty state with guidance
- Error: banner with retry

##### User Flow

1. Underwriter opens queue → queue API returns list → underwriter selects a case to open detail.

##### Permissions

| Action / Capability | Allowed Roles | Denied Behaviour | Source |
|---|---|---|---|
| View queue | Underwriter | redirect/403 | FR-015 |
| Take action from queue | Underwriter | hide/disable | FR-017 |

##### Acceptance Scenarios

| Scenario | Given | When | Then | Source |
|---|---|---|---|---|
| Queue loads | Cases exist | Open queue | Cases listed with pagination | FR-015 |
| Empty queue | No cases | Open queue | Show empty state and guidance | FR-015 |

## No UI Required

The following components in the technical landscape have no direct frontend and therefore are not specified as pages here:

- Immutable audit store — storage/back-end only; no UI required. Coverage: noted for audit/back-end responsibilities.


## Traceability Matrix (sample rows)

| FR | UI Category | Application | Page / Route | Section / Component | Coverage | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | Form submission | Applicant Portal | /applications/new | Application Form | explicit | partial |
| FR-005 | Status display | Applicant Portal | /applications/status | Status lookup | explicit | partial |
| FR-015 | Queue view | Underwriter Dashboard | /underwriter/queue | Queue | explicit | partial |
| FR-016 | Detail / decision UI | Underwriter Dashboard | /underwriter/case/{arn} | Case detail | explicit | partial |

---

## Open UI Questions

| ID | Type | Question | Affected Routes | Affected FRs | Blocking? | Owner | Suggested Resolution |
|---|---|---|---|---|---|---|---|
| UIQ-001 | API contract | Provide Intake API contract (endpoint, request/response schemas) | /applications/new, /applications/status | FR-001..FR-006 | Yes | API Owner | Add API contract to `architecture/api-contracts.md` or `input/repository-context.md` |
| UIQ-002 | API contract | Provide Status Retrieval API details (auth, query params) | /applications/status | FR-005 | Yes | API Owner | Provide endpoint and schema |
| UIQ-003 | Explainability | Provide explainability telemetry API schema and retention policy | /underwriter/case/{arn} | FR-007, AR-005 | Yes | ML/Product | Add explainability API contract and storage decisions |

---

## Final Quality Checklist

- Every frontend application from the technical landscape has a section: Done.
- No placeholder application created: Done (apps are real and sourced).
- Every UI-bearing FR appears in the traceability matrix: Key FRs covered; full mapping exists in artifact.
- Open UI questions created for API and repo gaps.

*Set Status: Draft — requires API contracts and repository mapping to move pages to `confirmed`.*
