# Observability Spec — {{Deliverable ID}}: {{Deliverable Name}}

> Distilled from `quality-gates/observability-plan.md` for this increment only.
> Full alert rules, dashboard JSON, and runbooks are in the source gate artifact.
> **These signals are mandatory — not optional.** Every implementation task that touches a listed component must emit the listed events.

## SLOs that apply to this increment

| SLO | Target | Measured by |
|---|---|---|

## Events to emit

| Event / metric | Type | Emitted by | When | Labels |
|---|---|---|---|---|

<!-- Type: Counter / Histogram / Gauge -->
<!-- When: on each occurrence — be specific (e.g. "on 202 response from POST /onboarding") -->
<!-- Labels: key/value dimensions to attach -->

## Tracing

- Correlation ID: <!-- how it flows through the system (header name, propagation) -->
- Spans to create: <!-- list span names per component boundary -->
- Sampling: <!-- e.g. 100% errors, 10% success -->
- PII in traces: <!-- fields that must be redacted before trace export -->

## Alerts (this increment)

| Alert | Condition | Severity | On-call channel |
|---|---|---|---|

<!-- Paste only alerts relevant to components built in this increment. -->

## Runbooks (links)

| Scenario | Runbook location |
|---|---|

<!-- Reference runbooks in quality-gates/observability-plan.md — do not duplicate them here. -->
