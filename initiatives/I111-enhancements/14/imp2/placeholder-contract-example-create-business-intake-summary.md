# Placeholder Contract Example - create-business-intake-summary

## Goal

Show how the placeholder contract works for an action where the workflow
declares both fixed inputs and wildcard-based supporting inputs.

This example uses the current action `create-business-intake-summary`.

## Current action contract source

The existing workflow-style contract is conceptually:

```yaml
inputs:
  required:
    - input/brs.md
    - routing/routing-decision.md
  optional:
    - input/brs/*.md
    - input/architecture.md
    - input/input-package.md
outputs:
  primary: business-intake/business-intake-summary.md
  secondary: []
```

## Why this example is useful

This action is a good placeholder example because:

- it has fixed required file inputs
- it has wildcard optional inputs
- it can enrich from several optional context files
- it still has a single clear primary output

## Placeholder values after engine resolution

The engine would prepare prompt-facing values like this:

```yaml
required_inputs:
  - input/brs.md
  - routing/routing-decision.md

optional_inputs:
  - input/brs/*.md
  - input/architecture.md
  - input/input-package.md

resolved_required_inputs:
  - input/brs.md
  - routing/routing-decision.md

resolved_optional_inputs:
  - input/brs/appendix-a.md
  - input/brs/glossary.md
  - input/architecture.md

primary_output: business-intake/business-intake-summary.md

secondary_outputs: []
```

## Example prompt wording using the placeholders

```text
You are following the `.b2s` action `create-business-intake-summary`.

Read every path listed in {resolved_required_inputs} fully before writing.
If {resolved_optional_inputs} is not empty, read those paths fully as well before writing.

Use the resolved required and optional inputs to:
- normalize the business content from the BRS
- preserve source conflicts instead of silently merging them
- extract objectives, scope, requirements, capabilities, risks, and open questions
- use the routing material to shape the expected depth and delivery framing

Write the artifact to {primary_output}.
Also produce any additional outputs listed in {secondary_outputs}.
```

## What this solves

Without placeholder resolution, a prompt usually has to hardcode things like:

```text
Read all available input files from {workspace_root}/input/
plus {workspace_root}/routing/routing-decision.md.
If supporting files such as {workspace_root}/input/architecture.md
or {workspace_root}/input/input-package.md exist, use them as context.
```

That works, but it makes the prompt depend directly on:

- concrete path conventions
- folder assumptions
- implicit wildcard behavior

With the placeholder contract, the engine already resolves those paths and the
prompt simply consumes:

- `{resolved_required_inputs}`
- `{resolved_optional_inputs}`
- `{primary_output}`

## Why wildcard resolution matters here

The declared optional input:

```text
input/brs/*.md
```

is not directly readable as one file.

What the prompt actually needs is the resolved list, such as:

- `input/brs/appendix-a.md`
- `input/brs/glossary.md`

This is exactly why `resolved_optional_inputs` is useful.

## What remains action-specific

The placeholder contract does not remove the need for action-specific
instructions.

For `create-business-intake-summary`, the skill still needs to explain:

- assign canonical IDs
- keep business sections as real tables
- separate resolved and unresolved questions correctly
- preserve contradictions instead of smoothing them away
- stop if the BRS is empty or insufficient

So the placeholder contract handles path injection, while the skill still
handles artifact-specific behavior.

## Summary

This example demonstrates the ideal use of the contract for wildcard-heavy
inputs:

- workflow declares the patterns
- engine resolves concrete file paths
- prompt reads the resolved paths
- prompt stays generic and does not hardcode the input folder structure
