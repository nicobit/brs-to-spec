# Observability Plan

## Metadata

| Field | Value |
|---|---|
| Initiative | I003-admin-portal |
| Gate | Observability plan |
| Triggered | Yes |
| Required | Yes |
| Owner | Ops / SRE |
| Artifact | quality-gates/observability-plan.md |
| Status | Accepted |
| Reviewer | Ops / SRE |
| Review date | 2026-06-09 |

## Purpose

Define monitoring, diagnostics, alerting, dashboards and retention required to operate the Admin Portal and the Action Orchestrator (sync + async jobs).

## Summary

- Primary telemetry: Application Insights for app traces/requests; Log Analytics workspace for logs and diagnostic queries.
- Key signals: action invocation latency, job queue depth, job failure rate, long-running job duration, auth/authorization failures, inventory ingestion errors.
- Alerts must include runbook links and playbooks for high-severity incidents.

## Evidence

- IaC alert rules: [quality-gates/evidence/alert-rules.bicep](quality-gates/evidence/alert-rules.bicep) (draft)
- API contract: [quality-gates/evidence/admin-portal-actions-openapi.yaml](quality-gates/evidence/admin-portal-actions-openapi.yaml)

## Metrics & Alerts (examples)

- `ActionInvocationLatency`: P95 of POST /actions/* — alert if > X ms for 5m.
- `JobFailureRate`: percentage of jobs with status=failed — alert if > 2% over 15m.
- `JobQueueDepth`: length of pending job queue — alert if > threshold for 5m.
- `LongJobDuration`: job duration > expected (e.g., > 30m) — trigger paging alert.
- `AuthFailures`: spikes in 401/403 responses — investigate potential credential/config issues.

## Log Analytics Queries (examples)

Job failures (sample):

```
// sample KQL
AppRequests
| where RequestName startswith "/actions/"
| where ResultCode == "500"
| summarize count() by bin(TimeGenerated, 5m)
```

Async job status (sample):

```
Jobs
| where status == "failed"
| project job_id, status, error.message, finished_at
```

### Concrete KQL queries

# Observability Plan — I003 Admin Portal

## Metadata

| Field | Value |
|---|---|
| Initiative | I003-admin-portal |
| Gate | Observability plan |
| Triggered | Yes |
| Required | Yes |
| Owner | Ops / SRE |
| Artifact | quality-gates/observability-plan.md |
| Status | Accepted |
| Reviewer | Ops / SRE |
| Review date | 2026-06-09 |

## Purpose

Define monitoring, diagnostics, alerting, dashboards and retention required to operate the Admin Portal and the Action Orchestrator (sync + async jobs).

## Summary

- Primary telemetry: Application Insights for app traces/requests; Log Analytics workspace for logs and diagnostic queries.
- Key signals: action invocation latency, job queue depth, job failure rate, long-running job duration, auth/authorization failures, inventory ingestion errors.
- Alerts must include runbook links and playbooks for high-severity incidents.

## Evidence

- IaC alert rules: `quality-gates/evidence/alert-rules.bicep` (draft)
- API contract: `quality-gates/evidence/admin-portal-actions-openapi.yaml`

## Metrics & Alerts (examples)

- `ActionInvocationLatency`: P95 of POST /actions/* — alert if > X ms for 5m.
- `JobFailureRate`: percentage of jobs with status=failed — alert if > 2% over 15m.
- `JobQueueDepth`: length of pending job queue — alert if > threshold for 5m.
- `LongJobDuration`: job duration > expected (e.g., > 30m) — trigger paging alert.
- `AuthFailures`: spikes in 401/403 responses — investigate potential credential/config issues.

## Log Analytics Queries (examples)

Job failures (sample):

```
// sample KQL
AppRequests
| where RequestName startswith "/actions/"
| where ResultCode == "500"
| summarize count() by bin(TimeGenerated, 5m)
```

Async job status (sample):

```
Jobs
| where status == "failed"
| project job_id, status, error.message, finished_at
```

### Concrete KQL queries

- Job failure rate (15m):

```
// Job failure rate over 15m
Jobs
| where TimeGenerated > ago(15m)
| summarize failures = countif(status == 'failed'), total = count()
| extend failure_rate = todouble(failures) / todouble(total) * 100
| where failure_rate > 2
```

- Action invocation P95 latency (5m):

```
requests
| where Url startswith "/actions/" and Timestamp > ago(5m)
| summarize p95 = percentiles(duration, 95)
| where p95 > 2000
```

## Dashboards

- Overview: Action throughput, latency histograms, job queue depth, failure trend.
- On-call: active alerts, top failing tenants, recent job traces.

## Runbooks / Response

- Playbook: Investigate failed job
  1. Open job status: `GET /jobs/{jobId}` → inspect `error` and `audit` fields.
  2. Open trace in Application Insights using `trace_id` from job metadata.
  3. Run Log Analytics query filtered by resourceId and correlation id.
  4. If action touched a resource and failed, consult subscription activity logs.

## Observability Acceptance Criteria

- Trace propagation across frontend → API → job processor verified with sample flows.
- Diagnostic deep-link generator available and validated for sample subscription IDs.
- Alerts configured and tested for P1 and P2 scenarios; playbooks documented.
- Dashboards created with key metrics and linked in this artifact.

## Evidence (selected)

- Application Insights instrumentation sample (code snippet)
- Log Analytics sample queries and shared dashboard UID
- Alert rules JSON or ARM/Bicep snippets
- Dashboard JSON: `quality-gates/evidence/observability-dashboard.json`

---

Observability plan reviewed and `Status: Accepted` by Ops/SRE on 2026-06-09. Attach additional evidence under `quality-gates/evidence/` as produced.
- Dashboards for SRE and Platform/Ops

## Instrumentation & Telemetry
- Use OpenTelemetry (traces + metrics) or Application Insights SDK for backend services.
- Correlate frontend requests and backend job processing via `trace_id` / `correlation_id` propagated in headers.
- Emit spans for: action invocation, job enqueue, job start, job complete, job failure, resource calls (start/restart), and audit writes.
- Minimum metrics:
  - `actions.request.count` (by tenant, action, result)
  - `actions.request.duration` (histogram)
  - `jobs.queue_depth` (gauge per queue/tenant)
  - `jobs.duration` (histogram)
  - `jobs.failures` (counter)
  - `audit.events.written` (counter)

## Diagnostic Links
- For each resource row in inventory, surface a Log Analytics link pre-populated with a sample query that filters by `resourceId` and time range.
- Example Log Analytics link (conceptual):
  - Query:

```
AzureDiagnostics
| where ResourceId == "{resourceId}"
| where TimeGenerated > ago(1h)
| sort by TimeGenerated desc
```

- Provide a helper endpoint to construct deep links to Application Insights traces and Log Analytics queries.

## Alerts & Thresholds
- High-severity (P1) alerts (notify on-call immediately):
  - `jobs.queue_depth` > 100 for 5m
  - `jobs.failures` rate > 5% of job starts in 10m window
  - Action invocation returning 5xx > 1% over 5m for critical actions
  - Audit write failures > 0 (indicates potential data-loss)
- Medium-severity (P2) alerts (email/Teams):
  - `actions.request.duration` p95 > configured SLA (e.g., 30s) for 10m
  - Intermittent auth failures > threshold
- Alert routing: use Action Groups to forward P1 to PagerDuty/Teams + Email and P2 to Teams channel.

## Retention & Costs
- Retain metrics at high resolution for 30 days, aggregated metrics for 90 days.
- Retain traces and logs at full fidelity for 30 days; consider sampled traces for 90+ day retention.
- Audit store retention policy: 365 days by default (comply with compliance requirements); export to cold storage as required.

## Dashboards
- SRE Dashboard: queue depth, job durations, failure rates, top failing actions, per-tenant health.
- Platform Dashboard: number of provisioned service principals, role assignment failures, subscription validation status.
- Product Ops Dashboard: inventory counts, recent audit events, top user actions.

## Diagnostic Playbooks
- Playbook: Investigate failed job
  1. Open job status: `GET /jobs/{jobId}` → inspect `error` and `audit` fields.
  2. Open trace in Application Insights using `trace_id` from job metadata.
  3. Run Log Analytics query filtered by resourceId and correlation id.
  4. If action touched a resource and failed, consult subscription activity logs.

## Observability Acceptance Criteria
- Trace propagation across frontend → API → job processor verified with sample flows.
- Diagnostic deep-link generator available and validated for sample subscription IDs.
- Alerts configured and tested for P1 and P2 scenarios; playbooks documented.
- Dashboards created with key metrics and linked in this artifact.

## Evidence (suggested)
- Application Insights instrumentation sample (code snippet)
- Log Analytics sample queries and shared dashboard UID
- Alert rules JSON or ARM/Bicep snippets
- Screenshot or link to created dashboards

---

Draft observability plan to satisfy the readiness-triggered gate. Attach evidence artifacts under `quality-gates/evidence/` as they are produced.
