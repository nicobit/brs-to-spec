# Skill - Create API Contract

## Identity

```text
skill_id:    engineering-lead.create-api-contract
persona:     engineering-lead
action_id:   create-api-contract
produces:    quality-gates/api-contract.md
```

## When this skill is used

Run this only when the readiness check explicitly triggers the API contract gate.

## Preconditions

Before starting, verify:
- `engineering-readiness/readiness-check.md` marks API Contract as triggered
- BRS source files are readable
- `architecture/architecture-review.md` exists
- `architecture/architecture-rules.md` exists
- `business-analysis/business-rules.md` exists

## Instructions

### Step 1 - Read all inputs

Read these files in full before writing anything:
- `{workspace_root}/engineering-readiness/readiness-check.md`
- `{workspace_root}/architecture/architecture-review.md`
- `{workspace_root}/architecture/architecture-rules.md`
- `{workspace_root}/business-analysis/business-rules.md`
- BRS source files under `{workspace_root}/input/`

Do not start writing until all available inputs are read completely.

### Step 2 - Enumerate endpoints

Enumerate new, changed, removed, or impacted endpoints and document auth, authorization, field-level request/response shape, error codes, idempotency, compatibility, and consumer impact.

## Output requirements

Write `quality-gates/api-contract.md` using `.b2s/artifact-templates/api-contract.md`.

## Done criteria

- [ ] Every new or changed endpoint has an `EP-NNN`
- [ ] Auth and authorization are explicit
- [ ] Schemas and error codes are concrete
- [ ] Breaking changes have migration/versioning notes
- [ ] Status is `In progress`
