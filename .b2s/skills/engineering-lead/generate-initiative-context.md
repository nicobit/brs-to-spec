# Skill - Generate Initiative Context

## Identity

```text
skill_id:    engineering-lead.generate-initiative-context
persona:     engineering-lead
action_id:   generate-initiative-context
produces:    engineering-readiness/initiative-context.md
```

## When this skill is used

Run this once the readiness decision is approved. It produces the compact binding context file loaded first by downstream implementation and review agents.

## Preconditions

Before starting, verify:
- `engineering-readiness/readiness-check.md` exists and is approved
- `architecture/architecture-rules.md` exists
- `architecture/architecture-review.md` exists

## Instructions

### Step 1 - Read all inputs

Read these files in full before writing anything:
- `{workspace_root}/engineering-readiness/readiness-check.md`
- `{workspace_root}/architecture/architecture-rules.md`
- `{workspace_root}/architecture/architecture-review.md`
- `{resolved_optional_inputs}` — technical-specification artifacts when workflow type is `technical-spec-modular`

Do not start writing until all available inputs are read completely.

### Step 1b - Apply integration specs when present

If `{workspace_root}/technical-specifications/integrations/` exists and contains files:
- Read each integration spec.
- Use the integration map section of `initiative-context.md` to list each external system with its protocol, timeout, retry policy, and fallback behaviour from the integration spec.
- Do not summarise from architecture-review alone when integration specs provide a more detailed map.

If `{workspace_root}/technical-specifications/api/exposed/` exists and contains files:
- Note the contract mode (`product`, `internal`, or `coordinated`) in the initiative context so downstream consumers know how to treat the API surface.

### Step 2 - Extract context

Extract only binding constraints, active gates, governed boundaries, rollback and regression sensitivity, open risks, and carried-forward context. Copy `AR-NNN` rules verbatim rather than paraphrasing.

## Output requirements

Write `engineering-readiness/initiative-context.md` using `.b2s/artifact-templates/initiative-context.md`.

## Done criteria

- [ ] `AR-NNN` rules are verbatim
- [ ] Technology constraints come from evidence
- [ ] Triggered gates are listed
- [ ] Carried-forward context is populated or explicitly marked none
- [ ] AI model version is populated
