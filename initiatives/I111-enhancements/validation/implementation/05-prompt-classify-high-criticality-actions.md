# Prompt 05 - Classify High-Criticality Actions

## Goal

Extend the new validation standard beyond architecture review to the rest of the
highest-risk `.b2s` actions.

## Files to modify

- `.b2s/workflow/stage-actions.yaml`
- `.b2s/scripts/b2s_engine/validation.py`
- relevant tests under `.b2s/tests/`

## Required work

Review the current action catalog and classify at least the high-risk actions
that act as authority artifacts for downstream work.

Minimum target set:

- `review-initial-architecture`
- `create-architecture-rules`
- `create-delivery-structure`
- `create-traceability-matrix`
- `check-engineering-readiness`
- `generate-initiative-context`
- `create-security-review`
- `create-test-strategy`
- `create-api-contract`
- `create-data-contract`
- `create-event-contract`
- `create-observability-plan`

For each, decide whether a reusable profile is enough or whether a dedicated
validator is still justified.

## Classification principle

- use profiles wherever a standard pattern is enough
- use dedicated validators only when profile checks cannot adequately guard the
  artifact

## Constraints

- do not aim for perfect semantic completeness in one pass
- focus on preventing obviously unsafe shallow artifacts from progressing
- preserve readability of action metadata

## Verification

Verify that:

1. every high-criticality action now has explicit coverage
2. none of those actions rely on silent generic fallback
3. the classification remains understandable to maintainers
