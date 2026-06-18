# Recommended Engine Changes for Placeholder Support

## Goal

Describe the minimum engine-side changes needed to support the prompt
placeholder contract defined in this folder.

This note does not propose changing prompt-generation behavior beyond what is
needed to expose workflow-resolved values safely.

## Placeholder contract to support

The engine should support these prompt-facing placeholders:

- `{required_inputs}`
- `{optional_inputs}`
- `{resolved_required_inputs}`
- `{resolved_optional_inputs}`
- `{primary_output}`
- `{secondary_outputs}`

## Current engine behavior

Today the engine already:

- reads the selected action from workflow state
- reads declared input patterns from `stage-actions.yaml`
- resolves those input patterns into concrete paths
- writes machine-readable input metadata to
  `.b2s/tmp/current-inputs.json`

That means the framework already has most of the information needed.

## Recommended minimum change

Extend the collected input result so it can serve both:

- engine/runtime diagnostics
- prompt placeholder interpolation

without requiring prompts to reconstruct anything from raw workflow files.

## Recommended output shape

The machine-written input file should expose a prompt-ready section such as:

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
    - input/brs/appendix-a.md
    - input/architecture.md
  primary_output: business-intake/business-intake-summary.md
  secondary_outputs: []
```

## Why a dedicated prompt_placeholders section is useful

It avoids forcing prompts or orchestration logic to derive prompt-facing values
from lower-level diagnostic structures like:

- `{ path, exists, matches }`

The diagnostic structure can stay for debugging, while prompt interpolation uses
the clean, stable section.

## Keep diagnostic and prompt views separate

Recommended split:

### Diagnostic view

Keep or preserve something close to the current structure:

```yaml
required_inputs:
  - path: input/brs.md
    exists: true
    matches:
      - input/brs.md
```

### Prompt view

Expose the simplified placeholder-ready view:

```yaml
prompt_placeholders:
  resolved_required_inputs:
    - input/brs.md
```

This keeps implementation detail out of prompts.

## Recommended engine responsibilities

The engine should:

1. Read declared `required` and `optional` input patterns from the selected
   action.
2. Resolve each pattern to concrete file or directory paths.
3. Flatten all resolved required paths into `resolved_required_inputs`.
4. Flatten all resolved optional paths into `resolved_optional_inputs`.
5. Read the action outputs and expose:
   - `primary_output`
   - `secondary_outputs`
6. Write all of the above into the prompt placeholder section.

## Flattening rules

### Required and optional declared inputs

These should remain simple declared lists:

```yaml
required_inputs:
  - input/brs.md
  - routing/routing-decision.md
```

### Resolved inputs

These should be flattened lists of actual paths:

```yaml
resolved_optional_inputs:
  - input/brs/appendix-a.md
  - input/brs/glossary.md
  - input/architecture.md
```

Do not preserve nested `matches` arrays in the prompt-facing section.

## Empty-value rules

Use stable empty values:

- `required_inputs`: `[]` only if truly none are declared
- `optional_inputs`: `[]` if none are declared
- `resolved_required_inputs`: `[]` only if the action contract allows that
- `resolved_optional_inputs`: `[]` when no optional input resolves
- `secondary_outputs`: `[]` when none exist

Do not omit keys entirely in the prompt placeholder section.

## Output placeholders

The engine should derive output placeholders from the selected action directly:

```yaml
primary_output: planning/delivery-structure.md
secondary_outputs:
  - business-analysis/use-cases.md
```

This ensures prompt output instructions stay aligned with the workflow action.

## Interpolation model

The orchestrator or prompt runner should load `prompt_placeholders` and replace
placeholders directly in the selected prompt text before execution context is
assembled.

Recommended behavior:

- if a placeholder is missing, fail fast
- if a placeholder resolves to an empty list, render it explicitly as `[]` or a
  consistent empty-list representation
- do not silently substitute null or blank text

## Suggested near-term implementation path

1. Keep the existing `current-inputs.json` structure intact.
2. Add a new `prompt_placeholders` object to it.
3. Populate it during `collect-inputs`.
4. Keep prompt changes incremental:
   - first update a few prompts to use the new placeholders
   - then expand gradually across skills

This minimizes migration risk.

## Benefits

If implemented this way, the framework gains:

- less hardcoded path text in prompts
- less drift between workflow contract and skill text
- better support for multiple workflow types
- cleaner support for wildcard and folder inputs
- a stable, generic prompt contract

## Summary

The minimum safe engine change is:

- keep the current diagnostic input resolution
- add a clean `prompt_placeholders` section
- expose:
  - `required_inputs`
  - `optional_inputs`
  - `resolved_required_inputs`
  - `resolved_optional_inputs`
  - `primary_output`
  - `secondary_outputs`

This is enough to support prompt placeholder interpolation without changing the
fundamental staged engine model.
