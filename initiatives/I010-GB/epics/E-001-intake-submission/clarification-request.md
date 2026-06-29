# Epic Clarification Request - E-001

## Summary

This epic has a small set of unresolved blocking questions related to the Intake API and Status API that must be clarified before story generation can produce complete, testable contracts and data bindings.

## Blocking Questions

| ID | Route | Page | Question | Why It Matters | Required For |
|---|---|---|---|---|---|
| UIQ-001 | /api/intake/submit | Application Form (/applications/new) | What is the definitive Intake API request/response contract (field names, required fields, and error response shape)? | The UI form data bindings and story acceptance criteria depend on the final API contract. | Story generation for S-001.1 / S-001.2 |
| UIQ-002 | /api/intake/status | Status Lookup (/applications/status) | What are the exact query parameters and response schema for the status lookup API (ARN + DOB vs ARN only)? | Status page stories and contract tests require the exact lookup parameters and response schema. | Story generation for S-001.4 |

## Answer Instructions

Record answers in:

```text
input/clarifications/E-001.yaml
```

Use the clarification input schema expected by the framework. Include rationale, owner, and artefacts to update.

## Resolution Rule

After answers are captured, rerun epic shell generation so the implementation contract can incorporate clarifications before story generation continues.
