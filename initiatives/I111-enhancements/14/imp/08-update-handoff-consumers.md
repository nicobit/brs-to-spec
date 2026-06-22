# Prompt 08 - Update Handoff Consumers

## Context

The value of the new workflow type depends on descendant actions actually using
the technical-spec artifacts. Otherwise the new folder structure becomes
ceremony with no delivery benefit.

Before making changes, read these files in full:

- `.b2s/skills/engineering-lead/create-openspec-handoff.md`
- `.b2s/skills/engineering-lead/create-standalone-handoff.md`
- `.b2s/skills/engineering-lead/generate-initiative-context.md`
- `framework_enhancement/14/05-update-openspec-handoff-and-validators.md`

## Goal

Update the downstream consumer skills so they use canonical
technical-specification artifacts in the new workflow type.

## Required work

1. Add the technical-spec paths as explicit optional or required inputs where
   appropriate.
2. Define how each consumer uses each artifact family.
3. Avoid reinventing fields already present in technical-spec artifacts.

## Placeholder rule

Update consumer skills so their read and write path instructions use the
placeholder contract where possible.

Prefer:

- `{resolved_required_inputs}`
- `{resolved_optional_inputs}`
- `{primary_output}`
- `{secondary_outputs}`

Do not reintroduce long hardcoded path-reading blocks if the workflow action
already declares those paths and the engine can resolve them.

## Minimum consumer expectations

- exposed API specs:
  provide exact endpoint paths, methods, request and response fields, auth,
  error codes, and SLA constraints
- consumed API specs:
  provide provider-facing path, auth, PII minimization constraints, and fallback
  considerations
- data specs:
  provide exact data assets, fields, constraints, retention, and PII details
- integration specs:
  provide timeout, retry, fallback, observability, and dependency semantics

## Important rule

Handoff skills must treat these artifacts as authoritative detail when present.
They should not regenerate equivalent details from scratch unless the specs are
missing.

## Done criteria

- [ ] Handoff consumer skills read technical-spec artifacts explicitly
- [ ] Consumer instructions explain how the artifacts populate descendant sections
- [ ] Redundant re-derivation is minimized
- [ ] Consumer prompts use placeholder-driven path wiring where appropriate
