# Use Case Diagram

## Metadata

| Field | Value |
|---|---|
| Initiative ID | {{initiative_id}} |
| Created at | {{date}} |
| Created by | product-owner |
| Status | Draft |

## Use Case Diagram

```mermaid
graph LR
  ACT_001([Actor Name])
  UC001(UC-001 Goal Title)
  ACT_001 --> UC001
```

Actors use person-shape syntax: `ACT_ID([Actor Name])`.
Use cases use rounded-rectangle syntax: `UC001(UC-001 Title)`.
One node declaration per actor and per use case. One arrow per actor-to-UC relationship.

## UC Catalog

| UC-NNN | Title | Primary Actor(s) | FR Sources |
|---|---|---|---|
| UC-001 | Goal Title | Actor Name | FR-001, FR-002 |

## Coverage Notes

Summarize how the UC set covers the major requirement clusters or lifecycle stages in the initiative.
If any requirement cluster is intentionally excluded, explain why.

---
*Set Status: Accepted only by workflow or human approval when applicable. Never self-accept.*
*This file is co-produced with `use-cases.puml`. UC-NNN IDs must remain identical in both files.*
