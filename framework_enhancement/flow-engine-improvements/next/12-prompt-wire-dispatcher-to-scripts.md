# Prompt 12 - Wire Dispatcher Prompts to Scripts

## Goal

Update the prompt layer so it calls script commands for deterministic mechanics
and keeps the model focused on content generation and semantic judgment.

## Files to review

At minimum review the main workflow prompts that:

- create initiatives
- dispatch one event
- dispatch multiple events
- restart or resume from a phase
- repair active processing state

## Required changes

Replace prompt-only instructions for:

- runtime event creation
- Step 10 input reads
- queue moves
- integrity checks
- result contract validation
- state updates

with instructions to run the corresponding commands:

- `instantiate-event`
- `collect-inputs`
- `move-event`
- `check-integrity`
- `validate-result`
- `validate-artifact-counts`
- `validate-no-placeholders`
- `update-state`

## Mandatory wiring convention

Do not wire dispatcher steps around stdout-only parsing.

Use fixed output files as required inputs for the next dispatcher boundary.

Examples:

- `collect-inputs` writes `.flow/events/processing/<event_id>-inputs.json`
- `check-integrity` writes `.flow/state/integrity-check.yaml`
- `validate-result` writes `.flow/events/processing/<event_id>-result-check.yaml`
- `validate-artifact-counts` writes `.flow/events/processing/<event_id>-artifact-counts.yaml`
- `validate-no-placeholders` writes `.flow/events/processing/<event_id>-placeholder-check.yaml`
- `update-state` writes `.flow/events/processing/<event_id>-state-update.json`

Note:

- `check-integrity` is intentionally workspace-scoped rather than event-scoped,
  so its output belongs under `.flow/state/` instead of
  `.flow/events/processing/`

Dispatcher instructions should say:

- run the command
- read the required output file
- if the file is missing, malformed, or reports failure, stop or fail the event
- only continue when the output file reports success

Do not phrase this merely as "treat script output as authoritative." Make the
file a gating artifact in the flow.

## Keep prompt-owned behavior

Do not move these into scripts in this step:

- writing business artifacts
- interpreting business intent
- explaining semantic gaps

## Verification

Verify:

1. prompts no longer ask the model to manually copy template fields
2. prompts no longer rely on freehand Step 10 evidence
3. prompts treat script output as authoritative for covered checks
4. prompts gate progression on required output files, not only on command execution
