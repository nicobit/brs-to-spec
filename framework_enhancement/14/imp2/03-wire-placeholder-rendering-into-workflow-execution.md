# Prompt 03 - Wire Placeholder Rendering into Workflow Execution

## Context

Once `collect-inputs` exposes prompt-ready placeholders, the workflow execution
path needs a small rendering step so prompt text can consume them.

Before making changes, read these files in full:

- `.b2s/prompts/run-workflow.md`
- `.b2s/scripts/b2s_engine/inputs.py`
- any current helper used to load prompt files during execution

## Goal

Add a lightweight placeholder-rendering mechanism to the workflow execution
path.

## Required work

1. Identify where prompt text is loaded before being used.
2. Add a rendering step that substitutes prompt placeholders using the
   `prompt_placeholders` object from `current-inputs.json`.
3. Fail fast if a referenced placeholder is missing.

## Rules

- Keep the rendering logic small and deterministic
- Do not introduce semantic placeholder expansion beyond the agreed contract
- Render list placeholders as stable multi-line lists, not comma-separated text
- If a placeholder resolves to an empty list, render it consistently

## Minimum supported placeholders

- `{required_inputs}`
- `{optional_inputs}`
- `{resolved_required_inputs}`
- `{resolved_optional_inputs}`
- `{primary_output}`
- `{secondary_outputs}`

## Suggested rendering behavior

- lists render as newline-delimited bullet lists or a stable YAML-like list
- strings render as-is
- empty lists render consistently as `[]` or another chosen stable convention

## Done criteria

- [ ] Prompt loading path applies placeholder rendering
- [ ] Missing placeholder references fail explicitly
- [ ] List rendering is stable and readable
- [ ] No workflow-specific semantic expansion is introduced
