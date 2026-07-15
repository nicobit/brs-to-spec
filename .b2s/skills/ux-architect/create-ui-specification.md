# Skill - Create UI Specification

## Identity

```text
skill_id:    ux-architect.create-ui-specification
persona:     ux-architect
action_id:   create-ui-specification
produces:    architecture/ui-specification.md
```

---

## When this skill is used

Run after requirements are mapped to systems.

This skill produces a structured UI specification for all frontend applications in the initiative. It is skipped for pure-backend initiatives.

Use this skill when the initiative includes one or more of:

* public portals
* authenticated portals
* dashboards
* admin panels
* operational UIs
* workflow UIs
* reporting/monitoring UIs
* user-facing pages
* internal user tools

---

## Role for this task

You are a UX architect producing a structured UI specification that a coding agent can implement without guessing page structure, navigation, form fields, validation, routing, states, permissions, API bindings, or user flows.

Your output must be precise enough for implementation:

* application inventory
* navigation
* route tree
* page coverage
* page specifications
* fields
* validation rules
* tables
* actions
* states
* route guards
* API bindings
* shared components
* user journeys
* traceability
* open UI questions

This is **not** a pixel-perfect design specification. Do not define colors, spacing, typography, branding, or final visual design unless explicitly provided in the inputs.

---

## Preconditions

Before starting, verify that all files listed in `{resolved_required_inputs}` exist and are readable.

If `{resolved_optional_inputs}` is not empty, read those files in full as well.

### Required inputs

The skill expects at least:

```text
requirements/atomic-requirements.md
architecture/technical-landscape.md
architecture/impacted-systems.md
```

### Optional inputs

Use if available:

```text
input/brs.md
input/architecture.md
input/repository-context.md
architecture/solution-decisions.md
architecture/architecture-rules.md
architecture/api-contracts.md
architecture/data-entities.md
```

---

## Skip condition

If the BRS, atomic requirements, impacted systems, and technical landscape contain **no frontend applications** and no UI-bearing requirements, produce a minimal artifact:

```md
# UI Specification

## Result

No frontend applications identified.

## Reason

The analyzed requirements and technical landscape do not describe portals, dashboards, admin UIs, user-facing pages, forms, lists, visual workflows, or interactive UI components.

## Follow-up

No UI specification is required for this initiative unless new UI-bearing requirements are added.
```

Then stop.

Do not invent UI for a pure-backend initiative.

---

## Hard constraints

* Every UI-bearing requirement must map to at least one application, route, page, section, or component.
* This artifact is the canonical initiative-level source for UI structure and behavior.
* Every form field must trace to a BRS field, atomic requirement, or explicit input artifact.
* Do not invent form fields.
* Validation rules must use concrete values from the BRS or atomic requirements.
* If a validation rule is unclear, mark it as `needs-clarification`.
* Every data-binding entry must reference an API endpoint from `impacted-systems.md`, `technical-landscape.md`, `solution-decisions.md`, or an explicit API contract.
* Do not invent API endpoints.
* Do not invent response fields.
* Do not design visual style.
* Do not create epics, features, stories, or coding tasks.
* Define states for every page and interactive component.
* Do not create placeholder applications such as `needs-clarification`, `unknown`, `TBD`, `frontend`, or `misc`.
* Do not describe the same application, route, or page in multiple competing sections.
* Every route must have exactly one canonical page definition in this artifact.
* Do not silently omit routes.
* Do not silently omit UI-bearing requirements.
* If information is missing, mark it clearly and add an open UI question.
* **Every application in the Application Inventory must have either a full route tree and page specifications, or an explicit note explaining why no standalone pages are specified** (e.g. "Compliance casework is handled within Underwriter Dashboard case detail panels; no standalone compliance pages required"). Do not list applications in the inventory and then leave them unspecified.
* **The Traceability Matrix must include every UI-bearing FR, not sample rows.** Do not write "sample rows" or truncate. If there are many FRs, list them all.
* **The UI Readiness Matrix is mandatory.** Every page from every route tree must appear with its readiness assessment.

---

## Anti-hallucination rules

If information is missing or ambiguous:

* do not invent it
* write `needs-clarification`
* add an open UI question
* mark the affected page, route, section, or API binding as `partial`
* explain what input is required to complete it

Never invent:

* applications
* routes
* API endpoints
* request schemas
* response schemas
* fields
* validation values
* roles
* permissions
* business rules
* backend responsibilities
* third-party flows
* status values
* workflow states
* repository names

If something is inferred, mark it as `inferred`.

If something is directly supported by the BRS, atomic requirements, technical landscape, or impacted systems, mark it as `explicit`.

---

## Implementation safety rules

These rules govern the `Specification Status`, `Contract Mode`, and `Blocking Dependencies` fields.

### Status assignment

* `confirmed` — all page details are fully specified and verified against inputs. A page may only be `confirmed` when ALL of these are true:
  - route guard behaviour is fully specified (no `needs-clarification` in auth)
  - all API bindings have contract mode `confirmed` or `partial` (not `unknown` or `mock`)
  - all form fields, states, and success/error navigation are fully specified
  - no blocking open UI questions reference the page
* `inferred` — page details are derived but not explicitly confirmed. Every `inferred` item must create or reference an explicit open UI question.
* `partial` — required details are missing or marked needs-clarification. Unresolved dependencies are listed in the page's `Blocking dependencies` field and will be resolved when the epic containing the page enters active elaboration.
* `blocked` — a blocking dependency prevents specification entirely.

### Contract mode assignment

Every data binding row must include a `Contract Mode`:

* `confirmed` — endpoint, request, and response schemas are fully defined in an API contract or impacted-systems artifact.
* `partial` — endpoint exists but request/response details are incomplete.
* `proposed-by-ui-spec` — endpoint path is proposed by this UI spec based on UI needs, but not confirmed by any API contract. Must be validated against the implementation contract before coding.
* `mock` — endpoint is assumed; implementation must use a mock/stub until the contract is provided.
* `unknown` — no contract information available; must not be implemented against.

### Blocking dependencies

Every page must list its blocking dependencies explicitly:

* Reference open UI question IDs (UIQ-NNN) and/or gap IDs (GAP-NNN).
* Write "none" if no blocking dependencies exist.
* A dependency may still be acceptable for initiative-level design if its open question is classified as `Required Before = epic-elaboration`. Only `Required Before = delivery-planning` should block the solution-design stage itself.

### Consistency checks

Before finalizing:

* Every `inferred` item in any table must have a corresponding open UI question.
* Shared component props must be consistent with page field tables - if a shared component lists fields (e.g., "name, dob, address, income, employment") then all listed fields must appear in the page field table for every page that uses the component.
* If a UI surface could be standalone or embedded (e.g., a notification center that could be its own app or a panel within another app), make an explicit boundary decision and record it in the open questions if unresolved.
* If repository ownership, frontend technology, hosting, or auth platform are already decided in `architecture/solution-decisions.md`, reference those decisions rather than redefining them here.
* Do not turn summary sections into second page specifications.

---

## Instructions

---

# Step 1 — Read all inputs

Read every file listed in `{resolved_required_inputs}` in full.

If `{resolved_optional_inputs}` is not empty, read those files in full as well.

Do not start writing the final artifact until all inputs have been read completely.

While reading, collect:

* frontend applications
* roles and audiences
* UI-bearing requirements
* routes or implied routes
* user actions
* forms
* fields
* validations
* dashboards
* tables
* status displays
* notifications
* document views
* workflow screens
* API endpoints
* impacted systems
* repository/application mapping gaps
* unclear requirements

---

# Step 2 — Identify frontend applications

From the technical landscape, impacted systems, BRS, and atomic requirements, identify every real frontend application.

Look for:

* portals
* dashboards
* admin panels
* operational consoles
* reporting screens
* monitoring screens
* user-facing pages
* internal workflow tools
* self-service UIs

For each application, identify:

* application name
* short description
* target audience
* framework/technology
* auth model
* hosting model
* entry point
* source evidence
* confidence: `explicit`, `inferred`, or `needs-clarification`

## Application identification rules

Do not create fake applications.

Invalid application names include:

```text
needs-clarification
unknown
TBD
frontend
misc
placeholder
not specified
```

If the technical landscape contains unresolved repository/application fields, do not turn them into applications.

Instead, record them under:

```md
## Repository / Application Mapping Gaps
```

For each gap, specify:

| Gap ID | Description | Source | Impact | Required Input | Owner |
| ------ | ----------- | ------ | ------ | -------------- | ----- |

---

# Step 3 — Extract UI-bearing requirements

Scan every requirement in `requirements/atomic-requirements.md`.

Classify UI-bearing requirements using this taxonomy:

| Category          | What to look for                                  | Examples                                          |
| ----------------- | ------------------------------------------------- | ------------------------------------------------- |
| Form submissions  | fields, validation rules, submit behaviour        | application forms, onboarding forms, search forms |
| Status displays   | status, progress, result display, refresh cadence | status lookup, progress tracker                   |
| Decision UIs      | approve, decline, request info, review actions    | underwriter actions, maker/checker approval       |
| Queue/list views  | items listed, filters, sorting, pagination        | work queue, search results                        |
| Document displays | offers, confirmations, reports, PDFs              | document preview, offer display                   |
| Notifications     | banners, in-app alerts, confirmations             | success banner, alert list                        |
| Dashboards        | metrics, charts, summary cards                    | admin metrics, monitoring                         |
| Detail pages      | record details, audit history, timeline           | application detail, client detail                 |
| Workflow pages    | multi-step flows, wizard, guided journey          | application journey, approval flow                |

For each UI-bearing requirement, capture:

| FR | Category | User / Role | What user sees | User action | Data involved | Application | Page / Route | Confidence |
| -- | -------- | ----------- | -------------- | ----------- | ------------- | ----------- | ------------ | ---------- |

If the requirement is backend-only but has a UI display or trigger, record the UI part only and classify the backend part separately in the UI/backend responsibility section.

---

# Step 4 — Build the application inventory

Create:

```md
## Application Inventory
```

Use this table:

| Application | Audience | Framework | Auth Model | Hosting | Entry Point | Confidence | Source |
| ----------- | -------- | --------- | ---------- | ------- | ----------- | ---------- | ------ |

Rules:

* Include only real applications.
* If framework, auth model, or hosting is missing, use `needs-clarification`.
* Do not invent technology choices.
* If an application is inferred, mark it as `inferred`.

---

# Step 5 — Build the portal map

For each application, create:

```md
## Application: <Application Name>
```

Include:

```md
Short description:
Audience:
Auth model:
Primary roles:
Entry point:
```

Then define:

## Navigation

| Nav Element | Type | Items | Visible To | Source |
| ----------- | ---- | ----- | ---------- | ------ |

Rules:

* Be specific.
* Do not write only “sidebar” or “header”.
* List concrete items and target routes.
* If navigation is unclear, mark `needs-clarification`.

## Route Tree

| Route | Page | Purpose | Roles | Linked FRs | Confidence | Specification Status |
| ----- | ---- | ------- | ----- | ---------- | ---------- | -------------------- |

`Specification Status` must be one of:

* `confirmed`
* `inferred`
* `partial`
* `blocked`

A page may only be `confirmed` if all its details are fully specified and no blocking open questions reference it. See **Implementation safety rules** above.

Rules:

* Routes must be concrete paths, such as `/apply`, `/applications/:arn`, `/admin/metrics`.
* If a route appears in navigation, it must appear in the route tree.
* If a route is required by an FR, it must appear in the route tree.
* Do not invent routes when the inputs do not support them.
* If the page is implied but the route is unknown, use `route-needs-clarification`.

---

# Step 6 — Create mandatory page specification coverage register

Before writing detailed page specifications, create:

```md
## Page Specification Coverage
```

List every route from every route tree.

Use this table:

| Application | Route | Page | Specification Status | Reason | Required Follow-up |
| ----------- | ----- | ---- | -------------------- | ------ | ------------------ |

Specification Status must be one of: `confirmed`, `inferred`, `partial`, `blocked`.

Rules:

* Every `confirmed` route must have a matching `### Page:` section.
* No route may be omitted silently.
* If a route is listed in navigation, it must appear here.
* If a route appears here but has no page spec, the reason must be explicit.
* If the details are insufficient, mark the route as `partial` or `blocked` and create an open UI question.
* A page may not be `confirmed` if it has blocking open questions, `unknown` contract modes, or unresolved auth.
* For `partial` or `blocked` pages, preserve known facts and blockers honestly instead of inventing missing detail to make the page look complete.

---

# Step 7 — Define route guards and authorization matrix

Create:

```md
## Route Guards and Authorization
```

Use this table:

| Route Pattern | Access Type | Allowed Roles | Unauthenticated Behaviour | Unauthorized Behaviour | Verification Required | Notes |
| ------------- | ----------- | ------------- | ------------------------- | ---------------------- | --------------------- | ----- |

Rules:

* Every route pattern must be covered.
* Public routes must explicitly say `No login required`.
* Authenticated routes must define redirect behaviour.
* Role-based routes must define forbidden behaviour.
* Public lookup/detail routes must specify verification requirements, for example ARN + DOB.
* If behaviour is unclear, write `needs-clarification`.

---

# Step 8 — Specify each page

This is the core of the artifact.

For each route marked `confirmed`, produce a full page section:

```md
### Page: <Page Name>
```

Include:

```md
**App:** <Application>
**Route:** <Route>
**Roles:** <Roles>
**Purpose:** <Purpose>
**Linked FRs:** <FRs>
**Entry points:** <Entry points>
**Specification status:** <confirmed/inferred/partial/blocked>
**Blocking dependencies:** <UIQ-NNN, GAP-NNN or "none">
```

Each page specification must include all of the following sections.

For pages marked `partial`, include only the confirmed structure, known fields or bindings, and explicit blockers.
For pages marked `blocked`, keep the page minimal and focus on why it cannot yet be specified safely.

---

## 8.1 Layout

Describe the page structure in implementation terms.

Example:

```text
Header with page title and status badge → main form card → review summary panel → sticky submit bar
```

Rules:

* Do not define colors, typography, spacing, or branding.
* Do define structural hierarchy.
* Include responsive layout notes if relevant.

---

## 8.2 Sections

Break the page into named sections.

For each section, specify whether it is:

* form
* table
* card
* action panel
* detail panel
* timeline
* dashboard
* document viewer
* notification area
* search/filter area

---

## 8.3 Forms

For every form, list every field:

| Field | Label | Type | Required | Validation | Default | Order | Source | Confidence |
| ----- | ----- | ---- | -------- | ---------- | ------- | ----- | ------ | ---------- |

Rules:

* Every field must trace to a BRS field or requirement.
* Do not invent fields.
* Use concrete validation rules from the BRS or atomic requirements.
* If validation is unclear, use `needs-clarification`.
* Include masks and format rules only when supported by inputs.
* Include field order if stated or logically required by the flow.

---

## 8.4 Tables

For every table, list columns:

| Column | Label | Type | Sortable | Filterable | Source | Confidence |
| ------ | ----- | ---- | -------- | ---------- | ------ | ---------- |

Also include:

```md
**Row actions:**
**Bulk actions:**
**Pagination:**
**Default sort:**
**Empty state:**
```

If unknown, write `needs-clarification`.

---

## 8.5 Actions

For every button or user action:

| Action ID | Label | Type | Trigger | Condition | Result | Source |
| --------- | ----- | ---- | ------- | --------- | ------ | ------ |

Action type must be one of:

* primary
* secondary
* danger
* link
* icon
* menu item
* system-triggered

Rules:

* Define the condition under which the action is enabled.
* Define the result.
* If the action calls an API, reference the API binding.

---

## 8.6 Data binding

For every section that calls or receives data from an API:

| Component / Section | API Endpoint | Method | Request | Response → Display | Source | Contract Status | Contract Mode |
| ------------------- | ------------ | ------ | ------- | ------------------ | ------ | --------------- | ------------- |

`Contract Status` must be one of:

* `explicit-contract`
* `partial-contract`
* `needs-contract`
* `inferred`

`Contract Mode` must be one of:

* `confirmed` — endpoint, request, and response schemas are fully defined
* `partial` — endpoint exists but request/response details are incomplete
* `mock` — endpoint is assumed; implementation must use a mock/stub
* `unknown` — no contract information available; must not be implemented against

Rules:

* Use only endpoints explicitly present in `impacted-systems.md`, `technical-landscape.md`, `solution-decisions.md`, or formal API contracts.
* Do not invent endpoints.
* Do not invent request or response schemas.
* If schema details are missing, mark `needs-contract` for Contract Status and `unknown` or `mock` for Contract Mode.
* If response fields are inferred from UI needs, mark `inferred` and add an open question.
* Include error response handling only if known; otherwise mark `needs-contract`.
* A page with any `unknown` Contract Mode binding must not be marked `confirmed`.

---

## 8.7 States

For every page and interactive component, define states.

Use this table:

| State | Trigger | Visual Behaviour | Data / API Dependency | Recovery / Next Action |
| ----- | ------- | ---------------- | --------------------- | ---------------------- |

Required states:

* page loading
* component loading
* form submitting, if applicable
* validation error, if applicable
* server error 4xx
* server error 5xx
* success
* empty
* unauthorized
* forbidden
* stale/refreshing, if applicable

Rules:

* Be specific.
* Do not write only “show loading”.
* Write concrete behaviour, such as “disable submit button and show spinner on the clicked button”.
* If a state is not applicable, write `n/a` with reason.

---

## 8.8 User flow

Create a numbered flow:

| Step | User Action | System Response | Next State / Page | Source |
| ---- | ----------- | --------------- | ----------------- | ------ |

Rules:

* Include happy path.
* Include important alternative paths.
* Include important error paths.
* Do not include backend-only processing as if the UI performs it.

---

## 8.9 Acceptance Scenarios

For every page, include 3-5 lightweight acceptance scenarios:

| Scenario | Given | When | Then | Source |
| -------- | ----- | ---- | ---- | ------ |

Rules:

* Cover the happy path, one key alternative path, and one key error path.
* Every scenario must trace to a linked FR.
* Keep scenarios lightweight — do not duplicate full QA acceptance criteria.
* These bridge the gap between UX analysis and story/test generation.

---

## 8.10 Permissions

Create:

| Action / Capability | Allowed Roles | Denied Behaviour | Source |
| ------------------- | ------------- | ---------------- | ------ |

Rules:

* Include view, submit, edit, approve, decline, export, search, and admin actions as applicable.
* If role levels are unclear, mark `needs-clarification`.

---

## 8.11 Responsive and accessibility notes

For each page, include:

```md
#### Responsive Behaviour
```

Specify high-level behaviour for:

* desktop
* tablet
* mobile

If not applicable or unknown, mark `needs-clarification`.

Also include:

```md
#### Accessibility Requirements
```

Specify:

* keyboard navigation expectations
* focus management
* error summary behaviour
* ARIA needs for tables, badges, forms, timelines, or modals
* screen reader considerations
* minimum accessibility target, if known

Default target: `WCAG 2.1 AA`, unless project inputs specify otherwise.

Do not define colors, spacing, typography, or brand style.

---

# Step 9 — Define shared components

Create:

```md
## Shared Components
```

Use this table:

| Component | Type | Used By Pages | Props / Inputs | States | Source | Confidence |
| --------- | ---- | ------------- | -------------- | ------ | ------ | ---------- |

Component types include:

* form input
* layout
* navigation
* feedback
* modal
* table
* card
* badge
* timeline
* chart
* document viewer

Rules:

* List reusable components only.
* Do not invent props that are unsupported by the page specs.
* If props are inferred from usage, mark confidence as `inferred`.

---

# Step 10 — Separate UI and backend responsibilities

Create:

```md
## UI vs Backend Responsibilities
```

Use this table:

| Requirement / Capability | UI Responsibility | Backend / System Responsibility | UI Trigger / Display | Source |
| ------------------------ | ----------------- | ------------------------------- | -------------------- | ------ |

Rules:

* UI may trigger or display backend outcomes.
* UI must not be described as performing backend-only work.
* Backend-only responsibilities include scoring, AML/KYC checks, disbursement, document generation, audit persistence, asynchronous processing, notifications, and third-party integration processing unless explicitly stated otherwise.
* If unclear, mark `needs-clarification`.

---

# Step 11 — Define user journeys

Create:

```md
## User Journeys
```

For each journey:

```md
### Journey: <Journey Name>
```

Include:

```md
**Actor:**
**Goal:**
**Linked FRs:**
```

Then use this table:

| Step | App | Page | User Action | System Response | Next | Source |
| ---- | --- | ---- | ----------- | --------------- | ---- | ------ |

Each journey should include:

* happy path
* alternative flows
* error flows

Rules:

* Do not make the UI responsible for backend-only behaviour.
* If backend processing happens, write “Backend/system processes...” and define what the UI displays next.
* If a required page is missing, mark the journey step as `needs-page-spec`.

---

# Step 12 — Build traceability matrix

Create:

```md
## Traceability Matrix
```

**Every UI-bearing FR must appear — no sample rows, no truncation.** List every FR from `atomic-requirements.md` that has any UI surface. If there are 30 UI-bearing FRs, the matrix must have at least 30 rows.

Use this table:

| FR | UI Category | Application | Page / Route | Section / Component | Coverage | Confidence | Notes |
| -- | ----------- | ----------- | ------------ | ------------------- | -------- | ---------- | ----- |

Coverage must be one of:

* `explicit`
* `inferred`
* `partial`
* `not-covered`
* `not-ui-bearing`

Rules:

* Every UI-bearing FR must map to a page or route.
* If no page exists, mark `not-covered` and add an open UI question.
* If only partial coverage exists, mark `partial`.
* Do not hide missing coverage.

---

# Step 13 — Add open UI questions

Create:

```md
## Open UI Questions
```

Use this table:

| ID | Type | Question | Affected Routes | Affected FRs | Blocking? | Required Before | Owner | Suggested Resolution |
| -- | ---- | -------- | --------------- | ------------ | --------- | --------------- | ----- | -------------------- |

Question types:

* validation
* permission
* navigation
* content
* API contract
* state/error handling
* responsive/accessibility
* repository mapping
* application mapping
* route coverage
* backend/UI boundary
* design system
* third-party integration

Rules:

* Every `needs-clarification` item should create or reference an open UI question.
* Mark `Blocking?` as `Yes` if some downstream stage would be unsafe without the answer.
* Use `Required Before` to classify the blocker:
  - `delivery-planning` — initiative-blocking; solution design should not pass the clarification gate without an answer
  - `epic-elaboration` — not initiative-blocking; delivery planning may continue, but the affected epic must not be elaborated as implementation-ready until answered
  - `coding-handoff` — acceptable through epic/story design, but must be resolved before coding handoff
* If `Blocking?` is `No`, set `Required Before` to `n/a`.
* Do not leave unresolved ambiguity hidden in prose.

---

# Step 14 — Add repository / application mapping gaps

If any unresolved application or repository mapping issue exists, create:

```md
## Repository / Application Mapping Gaps
```

Use this table:

| Gap ID | Description | Source | Impact | Required Input | Owner |
| ------ | ----------- | ------ | ------ | -------------- | ----- |

Rules:

* Do not create placeholder applications.
* Capture missing frontend repository/app mapping here.
* If no gaps exist, write:

```text
No repository/application mapping gaps identified.
```

---

# Step 15 — Final self-check before writing

Before producing the final artifact, verify:

* [ ] Every frontend application from the technical landscape has an application section.
* [ ] No placeholder application has been created.
* [ ] Every application has navigation and route tree.
* [ ] Every route appears in the Page Specification Coverage section.
* [ ] Every route marked `confirmed` has a matching `### Page:` section.
* [ ] Every UI-bearing FR appears in the traceability matrix.
* [ ] Every form has field-level detail with concrete validation rules or `needs-clarification`.
* [ ] Every table has column definitions.
* [ ] Every page has data binding with Contract Mode or explicitly states no API dependency.
* [ ] Every API binding references an existing endpoint or is marked `needs-contract`.
* [ ] Every page has states.
* [ ] Every page has a user flow.
* [ ] Every page has acceptance scenarios (3-5).
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

If any check fails, fix the artifact before finalizing it.

---

## Output requirements

Write:

```text
architecture/ui-specification.md
```

using:

```text
.b2s/artifact-templates/ui-specification.md
```

The artifact must be valid Markdown.

---

## Done criteria

* [ ] Every frontend application from the technical landscape has a full section.
* [ ] Every application has navigation structure and route tree.
* [ ] Every route appears in the Page Specification Coverage section with Specification Status.
* [ ] Every page marked `confirmed` has a `### Page:` specification.
* [ ] No fake placeholder applications exist.
* [ ] Every form has field-level detail: name, label, type, required, validation, default, order, source.
* [ ] Every table has column definitions with types, sort/filter flags, row actions, and pagination.
* [ ] Every page has data binding with Contract Mode to specific API endpoints or explicitly states no API dependency.
* [ ] API request/response details are not invented.
* [ ] Every page has states: loading, submitting if applicable, validation error if applicable, server error, success, empty, unauthorized, forbidden.
* [ ] Every page has a numbered user flow.
* [ ] Every page has 3-5 lightweight acceptance scenarios.
* [ ] Every page has permissions.
* [ ] Every page has blocking dependencies listed (or "none").
* [ ] No page is marked `confirmed` with blocking open questions, `unknown` contract modes, or unresolved auth.
* [ ] Every `inferred` item has a corresponding open UI question.
* [ ] Shared component props are consistent with page field tables.
* [ ] Route guards and authorization matrix covers all routes.
* [ ] Shared components are catalogued with usage and props.
* [ ] UI vs backend responsibilities are separated.
* [ ] User journeys cover happy path, alternative flows, and error flows.
* [ ] Traceability matrix maps every UI-bearing FR to a page.
* [ ] Open UI questions are explicitly listed and typed.
* [ ] Validation rules use concrete values from the BRS or are marked `needs-clarification`.
* [ ] Responsive and accessibility notes are included.
* [ ] Repository/application mapping gaps are captured separately.
* [ ] No placeholder text remains.
* [ ] No encoding artifacts (mojibake) remain in the output.
* [ ] No epics, features, stories, or coding tasks are created.

---

## Stop conditions

Stop and report the blocker if:

* `requirements/atomic-requirements.md` is missing.
* `architecture/technical-landscape.md` is missing.
* `architecture/impacted-systems.md` is missing.
* Required files in `{resolved_required_inputs}` are not readable.

If no frontend applications exist, produce the minimal “No frontend applications identified” artifact and stop.

---

## Notes for the staged engine

* Do not mention event completion, result files, dispatcher status, or internal engine state.
* This prompt writes only the artifact.
* Validation and state updates are handled by the `.b2s` engine.
* Do not self-accept the artifact.
* Set status to `Accepted` only when the workflow or a human approval step explicitly approves it.
