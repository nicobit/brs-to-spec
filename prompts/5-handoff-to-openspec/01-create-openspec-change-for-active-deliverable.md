# Prompt — Create OpenSpec Change for Active Deliverable

## Purpose

Create one OpenSpec change for the active delivery increment only.

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

## Output folder

```text
openspec/changes/<deliverable-id>-<deliverable-name>/
  proposal.md
  design.md
  tasks.md
```

## Proposal output

Include:
- why this deliverable is needed,
- what scope is included,
- what scope is excluded,
- which requirements/capabilities are covered,
- which modules are touched,
- which architecture constraints apply.

## Design output

Include:
- architecture constraints applied,
- module changes,
- API/data contracts,
- key design decisions,
- dependencies,
- risks,
- validation strategy,
- architecture conflicts/open decisions.

## Tasks output

Create small, sequential engineering tasks for this deliverable only.

Each task must include:
- objective,
- files likely to change,
- implementation note,
- explicit automated validation sub-task,
- completion criteria.

## Rules

- Do not create tasks for future deliverables.
- Do not violate initial architecture constraints.
- Do not create a second task system outside OpenSpec.
- Every task should include test or validation.
