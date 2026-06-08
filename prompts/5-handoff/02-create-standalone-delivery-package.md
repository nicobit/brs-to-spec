# Prompt - Create Standalone Delivery Package

## Role

You are an engineering lead preparing a disciplined standalone delivery package when OpenSpec is not used.

## Context

This prompt is used only when execution mode is Standalone. Standalone mode must not be lower quality than OpenSpec mode.

## Purpose

Create a delivery package with scope, design approach, tasks, validation, review checklist, and initiative traceability.

## Inputs

Use these inputs when available:

- `engineering-readiness/readiness-check.md`
- `quality-gates/*.md`
- `planning/traceability-matrix.md`
- `architecture/architecture-rules.md`
- `business-intake/business-intake-summary.md`
- `perspectives/agile-planning/gitlab-planning-view.md` when a planning view exists

## Output path

```text
standalone-delivery/D1-<deliverable-name>/
```

## Templates

Use:

```text
templates/standalone-delivery/delivery-spec.md
templates/standalone-delivery/implementation-plan.md
templates/standalone-delivery/tasks.md
templates/standalone-delivery/validation-plan.md
templates/standalone-delivery/review-checklist.md
```

Preserve the template headings in each file and add detail only where the evidence demands it.

## Quality bar

A good output must:

- make standalone mode disciplined and reviewable
- include quality gates and accepted risks
- make tasks small and validation-oriented
- include evidence expected for each task
- convert business planning items into engineering-ready implementation tasks
- reference requirements, user stories when available, acceptance sources, architecture constraints, and quality gates
- state out of scope clearly

## Anti-patterns to avoid

Do not produce outputs that:

- treat standalone as informal notes
- skip validation because OpenSpec is not used
- copy user stories directly as implementation tasks
- create broad tasks without evidence
- ignore required quality gates
- invent architecture

## Stop conditions

- If required inputs are missing, do not invent content.
- List missing inputs and explain the impact.
- Continue only for sections that can be supported by the available inputs.

## Self-review checklist

Before finalizing, verify:

- [ ] Delivery spec includes scope and constraints.
- [ ] Tasks include traceability back to requirement, user story when available, acceptance source, architecture constraint, and quality gate.
- [ ] Tasks include validation and evidence.
- [ ] Quality gates are reflected.
- [ ] Review checklist is complete.
- [ ] Standalone output is usable by engineering.
