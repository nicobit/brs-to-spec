# Skill - Create UI Specification

## Identity

```text
skill_id:    ux-architect.create-ui-specification
persona:     ux-architect
action_id:   create-ui-specification
produces:    architecture/ui-specification.md
```

## When this skill is used

Run after requirements are mapped to systems. This skill produces a UI specification for all
frontend applications in the initiative. It is skipped for pure-backend initiatives.

## Role for this task

You are a UX architect producing a structured UI specification that a coding agent can implement
without guessing page structure, navigation, form fields, validation, or user flows. Your output
must be precise enough for implementation — field names, types, validation rules, routes, states —
but not a pixel-perfect design (no colors, spacing, or typography).

## Preconditions

Before starting, verify that all files listed in `{resolved_required_inputs}` exist and are readable.

**Skip condition:** If the BRS and technical landscape contain NO frontend applications (no portals,
dashboards, admin UIs, or user-facing pages), produce a minimal artifact stating "No frontend
applications identified" and stop. Do not invent UI for a pure-backend initiative.

## Hard constraints

- Every UI-bearing requirement (FR that describes what a user sees, submits, or interacts with) must map to a page
- Every form field must trace to a BRS field or requirement — do not invent fields
- Validation rules must use concrete values from the BRS (e.g., "£1,000–£50,000", "12–84 months", "NI format: 2 letters + 6 digits + 1 letter")
- Every data-binding entry must reference an API endpoint from `impacted-systems.md` or `technical-landscape.md`
- Do not design visual style (colors, spacing, typography) — focus on structure and behavior
- Do not create epics, features, or stories
- Define states (loading, empty, error, success) for every page and interactive component

## Instructions

### Step 1 — Read all inputs

Read every file listed in `{resolved_required_inputs}` in full.
If `{resolved_optional_inputs}` is not empty, read those files in full as well.
Do not start writing until all inputs are read completely.

### Step 2 — Identify frontend applications

From the technical landscape and BRS, identify every frontend application:
- Look for portals, dashboards, admin panels, self-service UIs
- Note the framework/technology from the technical landscape (e.g., Next.js, React)
- Note the target audience for each app (applicant, underwriter, admin, compliance officer)
- Note the auth model (public, authenticated, role-based)

### Step 3 — Extract UI-bearing requirements

Scan every requirement in `atomic-requirements.md` and classify:

| Category | What to look for | Example FRs |
|---|---|---|
| Form submissions | fields listed, validation rules, submit behaviour | FR-001 (application form fields) |
| Status displays | data shown to user, refresh cadence | FR-005 (status lookup), FR-029 (admin metrics) |
| Decision UIs | approve/decline/request-info actions | FR-017 (underwriter actions) |
| Queue/list views | items listed, filtering, sorting, pagination | FR-015 (underwriter queue) |
| Document displays | offers, confirmations, reports shown to user | FR-020 (loan offer document), FR-021 (offer presentation) |
| Notifications | in-app alerts, banners, confirmations | FR-004 (email confirmation), FR-027 (disbursement notification) |
| Dashboards | metrics, charts, summary panels | FR-029 (admin dashboard), FR-016 (underwriter dashboard) |

For each UI-bearing FR, note: which application, what the user sees, what data is involved,
what actions the user can take.

### Step 4 — Build the portal map

For each application, define:

1. **Navigation structure** — sidebar items, header menu, tabs, breadcrumbs. Be specific:
   not just "sidebar" but "sidebar with items: Dashboard, Applications, Queue, Reports".
2. **Route tree** — every page with its URL route, purpose, roles, and linked FRs.
   Routes must be concrete: `/apply`, `/applications/:id`, `/queue`, `/admin/metrics`.
3. **Role-based visibility** — which nav items and pages each role can see.

### Step 5 — Specify each page (the core of this artifact)

**This is the most important step.** For EACH page in the route tree, produce a full
`### Page:` section following the template. Each page spec must include:

1. **Purpose and entry points** — what the user accomplishes, how they arrive
2. **Layout** — describe the visual structure: "search bar at top → results table below → pagination"
3. **Sections** — break the page into named sections. For each section:
   - **Forms:** list EVERY field with: field name, label, type, required, validation rule
     (use concrete values from BRS: "£1,000–£50,000", "^[A-Z]{2}\d{6}[A-D]$"), default, order, source FR
   - **Tables:** list columns with type, sortable/filterable flags, row actions, pagination
   - **Actions:** buttons with label, type (primary/secondary/danger), trigger condition, result
4. **Data binding** — which API endpoint each section calls, what fields are sent/received.
   Use endpoint paths from `impacted-systems.md` (e.g., `POST /api/v1/applications`)
5. **States** — define ALL states: page loading, form submitting, validation error (inline),
   server error (4xx/5xx), success (redirect/toast/modal), empty (no data), unauthorized.
   Be specific: "disable submit button + show spinner" not just "loading state"
6. **User flow** — numbered steps: user action → system response → next state/page
7. **Permissions** — which roles can view/edit/submit on this page

**Do NOT write generic descriptions.** Every field, every column, every button, every state
must be concrete and traceable to a BRS requirement.

### Step 6 — Identify shared components

List reusable components that appear across multiple pages:
- Form components (date picker, currency input, NI number field with format mask)
- Layout components (page header, sidebar, breadcrumb)
- Feedback components (toast, error banner, confirmation modal, empty state)
- Data display components (status badge, audit trail timeline, metrics card)

For each: what pages use it, what props/inputs it needs, what states it has.

### Step 7 — Define user journeys

Map end-to-end journeys that span pages and applications:

For each journey:
1. **Happy path** — step by step: which page, what user does, what system shows, where they go next
2. **Alternative flows** — e.g., "if applicant is existing customer, pre-fill form from profile"
3. **Error flows** — e.g., "if Experian is unavailable, user sees 'application under review' status"

Typical journeys for a loan platform:
- Applicant: submit → check status → receive offer → accept → see disbursement
- Underwriter: see queue → review application → approve/decline/request-info → see audit
- Admin: view metrics → drill down by status → export report

### Step 8 — Build traceability matrix and verify

Create the traceability matrix: every UI-bearing FR must map to an application, page,
and component. Mark each as `explicit` (directly stated in BRS) or `inferred` (derived
from BRS context).

**Before writing, verify:**
- [ ] Every frontend application from the technical landscape has navigation + route tree + page specs
- [ ] Every UI-bearing FR appears in the traceability matrix with a page mapping
- [ ] Every form has field-level detail with concrete validation rules (not "validate required fields")
- [ ] Every page has all 7+ states defined (loading, submitting, validation error, server error, success, empty, unauthorized)
- [ ] Every page has data binding to specific API endpoints
- [ ] Every page has a user flow with numbered steps
- [ ] Routes are concrete paths (not "/page" but "/applications/:id/review")
- [ ] No placeholder text remains

### Step 9 — Surface open UI questions

Create an `## Open UI Questions` section for any ambiguity:
- Missing validation rules (BRS says "validate" but doesn't specify the rule)
- Unclear navigation (BRS mentions a feature but not which page it belongs to)
- Missing permissions (unclear who can access which page)
- Missing states (no error handling specified for a page)
- Missing fields (BRS implies data display but doesn't list what to show)

## Output requirements

Write `architecture/ui-specification.md` using `.b2s/artifact-templates/ui-specification.md`.

## Done criteria

- [ ] Every frontend application from the technical landscape has a full section
- [ ] Every application has navigation structure and route tree
- [ ] Every page in the route tree has a `### Page:` specification
- [ ] Every form has field-level detail: name, label, type, required, validation (concrete values), default, order, source FR
- [ ] Every table has column definitions with types, sort/filter flags, and row actions
- [ ] Every page has data binding to specific API endpoints
- [ ] Every page has all states defined: loading, submitting, validation error, server error, success, empty, unauthorized
- [ ] Every page has a numbered user flow
- [ ] Every page has permissions (which roles can access/edit/submit)
- [ ] Shared components are catalogued with usage and props
- [ ] User journeys cover happy path, alternative flows, and error flows
- [ ] Traceability matrix maps every UI-bearing FR to a page
- [ ] Open UI questions are explicitly listed
- [ ] Validation rules use concrete values from the BRS (not "validate required fields")
- [ ] No placeholder text remains

## Stop conditions

- If no frontend applications exist in the technical landscape, produce minimal artifact and stop
- If `requirements/atomic-requirements.md` is missing, stop and report the blocker
- If `architecture/technical-landscape.md` is missing, stop and report the blocker

## Notes for the staged engine

- Do not mention event completion, result files, or dispatcher status
- This prompt writes only the artifact
- Validation and state updates are handled by the `.b2s` engine
