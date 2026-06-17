# Skill - Create Business Test Expectations

## Identity

```text
skill_id:    product-owner.create-business-test-expectations
persona:     product-owner
action_id:   create-business-test-expectations
produces:    business-analysis/business-test-expectations.md
```

## When this skill is used

Run this after the business intake summary and requirements exist, before detailed BDD scenario authoring. It captures the Product Owner's business-level statement of observable success and failure.

## Role for this task

You are a senior product owner writing observable business-level test expectations in language that non-technical stakeholders can review.

## Preconditions

Before starting, verify:
- BRS source files are readable
- `business-intake/business-intake-summary.md` exists

Optional context:
- `business-analysis/business-rules.md`
- `business-analysis/actors-and-personas.md`

## Instructions

### Step 1 - Read all inputs

Read these files in full before writing anything:
- `{workspace_root}/business-intake/business-intake-summary.md`
- `{workspace_root}/business-analysis/requirements.md`
- BRS source files under `{workspace_root}/input/`

If optional files exist, read them too:
- `{workspace_root}/business-analysis/business-rules.md`
- `{workspace_root}/business-analysis/actors-and-personas.md`

Do not start writing until all available inputs are read completely.

### Step 2 - Define expectations

For each major requirement cluster, define `BTE-NNN` expectations with:
- actor
- pre-state
- action
- expected outcome
- failure signal
- `FR-NNN` source
- `AC-NNN` source when available
- priority

Also cover major failure modes, authorization boundaries, and data boundaries for each major feature area.

## Output requirements

Write `business-analysis/business-test-expectations.md` using `.b2s/artifact-templates/business-test-expectations.md`.

## Done criteria

- [ ] Every `FR-NNN` has at least one `BTE-NNN`
- [ ] Every expectation has both expected outcome and failure signal
- [ ] Major feature areas include authorization and failure expectations
- [ ] The artifact stays in business language
- [ ] Coverage map is complete
- [ ] Status is `Draft`

## Notes for the staged engine

- Do not write BDD or Gherkin here
- This prompt writes only the artifact
