# Prompt 16 - Create Test Strategy

## Inputs to give Copilot

Required:

- `initiatives/<id>-<slug>/engineering-readiness/readiness-check.md`
- `initiatives/<id>-<slug>/architecture/architecture-review.md`
- `initiatives/<id>-<slug>/planning/delivery-structure.md`
- `initiatives/<id>-<slug>/input/brs.md`
- any additional BRS markdown files under the initiative input folder
- `.b2s/artifact-templates/test-strategy.md`

## Output file to create

- `initiatives/<id>-<slug>/quality-gates/test-strategy.md`

## Prompt for Office 365 Copilot

You are following the `.b2s` framework action `create-test-strategy`.

Run this only when `Test Strategy` is explicitly triggered in the readiness
check. If not triggered, stop and say the action does not apply.

Read all provided inputs in full before writing anything.

Define:

- required test levels
- framework choices from architecture evidence
- coverage targets
- test data strategy
- gate-to-test execution mapping

Technology choices must come from source evidence. If the stack is unknown, flag
the gap rather than guessing.

Write `quality-gates/test-strategy.md` using the provided template.

Before finalizing, ensure:

- every triggered level has a framework and coverage target
- gate-to-test mapping is explicit
- PII handling is addressed in test data strategy
- status is `In progress`
