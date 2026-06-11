# Prompt - Implement One Task

## Hard constraints

- Implement exactly one task — do not implement future tasks or expand scope
- Do not implement directly from raw BRS — use only the approved task artifact
- Do not re-derive technology constraints — trust `initiative-context.md`
- Do not perform unrelated refactoring
- Do not invent business rules
- Do not introduce new dependencies without approval
- Do not weaken security, authorization, auditability, or validation
- Do not ignore architecture constraints recorded in the initiative workspace
- Do not treat the planning view as the execution source of truth

## Stop conditions

- No approved active task artifact → stop
- `initiative-context.md` missing → run `.brs2spec/4-engineering-readiness/02-generate-initiative-context.md` first
- `readiness-check.md` missing → stop
- Required quality gate missing for this task → stop and report it
- Architecture constraints unclear and materially affect implementation → stop and report it
- No SCN-NNN referenced for the task → check `quality-gates/bdd-scenarios.md`; if none exist, note it as a risk before continuing

## Done criteria

A task is done when:

- Every referenced SCN-NNN scenario passes in CI (or a stub exists with a documented failure reason)
- All required tests are added or updated
- The implementation summary is written

## Role

You are implementing one approved engineering task for the active initiative workspace.
All relative paths are relative to: `initiatives/<initiative-id>-<slug>/`

## Recommended environment

- VS Code Copilot Agent mode
- GitHub Copilot Coding Agent

## Inputs

Load in this order:

```text
1. engineering-readiness/initiative-context.md          ← load first, always
2. quality-gates/bdd-scenarios.md                       ← identify SCN-NNN for this task
3. openspec/changes/D1-<name>/tasks.md                  ← or standalone-delivery/D1-<name>/tasks.md
4. openspec/changes/D1-<name>/design.md                 ← or standalone-delivery/D1-<name>/delivery-spec.md
5. engineering-readiness/readiness-check.md
6. quality-gates/*.md relevant to the task
```

Read only artifacts relevant to the selected execution mode and active task.

## Output

Primary output: code changes, test changes, implementation summary in the PR / MR description.

Optional saved trail:
```text
reviews/implementation/task-<task-id>-implementation-summary.md
```

## Required output structure

```markdown
## Task Implemented
## BDD Scenarios Covered (SCN-NNN list)
## Files Changed
## Requirements / Artifacts Covered
## Validation Evidence
## Tests Added or Updated
## Assumptions
## Risks
## Remaining Open Questions
```

## Process

1. Identify the exact task ID and scope
2. Identify SCN-NNN scenarios from `quality-gates/bdd-scenarios.md` that cover this task
3. Identify files likely to change
4. Inspect existing similar implementation patterns before editing
5. Implement only that task
6. Add or update tests for every behavior change
7. Write the implementation summary

## Quality bar

- One task only, traced to the task artifact
- At least one SCN-NNN referenced as done criterion
- Validation evidence present — not just code changes
- Tests updated for every behavior change
- Architecture constraints respected
- Assumptions and risks explicit

## Self-review checklist

- [ ] Exactly one task implemented
- [ ] Implementation traces back to the active task artifact
- [ ] At least one SCN-NNN referenced as done criterion
- [ ] Every implemented behavior covered by at least one SCN-NNN
- [ ] Referenced BDD scenarios pass (or stubs exist with documented failure reason)
- [ ] Tests added or updated for every behavior change
- [ ] Validation evidence visible
- [ ] Scope not silently expanded
- [ ] Assumptions and risks explicit
