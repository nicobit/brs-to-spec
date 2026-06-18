# Prompt 01 - Route Initiative

## Inputs to give Copilot

Required:

- `initiatives/<id>-<slug>/input/brs.md`
- any additional BRS markdown files under `initiatives/<id>-<slug>/input/brs/` or equivalent input folder
- `.b2s/artifact-templates/routing-decision.md`

Optional:

- `initiatives/<id>-<slug>/input/architecture.md`
- `initiatives/<id>-<slug>/input/input-package.md`

## Output file to create

- `initiatives/<id>-<slug>/routing/routing-decision.md`

## Prompt for Office 365 Copilot

You are following the `.b2s` framework action `route-initiative`.

Read every provided BRS input in full before writing anything. If supporting
files such as `architecture.md` or `input-package.md` are present, use them as
context, but treat the BRS as the primary source.

Your job is to choose the minimum safe delivery mode and execution mode before
any downstream action starts.

Score each criterion as `Low`, `Medium`, or `High` using evidence from the
inputs:

- requirement ambiguity
- architecture impact
- compliance or audit relevance
- business criticality
- number of teams
- delivery size
- AI context saturation risk
- small-change path applicability
- regression or contract sensitivity

Selection rules:

- 3 or more `High` scores -> `Enterprise` or `Enterprise+Modular`
- use `Enterprise+Modular` when delivery size is high, or multiple teams plus
  module boundary complexity exist
- 1 to 2 `High` scores -> `Standard`
- 0 `High` scores and small-change path applicable -> `FastPath`

Execution mode rules:

- select `OpenSpec` when the initiative has 5 or more functional requirements,
  spans more than one team or service boundary, and can be decomposed into
  story-sized implementation work
- select `Standalone` only for a single-team, single-service change with fewer
  than 5 FRs, or when the team explicitly does not use OpenSpec-style handoff
- select `BusinessCopilot` only when the output is for business stakeholders
  rather than engineering implementation
- default to `OpenSpec` for a real multi-feature initiative

Write `routing/routing-decision.md` using the provided template and populate all
sections:

- Metadata
- Decision Summary
- Delivery Mode Assessment
- Execution Mode Assessment
- Required Next Actions
- Actions Not Needed
- Risks of Under-Processing
- Risks of Over-Processing
- Small-Change Path Notes
- Constraints

Exact allowed values:

- `delivery_mode`: `OpenSpec`, `Standalone`, `FastPath`, `BusinessCopilot`
- `execution_mode`: `Enterprise`, `Enterprise+Modular`, `Standard`

For `Required Next Actions`, list staged action IDs in execution order, not
event names.

Do not leave placeholders or generic filler. If the BRS is missing or too thin
to justify a real routing decision, stop and say so.
