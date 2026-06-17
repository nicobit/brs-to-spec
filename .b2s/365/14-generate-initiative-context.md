# Prompt 14 - Generate Initiative Context

## Inputs to give Copilot

Required:

- `initiatives/<id>-<slug>/engineering-readiness/readiness-check.md`
- `initiatives/<id>-<slug>/architecture/architecture-rules.md`
- `initiatives/<id>-<slug>/architecture/architecture-review.md`
- `.b2s/artifact-templates/initiative-context.md`

## Output file to create

- `initiatives/<id>-<slug>/engineering-readiness/initiative-context.md`

## Prompt for Office 365 Copilot

You are following the `.b2s` framework action `generate-initiative-context`.

Run this only after the readiness check is approved. Read all provided inputs in
full before writing anything.

Extract only binding implementation context:

- technology constraints
- architecture rules in force
- governed boundaries
- active quality gates
- rollback and regression sensitivity
- open risks
- carried-forward context

Copy `AR-NNN` rules verbatim rather than paraphrasing them.

Write `engineering-readiness/initiative-context.md` using the provided
template.

Before finalizing, ensure:

- `AR-NNN` rules are verbatim
- technology constraints come from evidence
- triggered gates are listed
- carried-forward context is populated or explicitly marked none
- AI model version is populated
