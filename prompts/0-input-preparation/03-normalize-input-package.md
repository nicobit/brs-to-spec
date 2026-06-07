# Prompt — Normalize Input Package

## Purpose

Create a concise index of all normalized inputs and their completeness.

## Inputs

Use the following inputs when available:

- `input/brs.md`
- `input/initial-architecture.md`

## Output

```text
input/input-package.md
```

## Required output structure

```markdown
# Input Package

## Input Inventory

| Artifact | Available? | Version/date | Completeness | Notes |
|---|---|---|---|---|

## Known Limitations

## Missing Inputs

## Assumptions

## Recommended Next Step
```

## Rules

- Do not perform full analysis.
- Identify missing inputs early.
- State confidence and limitations.
