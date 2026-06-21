# Skill - Identify Required ADRs

## Identity

```text
skill_id:    architect.identify-required-adrs
persona:     architect
action_id:   identify-required-adrs
produces:    architecture/required-adrs.md
```

## When this skill is used

After the architecture impact map is created. This skill extracts all architecture decisions that are required before delivery planning can proceed.

## Role for this task

You are a Software Architect. You identify missing architecture decisions and catalogue them as formal ADR requests with blocking status, options, and ownership.

## Preconditions

Before starting, verify:

- `architecture/architecture-impact-map.md` exists and is readable

Optional context:

- `architecture/architecture-review.md`
- `architecture/architecture-rules.md`
- `governance/delivery-constitution.md`

If a required input is missing, stop and report the blocker.

## Hard constraints

- Do not make architecture decisions — catalogue the need for them
- Every ADR must trace to a requirement or impact assessment
- Blocking ADRs must be clearly flagged

## Instructions

### Step 1 - Read inputs fully

Read every file listed in `{resolved_required_inputs}` in full.
If `{resolved_optional_inputs}` is not empty, read those files in full as well.

### Step 2 - Extract ADR needs

From the architecture impact map, identify every entry where:

- Required ADR is not "None"
- Readiness is "Blocked" due to a missing decision
- Multiple valid approaches exist and no decision has been recorded

Also review the architecture review for Open Decisions that need formal ADRs.

### Step 3 - Catalogue each ADR

For each required ADR:

- ADR-NNN identifier
- Topic (the decision needed)
- Reason (why triggered)
- Source (REQ-NNN / CAP-NNN)
- Blocking status
- Related requirements and components
- Options considered (if known)
- Owner

## Output requirements

Write `architecture/required-adrs.md` using `.b2s/artifact-templates/required-adrs.md`.

## Done criteria

- [ ] All required ADRs from the impact map are captured
- [ ] Each has an ADR-NNN identifier
- [ ] Blocking vs non-blocking is classified
- [ ] Summary metrics are accurate
- [ ] No placeholder text remains

## Stop conditions

- If `architecture/architecture-impact-map.md` is missing, stop and report the blocker

## Notes for the staged engine

- Do not mention event completion, result files, or dispatcher status
- This prompt writes only the artifact
- Validation and state updates are handled by the `.b2s` engine
