# Proposed Command Surface

## Goal

Provide a small script surface that prompts can call explicitly.
Prompts stop describing low-level mechanics in prose and instead invoke commands.

## Priority 1 commands

### `instantiate-event`

Purpose:

- create a runtime event from a template

Inputs:

- workspace root
- template ID
- stage
- reason / note

Outputs:

- written runtime event path
- assigned `event_id`
- copied field counts (`must_include`, `validation_rules`)

Hard guarantees:

- `meta.template_id` always set
- `must_include` preserved
- `validation_rules` preserved
- `on_success` / `on_failure` preserved

### `collect-inputs`

Purpose:

- resolve and read every `read_from` item for an event

Inputs:

- workspace root
- runtime event path

Outputs:

- resolved input set
- `read_evidence` JSON payload
- explicit missing/optional input classification

Hard guarantees:

- one `read_evidence` entry per `read_from` item
- required input failures are machine-detected before persona work starts

### `move-event`

Purpose:

- perform queue transitions as real filesystem moves

Inputs:

- workspace root
- event ID
- source bucket
- target bucket

Outputs:

- final event path
- final result path if applicable

Hard guarantees:

- event exists in exactly one bucket after move
- no silent copy/recreate semantics

## Priority 2 commands

### `validate-result`

Purpose:

- validate the result file contract before Step 17/18 behavior continues

Checks:

- required fields
- `validation_notes` count
- `read_evidence` count
- contradiction checks
- natural-language validation entry presence

### `update-state`

Purpose:

- update `workflow-state.json`, `event-log.jsonl`, and `open-decisions.md`

Hard guarantees:

- event log appended once
- failed/pass state transitions consistent
- active/failed/completed event fields aligned

### `repair-processing`

Purpose:

- recover stale `processing/` contents deterministically

### `repair-chain`

Purpose:

- instantiate missing downstream events from the authoritative template chain

### `reset-to-phase`

Purpose:

- back up active state and rebuild the queue at a chosen phase

## Prompt integration model

Prompts should evolve from:

- “read this file now”
- “move that event”
- “copy fields from template”

to:

- “run `collect-inputs` for this event and use the returned evidence”
- “run `instantiate-event` for EVT-TPL-002”
- “run `validate-result` before finalizing”

This keeps prompts high-level and shifts deterministic work into scripts.
