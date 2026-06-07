# Quality Gate Prompt — Create BDD Scenarios

## Purpose

Create business-readable BDD scenarios for the active deliverable.

Use this only when the engineering readiness check requires explicit scenario-level validation.

## Inputs

Use:
- `input/brs.md`
- `business-intake/business-intake-summary.md`
- `planning/delivery-increments.md`
- `planning/traceability-matrix.md`
- `engineering-readiness/readiness-check.md`
- active OpenSpec change if already created.

## Output file

```text
quality-gates/bdd-scenarios.md
```

## Output structure

```markdown
# BDD Scenarios

## Active Deliverable

## Scenario Overview

| Scenario ID | Related requirement | Capability | Priority | Notes |
|---|---|---|---|---|

## Scenarios

### SCN-001 — <Scenario name>

**Related requirement:**  
**Related deliverable:**  
**Priority:**  

```gherkin
Given ...
When ...
Then ...
```

## Negative / Exception Scenarios

## Open Questions
```

## Rules

- Use Given/When/Then.
- Keep scenarios focused on the active deliverable.
- Do not create scenarios for future deliverables.
- Preserve traceability to requirements and acceptance criteria.
- Do not create implementation code.
