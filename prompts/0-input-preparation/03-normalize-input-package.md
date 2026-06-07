# Prompt - Normalize Input Package

## Purpose

Create a concise index of all normalized inputs for the current feature workspace and explain how single-file or multi-file inputs should be interpreted together.

## Inputs

Use the following inputs when available:

- `input/brs.md or input/brs/*.md`
- `input/architecture.md or input/architecture/*.md`

## Output

```text
input/input-package.md
```

## Template

Use:

```text
templates/input-preparation/input-package.md
```

Preserve the template headings and fill every section that can be supported by evidence.

## Rules

- Do not perform full analysis.
- Inventory every available BRS and architecture source.
- Identify missing inputs early.
- State confidence and limitations.
- If source files disagree, document the conflict instead of silently resolving it.
