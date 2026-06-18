# Prompt 22 - Create Observability Plan

## Inputs to give Copilot

Required:

- `initiatives/<id>-<slug>/engineering-readiness/readiness-check.md`
- `initiatives/<id>-<slug>/architecture/architecture-review.md`
- `initiatives/<id>-<slug>/architecture/architecture-rules.md`
- `initiatives/<id>-<slug>/input/brs.md`
- any additional BRS markdown files under the initiative input folder
- `.b2s/artifact-templates/observability-plan.md`

## Output file to create

- `initiatives/<id>-<slug>/quality-gates/observability-plan.md`

## Prompt for Office 365 Copilot

You are following the `.b2s` framework action `create-observability-plan`.

Run this only when `Observability Plan` is explicitly triggered in the readiness
check. If not triggered, stop and say the action does not apply.

Read all provided inputs in full before writing anything.

Define:

- logs
- metrics
- traces
- alerts
- dashboards
- runbook notes
- support diagnostics

Do this for each new operational flow and each SLI or SLO concern.

Write `quality-gates/observability-plan.md` using the provided template.

Before finalizing, ensure operational flows have observability coverage, SLI/SLO
needs map to metrics and alerts, and PII safety is explicit in log design.
Status must be `In progress`.
