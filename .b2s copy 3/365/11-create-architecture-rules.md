# Prompt 11 - Create Architecture Rules

## Inputs to give Copilot

Required:

- `initiatives/<id>-<slug>/architecture/architecture-review.md`
- `initiatives/<id>-<slug>/input/brs.md`
- any additional BRS markdown files under the initiative input folder
- `.b2s/artifact-templates/architecture-rules.md`

Optional:

- `initiatives/<id>-<slug>/business-analysis/business-rules.md`

## Output file to create

- `initiatives/<id>-<slug>/architecture/architecture-rules.md`

## Prompt for Office 365 Copilot

You are following the `.b2s` framework action `create-architecture-rules`.

Read the architecture review and all provided source inputs in full before
writing anything. Your job is to convert architecture-review constraints into a
stable, numbered `AR-NNN` ruleset that downstream engineering work must obey.

Extract each binding constraint and normalize it into an `AR-NNN` rule.

Rule categories:

- Boundary
- Technology
- Data
- Security
- Integration
- Observability
- Forbidden Pattern

For each rule, include:

- rule statement
- rationale
- source
- scope

Write `architecture/architecture-rules.md` using the provided template.

Before finalizing, ensure:

- every meaningful constraint from the architecture review has an `AR-NNN`
- every rule has rationale and source
- forbidden patterns are explicit where applicable
- rules are implementable and unambiguous
- no new rules are invented beyond the supplied source material
- status is `Draft`
