# Skill - Create Test Plan Per Story

## Identity

```text
skill_id:    qa-analyst.create-test-plan-per-story
persona:     qa-analyst
action_id:   create-test-plan-per-story
produces:    quality-gates/test-plans/F-NNN.X.md
```

## When this skill is used

Run this after test strategy and BDD outputs exist. It defines unit-level `TC-NNN` cases per story.

## Preconditions

Before starting, verify:
- `quality-gates/test-strategy.md` exists
- `quality-gates/bdd/` exists
- `planning/delivery-structure.md` exists
- `business-analysis/business-rules.md` exists when available
- BRS source files are readable

## Instructions

### Step 1 - Read all inputs

Read these files in full before writing anything:
- `{workspace_root}/quality-gates/test-strategy.md`
- `{workspace_root}/planning/delivery-structure.md`
- All BDD scenario files under `{workspace_root}/quality-gates/bdd/`
- All BRS source files under `{workspace_root}/input/`

If optional files exist, read them too:
- `{workspace_root}/business-analysis/business-rules.md`

Do not start writing until all available inputs are read completely.

### Step 2 - Create one file per story under `quality-gates/test-plans/` and derive `TC-NNN` cases from business rule branches, boundary values, null inputs, and error paths.

## Output requirements

Use `.b2s/artifact-templates/test-plan-per-story.md` as the shape for each story file.

## Done criteria

- [ ] Every story has a test plan file
- [ ] Every relevant business rule branch has TC coverage
- [ ] `TC-NNN` IDs are globally sequential
- [ ] Status is `In progress`
