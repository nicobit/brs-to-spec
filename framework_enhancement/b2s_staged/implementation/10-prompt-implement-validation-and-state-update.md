# Prompt 10 - Implement Validation and State Update

## Goal

Implement the deterministic `.b2s` mechanics that enforce artifact truth after
prompt generation.

## Files to modify

- `.b2s/scripts/b2s_cli.py`
- `.b2s/scripts/b2s_engine/validation.py`
- `.b2s/scripts/b2s_engine/state.py`

## Commands to implement

- `validate-artifact`
- `update-state`

## `validate-artifact` responsibilities

- verify artifact existence
- run placeholder checks
- run count checks where applicable
- verify required sections/IDs from action validation rules
- write `.b2s/tmp/current-validation.yaml`
- follow the `current-validation.yaml` contract from `04a-output-file-contracts.md`

## `update-state` responsibilities

- update `workflow-state.json`
- update open decision counts
- record last completed action and next action
- write `.b2s/tmp/current-state-update.json`
- follow the `current-state-update.json` contract from `04a-output-file-contracts.md`
- update gate fields according to `04b-state-and-gate-model.md`

## Hard rules

- if validation output says fail, the orchestrator must not advance state
- state updates must derive from action/result/validation truth, not from freehand prompt summaries

## Verification

Verify:

1. validation can fail even when an artifact file exists
2. state advances only after passing validation
3. both output files are written and parseable
4. output files match the agreed contract fields
