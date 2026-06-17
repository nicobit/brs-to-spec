# Skill - Create Data Contract

## Identity

```text
skill_id:    security-reviewer.create-data-contract
persona:     security-reviewer
action_id:   create-data-contract
produces:    quality-gates/data-contract.md
```

## When this skill is used

Run this only when the readiness check explicitly triggers the data contract gate.

## Preconditions

Before starting, verify:
- `engineering-readiness/readiness-check.md` marks Data Contract as triggered
- BRS source files are readable
- `architecture/architecture-review.md` exists
- `business-analysis/business-rules.md` exists
- `business-analysis/entity-model.md` exists when available

## Instructions

### Step 1 - Read all inputs

Read these files in full before writing anything:
- `{workspace_root}/architecture/architecture-review.md`
- `{workspace_root}/business-analysis/business-rules.md`

If optional files exist, read them too:
- `{workspace_root}/business-analysis/entity-model.md`

Do not start writing until all available inputs are read completely.

### Step 2 - Document each new or changed data asset with classification, schema, PII handling, encryption, retention, access control, flow, and migration approach.

## Output requirements

Write `quality-gates/data-contract.md` using `.b2s/artifact-templates/data-contract.md`.

## Done criteria

- [ ] Every new or changed data asset has a `DA-NNN`
- [ ] PII handling is explicit
- [ ] Migration and access control are documented
- [ ] Status is `In progress`
