# Skill - Create Compact Handoff

## Identity

```text
skill_id:    engineering-lead.create-compact-handoff
persona:     engineering-lead
action_id:   create-compact-handoff
produces:    handoff/compact-handoff-summary.md
```

## When this skill is used

Run this only after the real handoff package already exists. It creates a lightweight summary and does not replace the real handoff.

## Preconditions

Before starting, verify:
- the real handoff exists under `specs/` or `standalone-delivery/`
- `engineering-readiness/readiness-check.md` exists

## Instructions

### Step 1 - Read all inputs

Read these files in full before writing anything:
- `{workspace_root}/engineering-readiness/readiness-check.md`
- All files under `{workspace_root}/specs/` or `{workspace_root}/standalone-delivery/` (whichever exists)

Do not start writing until all available inputs are read completely.

### Step 2 - Summarize

Summarize:
- initiative and mode metadata
- binding AR rules
- gate status
- story counts
- accepted risks
- pointers to the real handoff artifacts

## Output requirements

Write `handoff/compact-handoff-summary.md` using `.b2s/artifact-templates/compact-handoff.md`.
