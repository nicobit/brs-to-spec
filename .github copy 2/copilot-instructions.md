# BRS to Spec Framework — Copilot Instructions

Framework behavioral rules are in `.github/instructions/brs-to-spec.instructions.md`.

This file is intentionally minimal.

## Framework activation — always active

At the start of every session, always load:

1. `.brs2spec2/agent-instructions.md`
2. `.flow-engine/instructions/dispatcher.md`

These two files are the authoritative behavioral contract for this framework. Load them before responding to any user request.

## Version routing

- Initiative workspace has `.flow/` folder → v2, use `.brs2spec2/`
- Initiative workspace has no `.flow/` folder → v1, use `.brs2spec/`
- No initiative exists yet → load v2 rules and wait for "new initiative"

## Hard stop — before creating any file or folder inside `initiatives/`

**v2 initiative (has `.flow/`):**
Follow the event queue. Read `.brs2spec2/prompts/dispatch-next.md` and execute the next pending event. Do not write artifacts directly.

**v1 initiative (no `.flow/`):**
1. STOP. Do not create anything yet.
2. Identify the active initiative workspace.
3. Run `.brs2spec/brs-to-spec-run-workflow.md`.

## Hard stop — before answering "what should I do?" or "what is next?"

**v2:** Read `.flow/state/workflow-state.json` and list the next unblocked event in `pending/`.
**v1:** Read `state/workflow-state.json` and run `.brs2spec/brs-to-spec-run-workflow.md`.

Do not invent next steps. Do not summarize the BRS. Run the workflow.

## Hard stop — when dispatcher reports "queue empty but initiative not complete"

Do NOT write any artifact. Do NOT modify workflow-state.json. Do NOT offer menus or alternatives.
Report the exact stop message and wait for the user to say "repair chain".
The complete recovery procedure is in `.brs2spec2/prompts/repair-chain.md` — read and execute it only when the user triggers it.
