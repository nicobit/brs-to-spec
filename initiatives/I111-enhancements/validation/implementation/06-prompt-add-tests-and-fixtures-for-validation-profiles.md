# Prompt 06 - Add Tests And Fixtures For Validation Profiles

## Goal

Make the validation standard durable by adding tests and fixtures that prove the
profile system works and prevents regression.

## Files to modify

- `.b2s/tests/test_engine_runtime.py`
- `.b2s/tests/test_engine_fixtures.py`
- `.b2s/tests/test_engine_maintenance.py` if helpful
- add or extend fixtures under `.b2s/tests/fixtures/`

## Required work

Add tests for:

- profile dispatch selection
- critical artifact rejection when validation coverage is missing
- placeholder `analytical-review` failure
- valid populated `analytical-review` success
- continued success of existing good fixtures

Add fixtures representing:

- placeholder architecture review
- minimally valid architecture review
- under-classified critical action configuration, if practical

## Minimum framework assertions

- human-gated critical artifacts do not pass as non-empty placeholders
- profile metadata is actually used by the engine
- dedicated validators and profile validators coexist safely

## Constraints

- keep tests deterministic
- avoid brittle wording-sensitive assertions where structure is enough
- prefer small focused fixtures

## Verification

Verify that:

1. the new tests fail without the validation-profile changes
2. the full targeted test suite passes after the implementation
3. future regressions in validation coverage are caught automatically
