# Prompt — Normalize Input Package

## Purpose

Create an input package that records the official source inputs for the framework.

## Inputs

Use:
- `input/brs.md`
- `input/initial-architecture.md`

## Output file

```text
input/input-package.md
```

## Output structure

```markdown
# Input Package

## Source Documents

| Type | File | Version | Date | Owner | Notes |
|---|---|---|---|---|---|
| BRS | input/brs.md |  |  |  |  |
| Initial Architecture | input/initial-architecture.md |  |  |  |  |

## Input Completeness

| Area | Available? | Notes |
|---|---|---|
| BRS |  |  |
| Initial architecture |  |  |
| Business objectives |  |  |
| Requirements |  |  |
| NFRs |  |  |
| Architecture constraints |  |  |
| Integration constraints |  |  |
| Security constraints |  |  |

## Known Limitations

## Assumptions

## Recommended Next Step
```

## Rules

- Do not analyze the whole delivery yet.
- Focus on input readiness.
- Mark missing architecture as a risk for later architecture review.
