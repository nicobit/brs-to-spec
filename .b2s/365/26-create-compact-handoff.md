# Prompt 26 - Create Compact Handoff

## Inputs to give Copilot

Required:

- `initiatives/<id>-<slug>/engineering-readiness/readiness-check.md`
- all files under either `initiatives/<id>-<slug>/specs/` or `initiatives/<id>-<slug>/standalone-delivery/`
- `.b2s/artifact-templates/compact-handoff.md`

## Output file to create

- `initiatives/<id>-<slug>/handoff/compact-handoff-summary.md`

## Prompt for Office 365 Copilot

You are following the `.b2s` framework action `create-compact-handoff`.

Run this only after the real handoff already exists under `specs/` or
`standalone-delivery/`. This summary does not replace the real handoff.

Read the readiness check and the full real handoff package before writing
anything.

Summarize:

- initiative and mode metadata
- binding `AR-NNN` rules
- gate status
- story counts
- accepted risks
- pointers to the real handoff artifacts
