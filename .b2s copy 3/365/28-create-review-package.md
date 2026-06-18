# Prompt 28 - Create Review Package

## Inputs to give Copilot

Required:

- `initiatives/<id>-<slug>/business-intake/business-intake-summary.md`
- `initiatives/<id>-<slug>/planning/delivery-structure.md`
- `initiatives/<id>-<slug>/architecture/architecture-review.md`
- `.b2s/artifact-templates/review-package.md`

Optional:

- `initiatives/<id>-<slug>/specs/`
- `initiatives/<id>-<slug>/standalone-delivery/`
- `initiatives/<id>-<slug>/business-analysis/`

## Output files to create

- the assembled package under `initiatives/<id>-<slug>/review-package/`

## Prompt for Office 365 Copilot

You are following the `.b2s` framework action `create-review-package`.

Read all provided inputs in full before writing anything.

Assemble the review package from existing artifacts. If a source section is
missing, mark it clearly as missing rather than inventing content.

This package is for stakeholder-friendly review and should point back to the
real source artifacts where needed.
