# Skill - Create Standalone Handoff

## Identity

```text
skill_id:    engineering-lead.create-standalone-handoff
persona:     engineering-lead
action_id:   create-standalone-handoff
produces:    standalone-delivery/
```

## When this skill is used

Run this only when the execution mode is `Standalone`, readiness is `Ready`, and all triggered gates are accepted.

## Preconditions

Before starting, verify:
- `engineering-readiness/readiness-check.md` is `Ready`
- all triggered gates are accepted
- `planning/delivery-structure.md` has story IDs
- `architecture/architecture-review.md` exists
- `architecture/architecture-rules.md` exists

## Instructions

### Step 1 - Read all inputs

Read these files in full before writing anything:
- `{workspace_root}/engineering-readiness/readiness-check.md`
- `{workspace_root}/planning/delivery-structure.md`
- `{workspace_root}/architecture/architecture-review.md`
- `{workspace_root}/architecture/architecture-rules.md`

Do not start writing until all available inputs are read completely.

### Step 2 - Create all five mandatory files under a deliverable folder:
- `delivery-spec.md`
- `implementation-plan.md`
- `tasks.md`
- `validation-plan.md`
- `review-checklist.md`

Keep story-level granularity and explicit FR/AC/AR traceability.

## Output requirements

Follow the structure described in `.b2s/artifact-templates/standalone-handoff.md`.

## Done criteria

- [ ] all five files exist
- [ ] planning is story-level, not epic-only
- [ ] tasks are concrete engineering actions
