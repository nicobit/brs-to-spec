# `.b2s` Repair State

## Purpose

This prompt repairs staged state by reconciling `workflow-state.json` with the
actual artifacts that exist in the initiative workspace.

## When To Use

Use this when:

- artifact files exist but staged state is stale or inconsistent
- a previous run was interrupted
- gate state no longer matches the actual artifact and progression state

If a gate was rejected and you want to regenerate only the rejected artifact
without a full stage rewind, use `retry-action` instead — see
`.b2s/prompts/retry-action.md`.

## Required Behavior

1. run `repair-state`
2. let the script rescan artifact truth
3. let the script rebuild compact state fields it can determine mechanically
4. read `.b2s/tmp/current-state-update.json`
5. if the repair still leaves a blocker, stop and surface it

## Rules

- repair is artifact/state reconciliation, not queue repair
- do not invent progress for artifacts that do not exist
- preserve human gate truth where it still exists
- do not silently clear a real blocker just to make the workflow move again

## Output Files

- `.b2s/tmp/current-state-update.json`
- updated `.b2s/state/workflow-state.json`

## Script Authority

The `repair-state` script owns the repaired state. The prompt does not repair
state by reasoning alone.
