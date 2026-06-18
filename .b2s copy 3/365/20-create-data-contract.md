# Prompt 20 - Create Data Contract

## Inputs to give Copilot

Required:

- `initiatives/<id>-<slug>/engineering-readiness/readiness-check.md`
- `initiatives/<id>-<slug>/architecture/architecture-review.md`
- `initiatives/<id>-<slug>/business-analysis/business-rules.md`
- `.b2s/artifact-templates/data-contract.md`

Optional but strongly recommended:

- `initiatives/<id>-<slug>/business-analysis/entity-model.md`
- `initiatives/<id>-<slug>/input/brs.md`
- any additional BRS markdown files under the initiative input folder

## Output file to create

- `initiatives/<id>-<slug>/quality-gates/data-contract.md`

## Prompt for Office 365 Copilot

You are following the `.b2s` framework action `create-data-contract`.

Run this only when `Data Contract` is explicitly triggered in the readiness
check. If not triggered, stop and say the action does not apply.

Read all provided inputs in full before writing anything.

Document each new or changed data asset with:

- classification
- schema
- PII handling
- encryption
- retention
- access control
- flow
- migration approach

Write `quality-gates/data-contract.md` using the provided template.

Before finalizing, ensure every new or changed data asset has a `DA-NNN`, PII
handling is explicit, migration is documented, and access control is clear.
Status must be `In progress`.
