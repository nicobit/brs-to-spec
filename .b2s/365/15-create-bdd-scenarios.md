# Prompt 15 - Create BDD Scenarios

## Inputs to give Copilot

Required:

- `initiatives/<id>-<slug>/engineering-readiness/readiness-check.md`
- `initiatives/<id>-<slug>/planning/delivery-structure.md`
- `initiatives/<id>-<slug>/business-analysis/business-rules.md`
- `initiatives/<id>-<slug>/business-analysis/actors-and-personas.md`
- `initiatives/<id>-<slug>/input/brs.md`
- any additional BRS markdown files under the initiative input folder
- `.b2s/artifact-templates/bdd-scenarios.md`

## Output files to create

- one file per feature under `initiatives/<id>-<slug>/quality-gates/bdd/`

## Prompt for Office 365 Copilot

You are following the `.b2s` framework action `create-bdd-scenarios`.

Run this only when `BDD` is explicitly triggered in
`engineering-readiness/readiness-check.md`. If `BDD` was not triggered, stop and
say that story-level BDD will instead be embedded later inside the OpenSpec
handoff.

Read all provided inputs in full before writing anything.

Create one BDD file per feature under `quality-gates/bdd/`. Assign globally
sequential `SCN-NNN` IDs.

Every scenario must:

- be valid Given/When/Then Gherkin
- describe observable business behavior, not implementation steps
- have a meaningful scenario name
- link to the `AC-NNN` it validates
- link to the story ID `F-XXX.X`

Required scenario coverage per story includes all applicable types:

- happy path
- negative or validation
- authorization or permission
- business rule enforcement
- state transition
- integration failure
- audit or compliance
- edge case

If a scenario type does not apply, document why it was omitted instead of
silently skipping it.

Status must be `In progress`.
