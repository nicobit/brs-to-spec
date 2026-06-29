# Epic Clarification Request - E-002

## Summary

The epic requires confirmation of the `/scores/{id}` contract used by UIs and storage. This affects UI binding and the storage schema for explainability traces.

## Blocking Questions

| ID | Route | Page | Question | Why It Matters | Required For |
|---|---|---|---|---|---|
| SDQ-002 | /api/v1/scores/{id} | Scoring API / Underwriter panels | Confirm the `/scores/{id}` response payload and explainability reference format. | UI binding and persistence schema depend on the payload shape and reference format. | Story generation for `/scores/{id}` and explainability persistence |

## Answer Instructions

Record answers in:

```text
input/clarifications/E-002.yaml
```

Include `id`, `answer`, `rationale`, `answered_at`, and `owner` for each answered question.
