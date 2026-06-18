# Entry Modes

## Purpose

Entry modes help a user choose the right starting pattern before selecting delivery mode and execution mode.

They are not a second routing framework.

They are a lightweight front door to the existing initiative workspace model.

## Rule

Use entry mode first.

Then use the normal framework routing:

```text
.brs2spec/skills/1-routing/01-select-delivery-and-execution-mode.md
```

## Entry mode summary

Supported entry modes:

```text
BRS-first
existing-system enhancement
small change / bug fix
large modular initiative
```

| Entry mode | Use when | Minimum starting artifacts | Likely next prompt | Risk if the wrong mode is chosen |
|---|---|---|---|---|
| BRS-first | The initiative begins from one or more business requirements documents | `input/brs.md`, optional `input/architecture.md`, `input/input-package.md` | `.brs2spec/skills/0-input-preparation/03-normalize-input-package.md` then routing | Business ambiguity, overlap, and assumptions may not be captured early enough |
| Existing-system enhancement | The initiative changes an existing service, module, integration, contract, or operational flow | normalized inputs plus available existing-system context | `.brs2spec/skills/2-business-intake/01-create-business-intake-summary.md` then architecture review | Regression, compatibility, and governed-boundary impact may be underestimated |
| Small change / bug fix | Scope is narrow and may qualify for Fast Path | concise business statement, architecture context when relevant, `input/input-package.md` | routing, then the smallest safe flow | Teams may either over-process a simple fix or under-control a risky one |
| Large modular initiative | Scope spans multiple capabilities, deliverables, teams, or increments | normalized inputs, architecture context, delivery-shaping context | routing, then modular planning prompts | Work may be under-sliced and context may become too large too early |

## How entry modes relate to delivery modes

Entry mode answers:

```text
What kind of situation am I entering?
```

Delivery mode answers:

```text
How much workflow control do I need?
```

Execution mode answers:

```text
What downstream engineering contract format will I use?
```

## Quick guidance

### BRS-first

Use this when the starting point is mainly requirements documentation.

Typical flow:

```text
prepare inputs
normalize input package
route the initiative
continue with intake
```

### Existing-system enhancement

Use this when the most important risk is not missing business intent, but changing something that already exists.

Focus early on:

```text
affected components
existing architecture constraints
contract impact
regression risk
operational dependencies
```

### Small change / bug fix

Use this when the change is narrow enough that Fast Path may be appropriate, but only if architecture and risk stay clear.

Do not assume a small change means:

```text
skip readiness
skip triggered quality gates
skip architecture constraints
```

### Large modular initiative

Use this when:

```text
multiple capabilities are involved
multiple teams are involved
the work must be sliced into deliverables or increments
context size would become too large in a single handoff
```

## Copilot usage

When using GitHub Copilot or VS Code Copilot, ask for both:

```text
the likely entry mode
the likely current workflow stage
```

Example:

```text
Based on the initiative workspace and available artifacts, identify the best entry mode, the current workflow stage, and the next prompt to run.
```
