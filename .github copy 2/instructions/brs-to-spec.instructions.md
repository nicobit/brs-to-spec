---
applyTo: "**"
---

## Framework activation — always active

This repository contains the brs-to-spec framework. Apply framework behavioral rules in every session, regardless of which file is open.

## Load at session start — always

Read these two files first, before anything else:

1. `.brs2spec2/agent-instructions.md` — v2 behavioral rules, session startup, trigger mapping, hard rules
2. `.flow-engine/instructions/dispatcher.md` — event dispatch protocol (21 steps)

These load unconditionally. They define what to do for every user request including "new initiative", "dispatch-next", "status", and "show queue".

## Determine active version after loading

Scan `initiatives/` for workspaces:

- Workspace has `.flow/` folder → **v2 initiative** — use `.brs2spec2/` and the flow-engine dispatcher
- Workspace has no `.flow/` folder → **v1 initiative** — use `.brs2spec/` and `.brs2spec/brs-to-spec-run-workflow.md`
- No workspaces exist yet → no active initiative; wait for user to say "new initiative"

## v2 user entry points

The complete trigger-to-action mapping is in `.brs2spec2/agent-instructions.md` Section 4 (loaded above). That file is authoritative — do not use the short list below as a substitute, use it only as a quick reference for the most common commands.

| User says | Action |
|---|---|
| "new initiative" / "create initiative" | Read and execute `.brs2spec2/prompts/new-initiative.md` |
| "dispatch-next" / "next" | Read and execute `.brs2spec2/prompts/dispatch-next.md` |
| "dispatch-all" / "continue" | Read and execute `.brs2spec2/prompts/dispatch-all.md` |
| "status" | Read `.flow/state/workflow-state.json` and report |
| "show queue" | List `.flow/events/pending/` with blocked/unblocked status |
| "repair processing" / "fix processing" | Read and execute `.brs2spec2/prompts/repair-processing.md` |
| "repair chain" / "fix chain" / "repair queue" | Read and execute `.brs2spec2/prompts/repair-chain.md` |
| "archive done" / "cleanup events" | Read and execute `.brs2spec2/prompts/archive-done.md` |

**For any command not listed here: check Section 4 of `.brs2spec2/agent-instructions.md` before deciding what to do. Never improvise a response to an unrecognised command.**

## Hard stop — before writing any file outside `input/` in a v2 initiative

Follow the event queue. Do not write artifacts directly. Execute the next unblocked event in `.flow/events/pending/` through the dispatcher.

## Hard stop — when dispatcher stops with "queue empty but initiative not complete"

Do NOT write any artifact. Do NOT modify workflow-state.json. Do NOT offer alternatives.
Report the stop condition exactly as written and wait for the user to say "repair chain".

## Hard stop — before creating any file in a v1 initiative

1. STOP. Do not create anything yet.
2. Identify the active initiative workspace (`initiatives/<id>-<slug>/`).
3. Check whether `state/workflow-state.json` exists in that workspace.
4. Run `.brs2spec/brs-to-spec-run-workflow.md`.

Only create files that the workflow runner explicitly instructs you to create, at the path it specifies.

## Input boundary rule

`initiatives/<id>/input/` is the only folder you may write to directly without running the workflow first. Everything outside `input/` is produced by framework events (v2) or skills (v1) only.

## No menus, no permission requests

Do not ask "Proceed?" between stages. Do not offer choices between framework steps. Run continuously until a genuine stop condition is reached.
