# Prompt 16 - Add Single-Action Retry After Gate Rejection

## Goal

Allow a rejected staged artifact to be retried directly, without forcing a full
stage reset.

## Files to modify

- `.b2s/scripts/b2s_cli.py`
- `.b2s/scripts/b2s_engine/gates.py`
- `.b2s/scripts/b2s_engine/state.py`
- `.b2s/scripts/b2s_engine/workspace.py`
- `.b2s/prompts/repair-state.md`
- `.b2s/prompts/resume-from-phase.md`
- optionally add `.b2s/prompts/retry-action.md`
- `.b2s/tests/test_engine_maintenance.py`
- `.b2s/tests/test_engine_fixtures.py`

## Required work

Implement a deterministic retry path for a rejected action.

### Required command shape

Implement this as a first-class CLI command:

- `retry-action --action-id <id>`

Do not hide the retry behavior inside a generic repair path only.

Add a machine-readable output file contract for retry behavior by reusing:

- `.b2s/tmp/current-state-update.json`

and ensure `workspace.py` contains the default output-path mapping for the new
command.

### Behavior

When `reject-current-gate` is used:

- preserve valid upstream accepted actions
- preserve valid upstream accepted artifacts
- record which source action must be retried
- do not force a full stage rewind

Add a retry mechanism, for example:

- `retry-action --action-id <id>`

Preferred behavior:

- clear the failed status for the rejected source action
- clear or downgrade only the source action outputs
- clear the blocker that came from that rejection
- set `next_action` back to the source action
- leave unrelated accepted upstream state intact

State-update output should include at least:

- `overall`
- `action_id`
- `previous_state_summary`
- `applied_changes`
- `next_action`
- `gate_state`

`applied_changes` should make it explicit that the action was reopened for
retry.

## Constraints

- do not silently rewrite unrelated stages
- do not require resetting to `0-routing` or restarting the whole stage
- the retry path must still go back through normal staged validation and state
  update
- if the requested action is not the last gate-rejected source action, fail
  clearly rather than reopening arbitrary workflow history

## Verification

Verify:

1. rejecting business-intake review blocks progress
2. retrying the source action reopens only that action
3. routing remains accepted
4. next-step selects the retried source action
5. the action still must pass validation and gate handling normally afterward
6. the retry command writes the expected machine-readable state-update output
