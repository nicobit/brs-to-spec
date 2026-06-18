# Prompt 08 - Review Initial Architecture

## Inputs to give Copilot

Required:

- `initiatives/<id>-<slug>/business-intake/business-intake-summary.md`
- `initiatives/<id>-<slug>/routing/routing-decision.md`
- `initiatives/<id>-<slug>/input/brs.md`
- any additional BRS markdown files under the initiative input folder
- `.b2s/artifact-templates/architecture-review.md`

Optional:

- `initiatives/<id>-<slug>/input/architecture.md`
- `initiatives/<id>-<slug>/business-analysis/business-rules.md`
- `initiatives/<id>-<slug>/business-analysis/requirements.md`
- `initiatives/<id>-<slug>/business-analysis/gaps-and-questions.md`

## Output file to create

- `initiatives/<id>-<slug>/architecture/architecture-review.md`

## Prompt for Office 365 Copilot

You are following the `.b2s` framework action `review-initial-architecture`.

Read all provided inputs in full before writing anything. If
`input/architecture.md` is missing, proceed with a BRS-driven review and state
that the basis is weaker.

Assess:

- initiative-architecture fit by major feature area
- architectural constraints with rationale and violation consequences
- brownfield impact
- open decisions and default assumptions
- active assumptions and what changes if they are false
- known unknowns
- quality attributes such as performance, security, scalability, and
  availability

Write `architecture/architecture-review.md` using the provided template.

Use the exact column names from the template for each table section. In
particular, `## Quality Attribute Assessment` must be one flat table with
columns `Attribute | Requirement (from BRS) | Assessment | Risk` — do not
split into sub-headings per attribute.

The artifact must be specific and actionable. Do not produce a summary-only
placeholder.

Before finalizing, ensure:

- every major feature area is assessed for architecture fit
- every constraint has rationale and violation consequence
- brownfield impact is explicit
- open decisions have owners and default assumptions
- active assumptions include `If False, Then` consequences
- status is `Draft`

Do not mention framework engine mechanics. Write only the artifact content.
