# Skill - Create Traceability Matrix

## Identity

```text
skill_id:    delivery-lead.create-traceability-matrix
persona:     delivery-lead
action_id:   create-traceability-matrix
produces:    planning/traceability-matrix.md
```

## When this skill is used

Run this after delivery structure is stable. It builds the end-to-end traceability chain from requirements through business rules and acceptance criteria into story-level delivery items.

## Role for this task

You are a senior delivery lead and QA-minded reviewer assembling the full traceability matrix and surfacing any coverage gaps rather than hiding them.

## Preconditions

Before starting, verify:
- BRS source files are readable
- `planning/delivery-structure.md` exists with `F-XXX.X` story IDs
- `business-intake/business-intake-summary.md` exists

Optional context:
- `business-analysis/business-rules.md`
- `business-analysis/actors-and-personas.md`

If required input is missing, stop and report the blocker.

## Instructions

### Step 1 - Read all inputs

Read these files in full before writing anything:
- `{workspace_root}/business-analysis/requirements.md`
- `{workspace_root}/planning/delivery-structure.md`
- `{workspace_root}/business-intake/business-intake-summary.md`

If optional files exist, read them too:
- `{workspace_root}/business-analysis/business-rules.md`
- `{workspace_root}/business-analysis/actors-and-personas.md`

Do not start writing until all available inputs are read completely.

### Step 2 - Build the matrix

Build:
- an `FR -> Story` matrix
- a `Story -> Requirements` matrix
- a coverage summary
- an explicit gaps section

Every unmapped `FR-NNN`, `F-XXX.X`, `AC-NNN`, or relevant `BR-NNN` must be called out rather than skipped.

## Output requirements

Write `planning/traceability-matrix.md` using `.b2s/artifact-templates/traceability-matrix.md`.

## Done criteria

- [ ] Every `FR-NNN` is represented as mapped or explicitly excluded
- [ ] Every `F-XXX.X` story is represented
- [ ] Every `AC-NNN` appears in the matrix when available
- [ ] Coverage gaps are explicit and explained
- [ ] Status is `Draft`

## Notes for the staged engine

- Do not mention result files or event status
- This prompt writes only the artifact
