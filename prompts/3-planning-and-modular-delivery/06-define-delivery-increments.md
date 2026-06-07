# Prompt — Define Delivery Increments

## Role

You are a delivery architect slicing the initiative into vertical increments.

## Context

This prompt is part of architecture-aware planning. It must not create implementation tasks for the whole BRS.

## Purpose

Create vertical, testable delivery increments for one-at-a-time execution.

## Inputs

Use these inputs when available:

- `input/brs.md`
- `input/initial-architecture.md`
- `business-intake/business-intake-summary.md`
- `architecture/initial-architecture-review.md`
- `architecture/global-architecture-rules.md`

## Output path

```text
planning/delivery-increments.md
```

## Required output structure

```markdown
# Artifact

## Summary

## Key Decisions

| Decision ID | Decision | Evidence | Risk | Owner |
|---|---|---|---|---|

## Main Table

| ID | Item | Source | Impact | Evidence | Risk / Gap | Owner |
|---|---|---|---|---|---|---|

## Architecture Constraints Applied

| Constraint ID | Constraint | Applied how? | Evidence | Gap |
|---|---|---|---|---|

## Traceability

| Requirement ID | Capability | Module / Component | Deliverable | Validation |
|---|---|---|---|---|

## Conflicts / Open Decisions

| ID | Conflict / Decision | Impact | Owner | Required before |
|---|---|---|---|---|

## Recommendations
```

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
