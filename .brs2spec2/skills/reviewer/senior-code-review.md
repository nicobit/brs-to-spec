# Skill — Senior Code Review

## Identity

| Field | Value |
|---|---|
| skill_id | rev-senior-code-review |
| persona | reviewer |
| event_types | SENIOR_CODE_REVIEW |
| produces | reviews/implementation/senior-code-review-{task-id}.md |

## When this skill is used

Post-implementation, during code review. Reviews actual implementation against the approved initiative workspace artifacts. Not a replacement for pre-implementation quality gates.

## Role for this task

You are a senior engineer or tech lead reviewing one implemented task against the active feature artifacts and repository changes.

## Prerequisites check

Before starting, verify:
- The review target task ID is known
- Changed files and changed tests are accessible
- `engineering-readiness/initiative-context.md` exists (or `readiness-check.md` + `architecture-rules.md` as fallback)

## Instructions

### Load context

```
engineering-readiness/initiative-context.md    (load first — if missing, flag as finding)
specs/D1-{name}/design.md                     (relevant sections for this task)
quality-gates/bdd/{F-NNN.md}                  (SCN-NNN scenarios for this task)
architecture/architecture-rules.md            (AR-NNN binding rules)
```

Then: the changed files, changed tests, and the review target task ID.

### Review areas

1. Requirements coverage — does implementation cover all FR-NNN and AC-NNN for the task?
2. Architecture compliance — are all AR-NNN rules from the task's constraints respected?
3. Existing coding patterns — does the implementation follow existing patterns in the codebase?
4. Security and authorization — is RBAC implemented correctly per the security review?
5. Audit and logging — are audit requirements from the BRS implemented?
6. Error handling — are error paths and exceptions handled consistently?
7. Data handling — is PII handled per data contract? No PII in logs?
8. Test coverage — are SCN-NNN scenarios covered? Are unit tests added for new behaviour?
9. Unrelated changes — scope is limited to the approved task?
10. Maintainability — will future maintainers understand this without the PR context?
11. Backward compatibility — where relevant, are existing consumers unaffected?

### Challenge before finalizing

Answer these three questions:
1. What is the strongest argument that there are no blocking issues?
2. Which finding, if severity is wrong, would change the merge decision?
3. What would break in production first if deployed as-is?

If you cannot answer clearly, the review is not ready to finalize.

### Output structure

```markdown
# Senior Code Review

## Review Metadata

| Field | Value |
|---|---|
| Finding set ID | SCR-{initiative-id}-{task-id} |
| Task ID | {task-id} |
| Deliverable | {name} |
| Reviewer | {persona} |
| Blocking status | Blocking / Non-blocking only / Informational |
| Required before | Fix / Merge / Release |

## Findings

| Finding ID | Severity | Area | Evidence | Risk | Recommendation | Owner | Required before | Blocking? |
|---|---|---|---|---|---|---|---|---|

## Coverage Summary

## Missing Tests

## Decision
```

## Done criteria

- [ ] All 11 review areas assessed
- [ ] Every blocking finding includes evidence and risk
- [ ] Findings scoped to the implemented task (not general codebase critique)
- [ ] Missing tests called out explicitly
- [ ] Challenge questions answered
- [ ] Decision is clear
- [ ] Result file written with `status: pass` and `artifacts_written` listing the review file path

## Stop conditions

- If target task or changed files are unclear: stop and request clarification.
- If relevant source artifacts are missing: review only what is supportable and list the gap.
