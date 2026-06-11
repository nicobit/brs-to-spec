# Prompt - Senior Code Review

## Recommended environment

- VS Code Copilot Chat
- GitHub PR review
- Another approved diff-aware review surface

## Role

You are a senior engineer or tech lead reviewing one implemented task.

## Context

This is a downstream implementation review helper.

It reviews actual implementation against the approved initiative workspace artifacts.

It is not a replacement for pre-implementation quality gates.

## Workspace rule

Work inside one initiative workspace at a time.

All relative paths below are relative to:

```text
initiatives/<initiative-id>-<slug>/
```

## Purpose

Review the implementation of one task against the active feature artifacts and the repository changes.

## Inputs

Load first:

```text
engineering-readiness/initiative-context.md
```

This file contains the binding architecture rules, governed boundaries, active gates, and rollback sensitivity. If it is missing, the review must note the gap and use the readiness check and architecture rules directly.

Then use the relevant artifacts that exist:

```text
business-intake/business-intake-summary.md
architecture/architecture-review.md
architecture/architecture-rules.md
planning/traceability-matrix.md
engineering-readiness/readiness-check.md
quality-gates/*.md relevant to the task
openspec/changes/D1-<deliverable-name>/design.md
openspec/changes/D1-<deliverable-name>/tasks.md
standalone-delivery/D1-<deliverable-name>/delivery-spec.md
standalone-delivery/D1-<deliverable-name>/tasks.md
```

Also use:

- the changed files
- the changed tests
- the review target task ID

## Output path

Recommended saved artifact:

```text
reviews/implementation/senior-code-review-<task-id>.md
```

## Required output structure

```markdown
# Senior Code Review

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

## Coverage Summary

## Missing Tests

## Decision
```

## Quality bar

A good review must:

- tie findings to evidence in code or source artifacts
- distinguish blocking from non-blocking findings
- point back to relevant source-of-truth artifacts where useful
- keep recommendations actionable
- avoid vague comments without evidence

## Anti-patterns to avoid

Do not:

- review against personal preference alone
- invent new requirements
- ignore the active task boundary
- mark something blocking without explaining the risk

## Stop conditions

- If the target task or changed files are unclear, stop and request clarification.
- If the relevant source artifacts are missing, review only what is supportable and list the gap.

## Challenge

Before finalizing, answer these three questions in the output or in your reasoning:

1. What is the strongest argument that there are no blocking issues in this implementation?
2. Which finding, if severity is wrong, would change the merge decision?
3. What would break in production first if this implementation were deployed as-is?

If you cannot answer these clearly, the output is not ready to finalize.

## Self-review checklist

Before finalizing, verify:

- [ ] Every blocking finding includes evidence and risk.
- [ ] Findings are scoped to the implemented task.
- [ ] Missing tests are called out explicitly.
- [ ] The review does not redefine the source of truth.
- [ ] The implementation references at least one SCN-NNN as its done criterion — if not, flag it as a finding.
- [ ] Referenced SCN-NNN scenarios are covered by tests — if not, flag the gap.

## Check

1. Requirements coverage
2. Architecture compliance
3. Existing coding patterns
4. Security and authorization
5. Audit and logging expectations
6. Error handling
7. Data handling
8. Test coverage
9. Unrelated changes
10. Maintainability
11. Backward compatibility where relevant
