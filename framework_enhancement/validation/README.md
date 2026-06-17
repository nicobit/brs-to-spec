# Validation Framework Enhancement

This package defines a framework-level improvement for `.b2s` artifact
validation so stage-critical artifacts cannot pass on file existence alone.

## Why this exists

The immediate trigger was `architecture/architecture-review.md` reaching
`ai_validated` while still being a placeholder. The root cause is broader:
validation coverage is inconsistent across actions, and important artifacts can
fall back to the generic non-empty-file validator.

## Package contents

- `00-validation-framework-plan.md` - design summary and target operating model
- `01-validation-profile-model.md` - standard validation profiles, criticality,
  and classification rules
- `implementation/00-implementation-plan.md` - ordered execution plan
- `implementation/01-prompt-add-validation-contract-to-stage-actions.md`
- `implementation/02-prompt-implement-profile-based-validation-engine.md`
- `implementation/03-prompt-add-framework-audit-for-validation-coverage.md`
- `implementation/04-prompt-add-analytical-review-profile-and-architecture-review-coverage.md`
- `implementation/05-prompt-classify-high-criticality-actions.md`
- `implementation/06-prompt-add-tests-and-fixtures-for-validation-profiles.md`

## Execution order

Run the files under `implementation/` in numeric order.

## Scope

This enhancement is framework-wide. It should not create a one-off architecture
review patch. `architecture/architecture-review.md` is only the first artifact
used to prove the new standard works.
