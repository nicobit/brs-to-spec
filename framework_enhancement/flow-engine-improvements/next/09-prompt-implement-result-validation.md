# Prompt 09 - Implement Result Validation

## Goal

Move mechanical validation out of the prompt layer and into scripts.

## Files to modify

- `.flow-engine/scripts/engine_cli.py`
- `.flow-engine/scripts/brs2spec_engine/results.py`

Add any small helper modules only if clearly needed.

## Commands to implement

- `validate-result`
- `validate-artifact-counts`
- `validate-no-placeholders`

## `validate-result` requirements

Check:

- `status` is `pass` or `fail`
- `event_id` exists and matches the expected pattern
- required fields exist
- `artifacts_written` is well-formed
- `read_evidence` exists when the event has `read_from`
- `validation_notes` exists and count matches the event contract
- contradiction cases are flagged

## `validate-artifact-counts` requirements

For intake and requirements-style artifacts:

- enumerate FR IDs in the source artifact
- enumerate FR IDs in the produced artifact
- compare counts and list missing IDs
- do the same for NFR IDs

## `validate-no-placeholders` requirements

- detect `TBD`, `TODO`, `[fill in]`, `PLACEHOLDER`, and similar markers
- report line numbers
- allow intentional gap sections where the rules say placeholders are acceptable

## Output format

Each command should emit machine-readable structured output with:

- command name
- timestamp
- checks
- overall pass/fail or pass/warn/fail status

Preferred fixed paths:

- `.flow/events/processing/<event_id>-result-check.yaml`
- `.flow/events/processing/<event_id>-artifact-counts.yaml`
- `.flow/events/processing/<event_id>-placeholder-check.yaml`

Stdout may be used for summaries only. Dispatcher gating must use the files.

## Verification

Verify:

1. invalid result schema fails
2. missing FR rows fail with explicit missing IDs
3. placeholder lines are reported with line numbers
4. script output can override an LLM-written `pass`
5. missing or failing check files would block dispatcher continuation
