# Prompt 12 - Implement Repair, Reset, and Human Gates

## Goal

Add the staged maintenance and gate-handling mechanics required for a usable
`.b2s` framework.

## Files to modify

- `.b2s/scripts/b2s_cli.py`
- `.b2s/scripts/b2s_engine/reset.py`
- `.b2s/scripts/b2s_engine/gates.py`
- `.b2s/prompts/repair-state.md`
- `.b2s/prompts/reset-to-phase.md`
- `.b2s/prompts/resume-from-phase.md`

## Commands to implement

- `repair-state`
- `reset-to-phase`
- `approve-current-gate`
- `reject-current-gate`

## Responsibilities

### `repair-state`

- rescan actual artifact truth
- rebuild staged state from artifacts and gate conditions

### `reset-to-phase`

- back up staged state
- downgrade downstream progress safely
- set next action at the chosen phase boundary

### gate commands

- change current gate status
- unblock or fail the next staged action path
- write `.b2s/tmp/current-gate.json` using the agreed contract

## Required state model

Implement gate behavior using the `workflow-state.json` fields defined in
`04b-state-and-gate-model.md`.

## Verification

Verify:

1. repair is artifact/state reconciliation, not queue repair
2. reset backs up state before rewinding
3. human gates work without WAIT_HUMAN event files
4. gate commands and `next-step` share one consistent gate-state model
