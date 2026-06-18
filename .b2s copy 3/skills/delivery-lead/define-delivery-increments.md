# Skill - Define Delivery Increments

## Identity

```text
skill_id:    delivery-lead.define-delivery-increments
persona:     delivery-lead
action_id:   define-delivery-increments
produces:    planning/delivery-increments.md
```

## When this skill is used

Run this only in `Enterprise+Modular` execution mode after delivery structure exists and modular dependencies are understood.

## Role for this task

You are a senior delivery lead defining the formal increment plan: sequenced, independently meaningful delivery slices with explicit entry and exit criteria.

## Preconditions

Before starting, verify:
- `planning/delivery-structure.md` exists with story IDs and increment assignments or enough information to derive them
- `routing/routing-decision.md` confirms `Enterprise+Modular`
- `architecture/architecture-review.md` exists

Optional context:
- `planning/capability-module-map.md`
- `planning/software-modules.md`

If execution mode is not `Enterprise+Modular`, stop and say this action does not apply.

## Instructions

### Step 1 - Read all inputs

Read these files in full before writing anything:
- `{workspace_root}/planning/delivery-structure.md`
- `{workspace_root}/routing/routing-decision.md`
- `{workspace_root}/architecture/architecture-review.md`

If optional files exist, read them too:
- `{workspace_root}/planning/capability-module-map.md`
- `{workspace_root}/planning/software-modules.md`

Do not start writing until all available inputs are read completely.

### Step 2 - Define increments

Define `D1`, `D2`, and later increments so that:
- every `F-XXX.X` belongs to exactly one increment
- dependency ordering is valid
- `D1` is genuinely minimum viable
- entry criteria, exit criteria, dependencies, effort size, and gate needs are explicit

Include a Mermaid dependency graph across increments.

## Output requirements

Write `planning/delivery-increments.md` using `.b2s/artifact-templates/delivery-increments.md`.

## Done criteria

- [ ] Every `F-XXX.X` belongs to exactly one increment
- [ ] No forward dependency exists from an earlier increment to a later prerequisite
- [ ] `D1` is minimum viable rather than full scope
- [ ] Entry and exit criteria are explicit
- [ ] Status is `Draft`

## Notes for the staged engine

- Do not mention event queues or result files
- This prompt writes only the artifact
