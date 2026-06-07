# Architecture-Aware Flow

The initial architecture document is a first-class input.

## Core propagation

```text
input/initial-architecture.md
  ↓
architecture/initial-architecture-review.md
  ↓
architecture/global-architecture-rules.md
  ↓
modules/software-modules.md
  ↓
planning/delivery-increments.md
  ↓
engineering-readiness/readiness-check.md
  ↓
openspec/changes/D1-.../design.md
```

## Rule

If the initial architecture document defines a constraint, do not override it unless explicitly marked as conflict or open decision.

## Initial Architecture Review

This artifact identifies:
- defined constraints,
- missing architecture information,
- conflicts with BRS,
- open decisions,
- inherited rules for modules and deliverables.

## Global Architecture Rules

This artifact turns reviewed architecture constraints into reusable rules.

All modules, deliverables, and OpenSpec designs must comply with them.
