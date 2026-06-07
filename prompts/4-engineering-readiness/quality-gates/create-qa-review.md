# Quality Gate Prompt — Create QA Review

## Purpose

Review the active deliverable from a QA perspective before or after OpenSpec handoff.

Use this only when a formal QA review is needed.

## Inputs

Use:
- business intake summary,
- delivery increments,
- traceability matrix,
- OpenSpec proposal/design/tasks,
- BDD scenarios if available,
- test strategy if available.

## Output file

```text
quality-gates/qa-review.md
```

## Output structure

```markdown
# QA Review

## Active Deliverable

## Review Decision
Approved / Approved with risks / Not approved

## Findings

| Finding ID | Severity | Area | Description | Recommendation |
|---|---|---|---|---|

## Coverage Review

| Requirement ID | Covered by test? | Notes |
|---|---|---|

## Automation Review

## Regression Risk

## Missing Test Scenarios

## Required Actions Before Implementation / Merge
```

## Rules

- Be critical.
- Identify missing acceptance criteria or test coverage.
- Do not rewrite the solution design.
- Keep findings actionable.
