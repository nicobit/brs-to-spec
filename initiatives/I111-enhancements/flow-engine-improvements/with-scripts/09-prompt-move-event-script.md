# Prompt 09 — Implement `move-event`

## Goal

Implement deterministic queue transitions as real filesystem moves.

This command addresses the observed bug where queue files appear copied or recreated
instead of cleanly moved between buckets.

## Files to modify

- `.flow-engine/scripts/engine_cli.py`
- `.flow-engine/scripts/brs2spec_engine/queue.py`
- `.flow-engine/scripts/brs2spec_engine/workspace.py`

## Behavior to implement

The command should accept:

- `--workspace`
- `--event-id`
- `--from`
- `--to`

Supported buckets:

- `pending`
- `processing`
- `done`
- `failed`

### Responsibilities

1. locate the event file by EVT-ID in the source bucket
2. move the event file to the target bucket
3. optionally move the paired result file if one exists and the caller requests it
4. verify the event no longer exists in the source bucket after the move

## Hard guarantees

After the move:

- the event file exists in exactly one bucket
- no copy should remain in the source bucket
- the script must fail if both source and target copies still exist

## Output

Emit structured JSON containing:

- `event_id`
- `source_path`
- `target_path`
- `result_path` if moved

## Verification

After implementation, verify:

1. moving an event leaves exactly one live event file
2. moving a missing event returns a clear failure
3. the script does not rewrite event contents during move
