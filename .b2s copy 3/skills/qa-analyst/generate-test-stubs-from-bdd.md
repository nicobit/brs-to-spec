# Skill - Generate Test Stubs from BDD

## Identity

```text
skill_id:    qa-analyst.generate-test-stubs-from-bdd
persona:     qa-analyst
action_id:   generate-test-stubs-from-bdd
produces:    target test folders
```

## When this skill is used

Run this only after accepted BDD scenarios and test strategy exist. It generates failing stub files, not real implementations.

## Preconditions

Before starting, verify:
- `quality-gates/bdd/` exists with complete Gherkin
- `quality-gates/test-strategy.md` exists
- `engineering-readiness/initiative-context.md` exists

If framework or test folder cannot be determined from source evidence, stop and ask rather than guessing.

## Instructions

### Step 1 - Read all inputs

Read these files in full before writing anything:
- `{workspace_root}/quality-gates/test-strategy.md`
- `{workspace_root}/engineering-readiness/initiative-context.md`
- All Gherkin scenario files under `{workspace_root}/quality-gates/bdd/`

If optional files exist, read them too:
- All test plan files under `{workspace_root}/quality-gates/test-plans/`

Do not start writing until all available inputs are read completely.

### Step 2 - Determine framework and target folder from test strategy and repository descriptors, then generate:
- one failing BDD stub per `SCN-NNN`
- one failing unit stub per `TC-NNN` when test plans exist

Keep `bdd/` and `unit/` outputs separate.
