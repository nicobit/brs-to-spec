# Prompt 02 - Implement Profile-Based Validation Engine

## Goal

Teach the `.b2s` validator to resolve by validation profile before using the
generic fallback path.

## Files to modify

- `.b2s/scripts/b2s_engine/validation.py`
- optionally supporting helper files under `.b2s/scripts/b2s_engine/`

## Required work

Refactor validation dispatch so it works in this order:

1. dedicated artifact validator when present
2. profile validator based on action metadata
3. explicit low-risk fallback only when allowed
4. failure or audit signal when a high-risk artifact lacks proper coverage

Implement reusable profile validators for:

- `basic-file`
- `structured-document`
- `catalog`
- `analytical-review`
- `artifact-package`

Use deterministic heuristics only. Do not add model-like reasoning inside the
validator.

## Engine behavior requirements

- profile validators should consume action metadata such as required sections
- dedicated validators should still override general profiles when needed
- generic non-empty validation should become a deliberate low-risk path, not the
  silent default for important artifacts

## Constraints

- preserve existing strong validators where they already work
- keep validation deterministic and local
- avoid overfitting the profiles to one artifact

## Verification

Verify that:

1. an action with a profile but no dedicated validator is validated through the
   profile
2. a dedicated validator still wins when present
3. critical artifacts cannot silently drop to the generic non-empty path
