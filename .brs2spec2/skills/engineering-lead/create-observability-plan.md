# Skill — Create Observability Plan

## Identity

| Field | Value |
|---|---|
| skill_id | eng-create-observability-plan |
| persona | engineering-lead |
| event_types | CREATE_OBSERVABILITY_PLAN |
| produces | quality-gates/observability-plan.md |

## When this skill is used

Conditional quality gate — triggered when `engineering-readiness/readiness-check.md` marks Observability Plan Triggered = Yes.

Observability plan trigger conditions (ANY of these):
- A new operational flow is introduced
- SLI/SLO requirements exist in the BRS
- An alerting need is introduced

## Role for this task

You are a senior SRE performing a Conditional Quality Gate review — defining logs, metrics, traces, alerts, dashboards, runbook notes, and support diagnostics for the initiative.

## Prerequisites check

Before starting, verify:
- [ ] `engineering-readiness/readiness-check.md` marks Observability Plan as Triggered = Yes
- [ ] `input/brs.md` is readable
- [ ] `architecture/architecture-review.md` exists
- [ ] `architecture/architecture-rules.md` exists

If this gate was NOT triggered: stop and state that the observability plan should not be run.

## Instructions

### Step 1 — Define observability scope

From the BRS and architecture review:
- Which new operational flows are introduced? (each flow = a monitoring scope boundary)
- What SLI/SLO requirements are stated in the BRS?
- What alert conditions are implied by the functional requirements? (failure states, thresholds, timeouts)

### Step 2 — Define logs

For each significant system event:
- What is logged? (event type, correlation ID, user/actor, action, outcome)
- At what log level? (DEBUG / INFO / WARN / ERROR / CRITICAL)
- PII safety: confirm no PII appears in log lines (reference data-contract.md PII fields)
- Structured format requirement (JSON, key-value, plain text)

### Step 3 — Define metrics

For each SLI from the BRS or implied by functional requirements:
- Metric name (following agreed naming convention)
- Type: counter / gauge / histogram / summary
- Labels: which dimensions to record (e.g. endpoint, status_code, tenant_id)
- Collection interval
- SLO target (if stated in BRS)

### Step 4 — Define traces

For each async or multi-service flow:
- What spans are needed?
- What attributes must each span carry?
- What is the trace sampling strategy?
- Is distributed tracing required across service boundaries?

### Step 5 — Define alerts

For each operational concern:
- Alert name and condition (metric threshold, error rate, latency breach)
- Severity: P1 / P2 / P3
- Trigger threshold and sustained window
- Auto-resolve condition
- On-call owner

### Step 6 — Define dashboards and runbook notes

- Which panels are needed for on-call visibility?
- What runbook steps are needed when an alert fires?
- What support diagnostic commands or queries are needed?

### Step 7 — Write the artifact

The output must start with `## Metadata` and `| **Status** | **In progress** |`.

## Output requirements

The artifact must contain:
- Metadata table with Status, Initiative ID, creation date
- Observability scope summary
- Logs specification table: Event, Level, Fields, PII-safe?
- Metrics catalog: Name, Type, Labels, SLO target
- Traces specification: Flow, Spans, Attributes, Sampling
- Alerts catalog: Name, Condition, Severity, Threshold, Owner
- Dashboard panels list
- Runbook notes per alert
- Accepted risks

## Done criteria

- [ ] All new operational flows have log, metric, and alert coverage
- [ ] SLI/SLO requirements from BRS are reflected in metrics and alerts
- [ ] PII safety confirmed in log specification
- [ ] Every alert has severity, threshold, and owner
- [ ] `Status: In progress` in the Metadata table
- [ ] Result file written with `status: pass` and `artifacts_written` listing `quality-gates/observability-plan.md`

## Stop conditions

- If this gate was not triggered: stop immediately.
- Do not invent operational requirements not present in the BRS or architecture.
