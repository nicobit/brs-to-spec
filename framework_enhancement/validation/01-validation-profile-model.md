# Validation Profile Model

## Purpose

Define a standard `.b2s` validation vocabulary that can be applied to any
artifact action.

## Validation profiles

### `basic-file`

Use for low-risk leaf artifacts only.

Checks:

- artifact exists
- artifact is non-empty

### `structured-document`

Use for ordinary markdown artifacts that are consumed downstream.

Checks:

- required headings exist
- required sections or tables exist
- content is not template-only
- content is not obvious placeholder-only
- content is not suspiciously tiny

### `catalog`

Use for row-oriented artifacts such as requirements, rules, gaps, or entity
catalogs.

Checks:

- all `structured-document` checks
- minimum row presence
- IDs present where expected
- traceability or source fields populated
- required sections are populated, not just present

### `analytical-review`

Use for architecture, readiness, security, test-strategy, and similar review
artifacts.

Checks:

- all `structured-document` checks
- required analysis dimensions are covered
- explicit risks, assumptions, decisions, and unknowns are present
- upstream critical gaps or constraints are reflected when relevant
- content is not merely a short summary

### `artifact-package`

Use for folder outputs like `specs/`, `standalone-delivery/`, or
`review-package/`.

Checks:

- required files or folders exist
- directory is non-empty
- representative files contain required sections
- package is not skeleton-only

## Criticality levels

### `low`

- low reuse
- not stage-authoritative
- safe to validate lightly

### `standard`

- consumed downstream
- needs structural validation

### `high`

- used by several downstream actions
- weak validation can distort planning or generation

### `critical`

- architecture, readiness, planning, or contract authority
- or opens a human gate
- or acts as a core reasoning input to many downstream steps

## Classification rules

### Mandatory rules

- `high` and `critical` artifacts may not use generic fallback validation
- human-gated artifacts may not use generic fallback validation
- artifacts referenced by multiple downstream actions must be at least
  `structured-document`
- review or authority artifacts must be `analytical-review` or a dedicated
  validator

### Recommended rules

- catalogs should use `catalog`
- package outputs should use `artifact-package`
- only explicitly low-risk leaf outputs may use `basic-file`

## Suggested action metadata

Each action should declare fields like:

- `validation_profile`
- `artifact_criticality`
- `required_sections`
- `required_tables`
- `forbidden_placeholders`

These should be optional for profile internals, but profile and criticality
should become mandatory for non-human-triggered actions.

## Proof-point classification

`review-initial-architecture` should be:

- `validation_profile: analytical-review`
- `artifact_criticality: critical`

because it opens a gate, is consumed by many downstream actions, and acts as
architecture authority.
