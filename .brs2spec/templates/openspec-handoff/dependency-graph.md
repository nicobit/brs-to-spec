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

## Cross-repo dependencies

> **Omit this entire section if `input/repositories/` does not exist or is empty.**
> This section captures intra-story repo sequencing — which repo subfolder within a story must deliver
> before another repo subfolder in the same story can start integration.
> This is NOT story-to-story ordering (that is in the waves above).
>
> A dependency exists when:
> - A UI subfolder consumes an API contract produced by the API subfolder of the same story
> - A service subfolder reads a schema produced by the DB subfolder of the same story
> - Any subfolder requires a build artifact or event contract from another subfolder of the same story
>
> One row per intra-story repo dependency. List only real blocking dependencies — not coordination preferences.

| Story | Repo subfolder | Depends on | Reason |
|---|---|---|---|
| F-XXX.X | ui | F-XXX.X/api | UI integration requires stable endpoint contract before components can be wired |
| F-XXX.X | api | F-XXX.X/db | API implementation requires schema migration to be applied before queries can run |

## Diagram

> Generate a Mermaid `graph LR` diagram from the waves and cross-repo dependencies above.
>
> **Mermaid syntax rules — these prevent parse errors:**
> - Node IDs must use only letters, digits, and underscores. Replace hyphens and dots: `F-001.1` → `F001_1`.
> - Always quote node labels: `F001_1["F-001.1 — Story name"]` — never `F001_1[F-001.1 — Story name]`.
> - Labels containing `()`, `,`, `/`, or spaces must be in double quotes inside `[]`.
> - Never use HTML tags (`<br/>`, `<b>`, etc.) in node labels — they cause parse errors. Use ` / ` or ` — ` as separators.
> - Never use `&` to connect multiple nodes in one edge statement — `A & B --> C` is invalid in Mermaid 11. Write one edge per line.
>
> **Without repo descriptors (Case A — flat):** one node per story, one arrow per story-to-story dependency.
> Node format: `F001_1["F-001.1 — Story name"]`
>
> **With repo descriptors (Case B — repo subfolders):** one node per repo subfolder, arrows for both
> story-to-story dependencies AND intra-story repo dependencies.
> Node ID convention: replace hyphens and dots with underscores, append underscore + repo name.
> Examples: `F-001.1` → `F001_1`, `F-012.3` → `F012_3`
> Full node format: `F001_1_api["F-001.1 / api"]`, `F012_3_ui["F-012.3 / ui"]`
> Intra-story arrow example: `F001_1_api --> F001_1_ui`
> Inter-story arrow example: `F001_1_api --> F002_1_api`
>
> Keep the diagram readable — if more than 12 nodes, group by wave using Mermaid subgraphs.

```mermaid
graph LR
```
