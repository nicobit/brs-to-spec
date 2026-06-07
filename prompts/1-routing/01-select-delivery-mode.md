# Prompt — Select Delivery Mode and Execution Mode

## Purpose

Decide two independent things:

1. **Delivery mode** — how much ceremony the change needs.
2. **Execution mode** — which downstream actually builds the deliverable.

## Inputs

Use:
- `input/brs.md` if available,
- `input/initial-architecture.md` if available,
- `input/input-package.md` if available,
- known business and tooling context.

## Output file

```text
routing/delivery-mode-decision.md
```

## Output

```markdown
# Delivery Mode Decision

## Recommended Delivery Mode
Fast Path / Standard Path / Enterprise Path / Enterprise + Modular Delivery

## Recommended Execution Mode
Execution Mode A — OpenSpec / Execution Mode B — Standalone / Execution Mode C — Business Copilot

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
| OpenSpec available downstream |  |  |
| No downstream framework available |  |  |
| Primary audience is business users (M365/Copilot) |  |  |

## Tracks to Use

## Tracks to Skip

## Recommended Next Prompt
```

## Delivery modes

- **Fast Path** — already engineering-ready; go straight to the chosen execution mode.
- **Standard Path** — light business clarification, then execution mode.
- **Enterprise Path** — formal BRS, architecture impact, readiness, then execution mode.
- **Enterprise + Modular Delivery** — large initiatives split into modules and increments.

## Execution modes

- **Execution Mode A — OpenSpec** (default). Use when OpenSpec is available; it is
  the default engineering downstream. Output goes to `openspec/changes/`.
- **Execution Mode B — Standalone**. Use when OpenSpec is not used. Output goes to
  `standalone-delivery/`. Keeps the same discipline (scope, architecture
  constraints, small tasks, validation, review gates) without pretending to be
  OpenSpec.
- **Execution Mode C — Business Copilot**. Use when business users drive the early
  work in Microsoft 365 Copilot / SharePoint / Word / Teams / Copilot Studio.

Delivery mode and execution mode are **orthogonal**: any delivery mode can be run
in any execution mode.

## Rules

- Do not recommend the full framework for small changes.
- Recommend Fast Path + Execution Mode A (OpenSpec directly) for clear
  engineering-ready changes when OpenSpec is available.
- Recommend Execution Mode B (Standalone) when no downstream framework is used.
- Recommend Modular Delivery only for large initiatives.
- If initial architecture is present, recommend architecture review for Enterprise
  paths.
