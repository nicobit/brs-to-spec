# Prompt 10 - Document Selection and Migration Boundaries

## Context

A new workflow type only helps if users know when to choose it and if
maintainers know what it does not replace yet.

Before making changes, read these files in full:

- `.b2s/workflow-types/index.yaml`
- `.b2s/workflow-types/enterprise-modular/README.md`
- `.b2s/workflow-types/fast-path/README.md`
- `framework_enhancement/14/plan.md`

## Goal

Document how the new workflow type should be selected and what migration
boundaries apply between the old flat contract artifacts and the new
technical-specification model.

## Required work

1. Add workflow-type README guidance for:
   - when to use the new workflow type
   - when not to use it
   - which delivery modes it supports
2. Define the source-of-truth rule explicitly:
   - which artifacts are canonical in the new workflow type
   - whether any legacy flat quality-gate contract files still exist
   - which artifact wins if both exist
3. Document migration boundary decisions:
   - existing initiatives are unaffected
   - new initiatives can opt into the new workflow type
   - no silent cross-upgrade of active initiatives

## Placeholder documentation rule

The documentation for the new workflow type should assume the shared prompt
placeholder contract is available.

Document clearly that:

- workflow actions define the declared inputs and outputs
- the engine resolves prompt-facing input/output placeholders
- prompts in the new workflow type should prefer placeholder-driven path wiring
  over hardcoded path text

## Important rule

If dual-path compatibility exists temporarily, document precedence explicitly.
Do not force users to infer it from implementation details.

## Done criteria

- [ ] The new workflow type is documented in a user-selectable way
- [ ] Canonical artifact ownership is documented clearly
- [ ] Migration boundary and precedence rules are explicit
- [ ] Placeholder-driven prompt usage is aligned with the new workflow-type documentation
