# Prompt 01 - Add Prompt Placeholders to collect-inputs

## Context

You are implementing workflow-driven prompt placeholders for `.b2s`.

Before making changes, read these files in full:

- `.b2s/scripts/b2s_engine/inputs.py`
- `.b2s/scripts/b2s_engine/workspace.py`
- `framework_enhancement/14/imp2/prompt-placeholder-contract.md`
- `framework_enhancement/14/imp2/recommended-engine-changes-for-placeholder-support.md`

## Goal

Extend `collect-inputs` so it produces a prompt-facing placeholder contract in
addition to the current diagnostic structure.

## Required work

In `.b2s/scripts/b2s_engine/inputs.py`:

1. Keep the current `required_inputs` and `optional_inputs` diagnostic entries.
2. Build a new `prompt_placeholders` object in the output payload.
3. Populate these keys:
   - `required_inputs`
   - `optional_inputs`
   - `resolved_required_inputs`
   - `resolved_optional_inputs`
4. Use the declared input patterns for:
   - `required_inputs`
   - `optional_inputs`
5. Use the flattened concrete resolved paths for:
   - `resolved_required_inputs`
   - `resolved_optional_inputs`

## Rendering rules

- `required_inputs` and `optional_inputs` must be simple declared pattern lists
- `resolved_required_inputs` and `resolved_optional_inputs` must be flattened
  lists of concrete resolved paths
- do not expose nested `matches` arrays in the prompt-facing section
- do not remove the current diagnostic structure

## Example target shape

```yaml
prompt_placeholders:
  required_inputs:
    - input/brs.md
    - routing/routing-decision.md
  optional_inputs:
    - input/brs/*.md
    - input/architecture.md
  resolved_required_inputs:
    - input/brs.md
    - routing/routing-decision.md
  resolved_optional_inputs:
    - input/brs/context.md
    - input/architecture.md
```

## Done criteria

- [ ] `collect-inputs` output keeps the existing diagnostic structure
- [ ] `collect-inputs` output adds `prompt_placeholders`
- [ ] Declared placeholders and resolved placeholders are both populated
- [ ] Resolved placeholders are flattened concrete path lists
