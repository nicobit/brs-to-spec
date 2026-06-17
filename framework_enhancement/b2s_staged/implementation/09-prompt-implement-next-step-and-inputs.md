# Prompt 09 - Implement `next-step` and `collect-inputs`

## Goal

Implement the first two critical `.b2s` script commands:

- `next-step`
- `collect-inputs`

## Files to modify

- `.b2s/scripts/b2s_cli.py`
- `.b2s/scripts/b2s_engine/workspace.py`
- `.b2s/scripts/b2s_engine/next_step.py`
- `.b2s/scripts/b2s_engine/inputs.py`

## `next-step` responsibilities

- read staged workflow state
- inspect action prerequisites
- inspect artifact statuses and conditions
- choose the next executable action
- write `.b2s/state/next-step.json`
- follow the `next-step.json` contract from `04a-output-file-contracts.md`

## `collect-inputs` responsibilities

- read the selected action definition
- resolve required and optional inputs
- expand globs where the action definition allows them
- write `.b2s/tmp/current-inputs.json`
- follow the `current-inputs.json` contract from `04a-output-file-contracts.md`

## Hard rules

- output files are required, not optional
- if `next-step.json` or `current-inputs.json` is missing, the orchestrator must stop
- path resolution must stay inside the initiative workspace

## Verification

Verify:

1. next step selection works for the first thin-slice stages
2. required inputs are resolved mechanically
3. missing required inputs fail clearly
4. both output files are written and parseable
5. both output files match the agreed contract fields
