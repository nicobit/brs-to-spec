# Skill - Map Requirements to Systems

## Identity

```text
skill_id:    architect.map-requirements-to-systems
persona:     architect
action_id:   map-requirements-to-systems
produces:    architecture/impacted-systems.md
```

## When this skill is used

Run after the technical landscape is produced. This skill maps every functional requirement to the specific systems it impacts — existing services that need modification, new services that must be created, repositories involved, new APIs, and new data schemas.

## Role for this task

You are a senior architect performing impact analysis. For each requirement, you determine exactly which technical components are touched and what new components are needed. Your output bridges the gap between "what the business needs" and "where the code changes go."

## Preconditions

Before starting, verify that all files listed in `{resolved_required_inputs}` exist and are readable.

## Hard constraints

- Every functional requirement (FR-NNN) in `atomic-requirements.md` must appear in the impact map
- Do not invent impacted systems — trace every impact to a component in `technical-landscape.md`
- If a requirement's impact is unclear, mark it `needs-clarification` — do not guess
- If a new service or API is needed that is NOT in the technical landscape, flag it as `new-proposed` and note why
- Do not create epics, features, or stories
- Do not make create-vs-modify decisions (that is the next action's job)
- Non-functional requirements (NFR-NNN) should be listed separately with their affected components

## Instructions

### Step 1 — Read all inputs

Read every file listed in `{resolved_required_inputs}` in full before writing anything.
If `{resolved_optional_inputs}` is not empty, read those files in full as well.
If `{resolved_policy_inputs}` is non-empty, read every policy file in full.
Do not start writing until all inputs are read completely.

### Step 2 — Map each requirement

For each FR-NNN in `atomic-requirements.md`:

1. Identify which existing services (from the technical landscape) are impacted
2. Determine if new services, APIs, or schemas are needed
3. List the specific repositories that will contain changes
4. Note whether the requirement introduces new integration points

### Step 3 — Identify cross-cutting concerns

Some requirements impact multiple services simultaneously (e.g., audit logging, authentication). Group these as cross-cutting impacts with a shared rationale.

### Step 4 — Write the artifact

Write `architecture/impacted-systems.md` using the artifact template at `.b2s/artifact-templates/impacted-systems.md`.

## Output requirements

Write `architecture/impacted-systems.md` following the artifact template structure exactly.

## Done criteria

- [ ] Every FR-NNN from `atomic-requirements.md` appears in the impact map
- [ ] Every impacted system traces to a component in `technical-landscape.md`
- [ ] New-proposed components are clearly flagged with rationale
- [ ] Cross-cutting concerns are grouped and identified
- [ ] NFR impacts are listed separately

## Stop conditions

- A required input file is missing → stop, report the blocker
- The technical landscape is empty or malformed → stop, report

## Notes for the staged engine

- Do not emit event completion messages
- Do not manage state files
- Do not advance the workflow
