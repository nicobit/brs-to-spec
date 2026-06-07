# Prompt — Check Engineering Readiness

## Role

You are a senior delivery, architecture and QA reviewer deciding whether a deliverable is ready for engineering handoff.

## Context

This is the main governance decision point. It decides readiness and triggers mandatory Conditional Quality Gates.

## Purpose

Assess the active deliverable and determine required quality gates using evidence, risk and required-before stages.

## Inputs

Use these inputs when available:

- `input/brs.md`
- `input/initial-architecture.md`
- `business-intake/business-intake-summary.md`
- `architecture/initial-architecture-review.md`
- `architecture/global-architecture-rules.md`
- `planning/delivery-structure.md`
- `planning/delivery-increments.md`
- `planning/traceability-matrix.md`
- `routing/delivery-and-execution-mode-decision.md`

## Output path

```text
engineering-readiness/readiness-check.md
```

## Required output structure

```markdown
# Engineering Readiness Check

## Metadata

| Field | Value |
|---|---|
| Initiative / Feature |  |
| Active deliverable |  |
| Delivery mode |  |
| Execution mode |  |
| Reviewer |  |
| Review date |  |

## Readiness Decision

| Decision | Value |
|---|---|
| Status | Ready / Ready with risks / Not ready |
| Decision owner |  |
| Conditions / caveats |  |

## Decision Rationale

## Core Checklist

| Area | Status | Evidence | Gap / Risk | Required action | Owner | Required before |
|---|---|---|---|---|---|---|
| Business scope clear |  |  |  |  |  | Handoff |
| Requirements traceable |  |  |  |  |  | Handoff |
| Initial architecture reviewed |  |  |  |  |  | Handoff |
| Architecture constraints applied |  |  |  |  |  | Implementation |
| Architecture conflicts resolved or accepted |  |  |  |  |  | Implementation |
| Impacted modules known |  |  |  |  |  | Implementation |
| Acceptance expectations clear |  |  |  |  |  | Implementation |
| Validation approach clear |  |  |  |  |  | Implementation |

## Conditional Quality Gates

| Quality Gate | Triggered? | Required? | Trigger evidence | Risk if skipped | Owner | Required before | Output |
|---|---|---|---|---|---|---|---|
| BDD scenarios |  |  |  |  | PO/QA | Implementation | `quality-gates/bdd-scenarios.md` |
| Test strategy |  |  |  |  | QA | Implementation | `quality-gates/test-strategy.md` |
| QA review |  |  |  |  | QA | Merge | `quality-gates/qa-review.md` |
| Architecture review |  |  |  |  | Architect | Implementation | `quality-gates/architecture-review.md` |
| Security review |  |  |  |  | Security/Architect | Implementation/Merge | `quality-gates/security-review.md` |
| Release readiness review |  |  |  |  | Dev/QA/SRE | Release | `quality-gates/release-readiness-review.md` |
| API contract |  |  |  |  | Engineering | Implementation | `quality-gates/api-contract.md` |
| Data contract |  |  |  |  | Engineering/DB | Implementation | `quality-gates/data-contract.md` |
| Event contract |  |  |  |  | Engineering | Implementation | `quality-gates/event-contract.md` |
| Threat model |  |  |  |  | Security/Architect | Implementation | `quality-gates/threat-model.md` |
| Observability plan |  |  |  |  | SRE/Engineering | Release | `quality-gates/observability-plan.md` |

## Blocking Issues

## Accepted Risks

## Required Actions Before Handoff

## Recommended Handoff
```

## Quality bar

A good output must:

- apply trigger rules strictly
- mark triggered gates as required
- include evidence for each decision
- assign owner and required-before stage for each action
- return Not ready if critical inputs are missing

## Anti-patterns to avoid

Do not produce outputs that:

- call quality gates optional
- mark Ready without evidence
- ignore architecture constraints
- skip gates because they are inconvenient
- use generic text such as 'security should be considered'

## Stop conditions

- If required inputs are missing, do not invent content.
- List missing inputs and explain the impact.
- Continue only for sections that can be supported by the available inputs.

## Self-review checklist

Before finalizing, verify:

- [ ] Every triggered gate has trigger evidence.
- [ ] Every risk has an owner or accepted-risk decision.
- [ ] Readiness decision is justified.
- [ ] Required-before stages are clear.
- [ ] Unsupported assumptions are flagged.
