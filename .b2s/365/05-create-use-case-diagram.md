# Prompt 05 - Create Use Case Diagram

## Inputs to give Copilot

Required:

- `initiatives/<id>-<slug>/business-analysis/requirements.md`
- `.b2s/artifact-templates/use-cases.md`

Optional:

- `initiatives/<id>-<slug>/business-intake/business-intake-summary.md`
- `initiatives/<id>-<slug>/input/brs.md`
- any additional BRS markdown files under the initiative input folder

## Output files to create

- `initiatives/<id>-<slug>/business-analysis/use-cases.puml`
- `initiatives/<id>-<slug>/business-analysis/use-cases.md`

## Prompt for Office 365 Copilot

You are following the `.b2s` framework action `create-use-case-diagram`.

Read `requirements.md` in full before writing anything. Use the intake summary
and BRS only as supporting context.

Identify every human role and external system that:

- initiates a use case
- participates as a secondary actor
- receives an output from a use case

Group requirements into actor-visible goals.

Rules:

- every use case must trace to at least one `FR-NNN`
- do not create one use case per requirement unless they are truly separate
  goals
- do not collapse the whole initiative into one generic use case
- preserve lifecycle breadth when the initiative spans multiple stages
- if requirements imply many distinct goals, do not stop at a tiny 2-3 use case
  model

Assign stable `UC-NNN` IDs starting from `UC-001`.

Create `business-analysis/use-cases.puml` with:

- `@startuml`
- `@enduml`
- `left to right direction`
- actors outside the system boundary
- all use cases inside one system rectangle
- quoted use case names when they contain hyphens

Create `business-analysis/use-cases.md` using the provided template.

Before finalizing, verify:

- every `UC-NNN` in the PUML exists in the markdown file
- actor names are identical across both files
- every use case traces to at least one `FR-NNN`
- the set covers the initiative breadth, not only the first entry flow

Do not invent use cases that are not traceable to the requirements catalog.
