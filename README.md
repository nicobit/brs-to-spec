# Adaptive Enterprise BRS-to-Delivery Framework

An adaptive enterprise BRS-to-delivery-readiness framework that transforms a raw
BRS and an initial architecture document into **business-approved,
architecture-aligned delivery increments**, with **OpenSpec as the default
downstream** and **standalone execution supported** when OpenSpec is not used.

## What this framework is

- A front door that turns business-heavy, ambiguous, multi-stakeholder,
  architecture-sensitive BRS input into small, engineering-ready deliverables.
- Architecture-aware: the initial architecture document is a first-class input
  whose constraints propagate through the whole flow.
- Adaptive: you pick the smallest delivery mode and the execution mode that match
  your situation.

## What this framework is not

- It is **not** a replacement for OpenSpec.
- It does not require dozens of artifacts for every change.
- It does not generate tasks for the whole BRS at once.
- It does not let AI invent architecture that conflicts with the initial
  architecture document.

## When to use OpenSpec directly vs this framework

```text
Use OpenSpec directly
  → for clear engineering changes.

Use this framework
  → when a raw BRS and optional initial architecture document must be transformed
    into business-approved, architecture-aligned, OpenSpec-ready (or standalone)
    delivery increments.
```

## Input artifacts

Source documents (Word / SharePoint / Confluence / text) are normalized into:

```text
input/brs.md
input/initial-architecture.md
input/input-package.md
```

The initial architecture document is a first-class input. If none exists, create
`input/initial-architecture.md` and mark it as
`No initial architecture document provided.`

## Structure

```text
docs/
prompts/
  0-input-preparation/
  1-routing/
  2-business-intake/
  3-planning-and-modular-delivery/
  4-engineering-readiness/
    quality-gates/
  5-handoff/
  6-business-copilot/
templates/
examples/
schemas/
tools/scripts/
```

`5-handoff` is intentionally generalized (not `5-handoff-to-openspec`): OpenSpec is
the default downstream, but it is not the only supported execution path.

## Delivery modes

How much ceremony the change needs:

```text
Fast Path                     → go straight to the chosen execution mode
Standard Path                 → business intake summary + execution mode
Enterprise Path               → BRS + architecture + readiness + execution mode
Enterprise + Modular Delivery → modules + vertical increments + execution mode
```

## Execution modes

Which downstream actually builds it (orthogonal to delivery mode):

```text
Execution Mode A — OpenSpec    (default downstream)
Execution Mode B — Standalone  (when OpenSpec is not used)
Execution Mode C — Business Copilot (M365 / SharePoint / Word / Teams / Copilot Studio)
```

## Conditional Quality Gates

Detailed governance is preserved but **conditional** — not "optional".

```text
Not triggered → skipped
Triggered     → required (mandatory before implementation, merge, or release)
```

The engineering readiness check decides which gates trigger:

```text
| Quality Gate | Triggered? | Required? | Reason | Owner | Output |
```

Gates: BDD scenarios, test strategy, QA review, architecture review, security
review, release readiness, API contract, data contract, event contract, threat
model, observability plan. See `docs/06-conditional-quality-gates.md`.

## Architecture-aware rule

If the initial architecture document defines a constraint, do not override it
unless explicitly marked as a conflict or open decision. Constraints propagate
into the architecture review, global rules, modules, increments, traceability
matrix, readiness check, and the downstream design (OpenSpec) or delivery spec
(standalone).

## Product Owner experience

The Product Owner primarily reviews one artifact:

```text
business-intake/business-intake-summary.md
```

POs do not manage module specs, API contracts, implementation tasks, OpenSpec
tasks, or low-level test automation.

## Final outputs

```text
Execution Mode A — OpenSpec
openspec/changes/D1-<deliverable-name>/
  proposal.md
  design.md
  tasks.md

Execution Mode B — Standalone
standalone-delivery/D1-<deliverable-name>/
  delivery-spec.md
  implementation-plan.md
  tasks.md
  validation-plan.md
  review-checklist.md
```

## Where to go next

- `HOW_TO_USE.md` — step-by-step usage.
- `docs/02-delivery-modes.md` — delivery + execution modes.
- `docs/06-conditional-quality-gates.md` — quality gates.
- `docs/08-execution-modes.md` — OpenSpec / Standalone / Business Copilot.
- `docs/09-migration-0.0.7-to-0.0.8.md` — what changed from 0.0.7.
