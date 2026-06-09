---
description: Generate a draft architecture from the BRS when no architecture input exists — requires architect review before use.
---

# Draft Architecture from BRS

Use this when `input/architecture.md` is missing, empty, or contains only a stub.

Follow:

```text
.brs2spec/0-input-preparation/04-draft-architecture-from-brs.md
```

## Purpose

Derive a draft architecture proposal from the BRS requirements, integrations, constraints, and NFRs.

This unblocks the workflow when no architecture document has been provided and gives an architect a concrete starting point to validate or correct.

## Preconditions

```text
input/brs.md must exist and contain real requirements
```

## Output

```text
input/architecture.md  (marked DRAFT — requires architect review)
```

## Mandatory next step

After saving the draft, run the architecture review immediately:

```text
.brs2spec/3-planning-and-modular-delivery/01-review-initial-architecture.md
```

The architecture review will assess the draft against the BRS and flag what the architect must confirm or correct before the output is treated as authoritative.
