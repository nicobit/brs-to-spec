# Prompt Placeholder Contract for Workflow-Driven Inputs

## Goal

Define a prompt-facing placeholder contract that is:

- workflow-driven
- generic across workflow types
- independent from hardcoded semantic artifact names
- readable inside prompts
- compatible with wildcard and folder-based input resolution

This contract is intended for `.b2s` prompts and skills.

## Design principles

1. Placeholder names should describe prompt-facing meaning, not engine
   implementation details.
2. Do not expose terms like `matches` in placeholder names.
3. Distinguish between:
   - declared inputs from the workflow contract
   - resolved inputs found on disk by the engine
4. Prompts should mainly use resolved inputs for reading instructions.
5. Python should render placeholders as structured lists, not comma-separated
   strings.

## Final placeholder set

Use these placeholders:

- `{required_inputs}`
- `{optional_inputs}`
- `{resolved_required_inputs}`
- `{resolved_optional_inputs}`
- `{primary_output}`
- `{secondary_outputs}`

## Meaning of each placeholder

### `{required_inputs}`

The declared required input patterns from the workflow action contract.

Examples:

- `input/brs.md`
- `routing/routing-decision.md`
- `input/brs/*.md`

Use case:

- traceability
- diagnostics
- prompt explanation of what the workflow expected

### `{optional_inputs}`

The declared optional input patterns from the workflow action contract.

Use case:

- traceability
- diagnostics
- prompt explanation of which enrichers may exist

### `{resolved_required_inputs}`

The concrete files or directories actually resolved by the engine from the
declared required input patterns.

Use case:

- the main prompt-facing input list to read before writing

### `{resolved_optional_inputs}`

The concrete files or directories actually resolved by the engine from the
declared optional input patterns.

Use case:

- additional prompt-facing input list to read when present

### `{primary_output}`

The primary output path declared by the workflow action.

Use case:

- where the main artifact must be written

### `{secondary_outputs}`

The declared secondary output paths for the action, if any.

Use case:

- additional output targets
- co-produced artifacts

## Rendering rules

## Rule 1 - no comma-separated flattening

Do not render list placeholders as comma-separated strings.

Bad:

```text
input/brs.md, routing/routing-decision.md
```

Good:

```yaml
- input/brs.md
- routing/routing-decision.md
```

## Rule 2 - resolved placeholders must be concrete

`{resolved_required_inputs}` and `{resolved_optional_inputs}` must contain actual
resolved paths, not wildcard expressions.

Bad:

```yaml
- input/brs/*.md
```

Good:

```yaml
- input/brs/context.md
- input/brs/rules.md
```

## Rule 3 - preserve directories when directories are the intended artifact

If the workflow input is a directory artifact, preserve it as a directory path
unless the framework explicitly chooses to expand its contents.

Example:

```yaml
- business-analysis/use-cases/
```

## Rule 4 - stable empty rendering

If no optional inputs resolve, render `{resolved_optional_inputs}` as an empty
list, not as missing text.

Preferred:

```yaml
[]
```

or

```yaml
# none
```

Choose one convention and keep it consistent across the framework.

## Recommended prompt usage

Prompts should prefer the resolved placeholders for actual reading guidance.

Recommended pattern:

```text
Read every path listed in {resolved_required_inputs} fully before writing.
If {resolved_optional_inputs} is not empty, read those paths as well before writing.
Write the main artifact to {primary_output}.
Also produce any paths listed in {secondary_outputs}.
```

## Role of the declared placeholders

Prompts do not need to rely primarily on `{required_inputs}` or
`{optional_inputs}` for artifact reading.

Those declared placeholders are still useful for:

- debugging
- traceability
- validating prompt-to-workflow alignment
- human-readable execution logs

## Recommended Python serialization shape

For prompt interpolation, the easiest safe rendering is:

```yaml
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
  - input/brs/appendix.md

primary_output: business-intake/business-intake-summary.md

secondary_outputs: []
```

This shape is simple, readable, and generic across workflow types.

## Recommended future extension

If the framework later needs richer prompt guidance, do not change these base
placeholder names first.

Instead, extend the value shape behind them while preserving the names.

For example, later evolution could become:

```yaml
resolved_required_inputs:
  - path: input/brs.md
    type: file
  - path: business-analysis/use-cases/
    type: directory
```

But the placeholder name should remain `resolved_required_inputs`.

## Summary

The recommended placeholder contract is:

- `{required_inputs}`
- `{optional_inputs}`
- `{resolved_required_inputs}`
- `{resolved_optional_inputs}`
- `{primary_output}`
- `{secondary_outputs}`

This keeps prompts generic, workflow-driven, and free from hardcoded semantic
artifact names while still giving them concrete paths to read and concrete
targets to write.
