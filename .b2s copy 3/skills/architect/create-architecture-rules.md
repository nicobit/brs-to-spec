# Skill - Create Architecture Rules

## Identity

```text
skill_id:    architect.create-architecture-rules
persona:     architect
action_id:   create-architecture-rules
produces:    architecture/architecture-rules.md
```

## When this skill is used

Run this after the architecture review exists. It converts review constraints into stable, numbered `AR-NNN` rules for downstream engineering and handoff artifacts.

## Role for this task

You are a senior architect formalizing architectural constraints into a binding, engineering-actionable ruleset.

## Preconditions

Before starting, verify:
- `architecture/architecture-review.md` exists
- at least one BRS source file is readable
- `business-analysis/business-rules.md` exists when available for alignment

If the architecture review is missing, stop and report the blocker.

## Instructions

### Step 1 - Read all inputs

Read these files in full before writing anything:
- `{workspace_root}/architecture/architecture-review.md`
- BRS source files under `{workspace_root}/input/`

If available, read:
- `{workspace_root}/business-analysis/business-rules.md`

Do not start writing until all available inputs are read completely.

### Step 2 - Extract and normalize

Extract each binding constraint from `{workspace_root}/architecture/architecture-review.md` and normalize it into an `AR-NNN` rule.

Categories:
- Boundary
- Technology
- Data
- Security
- Integration
- Observability
- Forbidden Pattern

For each rule, include:
- rule statement
- rationale
- source
- scope

## Output requirements

Write `architecture/architecture-rules.md` using `.b2s/artifact-templates/architecture-rules.md`.

## Done criteria

- [ ] Every review constraint has an `AR-NNN`
- [ ] Every rule has rationale and source
- [ ] Forbidden patterns are explicit where applicable
- [ ] Rules are implementable and unambiguous
- [ ] No rules are invented beyond the review and source material
- [ ] Status is `Draft`

## Notes for the staged engine

- Do not mention result files or dispatcher status
- This prompt writes only the architecture rules artifact
