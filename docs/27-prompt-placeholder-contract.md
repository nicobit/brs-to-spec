# Prompt Placeholder Contract

## Purpose

This document defines the workflow-driven prompt placeholder contract for `.b2s`
skills and orchestration prompts.

The goal is to reduce hardcoded path text inside prompts while keeping the
workflow action contract authoritative.

## Supported placeholders

Use these prompt-facing placeholders:

- `{required_inputs}`
- `{optional_inputs}`
- `{resolved_required_inputs}`
- `{resolved_optional_inputs}`
- `{primary_output}`
- `{secondary_outputs}`

## Meaning

### `{required_inputs}`

The declared required input patterns from the selected workflow action.

### `{optional_inputs}`

The declared optional input patterns from the selected workflow action.

### `{resolved_required_inputs}`

The concrete required file or directory paths resolved by the engine from the
declared required input patterns.

### `{resolved_optional_inputs}`

The concrete optional file or directory paths resolved by the engine from the
declared optional input patterns.

### `{primary_output}`

The selected action's declared primary output path.

### `{secondary_outputs}`

The selected action's declared secondary output paths.

## Usage rules

Use the resolved placeholders for actual prompt reading and writing guidance.

Recommended pattern:

```text
Read every path listed in {resolved_required_inputs} fully before writing.
If {resolved_optional_inputs} is not empty, read those paths fully as well before writing.
Write the main artifact to {primary_output}.
Also produce any paths listed in {secondary_outputs}.
```

## Rendering rules

- Do not render list placeholders as comma-separated strings.
- Render list placeholders as stable structured lists.
- Use stable empty-list rendering for empty optional or secondary lists.
- Keep output paths relative to the workspace root, consistent with workflow
  action definitions.

## Diagnostic vs prompt-facing structures

The engine keeps two views of input resolution:

1. Diagnostic view
   Used for debugging and runtime mechanics.
   This may include fields such as:
   - `path`
   - `exists`
   - `matches`

2. Prompt-facing view
   Used for placeholder interpolation in prompts.
   This should expose only the clean placeholder contract, not lower-level
   engine jargon.

The prompt-facing contract should not use names such as `matches`.

## Migration note for older prompts

Older prompts may still contain hardcoded path-reading instructions such as:

```text
Read {workspace_root}/routing/routing-decision.md
Read {workspace_root}/business-intake/business-intake-summary.md
```

These prompts do not need to be rewritten all at once.

Preferred migration path:

1. keep the action-specific guidance
2. replace hardcoded path-reading instructions with resolved placeholders
3. replace hardcoded output-writing instructions with `{primary_output}` and
   `{secondary_outputs}`
4. leave unrelated prompt behavior unchanged

## Authoring guidance

When writing or updating prompts:

- prefer `{resolved_required_inputs}` over repeating specific read paths
- prefer `{resolved_optional_inputs}` over repeating optional path branches
- prefer `{primary_output}` over hardcoding the main output path
- keep action-specific reasoning guidance separate from path wiring

## What not to do

- do not introduce prompt-facing placeholders with `matches` in the name
- do not flatten lists into ambiguous inline text
- do not replace action-specific generation rules with generic placeholder text
- do not assume all workflow types use the same semantic artifact vocabulary

## Summary

The placeholder contract gives prompts a stable workflow-driven interface while
keeping:

- workflow actions as the declared input/output contract
- engine scripts as the input resolver
- prompts as the artifact-generation instructions
