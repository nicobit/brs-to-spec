# BRS to Spec Framework — Claude Code Instructions

## Framework activation

This repository contains the brs-to-spec framework. Apply the framework behavioral rules in every session.

**Load at session start:**
1. `.b2s/agent-instructions.md` — core behavioral rules, gate rules, state rule, prompt loading rule
2. `.b2s/module-index.md` — action registry, loading rules
3. `.b2s/prompts/run-workflow.md` — staged execution loop (19-step sequence)

After loading these files, follow all rules found there. They are the authoritative behavioral contract for this framework.

## Hard stop — when asked to create a new initiative

When the user says anything like "create initiative", "new initiative", "initialize I0XX-...", or "set up a new workspace":

1. Do NOT create any files or folders manually.
2. Do NOT create `initiative.yaml`, `00-start.md`, `README.md`, or any file not produced by the CLI.
3. Do NOT copy or recreate the `.b2s/` framework folder inside the initiative workspace.
4. Read and follow `.github/prompts/b2s-new-initiative.prompt.md` — follow it exactly.

## Hard stop — before creating any file or folder inside `initiatives/`

1. STOP. Do not create anything yet.
2. Identify the active initiative workspace (`initiatives/<id>-<slug>/`).
3. Check whether `.b2s/state/workflow-state.json` exists in that workspace.
4. Run the staged execution loop from `.b2s/prompts/run-workflow.md`.

Only create files that the workflow runner explicitly instructs you to create, at the path it specifies.

## Input boundary rule

`initiatives/<id>/input/` is the only folder you may write to directly without running the workflow first. Everything outside `input/` is produced by framework skills only.

**Never create files or folders at the repository root.** Implementation artefacts (API schemas, migration scripts, CI config, test fixtures) belong inside an initiative workspace or in the target application repository — not at the repo root alongside `.b2s/` and `initiatives/`.

## Rerun last action

When the user says `rerun`, `redo last`, `rerun last action`, or similar:

Read and follow `.github/prompts/b2s-rerun-last-action.prompt.md`. Do not modify state manually. Do not self-approve a gate.

## Help

When the user says `b2s-help`, `help`, or `b2s-help <phase or action>`:

Read and follow `.github/prompts/b2s-help.prompt.md`. Do not run the workflow. Do not write any files.

## No menus, no permission requests

Do not ask "Proceed?" between stages. Do not offer choices between framework steps. Run the workflow continuously until a genuine stop condition is reached. Stop conditions are defined in the framework prompts — do not invent new ones.
