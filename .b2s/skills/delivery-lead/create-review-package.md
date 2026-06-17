# Skill - Create Review Package

## Identity

```text
skill_id:    delivery-lead.create-review-package
persona:     delivery-lead
action_id:   create-review-package
produces:    review-package/
```

## When this skill is used

Run this after handoff exists or whenever a stakeholder-friendly assembled package is needed.

## Preconditions

Before starting, verify:
- `business-intake/business-intake-summary.md` exists
- `planning/delivery-structure.md` exists
- `architecture/architecture-review.md` exists

## Instructions

### Step 1 - Read all inputs

Read these files in full before writing anything:
- `{workspace_root}/business-intake/business-intake-summary.md`
- `{workspace_root}/planning/delivery-structure.md`
- `{workspace_root}/architecture/architecture-review.md`

Do not start writing until all available inputs are read completely.

### Step 2 - Assemble the review package from existing artifacts, marking any missing source sections clearly rather than inventing them.

## Output requirements

Follow the package structure described in `.b2s/artifact-templates/review-package.md`.
