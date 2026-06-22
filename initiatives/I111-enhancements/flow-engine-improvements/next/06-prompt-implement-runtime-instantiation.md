# Prompt 06 - Implement Runtime Instantiation

## Goal

Implement `instantiate-event` so runtime events are always created from an
authoritative template, never hand-built in prompts.

## Files to modify

- `.flow-engine/scripts/engine_cli.py`
- `.flow-engine/scripts/brs2spec_engine/templates.py`
- `.flow-engine/scripts/brs2spec_engine/workspace.py`

## Required behavior

- resolve the active initiative workspace
- load the requested template
- validate that the template exists
- allocate the next `EVT-NNNNN` identifier
- build the runtime event from the template
- preserve all template-driven fields, including:
  - `must_include`
  - `validation_rules`
  - `on_success`
  - `on_failure`
  - `meta.template_id`
- write the event into `.flow/events/pending/`

## Hard rules

- do not let the prompt supply `must_include` content freehand
- do not drop fields that exist in the template
- fail clearly if the workspace or template cannot be resolved

## Verification

Verify:

1. a runtime event file is created in `pending/`
2. `meta.template_id` is present
3. field counts match the source template
4. repeated runs allocate incrementing EVT IDs
