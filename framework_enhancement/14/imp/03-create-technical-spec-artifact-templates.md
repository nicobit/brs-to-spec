# Prompt 03 - Create Technical Specification Artifact Templates

## Context

The new workflow type needs concrete output-shape contracts for each technical
spec family. These templates must align with how descendant actions will consume
them, not just how they are authored.

Before making changes, read these files in full:

- `.b2s/artifact-templates/api-contract.md`
- `.b2s/artifact-templates/data-contract.md`
- `.b2s/artifact-templates/event-contract.md`
- `.b2s/artifact-templates/story-package.md`
- `framework_enhancement/14/02-artifact-templates.md`

## Goal

Create the artifact templates for the canonical technical specification
artifacts used by the new workflow type.

## Required template families

1. Exposed API specification
2. Consumed API specification
3. Data schema or data contract specification
4. Integration specification
5. Event specification, if the new workflow type requires event-level technical
   detail beyond the existing flat event contract

## Shape requirements

Each template must include:

- metadata
- traceability to story IDs where applicable
- explicit source or evidence references
- open questions section when upstream evidence is insufficient
- enough structure for downstream handoff consumption without forcing the
  handoff step to invent missing fields

## Output-location mapping

The templates must map cleanly to the canonical folder structure:

- `.b2s/artifact-templates/exposed-api-spec.md`
- `.b2s/artifact-templates/consumed-api-spec.md`
- `.b2s/artifact-templates/data-schema-spec.md` or equivalent stable name
- `.b2s/artifact-templates/integration-spec.md`

## Important rule

Do not let the template names and folder names drift semantically. If the folder
is `data/`, the template should not imply a strictly SQL-only worldview unless
that is an explicit framework decision.

## Done criteria

- [ ] Template set covers all canonical technical-spec families for the new workflow type
- [ ] Templates support downstream consumption by handoff steps
- [ ] Story and constraint traceability are first-class, not optional afterthoughts
