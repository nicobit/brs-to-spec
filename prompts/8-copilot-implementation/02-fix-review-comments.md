# Prompt - Fix Review Comments

## Recommended environment

- VS Code Copilot Agent mode
- GitHub Copilot Coding Agent
- Another approved coding agent with repository and test access

## Role

You are implementing approved fixes for review findings on one already-implemented task.

## Context

This is a downstream implementation helper.

It should tighten an already-scoped implementation, not reopen the whole feature or create new source-of-truth requirements.

## Workspace rule

Work inside one initiative workspace at a time.

All relative paths below are relative to:

```text
initiatives/<initiative-id>-<slug>/
```

## Purpose

Address review findings for one implemented task without expanding scope.

## Inputs

Use:

- the active downstream task artifact
- the changed files
- the relevant tests
- the review findings
- the relevant initiative workspace source artifacts needed to understand the finding

## Output path

There is no mandatory new framework artifact.

Primary output is:

```text
code changes
test changes
fix summary in the coding session or PR / MR description
```

Optional saved review trail:

```text
reviews/implementation/task-<task-id>-review-fix-summary.md
```

## Required output structure

Return a final fix summary using:

```markdown
## Findings Addressed
## Files Changed
## Validation Evidence
## Tests Added or Updated
## Deferred Findings
## Remaining Risks
## Open Questions
```

## Quality bar

A good fix pass must:

- address only the review findings approved for the current task
- preserve the original task scope unless the finding explicitly requires escalation
- include validation evidence for the fix
- keep deferred findings visible rather than silently dropping them

## Anti-patterns to avoid

Do not:

- reopen unrelated design decisions
- implement future tasks
- silently ignore a blocking review issue
- remove tests without replacing the coverage
- introduce new scope because a reviewer mentioned a broader idea

## Stop conditions

- If the review finding conflicts with the active source artifacts, stop and surface the conflict.
- If the review finding would expand the task beyond its approved scope, stop and propose escalation.
- If the required test or validation evidence cannot be produced, stop and explain why.

## Self-review checklist

Before finalizing, verify:

- [ ] Only the approved findings were addressed.
- [ ] Blocking findings were not silently ignored.
- [ ] Validation evidence is visible.
- [ ] Deferred findings are explicit.
- [ ] Scope was not expanded accidentally.

## Required process

1. Group review findings into:
   - blocking
   - non-blocking
   - follow-up / outside current scope
2. Confirm which findings should be fixed in the current task.
3. Inspect the current implementation and tests.
4. Make the smallest safe changes needed to address the approved findings.
5. Update tests when behavior or coverage changes.
6. Report which findings were fixed, deferred, or still unclear.

## Mandatory rules

- Do not reopen unrelated design decisions unless a review finding explicitly requires it.
- Do not implement future tasks.
- Do not silently ignore a blocking review issue.
- Do not remove tests without replacing the coverage.
