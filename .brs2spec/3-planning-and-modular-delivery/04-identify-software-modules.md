# Prompt â€” Identify Software Modules

## Role

You are a software architect decomposing a large initiative into coherent modules.

## Context

This prompt is part of architecture-aware planning. It must not create implementation tasks for the whole BRS.

## Purpose

Identify modules while preserving business traceability and architecture constraints.

## Inputs

Use these inputs when available:

- `input/brs.md or input/brs/*.md`
- `input/architecture.md or input/architecture/*.md`
- `business-intake/business-intake-summary.md`
- `architecture/architecture-review.md`
- `architecture/architecture-rules.md`

## Output path

```text
modules/software-modules.md
```

## Template

Use:

```text
.brs2spec/templates/planning-and-modular-delivery/software-modules.md
```

Preserve the template headings and add structure only where the evidence demands it.

## Quality bar

A good output must:

- respect the initial architecture constraints
- keep business traceability visible
- mark conflicts instead of resolving them silently
- assign owners for gaps and decisions
- avoid creating low-level implementation tasks

## Anti-patterns to avoid

Do not produce outputs that:

- invent architecture not present in the inputs
- slice work only by technical layer
- create tasks for all future deliverables
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
- [ ] Open decisions include owners.
- [ ] Risks and gaps are visible.
- [ ] The output supports the next workflow step.


