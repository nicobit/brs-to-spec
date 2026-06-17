# Prompt 06 - Define Stage Actions and State

## Goal

Turn the `.brs2spec2` event-driven workflow into a staged `.b2s` action model.

## Files to modify

- `.b2s/workflow/workflow-definition.yaml`
- `.b2s/workflow/stage-actions.yaml`
- `.b2s/templates/state/workflow-state.json`
- `.b2s/templates/state/open-decisions.md`

## Required work

- define the `.b2s` stage graph using `.brs2spec2/workflow/workflow-definition.yaml` as source
- create stage actions derived from the relevant `.brs2spec2` event templates
- capture required/optional inputs, outputs, validation expectations, conditions, and blocking rules
- define a compact staged `workflow-state.json` schema
- formalize the stage-action schema and action lifecycle from `02-stage-action-model.md`
- formalize gate fields and allowed artifact statuses from `04b-state-and-gate-model.md`

## Constraints

- do not recreate runtime event files
- do not introduce queue buckets
- preserve `.brs2spec2` output paths and stage ordering where they are still valid
- define the first implementation as single-active-action only

## Verification

Verify:

1. every core `.brs2spec2` stage has a `.b2s` counterpart
2. stage actions preserve input/output/validation intent
3. the state schema is sufficient to restart and resume without event files
4. stage actions follow one explicit schema rather than prompt-invented fields
