# Delivery and Execution Modes

## Delivery modes

Delivery mode defines how much workflow control is needed for the initiative.

| Delivery mode | Score | Use when | Typical output |
|---|---|---|---|
| Fast Path | 0–3 | Change is already clear and engineering-ready | OpenSpec directly or small standalone package |
| Standard | 4–7 | Some clarification is needed | Business intake + readiness + handoff |
| Enterprise | 8–11 | Formal BRS, architecture impact, compliance, multiple stakeholders | Intake + architecture + traceability + gates |
| Enterprise + Modular Delivery | 12–14 | Large, multi-team, multi-quarter work or AI context saturation risk | Modules + increments + active-deliverable handoff |

Score your initiative using `docs/03-decision-tree.md` before selecting a mode.

Do not choose Enterprise + Modular by default. Reach score 12+ before selecting it.

## Execution modes

Execution mode defines the downstream engineering contract format.

| Execution mode | Use when | Output location |
|---|---|---|
| OpenSpec | OpenSpec is available and should be the engineering source of truth | `openspec/changes/D1-<name>/` inside the initiative workspace |
| Standalone | OpenSpec is not used | `standalone-delivery/D1-<name>/` inside the initiative workspace |
| Business Copilot | Business users review and approve in Microsoft 365 / SharePoint / Word / Teams | SharePoint/Word review outputs plus initiative-scoped framework artifacts |

Execution mode does not change the upstream workflow. It only changes where the engineering handoff lands.

## Minimum artifact set by delivery mode

| Artifact | Fast Path | Standard | Enterprise | Enterprise + Modular |
|---|---|---|---|---|
| `input/input-package.md` | Required | Required | Required | Required |
| `routing/routing-decision.md` | Required | Required | Required | Required |
| `business-intake/business-intake-summary.md` | Optional | Required | Required | Required |
| `architecture/architecture-review.md` | Skip | Optional | Required | Required |
| `architecture/architecture-rules.md` | Skip | Optional | Required | Required |
| `planning/delivery-structure.md` | Skip | Required | Required | Required |
| `planning/delivery-increments.md` | Skip | Skip | Skip | Required |
| `planning/traceability-matrix.md` | Skip | Optional | Required | Required |
| `engineering-readiness/readiness-check.md` | Required if risk exists | Required | Required | Required |
| Quality gates | Triggered only | Triggered only | Triggered only | Triggered only |
| Handoff artifact | Required | Required | Required | Required |

## Important rule

Quality gates are conditional, not optional.

If the readiness check marks a gate as triggered and required, it must be completed before the required-before stage regardless of the delivery mode.

See [Conditional Quality Gates](06-conditional-quality-gates.md).

## See also

- [Decision Tree](03-decision-tree.md)
- [Entry Modes](18-entry-modes.md)
- [Conditional Quality Gates](06-conditional-quality-gates.md)
