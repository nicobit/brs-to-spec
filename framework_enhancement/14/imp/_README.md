# Framework Enhancement 14 Implementation Pack

This folder contains the ordered implementation prompts for turning Framework
Enhancement 14 into a workflow-type-based change that runs in parallel to the
existing `.b2s` workflow types.

## Design intent

Do not retrofit the existing workflow types in place as the primary mechanism.
Instead:

- introduce a new workflow type under `.b2s/workflow-types/`
- keep the existing workflow types intact
- make the new workflow type the place where technical-specification actions and
  sequencing live
- preserve shared artifact locations and shared engine behavior wherever
  possible

## Placeholder alignment

This implementation pack assumes the prompt placeholder infrastructure from
`framework_enhancement/14/imp2` is available or will be introduced first.

That means:

- workflow actions still declare the formal input and output contract
- the engine resolves prompt-facing placeholders from that contract
- skill prompts should prefer:
  - `{resolved_required_inputs}`
  - `{resolved_optional_inputs}`
  - `{primary_output}`
  - `{secondary_outputs}`
  instead of reintroducing hardcoded path-reading and output-writing text

## Primary objective

Create a parallel workflow that:

- preserves the canonical business, architecture, planning, readiness, and
  handoff stages
- adds first-class `technical-specifications/` artifacts
- ensures upstream inputs are explicit
- ensures downstream consumers read the new artifacts deterministically
- avoids dual-source ambiguity between `quality-gates/` and
  `technical-specifications/`

## Support files

- `_README.md`
- `_00-plan.md`

## Ordered runnable prompts

1. `01-define-parallel-workflow-type.md`
2. `02-add-technical-specifications-workspace-layout.md`
3. `03-create-technical-spec-artifact-templates.md`
4. `04-create-technical-spec-skills.md`
5. `05-wire-readiness-and-state-fields.md`
6. `06-create-parallel-workflow-definition.md`
7. `07-create-parallel-stage-actions.md`
8. `08-update-handoff-consumers.md`
9. `09-add-validation-and-tests.md`
10. `10-document-selection-and-migration-boundaries.md`

## Non-goals

- Do not silently redefine existing `enterprise-modular` behavior.
- Do not leave the same technical truth split across two canonical folders.
- Do not make workflow mode determine folder names.
- Do not assume the parallel workflow is OpenSpec-only unless explicitly wired
  that way.
