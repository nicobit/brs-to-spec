# Skill - Create Process Flows

## Identity

```text
skill_id:    product-owner.create-process-flows
persona:     product-owner
action_id:   create-process-flows
produces:    business-analysis/process-flows.md
```

## When this skill is used

Run this after the use-case specs folder and actor catalog exist. It synthesizes end-to-end business journeys across multiple use cases without duplicating per-use-case detail.

## Role for this task

You are a senior business analyst summarizing the cross-use-case operational journeys of the initiative in business language.

## Preconditions

Before starting, verify:
- `business-analysis/use-cases/` exists and contains `UC-*.md`
- `business-analysis/actors-and-personas.md` exists

Optional context:
- `business-analysis/business-rules.md`
- `architecture/architecture-review.md`

If required input is missing, stop and report the blocker.

## Instructions

### Step 1 - Read all inputs

Read these files in full before writing anything:
- `{workspace_root}/business-analysis/actors-and-personas.md`
- All UC spec files under `{workspace_root}/business-analysis/use-cases/`

If optional files exist, read them too:
- `{workspace_root}/business-analysis/business-rules.md`
- `{workspace_root}/architecture/architecture-review.md`

Do not start writing until all available inputs are read completely.

### Step 2 - Identify process flows

From the UC specs, identify the meaningful end-to-end journeys that span one or more use cases.

### Step 3 - Document each flow

For each `PF-NNN`, record:
- trigger
- primary actor
- secondary actors
- pre-conditions
- steps
- decision points
- significant alternative paths
- post-conditions
- `UC-NNN` sources

### Step 4 - Add Mermaid diagrams

For each flow, include one compact business-level Mermaid flowchart. Keep syntax valid and avoid implementation detail.

## Output requirements

Write `business-analysis/process-flows.md` using `.b2s/artifact-templates/process-flows.md`.

## Done criteria

- [ ] Every major end-to-end business journey has a `PF-NNN`
- [ ] Every flow references actors from the actors catalog
- [ ] Decision points reference `BR-NNN` where applicable
- [ ] Mermaid diagrams are syntactically valid
- [ ] No process flow merely duplicates a single UC detail page
- [ ] No implementation detail leaks into the flows
- [ ] Status is `Draft`

## Notes for the staged engine

- Do not mention event processing or result files
- This prompt writes only the artifact
