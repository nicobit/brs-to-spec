# Prompt — Create Actors and Personas

## Purpose

Create or update `business-analysis/actors-and-personas.md`.

This prompt is adapted from `.brs2spec2/skills/product-owner/create-actors-and-personas.md`, refocused so actor identification is aligned with the use-case diagram rather than derived only from the raw BRS.

## Instructions

Create or update `business-analysis/actors-and-personas.md`.

Assign stable IDs for:

- human actors: `ACT-NNN`
- external systems: `SYS-NNN`

## DO NOT

- Invent actors or systems not supported by requirements, use-case diagram, or source materials
- Treat implementation components as business actors
- Write personas detached from actual use-case participation

## Inputs

Required:

- `business-analysis/requirements.md`
- `business-analysis/use-cases.puml`

Optional:

- `business-analysis/business-rules.md`
- `input/brs.md`

## Workflow

1. Read the requirements catalog and use-case diagram.
2. Identify all human actors who initiate, approve, review, receive, or manage business actions.
3. Identify all external systems visible in the initiative scope.
4. Assign stable IDs.
5. Capture each actor's goal, major interactions, and relevant permissions or restrictions.
6. Build an interaction matrix that shows which actors interact with which use cases or system boundaries.

## Required structure

Suggested sections:

- Metadata
- Human Actors
- Systems
- Interaction Matrix

Suggested actor table:

| ID | Name | Type | Primary Goal | Key Interactions | Source |
|---|---|---|---|---|---|
| ACT-001 |  | Human |  |  |  |

## Quality rules

- Every actor in `use-cases.puml` should appear here.
- Names should be stable enough for later use in process flows and handoff.
- Permissions and restrictions should trace to source requirements or business rules.

## Output expectations

This artifact should later support:

- process flows
- use-case specifications
- architecture review
- handoff role mapping

## Error handling

- If actor naming is inconsistent across sources, choose the clearest stable label and note the aliasing.
- If a system is purely internal implementation detail, do not elevate it to a business actor unless the scope explicitly treats it that way.
