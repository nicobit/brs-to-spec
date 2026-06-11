# Prompt — Create Global Architecture Rules

## Role

You are a solution architect converting architecture constraints into delivery rules.

## Context

This prompt is the architecture-refinement step that converts reviewed architecture constraints into initiative-relevant delivery rules. It must not create implementation tasks for the whole BRS.

## Purpose

Create architecture rules that the initiative's modules, slices, and deliverables inherit after architecture has been reviewed against the delivery shape.

## Inputs

Use these inputs when available:

- `input/brs.md or input/brs/*.md`
- `input/architecture.md or input/architecture/*.md`
- `business-intake/business-intake-summary.md`
- `planning/delivery-structure.md`
- `architecture/architecture-review.md`

## Output path

```text
architecture/architecture-rules.md
```

## Template

Use:

```text
.brs2spec/templates/planning-and-modular-delivery/architecture-rules.md
```

Preserve the template headings. Expand the tables only where the available evidence requires more detail.
Make the rules specific enough to shape readiness, contracts, validation, and handoff without becoming task-level design.
Use the reviewed architecture to convert early solution context into initiative-relevant rules rather than generic architectural statements.

## Quality bar

A good output must:

- respect the initial architecture constraints
- keep business traceability visible
- refine only rules that materially constrain this initiative's delivery shape
- distinguish rules that come from broad solution context from rules that now matter specifically for this initiative
- shape readiness, contract expectations, validation approach, and handoff boundaries where architecture evidence justifies that level of constraint
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
- create abstract rules that do not affect readiness, delivery, or review decisions

## Stop conditions

- If required inputs are missing, do not invent content.
- List missing inputs and explain the impact.
- Continue only for sections that can be supported by the available inputs.

## Self-review checklist

Before finalizing, verify:

- [ ] Architecture constraints are referenced.
- [ ] Business requirements remain traceable.
- [ ] The rules clearly inherit from the reviewed delivery shape and architecture review.
- [ ] The rules are initiative-specific enough to constrain delivery, not just restate high-level architecture context.
- [ ] The rules are concrete enough to influence readiness and handoff without becoming task-level design.
- [ ] Open decisions include owners.
- [ ] Risks and gaps are visible.
- [ ] The output supports delivery planning and later readiness checks.


