# Observability Spec — {{F-XXX.X}}: {{User Story Name}}

> Distilled from `quality-gates/observability-plan.md` for this user story only.
> Only signals emitted by components built in this story appear here.
> Full alert rules, dashboard queries, and runbooks are in `quality-gates/observability-plan.md`.
> Delete this file if this story emits no telemetry signals.
> **All signals listed here are mandatory — not optional.**

## Signals to emit

| Signal | Type | Emitted by | When | Labels |
|---|---|---|---|---|

## Tracing

- Span name: <!-- span name for the operation this story adds -->
- Correlation ID: <!-- how it flows through this story's components -->
- PII in traces: <!-- fields that must be redacted, or "none" -->

## Alerts (if this story introduces new alert conditions)

| Alert | Condition | Severity | Notification |
|---|---|---|---|

<!-- Omit this section if this story adds no new alert conditions. -->

## Runbooks (by reference)

| Scenario | Location |
|---|---|

<!-- Reference runbooks by path — do not duplicate content here. -->
<!-- Omit if this story adds no new runbook scenarios. -->
