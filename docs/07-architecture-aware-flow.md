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
planning/traceability-matrix.md
  ↓
engineering-readiness/readiness-check.md
  ↓
Execution Mode A: openspec/changes/D1-.../design.md
Execution Mode B: standalone-delivery/D1-.../delivery-spec.md
```

In both execution modes the architecture constraints must propagate all the way
into the downstream design / delivery spec and into any triggered quality gates.

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

All modules, deliverables, OpenSpec designs, and standalone delivery specs must
comply with them.
