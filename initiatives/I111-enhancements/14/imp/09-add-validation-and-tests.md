# Prompt 09 - Add Validation and Tests

## Context

The parallel workflow is only safe if its new artifact families and workflow
selection behavior are validated. Technical specifications should not be added
without machine-checkable structure.

Before making changes, read these files in full:

- `.b2s/scripts/b2s_engine/validation.py`
- `.b2s/tests/test_engine_runtime.py`
- `.b2s/tests/test_engine_fixtures.py`
- `framework_enhancement/14/05-update-openspec-handoff-and-validators.md`

## Goal

Add validators and tests for the new technical-spec artifacts and for the new
workflow-type wiring.

## Required coverage

1. Artifact validation for each technical-spec family in the new workflow type.
2. Workflow-type initialization coverage:
   - selection from `.b2s/workflow-types/index.yaml`
   - copy into initiative workspace
3. Runtime coverage:
   - state field parsing
   - condition evaluation for technical-spec sequencing
4. Consumer coverage:
   - handoff can read the new paths without breaking existing behavior
5. Placeholder compatibility coverage:
   - technical-spec workflow actions expose clean input/output contracts
   - migrated consumer prompts render correctly with placeholder substitution

## Important rule

Do not validate only the easiest artifact families. If the new workflow type
creates a data spec family, it must have matching validation coverage.

Also do not assume prompt rendering is automatically correct just because the
stage-action wiring is correct. Add tests where the new workflow type depends on
placeholder-rendered prompts or consumers.

## Done criteria

- [ ] Validators exist for every canonical technical-spec artifact family
- [ ] Tests cover workflow-type registration and initialization
- [ ] Tests cover stage-action sequencing for the new workflow type
- [ ] Existing workflow types still pass their current tests
- [ ] Tests cover placeholder-driven prompt rendering where the new workflow type depends on it
