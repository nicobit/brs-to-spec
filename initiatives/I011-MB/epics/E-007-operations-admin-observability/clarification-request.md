# Epic Clarification Request — E-007 Operations, Admin & Observability

## Summary

WHEN preparing the Operations & Observability epic, THE TEAM REQUIRES CLARIFICATION on metrics retention, alerting thresholds, and multi-tenant data separation.

## Blocking Questions

| ID | Route | Page | Question | Why It Matters | Required For |
|---|---|---|---|---|---|
| OAQ-101 | /api/v1/metrics | Metrics ingest | What is the retention policy and aggregation window for metrics (raw retention, rollup cadence)? | Drives storage costs, query performance, and dashboard accuracy. | Data storage design, retention, rollups |
| OAQ-102 | alerting config | Alerts | What are the default alert severities and escalation paths for thresholds? | Ensures consistent operational responses and on-call procedures. | Alerting rules, notification pipelines |
| OAQ-103 | /api/v1/metrics | Metrics ingest | Is multi-tenant separation required (per-customer metric isolation) and how is tenant identified? | Affects data partitioning, access control, and billing. | Data model, ingestion pipeline, RBAC |
| OAQ-104 | /api/v1/admin/flags | Admin API | Are feature flags managed centrally or per-environment, and what role can update them? | Affects admin UI and RBAC for feature toggles. | Admin stories, API auth |

## Answer Instructions

Record answers in:

```text
input/clarifications/E-007.yaml
```

Include `id`, `answer`, `rationale`, `answered_at`, and `owner` for each answered question.

*End of clarification request.*
