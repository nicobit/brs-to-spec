# Observability Plan Quality Gate

> Primary consumer: Platform / SRE, Engineering, Product
> Purpose: define telemetry, dashboards, alerts, and runbooks required to validate NFRs and support operations before handoff

## Metadata

| Field | Value |
|---|---|
| Initiative | I001 — Customer Onboarding |
| Gate owner | Platform / SRE |
| Review date | 2026-06-09 |
| Status | Accepted |
| Source artifacts | `input/brs.md`, `input/architecture.md`, `engineering-readiness/readiness-check.md` |

## SLOs

| SLO | Target | Owner |
|---|---|---|
| Service availability | 99.9% monthly | Platform / Ops |
| Verification latency p95 | < 30 000 ms | Integration |
| Onboarding success rate | ≥ 95% (primary persona) | Product |
| Conversion rate | ≥ 25% (pilot cohort) | Product |

## Telemetry Event Catalog

| Event / metric | Type | Emitted by | Purpose |
|---|---|---|---|
| `onboarding_start` | Counter | API / Frontend | Count initiated flows |
| `onboarding_success` | Counter | API | Count completions |
| `onboarding_failure` | Counter + reason label | API | Count failures by stage |
| `verification_latency_ms` | Histogram (p50/p95/p99) | API / IDP handler | IDP latency SLO |
| `onboarding_in_progress` | Gauge | API | Concurrent flows |
| `idp_requests_total` | Counter | IDP client | IDP call volume |
| `idp_errors_total` | Counter + code label | IDP client | IDP failures |
| `idp_webhook_received` | Counter | Webhook handler | Webhook delivery tracking |
| `idp_webhook_processing_delay_seconds` | Histogram | Webhook handler | Webhook lag |
| `payment_validation_errors_total` | Counter | Payment client | Payment failures |
| `support_retries_total` | Counter | Support UI | Manual retries |

## Instrumentation Points

| Component | Spans / events to emit | Notes |
|---|---|---|
| Frontend | `onboarding_start`, correlation id | Pass W3C trace context downstream |
| API / Orchestrator | `onboarding.request`, `onboarding_success`, `onboarding_failure`, `idp.request`, `email.send`, `db.write` | Attach span ids; propagate correlation id |
| IDP webhook handler | `idp.webhook`, `idp_webhook_received`, webhook lag | Validate signature before emitting |
| Background queue | Job status, retry counts | Include `onboarding_id` in all job payloads |
| Support UI | `support_retries_total`, manual actions | Audited actions only |

Tracing: use distributed tracing with correlation ids through frontend → API → IDP → webhook → background job. Span names as above. Sampling: 100% for errors, ≥ 10% for success paths.

## Dashboards

| Dashboard | Key panels | Primary consumer |
|---|---|---|
| Onboarding Health Overview | Throughput (starts/min), success rate (1h/24h rolling), p95 latency, concurrent flows, recent failures table | Product, SRE |
| Integration Health — IDP | IDP request rate, IDP failure rate, webhook lag distribution, recent webhook events | Integration, SRE |
| Integration Health — Payment | Payment validation rate, error count, latency | Integration |
| Support View | Recent failed flows with correlation ids, top failure reasons, retry counts, manual interventions | Support, SRE |

Sample queries (Prometheus-style):

```
# Onboarding success rate (1h)
1 - (increase(onboarding_failure_total[1h]) / increase(onboarding_start_total[1h]))

# IDP p95 verification latency
histogram_quantile(0.95, sum(rate(verification_latency_ms_bucket[5m])) by (le))

# IDP failure rate (15m)
increase(idp_errors_total[15m]) / increase(idp_requests_total[15m])
```

Dashboard JSON / monitoring-as-code: to be created by Platform/SRE and links attached here before sign-off.

## Alert Rules

| Alert | Expression (example) | Severity | Notification |
|---|---|---|---|
| High onboarding failure rate | `increase(onboarding_failure_total[15m]) / increase(onboarding_start_total[15m]) > 0.05` | P1 — Pager | SRE on-call, Integration |
| IDP webhook failures | `increase(idp_webhook_errors_total[15m]) > 10` | P1 — Pager | Integration on-call, Security |
| IDP verification latency | `histogram_quantile(0.95, ...) > 30000` | P2 | Integration, SRE |
| Payment validation errors | `increase(payment_validation_errors_total[15m]) > 10` | P1 if >1% rate | Integration, SRE |
| API 5xx error rate | `increase(api_5xx_total[5m]) / increase(api_requests_total[5m]) > 0.01` | P1 — Pager | SRE, Engineering |
| Conversion drop | > 30% below 7-day rolling baseline | P2 — Notify | Product |

Tune thresholds against pilot traffic before enabling pager rules in production. Include maintenance-window suppression rules for known deployments.

## Runbook: Onboarding High Failure Rate

**Purpose:** diagnose and mitigate a sustained increase in onboarding failures.
**Owner:** Platform / SRE (primary); Integration, Engineering (secondary)
**Severity triggers:** P1 if failure rate > 5% over 15 min; P2 if 2–5% over 30 min

Triage:
1. Confirm scope — vendor-side (IDP / Payment / SendGrid) or internal (DB, queue, code change). Use Integration Health and Support View dashboards.
2. Check recent deploys and feature flags coincident with alert onset.
3. Correlate traces using correlation id from a failed flow; find failing span (`idp.request`, `payment.validation`, `email.send`).
4. Review structured logs (PII redacted) for error codes and stack traces.

Mitigation — vendor failure (IDP or Payment):
1. Confirm vendor status (sandbox / prod status page).
2. Engage Integration owner and vendor on-call; apply retry/backoff throttle or enable fallback UX.
3. If sustained outage, feature-flag the dependency or display informative UX to the user.

Mitigation — internal failure (DB / queue / back-end):
1. Check DB connections, error logs, queue backlog.
2. Scale worker pool or apply mitigation (drain, increase instances).
3. If a deploy caused regression, roll back to last known good and notify Delivery lead and Product.

Post-incident: run impact analysis (failed flows, affected users, conversion delta). Create incident report in `input/` with root cause, timeline, mitigation, and corrective actions. Update runbook with lessons learned.

## Runbook: IDP Webhook Failure

**Purpose:** respond to webhook delivery failures, signature verification failures, or replay attacks from Identity Provider B.
**Owner:** Integration (primary); Platform / SRE, Security (secondary)
**Severity triggers:** P1 if > 50% of expected callbacks failing over 15 min; P2 for widespread signature verification failures.

Triage:
1. Confirm webhook endpoint is reachable from vendor network (vendor sandbox test logs).
2. Validate webhook signature: collect raw payload and signature header for a failing example. Security redacts PII before sharing externally.
3. Check application logs for signature mismatch, timestamp skew, or missing headers.
4. Confirm NTP / clock drift on webhook-handling instances if signature includes timestamp.

Mitigation — delivery / connectivity:
1. Check ingress / WAF / API Gateway for recent rules blocking vendor IPs.
2. Verify TLS cert expiration and renew if necessary.
3. If transient, re-enqueue failed webhooks (ensure idempotency).

Mitigation — signature verification failures:
1. Verify shared secret or public key in staging/prod matches vendor-provided key.
2. Validate HMAC-SHA256 implementation and payload canonicalization.
3. If timestamp window causes rejection, coordinate with vendor to confirm tolerance.

Mitigation — replay / attack detection:
1. Block offending IPs at perimeter; notify Security.
2. Increase logging, enable stricter replay protection, rotate signing secrets if compromise suspected.

Post-incident: attach redacted failing payloads and timeline to incident report. Coordinate key rotation and vendor re-registration. Update `input/contracts/identity-provider-b-contract.md` with discovered behaviours and mitigations.

## Logging and Retention

- Structured request/response logs with PII redaction enforced at emission point
- Tracing data: retain 30 days
- Metrics: retain 90 days raw, 365 days aggregated
- Adjust per Legal/compliance requirements for Italy residency

## Acceptance Checklist

- [ ] Telemetry events emitted and verifiable in staging for all key lifecycle transitions
- [ ] Dashboards created (links below) with correct queries and correlation ids
- [ ] All P1 alerts configured, tested (pager drill), and mapped to on-call contacts
- [ ] Runbooks reviewed by SRE and Engineering and linked from alert rules
- [ ] Retention and PII redaction rules confirmed by Security
- [ ] Dashboard links and alert-rule references attached before sign-off

Dashboard links (to fill before sign-off):
- Onboarding Health Overview: ___
- Integration Health — IDP: ___
- Support View: ___

## Acceptance

Status: `Accepted`
