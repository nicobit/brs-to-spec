# Prompt 03 - Business Intake Review Gate

## Inputs to give Copilot

Required:

- `initiatives/<id>-<slug>/business-intake/business-intake-summary.md`
- `initiatives/<id>-<slug>/input/brs.md`
- any additional BRS markdown files used in step 2

Optional:

- `initiatives/<id>-<slug>/routing/routing-decision.md`

## Output file to create

- no framework artifact is created in this step

## Prompt for Office 365 Copilot

You are supporting the `.b2s` business intake review gate.

Review the provided `business-intake-summary.md` against the source BRS content.
Do not rewrite the artifact unless a concrete issue is found.

Produce a review note with these sections:

- Overall gate recommendation: `Approve` or `Needs changes`
- Missing objectives or requirements
- Incorrect normalization or merged items
- Unresolved conflicts between sources
- Gaps that are already answered but still listed as open
- Gaps that are missing but should exist
- Scope errors
- Confidence level

Approval rules:

- approve only if the business intake summary is complete, traceable, and ready
  to act as the normalized business source for downstream work
- recommend changes if objectives, scope, requirements, gaps, or source
  traceability are materially incomplete or incorrect

If the recommendation is `Needs changes`, list the minimum concrete fixes
required before moving to requirements generation.
