# `.b2s` Agent Instructions

## Purpose

These instructions govern the staged `.b2s` framework.

## Core rules

- `.b2s` is a staged framework, not an event-queue framework.
- Determine work through stage actions and compact state.
- Scripts own deterministic orchestration mechanics.
- Prompts own artifact generation and business judgment.
- Load only the active skill prompt for the selected action.
- Gate progression on script-written output files, not stdout summaries.

## Runtime artifacts

Framework state for each initiative lives under:

```text
initiatives/<id>-<slug>/.b2s/
  state/
  tmp/
```

## Initial execution model

The first implementation supports exactly one active action at a time.

## Prompt loading rule

Do not load unrelated prompts or personas during execution.

## Prompt placeholder rule

When a skill prompt uses workflow-driven placeholders, prefer the engine-resolved
prompt placeholder contract over hardcoded path text.

Supported prompt-facing placeholders include:

- `{required_inputs}`
- `{optional_inputs}`
- `{resolved_required_inputs}`
- `{resolved_optional_inputs}`
- `{primary_output}`
- `{secondary_outputs}`

Use resolved placeholders for actual read and write instructions. Do not expose
engine-internal terms like `matches` in prompt-facing placeholder names.

## State rule

`workflow-state.json` is the source of staged orchestration truth, but only
after `state_validated` is true.

## Orchestrator rule

`run-workflow.md` defines the staged execution loop. Follow that loop exactly
and stop whenever a required engine output file is missing or reports failure.

## Gate rule

When `awaiting_human` is true, do not continue artifact generation. The only
valid next operations are gate approval, gate rejection, repair, or reset.
