# Prompt 24 - Create OpenSpec Handoff

## Inputs to give Copilot

Required:

- `initiatives/<id>-<slug>/planning/delivery-structure.md`
- `initiatives/<id>-<slug>/engineering-readiness/initiative-context.md`
- `initiatives/<id>-<slug>/architecture/architecture-rules.md`
- `initiatives/<id>-<slug>/engineering-readiness/readiness-check.md`
- `.b2s/artifact-templates/story-package.md`

Read if present:

- `initiatives/<id>-<slug>/business-analysis/requirements.md`
- `initiatives/<id>-<slug>/business-analysis/business-rules.md`
- files under `initiatives/<id>-<slug>/business-analysis/use-cases/`
- `initiatives/<id>-<slug>/business-analysis/actors-and-personas.md`
- `initiatives/<id>-<slug>/architecture/architecture-review.md`
- `initiatives/<id>-<slug>/planning/traceability-matrix.md`
- `initiatives/<id>-<slug>/quality-gates/bdd/`
- `initiatives/<id>-<slug>/quality-gates/api-contract.md`
- `initiatives/<id>-<slug>/quality-gates/data-contract.md`

## Output files to create

- `initiatives/<id>-<slug>/specs/dependency-graph.md`
- one folder per story under `initiatives/<id>-<slug>/specs/`
- in each story folder: `story.md`, `design.md`, `tasks.md`, `coding-prompt.md`

## Prompt for Office 365 Copilot

You are following the `.b2s` framework action `create-openspec-handoff`.

Run this only when:

- delivery mode is `OpenSpec`
- readiness decision is `Ready`
- all triggered gates are accepted

Read all provided inputs in full before writing anything.

Extract the full ordered list of story IDs from `planning/delivery-structure.md`.
The number of story folders you create must equal that story count exactly.

Create `specs/dependency-graph.md` with:

- story ID and title
- story dependencies
- external system dependencies
- recommended implementation order

For each story `F-XXX.X`, create `specs/F-XXX.X-<slug>/` and generate:

- `story.md`
- `design.md`
- `tasks.md`
- `coding-prompt.md`

`story.md` must follow the provided story-package template and fully populate:

- user story
- source traceability
- business rules applied
- acceptance criteria
- BDD scenarios
- implementation context
- constraints
- dependencies
- implementation tasks
- test expectations
- definition of done
- coding-agent prompt

If standalone BDD files exist, reuse them rather than inventing different
scenarios. If BDD was not gate-triggered, still embed story-level BDD scenarios
in each `story.md`.

The result should be the closest Office 365 equivalent to the richer VS Code
handoff package.
