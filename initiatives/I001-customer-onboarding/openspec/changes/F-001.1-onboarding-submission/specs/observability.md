# Observability Spec — F-001.1: Onboarding Submission

**All signals listed here are mandatory.**

## Signals to emit

| Signal | Type | Emitted by | When | Labels |
|---|---|---|---|---|
| `onboarding_start` | Counter | Onboarding API | On 202 response from `POST /onboarding` | none |

## Tracing

- Span name: `onboarding.request` — covers entire `POST /onboarding` handler
- Correlation ID: W3C `traceparent` header — inject at this entry point; propagate to all downstream spans
- PII in traces: `email` and `phone` must not appear in span attributes
