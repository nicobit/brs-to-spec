# Epic Clarification Request - E-004

## Summary

This epic requires clarification on actor identity and audit binding for underwriter actions to ensure the audit trail and UI bindings meet compliance requirements.

## Blocking Questions

| ID | Route | Page | Question | Why It Matters | Required For |
|---|---|---|---|---|---|
| UQ-001 | /api/v1/underwriter/actions | Underwriter API / Panels | Confirm underwriter `actor_id` format and identity provider (e.g., enterprise SSO username, employee id). | Affects authentication, authorization, and audit linking of actions to users. | Story generation for underwriter API and UI authentication |
| UQ-002 | /api/v1/underwriter/actions | Underwriter API | Confirm required fields for decline action (is `reason` mandatory and any constraints). | Ensures validation rules and UI enforced behavior match compliance requirements. | Story generation and API validation tests |
| UQ-003 | AuditStore binding | AuditStore integration | Confirm the canonical reference to AuditStore events (event id format and retention policy) for underwriter actions. | Ensures audit entries meet write-once, tamper-evident requirements and retention policy aligns with NFRs. | Story generation and audit integration work |

## Answer Instructions

Record answers in:

```text
input/clarifications/E-004.yaml
```

Include `id`, `answer`, `rationale`, `answered_at`, and `owner` for each answered question.
