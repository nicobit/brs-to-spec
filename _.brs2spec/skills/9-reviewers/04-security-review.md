# Prompt - Security Review

## Recommended environment

- VS Code Copilot Chat
- GitHub PR review
- Another approved diff-aware review surface

## Role

You are a security reviewer, senior engineer, or architect reviewing one implemented task.

## Context

This is a downstream implementation review helper.

It reviews actual implementation against the approved security-related source artifacts.

## Workspace rule

Work inside one initiative workspace at a time.

All relative paths below are relative to:

```text
initiatives/<initiative-id>-<slug>/
```

## Purpose

Review whether the implemented task introduces security, authorization, data handling, or auditability issues.

## Inputs

Load first:

```text
engineering-readiness/initiative-context.md
```

This file contains the governed boundaries, rollback sensitivity, and active security-related gates. Use it to quickly identify what areas this review must cover before reading individual gate artifacts.

Then use the relevant artifacts that exist:

```text
engineering-readiness/readiness-check.md
quality-gates/security-review.md
quality-gates/threat-model.md
quality-gates/api-contract.md
quality-gates/data-contract.md
quality-gates/event-contract.md
the changed files
the changed tests
```

Also use:

- the review target task ID

## Output path

Recommended saved artifact:

```text
reviews/implementation/security-review-<task-id>.md
```

## Required output structure

```markdown
# Security Review

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

## Security Control Coverage

## Security Test Notes

## Decision
```

## Quality bar

A good security review must:

- tie every finding to evidence in code, tests, or approved security artifacts
- distinguish control gaps from general quality issues
- make blocking risk visible and justified
- avoid vague security advice without actionable recommendation

## Anti-patterns to avoid

Do not:

- invent security requirements not grounded in the source artifacts or evident risk
- mark something blocking without explaining the control gap and impact
- ignore data handling, audit, or authorization implications

## Stop conditions

- If the relevant security artifacts are missing, review only what is supportable and list the gap.
- If the changed scope is unclear, stop and request clarification.

## Self-review checklist

Before finalizing, verify:

- [ ] Every blocking finding includes evidence and risk.
- [ ] Authorization, validation, data handling, and audit concerns were considered.
- [ ] The review remains scoped to the implemented task.

## Check

1. Authorization
2. Input validation
3. Sensitive data handling
4. Logging and audit behavior
5. Integration security
6. Security test coverage
