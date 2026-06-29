# Epic Clarification Request - E-003

## Summary

This epic has an unresolved integration question regarding HMRC contract and SLA that affects integration reliability and implementation planning.

## Blocking Questions

| ID | Route | Page | Question | Why It Matters | Required For |
|---|---|---|---|---|---|
| SDQ-003 | External Integration (HMRC) | Compliance Worker / Integrations | Confirm HMRC contract terms and SLA, including expected throughput, error model, and retry guidance. | Integration reliability, circuit-breaker thresholds, and fallback behaviors depend on contract and SLA. | Story generation for HMRC adapter and compliance workflows |

## Answer Instructions

Record answers in:

```text
input/clarifications/E-003.yaml
```

Include `id`, `answer`, `rationale`, `answered_at`, and `owner` for each answered question.
