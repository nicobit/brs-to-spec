# Prompt — Check Engineering Readiness

## Purpose

Decide whether the active deliverable is ready to become an OpenSpec change.

## Inputs

Use:
- `input/brs.md`
- `input/initial-architecture.md`
- `business-intake/business-intake-summary.md`
- `architecture/initial-architecture-review.md`
- `architecture/global-architecture-rules.md`
- `planning/delivery-increments.md`
- `planning/traceability-matrix.md`

## Output file

```text
engineering-readiness/readiness-check.md
```

## Output structure

```markdown
# Engineering Readiness Check

## Active Deliverable

## Readiness Decision
Ready / Ready with risks / Not ready

## Checklist

| Area | Ready? | Notes |
|---|---|---|
| Business scope clear |  |  |
| Requirements traceable |  |  |
| Initial architecture reviewed |  |  |
| Architecture constraints applied |  |  |
| Conflicts with architecture resolved |  |  |
| Open architecture decisions assigned |  |  |
| Modules impacted known |  |  |
| Acceptance criteria clear |  |  |
| Dependencies known |  |  |
| Risks identified |  |  |
| Automated validation expectations clear |  |  |

## Required Advanced Contracts

| Contract / artifact | Needed? | Reason |
|---|---|---|
| API contract |  |  |
| Data contract |  |  |
| Event contract |  |  |
| Threat model |  |  |
| Observability plan |  |  |
| CI/CD readiness |  |  |
| Module technical spec |  |  |

## Recommendation
```

## Rules

- Do not create advanced contracts unless needed.
- If architecture conflicts are unresolved, mark Not ready or Ready with risks.
- If ready, recommend creating an OpenSpec change.
