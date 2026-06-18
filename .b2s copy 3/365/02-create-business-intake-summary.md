# Prompt 02 - Create Business Intake Summary

## Inputs to give Copilot

Required:

- `initiatives/<id>-<slug>/input/brs.md`
- any additional BRS markdown files under the initiative input folder
- `initiatives/<id>-<slug>/routing/routing-decision.md`
- `.b2s/artifact-templates/business-intake-summary.md`

Optional:

- `initiatives/<id>-<slug>/input/architecture.md`
- `initiatives/<id>-<slug>/input/input-package.md`

## Output file to create

- `initiatives/<id>-<slug>/business-intake/business-intake-summary.md`

## Prompt for Office 365 Copilot

You are following the `.b2s` framework action
`create-business-intake-summary`.

Read every provided input fully before writing anything. Your output is the
normalization layer between the raw BRS and all downstream framework artifacts.

Rules:

- never write a skeleton only to satisfy structure
- assign canonical IDs here
- never bundle multiple atomic requirements into one row
- never compress multiple unresolved questions into one gap row
- keep the major business sections as real tables
- do not invent requirements not present in the source
- if two source documents conflict, record the conflict rather than silently
  merging it away

Write the output using the provided template and populate all sections:

- Metadata
- Executive Summary
- Source Document Inventory
- Objectives
- Scope
- Requirements
- Capabilities
- Existing-System Context
- Optional Visual View only if it adds real value
- Gaps and Questions
- Risks and Assumptions
- Consolidation Notes
- PO Review Checklist

Canonical ID conventions:

- objectives: `OBJ-NNN`
- functional requirements: `FR-NNN`
- non-functional requirements: `NFR-NNN`
- gaps: `GAP-NNN`
- risks: `RSK-NNN`

Use `routing/routing-decision.md` to shape the level of detail:

- `FastPath`: keep it deliberately small but still real
- `BusinessCopilot`: write for non-technical business stakeholders
- `OpenSpec` or `Standalone`: produce the full artifact

Before finalizing, ensure:

- every objective has a specific success measure
- every requirement row has business value and source reference
- every unresolved question becomes its own actionable `GAP-NNN`
- scope is explicit in-scope and out-of-scope content
- status is `Draft`
- no placeholder text remains

If the BRS is missing, empty, or has no extractable requirements, stop and say
so instead of fabricating output.
