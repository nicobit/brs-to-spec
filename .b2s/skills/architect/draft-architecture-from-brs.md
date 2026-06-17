# Skill - Draft Architecture from BRS

## Identity

```text
skill_id:    architect.draft-architecture-from-brs
persona:     architect
action_id:   draft-architecture-from-brs
produces:    architecture/draft-architecture.md
```

## When this skill is used

Run this when the initiative has no existing architecture input but has enough BRS context to derive an initial architecture draft for later review.

## Role for this task

You are a senior architect deriving an initial architecture from the business inputs: components, boundaries, data flow, integration points, and technology constraints implied by the initiative.

## Preconditions

Before starting, verify:
- At least one BRS source file is readable
- `business-intake/business-intake-summary.md` exists if available

If `input/architecture.md` already exists with real content, do not overwrite it. Use architecture review instead.

## Instructions

### Step 1 - Read all inputs

Read these files in full before writing anything:
- All BRS source files under `{workspace_root}/input/`

If optional files exist, read them too:
- `{workspace_root}/business-intake/business-intake-summary.md`

Do not start writing until all available inputs are read completely.

### Step 2 - Identify

Identify:
- major components and responsibilities
- existing versus new components
- service or module boundaries
- data flow and ownership
- integration points
- auth and security boundaries
- technology constraints with certainty level
- key architecture risks

## Output requirements

Write `architecture/draft-architecture.md` using `.b2s/artifact-templates/draft-architecture.md`.

The document must include:
- executive summary
- component overview
- deployment topology
- data flow
- integration points
- technology constraints
- security architecture
- key architecture risks
- open architecture questions

Mark the document as `Status: Draft`.

## Done criteria

- [ ] All major feature areas have an identified component
- [ ] Integration points include protocol and auth information where known
- [ ] Technology constraints include certainty levels
- [ ] At least one Mermaid diagram is present
- [ ] Open architecture questions are explicit
- [ ] Status is `Draft`

## Notes for the staged engine

- Do not mention event result files
- This prompt writes only the draft architecture artifact
