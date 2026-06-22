# Prompt 07 - Implement Input Collection

## Goal

Implement `collect-inputs` so Step 10 input preparation becomes script-owned and
machine-verifiable.

## Files to modify

- `.flow-engine/scripts/engine_cli.py`
- `.flow-engine/scripts/brs2spec_engine/workspace.py`
- `.flow-engine/scripts/brs2spec_engine/inputs.py`

## Required behavior

- read the runtime event file
- resolve every `read_from` entry relative to the initiative workspace
- expand globs deterministically
- classify inputs as required or optional
- record existence, resolved path, and basic metadata for each input
- emit a machine-written input bundle that includes `read_evidence`

## Output expectations

Produce structured output at a fixed required path that the dispatcher can read
back as a gating input.

Preferred output:

- `.flow/events/processing/<event_id>-inputs.json`

Stdout may print a short summary, but stdout is not the dispatcher contract.

## Hard rules

- one evidence entry per `read_from` item
- missing required inputs must fail before persona generation starts
- path resolution must reject paths outside the workspace boundary
- if the output file is not written, the dispatcher must treat the step as failed

## Verification

Verify:

1. `input/brs.md` resolves correctly from a workspace root
2. missing required files are reported mechanically
3. optional missing files are reported but do not fail
4. `read_evidence` count matches the event definition
5. the fixed output file is written and parseable
