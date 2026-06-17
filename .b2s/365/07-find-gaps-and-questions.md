# Prompt 07 - Find Gaps And Questions

## Inputs to give Copilot

Required:

- `initiatives/<id>-<slug>/business-intake/business-intake-summary.md`
- `initiatives/<id>-<slug>/business-analysis/requirements.md`
- `.b2s/artifact-templates/gaps-and-questions.md`

Optional:

- `initiatives/<id>-<slug>/business-analysis/entity-model.md`
- `initiatives/<id>-<slug>/business-analysis/use-cases.md`
- `initiatives/<id>-<slug>/business-analysis/business-rules.md`
- `initiatives/<id>-<slug>/architecture/architecture-review.md`

## Output file to create

- `initiatives/<id>-<slug>/business-analysis/gaps-and-questions.md`

## Prompt for Office 365 Copilot

You are following the `.b2s` framework action `find-gaps-and-questions`.

Read all provided inputs in full before writing. Review the source
systematically for:

- ambiguity gaps
- missing specification gaps
- conflict gaps
- scope boundary gaps
- acceptance-criteria gaps
- integration or external-system gaps
- data ownership or lifecycle gaps

If optional artifacts exist, cross-check them for omitted behaviors, unresolved
rules, and unresolved business questions.

For each gap, record:

- `GAP-NNN`
- category
- description
- impact
- severity: `Blocking`, `High`, or `Low`
- suggested resolution
- owner
- source

Write the output using the provided template and include:

- metadata with `Status: Draft`
- gap catalog
- critical path sections
- coverage summary

Separate:

- blocking gaps that must be resolved before planning or architecture
- high-severity gaps that should be resolved before handoff
- low-severity gaps that can proceed with explicit assumptions

Do not invent gaps. Only raise issues supported by the supplied artifacts.
