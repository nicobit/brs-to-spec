# Delivery Modes and Execution Modes

The framework separates two orthogonal decisions:

- **Delivery mode** — how much ceremony the change needs.
- **Execution mode** — which downstream actually builds the deliverable.

Any delivery mode can be combined with any execution mode.

## Delivery modes

### Fast Path

Go straight to the chosen execution mode.

Good for:
- bugfix,
- local change,
- clear engineering work,
- no formal business approval.

### Standard Path

Business intake summary, then the chosen execution mode.

Good for:
- medium feature,
- limited ambiguity,
- limited architecture impact.

### Enterprise Path

Business intake, architecture review, engineering readiness, then the chosen
execution mode.

Good for:
- formal BRS,
- initial architecture document,
- architecture alignment,
- compliance/audit,
- multiple stakeholders.

### Enterprise + Modular Delivery

For large initiatives split into modules and vertical increments.

Good for:
- 12-15+ person-months,
- multi-quarter roadmap,
- multiple teams,
- multiple systems,
- high AI context saturation risk.

## Execution modes

### Execution Mode A — OpenSpec (default)

Used when OpenSpec is available; it is the default engineering downstream.

```text
openspec/changes/D1-<deliverable-name>/
  proposal.md
  design.md
  tasks.md
```

### Execution Mode B — Standalone

Used when OpenSpec is not used.

```text
standalone-delivery/D1-<deliverable-name>/
  delivery-spec.md
  implementation-plan.md
  tasks.md
  validation-plan.md
  review-checklist.md
```

### Execution Mode C — Business Copilot

Used by business users in Microsoft 365 Copilot / SharePoint / Word / Teams /
Copilot Studio. See `docs/04-business-copilot/` and
`prompts/6-business-copilot/`.

## Rule

Use the smallest delivery mode that still gives enough control, and the execution
mode that matches your downstream tooling.
