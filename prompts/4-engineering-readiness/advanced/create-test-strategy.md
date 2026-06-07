# Advanced Prompt — Create Test Strategy

## Purpose

Create a focused test strategy for the active deliverable.

Use this only when the engineering readiness check requires explicit QA/test planning.

## Inputs

Use:
- active deliverable,
- BRS,
- traceability matrix,
- architecture constraints,
- OpenSpec proposal/design if available,
- readiness check.

## Output file

```text
advanced-governance/test-strategy.md
```

## Output structure

```markdown
# Test Strategy

## Active Deliverable

## Scope

## Test Objectives

## Test Levels

| Level | Required? | Notes |
|---|---|---|
| Unit tests |  |  |
| API tests |  |  |
| Integration tests |  |  |
| UI tests |  |  |
| Regression tests |  |  |
| Security tests |  |  |
| Performance tests |  |  |
| Audit/compliance tests |  |  |

## Requirement-to-Test Mapping

| Requirement ID | Test type | Validation approach | Automation? |
|---|---|---|---|

## Test Data

## Entry Criteria

## Exit Criteria

## Risks

## Open Questions
```

## Rules

- Keep the test strategy scoped to the active deliverable.
- Prefer automated validation where possible.
- Do not define tests for unrelated future deliverables.
- Preserve traceability to the BRS and OpenSpec tasks.
