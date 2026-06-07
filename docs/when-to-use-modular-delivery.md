# When to Use Modular Delivery

Use Modular Delivery only for large initiatives. It is not the default path for every change.

## Use Modular Delivery when

| Signal | Meaning |
|---|---|
| Effort > 12-15 person-months | Too large for a flat feature list |
| Delivery spans more than one quarter | Needs vertical increments |
| Multiple systems involved | Needs module boundaries |
| Multiple teams involved | Needs ownership separation |
| High AI context saturation risk | Coding agents need smaller scopes |
| Complex architecture impact | Needs global rules and module contracts |
| Significant compliance/audit impact | Needs traceability and controlled handoff |

## Do not use Modular Delivery when

Avoid this track if:
- the request is small,
- the change is local to one component,
- OpenSpec can directly handle the change,
- there is no architectural ambiguity,
- the business request is already precise.

## Core idea

```text
Business capabilities
  ↓
Software modules
  ↓
Vertical deliverables
  ↓
OpenSpec change for active deliverable
```

## OpenSpec rule

Do not create a second engineering task system outside OpenSpec.

For OpenSpec-based execution, generate:

```text
openspec/changes/D1-<deliverable-name>/
  proposal.md
  design.md
  tasks.md
```
