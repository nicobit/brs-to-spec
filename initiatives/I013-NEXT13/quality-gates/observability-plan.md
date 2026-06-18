## Metadata

- Initiative: I013-NEXT13
- Artifact: Observability Plan
- Author: b2s-agent
- Status: Draft

## Key Metrics and SLIs

- Request latency (p50/p95/p99) for `/decisions` and `/loans` endpoints.
- Error rate (5xx) and success rate for critical flows.
- Throughput (requests/sec) and queue lengths for async processors.

## SLOs

- p95 latency < 500ms for decision endpoint; error rate < 0.5%.

## Tracing and Distributed Context

- Ensure all services propagate correlation IDs and instrument spans for decisioning flows.

## Logging and Structured Events

- Centralized structured logs with JSON schema; include correlation id, tenant, environment.

## Dashboards and Runbooks

- Dashboards for latency, error rate, queue depth, and resource utilization; runbooks for common alerts.

## Alerting and Escalation

- Pager duty integration for critical SLO breaches; alerts tuned to actionable thresholds.

## Ownership

- Observability: Platform SRE; Application owners: feature teams.

## Observability Scope

- Instrumentation across API gateways, decision engine, and payment integration.

## Logs

- Structured application logs captured centrally; include context and sanitized PII.

## Metrics

- Latency, error rates, queue sizes, DB connection pool metrics, cache hit ratios.

## Traces

- Distributed tracing with sampled spans for decision flows; capture key span tags.

## Alerts

- Define alert thresholds tied to SLOs with actionable runbooks for on-call.

## Runbook Notes

- For high error-rate alerts: check service logs, trace flows, and dependency status; roll back if necessary.

## Support Diagnostics

- Capture request/response examples, correlation ids, and recent deployment metadata to aid debugging.

## Accepted Risks

- Sampling in tracing may miss rare edge-case failures; increase sampling during incident windows.
