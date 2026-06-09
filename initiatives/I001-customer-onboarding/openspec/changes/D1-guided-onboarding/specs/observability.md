# Observability Spec — D1: Guided Onboarding (MVP)

> Distilled from `quality-gates/observability-plan.md` for this increment only.
> Full dashboard JSON, alert rule expressions, and runbooks are in `quality-gates/observability-plan.md`.
> **All signals below are mandatory** — every task that touches the listed component must emit them.

## SLOs that apply to D1

| SLO | Target | Measured by |
|---|---|---|
| IDP verification latency p95 | < 30 000 ms | `verification_latency_ms` histogram |
| Onboarding success rate | ≥ 95% of started flows complete (pilot target) | `onboarding_success / onboarding_start` |

## Events to emit

| Event / metric | Type | Emitted by | When | Labels |
|---|---|---|---|---|
| `onboarding_start` | Counter | Onboarding API | On `POST /onboarding` — 202 response only | — |
| `onboarding_success` | Counter | Webhook handler | On IDP callback `result = verified` | — |
| `onboarding_failure` | Counter | API or Webhook handler | On any failure (IDP error, timeout, invalid input) | `reason` (e.g. `idp_timeout`), `stage` (e.g. `verification`) |
| `verification_latency_ms` | Histogram (p50/p95/p99) | Webhook handler | Time from `submitted_at` to webhook `completed_at` | — |
| `idp_requests_total` | Counter | IDP client | On each outbound IDP call attempt | — |
| `idp_errors_total` | Counter | IDP client | On IDP API error or timeout | `error_code` |
| `idp_webhook_received` | Counter | Webhook handler | On every webhook receipt (before signature check) | `status` (valid/invalid) |

## Tracing

- **Correlation ID:** W3C `traceparent` header — injected at API gateway, propagated downstream
- **Spans to create:**

| Span name | Created by | Covers |
|---|---|---|
| `onboarding.request` | Onboarding API | Entire `POST /onboarding` handler |
| `idp.request` | IDP client | Outbound IDP API call |
| `idp.webhook` | Webhook handler | Entire webhook processing (signature → DB update → queue) |
| `email.send` | Notification job | SendGrid API call |

- **Sampling:** 100% for all error spans; 10% for success spans
- **PII in traces:** `email`, `phone`, and IDP payload fields must not appear in span attributes or log fields — redact at emission point, not at aggregation layer

## Alerts (D1 components)

| Alert | Condition | Severity | Notification |
|---|---|---|---|
| High onboarding failure rate | `onboarding_failure_total[15m] / onboarding_start_total[15m] > 0.05` | P1 — Pager | SRE on-call, Integration |
| IDP webhook invalid signatures | `idp_webhook_received{status="invalid"}[15m] > 5` | P2 — Notify | Integration, Security |
| IDP errors | `idp_errors_total[15m] > 10` | P2 — Notify | Integration on-call |

Tune thresholds against pilot traffic before enabling pager rules in production.

## Runbooks (by reference)

| Scenario | Location |
|---|---|
| High onboarding failure rate | `quality-gates/observability-plan.md` — Runbook: Onboarding High Failure Rate |
| IDP webhook failure | `quality-gates/observability-plan.md` — Runbook: IDP Webhook Failure |

Do not duplicate runbook content here — reference the source.
