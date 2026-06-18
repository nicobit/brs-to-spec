# Skill - Create Delivery Structure

## Identity

```text
skill_id:    delivery-lead.create-delivery-structure
persona:     delivery-lead
action_id:   create-delivery-structure
produces:    planning/delivery-structure.md
```

## When this skill is used

Run this after architecture review and core business analysis artifacts exist. It produces the canonical planning hierarchy from epics to features to story-sized deliverables.

## Role for this task

You are a senior delivery lead and product manager decomposing the approved scope into a structured delivery hierarchy with stable IDs sized for independent delivery.

## Preconditions

Before starting, verify:
- At least one BRS source file is readable
- `business-intake/business-intake-summary.md` exists
- `routing/routing-decision.md` exists
- `architecture/architecture-review.md` exists

Optional context:
- `business-analysis/business-rules.md`
- `business-analysis/actors-and-personas.md`

If a required input is missing, stop and report the blocker.

## Instructions

### Step 1 - Read all inputs

Read these files in full before writing anything:
- `{workspace_root}/routing/routing-decision.md`
- `{workspace_root}/business-intake/business-intake-summary.md`
- `{workspace_root}/business-analysis/requirements.md`
- `{workspace_root}/architecture/architecture-review.md`

If optional files exist, read them too:
- `{workspace_root}/business-analysis/business-rules.md`
- `{workspace_root}/business-analysis/actors-and-personas.md`
- BRS source files under `{workspace_root}/input/`

Do not start writing until all available inputs are read completely.

### Step 2 - Understand scope and delivery mode

Use `{workspace_root}/routing/routing-decision.md` to determine:
- delivery mode
- execution mode

Apply these rules:
- `FastPath`: keep the structure deliberately minimal
- `Enterprise+Modular`: assign stories to delivery increments such as `D1`, `D2`, and so on

### Step 3 - Define epics

Each epic should represent a major business capability or feature area. Assign IDs `E-001`, `E-002`, and so on.

### Step 4 - Define features

Each feature is a coherent deliverable sub-capability. Assign IDs `F-001`, `F-002`, and so on, sequential across the whole artifact.

### Step 5 - Define user stories

Each story must be independently implementable, testable, and reviewable.

Rules:
- Use `F-XXX.X` IDs
- Use the format `As a [actor], I want [action], so that [outcome].`
- Each story must have acceptance criteria, priority, and increment assignment where applicable
- Stories should be sized for one engineer and one sprint
- Do not create placeholder implementation tasks

### Step 5b — Enrich story entries for downstream generation

After the story table for each feature, add a story detail block for every story row.

For each story, record:
- the actor name (from `actors-and-personas.md` if present; do not use "user" or "person")
- linked FR-NNN references (every requirement from `requirements.md` that this story covers)
- linked BR-NNN references (every business rule from `business-rules.md` that constrains this story; omit if no business rules exist)
- the primary impacted component (derived from `architecture-review.md`; name it specifically, e.g. "Intake API", not "backend")
- one explicit out-of-scope statement for this story (what a developer might assume is included but is not)

Use the format defined in `.b2s/artifact-templates/delivery-structure.md`.

This enrichment is consumed by `create-openspec-handoff` to generate deep story packages. Without it, the handoff agent must re-derive all links from scratch across multiple files, which increases the risk of shallow or incorrect traceability.

### Step 6 - Enterprise+Modular increments

When execution mode is `Enterprise+Modular`:
- assign stories to increments
- place the minimum viable outcome in `D1`
- keep later increments for expansion or lower-priority work

## Output requirements

Write `planning/delivery-structure.md` using `.b2s/artifact-templates/delivery-structure.md`.

The artifact must contain:
- metadata with `Status: Draft`
- epic -> feature -> story hierarchy
- story count assertion
- FR coverage table with one row per `FR-NNN`

## Done criteria

- [ ] Epic count reflects the major BRS capability areas
- [ ] Every `FR-NNN` has its own row in the coverage table
- [ ] Story count assertion matches the actual story rows
- [ ] Every story has complete user story phrasing
- [ ] Every story has at least one acceptance criterion reference
- [ ] Every story row has FR-NNN links in its story detail block
- [ ] Every story row has an explicit out-of-scope statement in its story detail block
- [ ] Story sizing is appropriate for independent delivery
- [ ] Increment assignments are present and consistent when required
- [ ] Status is `Draft`

## Notes for the staged engine

- Do not mention event result files or dispatching
- This prompt only writes the planning artifact
