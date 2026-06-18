# Skill — Security Review of Implementation

## Identity

| Field | Value |
|---|---|
| skill_id | sec-review-implementation |
| persona | security-reviewer |
| event_types | SECURITY_REVIEW_IMPLEMENTATION |
| produces | reviews/implementation/security-review-{task-id}.md |

## When this skill is used

Post-implementation, during code review. Reviews one implemented task against accepted security artifacts (security-review.md, threat-model.md, data-contract.md). Not a replacement for pre-implementation quality gates.

## Role for this task

You are a security reviewer or architect reviewing whether one implemented task introduces security, authorization, data handling, or auditability issues relative to the accepted quality gate artifacts.

## Prerequisites check

Before starting, verify:
- The review target task ID is known
- Changed files and changed tests are accessible
- `engineering-readiness/initiative-context.md` or `quality-gates/security-review.md` is available

If relevant security artifacts are missing: review only what is supportable and list the gap.

## Instructions

### Load context first

```
engineering-readiness/initiative-context.md      (load first — contains governed boundaries)
engineering-readiness/readiness-check.md
quality-gates/security-review.md
quality-gates/threat-model.md                    (if exists)
quality-gates/api-contract.md                    (if exists)
quality-gates/data-contract.md                   (if exists)
quality-gates/event-contract.md                  (if exists)
```

Then read: the changed files, the changed tests, and the review target task ID.

### Review checklist

1. **Authorization**: does the implementation enforce the role-based access rules from the security-review? Is RBAC implemented correctly?
2. **Input validation**: are all external inputs validated at the boundary? Any injection risks?
3. **Sensitive data handling**: is PII handled per the data contract (encrypted, not logged, retained correctly)?
4. **Logging and audit**: are audit trail requirements from the BRS implemented? Is PII excluded from logs?
5. **Integration security**: are integration credentials stored securely? Is inter-service auth in place?
6. **Security test coverage**: are security-specific test cases (unauthorized access, injection, boundary) present?

### Output structure

```markdown
# Security Review

## Review Metadata

| Field | Value |
|---|---|
| Finding set ID | SECR-{initiative-id}-{task-id} |
| Task ID | {task-id} |
| Deliverable | {deliverable name} |
| Reviewer | {persona} |
| Blocking status | Blocking / Non-blocking only / Informational |
| Required before | Fix / Merge / Release |

## Findings

| Finding ID | Severity | Area | Evidence | Risk | Recommendation | Owner | Required before | Blocking? |
|---|---|---|---|---|---|---|---|---|

## Security Control Coverage

| Control | Status | Evidence |
|---|---|---|

## Security Test Notes

## Decision
```

## Done criteria

- [ ] All 6 review areas assessed (Authorization, Input Validation, Data Handling, Audit, Integration, Test Coverage)
- [ ] Every blocking finding includes evidence and risk
- [ ] Authorization, data handling, and audit concerns explicitly addressed
- [ ] Decision is clear
- [ ] Result file written with `status: pass` and `artifacts_written` listing the review file path

## Stop conditions

- If relevant security artifacts are missing: review only what is supportable and list the gap.
- If changed scope is unclear: stop and request clarification.
- Do not invent security requirements not grounded in source artifacts or evident risk.
