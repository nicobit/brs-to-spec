# Execution Modes

Execution mode answers: *who builds the deliverable, and with what downstream?*

It is independent of the delivery mode (Fast / Standard / Enterprise /
Enterprise + Modular).

## Execution Mode A — OpenSpec (default)

Use when OpenSpec is available. OpenSpec is the default engineering downstream.

```text
prompts/5-handoff/01-create-openspec-change-for-active-deliverable.md
  → openspec/changes/D1-<deliverable-name>/
      proposal.md
      design.md
      tasks.md
```

## Execution Mode B — Standalone

Use when OpenSpec is **not** used. The framework remains the source of truth for
engineering execution.

```text
prompts/5-handoff/03-create-standalone-delivery-package.md
  → standalone-delivery/D1-<deliverable-name>/
      delivery-spec.md
      implementation-plan.md
      tasks.md
      validation-plan.md
      review-checklist.md
```

Standalone preserves the same discipline as OpenSpec:
- clear scope,
- architecture constraints,
- small tasks,
- validation,
- review gates.

It does **not** pretend to be OpenSpec, and it uses its own `standalone-delivery/`
output tree.

## Execution Mode C — Business Copilot

Use when business users drive the early work in Microsoft 365 Copilot,
SharePoint, Word, Teams, or Copilot Studio.

```text
prompts/6-business-copilot/
docs/04-business-copilot/
```

Business Copilot focuses on business-friendly intake and approval, and feeds into
the same planning and (eventually) Mode A or Mode B execution.

## Source-of-truth rule

```text
Mode A: OpenSpec owns execution.
Mode B: this framework (standalone-delivery/) owns execution.
```

Do not run Mode A and Mode B for the same deliverable at the same time.
