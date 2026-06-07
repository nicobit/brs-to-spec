# Prompt — Create Standalone Delivery Package (Execution Mode B)

## Purpose

Create a self-contained delivery package for the active deliverable when
**OpenSpec is not used** (Execution Mode B — Standalone).

This package keeps the **same discipline** as the OpenSpec path — clear scope,
architecture constraints, small tasks, validation, and review gates — but it does
**not** pretend to be OpenSpec. It is the source of truth for engineering
execution in standalone mode.

## When to use

Use this instead of `01-create-openspec-change-for-active-deliverable.md` when the
routing decision selected **Execution Mode B — Standalone**.

## Inputs

Use:
- `input/brs.md`
- `input/initial-architecture.md`
- `business-intake/business-intake-summary.md`
- `architecture/initial-architecture-review.md`
- `architecture/global-architecture-rules.md`
- `planning/delivery-increments.md`
- `planning/traceability-matrix.md`
- `engineering-readiness/readiness-check.md`
- any triggered `quality-gates/*` artifacts.

## Output folder

```text
standalone-delivery/<deliverable-id>-<deliverable-name>/
  delivery-spec.md
  implementation-plan.md
  tasks.md
  validation-plan.md
  review-checklist.md
```

## delivery-spec.md

Include:
- why this deliverable is needed,
- in scope / out of scope,
- requirements / capabilities covered,
- modules touched,
- architecture constraints applied (from the initial architecture document),
- acceptance criteria,
- risks and open decisions.

## implementation-plan.md

Include:
- approach and sequencing,
- module-level changes,
- dependencies,
- key technical decisions consistent with the architecture constraints.

## tasks.md

Create small, sequential engineering tasks for **this deliverable only**.

Each task must include:
- objective,
- files likely to change,
- implementation note,
- explicit automated validation sub-task,
- completion criteria.

## validation-plan.md

Include:
- how the deliverable is validated,
- automated test expectations,
- links to any triggered quality gates (BDD scenarios, test strategy, etc.).

## review-checklist.md

Include the review gates that must pass before merge or release, including any
**triggered Conditional Quality Gates** from the readiness check.

## Rules

- Do not create tasks for future deliverables.
- Do not violate initial architecture constraints.
- Do not duplicate the OpenSpec output tree — standalone uses
  `standalone-delivery/`, not `openspec/changes/`.
- Every task must include test or validation.
- Standalone mode remains the single source of truth for execution; do not also
  create an OpenSpec change for the same deliverable.
