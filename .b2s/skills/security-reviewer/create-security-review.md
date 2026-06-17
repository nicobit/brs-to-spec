# Skill - Create Security Review

## Identity

```text
skill_id:    security-reviewer.create-security-review
persona:     security-reviewer
action_id:   create-security-review
produces:    quality-gates/security-review.md
```

## When this skill is used

Run this only when the readiness check explicitly triggers the security review gate.

## Preconditions

Before starting, verify:
- `engineering-readiness/readiness-check.md` marks Security Review as triggered
- BRS source files are readable
- `architecture/architecture-review.md` exists
- `architecture/architecture-rules.md` exists

## Instructions

### Step 1 - Read all inputs

Read these files in full before writing anything:
- `{workspace_root}/architecture/architecture-review.md`
- `{workspace_root}/business-analysis/requirements.md`
- All BRS source files under `{workspace_root}/input/`

If optional files exist, read them too:
- `{workspace_root}/architecture/architecture-rules.md`
- `{workspace_root}/business-analysis/business-rules.md`

Do not start writing until all available inputs are read completely.

### Step 2 - Assess
- authorization
- authentication
- input validation
- sensitive data handling
- audit trail
- integration security

Every finding must include evidence, risk, recommendation, owner, and required-before timing.

## Output requirements

Write `quality-gates/security-review.md` using `.b2s/artifact-templates/security-review.md`.

## Done criteria

- [ ] All six security domains are assessed
- [ ] Findings are actionable and evidence-based
- [ ] Accepted risks have owners and justification
- [ ] Status is `In progress`
