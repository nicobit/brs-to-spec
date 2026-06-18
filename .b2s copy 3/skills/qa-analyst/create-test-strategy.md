# Skill - Create Test Strategy

## Identity

```text
skill_id:    qa-analyst.create-test-strategy
persona:     qa-analyst
action_id:   create-test-strategy
produces:    quality-gates/test-strategy.md
```

## When this skill is used

Run this only when the readiness check explicitly triggers the test strategy gate.

## Preconditions

Before starting, verify:
- `engineering-readiness/readiness-check.md` marks Test Strategy as triggered
- BRS source files are readable
- `architecture/architecture-review.md` exists
- `planning/delivery-structure.md` exists

If the gate was not triggered, stop and say the action does not apply.

## Instructions

### Step 1 - Read all inputs

Read these files in full before writing anything:
- `{workspace_root}/engineering-readiness/readiness-check.md`
- `{workspace_root}/architecture/architecture-review.md`
- `{workspace_root}/planning/delivery-structure.md`
- BRS source files under `{workspace_root}/input/`

Do not start writing until all available inputs are read completely.

### Step 2 - Define strategy

Define required test levels, framework choices from architecture evidence, coverage targets, test data strategy, and gate-to-test execution mapping.

Technology choices must come from source evidence. If the stack is unknown, flag the gap rather than guessing.

## Output requirements

Write `quality-gates/test-strategy.md` using `.b2s/artifact-templates/test-strategy.md`.

## Done criteria

- [ ] Every triggered level has a framework and coverage target
- [ ] Gate-to-test mapping is explicit
- [ ] PII handling is addressed in test data strategy
- [ ] Status is `In progress`
