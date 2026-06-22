# Prompt 01 - Define the Parallel Workflow Type

## Context

You are implementing Enhancement 14 in a way that runs in parallel to the
existing workflow types under `.b2s/workflow-types/`.

Before making changes, read these files in full:

- `.b2s/workflow-types/index.yaml`
- `.b2s/workflow-types/enterprise-modular/README.md`
- `.b2s/workflow-types/enterprise-modular/workflow-definition.yaml`
- `.b2s/workflow-types/enterprise-modular/stage-actions.yaml`
- `.b2s/scripts/b2s_engine/init_workspace.py`

## Goal

Define a new workflow type for technical-specification-aware delivery without
breaking `enterprise-modular` or `fast-path`.

## Required work

1. Create a new workflow type directory under `.b2s/workflow-types/`.
2. Choose a stable workflow type ID and use it consistently in:
   - the directory name
   - `.b2s/workflow-types/index.yaml`
   - the workflow README
3. Document the purpose of the new workflow type clearly:
   - parallel to existing workflow types
   - suitable for initiatives requiring first-class technical specifications
   - not a replacement for existing workflow types by default
4. Ensure initiative initialization can select the new workflow type through the
   existing workflow-type copy mechanism.

## Naming rule

Use a name that reflects capability, not a single artifact. Recommended style:

- `technical-spec-modular`
- `contract-governed-modular`

Avoid names like:

- `api-workflow`
- `new-workflow`
- `parallel`

## Done criteria

- [ ] New workflow type ID is added to `.b2s/workflow-types/index.yaml`
- [ ] New workflow type directory exists with README, workflow-definition, and stage-actions files
- [ ] Existing workflow type IDs remain unchanged
- [ ] `init_workspace.py` can continue copying workflow types without a special-case branch
