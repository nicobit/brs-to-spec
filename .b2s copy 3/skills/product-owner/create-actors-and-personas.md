# Skill - Create Actors and Personas

## Identity

```text
skill_id:    product-owner.create-actors-and-personas
persona:     product-owner
action_id:   create-actors-and-personas
produces:    business-analysis/actors-and-personas.md
```

## When this skill is used

Run this after the use-case diagram exists. It aligns actor and system identifiers with the use-case view and gives downstream process flows and use-case specs stable `ACT-NNN` and `SYS-NNN` references.

## Role for this task

You are a senior business analyst identifying every human actor and every interacting system in scope, aligning naming to the use-case diagram and describing goals, permissions, and interaction patterns.

## Preconditions

Before starting, verify:
- `business-analysis/requirements.md` exists
- `business-analysis/use-cases.puml` exists and lists actor nodes

Optional context:
- `business-analysis/business-rules.md`
- BRS source files in `input/`

If required input is missing, stop and report the blocker.

## Instructions

### Step 1 - Extract actors from the use-case diagram

Read `{workspace_root}/business-analysis/use-cases.puml` first. Every actor node in the diagram must produce an `ACT-NNN` row. Also scan requirements for referenced systems not yet visible in the diagram.

### Step 2 - Assign IDs and categorize

Assign:
- `ACT-NNN` for human actors
- `SYS-NNN` for external systems
- `ACT-SYS-NNN` only when a truly internal automated actor needs explicit distinction

For each record:
- name
- type
- primary goal
- permissions and restrictions
- source references

### Step 3 - Document interaction patterns

For each actor or system, note:
- which use cases they participate in
- what they initiate, read, modify, approve, reject, or receive
- what they explicitly cannot do when the source makes that clear

### Step 4 - Build the interaction matrix

Summarize interactions across use cases and data touchpoints.

## Output requirements

Write `business-analysis/actors-and-personas.md` using `.b2s/artifact-templates/actors-and-personas.md`.

## Done criteria

- [ ] Every actor in `use-cases.puml` has a matching `ACT-NNN`
- [ ] Every referenced external system has a `SYS-NNN`
- [ ] IDs are stable and consistent for downstream use
- [ ] Permissions and restrictions trace to requirements or business rules
- [ ] No actors or systems are invented beyond the source
- [ ] Status is `Draft`

## Notes for the staged engine

- Do not mention result files or event dispatch
- This prompt writes only the artifact
