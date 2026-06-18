# BRS to Spec Framework — Copilot Instructions

Framework behavioral rules are in `.github/instructions/brs-to-spec.instructions.md`.

This file is intentionally minimal.

## Framework activation — always active

At the start of every session, always load:

1. `.b2s/agent-instructions.md`
2. `.b2s/prompts/run-workflow.md`

These two files are the authoritative behavioral contract for this framework. Load them before responding to any user request.

## Framework routing

- Initiative workspace has `.b2s/` folder → use `.b2s/`
- Ignore legacy `.brs2spec/`, `.brs2spec2/`, and `.flow-engine/` routing for active Copilot behavior

## Hard stop — when asked to create a new initiative

When the user says anything like "create initiative", "new initiative", "initialize I0XX-...", or "set up a new workspace":

1. Do NOT create any files or folders manually.
2. Do NOT create `initiative.yaml`, `00-start.md`, `README.md`, or any file not produced by the CLI.
3. Do NOT copy or recreate the `.b2s/` framework folder inside the initiative workspace.
4. Use `.github/prompts/b2s-new-initiative.prompt.md` — follow it exactly.

## Rerun last action

When the user says `rerun`, `redo last`, `rerun last action`, or similar:

Read and follow `.github/prompts/b2s-rerun-last-action.prompt.md`. Do not modify state manually. Do not self-approve a gate.

## Help

When the user says `b2s-help`, `help`, or `b2s-help <phase or action>`:

Read and follow `.github/prompts/b2s-help.prompt.md`. Do not run the workflow. Do not write any files.

## Hard stop — before creating any file or folder inside `initiatives/`

1. Identify the active initiative workspace.
2. Use `.b2s/prompts/run-workflow.md` for staged execution.
3. Do not follow event queues or `.flow/` buckets.

## Hard stop — before answering "what should I do?" or "what is next?"

Read `.b2s/state/workflow-state.json` when it exists, then use `.b2s/prompts/run-workflow.md` and the `.b2s` engine outputs to determine the next staged action.

Do not invent next steps. Do not summarize the BRS. Run the workflow.

## Hard stop — when staged state is inconsistent or blocked

Do NOT invent progress. Do NOT bypass validation or gates.
Use `.github/prompts/b2s-repair-chain.prompt.md` (repair), `.github/prompts/b2s-reset-to-phase.prompt.md` (rewind to a stage), or `.github/prompts/b2s-resume.prompt.md` (repair/retry/reset decision then continue) only when the user explicitly triggers repair, reset, or resume.
