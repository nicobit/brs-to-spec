# Prompt 25 - Create Standalone Handoff

## Inputs to give Copilot

Required:

- `initiatives/<id>-<slug>/engineering-readiness/readiness-check.md`
- `initiatives/<id>-<slug>/planning/delivery-structure.md`
- `initiatives/<id>-<slug>/architecture/architecture-review.md`
- `initiatives/<id>-<slug>/architecture/architecture-rules.md`
- `.b2s/artifact-templates/standalone-handoff.md`

## Output files to create

- the required files under `initiatives/<id>-<slug>/standalone-delivery/`

## Prompt for Office 365 Copilot

You are following the `.b2s` framework action `create-standalone-handoff`.

Run this only when:

- delivery mode is `Standalone`
- readiness decision is `Ready`
- all triggered gates are accepted

Read all provided inputs in full before writing anything.

Create all five mandatory files under the standalone delivery folder:

- `delivery-spec.md`
- `implementation-plan.md`
- `tasks.md`
- `validation-plan.md`
- `review-checklist.md`

Keep story-level granularity and explicit FR, AC, and AR traceability.
