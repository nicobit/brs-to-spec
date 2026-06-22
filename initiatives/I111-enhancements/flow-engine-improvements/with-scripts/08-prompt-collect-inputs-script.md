# Prompt 08 — Implement `collect-inputs`

## Goal

Implement deterministic input resolution and `read_evidence` generation.

This command is the script replacement for the mechanical part of dispatcher Step 10.

## Files to modify

- `.flow-engine/scripts/engine_cli.py`
- `.flow-engine/scripts/brs2spec_engine/inputs.py`
- `.flow-engine/scripts/brs2spec_engine/workspace.py`

## Behavior to implement

The command should accept:

- `--workspace`
- `--event`

Where `--event` is the runtime event YAML path.

### Responsibilities

1. load the runtime event
2. resolve each `read_from` entry against the workspace root
3. distinguish required vs optional using:
   - `required_inputs`
   - `optional_inputs`
4. expand glob patterns
5. produce machine-generated `read_evidence`

## `read_evidence` rules

One entry per `read_from` item:

- for concrete files:
  - `path`
  - `required`
  - `exists`
  - `lines`
  - `bytes`
  - `first_nonempty_line`
  - `read_at`

- for globs:
  - `path`
  - `required`
  - `matched_files`
  - `read_at`

## Failure behavior

- if a required concrete file is missing, fail with structured output
- if a required glob matches nothing, fail with structured output
- optional missing files should not fail the command

## Output

Emit structured JSON containing:

- `ok`
- `required_missing`
- `resolved_inputs`
- `read_evidence`

## Verification

After implementation, verify:

1. every `read_from` item gets exactly one `read_evidence` entry
2. required missing inputs are detected deterministically
3. glob patterns produce `matched_files`
4. `first_nonempty_line` is captured for existing files
