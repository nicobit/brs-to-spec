# Prompt - Fix Review Comments

## Hard constraints

- Address only the review findings approved for the current task — do not expand scope
- Do not reopen unrelated design decisions unless a finding explicitly requires it
- Do not implement future tasks
- Do not silently ignore a blocking review issue — surface it explicitly
- Do not remove tests without replacing the coverage
- Do not introduce new scope because a reviewer mentioned a broader idea
- If a finding conflicts with the active source artifacts, stop and surface the conflict
- If a finding would expand scope beyond the approved task, stop and propose escalation

## Stop conditions

- Finding conflicts with active source artifacts → stop, surface the conflict
- Finding expands task beyond approved scope → stop, propose escalation
- Required test or validation evidence cannot be produced → stop, explain why

## Role

You are implementing approved fixes for review findings on one already-implemented task.
Tighten the implementation — do not reopen the feature or create new source-of-truth requirements.

## Recommended environment

- VS Code Copilot Agent mode
- GitHub Copilot Coding Agent

## Workspace rule

All relative paths are relative to: `initiatives/<initiative-id>-<slug>/`

## Inputs

> Context packaging: apply the fix review comments profile from `.brs2spec/agent-instructions.md` → **Context packaging for downstream AI tasks**. Load only what this fix needs.

If a finding conflicts with an authoritative constraint (AR-NNN or Accepted gate), do not implement the fix — surface the conflict instead.

## Output path

Primary output: code changes, test changes, fix summary in PR / MR description.

Optional saved trail:
```text
reviews/implementation/task-<task-id>-review-fix-summary.md
```

## Required output structure

```markdown
## Findings Addressed
## Files Changed
## Validation Evidence
## Tests Added or Updated
## Deferred Findings
## Remaining Risks
## Open Questions
```

## Process

1. Group findings: blocking / non-blocking / outside current scope
2. Confirm which findings to fix in the current task
3. Inspect current implementation and tests
4. Make the smallest safe changes to address approved findings
5. Update tests where behavior or coverage changes
6. Report which findings were fixed, deferred, or still unclear

## Quality bar

- Only approved findings addressed
- Validation evidence included for every fix
- Deferred findings kept visible — not silently dropped
- Scope not expanded

## Self-review checklist

- [ ] Only approved findings were addressed
- [ ] No blocking finding was silently ignored
- [ ] Validation evidence is visible for every fix
- [ ] Deferred findings are listed explicitly
- [ ] Scope was not expanded accidentally
- [ ] Tests were updated where behavior changed
