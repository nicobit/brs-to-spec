# Prompt 10 - Implement State Updates

## Goal

Implement `update-state` so workflow state derives from authoritative queue and
result facts rather than ad hoc prompt reconstruction.

## Files to modify

- `.flow-engine/scripts/engine_cli.py`
- `.flow-engine/scripts/brs2spec_engine/state.py`
- `.flow-engine/scripts/brs2spec_engine/results.py`

## Required behavior

- read the validated event and result inputs
- update `workflow-state.json`
- append to `event-log.jsonl`
- update `open-decisions.md` when the result requires it
- keep active, completed, and failed event references aligned
- write a machine-readable state-update output file summarizing the applied plan

Preferred output:

- `.flow/events/processing/<event_id>-state-update.json`

## Hard rules

- append the event log once per event outcome
- do not advance stage from an invalid or failed state transition
- do not trust freehand prompt summaries over event/result data

## Verification

Verify:

1. successful events update the expected state fields
2. failed events are reflected consistently
3. event-log entries are not duplicated
4. state remains aligned with queue and result facts
5. the state-update output file is written and parseable
