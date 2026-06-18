# Prompt 19 - Create API Contract

## Inputs to give Copilot

Required:

- `initiatives/<id>-<slug>/engineering-readiness/readiness-check.md`
- `initiatives/<id>-<slug>/architecture/architecture-review.md`
- `initiatives/<id>-<slug>/architecture/architecture-rules.md`
- `initiatives/<id>-<slug>/business-analysis/business-rules.md`
- `initiatives/<id>-<slug>/input/brs.md`
- any additional BRS markdown files under the initiative input folder
- `.b2s/artifact-templates/api-contract.md`

## Output file to create

- `initiatives/<id>-<slug>/quality-gates/api-contract.md`

## Prompt for Office 365 Copilot

You are following the `.b2s` framework action `create-api-contract`.

Run this only when `API Contract` is explicitly triggered in the readiness
check. If not triggered, stop and say the action does not apply.

Read all provided inputs in full before writing anything.

Enumerate every new, changed, removed, or impacted endpoint and document:

- auth and authorization
- request and response shape
- field-level schema expectations
- error codes
- idempotency
- compatibility
- consumer impact

Write `quality-gates/api-contract.md` using the provided template.

Before finalizing, ensure every new or changed endpoint has an `EP-NNN`, auth
is explicit, schemas and error codes are concrete, and breaking changes include
migration or versioning notes. Status must be `In progress`.
