# `.b2s` Retry Action

## Purpose

This prompt reopens a single failed (gate-rejected) action for regeneration
without forcing a full stage reset.

## When To Use

Use this when:

- a human gate was rejected (`reject-current-gate` was run)
- the source action is marked `failed` in `workflow-state.json`
- you want to regenerate only that artifact without rewinding unrelated upstream
  accepted state

Do not use this to bypass a gate that is still `waiting_human`. Use
`approve-current-gate` or `reject-current-gate` first.

## Required Behavior

1. run `retry-action --action-id <action-id>`
2. read `.b2s/tmp/current-state-update.json`
3. verify `overall == pass` and `applied_changes.action_reopened` matches the
   intended action
4. load the skill prompt for the reopened action
5. regenerate the artifact — do not copy or patch the previous version
6. run `validate-artifact`
7. if validation passes, run `update-state`
8. the gate will reopen normally; wait for human approval again

## Rules

- only a `failed` action may be retried — any other status causes a clear error
- retry clears only the failed action and its gate; upstream accepted state is
  preserved
- the retry path still goes through normal validation and gate handling
- do not self-approve the gate after retry

## Output Files

- `.b2s/tmp/current-state-update.json`
- updated `.b2s/state/workflow-state.json`

## Script Authority

The `retry-action` script owns state changes. The prompt does not modify state
by reasoning alone.
