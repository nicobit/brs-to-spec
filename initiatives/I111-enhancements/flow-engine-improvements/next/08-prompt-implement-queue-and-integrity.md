# Prompt 08 - Implement Queue Moves and Integrity Checks

## Goal

Implement the mechanics that keep queue state trustworthy:

- `move-event`
- `check-integrity`

## Files to modify

- `.flow-engine/scripts/engine_cli.py`
- `.flow-engine/scripts/brs2spec_engine/queue.py`
- `.flow-engine/scripts/brs2spec_engine/results.py`
- `.flow-engine/scripts/brs2spec_engine/state.py`

## Part A - `move-event`

Implement real move semantics for event lifecycle transitions.

Required behavior:

- move event files across queue buckets
- move related result files when appropriate
- reject transitions when the source file does not exist
- reject transitions when the event already exists in multiple buckets

## Part B - `check-integrity`

Implement a pre-dispatch integrity scan.

Required checks:

- result file in `done/` without matching event file in `done/`
- result file in `processing/` without matching event file in `processing/`
- `artifact_status` entries that reference an event not present in `done/`

Required output:

- write workspace-wide integrity results to `.flow/state/integrity-check.yaml`

## Dispatcher intent

This command is intended to run before dispatch continues. If it reports orphan
result files in `done/`, dispatch should stop.

The dispatcher must read `.flow/state/integrity-check.yaml` as a required input.
If the file is missing, malformed, or reports failure, dispatch must stop at
that point.

## Verification

Verify:

1. queue transitions are moves, not file recreation
2. an orphan result file in `done/` is detected
3. an orphan result file in `processing/` is detected
4. the output is structured enough for prompt consumption
5. dispatcher-facing integrity output is written to the fixed path
