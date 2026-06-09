---
description: Generate initiative-context.md after readiness is approved — required before implementation starts.
---

# Generate Initiative Context

Run this once per deliverable, after `engineering-readiness/readiness-check.md` is approved and before implementation begins.

Follow:

```text
.brs2spec/4-engineering-readiness/02-generate-initiative-context.md
templates/engineering-readiness/initiative-context.md
```

## Purpose

Distill the approved readiness decision into a single compact file that all downstream agents load first:

```text
engineering-readiness/initiative-context.md
```

This file carries technology constraints, architecture rules, governed boundaries, active gates, and rollback sensitivity so implementation and review sessions stay consistent across context windows.

## Preconditions

```text
engineering-readiness/readiness-check.md must exist and be approved
```

## Output

```text
engineering-readiness/initiative-context.md
```
