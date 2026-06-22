# Prompt 10 — Implement `validate-result`

## Goal

Implement deterministic result-file contract validation.

This command should take over the mechanical part of dispatcher Step 16-G.

## Files to modify

- `.flow-engine/scripts/engine_cli.py`
- `.flow-engine/scripts/brs2spec_engine/results.py`

## Behavior to implement

The command should accept:

- `--workspace`
- `--event`
- `--result`

### Responsibilities

1. load the runtime event
2. load the result file
3. validate:
   - `event_id`
   - `status`
   - `completed_at`
   - `artifacts_written`
   - `validation_notes`
   - `read_evidence`
4. check count rules against the event:
   - `must_include`
   - `validation_rules.natural_language`
   - `read_from`
5. detect contradictions such as:
   - missing `read_evidence`
   - generic emptiness claim on a non-empty file
   - “required input missing” when `read_evidence` shows the file exists

## Output

Emit structured JSON containing:

- `ok`
- `normalized_status`
- `violations`
- `recommended_failure_reason` when invalid

## Verification

After implementation, verify:

1. incomplete `read_evidence` is detected
2. missing natural-language validation entry is detected
3. contradictory failure claims are detected
4. valid result files pass without mutation
