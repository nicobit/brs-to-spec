# Prompt 05 - Add Tests for Placeholder Support

## Context

Placeholder support changes both engine output and prompt execution behavior, so
it needs focused tests.

Before making changes, read these files in full:

- `.b2s/tests/test_engine_runtime.py`
- `.b2s/tests/test_engine_fixtures.py`
- `.b2s/scripts/b2s_engine/inputs.py`
- any tests covering prompt or workflow execution helpers

## Goal

Add tests for the prompt placeholder contract and the initial migrated actions.

## Required coverage

1. `collect-inputs` writes `prompt_placeholders`
2. `prompt_placeholders.required_inputs` and `optional_inputs` reflect declared
   patterns
3. `prompt_placeholders.resolved_required_inputs` and
   `resolved_optional_inputs` reflect flattened resolved paths
4. `primary_output` and `secondary_outputs` are populated correctly
5. placeholder rendering fails clearly for unknown placeholders
6. migrated prompts render correctly for:
   - `create-business-intake-summary`
   - `create-delivery-structure`

## Fixture recommendations

Use representative fixtures that include:

- fixed required file inputs
- wildcard optional inputs
- at least one directory input
- empty secondary outputs

## Done criteria

- [ ] Engine tests cover placeholder generation
- [ ] Rendering tests cover placeholder substitution behavior
- [ ] Migrated prompt coverage exists for the first selected actions
- [ ] Existing tests remain green
