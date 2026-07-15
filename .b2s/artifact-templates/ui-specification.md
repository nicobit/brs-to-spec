# UI Specification

## Metadata

| Field         | Value             |
| ------------- | ----------------- |
| Initiative ID | {{initiative_id}} |
| Created at    | {{date}}          |
| Created by    | ux-architect      |
| Status        | Draft             |

---

## Result

{{UI specification result summary. Use "Frontend applications identified" or "No frontend applications identified".}}

{{If no frontend applications are identified, explain why and stop after this section.}}

---

## Agent Safety Rules

- Do not invent routes, fields, auth logic, API contracts, or status values.
- If information is unresolved, emit `needs-clarification` and create an open UI question.
- Do not mark any page as `confirmed` unless its route guard, API contract mode, fields, states, and success/error navigation are all fully specified and no blocking open questions reference it.
- Pages with status `partial` or `blocked` have unresolved dependencies listed in their `Blocking dependencies` field. These must be resolved before the page can be treated as implementation scope. Resolution happens when the epic containing the page enters active elaboration.
- Open UI questions may block different stages. Use `Required Before` to distinguish initiative-blocking questions (`delivery-planning`) from deferred implementation-detail blockers (`epic-elaboration` or `coding-handoff`).

---

## Canonical Ownership Note

This artifact is the canonical initiative-level source for UI structure and behavior.

Downstream artifacts may scope or copy information from this document, but they must not silently redefine:

- routes
- page ownership
- fields
- validation rules
- guards and auth behavior
- states
- UI-to-API bindings

If later clarification changes one of these facts, the clarification must reference the original `UIQ-*` and remain traceable.

---

## Application Inventory

| Application  | Audience         | Framework                                             | Auth Model                                              | Hosting                                   | Entry Point           | Confidence                                | Source                                              |
| ------------ | ---------------- | ----------------------------------------------------- | ------------------------------------------------------- | ----------------------------------------- | --------------------- | ----------------------------------------- | --------------------------------------------------- |
| {{app name}} | {{user role(s)}} | {{React/Next.js/Angular/etc. or needs-clarification}} | {{public/authenticated/role-based/needs-clarification}} | {{hosting target or needs-clarification}} | {{main URL or route}} | {{explicit/inferred/needs-clarification}} | {{FR-NNN / technical-landscape / impacted-systems}} |

---

## Repository / Application Mapping Gaps

| Gap ID      | Description                                                    | Source              | Impact                                  | Required Input     | Owner     |
| ----------- | -------------------------------------------------------------- | ------------------- | --------------------------------------- | ------------------ | --------- |
| {{GAP-NNN}} | {{missing or unclear frontend application/repository mapping}} | {{source artifact}} | {{impact on UI spec or coding handoff}} | {{required input}} | {{owner}} |

If no gaps exist, write:

```text
No repository/application mapping gaps identified.
```

---

## Portal Map

*Repeat this section for each real frontend application.*

## Application: {{App Name}}

Short description: {{short description}}

| Field         | Value                                     |
| ------------- | ----------------------------------------- |
| Audience      | {{audience}}                              |
| Auth model    | {{auth model}}                            |
| Primary roles | {{roles}}                                 |
| Entry point   | {{entry point}}                           |
| Confidence    | {{explicit/inferred/needs-clarification}} |
| Source        | {{source artifact / FRs}}                 |

### Navigation: {{App Name}}

| Nav Element                         | Type                      | Items                                 | Visible To | Source                                      |
| ----------------------------------- | ------------------------- | ------------------------------------- | ---------- | ------------------------------------------- |
| {{header/sidebar/tabs/breadcrumbs}} | {{persistent/contextual}} | {{label → route, label → route, ...}} | {{roles}}  | {{FR-NNN / inferred / needs-clarification}} |

### Route Tree: {{App Name}}

| Route     | Page          | Purpose              | Roles                  | Linked FRs         | Confidence                                | Specification Status                   |
| --------- | ------------- | -------------------- | ---------------------- | ------------------ | ----------------------------------------- | -------------------------------------- |
| {{/path}} | {{Page Name}} | {{one-line purpose}} | {{All / Role1, Role2}} | {{FR-NNN, FR-NNN}} | {{explicit/inferred/needs-clarification}} | {{confirmed/inferred/partial/blocked}} |

Specification Status values:
- `confirmed` — all page details are fully specified and verified against inputs
- `inferred` — page details are derived from inputs but not explicitly confirmed
- `partial` — some required details are missing or marked needs-clarification
- `blocked` — a blocking dependency prevents specification

---

## Page Specification Coverage

| Application  | Route     | Page          | Specification Status                   | Reason                           | Required Follow-up       |
| ------------ | --------- | ------------- | -------------------------------------- | -------------------------------- | ------------------------ |
| {{App Name}} | {{/path}} | {{Page Name}} | {{confirmed/inferred/partial/blocked}} | {{why this status was assigned}} | {{required action or —}} |

Rules:

* Every route from every route tree must appear here.
* Every route marked `confirmed` must have a matching `### Page:` section below.
* No route may be omitted silently.
* A page may not be `confirmed` if it has blocking open questions, `unknown` contract modes, or unresolved auth.

---

## UI Readiness Matrix

*Every page from every route tree must appear here. This table is mandatory.*

| Page | Route | Specification Status | API Contract Mode | Auth Clarity | Blocking Dependencies | Ready for Story Generation? | Ready for Coding? | Blocking Reasons |
|---|---|---|---|---|---|---|---|---|
| {{Page Name}} | {{/path}} | {{confirmed/inferred/partial/blocked}} | {{confirmed/partial/proposed-by-ui-spec/mock/unknown}} | {{clear/partial/unknown}} | {{none or UIQ/GAP IDs}} | {{Yes/No}} | {{Yes/No}} | {{reason or —}} |

---

## Route Guards and Authorization

| Route Pattern        | Access Type                         | Allowed Roles    | Unauthenticated Behaviour                           | Unauthorized Behaviour                   | Verification Required                                    | Notes     |
| -------------------- | ----------------------------------- | ---------------- | --------------------------------------------------- | ---------------------------------------- | -------------------------------------------------------- | --------- |
| {{/path or /path/*}} | {{public/authenticated/role-based}} | {{roles or n/a}} | {{allow / redirect to login / needs-clarification}} | {{403 / access denied / hide nav / n/a}} | {{none / ARN+DOB / session / MFA / needs-clarification}} | {{notes}} |

---

## Shared Components

| Component          | Type                                                         | Used By Pages    | Props / Inputs  | States                                  | Source                 | Confidence            |
| ------------------ | ------------------------------------------------------------ | ---------------- | --------------- | --------------------------------------- | ---------------------- | --------------------- |
| {{component name}} | {{form/modal/table/card/stepper/alert/badge/timeline/chart}} | {{page1, page2}} | {{data inputs}} | {{loading/error/empty/active/disabled}} | {{FR-NNN / page spec}} | {{explicit/inferred}} |

---

## Page Specifications

*One section per route marked `confirmed` in the Page Specification Coverage table.*

For `confirmed` pages, provide full detail.
For `partial` or `blocked` pages, do not force full-detail sections where information is genuinely missing. Capture known facts, blockers, and required follow-up explicitly instead of inventing completeness.

---

### Page: {{Page Name}}

**App:** {{application}}
**Route:** {{/path}}
**Roles:** {{who can access}}
**Purpose:** {{what the user accomplishes on this page — 1-2 sentences}}
**Linked FRs:** {{FR-NNN, FR-NNN}}
**Entry points:** {{how the user arrives — nav item, link from another page, redirect}}
**Specification status:** {{confirmed/inferred/partial/blocked}}
**Blocking dependencies:** {{UIQ-NNN, GAP-NNN or "none"}}

#### Layout

{{Describe the page structure in implementation terms. Example: "Header with breadcrumb → search form card → results table → pagination bar" or "Wizard stepper → step content area → back/next action bar".}}

Do not define colors, spacing, typography, or branding.

#### Responsive Behaviour

| Breakpoint / Device | Behaviour                                   |
| ------------------- | ------------------------------------------- |
| Desktop             | {{layout behaviour}}                        |
| Tablet              | {{layout behaviour or needs-clarification}} |
| Mobile              | {{layout behaviour or needs-clarification}} |

#### Accessibility Requirements

| Area                    | Requirement                                                          |
| ----------------------- | -------------------------------------------------------------------- |
| Keyboard navigation     | {{tab order, actionable elements, shortcuts if any}}                 |
| Focus management        | {{focus on load, after errors, after modal close, after navigation}} |
| Error handling          | {{error summary, inline errors, screen reader announcement}}         |
| ARIA / semantics        | {{tables, badges, forms, timelines, modals}}                         |
| Screen reader behaviour | {{important announcements / labels}}                                 |
| Target standard         | {{WCAG 2.1 AA unless otherwise specified}}                           |

#### Sections

**Section: {{section name}}** — {{form / table / card-grid / detail-panel / chart / stepper / action-panel / timeline / document-viewer}}

##### Form Fields

| Field         | Label             | Type                                                     | Required   | Validation                               | Default          | Order | Source     | Confidence                                |
| ------------- | ----------------- | -------------------------------------------------------- | ---------- | ---------------------------------------- | ---------------- | ----- | ---------- | ----------------------------------------- |
| {{fieldName}} | {{Display Label}} | {{text/number/select/date/currency/checkbox/radio/file}} | {{Yes/No}} | {{concrete rule or needs-clarification}} | {{default or —}} | {{1}} | {{FR-NNN}} | {{explicit/inferred/needs-clarification}} |

##### Table Columns

| Column        | Label             | Type                                            | Sortable   | Filterable | Source     | Confidence                                |
| ------------- | ----------------- | ----------------------------------------------- | ---------- | ---------- | ---------- | ----------------------------------------- |
| {{fieldName}} | {{Display Label}} | {{text/date/currency/status-badge/action-link}} | {{Yes/No}} | {{Yes/No}} | {{FR-NNN}} | {{explicit/inferred/needs-clarification}} |

**Row actions:** {{view / edit / delete / approve — what each row can do}}
**Bulk actions:** {{bulk actions or n/a}}
**Pagination:** {{page size, infinite scroll, load-more, or needs-clarification}}
**Default sort:** {{default sort or needs-clarification}}
**Empty state:** {{empty state message and CTA}}

##### Actions

| Action ID    | Label             | Type                                                              | Trigger                                    | Condition        | Result                                           | Source     |
| ------------ | ----------------- | ----------------------------------------------------------------- | ------------------------------------------ | ---------------- | ------------------------------------------------ | ---------- |
| {{actionId}} | {{Display Label}} | {{primary/secondary/danger/link/icon/menu item/system-triggered}} | {{click / submit / change / system event}} | {{when enabled}} | {{API call / navigation / modal / state update}} | {{FR-NNN}} |

#### Data Binding

| Component / Section    | API Endpoint                           | Method                        | Request                           | Response → Display                     | Source                                                                          | Contract Status                                                | Contract Mode                              |
| ---------------------- | -------------------------------------- | ----------------------------- | --------------------------------- | -------------------------------------- | ------------------------------------------------------------------------------- | -------------------------------------------------------------- | ------------------------------------------ |
| {{section/form/table}} | {{/api/v1/resource or needs-contract}} | {{GET/POST/PUT/PATCH/DELETE}} | {{fields sent or needs-contract}} | {{fields displayed or needs-contract}} | {{impacted-systems / technical-landscape / solution-decisions / api-contracts}} | {{explicit-contract/partial-contract/needs-contract/inferred}} | {{confirmed/partial/mock/unknown}} |

Contract Mode values:
- `confirmed` — endpoint, request, and response schemas are fully defined in an API contract or impacted-systems artifact
- `partial` — endpoint exists but request/response details are incomplete
- `proposed-by-ui-spec` — endpoint path is proposed by this UI spec based on UI needs, but not confirmed by any API contract. Must be validated against the implementation contract before coding.
- `mock` — endpoint is assumed; implementation must use a mock/stub until the contract is provided
- `unknown` — no contract information available; must not be implemented against

Rules:

* Do not invent endpoints.
* Do not invent request or response schemas.
* If details are missing, use `needs-contract` for Contract Status and `unknown` or `mock` for Contract Mode.
* A page with any `unknown` Contract Mode binding must not be marked `confirmed`.

#### States

| State              | Trigger                             | Visual Behaviour                                                   | Data / API Dependency                     | Recovery / Next Action                      |
| ------------------ | ----------------------------------- | ------------------------------------------------------------------ | ----------------------------------------- | ------------------------------------------- |
| Page loading       | on mount / on navigation            | {{skeleton screen / spinner over content area}}                    | {{API dependency or n/a}}                 | {{wait / retry if timeout}}                 |
| Component loading  | component fetch / refresh           | {{component-level skeleton/spinner}}                               | {{API dependency or n/a}}                 | {{wait / retry}}                            |
| Form submitting    | on submit click                     | {{disable fields + submit button, show spinner on clicked button}} | {{API dependency}}                        | {{wait / cancel if applicable}}             |
| Validation error   | on blur per field / on submit       | {{inline error message, error summary, submit blocked}}            | {{client validation / server validation}} | {{user corrects field}}                     |
| Server error 4xx   | API returns 400/401/403/404/409/422 | {{inline field errors or banner}}                                  | {{API response}}                          | {{correct input / re-authenticate / retry}} |
| Server error 5xx   | API returns 500/503                 | {{error banner: "Something went wrong. Please try again."}}        | {{API response}}                          | {{retry}}                                   |
| Success            | API returns 200/201/204             | {{redirect / toast / confirmation modal / update page}}            | {{API response}}                          | {{next page or state}}                      |
| Empty              | no data to display                  | {{empty state message + CTA}}                                      | {{API response}}                          | {{CTA / adjust filters}}                    |
| Unauthorized       | not authenticated                   | {{redirect to login or verification}}                              | {{auth/session}}                          | {{login / verify}}                          |
| Forbidden          | authenticated but missing role      | {{403 / access denied / hide action}}                              | {{authz}}                                 | {{request access / go back}}                |
| Stale / refreshing | periodic refresh / manual refresh   | {{small spinner / last updated timestamp}}                         | {{API dependency}}                        | {{refresh complete / retry}}                |

Use `n/a` with reason for states that do not apply.

#### User Flow

| Step | User Action                 | System Response                               | Next State / Page   | Source     |
| ---- | --------------------------- | --------------------------------------------- | ------------------- | ---------- |
| 1    | {{user navigates to route}} | {{page loads}}                                | {{loading / ready}} | {{FR-NNN}} |
| 2    | {{user action}}             | {{system validates / calls API / updates UI}} | {{next state/page}} | {{FR-NNN}} |
| 3    | {{success or error action}} | {{system response}}                           | {{next state/page}} | {{FR-NNN}} |

Include happy path, important alternative paths, and important error paths.

#### Acceptance Scenarios

| Scenario | Given | When | Then | Source |
| -------- | ----- | ---- | ---- | ------ |
| {{short name}} | {{precondition}} | {{user action}} | {{expected outcome}} | {{FR-NNN}} |

Rules:
* 3-5 scenarios per page maximum — happy path, key alternative, key error.
* Do not duplicate full QA acceptance criteria — keep lightweight.
* Every scenario must trace to a linked FR.

#### Permissions

| Action / Capability                   | Allowed Roles             | Denied Behaviour                    | Source                  |
| ------------------------------------- | ------------------------- | ----------------------------------- | ----------------------- |
| {{view page}}                         | {{Role1, Role2 / Public}} | {{redirect / 403 / hide nav / n/a}} | {{FR-NNN / auth model}} |
| {{submit form}}                       | {{Role1 / Public}}        | {{button hidden / disabled / n/a}}  | {{FR-NNN}}              |
| {{approve / decline / export / edit}} | {{Role}}                  | {{button hidden / 403}}             | {{FR-NNN}}              |

---

*Repeat `### Page:` for every route marked `confirmed`.*

---

## UI vs Backend Responsibilities

| Requirement / Capability | UI Responsibility    | Backend / System Responsibility | UI Trigger / Display                 | Source     |
| ------------------------ | -------------------- | ------------------------------- | ------------------------------------ | ---------- |
| {{FR-NNN / capability}}  | {{what the UI does}} | {{what backend/system does}}    | {{what the UI triggers or displays}} | {{source}} |

Rules:

* UI may submit, display, trigger, confirm, and navigate.
* UI must not be described as performing backend-only work such as scoring, AML/KYC checks, disbursement, audit persistence, document generation, or asynchronous processing unless explicitly stated in the inputs.

---

## User Journeys

### Journey: {{Journey Name}}

**Actor:** {{role}}
**Goal:** {{what they accomplish end-to-end}}
**Linked FRs:** {{FR-NNN, FR-NNN}}

| Step | App     | Page     | User Action        | System Response            | Next                | Source     |
| ---- | ------- | -------- | ------------------ | -------------------------- | ------------------- | ---------- |
| 1    | {{app}} | {{page}} | {{what user does}} | {{what system shows/does}} | {{next page/state}} | {{FR-NNN}} |
| 2    | {{app}} | {{page}} | {{what user does}} | {{what system shows/does}} | {{next page/state}} | {{FR-NNN}} |

#### Alternative flows

| Condition     | Alternative Path   | Result     |
| ------------- | ------------------ | ---------- |
| {{condition}} | {{different path}} | {{result}} |

#### Error flows

| Error Condition     | User Sees         | Recovery Action                        |
| ------------------- | ----------------- | -------------------------------------- |
| {{error condition}} | {{message/state}} | {{retry/correct/contact support/etc.}} |

---

## Traceability Matrix

| FR         | UI Category                                                                  | Application | Page / Route     | Section / Component                 | Coverage                                                 | Confidence                                | Notes     |
| ---------- | ---------------------------------------------------------------------------- | ----------- | ---------------- | ----------------------------------- | -------------------------------------------------------- | ----------------------------------------- | --------- |
| {{FR-NNN}} | {{form/status display/decision UI/queue/document/dashboard/detail/workflow}} | {{app}}     | {{page / route}} | {{form / table / action / display}} | {{explicit/inferred/partial/not-covered/not-ui-bearing}} | {{explicit/inferred/needs-clarification}} | {{notes}} |

Rules:

* Every UI-bearing FR must appear.
* If a UI-bearing FR has no page mapping, mark it as `not-covered` and create an open UI question.
* If partially covered, mark it as `partial`.

---

## Open UI Questions

| ID          | Type                                                                                                                                                                                                           | Question     | Affected Routes  | Affected FRs | Blocking?  | Required Before                                       | Owner           | Suggested Resolution     |
| ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------ | ---------------- | ------------ | ---------- | ----------------------------------------------------- | --------------- | ------------------------ |
| {{UIQ-NNN}} | {{validation/permission/navigation/content/API contract/state-error/responsive-accessibility/repository mapping/application mapping/route coverage/backend-UI boundary/design system/third-party integration}} | {{question}} | {{page1, page2}} | {{FR-NNN}}   | {{Yes/No}} | {{delivery-planning / epic-elaboration / coding-handoff / n/a}} | {{who decides}} | {{suggested resolution}} |

---

## Final Quality Checklist

* [ ] Every frontend application from the technical landscape has a section.
* [ ] No placeholder application has been created.
* [ ] Every application has navigation and route tree.
* [ ] Every route appears in Page Specification Coverage.
* [ ] Every route marked `confirmed` has a matching `### Page:` section.
* [ ] Every UI-bearing FR appears in the traceability matrix.
* [ ] Every form has field-level detail with concrete validation rules or `needs-clarification`.
* [ ] Every table has column definitions.
* [ ] Every page has data binding with Contract Mode or explicitly states no API dependency.
* [ ] Every API binding references an existing endpoint or is marked `needs-contract`.
* [ ] Every page has states.
* [ ] Every page has a user flow.
* [ ] Every page has acceptance scenarios (3-5 per page).
* [ ] Every page has permissions.
* [ ] Every page has blocking dependencies listed (or "none").
* [ ] Every route has route guard behaviour.
* [ ] No page is marked `confirmed` while it has blocking open questions, `unknown` contract modes, or unresolved auth.
* [ ] Every `inferred` item has a corresponding open UI question.
* [ ] Shared component props are consistent with page field tables.
* [ ] UI/backend responsibilities are separated.
* [ ] Responsive and accessibility notes are included.
* [ ] Open UI questions are listed for every unresolved ambiguity.
* [ ] No placeholder text remains.
* [ ] No encoding artifacts (mojibake) remain in the output.
* [ ] No epics, features, stories, or coding tasks are created.

---

*Set Status: Accepted only by workflow or human approval when applicable. Never self-accept.*
