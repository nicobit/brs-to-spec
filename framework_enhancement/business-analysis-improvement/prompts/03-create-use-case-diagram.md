# Prompt — Create Use Case Diagram

## Purpose

Create or update `business-analysis/use-cases.puml` based on:

- `business-analysis/requirements.md`

This prompt is based on the AI Unified Process `/use-case-diagram` behavior documented in the marketplace README and adapted for initiative-local artifact production.

## Instructions

Create or update the PlantUML use case diagram at `business-analysis/use-cases.puml`.

The diagram must:

- identify actors from the requirements catalog
- identify use cases from the functional requirements
- assign stable `UC-NNN` IDs
- show actor-to-use-case relationships

## DO NOT

- Add implementation details to use case names
- Use technology names inside use case titles
- Collapse the entire initiative into one use case
- Create use cases that do not trace back to functional requirements

## Inputs

Required:

- `business-analysis/requirements.md`

Optional:

- `business-intake/business-intake-summary.md`
- `business-analysis/gaps-and-questions.md`

## Diagram rules

Use standard PlantUML use-case syntax.

Include:

- `left to right direction`
- a single system boundary rectangle
- actors outside the system boundary
- use cases inside the boundary
- stable IDs in use case labels or alias structure

## Mapping rules

- Each use case must trace to at least one functional requirement.
- The number of use cases should be at least the number of major user-goal areas in the requirements catalog.
- Separate independent goals into separate use cases.
- Do not create one use case per story or per implementation task.

## Suggested structure

```text
@startuml
left to right direction

actor "Actor Name" as ACTOR_1

rectangle "System Name" {
  usecase "UC-001 Do Something" as UC001
  usecase "UC-002 Do Something Else" as UC002
}

ACTOR_1 --> UC001
ACTOR_1 --> UC002
@enduml
```

## Workflow

1. Read `business-analysis/requirements.md`.
2. Identify actors explicitly named or clearly implied by the functional requirements.
3. Group functional requirements into distinct user goals.
4. Assign stable `UC-NNN` IDs.
5. Draw the diagram with actor relationships.
6. Verify that every use case traces back to one or more FRs.

## Output expectations

This artifact is the behavioral map used before writing detailed use-case specifications.

It should be good enough to support:

- `actors-and-personas.md`
- `use-cases/UC-*.md`
- planning decomposition
- stakeholder review

## Error handling

- If actor names are ambiguous, choose the best-supported role name and note the ambiguity for later alignment.
- If the initiative is purely technical and has no real user goals, explain that clearly instead of inventing business use cases.
