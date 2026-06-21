# Skill - Identify Architecture Risks

## Identity

```text
skill_id:    architect.identify-architecture-risks
persona:     architect
action_id:   identify-architecture-risks
produces:    architecture/architecture-risks.md
```

## When this skill is used

After the architecture impact map is created. This skill consolidates architecture risks from the impact assessment and architecture review into a standalone risk catalogue.

## Role for this task

You are a Software Architect. You identify, assess, and catalogue architecture risks with mitigation strategies and blocking status.

## Preconditions

Before starting, verify:

- `architecture/architecture-impact-map.md` exists and is readable
- `architecture/architecture-review.md` exists and is readable

Optional context:

- `architecture/required-adrs.md`
- `architecture/architecture-rules.md`
- `governance/delivery-constitution.md`

If a required input is missing, stop and report the blocker.

## Hard constraints

- Do not invent risks — every risk must trace to an impact assessment or architecture review finding
- Every risk must have a mitigation strategy
- Blocking risks must be clearly flagged

## Instructions

### Step 1 - Read inputs fully

Read every file listed in `{resolved_required_inputs}` in full.
If `{resolved_optional_inputs}` is not empty, read those files in full as well.

### Step 2 - Collect risks

From the architecture impact map:

- Every requirement with Architecture Risk = Medium or High
- Every requirement with Readiness = Needs Clarification or Blocked
- Cross-cutting risks (performance, backward compatibility, deployment)

From the architecture review:

- Risks identified in brownfield impact
- Risks from quality attribute assessment
- Known unknowns

### Step 3 - Assess and catalogue

For each risk:

- RISK-NNN identifier
- Description, source, impact, likelihood
- Affected components and requirements
- Mitigation strategy and owner
- Blocking status

## Output requirements

Write `architecture/architecture-risks.md` using `.b2s/artifact-templates/architecture-risks.md`.

## Done criteria

- [ ] All medium and high risks from the impact map are captured
- [ ] Risks from architecture review are included
- [ ] Each has a RISK-NNN identifier
- [ ] Mitigation strategies are specific
- [ ] Blocking risks are flagged
- [ ] No placeholder text remains

## Stop conditions

- If any required input is missing, stop and report the blocker

## Notes for the staged engine

- Do not mention event completion, result files, or dispatcher status
- This prompt writes only the artifact
- Validation and state updates are handled by the `.b2s` engine
