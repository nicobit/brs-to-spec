# Implementation Plan - Validation Framework Standardization

## Goal

Standardize `.b2s` validation so important artifacts cannot pass on generic
non-empty checks alone.

## Ordered prompts

Run these prompts in order:

1. `01-prompt-add-validation-contract-to-stage-actions.md`
2. `02-prompt-implement-profile-based-validation-engine.md`
3. `03-prompt-add-framework-audit-for-validation-coverage.md`
4. `04-prompt-add-analytical-review-profile-and-architecture-review-coverage.md`
5. `05-prompt-classify-high-criticality-actions.md`
6. `06-prompt-add-tests-and-fixtures-for-validation-profiles.md`

## Delivery strategy

### Phase 1

Create the standard mechanism:

- validation contract fields
- profile resolution
- audit checks

### Phase 2

Prove the mechanism on the triggering case:

- `review-initial-architecture`

### Phase 3

Apply the classification to other high-criticality actions:

- architecture
- planning
- readiness
- quality-gate authority artifacts

### Phase 4

Lock it down with tests and fixtures.

## Success criteria

- no human-gated authority artifact can pass on fallback non-empty validation
- validation coverage is explicit in action metadata
- framework audit detects unclassified or under-validated critical actions
- tests show placeholders fail where the new standard applies
