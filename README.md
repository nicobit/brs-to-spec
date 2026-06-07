# Enterprise BRS to OpenSpec Readiness Framework

**Purpose:** transform a raw enterprise BRS and an optional initial architecture document into **business-approved, architecture-aligned, OpenSpec-ready delivery increments**.

This framework is intentionally **not** a replacement for OpenSpec.

Use OpenSpec directly for clear engineering changes. Use this framework when the input is still business-heavy, ambiguous, multi-stakeholder, architecture-sensitive, or too large for a single AI coding context.

## What this framework does

```text
Word / SharePoint / Confluence BRS
+
Initial Architecture Document
  ↓
0. Input Preparation
  ↓
1. Routing
  ↓
2. Business Intake
  ↓
3. Planning and Modular Delivery
  ↓
4. Engineering Readiness
  ↓
5. Handoff to OpenSpec
```

## What this framework does not do

This framework does not:
- replace OpenSpec,
- replace engineering judgment,
- require dozens of artifacts for every change,
- generate tasks for the whole BRS at once,
- let AI invent architecture that conflicts with the initial architecture document.

## Core principle

Use the smallest path that gives enough control.

```text
Fast Path
  → OpenSpec directly

Standard Path
  → input preparation + business intake summary + OpenSpec

Enterprise Path
  → BRS + initial architecture + readiness + OpenSpec

Enterprise + Modular Delivery
  → modules + vertical deliverables + OpenSpec change for active deliverable
```

## Final project structure

```text
docs/
prompts/
  0-input-preparation/
  1-routing/
  2-business-intake/
  3-planning-and-modular-delivery/
  4-engineering-readiness/
  5-handoff-to-openspec/
  6-business-copilot/
templates/
examples/
schemas/
tools/scripts/
```

## Official input artifacts

The framework normalizes source documents into:

```text
input/brs.md
input/initial-architecture.md
input/input-package.md
```

All downstream prompts should use these normalized inputs.

## Architecture-aware rule

If the initial architecture document defines a constraint, do not override it unless explicitly marked as a conflict or open decision.

This rule applies to:
- global architecture rules,
- software modules,
- delivery increments,
- engineering readiness,
- OpenSpec proposal/design/tasks.

## Main workflow

```text
0. Prepare inputs
1. Select delivery mode
2. Create business intake summary
3. Review initial architecture
4. Create delivery structure
5. Create global architecture rules
6. Use modular delivery only if needed
7. Create traceability matrix
8. Check engineering readiness
9. Create OpenSpec change for the active deliverable
```

## Default downstream

The default downstream execution layer is:

```text
OpenSpec
```

The final engineering output should normally be:

```text
openspec/changes/D1-<deliverable-name>/
  proposal.md
  design.md
  tasks.md
```

## Business Copilot

Business users can run the early intake in:
- Microsoft 365 Copilot,
- Word,
- SharePoint,
- Teams,
- Copilot Studio.

Use:

```text
prompts/6-business-copilot/
docs/04-business-copilot/
```

## Recommended sentence

Use OpenSpec directly for clear engineering changes.  
Use this framework when a raw BRS and initial architecture document must be transformed into business-approved, architecture-aligned, OpenSpec-ready delivery increments.

## Advanced optional governance pack

The simplified framework keeps the main path small, but includes optional enterprise review prompts when needed:

```text
BDD scenarios
test strategy
QA review
architecture review
security review
release readiness review
```

These are under:

```text
prompts/4-engineering-readiness/advanced/
templates/advanced-governance/
```

They are not part of the default workflow. Use them only when `engineering-readiness/readiness-check.md` requires them.
