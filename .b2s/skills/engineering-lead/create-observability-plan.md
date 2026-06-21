# Skill - Create Observability Plan

## Identity

```text
skill_id:    engineering-lead.create-observability-plan
persona:     engineering-lead
action_id:   create-observability-plan
produces:    quality-gates/observability-plan.md
```

## When this skill is used

Run this only when the readiness check explicitly triggers the observability gate.

## Preconditions

Before starting, verify:
- `engineering-readiness/readiness-check.md` marks Observability Plan as triggered
- BRS source files are readable
- `architecture/architecture-review.md` exists
- `architecture/architecture-rules.md` exists

## Instructions

### Step 1 - Read all inputs

Read every file listed in `{resolved_required_inputs}` in full before writing anything.

If `{resolved_optional_inputs}` is not empty, read those files as well.
Read every policy file listed in `{resolved_policy_inputs}` in full before writing.

Do not start writing until all available inputs are read completely.

### Step 2 - Define logs, metrics, traces, alerts, dashboards, runbook notes, and support diagnostics for each new operational flow and SLI/SLO concern.

Apply the policy context from `{resolved_policy_inputs}`:
- make availability and performance expectations observable
- ensure log design is safe for PII and compliance concerns
- connect operational concerns to concrete tests, alerts, and runbook signals

## Output requirements

Write `quality-gates/observability-plan.md` using `.b2s/artifact-templates/observability-plan.md`.

## Done criteria

- [ ] Operational flows have observability coverage
- [ ] SLI/SLO requirements map to metrics and alerts
- [ ] PII safety is explicit in log design
- [ ] Status is `In progress`
