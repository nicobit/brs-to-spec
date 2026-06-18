# Skill — Create Use Case Diagram

## Identity

| Field | Value |
|---|---|
| skill_id | po-create-use-case-diagram |
| persona | product-owner |
| event_types | CREATE_USE_CASE_DIAGRAM |
| produces | business-analysis/use-cases.puml, business-analysis/use-cases.md |

## When this skill is used

After `CREATE_REQUIREMENTS_CATALOG` completes and `business-analysis/requirements.md` exists. This event produces two co-produced outputs in one pass. Both must be written before the event is marked complete. `CREATE_USE_CASE_SPECS` and `CREATE_ACTORS_AND_PERSONAS` depend on these files.

## Role for this task

You are a senior business analyst producing the behavioral map of the initiative. This diagram assigns stable `UC-NNN` identifiers that are used by every downstream artifact — use-case specs, actors, process flows, planning, BDD, handoff. The IDs must be stable and consistent across both output files.

## Prerequisites check

Before starting, verify:
- [ ] `business-analysis/requirements.md` exists and has at least one FR-NNN row

If the required input is missing, stop and report what is absent.

## Instructions

### Step 1 — Read inputs

Read `business-analysis/requirements.md` in full.
Optionally read `business-intake/business-intake-summary.md` for additional actor context.
Optionally read `input/brs.md` (or `input/brs/*.md`) to cross-check initiative breadth, lifecycle stages, and domain vocabulary.
Do not start writing until requirements are read completely.

### Step 2 — Identify actors

From the functional requirements, identify every human role and external system that:
- initiates a use case
- participates in a use case as a secondary actor
- receives output from a use case

Use the clearest, most stable role name supported by the requirements. If names are ambiguous, choose the best-supported label and note the ambiguity.

### Step 3 — Group requirements into use cases

Group functional requirements into distinct user goals. One use case per distinct, complete goal an actor can achieve. Rules:
- Each use case must trace to at least one FR-NNN
- Do not create one use case per FR — group related FRs under one goal
- Do not collapse the entire initiative into one use case
- Do not add implementation detail or technology names to use case titles
- Separate independent goals into separate use cases

Coverage rules:
- First, scan `requirements.md` by business capability or epic and list the distinct actor-visible goals before drawing anything
- Preserve initiative breadth: if requirements span intake, scoring, compliance, review, offer, disbursement, and administration, the use cases must reflect that breadth rather than stopping at the first entry flow
- A use case may cover multiple FRs only when they belong to the same observable actor goal or tightly-coupled business outcome
- System-only FRs still need representation when they create a distinct governed business outcome or state transition consumed by another actor or process
- If the requirements clearly imply 8 or more distinct user or business goals, producing only 2 or 3 UCs is almost certainly under-modeled and must be treated as a failure to complete the task

Before assigning UC IDs, create a scratch mapping for yourself:
- `Capability/Epic -> candidate goal(s) -> FR-NNN coverage`
- Use that mapping to confirm that no major requirement cluster is silently omitted
- If `requirements.md` appears domain-mismatched, suspiciously tiny, or contaminated by generic starter content, cross-check against the BRS and fail the event instead of producing shallow UCs

### Step 4 — Assign stable UC-NNN IDs

Assign sequential IDs starting at UC-001. These IDs are permanent — downstream artifacts reference them by ID. Do not renumber after assignment.

### Step 5 — Write Output A: use-cases.puml

Write the PlantUML file at `business-analysis/use-cases.puml`.

Use standard PlantUML use-case syntax:

```
@startuml
left to right direction

actor "Actor Name" as ACTOR_1
actor "Second Actor" as ACTOR_2

rectangle "System Name" {
  usecase "UC-001 Do Something" as UC001
  usecase "UC-002 Do Something Else" as UC002
  usecase "UC-003 Another Goal" as UC003
}

ACTOR_1 --> UC001
ACTOR_1 --> UC002
ACTOR_2 --> UC003
@enduml
```

Rules:
- `left to right direction` must be present
- One system boundary rectangle containing all use cases
- Actors declared outside the rectangle
- UC-NNN ID must appear in the usecase label or alias
- Every actor must connect to at least one use case

### Step 6 — Write Output B: use-cases.md

Write the markdown file at `business-analysis/use-cases.md`.

This file uses the same UC-NNN IDs and actor names as the PUML file. It is the GitLab Pages / IDE-renderable version. Use the artifact template at `.brs2spec2/artifact-templates/use-cases.md`.

Mermaid diagram conventions:
- Use `graph LR` (horizontal, matching PlantUML left-to-right convention)
- Actors: person shape — `ACTOR_1([Actor Name])`
- Use cases: rounded rectangle — `UC001(UC-001 Do Something)`
- Connections: `ACTOR_1 --> UC001`

Example:

```
graph LR
  ACTOR_1([Actor Name])
  ACTOR_2([Second Actor])
  UC001(UC-001 Do Something)
  UC002(UC-002 Do Something Else)
  UC003(UC-003 Another Goal)
  ACTOR_1 --> UC001
  ACTOR_1 --> UC002
  ACTOR_2 --> UC003
```

After the diagram, include a UC Catalog table:

| UC-NNN | Title | Primary Actor(s) | FR Sources |
|---|---|---|---|
| UC-001 | Do Something | Actor Name | FR-001, FR-002 |

### Step 7 — Verify consistency

Before finishing, verify:
- Every UC-NNN ID in `use-cases.puml` has an identical entry in `use-cases.md`
- Every actor in `use-cases.puml` appears in `use-cases.md`
- Every use case traces to at least one FR-NNN in the catalog table
- No UC-NNN in the catalog table is missing from the diagram
- Every major FR cluster from `requirements.md` is covered by at least one UC, or explicitly excluded with a brief justification in `use-cases.md`
- The UC set represents the whole initiative lifecycle, not just the first submission flow, when the requirements describe a broader lifecycle

## Output requirements

Both files must be written:
- `business-analysis/use-cases.puml` — valid PlantUML, at least one UC-NNN, actors declared
- `business-analysis/use-cases.md` — metadata table, Mermaid graph LR block, UC catalog table

UC-NNN IDs must be identical in both files.

## Done criteria

- [ ] `business-analysis/use-cases.puml` written and contains at least one UC-NNN
- [ ] `business-analysis/use-cases.md` written and contains at least one UC-NNN
- [ ] UC-NNN IDs are identical across both files
- [ ] Actor names are identical across both files
- [ ] Every UC-NNN traces to at least one FR-NNN in the catalog table
- [ ] Every major FR cluster or epic in `requirements.md` is represented by at least one UC or explicit exclusion note
- [ ] The number of UCs is proportionate to the breadth of the requirements, not just the first one or two entry flows
- [ ] `Status: Draft` in the metadata table of `use-cases.md`
- [ ] Result file written with `status: pass` and `artifacts_written` listing both files

## Stop conditions

- If `requirements.md` is missing or has no FR-NNN rows, stop and report the blocker.
- If the initiative is purely technical with no user-facing goals, produce the artifacts with an explanation rather than inventing business use cases.
- Do not invent use cases not traceable to FR-NNN entries in requirements.md.
