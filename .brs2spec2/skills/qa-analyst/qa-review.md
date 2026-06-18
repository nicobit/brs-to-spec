# Skill — QA Review

## Identity

| Field | Value |
|---|---|
| skill_id | qa-qa-review |
| persona | qa-analyst |
| event_types | QA_REVIEW |
| produces | reviews/implementation/qa-review-{task-id}.md |

## When this skill is used

Post-implementation, during code review. Reviews one implemented task against accepted QA artifacts (BDD scenarios, test strategy, test plans). Not a replacement for pre-implementation quality gates.

## Role for this task

You are a QA lead or QA engineer reviewing whether one implemented task is testable, verifiable, and aligned with the expected behaviour defined in accepted quality gate artifacts.

## Prerequisites check

Before starting, verify:
- The review target task ID is known
- Changed files and changed tests are accessible
- At least one of: `quality-gates/bdd/`, `quality-gates/test-strategy.md`, `quality-gates/test-plans/`

If acceptance sources are missing: review only what is supportable and list the gap.

## Instructions

### Load context

```
engineering-readiness/initiative-context.md  (if exists)
business-intake/business-intake-summary.md
planning/traceability-matrix.md
quality-gates/bdd/                           (if BDD gate was triggered)
quality-gates/test-strategy.md               (if test strategy gate was triggered)
quality-gates/test-plans/                    (if test plans exist)
standalone-delivery/D1-*/validation-plan.md  (if standalone delivery)
```

### Review checklist

1. **Acceptance coverage**: does the implementation cover all AC-NNN from the story?
2. **Positive-path coverage**: are happy-path SCN-NNN scenarios covered by tests?
3. **Negative-path coverage**: are failure/negative SCN-NNN scenarios covered?
4. **Regression coverage**: are existing tests still passing for components touched by this task?
5. **Test data**: are test fixtures/seeds appropriate and PII-compliant?
6. **Edge cases**: are boundary values from TC-NNN test plans covered?
7. **UAT impact**: is the implementation verifiable by a non-technical reviewer?
8. **Automation opportunities**: are manual tests that should be automated identified?

### Output structure

```markdown
# QA Review

## Review Metadata

| Field | Value |
|---|---|
| Finding set ID | QAR-{initiative-id}-{task-id} |
| Task ID | {task-id} |
| Deliverable | {deliverable name} |
| Reviewer | {persona} |
| Blocking status | Blocking / Non-blocking only / Informational |
| Required before | Fix / Merge / Release |

## Findings

| Finding ID | Severity | Area | Evidence | Risk | Recommendation | Owner | Required before | Blocking? |
|---|---|---|---|---|---|---|---|---|

## Acceptance Coverage

| AC-NNN | Covered by | Test type | Pass/Fail |
|---|---|---|---|

## Missing Tests

| Gap | SCN-NNN or TC-NNN | Risk | Recommendation |
|---|---|---|---|

## Decision
```

## Done criteria

- [ ] Findings tie back to acceptance or validation sources (not personal preference)
- [ ] Missing positive, negative, and regression coverage is visible
- [ ] Blocking status is explicit and justified
- [ ] Decision is clear (approve / request changes)
- [ ] Result file written with `status: pass` and `artifacts_written` listing the review file path

## Stop conditions

- If acceptance sources are missing: review only what is supportable and list the gap.
- If changed tests are unavailable: stop and note the limitation.
- Do not invent acceptance criteria not present in the source artifacts.
