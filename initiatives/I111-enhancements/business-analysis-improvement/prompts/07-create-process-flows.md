# Prompt — Create Process Flows

## Purpose

Create or update `business-analysis/process-flows.md`.

This prompt is adapted from `.brs2spec2/skills/product-owner/create-process-flows.md`, but refocused so process flows are synthesized from stable use cases and actors rather than generated directly from raw BRS text alone.

## Instructions

Create or update `business-analysis/process-flows.md`.

Treat this artifact as the cross-use-case operational journey view.

## DO NOT

- Duplicate detailed use-case specs here
- Describe implementation design or component internals
- Invent flows that are not supported by the use cases or source requirements
- Turn every edge case into its own process flow

## Inputs

Required:

- `business-analysis/use-cases/UC-*.md`
- `business-analysis/actors-and-personas.md`

Optional:

- `business-analysis/business-rules.md`
- architecture feedback where system boundaries or integrations affect the journey

## Workflow

1. Read the available `UC-*.md` files.
2. Identify the major end-to-end business journeys that span one or more use cases.
3. Define one `PF-NNN` per meaningful operational flow.
4. For each flow, record trigger, primary actor, major steps, decision points, alternative paths, and outcomes.
5. Add a compact Mermaid flowchart for each flow.

## Required structure

Suggested catalog:

| ID | Name | Primary Actor | Trigger | Outcome | Source |
|---|---|---|---|---|---|
| PF-001 |  | ACT-001 |  |  |  |

Each flow should include:

- trigger
- preconditions
- steps
- decision points
- alternative paths
- postconditions
- references to relevant `BR-NNN` rules where applicable

## Diagram rules

Use Mermaid `flowchart LR` or `flowchart TD`.

- Node IDs must be alphanumeric or underscore only
- Labels with special characters should be quoted
- Diagrams should stay at the business flow level

## Output expectations

This artifact should later support:

- architecture review
- observability planning
- event and integration reasoning
- operations-oriented planning

## Error handling

- If the use cases are not mature enough to synthesize reliable flows, produce a partial artifact and explicitly state what is still unstable.
- If a flow depends on unresolved architecture or integration choices, surface that as a dependency rather than guessing.
