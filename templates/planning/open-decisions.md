# Open Decisions Register

> Primary consumer: Delivery lead, architect, PO, program lead
> Purpose: single view of every open decision across the initiative — status, owner, and which artifact holds the detail
> Updated at every workflow stage that creates or resolves a decision
> Do not copy decision detail here — reference the home artifact and link to it
> A decision marked Blocking must be resolved before the Required-before stage can proceed

## Metadata

| Field | Value |
|---|---|
| Initiative |  |
| Last updated |  |
| Updated by |  |
| Open blocking decisions | (count) |
| Open non-blocking decisions | (count) |
| Resolved decisions | (count) |

## Decision Register

| Decision ID | Decision | Status | Blocking? | Owner | Required before | Home artifact | Resolved date | Resolution summary |
|---|---|---|---|---|---|---|---|---|

Status values: `Open` / `In progress` / `Resolved` / `Accepted risk`

## Blocking decisions summary

List only decisions where Blocking = Yes and Status ≠ Resolved.
This section is the single place to check before advancing any stage.

| Decision ID | Decision | Owner | Required before | Action needed |
|---|---|---|---|---|

## How to use this register

**Adding a decision:**
When any prompt creates an open decision, add a row here immediately. Set status to Open. Do not wait until the end of the stage.

**Resolving a decision:**
When a human provides an answer — in `input/input-package.md`, a vendor call, a PO session — update the row: set Status to Resolved, fill in Resolved date and Resolution summary. Update the home artifact too.

**Before advancing a stage:**
Check the Blocking decisions summary. If any blocking decision for the next stage is still Open or In progress, the workflow must not advance.

**Accepting a risk:**
If a decision cannot be resolved before handoff and the team accepts the risk, set Status to Accepted risk, record who accepted it and when in Resolution summary, and move it out of the Blocking decisions summary.
