# Prompt 01 - Introduce Action Contract v2

## Context

You are enhancing the `.b2s` engine in an additive way. The goal is to make
each action definition closer to:

```text
inputs -> policies -> prompt -> template -> artifact -> validation -> gate
```

The current action contract already includes inputs, outputs, validation
profiles, conditions, and human gates. This prompt adds richer metadata without
breaking current actions.

## Step 1 - Inspect the current schema usage

Read these files in full:

- `.b2s/workflow/stage-actions.yaml`
- `.b2s/scripts/b2s_engine/inputs.py`
- `.b2s/scripts/b2s_engine/validation.py`
- `.b2s/scripts/b2s_engine/dispatch.py`
- `.b2s/scripts/b2s_engine/state.py`

Identify every place where an action record is read directly.

## Step 2 - Define a backward-compatible v2 contract

Extend the action shape in `.b2s/workflow/stage-actions.yaml` support code so an
action may optionally declare:

```yaml
prompt_family: b2s
policy_refs:
  - ".b2s/policies/business/business-writing-guidelines.md"
validation_rules:
  required: []
  optional: []
template_mode: strict
compatibility:
  fallback_skill_ref: ".b2s/skills/product-owner/create-requirements.md"
```

Rules:

- all new fields must be optional
- missing new fields must preserve existing behavior
- `skill_ref` remains supported exactly as today
- `prompt_family` defaults to `b2s`
- `template_mode` defaults to `strict`

## Step 3 - Create a schema helper module

Create a small helper in `.b2s/scripts/b2s_engine/` that normalizes action
records into a canonical in-memory shape. Use this helper everywhere instead of
scattered dictionary access.

The helper should:

- populate defaults for new fields
- preserve current fields unchanged
- make old actions behave as valid v2 actions

## Step 4 - Update the workflow registry documentation

Update `.b2s/module-index.md` or another appropriate framework doc to explain
the new action fields and their purpose.

Keep the explanation brief and implementation-oriented.

## Step 5 - Seed one or two representative actions

Update a small number of existing actions in `.b2s/workflow/stage-actions.yaml`
to demonstrate the new fields without mass-editing the whole registry.

Good candidates:

- `create-business-intake-summary`
- `create-requirements`
- `review-initial-architecture`

For those actions, add realistic `policy_refs`, `prompt_family`, and
`validation_rules.required` examples.

## Step 6 - Verify

Run the relevant tests. If no targeted tests exist, add them later in Prompt 08.

## Done criteria

- [ ] actions support new optional metadata fields
- [ ] old action definitions still work unchanged
- [ ] action normalization is centralized in code
- [ ] at least two real actions demonstrate the new contract
