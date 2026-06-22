# Prompt 04 - Add Analytical Review Profile And Architecture Review Coverage

## Goal

Prove the new standard on the original failure case by making
`review-initial-architecture` validate as an `analytical-review`.

## Files to modify

- `.b2s/scripts/b2s_engine/validation.py`
- `.b2s/workflow/stage-actions.yaml`
- `.b2s/tests/test_engine_runtime.py`
- `.b2s/tests/test_engine_fixtures.py`
- fixtures under `.b2s/tests/fixtures/` as needed

## Required work

Implement the `analytical-review` profile so it can reject placeholder review
artifacts mechanically.

For `architecture/architecture-review.md`, require checks such as:

- all major template sections are present
- initiative-architecture fit section is populated
- architecture constraints have rationale and violation consequence
- brownfield impact is explicitly covered
- quality attributes are populated
- open decisions are populated when upstream gaps exist
- assumptions include `If False, Then`
- artifact is not just a short summary or placeholder note

Use deterministic structure checks and upstream-signal checks only.

## Upstream references allowed

This validation may inspect directly relevant upstream artifacts such as:

- `business-analysis/requirements.md`
- `business-analysis/gaps-and-questions.md`
- `business-intake/business-intake-summary.md`
- `input/architecture.md`

## Constraints

- do not hardcode logic specific only to the I013 example
- keep the checks general for architecture review artifacts
- reject shallow placeholders without trying to prove full architectural
  correctness

## Verification

Verify that:

1. the current placeholder-style architecture review would fail
2. a real populated architecture review passes
3. the artifact still opens the human gate only after substantive machine
   validation succeeds
