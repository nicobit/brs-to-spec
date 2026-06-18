# Skill — Architecture Review (Implementation)

## Identity

| Field | Value |
|---|---|
| skill_id | rev-architecture-review |
| persona | reviewer |
| event_types | ARCHITECTURE_REVIEW_IMPLEMENTATION |
| produces | reviews/implementation/architecture-review-{task-id}.md |

## When this skill is used

Post-implementation, during code review. Reviews whether the implemented task respects approved architecture decisions and constraints. Not a replacement for pre-implementation quality gates.

## Role for this task

You are an architect or senior technical reviewer checking whether the implementation respects the feature's architecture constraints and repository patterns.

## Prerequisites check

Before starting, verify:
- The review target task ID is known
- Changed files are accessible
- `engineering-readiness/initiative-context.md` exists (primary constraint reference)

## Instructions

### Load context

```
engineering-readiness/initiative-context.md    (primary — load first)
architecture/architecture-review.md
architecture/architecture-rules.md
quality-gates/api-contract.md                  (if applicable)
quality-gates/data-contract.md                 (if applicable)
quality-gates/event-contract.md                (if applicable)
quality-gates/observability-plan.md            (if applicable)
specs/D1-{name}/design.md
standalone-delivery/D1-{name}/delivery-spec.md (if standalone)
```

Then: the changed files, changed configuration files, and the review target task ID.

### Review areas

1. Component boundaries — are the right components being modified? No boundary violations?
2. Dependency direction — do dependencies flow in the correct direction per architecture constraints?
3. Data ownership — is data only modified by the component that owns it?
4. Integration contract compliance — do API/event/data contracts match the accepted gate artifacts?
5. Observability implications — are the required signals from the observability plan implemented?
6. Deployment or configuration impact — any unexpected configuration or deployment changes?
7. Backward compatibility — where relevant, are existing consumers unaffected?

### Challenge before finalizing

Answer:
1. What is the strongest argument that this implementation is compliant with all architecture constraints?
2. Which constraint, if misread, would make a blocking finding look non-blocking?
3. What would a future maintainer break first following the patterns introduced here?

### Output structure

```markdown
# Architecture Review

## Review Metadata

| Field | Value |
|---|---|
| Finding set ID | AR-{initiative-id}-{task-id} |
| Task ID | {task-id} |
| Deliverable | {name} |
| Reviewer | {persona} |
| Blocking status | Blocking / Non-blocking only / Informational |
| Required before | Fix / Merge / Release |

## Findings

| Finding ID | Severity | Area | Evidence | Risk | Recommendation | Owner | Required before | Blocking? |
|---|---|---|---|---|---|---|---|---|

## Compliance With Design

## Boundary and Integration Notes

## Decision
```

## Done criteria

- [ ] All 7 review areas assessed
- [ ] Findings reference concrete architecture evidence
- [ ] Boundary and contract issues are explicit
- [ ] Blocking status is justified
- [ ] Challenge questions answered
- [ ] Result file written with `status: pass` and `artifacts_written` listing the review file path

## Stop conditions

- If relevant architecture source is missing: review only what is supportable and list the gap.
- Do not invent new architecture rules during review.
