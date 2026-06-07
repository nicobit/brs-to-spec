# GitLab Planning View

> This file is a planning projection.
> It is not the source of truth.
> If scope, requirements, architecture constraints, quality gates or implementation tasks change,
> update the source artifacts first and regenerate this view.

## Metadata

| Field | Value |
|---|---|
| Initiative / Feature | Client Onboarding Workflow |
| Active deliverable | D1 — Create onboarding request |
| Delivery mode | Enterprise + Modular |
| Execution mode | Standalone |
| Source of truth | `standalone-delivery/D1-create-onboarding-request/` |
| Generated from | BRS, initial architecture, readiness check, quality gates |
| View status | Draft |

## Suggested GitLab Hierarchy

| GitLab level | Suggested title | Source artifact | Source ID | Notes |
|---|---|---|---|---|
| Epic | Client Onboarding Workflow | `business-intake/business-intake-summary.md` | OBJ-001 | Parent planning item |
| Feature / Issue | Create onboarding request | `planning/delivery-increments.md` | D1 | First vertical slice |
| User story / Issue | Create onboarding request as authorized user | `input/brs.md` | REQ-001 | Story projection only |
| Task / Checklist item | Implement create request API | `standalone-delivery/D1-create-onboarding-request/tasks.md` | TASK-001 | Engineering task source remains standalone package |

## User Story Projection

| Story ID | Suggested GitLab title | User story | Source requirement | Acceptance source | Quality gate references | Labels |
|---|---|---|---|---|---|---|
| STORY-001 | Create onboarding request | As an authorized user, I want to create an onboarding request so that onboarding can start. | REQ-001 | BDD scenarios / delivery spec | BDD, Security, QA | backend, onboarding |
| STORY-002 | Validate mandatory fields | As an authorized user, I want mandatory fields validated so that incomplete requests are rejected. | REQ-002 | BDD scenarios / test strategy | BDD, QA | validation, onboarding |
| STORY-003 | Emit audit event | As an auditor, I want status changes audited so that onboarding actions are traceable. | REQ-003 | event contract / security review | Event, Security | audit, integration |

## Quality Gate Actions to Track

| Gate | Action | Source artifact | Required before | Suggested GitLab representation | Owner |
|---|---|---|---|---|---|
| Security review | Confirm role matrix | `quality-gates/security-review.md` | Implementation | Checklist item on D1 issue | Security/Architect |
| Security review | Define sensitive-field logging deny-list | `quality-gates/security-review.md` | Merge | Checklist item on D1 issue | Engineering |
| Observability plan | Define structured log events | `quality-gates/observability-plan.md` | Release | Checklist item or child issue | SRE/Engineering |

## Sync Notes

| Item | Source of truth | What to do if this changes |
|---|---|---|
| Requirement scope | `input/brs.md` and `traceability-matrix.md` | Update source and regenerate view |
| Implementation tasks | `standalone-delivery/D1-create-onboarding-request/tasks.md` | Update source and regenerate view |
| Quality gate actions | `quality-gates/*.md` | Update gate and regenerate view |
