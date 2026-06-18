# Prompt 02 - Add Technical Specifications Workspace Layout

## Context

The new workflow type needs a stable artifact home for technical specifications.
That folder structure must be workflow-independent so descendant actions can
consume the same paths regardless of execution mode.

Before making changes, read these files in full:

- `.b2s/scripts/b2s_engine/init_workspace.py`
- `.b2s/scripts/b2s_engine/workspace.py`
- `framework_enhancement/14/plan.md`
- `framework_enhancement/14/01-create-technical-specifications-folder.md`

## Goal

Introduce the canonical technical-specifications folder structure at workspace
initialization time.

## Required work

1. Add the new folder structure to initiative workspace initialization.
2. Add any helper or constant needed to resolve the technical-specifications
   root reliably from the workspace root.
3. Add a template README describing ownership and purpose of each sub-folder.

## Canonical structure

Use this exact structure unless a prior prompt explicitly requires a different
name:

```text
technical-specifications/
  api/
    exposed/
    consumed/
  data/
  events/
  integrations/
```

## Important rules

- Prefer `data/` over `database/` to avoid overfitting the framework to
  relational-only schemas.
- Do not create workflow-specific subfolders such as `openspec/`,
  `standalone/`, or `parallel/` under `technical-specifications/`.
- Keep the folder names artifact-domain-oriented.

## Done criteria

- [ ] Workspace initialization creates the canonical technical-specifications tree
- [ ] Tracking files are added consistently with existing workspace conventions
- [ ] A README explains purpose and ownership of each folder
- [ ] No workflow-specific folder branching is introduced under technical-specifications
