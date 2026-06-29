
# Epic Clarification Request - E-001

## Summary

The epic contains UI pages that have unresolved UI and integration questions that must be clarified before safe story generation.

## Blocking Questions

| ID | Route | Page | Question | Why It Matters | Required For |
|---|---|---|---|---|---|
| UIQ-002 | /applications | Application Form | Does Applicant Portal require user accounts or only ARN-based status lookup? | Affects auth model for submission and status lookup; changes API and UX requirements. | Story generation for Application Form and auth integration |
| UIQ-003 | /underwriter/application/:arn | Underwriter Application Detail | Provide `/scores/{id}` explanation payload schema for underwriter page. | Underwriter UI and explainability integration require a stable payload schema for data binding. | Story generation for underwriter panels and explainability API |
| G-UI-001 | n/a | Applicant Portal (repo mapping) | Repository mapping and build pipeline for frontend apps not provided. | Without repo/pipeline mapping, contract mode and CI/CD integration cannot be finalized. | Finalizing frontend contract mode and story scoping |
| Q-001 | /applications/status | Status Lookup | Confirm route and data source for Status Lookup (ARN-only or requires auth). | Affects story scope and backend API requirements for status retrieval. | Story generation for Status Lookup |

## Answer Instructions

Record answers in:

```text
input/clarifications/E-001.yaml
```

Include `id`, `answer`, `rationale`, `answered_at`, and `owner` for each answered question.

