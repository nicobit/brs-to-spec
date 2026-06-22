# Prompt 03 - Introduce Named Validation Rules

## Context

The framework already validates artifacts, but the validation model is still too
opaque for a policy-driven action system. This prompt introduces named reusable
validation rules so actions can declare what "good" means more explicitly.

## Step 1 - Read the validation implementation

Read these files in full:

- `.b2s/scripts/b2s_engine/validation.py`
- `.b2s/workflow/stage-actions.yaml`

Inspect how `validation_profile`, `required_sections`, `must_include`, and any
other validation-related fields are currently applied.

## Step 2 - Create a rule catalog structure

Create a rule catalog format in code for reusable checks such as:

- `requirement_has_id`
- `requirement_is_testable`
- `architecture_lists_impacted_systems`
- `architecture_lists_constraints`
- `architecture_lists_risks`
- `readiness_has_decision`
- `contract_has_schema_definitions`

Start with artifact types that already exist clearly in the current workflow:

- requirements
- architecture review
- readiness outputs
- API/data/event contract outputs

Do not introduce story-specific rules in the first pass unless a first-class
story action and canonical story artifact already exist in the core workflow.
The catalog must support multiple artifact types.

## Step 3 - Wire action-declared rules into validation

Support `validation_rules.required` and `validation_rules.optional` from the
action contract.

Validation behavior:

- required rule failures make validation fail
- optional rule failures should be reported but not fail validation unless the
  framework already has a suitable severity model
- existing validation profiles must still run

## Step 4 - Improve validator output

Update `.b2s/tmp/current-validation.yaml` output structure if needed so it can
report:

- which named rules ran
- which failed
- failure messages tied to rule names

Keep the output compact and machine-usable.

## Step 5 - Seed rules into a few actions

Update representative actions in `stage-actions.yaml` to use the rule catalog.

Good candidates:

- `create-requirements`
- `review-initial-architecture`
- `check-engineering-readiness`
- one contract-related action such as API, data, or event contract

## Step 6 - Verify

Add or update tests around rule execution and output formatting.

## Done criteria

- [ ] validation supports named required rules
- [ ] validator output reports rule-level results
- [ ] current validation profiles still work
- [ ] several real actions use the new rule catalog
