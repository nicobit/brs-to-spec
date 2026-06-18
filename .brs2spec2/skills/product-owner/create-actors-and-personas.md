# Skill — Create Actors and Personas

## Identity

| Field | Value |
|---|---|
| skill_id | po-create-actors-and-personas |
| persona | product-owner |
| event_types | CREATE_ACTORS_AND_PERSONAS |
| produces | business-analysis/actors-and-personas.md |

## When this skill is used

After `CREATE_USE_CASE_DIAGRAM` completes and both `business-analysis/requirements.md` and `business-analysis/use-cases.puml` exist. The use-case diagram is the authoritative actor source — actor IDs assigned here must match the actor nodes in the diagram. The output (ACT-NNN / SYS-NNN IDs) feeds process flows and use-case specs.

## Role for this task

You are a senior business analyst identifying every human actor and every system that interacts with the initiative's scope, aligning actor names and IDs with the use-case diagram, and characterizing their goals, permissions, and interaction patterns.

## Prerequisites check

Before starting, verify:
- [ ] `business-analysis/requirements.md` exists and has FR-NNN rows
- [ ] `business-analysis/use-cases.puml` exists and lists actor nodes

Optional inputs (read if available, do not block if missing):
- [ ] `business-analysis/business-rules.md` (authorization rules BR-NNN for permission characterization)
- [ ] `input/brs.md` (or `input/brs/*.md`) — cross-check for additional actors not yet in the diagram

If any required input is missing, stop and report what is absent.

## Instructions

### Step 1 — Extract actors from use-case diagram

Read `business-analysis/use-cases.puml` first. Every `actor` node in the diagram is a human actor that must have an ACT-NNN entry. Every `rectangle` boundary that represents an external system is a SYS-NNN.

Also scan `business-analysis/requirements.md` for:
- External systems referenced in FR-NNN rows not yet visible in the diagram
- Automated or system-internal actors implied by requirements

### Step 2 — Assign IDs and categorize

Assign IDs:
- Human actors: ACT-001, ACT-002, ...
- External systems: SYS-001, SYS-002, ...
- Automated actors (internal): ACT-SYS-001

For each:
1. Name — use the exact label from `use-cases.puml` for human actors; use the BRS name for systems
2. Type (Human / External System / Internal Automated)
3. Primary goal in this initiative's scope
4. Permissions and restrictions — derived from BR-NNN authorization rules where available
5. Source references (UC-NNN, FR-NNN)

### Step 3 — Document interaction patterns

For each actor, note:
- Which use cases they participate in (from use-cases.puml)
- What they can initiate, read, modify, approve, or reject
- What events or notifications they receive
- What they explicitly cannot do (derived from authorization rules)

### Step 4 — Build interaction matrix

Create a table showing which actors interact with which use cases or system boundaries. Rows = actors; columns = UC-NNN IDs.

### Step 5 — Write the artifact

Use the artifact template at `.brs2spec2/artifact-templates/actors-and-personas.md`. Preserve all headings.

Set `Status: Draft` in the Metadata table.

## Output requirements

The artifact must contain:
- Metadata table with Status, Initiative ID, and creation date
- ACT-NNN catalog for all human actors
- SYS-NNN catalog for all external and automated systems
- Interaction matrix showing which actors interact with which use cases and system boundaries
- Permission notes derived from BR-NNN or requirements.md (not invented)

## Done criteria

- [ ] Every actor in `use-cases.puml` has an ACT-NNN entry with a matching name
- [ ] Every external system in requirements.md has a SYS-NNN entry
- [ ] All ACT-NNN and SYS-NNN IDs are stable — these are used consistently by process-flows and use-case-specs
- [ ] Permissions and restrictions trace to BR-NNN or requirements.md source
- [ ] No actors invented beyond what requirements.md and use-cases.puml support
- [ ] `Status: Draft` in the Metadata table
- [ ] Result file written with `status: pass` and `artifacts_written` listing `business-analysis/actors-and-personas.md`

## Stop conditions

- If `requirements.md` or `use-cases.puml` is missing, stop and report the blocker.
- If actor naming is inconsistent across sources, choose the clearest stable label from use-cases.puml and note the aliasing.
- Do not invent actor roles or systems not present in requirements.md or use-cases.puml.
