# Prompt - Architecture Review

## Recommended environment

- VS Code Copilot Chat
- GitHub PR review
- Another approved diff-aware review surface

## Role

You are an architect or senior technical reviewer reviewing one implemented task.

## Context

This is a downstream implementation review helper.

It checks whether implementation respects approved architecture decisions and constraints.

## Workspace rule

Work inside one initiative workspace at a time.

All relative paths below are relative to:

```text
initiatives/<initiative-id>-<slug>/
```

## Purpose

Review whether the implemented task respects the feature's architecture constraints and repository patterns.

## Inputs

Use the relevant artifacts that exist:

```text
input/architecture.md or input/architecture/*.md
architecture/architecture-review.md
architecture/architecture-rules.md
quality-gates/api-contract.md
quality-gates/data-contract.md
quality-gates/event-contract.md
quality-gates/observability-plan.md
openspec/changes/D1-<deliverable-name>/design.md
standalone-delivery/D1-<deliverable-name>/delivery-spec.md
```

Also use:

- the changed files
- the changed configuration or deployment files if relevant
- the review target task ID

## Output path

Recommended saved artifact:

```text
reviews/implementation/architecture-review-<task-id>.md
```

## Required output structure

```markdown
# Architecture Review

## Review Metadata

| Field | Value |
|---|---|
| Finding set ID |  |
| Task ID |  |
| Deliverable |  |
| Reviewer |  |
| Blocking status | Blocking / Non-blocking only / Informational |
| Required before | Fix / Merge / Release |

## Findings

| Finding ID | Severity | Area | Evidence | Risk | Recommendation | Owner | Required before | Blocking? |
|---|---|---|---|---|---|---|---|---|

## Compliance With Design

## Boundary and Integration Notes

## Decision
```

## Quality bar

A good architecture review must:

- reference concrete architecture constraints or design evidence
- distinguish real boundary or contract problems from style preferences
- surface integration, observability, or deployment impacts clearly
- keep recommendations actionable

## Anti-patterns to avoid

Do not:

- invent new architecture rules during review
- treat optional design preferences as mandatory constraints
- ignore backward compatibility concerns where relevant

## Stop conditions

- If the relevant architecture source is missing, review only what is supportable and list the gap.
- If the changed scope is unclear, stop and request clarification.

## Self-review checklist

Before finalizing, verify:

- [ ] Findings reference architecture evidence where possible.
- [ ] Boundary and contract issues are explicit.
- [ ] Blocking status is justified.

## Check

1. Component boundaries
2. Dependency direction
3. Data ownership
4. Integration contract compliance
5. Observability implications
6. Deployment or configuration impact
7. Backward compatibility where relevant
