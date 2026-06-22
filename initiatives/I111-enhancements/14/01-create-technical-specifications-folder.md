# Prompt 01 — Create technical-specifications Folder Convention

## Context

You are working on the `.b2s` framework at the root of this repository.

The initiative workspace currently has no canonical location for technical specifications.
APIs, database schemas, event schemas, and integration specs are scattered across
`quality-gates/` as flat files or buried inside story implementation context.

This prompt introduces the `technical-specifications/` folder as a first-class workspace
location and wires it into workspace initialisation.

## Step 1 — Update init_workspace.py

Read `.b2s/scripts/b2s_engine/init_workspace.py` in full.

Add `technical-specifications/` sub-folder creation to the workspace initialisation
routine, alongside the existing folder structure. Create these sub-folders:

```
technical-specifications/
  api/
    exposed/
    consumed/
  database/
  events/
  integrations/
```

Each folder should be created with a `.gitkeep` file so they are tracked in git
even when empty. Follow the same pattern used for other folders in init_workspace.py.

## Step 2 — Update workspace.py folder constants

Read `.b2s/scripts/b2s_engine/workspace.py` in full.

Add a constant or helper that resolves the `technical-specifications/` path within
a workspace root, consistent with how other workspace paths are resolved.

## Step 3 — Add a README to the technical-specifications template

Create `.b2s/templates/technical-specifications/README.md` with this content:

```markdown
# Technical Specifications

This folder contains all technical specifications for this initiative.

## Structure

| Folder | Purpose |
|---|---|
| `api/exposed/` | OpenAPI-level specs for APIs you publish. One file per API surface. |
| `api/consumed/` | Specs for external APIs you depend on. One file per external system. |
| `database/` | Table schemas, column definitions, constraints, migration notes. |
| `events/` | Domain events you emit and events you subscribe to. |
| `integrations/` | Auth, SLA, retry policy, and fallback behaviour per external system. |

## Ownership

- `api/exposed/` — owned by this initiative's engineering lead
- `api/consumed/` — sourced from external system documentation; annotated by this team
- `database/` — owned by this initiative; shared schemas noted explicitly
- `integrations/` — owned by this initiative; reviewed by architecture
```

## Step 4 — Verify

Run the existing test suite and confirm all tests pass:

```
python -m pytest .b2s/tests/ -q
```

If any test fails due to the workspace layout change, fix it before proceeding.

## Done criteria

- [ ] `init_workspace.py` creates all 5 sub-folders under `technical-specifications/`
- [ ] Each sub-folder has a `.gitkeep` file
- [ ] `workspace.py` has a helper or constant for `technical-specifications/` path
- [ ] `.b2s/templates/technical-specifications/README.md` exists with the content above
- [ ] All existing tests pass
