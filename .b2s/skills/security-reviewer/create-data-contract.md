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

Read every file listed in `{resolved_required_inputs}` in full before writing anything.

If `{resolved_optional_inputs}` is not empty, read those files too.
Read every policy file listed in `{resolved_policy_inputs}` in full before writing.

Do not start writing until all available inputs are read completely.

### Step 2 - Document each new or changed data asset with classification, schema, PII handling, encryption, retention, access control, flow, and migration approach.

Apply the policy context from `{resolved_policy_inputs}`:
- make security controls and access boundaries explicit
- preserve regulatory and retention obligations from the source context
- do not leave PII handling implicit

## Output requirements

Write `quality-gates/data-contract.md` using `.b2s/artifact-templates/data-contract.md`.

## Done criteria

- [ ] Every new or changed data asset has a `DA-NNN`
- [ ] PII handling is explicit
- [ ] Migration and access control are documented
- [ ] Status is `In progress`
