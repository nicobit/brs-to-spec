# Skill — Create Agile Planning View

## Identity

| Field | Value |
|---|---|
| skill_id | dl-create-agile-planning-view |
| persona | delivery-lead |
| event_types | CREATE_AGILE_PLANNING_VIEW |
| produces | perspectives/agile-planning/gitlab-planning-view.md |

## When this skill is used

After `CREATE_DELIVERY_STRUCTURE` completes (and optionally after `DEFINE_DELIVERY_INCREMENTS`). On demand when the team wants a GitLab or planning-tool projection of the initiative.

This is a read-only projection — not a second source of truth. Engineers implement from OpenSpec or standalone handoff artifacts, not from this view.

## Role for this task

You are a senior agile delivery lead translating the framework's delivery artifacts into a team-facing planning view — projecting epics, features, and stories into GitLab planning language, showing quality gate actions as issue checklist items, and making the relationship between planning and implementation explicit.

## Prerequisites check

Before starting, verify:
- [ ] `planning/delivery-structure.md` exists with F-XXX.X story IDs
- [ ] `business-intake/business-intake-summary.md` exists

Optional:
- [ ] `planning/delivery-increments.md` (for milestone mapping)
- [ ] `planning/traceability-matrix.md`
- [ ] `engineering-readiness/readiness-check.md`
- [ ] `quality-gates/*.md` (for gate action tracking)

If required inputs are missing: produce a draft view and mark missing inputs explicitly.

## Instructions

### Step 1 — Project the delivery hierarchy

Map the framework hierarchy to GitLab planning items:
- Epic → GitLab Epic (E-NNN)
- Feature → GitLab Feature or Parent Issue (F-NNN)
- User Story → GitLab Issue (F-NNN.N)
- Delivery Increment → GitLab Milestone (D1, D2, ...)

### Step 2 — Add quality gate tracking

For each triggered quality gate from `readiness-check.md`:
- Add as a GitLab checklist item on the relevant epic or milestone issue
- Reference the gate artifact path as the source of truth
- Do not duplicate gate content — link to it

### Step 3 — Add implementation notes

For each story, note:
- Source artifact path where the engineer should start (specs/F-XXX.X or standalone-delivery)
- This is for navigation, not a second task list
- User stories are business context and traceability — engineers use the handoff artifacts

### Step 4 — Write the planning view

Use the artifact template at `.brs2spec2/artifact-templates/gitlab-planning-view.md` if available.

The file must state clearly: "This is a planning projection — not the source of truth. Engineers implement from the approved handoff artifacts."

Set `Status: Draft`.

## Output requirements

The artifact must contain:
- Metadata table with Status, Initiative ID, creation date
- GitLab planning mapping table: Framework ID, GitLab Type, Title, Milestone, Source Artifact
- Quality gate tracking section
- Sync notes: how to update the planning view when the source artifacts change
- Statement that this is a projection, not implementation input

## Done criteria

- [ ] Every F-XXX.X story appears in the planning view
- [ ] The file explicitly states it is a projection, not the source of truth
- [ ] Quality gate items reference source artifacts, not duplicated content
- [ ] No requirements redefined independently from the delivery structure
- [ ] `Status: Draft` in the Metadata table
- [ ] Result file written with `status: pass` and `artifacts_written` listing `perspectives/agile-planning/gitlab-planning-view.md`

## Stop conditions

- If delivery-structure.md is missing: produce a draft with a gap note — do not invent stories.
- Do not create new scope not present in the delivery structure.
- Do not duplicate implementation tasks from the handoff artifacts.
