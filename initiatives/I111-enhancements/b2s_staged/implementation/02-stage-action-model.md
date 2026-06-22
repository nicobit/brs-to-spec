# Stage Action Model

## Core idea

`.b2s` should replace runtime events with **stage actions**.

A stage action is the executable unit of staged work.

## Suggested action fields

Each action in `.b2s/workflow/stage-actions.yaml` should define:

- `action_id`
- `stage_id`
- `title`
- `persona`
- `skill_ref`
- `artifact_template_ref`
- `inputs.required`
- `inputs.optional`
- `outputs.primary`
- `outputs.secondary`
- `must_include`
- `validation_rules`
- `blocked_by_stage`
- `blocked_by_action`
- `conditions`
- `human_gate`
- `selection_mode`
- `status_model`
- `on_pass.update_state`
- `on_fail.raise_decision`

## Required action schema

The action model should be formal, not inferred ad hoc.

Recommended minimum schema:

```yaml
action_id: create-business-intake-summary
stage_id: 2-business-intake
title: Create business intake summary
persona: product-owner
skill_ref: .b2s/skills/product-owner/create-business-intake-summary.md
artifact_template_ref: .b2s/artifact-templates/business-intake-summary.md
inputs:
  required:
    - input/brs.md
  optional:
    - input/architecture.md
outputs:
  primary: business-intake/business-intake-summary.md
  secondary: []
must_include: []
validation_rules: {}
blocked_by_stage: []
blocked_by_action: []
conditions: []
human_gate:
  required: false
selection_mode: serial
status_model:
  artifact_on_pass: ai_validated
  artifact_on_gate_accept: accepted
  artifact_on_fail: failed
on_pass:
  update_state: {}
on_fail:
  raise_decision: null
```

## Action lifecycle

Every action should move through a staged lifecycle, even without event files:

- `eligible`
- `selected`
- `running`
- `waiting_validation`
- `waiting_human`
- `completed`
- `failed`

This lifecycle should be represented in `workflow-state.json` and in script
output files rather than in queue buckets.

## Mapping from `.brs2spec2`

Use `.brs2spec2` event templates as the source for these fields, but do not
carry over:

- `event_id`
- queue bucket behavior
- runtime event files
- result files

## Example

Conceptually:

```yaml
action_id: create-business-intake-summary
stage_id: 2-business-intake
persona: product-owner
skill_ref: .b2s/skills/product-owner/create-business-intake-summary.md
artifact_template_ref: .b2s/artifact-templates/business-intake-summary.md
inputs:
  required:
    - input/brs.md
    - routing/routing-decision.md
  optional:
    - input/architecture.md
outputs:
  primary: business-intake/business-intake-summary.md
must_include:
  ...
validation_rules:
  ...
blocked_by_stage:
  - 0-routing
```

## Why this matters

This preserves the stronger `.brs2spec2` artifact contract without bringing the
event queue back into the staged design.

## Serial execution rule

For the first `.b2s` implementation, support only one active action at a time.

Even if multiple actions are logically ready in a stage, `next-step` should
select exactly one action. Parallel staged execution can be added later only
after the single-action model is proven.
