# `.b2s` Module Index

## Purpose

This file will map stage actions to prompts, personas, and outputs.

## Status

Initial staged action registry is now in place and backed by concrete skill and
template files. Engine mechanics are implemented for stage selection, input
collection, validation, state update, gates, and reset or repair.

## Active prompt and template slice

- `route-initiative`
- `create-business-intake-summary`
- `gate-business-intake-review`
- `create-requirements`
- `create-use-case-diagram`
- `create-entity-model`
- `create-business-rules`
- `find-gaps-and-questions`
- `create-actors-and-personas`
- `create-use-case-specs`
- `create-process-flows`
- `create-business-test-expectations`
- `draft-architecture-from-brs`
- `review-initial-architecture`
- `create-architecture-rules`
- `review-existing-system-impact`
- `create-delivery-structure`
- `create-traceability-matrix`
- `identify-software-modules`
- `map-capabilities-to-modules`
- `define-delivery-increments`
- `check-engineering-readiness`
- `generate-initiative-context`
- `create-bdd-scenarios`
- `create-test-strategy`
- `create-security-review`
- `create-threat-model`
- `create-api-contract`
- `create-data-contract`
- `create-event-contract`
- `create-observability-plan`
- `create-test-plan-per-story`
- `create-openspec-handoff`
- `create-standalone-handoff`
- `create-compact-handoff`
- `generate-test-stubs-from-bdd`
- `create-agile-planning-view`
- `create-review-package`
- `create-brs`
- `senior-code-review`
- `architecture-review`
- `spec-correction`
- `gate-architecture-review`
- `gate-engineering-readiness-review`

## Current loading rules

- Resolve executable actions from `.b2s/workflow/stage-actions.yaml`
- Load exactly one skill prompt from `.b2s/skills/...` for the selected action
- Use `.b2s/artifact-templates/...` only as the output shape contract
- Gate progression on machine-written files under `.b2s/state/` and `.b2s/tmp/`
- Stop if any required engine output file is missing or reports failure
