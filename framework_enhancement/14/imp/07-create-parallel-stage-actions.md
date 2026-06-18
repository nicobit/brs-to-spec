# Prompt 07 - Create the Parallel Stage Actions

## Context

Once the new workflow stage graph exists, the corresponding action registry must
be defined under the new workflow type.

Before making changes, read these files in full:

- `.b2s/workflow-types/enterprise-modular/stage-actions.yaml`
- `.b2s/workflow/stage-actions.yaml`
- `framework_enhancement/14/04-contract-mode-and-stage-wiring.md`

## Goal

Create the stage-actions file for the new workflow type, including the
technical-specification actions and explicit producer-consumer dependencies.

## Required work

1. Start from the closest existing workflow type.
2. Add the new technical-spec actions only in the new workflow type.
3. Make required inputs and outputs explicit.
4. Ensure descendant actions consume canonical technical-spec paths.

## Placeholder alignment rule

This prompt is about workflow action definitions, not direct prompt wording.
However, the resulting actions must be compatible with the placeholder-based
input/output contract now used by `.b2s`.

That means:

- define `inputs.required`
- define `inputs.optional`
- define `outputs.primary`
- define `outputs.secondary`

cleanly enough that the engine can expose:

- `{required_inputs}`
- `{optional_inputs}`
- `{resolved_required_inputs}`
- `{resolved_optional_inputs}`
- `{primary_output}`
- `{secondary_outputs}`

without needing any technical-spec-specific placeholder special cases.

## Required action families

- create-exposed-api-specs
- create-consumed-api-specs
- create-data-schema-specs or equivalent
- create-event-specs if included in the new design
- create-integration-specs

## Required output paths

- `technical-specifications/api/exposed/`
- `technical-specifications/api/consumed/`
- `technical-specifications/data/`
- `technical-specifications/events/` when applicable
- `technical-specifications/integrations/`

## Required downstream consumers

At minimum, update the new workflow type so these actions can consume
technical-spec outputs when present:

- `generate-initiative-context` if needed for compact binding context
- `create-openspec-handoff`
- `create-standalone-handoff` if the new workflow type supports Standalone
- any review-package assembler that should reference them

## Important rule

Do not leave the same descendant action reading both a legacy path and a new
canonical path without an explicit precedence rule.

## Done criteria

- [ ] New workflow-type stage-actions file includes all technical-spec actions
- [ ] Inputs and outputs are explicit and stage-correct
- [ ] Downstream consumers are wired to canonical technical-spec paths
- [ ] No ambiguous dual-source-of-truth behavior is introduced
