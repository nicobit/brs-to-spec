# Proposal — F-005.1: Metrics and Tracing

**As an** SRE,
**I want** telemetry for onboarding_start/onboarding_success/onboarding_failure and tracing across integrations,
**so that** we can measure KPIs and alert on regressions.

**Requirement:** NFR-005
**Acceptance criteria:** `quality-gates/observability-plan.md` — SLOs and telemetry catalog

## Why now

F-001.2 established the onboarding flow entry point. Instrumentation must be added before the IDP integration (F-002.1) goes live so that the full flow is observable from day one. Agreed signal names are a shared dependency with F-002.1.

## What changes

- Telemetry middleware added to Onboarding API — W3C trace context, span creation
- `onboarding_start`, `onboarding_success`, `onboarding_failure` counters wired to existing handlers (F-001.1, F-002.1 webhook)
- `verification_latency_ms` histogram wired to webhook handler
- `idp_requests_total`, `idp_errors_total`, `idp_webhook_received` counters
- Staging dashboard configured with correct queries

## Dependencies

| Relationship | Story ID | Reason |
|---|---|---|
| Depends on | F-001.2 | Needs `onboarding_start` emission point from F-001.1 to exist |
| Can run in parallel with | F-002.1 | Coordinate on span names and signal names before starting |
| Blocks | F-005.2 | Runbooks and alerts require these signals to exist |

## Acceptance criteria

| AC | Criterion | How to verify | Evidence expected |
|---|---|---|---|
| AC-001 | All signals from observability-plan.md emit in staging | Run test flows; query each metric | Counter/histogram values visible per signal |
| AC-002 | End-to-end trace visible with correlation ID across all spans | Run one flow; inspect trace | Single trace with `onboarding.request` → `idp.request` → `idp.webhook` spans |
| AC-003 | No PII in span attributes | Inspect trace attributes | Email/phone absent from all spans |
| AC-004 | Staging dashboard shows SLO queries returning data | Open dashboard | All panels populated |

## Constraints inherited from upstream

| Constraint | Source artifact |
|---|---|
| W3C trace context — `traceparent` header propagated end-to-end | `architecture/architecture-rules.md` AR-OBS-001 |
| PII redacted from traces at emission point | `quality-gates/security-review.md` |
| Sampling: 100% errors, 10% success | `quality-gates/observability-plan.md` |

## Reference artifacts

| Artifact | Path | What to read there |
|---|---|---|
| Observability plan | `quality-gates/observability-plan.md` | Full telemetry catalog, SLOs, dashboard queries, alert rules |
| Security review | `quality-gates/security-review.md` | PII redaction requirements for traces |
