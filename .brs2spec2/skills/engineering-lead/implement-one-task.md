# Skill — Implement One Task

## Identity

| Field | Value |
|---|---|
| skill_id | eng-implement-one-task |
| persona | engineering-lead |
| event_types | IMPLEMENT_ONE_TASK |
| produces | code changes + reviews/implementation/task-{task-id}-implementation-summary.md |

## When this skill is used

When an engineer or AI coding agent is implementing one specific approved engineering task from the OpenSpec or Standalone handoff.

## Role for this task

You are implementing one approved engineering task for the active initiative workspace. You implement exactly one task — no scope expansion, no future tasks, no unrelated refactoring.

## Hard constraints

- Implement exactly one task
- Do not implement from raw BRS — use only the approved task artifact
- Do not re-derive technology constraints — trust `initiative-context.md`
- Do not perform unrelated refactoring
- Do not invent business rules
- Do not introduce new dependencies without approval
- Do not weaken security, authorization, auditability, or validation
- Do not ignore architecture constraints in the initiative workspace

## Prerequisites check

Before starting, verify:
- [ ] An approved task artifact exists (from `specs/F-XXX.X/tasks.md` or `standalone-delivery/D1-*/tasks.md`)
- [ ] `engineering-readiness/initiative-context.md` exists — REQUIRED, load first
- [ ] `engineering-readiness/readiness-check.md` exists

If any required artifact is missing: stop and report.

## Instructions

### Step 1 — Load context

Load in this order:
1. `engineering-readiness/initiative-context.md` — REQUIRED, always first
2. `specs/D1-{name}/tasks.md` or `standalone-delivery/D1-{name}/tasks.md` — the task artifact
3. `specs/D1-{name}/design.md` — sections relevant to this task only
4. `quality-gates/bdd/{F-NNN.md}` — required when SCN-NNN exist for this task
5. `architecture/architecture-rules.md` — AR-NNN rules relevant to this task
6. `engineering-readiness/readiness-check.md` — scope and gate decisions
7. Relevant quality gate files — only gates triggered for this initiative

**Precedence**: if `architecture-rules.md` conflicts with a note in `design.md`, the architecture rule wins.

### Step 2 — Implement the task

1. Identify the exact task ID and scope
2. Identify SCN-NNN scenarios for this task's feature
3. Identify files likely to change
4. Inspect existing similar implementation patterns before editing
5. Implement only that task
6. Add or update tests for every behaviour change
7. Write the implementation summary

### Step 3 — Write implementation summary

Output structure:
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

## Done criteria

- [ ] Exactly one task implemented
- [ ] Implementation traces to the approved task artifact
- [ ] At least one SCN-NNN referenced as done criterion
- [ ] Every implemented behaviour covered by at least one SCN-NNN
- [ ] Tests added or updated for every behaviour change
- [ ] Validation evidence present
- [ ] Scope not silently expanded
- [ ] Assumptions and risks explicit
- [ ] Result file written with `status: pass`

## Stop conditions

- No approved active task artifact → stop
- `initiative-context.md` missing → run `GENERATE_INITIATIVE_CONTEXT` first
- `readiness-check.md` missing → stop
- Required quality gate missing for this task → stop and report
- Architecture constraints unclear and affect implementation → stop and report
