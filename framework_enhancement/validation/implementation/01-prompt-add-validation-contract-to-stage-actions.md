# Prompt 01 - Add Validation Contract To Stage Actions

## Goal

Make validation coverage explicit in `.b2s/workflow/stage-actions.yaml` instead
of relying on whether an artifact happens to have a custom validator.

## Files to modify

- `.b2s/workflow/stage-actions.yaml`
- optionally `.b2s/module-index.md` if documentation of validation contract
  fields belongs there

## Required work

Add a standard validation contract to non-human-triggered actions.

Introduce fields such as:

- `validation_profile`
- `artifact_criticality`
- optional structural hints:
  - `required_sections`
  - `required_tables`
  - `forbidden_placeholders`

Do not overfill every action with bespoke rules in this step. Focus on adding
the contract shape consistently so the engine can rely on it later.

## Minimum classification expectations

- `review-initial-architecture` must not remain unclassified
- human-gated actions must be classified explicitly
- stage-critical planning and readiness actions must be classified explicitly
- low-risk artifacts may remain on `basic-file` only if that choice is
  deliberate and justified by low criticality

## Constraints

- keep the metadata readable
- prefer reusable profile names over action-specific flags
- do not encode the full validator logic inside `stage-actions.yaml`

## Verification

Verify that:

1. all non-human-triggered actions have a validation profile
2. all human-gated actions have `artifact_criticality` of at least `high`
3. `review-initial-architecture` is classified as a review-style artifact, not
   a basic file
