# Prompt 06 - Create Use Case Specs

## Inputs to give Copilot

Required:

- `initiatives/<id>-<slug>/business-analysis/requirements.md`
- `initiatives/<id>-<slug>/business-analysis/use-cases.puml`
- `initiatives/<id>-<slug>/business-analysis/use-cases.md`
- `.b2s/artifact-templates/use-case-detail.md`

Optional:

- `initiatives/<id>-<slug>/business-analysis/business-rules.md`
- `initiatives/<id>-<slug>/business-analysis/actors-and-personas.md`
- `initiatives/<id>-<slug>/architecture/architecture-review.md`

## Output files to create

- one file per use case under `initiatives/<id>-<slug>/business-analysis/use-cases/`

## Prompt for Office 365 Copilot

You are following the `.b2s` framework action `create-use-case-specs`.

Read `use-cases.puml` and extract the authoritative `UC-NNN` list. Read
`requirements.md` and build a private coverage map:

- `UC-NNN -> covered FR-NNNs`
- `FR-NNN -> owning UC-NNNs`

Do not write files until every `FR-NNN` is covered by a use case or explicitly
excluded with justification.

For each `UC-NNN`, create a separate markdown file using the provided
`use-case-detail` template.

Each file must include:

- overview
- preconditions
- main success scenario
- at least one meaningful alternative flow
- exception paths
- postconditions
- business rules referenced
- FR sources

Validate completeness before finishing:

- every `UC-NNN` from the diagram has exactly one file
- no file contains more than one use case
- every `FR-NNN` is covered by at least one use case or explicitly excluded
- actor references are consistent
- no file is a shallow stub

All files must have `Status: Draft`.
