# Prompt 23 - Create Test Plan Per Story

## Inputs to give Copilot

Required:

- `initiatives/<id>-<slug>/quality-gates/test-strategy.md`
- `initiatives/<id>-<slug>/planning/delivery-structure.md`
- all BDD files under `initiatives/<id>-<slug>/quality-gates/bdd/`
- `initiatives/<id>-<slug>/input/brs.md`
- any additional BRS markdown files under the initiative input folder
- `.b2s/artifact-templates/test-plan-per-story.md`

Optional:

- `initiatives/<id>-<slug>/business-analysis/business-rules.md`

## Output files to create

- one file per story under `initiatives/<id>-<slug>/quality-gates/test-plans/`

## Prompt for Office 365 Copilot

You are following the `.b2s` framework action `create-test-plan-per-story`.

Run this after the test strategy exists and standalone BDD files exist.

Read all provided inputs in full before writing anything.

Create one file per story under `quality-gates/test-plans/`. Derive globally
sequential `TC-NNN` cases from:

- business rule branches
- boundary values
- null inputs
- error paths

Ensure:

- every story has a test plan file
- every relevant business rule branch has `TC` coverage
- `TC-NNN` IDs are globally sequential
- status is `In progress`

The goal is to give each user story acceptance-test depth, not just initiative-
level testing guidance.
