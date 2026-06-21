# Skill - Validate FR Coverage

## Identity

```text
skill_id:    delivery-lead.validate-fr-coverage
persona:     delivery-lead
action_id:   validate-fr-coverage
produces:    planning/fr-coverage.md
```

## When this skill is used

Run after all feature story files are generated. This skill validates that every requirement from atomic-requirements.md is covered by at least one story, and produces a coverage report.

## Role for this task

You are a delivery lead validating requirement coverage. You compare the full list of requirements against the stories produced across all feature story files and report gaps.

## Preconditions

Before starting, verify:

- `requirements/atomic-requirements.md` exists and is readable
- `planning/delivery-skeleton.md` exists and is readable
- `planning/stories/` directory exists with at least one story file

Optional context:

- `domain/capability-map.md`
- `planning/epics/`

If a required input is missing, stop and report the blocker.

## Hard constraints

- Every requirement from atomic-requirements.md must appear in the coverage matrix
- Do not invent stories to fill gaps — report gaps with recommended actions
- Coverage percentage must be accurate

## Instructions

### Step 1 - Read inputs fully

Read every file listed in `{resolved_required_inputs}` in full.
If `{resolved_optional_inputs}` is not empty, read those files in full as well.
Read every file in `planning/stories/` in full.
Do not start writing until all inputs are read completely.

### Step 2 - Extract requirement list

From `atomic-requirements.md`, extract every requirement ID (FR-NNN, REQ-NNN, NFR-NNN) and its title.

### Step 3 - Scan stories for coverage

For each story file in `planning/stories/`, extract the Linked Requirements field from every story. Build a mapping: requirement → stories that cover it.

### Step 4 - Build coverage matrix

For each requirement:

- If at least one story covers it → Status: Covered
- If no story covers it → Status: **Not Covered**

For not-covered requirements, determine:

- Why it's not covered (out of scope, deferred, blocked, missing capability)
- Recommended action (add story, defer to Phase 2, escalate)

### Step 5 - Build summary views

- Coverage by Capability
- Coverage by Epic
- Gaps and Risks

### Step 6 - Calculate metrics

- Total requirements, covered, not covered, coverage percentage
- Flag if coverage is below 100%

## Output requirements

Write `planning/fr-coverage.md` using `.b2s/artifact-templates/fr-coverage.md`.

## Done criteria

- [ ] Every requirement from atomic-requirements.md appears in the matrix
- [ ] Not-covered requirements have reasons and recommended actions
- [ ] Coverage percentage is accurate
- [ ] Summary views by capability and epic are populated
- [ ] Gaps and risks are identified
- [ ] No placeholder text remains

## Stop conditions

- If `requirements/atomic-requirements.md` is missing, stop and report the blocker
- If `planning/stories/` is empty, stop and report the blocker

## Notes for the staged engine

- Do not mention event completion, result files, or dispatcher status
- This prompt writes only the artifact
- Validation and state updates are handled by the `.b2s` engine
