# `.b2s` Rerun Last Action

## Purpose

This prompt re-executes the last completed action, discarding its artifact and
regenerating it from scratch — without requiring a gate rejection and without
resetting the entire stage.

## When To Use

Use this when:

- the last completed action produced a poor-quality or placeholder artifact
- the action status is `ai_validated` or `waiting_human` (gate pending)
- you want to regenerate only that artifact without rewinding unrelated upstream
  accepted state

Do not use this when:

- the action status is `accepted` (human-approved) — use `reject-current-gate`
  then `retry-action` instead
- you want to rewind multiple actions — use `reset-to-phase` instead

## Required Behavior

1. run `rerun-last-action`
2. read `.b2s/tmp/rerun-last-action.json` (or `current-state-update.json`)
3. verify `overall == pass` and `applied_changes.action_reopened` is correct
4. continue from step 7 of `run-workflow.md` (`collect-inputs`) — the action
   is already selected in state; do not re-run `next-step`
5. regenerate the artifact — do not copy or patch the previous version
6. run `validate-artifact`
7. if validation passes, run `update-state`
8. if a gate reopens, stop and wait for human approval

## Rules

- only `ai_validated` or gate-pending actions may be rerun — `accepted` causes
  a clear error
- rerun clears only the last action and its gate; all upstream accepted state
  is preserved
- the rerun path goes through normal validation and gate handling
- do not self-approve the gate after rerun

## Output Files

- `.b2s/tmp/rerun-last-action.json`
- updated `.b2s/state/workflow-state.json`

## Script Authority

The `rerun-last-action` script owns state changes. The prompt does not modify
state by reasoning alone.
