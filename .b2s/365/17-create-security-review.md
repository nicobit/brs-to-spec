# Prompt 17 - Create Security Review

## Inputs to give Copilot

Required:

- `initiatives/<id>-<slug>/engineering-readiness/readiness-check.md`
- `initiatives/<id>-<slug>/architecture/architecture-review.md`
- `initiatives/<id>-<slug>/architecture/architecture-rules.md`
- `initiatives/<id>-<slug>/business-analysis/requirements.md`
- `initiatives/<id>-<slug>/input/brs.md`
- any additional BRS markdown files under the initiative input folder
- `.b2s/artifact-templates/security-review.md`

Optional:

- `initiatives/<id>-<slug>/business-analysis/business-rules.md`

## Output file to create

- `initiatives/<id>-<slug>/quality-gates/security-review.md`

## Prompt for Office 365 Copilot

You are following the `.b2s` framework action `create-security-review`.

Run this only when `Security Review` is explicitly triggered in the readiness
check. If not triggered, stop and say the action does not apply.

Read all provided inputs in full before writing anything.

Assess these six security domains:

- authorization
- authentication
- input validation
- sensitive data handling
- audit trail
- integration security

Every finding must include:

- evidence
- risk
- recommendation
- owner
- required-before timing

Write `quality-gates/security-review.md` using the provided template.

Status must be `In progress`.
