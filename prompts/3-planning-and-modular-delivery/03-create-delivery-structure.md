# Prompt â€” Create Delivery Structure

## Role

You are a delivery architect structuring business scope into deliverable units.

## Context

This prompt is part of architecture-aware planning. It must not create implementation tasks for the whole BRS.

## Purpose

Create a delivery structure connecting objectives, capabilities, candidate increments and architecture impact.

## Inputs

Use these inputs when available:

- `input/brs.md or input/brs/*.md`
- `input/architecture.md or input/architecture/*.md`
- `business-intake/business-intake-summary.md`
- `architecture/architecture-review.md`
- `architecture/architecture-rules.md`

## Output path

```text
planning/delivery-structure.md
```

## Template

Use:

```text
templates/planning-and-modular-delivery/delivery-structure.md
```

Preserve the template headings. Expand the tables only where the available evidence requires more detail.

## Quality bar

A good output must:

- respect the initial architecture constraints
- keep business traceability visible
- make governed service/API, data, and event boundaries explicit where they exist
- mark conflicts instead of resolving them silently
- assign owners for gaps and decisions
- avoid creating low-level implementation tasks

## Anti-patterns to avoid

Do not produce outputs that:

- invent architecture not present in the inputs
- slice work only by technical layer
- create tasks for all future deliverables
- hide governed boundary changes inside generic capability names
- ignore architecture conflicts
- produce a table without evidence or owner

## Stop conditions

- If required inputs are missing, do not invent content.
- List missing inputs and explain the impact.
- Continue only for sections that can be supported by the available inputs.

## Self-review checklist

Before finalizing, verify:

- [ ] Architecture constraints are referenced.
- [ ] Business requirements remain traceable.
- [ ] Governed service/API, data, and event boundaries are visible where relevant.
- [ ] Open decisions include owners.
- [ ] Risks and gaps are visible.
- [ ] The output supports the next workflow step.


