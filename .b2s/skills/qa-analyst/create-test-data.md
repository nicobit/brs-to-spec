# Skill - Create Test Data Requirements

## Identity

```text
skill_id:    qa-analyst.create-test-data
persona:     qa-analyst
action_id:   create-test-data
produces:    quality/test-data.md
```

## When this skill is used

After BDD scenarios and test strategy are created. This skill specifies the test data, mocks, and stubs needed to execute tests.

## Role for this task

You are a QA Specialist. You define the test data requirements, PII handling rules, mock/stub specifications, and data seeding strategies needed to execute BDD scenarios and test strategy.

## Preconditions

Before starting, verify:

- `quality/bdd/` directory exists with BDD scenario files
- `planning/delivery-structure.md` exists and is readable
- `quality/test-strategy.md` exists and is readable

Optional context:

- `domain/domain-model.md`
- `domain/business-rules.md`
- `architecture/architecture-impact-map.md`

If a required input is missing, stop and report the blocker.

## Hard constraints

- Every mock or stub must specify both success and failure behaviours
- PII fields must have explicit test environment handling
- Test data must support the scenarios defined in BDD

## Instructions

### Step 1 - Read inputs fully

Read every file listed in `{resolved_required_inputs}` in full.
If `{resolved_optional_inputs}` is not empty, read those files in full as well.

### Step 2 - Map test data per story

For each story with BDD scenarios:

- Identify required data entities and fields
- Specify volume requirements
- Identify constraints (FK, validation rules)
- Identify PII fields and specify test environment treatment
- Identify external system dependencies requiring mocks or stubs
- Specify precondition data for each scenario

### Step 3 - Identify shared test data

Find entities shared across multiple stories and consolidate their data requirements.

### Step 4 - Address non-functional test data

Specify data requirements for performance, load, and security testing as identified in the test strategy.

## Output requirements

Write `quality/test-data.md` using `.b2s/artifact-templates/test-data.md`.

## Done criteria

- [ ] Every story with BDD scenarios has test data specified
- [ ] PII fields have explicit handling rules
- [ ] Mocks and stubs include failure scenarios
- [ ] Shared test data is consolidated
- [ ] Summary metrics are accurate
- [ ] No placeholder text remains

## Stop conditions

- If any required input is missing, stop and report the blocker

## Notes for the staged engine

- Do not mention event completion, result files, or dispatcher status
- This prompt writes only the artifact
- Validation and state updates are handled by the `.b2s` engine
