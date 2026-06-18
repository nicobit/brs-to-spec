# Fast Path Example — Password Reset Email Delay

This example shows the **minimum viable artifact set** for a narrow, engineering-ready change.

- Entry mode: `small change / bug fix`
- Delivery mode: `Fast Path` (routing score: 2)
- Execution mode: `Standalone`

## Scenario

A customer-reported bug: password reset emails are delayed by 3–5 minutes in production because the email send is synchronous inside the HTTP request handler. The fix is to move the send to a background queue. The affected system is existing and well-understood. No new API boundaries, no schema changes, no compliance requirements.

## Why Fast Path is correct here

| Criterion | Score | Reason |
|---|---|---|
| Requirement ambiguity | 0 | Root cause is clear, fix is agreed |
| Architecture impact | 1 | Touches existing email service — no new boundary |
| Compliance / audit relevance | 0 | Password reset is not a compliance-scoped flow |
| Business criticality | 1 | Customer-facing but not revenue-blocking |
| Number of teams | 0 | Single backend team |
| Delivery size | 0 | One story |
| Brownfield regression risk | 0 | Existing tests cover the happy path |
| **Total** | **2** | → Fast Path |

## Artifacts in this example

```
examples/fast-path/
├── README.md                                      ← this file
├── input/
│   └── input-package.md                           ← concise problem statement
├── routing/
│   └── routing-decision.md                        ← Fast Path confirmed
├── engineering-readiness/
│   ├── readiness-check.md                         ← lightweight, no triggered gates
│   └── initiative-context.md                      ← compact context for implementation
└── standalone-delivery/
    └── D1-password-reset-async/
        ├── delivery-spec.md                       ← what to build
        └── tasks.md                               ← one task
```

## What is intentionally absent

| Artifact | Why absent |
|---|---|
| `business-intake/business-intake-summary.md` | No PO review needed — bug fix with clear root cause |
| `architecture/architecture-review.md` | No new architecture decisions |
| `architecture/architecture-rules.md` | Existing rules apply — no initiative-specific constraints |
| `planning/delivery-structure.md` | One story, no slicing needed |
| `planning/traceability-matrix.md` | Single requirement, traceability in delivery-spec is sufficient |
| Quality gates | None triggered — no new API/data/event boundaries, no security scope change |

## Prompts used

```text
.brs2spec/00-start.md
.brs2spec/skills/1-routing/01-select-delivery-and-execution-mode.md
.brs2spec/skills/4-engineering-readiness/01-check-engineering-readiness.md
.brs2spec/skills/4-engineering-readiness/02-generate-initiative-context.md
.brs2spec/skills/5-handoff/02-create-standalone-delivery-package.md
.brs2spec/skills/8-copilot-implementation/01-implement-one-task.md
.brs2spec/skills/9-reviewers/01-senior-code-review.md
```

## Prompts skipped and why

| Prompt | Reason skipped |
|---|---|
| `skills/0-input-preparation/01-convert-brs-word-to-markdown.md` | No Word document — problem is stated directly |
| `skills/2-business-intake/01-create-business-intake-summary.md` | No PO review needed |
| `skills/3-planning-and-modular-delivery/*` | No delivery slicing, no modular planning |
| `skills/4-engineering-readiness/quality-gates/*` | No gates triggered |
| `skills/6-business-copilot/*` | No M365 review path |
| `skills/7-perspectives/*` | No sprint board needed |
