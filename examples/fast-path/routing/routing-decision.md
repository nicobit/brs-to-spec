# Routing Decision

## Decision Summary

| Decision | Selected value | Reason | Confidence |
|---|---|---|---|
| Delivery mode | Fast Path | Score 2 — narrow scope, clear root cause, no architecture or compliance risk | High |
| Execution mode | Standalone | OpenSpec not in use for this project | High |
| Small-change path applicable? | Yes | Single story, existing system, root cause confirmed | High |

## Delivery Mode Assessment

| Criterion | Score | Evidence | Impact |
|---|---|---|---|
| Requirement ambiguity | 0 | Root cause confirmed by backend team, fix approach agreed | None |
| Architecture impact | 1 | Touches existing `auth-service` and `job-queue` — no new boundary | Low |
| Compliance / audit relevance | 0 | Password reset is not a regulated flow in this system | None |
| Business criticality | 1 | Customer-facing but not revenue-blocking or SLA-bound | Low |
| Number of teams | 0 | Single backend team | None |
| Delivery size | 0 | One story | None |
| Brownfield regression risk | 0 | Existing tests cover reset flow; queue pattern already proven | None |
| **Total** | **2** | | → Fast Path |

## Execution Mode Assessment

| Criterion | OpenSpec | Standalone | Business Copilot |
|---|---|---|---|
| Available in project? | No | Yes | No |
| Recommended? | No | Yes | No |
| Reason | Not used | Default for this project | No M365 review needed |

## Required Next Prompts

| Step | Prompt | Required? | Reason |
|---|---|---|---|
| Readiness check | `.brs2spec/skills/4-engineering-readiness/01-check-engineering-readiness.md` | Yes | Confirm no gates triggered despite narrow scope |
| Generate context | `.brs2spec/skills/4-engineering-readiness/02-generate-initiative-context.md` | Yes | Needed before implementation |
| Handoff | `.brs2spec/skills/5-handoff/02-create-standalone-delivery-package.md` | Yes | Produces delivery spec and tasks |
| Implement | `.brs2spec/skills/8-copilot-implementation/01-implement-one-task.md` | Yes | One task |
| Code review | `.brs2spec/skills/9-reviewers/01-senior-code-review.md` | Yes | Standard post-implementation check |

## Prompts Not Needed

| Prompt | Reason not needed |
|---|---|
| `skills/0-input-preparation/01-convert-brs-word-to-markdown.md` | No BRS document |
| `skills/2-business-intake/01-create-business-intake-summary.md` | No PO review required |
| `skills/3-planning-and-modular-delivery/*` | No delivery slicing |
| `skills/4-engineering-readiness/quality-gates/*` | No gates expected to trigger |
| `skills/6-business-copilot/*` | No M365 path |
| `skills/7-perspectives/*` | No sprint projection |

## Risks of Under-Processing

- If the queue integration introduces a contract with `job-queue` that isn't documented, a later change could break the reset flow silently. Readiness check will confirm whether an event or API contract is needed.

## Risks of Over-Processing

- Adding delivery structure, traceability matrix, or architecture review artifacts for a single-story bug fix wastes time and creates noise in the initiative workspace with no governance benefit.

## Small-Change Path Notes

| Item | Decision / note |
|---|---|
| Is Fast Path acceptable? | Yes — scope narrow, root cause confirmed, no unresolved ambiguity |
| Minimum required artifacts | input-package, routing-decision, readiness-check, initiative-context, delivery-spec, tasks |
| Readiness still required? | Yes — to confirm no contract gate is triggered by the queue integration |
| Gates that still may trigger | API contract (if job-queue interaction is new) — readiness will confirm |
