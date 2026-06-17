# Prompt 03 - Add Framework Audit For Validation Coverage

## Goal

Detect framework misconfiguration where important actions lack adequate
validation coverage.

## Files to modify

- `.b2s/scripts/b2s_engine/validation.py` or a new adjacent audit helper
- `.b2s/tests/` to cover the audit behavior
- optionally add a dedicated lightweight audit script if that fits the engine
  structure better

## Required work

Add a framework-level audit that can detect cases such as:

- human-gated artifact uses `basic-file`
- `high` or `critical` artifact has no profile
- artifact consumed by many downstream actions has only generic fallback
- template-rich analytical artifact is treated as a generic non-empty file

The audit may run:

- during validation dispatch
- as a separate framework check
- or both

The important part is that missing validation coverage becomes visible as a
framework defect.

## Minimum required findings

The audit should be able to flag:

- `review-initial-architecture` if it is unclassified or under-validated
- any human-gated analytical artifact left on `basic-file`

## Constraints

- keep the rules deterministic
- derive risk from stage-action metadata and downstream use where practical
- do not depend on AI interpretation for the audit

## Verification

Verify that:

1. obviously under-validated critical actions are reported
2. properly classified actions do not trigger false failures
3. the audit output is understandable to a maintainer
