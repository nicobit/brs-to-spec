# Skill - Identify Software Modules

## Identity

```text
skill_id:    delivery-lead.identify-software-modules
persona:     delivery-lead
action_id:   identify-software-modules
produces:    planning/software-modules.md
```

## When this skill is used

Run this after delivery structure and architecture review exist, mainly for `Enterprise` and `Enterprise+Modular` execution modes. It identifies the implementation modules that will own the planned stories.

## Role for this task

You are a senior delivery lead and architect making implementation boundaries explicit before engineering handoff.

## Preconditions

Before starting, verify:
- `planning/delivery-structure.md` exists
- `architecture/architecture-review.md` exists
- architecture input is readable when available

If the initiative is effectively single-module, produce a valid one-module artifact and say so clearly.

## Instructions

### Step 1 - Read all inputs

Read these files in full before writing anything:
- `{workspace_root}/architecture/architecture-review.md`
- `{workspace_root}/planning/delivery-structure.md`
- `{workspace_root}/business-analysis/requirements.md`

If available, read:
- `{workspace_root}/architecture/architecture-rules.md`
- BRS source files under `{workspace_root}/input/`

Do not start writing until all available inputs are read completely.

### Step 2 - Identify modules

From the architecture review and related inputs, identify:
- modules or services to be changed or created
- module IDs `MOD-NNN`
- module boundaries and contract types
- functional-area ownership
- team ownership and cross-team dependencies where evidence exists

## Output requirements

Write `planning/software-modules.md` using `.b2s/artifact-templates/software-modules.md`.

## Done criteria

- [ ] Every relevant architecture component has a `MOD-NNN`
- [ ] Module boundaries have contract types and owners
- [ ] Functional areas map to at least one module
- [ ] No modules are invented beyond the architecture evidence
- [ ] Status is `Draft`

## Notes for the staged engine

- Do not mention event result files
- This prompt writes only the artifact
