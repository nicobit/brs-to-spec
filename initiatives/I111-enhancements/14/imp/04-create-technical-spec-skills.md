# Prompt 04 - Create Technical Specification Skills

## Context

Templates alone are not sufficient. The new workflow type needs skill prompts
that define what each technical-spec action reads, how it reasons, and what it
produces.

Before making changes, read these files in full:

- `.b2s/skills/engineering-lead/create-api-contract.md`
- `.b2s/skills/security-reviewer/create-data-contract.md`
- `.b2s/skills/engineering-lead/create-event-contract.md`
- `.b2s/skills/engineering-lead/create-openspec-handoff.md`
- `framework_enhancement/14/03-skills.md`

## Goal

Create skill files for the technical-spec families required by the new workflow
type.

## Required skill behavior

Every skill must:

1. Read explicit upstream artifacts in full before writing.
2. Prefer architecture review and architecture rules for technical constraints.
3. Use delivery structure for story ownership and story references.
4. Use readiness output for contract mode and gate-trigger decisions when
   applicable.
5. Record open questions instead of inventing details.

## Placeholder rule

When writing or updating these skills, do not hardcode path-reading instructions
if the engine already exposes the workflow-driven prompt placeholder contract.

Prefer prompt text such as:

- `Read every path listed in {resolved_required_inputs} fully before writing.`
- `If {resolved_optional_inputs} is not empty, read those paths fully as well before writing.`
- `Write the artifact to {primary_output}.`

Use the action-specific text to explain how the inputs should be interpreted,
not to restate fixed filesystem paths unnecessarily.

## Minimum upstream inputs by family

- exposed API specs:
  - `architecture/architecture-review.md`
  - `architecture/architecture-rules.md`
  - `planning/delivery-structure.md`
  - `engineering-readiness/readiness-check.md`
- consumed API specs:
  - `architecture/architecture-review.md`
  - `architecture/architecture-rules.md`
  - `planning/delivery-structure.md`
- data specs:
  - `architecture/architecture-review.md`
  - `architecture/architecture-rules.md`
  - `planning/delivery-structure.md`
  - `business-analysis/requirements.md`
  - `business-analysis/business-rules.md` when present
- integration specs:
  - `architecture/architecture-review.md`
  - `architecture/architecture-rules.md`
  - `planning/delivery-structure.md`

## Important rule

Do not design the skills so they depend on artifacts that do not yet exist at
their workflow stage.

## Done criteria

- [ ] Skill files exist for the technical-spec actions used by the new workflow type
- [ ] Every skill has explicit required and optional inputs
- [ ] Every skill is written so downstream consumers can rely on its output deterministically
- [ ] Skills use the placeholder contract for path wiring where appropriate, instead of new hardcoded path text
