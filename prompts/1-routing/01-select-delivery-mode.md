# Prompt — Select Delivery Mode

## Purpose

Decide which delivery mode should be used.

## Inputs

Use:
- `input/brs.md` if available,
- `input/initial-architecture.md` if available,
- `input/input-package.md` if available,
- known business context.

## Output file

```text
routing/delivery-mode-decision.md
```

## Output

```markdown
# Delivery Mode Decision

## Recommended Mode
Fast Path / Standard Path / Enterprise Path / Enterprise + Modular Delivery

## Rationale

## Signals Observed

| Signal | Observed? | Notes |
|---|---|---|
| Clear engineering-ready request |  |  |
| Formal BRS |  |  |
| Initial architecture document provided |  |  |
| Multiple stakeholders |  |  |
| Multiple systems |  |  |
| Multiple teams |  |  |
| Compliance/audit impact |  |  |
| Architecture alignment needed |  |  |
| Multi-quarter delivery |  |  |
| Effort > 12-15 person-months |  |  |
| AI context saturation risk |  |  |

## Tracks to Use

## Tracks to Skip

## Recommended Next Prompt
```

## Rules

- Do not recommend the full framework for small changes.
- Recommend OpenSpec directly for clear engineering-ready changes.
- Recommend Modular Delivery only for large initiatives.
- If initial architecture is present, recommend architecture review for Enterprise paths.
