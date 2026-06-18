# Prompt 04 - Create Requirements

## Inputs to give Copilot

Required:

- `initiatives/<id>-<slug>/business-intake/business-intake-summary.md`
- `initiatives/<id>-<slug>/input/brs.md`
- any additional BRS markdown files under the initiative input folder
- `.b2s/artifact-templates/requirements.md`

## Output file to create

- `initiatives/<id>-<slug>/business-analysis/requirements.md`

## Prompt for Office 365 Copilot

You are following the `.b2s` framework action `create-requirements`.

Read the business intake summary in full. Read all BRS inputs in full. Rebuild
the target file from the current inputs only.

Treat the BRS as the primary source of truth and the intake summary as the
normalization aid.

Build a complete inventory across three types:

- functional requirements `FR-NNN`: what the system must do
- non-functional requirements `NFR-NNN`: measurable quality attributes or
  objectively testable conditions
- constraints `C-NNN`: regulatory, platform, schedule, integration, or business
  boundaries

For each requirement:

1. assign a sequential ID in the correct series
2. write a short title
3. write the requirement statement in the proper format
4. assign priority: `High`, `Medium`, or `Low`
5. set status to `Open`
6. record the source reference

Write `business-analysis/requirements.md` using the provided template.

The artifact must contain:

- Metadata table with `Status: Draft`
- Functional Requirements table
- Non-Functional Requirements table
- Constraints table

Before finalizing, verify:

- all functional requirements are represented as individual rows
- all non-functional requirements are explicit
- all constraints are explicit
- every NFR contains a measurable threshold or objectively testable condition
- every row has a source reference
- no duplicate IDs exist
- no invented requirements remain

If the BRS and intake summary conflict, preserve the BRS-backed requirement and
record the conflict instead of silently merging it away.
