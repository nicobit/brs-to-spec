# Prompt — Check Engineering Readiness

## Purpose

Decide whether the active deliverable is ready to be implemented (as an OpenSpec
change in Execution Mode A, or as a standalone delivery package in Execution Mode
B), and decide **which Conditional Quality Gates are triggered**.

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

## Conditional Quality Gates

These gates are not always required. But when **Triggered**, they become
**Required** and are mandatory before implementation, merge, or release
(depending on the gate).

| Quality Gate | Triggered? | Required? | Reason | Owner | Output |
|---|---|---|---|---|---|
| BDD scenarios | Yes/No | Yes/No |  |  | quality-gates/bdd-scenarios.md |
| Test strategy | Yes/No | Yes/No |  |  | quality-gates/test-strategy.md |
| QA review | Yes/No | Yes/No |  |  | quality-gates/qa-review.md |
| Architecture review | Yes/No | Yes/No |  |  | quality-gates/architecture-review.md |
| Security review | Yes/No | Yes/No |  |  | quality-gates/security-review.md |
| Release readiness | Yes/No | Yes/No |  |  | quality-gates/release-readiness-review.md |
| API contract | Yes/No | Yes/No |  |  | quality-gates/api-contract.md |
| Data contract | Yes/No | Yes/No |  |  | quality-gates/data-contract.md |
| Event contract | Yes/No | Yes/No |  |  | quality-gates/event-contract.md |
| Threat model | Yes/No | Yes/No |  |  | quality-gates/threat-model.md |
| Observability plan | Yes/No | Yes/No |  |  | quality-gates/observability-plan.md |

## Recommendation
```

## Rules

- The readiness check **decides which Conditional Quality Gates are triggered**.
- A gate that is not triggered is skipped. A gate that is triggered is mandatory.
- Do not create quality-gate artifacts that are not triggered.
- If architecture conflicts are unresolved, mark Not ready or Ready with risks.
- If ready, recommend creating the OpenSpec change (Mode A) or the standalone
  delivery package (Mode B), plus any triggered quality gates.
