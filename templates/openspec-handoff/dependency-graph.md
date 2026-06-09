# Dependency Graph — {{Initiative ID}}: {{Initiative Name}}

> Engineering lead reference. Shows which user stories can start in parallel and which must wait.
> Generated from `planning/delivery-structure.md` increment grouping and shared schema/API dependencies.
> Update this file when stories are added, reordered, or dependencies change.

## Execution order

<!-- Stories are grouped into waves — all stories in a wave can run in parallel. -->
<!-- A wave starts only when all stories in the previous wave are deployed. -->

### Wave 1 — can start immediately

| Story | Title | Owner | Folder |
|---|---|---|---|

### Wave 2 — starts when Wave 1 is deployed

| Story | Title | Depends on | Owner | Folder |
|---|---|---|---|---|

### Wave 3 — starts when Wave 2 is deployed

| Story | Title | Depends on | Owner | Folder |
|---|---|---|---|---|

<!-- Add more waves as needed. -->

## Dependency detail

<!-- One row per dependency. Use this to explain WHY a dependency exists. -->

| Story | Depends on | Reason |
|---|---|---|

## Parallelism notes

<!-- Call out any non-obvious parallelism — stories in the same wave that share a component -->
<!-- and need coordination even though they can start at the same time. -->

## Diagram

<!-- Mermaid dependency graph. Generate from the waves table above. -->

```mermaid
graph LR
```
