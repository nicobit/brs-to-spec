# Validation Framework Plan

## Problem

`.b2s` currently has two validation paths:

- dedicated artifact validators for some actions
- fallback non-empty file or non-empty directory checks for everything else

This makes workflow progression depend too heavily on whether a specific
artifact happened to receive a custom validator. The result is that some
stage-critical artifacts can pass validation despite being placeholders.

## Target outcome

Every action must have an explicit validation contract. That contract should be
expressed in a standard framework way, not buried in one-off custom code.

The framework should support:

1. standard validation profiles
2. artifact criticality levels
3. explicit per-action classification
4. profile-based validation before generic fallback
5. framework audit rules that detect missing validation coverage

## Core principle

If downstream work depends on the content of an artifact, validation must check
content shape and minimum semantic coverage, not just file existence.

## Proposed model

Each action should declare:

- `validation_profile`
- `artifact_criticality`
- optional machine-checkable structural requirements

The validator should resolve in this order:

1. dedicated validator if one exists
2. profile validator if the action declares a profile
3. generic fallback only for explicitly low-risk artifacts
4. framework validation configuration failure for high-risk actions with no
   proper validation definition

## Desired framework rule

The following artifacts must never rely on generic non-empty validation:

- human-gated artifacts
- artifacts consumed by multiple downstream actions
- architecture, planning, readiness, and contract authority artifacts
- review artifacts used as reasoning inputs downstream

## Immediate proof point

`review-initial-architecture` should move from implicit fallback validation to a
standard `analytical-review` profile.

## Implementation strategy

1. define validation profiles and criticality levels
2. add explicit validation contract fields to `stage-actions.yaml`
3. implement profile-based validation dispatch in the engine
4. add a framework audit for missing coverage
5. classify and migrate the highest-risk actions first
6. add tests and fixtures proving placeholders fail appropriately
