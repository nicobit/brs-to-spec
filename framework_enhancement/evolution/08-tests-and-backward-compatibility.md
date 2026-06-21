# Prompt 08 - Lock In Backward Compatibility with Tests

## Context

This evolution only succeeds if the framework remains stable for current users.
This prompt adds the tests that prove the enhancements are additive rather than
breaking.

## Step 1 - Inspect the current test layout

Read the existing engine test files under `.b2s/tests/` in full.

Identify where tests already exist for:

- action loading
- input collection
- next-step selection
- validation
- gates

## Step 2 - Add compatibility tests for old actions

Create tests that prove an old-style action record with no new metadata still:

- normalizes correctly
- resolves inputs correctly
- validates correctly
- dispatches correctly

## Step 3 - Add tests for v2 action metadata

Create tests for:

- `policy_refs` resolution
- `prompt_family` defaulting and explicit override
- `template_mode` defaulting
- named `validation_rules.required`
- fallback skill behavior when a family-specific skill is missing

## Step 4 - Add validator output tests

Assert that `current-validation.yaml` reports named rules in a stable,
machine-readable way.

## Step 5 - Add a realistic mixed-family fixture

Create one compact fixture action set that demonstrates:

- native `.b2s` business intake
- `speckit`-style requirements
- `b2s` or architecture-influenced architecture review
- `hve`-style handoff

This fixture exists to verify the orchestration layer, not the quality of the
prompt prose itself.

## Step 6 - Run the test suite

Run the relevant tests and fix regressions before finishing.

## Done criteria

- [ ] old actions are proven compatible
- [ ] new metadata is covered by tests
- [ ] mixed-family orchestration is tested
- [ ] validator rule reporting is tested
