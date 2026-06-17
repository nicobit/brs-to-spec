---
description: Create a new initiative workspace for the staged .b2s framework.
---

## Create a new .b2s initiative workspace

### Step 1 — Confirm the initiative ID

Ask the user for the initiative ID if not already provided.
Format: `I<number>-<short-slug>` — e.g. `I012-MY-APP`, `I013-PORTAL`.

Do not proceed until you have a confirmed ID.

### Step 2 — Run the CLI initializer

Run this exact command from the repository root:

```
python .b2s/scripts/b2s_cli.py init-workspace --initiative-id <ID>
```

Do not create any files or folders manually. The CLI owns the workspace structure.

### Step 3 — Confirm what was created

Read the output. A successful init produces exactly:

```
initiatives/<ID>/
  input/
    brs.md          ← blank BRS template — the user fills this in
  .b2s/
    state/
      workflow-state.json
      open-decisions.md
    tmp/
      init-workspace.json
```

If the CLI reports `FileExistsError`, the workspace already exists. Do not reinitialize. Tell the user and stop.

### Step 4 — Tell the user what to do next

Report the workspace path and say:

> Fill in `initiatives/<ID>/input/brs.md` with the business requirements.
> When ready, run the workflow with `b2s-dispatch-next` or `b2s-dispatch-all`.

### Hard stops

- Do NOT copy `.b2s/agent-instructions.md`, `.b2s/module-index.md`, or `.b2s/prompts/run-workflow.md` into the initiative workspace. Those files live at the repo root only.
- Do NOT create `00-start.md`, `README.md`, or any other files beyond what the CLI produces.
- Do NOT run the workflow automatically. The user must fill in the BRS first.
- Do NOT use `--workspace-root` unless the user explicitly requests a non-standard path.
