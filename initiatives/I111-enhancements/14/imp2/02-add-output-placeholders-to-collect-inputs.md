# Prompt 02 - Add Output Placeholders to collect-inputs

## Context

The prompt-facing contract must include both inputs and outputs, so prompts can
read and write without hardcoded path text.

Before making changes, read these files in full:

- `.b2s/scripts/b2s_engine/inputs.py`
- `.b2s/scripts/b2s_engine/workspace.py`
- `.b2s/workflow/stage-actions.yaml`

## Goal

Extend the prompt placeholder payload so it also includes output targets.

## Required work

In `.b2s/scripts/b2s_engine/inputs.py`:

1. Read the selected action's output contract.
2. Add these keys under `prompt_placeholders`:
   - `primary_output`
   - `secondary_outputs`
3. Set:
   - `primary_output` to the declared primary output path
   - `secondary_outputs` to the declared secondary output list

## Rules

- `primary_output` must always be present when the action defines a primary output
- `secondary_outputs` must always exist as a list, even when empty
- keep output paths relative to the workspace root, consistent with the current
  framework conventions

## Example target shape

```yaml
prompt_placeholders:
  primary_output: planning/delivery-structure.md
  secondary_outputs: []
```

## Done criteria

- [ ] `prompt_placeholders.primary_output` is populated from the action output contract
- [ ] `prompt_placeholders.secondary_outputs` is populated consistently
- [ ] Output placeholder values remain relative workspace paths
