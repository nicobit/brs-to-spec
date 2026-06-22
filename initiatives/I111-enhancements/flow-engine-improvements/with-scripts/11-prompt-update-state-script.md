# Prompt 11 — Implement `update-state`

## Goal

Implement deterministic updates for:

- `workflow-state.json`
- `event-log.jsonl`
- `open-decisions.md`

This command takes over the mechanical part of dispatcher Steps 18–19.

## Files to modify

- `.flow-engine/scripts/engine_cli.py`
- `.flow-engine/scripts/brs2spec_engine/state.py`

## Behavior to implement

The command should accept:

- `--workspace`
- `--event`
- `--result`

### Responsibilities

1. update artifact status from the event/result outcome
2. update:
   - `last_completed_event`
   - `failed_events`
   - `active_events`
   - `event_counter` when relevant
3. append one event-log line only once
4. insert open decisions from `open_decisions_raised`
5. recalculate:
   - `open_decisions`
   - `blocking_decisions`

## Hard guarantees

- state and event log must not contradict each other after execution
- duplicate event-log writes must fail
- pass/fail must be reflected consistently in state

## Output

Emit structured JSON containing:

- `ok`
- `updated_files`
- `state_changes`
- `decisions_added`

## Verification

After implementation, verify:

1. failed events leave `active_events`
2. pass events set artifact status correctly
3. event-log duplication is blocked
4. decision counts match `open-decisions.md`
