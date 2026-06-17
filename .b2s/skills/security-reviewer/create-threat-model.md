# Skill - Create Threat Model

## Identity

```text
skill_id:    security-reviewer.create-threat-model
persona:     security-reviewer
action_id:   create-threat-model
produces:    quality-gates/threat-model.md
```

## When this skill is used

Run this after security review when significant trust boundaries or attack surface justify a structured threat model.

## Preconditions

Before starting, verify:
- `quality-gates/security-review.md` exists
- `architecture/architecture-review.md` exists
- architecture input is readable
- BRS source files are readable

## Instructions

### Step 1 - Read all inputs

Read these files in full before writing anything:
- `{workspace_root}/architecture/architecture-review.md`
- `{workspace_root}/business-analysis/requirements.md`
- All BRS source files under `{workspace_root}/input/`
- `{workspace_root}/quality-gates/security-review.md`

If optional files exist, read them too:
- `{workspace_root}/architecture/architecture-rules.md`
- `{workspace_root}/business-analysis/business-rules.md`

Do not start writing until all available inputs are read completely.

### Step 2 - Identify trust boundaries and assess all six STRIDE categories for each. Document threats with `THR-NNN`, DREAD score, risk level, mitigation, owner, and status.

## Output requirements

Write `quality-gates/threat-model.md` using `.b2s/artifact-templates/threat-model.md`.

## Done criteria

- [ ] Every trust boundary is assessed across STRIDE
- [ ] Every threat has DREAD and mitigation
- [ ] Accepted threats are explicit
- [ ] Status is `In progress`
