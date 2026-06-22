# Placeholder Contract Example - create-delivery-structure

## Goal

Show how the prompt placeholder contract can be applied to a real existing
`.b2s` action without relying on hardcoded semantic placeholder names.

This example uses the current action `create-delivery-structure`.

## Current action contract source

The existing workflow action declares:

- required inputs
- optional inputs
- primary output

For `create-delivery-structure`, the current workflow-style contract is
conceptually:

```yaml
inputs:
  required:
    - business-analysis/use-cases/
    - architecture/architecture-review.md
    - business-analysis/requirements.md
    - business-intake/business-intake-summary.md
    - routing/routing-decision.md
    - input/brs.md
  optional:
    - input/brs/*.md
    - business-analysis/business-rules.md
    - business-analysis/actors-and-personas.md
outputs:
  primary: planning/delivery-structure.md
  secondary: []
```

## Placeholder values after engine resolution

The engine would resolve the declared inputs and prepare prompt-facing
placeholder values like this:

```yaml
required_inputs:
  - business-analysis/use-cases/
  - architecture/architecture-review.md
  - business-analysis/requirements.md
  - business-intake/business-intake-summary.md
  - routing/routing-decision.md
  - input/brs.md

optional_inputs:
  - input/brs/*.md
  - business-analysis/business-rules.md
  - business-analysis/actors-and-personas.md

resolved_required_inputs:
  - business-analysis/use-cases/
  - architecture/architecture-review.md
  - business-analysis/requirements.md
  - business-intake/business-intake-summary.md
  - routing/routing-decision.md
  - input/brs.md

resolved_optional_inputs:
  - input/brs/appendix.md
  - input/brs/domain-notes.md
  - business-analysis/business-rules.md
  - business-analysis/actors-and-personas.md

primary_output: planning/delivery-structure.md

secondary_outputs: []
```

## Example prompt wording using the placeholders

Below is an example of how the skill prompt could be written using the generic
placeholder contract.

```text
You are following the `.b2s` action `create-delivery-structure`.

Read every path listed in {resolved_required_inputs} fully before writing.
If {resolved_optional_inputs} is not empty, read those paths fully as well before writing.

Use the resolved required and optional inputs to:
- determine delivery mode and execution mode from the routing material
- identify the approved business scope and requirement coverage
- derive epics, features, and story-sized deliverables
- preserve architecture constraints and business-rule impacts where they affect story design

Write the main artifact to {primary_output}.
Also produce any additional outputs listed in {secondary_outputs}.
```

## Why this is better than hardcoded paths

This pattern avoids embedding fixed prompt text such as:

```text
Read {workspace_root}/routing/routing-decision.md
Read {workspace_root}/business-intake/business-intake-summary.md
Read {workspace_root}/business-analysis/requirements.md
```

Advantages:

- the workflow remains the source of truth for inputs
- the prompt stays reusable across workflow types
- wildcard inputs are already resolved by the engine
- the prompt does not depend on one specific folder assumption beyond the action
  contract

## What the prompt still keeps responsibility for

Even with generic placeholders, the prompt still needs to explain how to use the
inputs.

For this action, the skill still needs to say things like:

- derive delivery mode and execution mode from the routing material
- create epics with `E-001`, `E-002`, and so on
- create features with `F-001`, `F-002`, and so on
- create stories with `F-XXX.X`
- include FR coverage and story detail blocks

So the placeholder contract removes hardcoded path coupling, but it does not
remove the need for action-specific generation guidance.

## Practical implementation rule

For an action like `create-delivery-structure`:

- the workflow action definition owns the declared inputs and outputs
- the engine resolves them into the placeholder values
- the prompt uses the placeholder values for reading and writing instructions
- the action-specific skill text explains how to interpret those inputs

## Summary

This example shows the intended split clearly:

- declared workflow contract:
  - `required_inputs`
  - `optional_inputs`
  - `primary_output`
- engine-resolved prompt contract:
  - `resolved_required_inputs`
  - `resolved_optional_inputs`
  - `primary_output`
  - `secondary_outputs`
- skill prompt:
  - explains how to transform those resolved inputs into the correct artifact
