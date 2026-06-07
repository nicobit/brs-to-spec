# Prompt — Select Delivery Mode

## Purpose

Decide which delivery mode should be used for the requested change or BRS.

## Output

```markdown
# Delivery Mode Decision

## Recommended Mode
Fast Path / Standard Path / Enterprise Path / Enterprise + Modular Delivery

## Rationale

## Signals Observed
| Signal | Observed? | Notes |
|---|---|---|
| Small local change |  |  |
| Formal BRS |  |  |
| Multiple stakeholders |  |  |
| Multiple systems |  |  |
| Multiple teams |  |  |
| Compliance/audit impact |  |  |
| Architecture alignment needed |  |  |
| Multi-quarter delivery |  |  |
| Effort > 12-15 person-months |  |  |
| AI context saturation risk |  |  |

## Required Framework Tracks

## Tracks to Skip

## Recommended Next Prompt
```

## Rules

- Do not recommend the full framework for small changes.
- Recommend OpenSpec directly for clear engineering-ready changes.
- Recommend Modular Delivery only for large initiatives.
- Prefer the smallest process that still gives enough control and traceability.
