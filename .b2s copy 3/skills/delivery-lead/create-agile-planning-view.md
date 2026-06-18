# Skill - Create Agile Planning View

## Identity

```text
skill_id:    delivery-lead.create-agile-planning-view
persona:     delivery-lead
action_id:   create-agile-planning-view
produces:    perspectives/agile-planning/gitlab-planning-view.md
```

## When this skill is used

Run this after delivery structure exists, optionally after increments. It creates a planning projection, not a new source of truth.

## Preconditions

Before starting, verify:
- `planning/delivery-structure.md` exists
- `business-intake/business-intake-summary.md` exists

## Instructions

### Step 1 - Read all inputs

Read these files in full before writing anything:
- `{workspace_root}/planning/delivery-structure.md`
- `{workspace_root}/business-intake/business-intake-summary.md`

Do not start writing until all available inputs are read completely.

### Step 2 - Project epics, features, stories, and increments into planning-tool language, link gate artifacts, and point engineers back to the true handoff artifacts.

## Output requirements

Write `perspectives/agile-planning/gitlab-planning-view.md` using `.b2s/artifact-templates/agile-planning-view.md`.
