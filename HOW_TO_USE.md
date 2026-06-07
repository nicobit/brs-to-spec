# How to Use This Framework

## Step 0 — Prepare inputs

If your source documents are Word, SharePoint exports, Confluence pages, or unstructured text, first normalize them.

Run:

```text
prompts/0-input-preparation/01-convert-brs-word-to-markdown.md
prompts/0-input-preparation/02-convert-architecture-word-to-markdown.md
prompts/0-input-preparation/03-normalize-input-package.md
```

Outputs:

```text
input/brs.md
input/initial-architecture.md
input/input-package.md
```

If no architecture document exists, create `input/initial-architecture.md` and mark it as:

```text
No initial architecture document provided.
```

## Step 1 — Select delivery mode

Run:

```text
prompts/1-routing/01-select-delivery-mode.md
```

The output recommends:

```text
Fast Path
Standard Path
Enterprise Path
Enterprise + Modular Delivery
```

## Fast Path

Use when the change is already clear and engineering-ready.

```text
request
  ↓
OpenSpec directly
```

Skip the rest of the framework.

## Standard Path

Use when the change needs light business clarification.

Run:

```text
0-input-preparation if needed
2-business-intake/01-create-business-intake-summary.md
5-handoff-to-openspec/01-create-openspec-change-for-active-deliverable.md
```

## Enterprise Path

Use when there is a formal BRS, business approval, or architecture impact.

Run:

```text
0-input-preparation/*
1-routing/01-select-delivery-mode.md
2-business-intake/01-create-business-intake-summary.md
3-planning-and-modular-delivery/01-create-delivery-structure.md
3-planning-and-modular-delivery/02-review-initial-architecture.md
3-planning-and-modular-delivery/03-create-global-architecture-rules.md
4-engineering-readiness/01-check-engineering-readiness.md
5-handoff-to-openspec/01-create-openspec-change-for-active-deliverable.md
```

## Enterprise + Modular Delivery

Use only when needed:
- 12-15+ person-months,
- multi-quarter delivery,
- multiple systems or teams,
- high AI context saturation risk,
- complex architecture impact.

Run:

```text
0-input-preparation/*
1-routing/01-select-delivery-mode.md
2-business-intake/01-create-business-intake-summary.md
3-planning-and-modular-delivery/01-create-delivery-structure.md
3-planning-and-modular-delivery/02-review-initial-architecture.md
3-planning-and-modular-delivery/03-create-global-architecture-rules.md
3-planning-and-modular-delivery/04-identify-software-modules.md
3-planning-and-modular-delivery/05-map-capabilities-to-modules.md
3-planning-and-modular-delivery/06-define-delivery-increments.md
3-planning-and-modular-delivery/07-create-traceability-matrix.md
4-engineering-readiness/01-check-engineering-readiness.md
5-handoff-to-openspec/01-create-openspec-change-for-active-deliverable.md
```

## Product Owner experience

The Product Owner should primarily review:

```text
business-intake/business-intake-summary.md
```

The PO should not manage:
- module technical specs,
- API contracts,
- implementation tasks,
- OpenSpec tasks,
- low-level test automation.

## Engineering experience

Engineering should receive a compact package:

```text
input/brs.md
input/initial-architecture.md
business-intake/business-intake-summary.md
architecture/initial-architecture-review.md
architecture/global-architecture-rules.md
planning/delivery-increments.md
planning/traceability-matrix.md
engineering-readiness/readiness-check.md
```

Then engineering creates or reviews:

```text
openspec/changes/D1-<deliverable-name>/
  proposal.md
  design.md
  tasks.md
```

## Important rules

- Do not generate tasks for all deliverables at once.
- Do not create a second task system outside OpenSpec.
- Do not ignore the initial architecture document.
- Do not use Modular Delivery for small changes.
- Use advanced governance only when the readiness check requires it.
