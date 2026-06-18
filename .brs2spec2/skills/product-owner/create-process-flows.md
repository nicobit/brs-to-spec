# Skill — Create Process Flows

## Identity

| Field | Value |
|---|---|
| skill_id | po-create-process-flows |
| persona | product-owner |
| event_types | CREATE_PROCESS_FLOWS |
| produces | business-analysis/process-flows.md |

## When this skill is used

After `CREATE_USE_CASE_SPECS` and `CREATE_ACTORS_AND_PERSONAS` both complete. The use-case specs (use-cases/UC-NNN.md) provide the stable scenario definitions, and the actors catalog provides stable ACT-NNN / SYS-NNN IDs. Process flows synthesize the cross-use-case operational journey view from these stable artifacts.

## Role for this task

You are a senior business analyst synthesizing end-to-end operational journeys from the use-case specs and actor catalog, showing how actors and systems interact across multiple use cases — without duplicating the per-UC detail and without prescribing implementation.

## Prerequisites check

Before starting, verify:
- [ ] `business-analysis/use-cases/` folder exists and contains at least one `UC-*.md` file
- [ ] `business-analysis/actors-and-personas.md` exists with ACT-NNN / SYS-NNN IDs

Optional inputs (read if available, do not block if missing):
- [ ] `business-analysis/business-rules.md` (BR-NNN for decision point references)
- [ ] `architecture/architecture-review.md` (architecture feedback on system boundaries)

If any required input is missing, stop and report what is absent.

## Instructions

### Step 1 — Identify all process flows

Read all available `use-cases/UC-*.md` files. Identify the major end-to-end business journeys that span one or more use cases. Each meaningful operational flow becomes one PF-NNN. Typical sources:
- A sequence of use cases a primary actor moves through to reach a business goal
- A cross-actor handoff that spans two or more UC-NNN steps
- A state machine that evolves through multiple use cases over time
- An integration path that spans system boundaries

Do not create a PF-NNN for every edge case — those belong in BDD scenarios.

### Step 2 — For each flow, document

1. **PF-NNN ID and name** — sequential, stable ID
2. **Trigger** — what initiates the flow (actor action, system event, time-based trigger)
3. **Primary actor** — ACT-NNN from actors-and-personas.md
4. **Secondary actors** — other ACT-NNN or SYS-NNN involved
5. **Pre-conditions** — what must be true for the flow to start
6. **Steps** — numbered, one action per step; reference actors by ACT-NNN; note system responses
7. **Decision points** — branch conditions, reference BR-NNN rules where applicable
8. **Alternative paths** — only significant branches; minor exceptions go in BDD
9. **Post-conditions / outcomes** — observable system state after the flow completes
10. **UC sources** — UC-NNN references that contribute to this flow

### Step 3 — Add Mermaid flow diagrams

For each PF-NNN, add a compact `flowchart LR` or `flowchart TD` Mermaid diagram showing the main actor actions, system responses, and decision points. Keep diagrams at business flow summary level — not implementation level.

Mermaid syntax rules:
- Node IDs use only alphanumeric characters and underscores (no hyphens, no dots, no brackets)
- Quote node labels that contain parentheses, colons, or special characters: `A["Label (with parens)"]`
- No subgraph nesting beyond one level
- Every node must be reachable from the start node

### Step 4 — Write the artifact

Use the artifact template at `.brs2spec2/artifact-templates/process-flows.md`. Preserve all headings. Set `Status: Draft`.

## Output requirements

The artifact must contain:
- Metadata table with Status, Initiative ID, and creation date
- PF-NNN catalog table (ID, Name, Primary Actor, Trigger, Outcome, UC Sources)
- One full flow description per PF-NNN with all required fields
- One Mermaid diagram per PF-NNN
- Coverage note confirming every major end-to-end journey has at least one flow

## Done criteria

- [ ] Every major end-to-end business journey has a PF-NNN
- [ ] Every PF-NNN references ACT-NNN actors from actors-and-personas.md (not invented names)
- [ ] Decision points reference BR-NNN rules where applicable
- [ ] Mermaid diagrams are syntactically valid (alphanumeric/underscore node IDs, quoted labels with special chars)
- [ ] No use-case detail duplicated — flows stay at the cross-UC journey level
- [ ] No implementation details leaked into flows (flows describe WHAT, not HOW)
- [ ] `Status: Draft` in the Metadata table
- [ ] Result file written with `status: pass` and `artifacts_written` listing `business-analysis/process-flows.md`

## Stop conditions

- If `use-cases/` folder is missing or empty, stop and report the blocker — process flows cannot be synthesized without stable use-case specs.
- If `actors-and-personas.md` is missing, proceed using role names from UC-NNN files and flag for later ID alignment.
- If use cases are not mature enough to synthesize reliable flows, produce a partial artifact and explicitly state what is still unstable.
- Do not duplicate content already in UC-NNN files.
- Do not invent flows not supported by the use cases.
