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
- `create-nfr-assessment`
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

## Action contract

Actions are still declared in `.b2s/workflow/stage-actions.yaml`, but the engine
now normalizes them into a canonical in-memory contract before use.

The typical enriched action shape now includes:

- `inputs.required` and `inputs.optional`
- `policy_refs`
- `prompt_family`
- `skill_ref`
- `artifact_template_ref`
- `validation_profile`
- `validation_rules.required`
- `validation_rules.optional`
- `human_gate`
- `compatibility.fallback_skill_ref`

Representative optional fields in the additive v2 contract include:

- `prompt_family` - prompt strategy label; defaults to `b2s`
- `policy_refs` - policy files that govern artifact generation
- `template_mode` - template enforcement mode; defaults to `strict`
- `validation_rules.required` - named rule identifiers for required validation
- `validation_rules.optional` - named rule identifiers for advisory validation
- `compatibility.fallback_skill_ref` - future-safe fallback when alternate prompt
  families are introduced

Older action definitions remain valid. Missing v2 fields are defaulted by the
engine at load time.

Policy resolution rules:

- `policy_refs` are resolved as framework-governed inputs during `collect-inputs`
- resolved policy paths are surfaced to prompts through
  `{resolved_policy_inputs}`
- policy files must be read before artifact generation begins

Validation declaration rules:

- `validation_profile` selects the structural validator family
- `validation_rules.required` declares named must-pass checks
- `validation_rules.optional` declares advisory checks that surface as
  non-blocking guidance

## Prompt families

`.b2s` remains the orchestration layer. `prompt_family` is metadata that tells
the engine and maintainers which prompt strategy an action is aligned to.

Current implementation rules:

- keep the existing persona-based `.b2s/skills/...` tree in place
- do not move or rename current skill files to match families
- allow actions to declare families such as `b2s`, `speckit`, `bmad`, and `hve`
- if a non-`b2s` action points to a missing skill, require
  `compatibility.fallback_skill_ref` or fail clearly

This means prompt-family routing is supported now without requiring a filesystem
migration.

## Reference Docs

See the framework reference docs for the current enriched model:

- `.b2s/docs/action-contract-v2.md`
- `.b2s/docs/golden-action-examples.md`
- `.b2s/docs/action-migration-guide.md`
- `.b2s/docs/phase-family-map.md`
