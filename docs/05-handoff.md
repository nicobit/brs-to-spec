# Handoff

Handoff turns the prepared, architecture-aligned deliverable into engineering
execution. There are two execution paths.

- **Execution Mode A — OpenSpec** (default downstream).
- **Execution Mode B — Standalone** (used when OpenSpec is not used).

OpenSpec is the default, but it is **not** the only supported path.

## Handoff objective

Create work for the **active deliverable only** — never the whole BRS.

## Execution Mode A — OpenSpec

Prompt: `prompts/5-handoff/01-create-openspec-change-for-active-deliverable.md`

```text
openspec/changes/D1-<deliverable-name>/
  proposal.md
  design.md
  tasks.md
```

## Execution Mode B — Standalone

Prompt: `prompts/5-handoff/03-create-standalone-delivery-package.md`

```text
standalone-delivery/D1-<deliverable-name>/
  delivery-spec.md
  implementation-plan.md
  tasks.md
  validation-plan.md
  review-checklist.md
```

Standalone keeps the same discipline (clear scope, architecture constraints,
small tasks, validation, review gates) but does not pretend to be OpenSpec.

## Shared inputs

Both modes use:
- normalized BRS,
- normalized initial architecture,
- business intake summary,
- initial architecture review,
- global architecture rules,
- delivery increments,
- traceability matrix,
- engineering readiness check,
- any triggered `quality-gates/*` artifacts.

## Important rules

- Do not create tasks for the whole BRS.
- Use exactly one execution mode per deliverable; do not create both an OpenSpec
  change and a standalone package for the same deliverable.
- Downstream adapters (gstack, kiro, spec-kit) remain available under
  `prompts/5-handoff/advanced/`.
