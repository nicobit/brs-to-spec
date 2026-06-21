---
applyTo: "**"
---

## Framework activation — always active

This repository contains the brs-to-spec framework. Apply framework behavioral rules in every session, regardless of which file is open.

## Load at session start — always

Read these files first, before anything else:

1. `.b2s/agent-instructions.md` — staged framework behavioral rules
2. `.b2s/prompts/run-workflow.md` — staged orchestration loop
3. `.b2s/module-index.md` — action-to-skill and artifact routing reference

These load unconditionally. They define what to do for every user request including "new initiative", "dispatch-next", "continue", "status", "reset to phase", and "resume".

## Determine active framework after loading

Scan `initiatives/` for workspaces:

- Workspace has `.b2s/` folder → **active staged initiative** — use `.b2s/`
- Workspace has no `.b2s/` folder yet → **staged initiative target** — initialize and use `.b2s/`
- Ignore legacy `.brs2spec/`, `.brs2spec2/`, and `.flow-engine/` paths for active Copilot behavior
- No workspaces exist yet → no active initiative; wait for user to say "new initiative"

## `.b2s` user entry points

Use the staged prompts and engine outputs. The quick reference below is authoritative for Copilot routing in this repository.

| User says | Action |
|---|---|
| "new initiative" / "create initiative" | Follow `.github/prompts/b2s-new-initiative.prompt.md` |
| "dispatch-next" / "next" | Execute exactly one staged action using `.b2s/prompts/run-workflow.md` |
| "dispatch-all" / "continue" | Continue staged execution using `.b2s/prompts/run-workflow.md` until a stop condition is reached |
| "status" / "what is next" | Read `.b2s/state/workflow-state.json` and `.b2s/state/next-step.json` when present, otherwise run staged next-step selection |
| "repair processing" / "fix processing" | Follow `.github/prompts/b2s-repair-chain.prompt.md` |
| "repair chain" / "fix chain" / "repair queue" | Follow `.github/prompts/b2s-repair-chain.prompt.md` |
| "reset to <phase>" / "rewind to <phase>" | Follow `.github/prompts/b2s-reset-to-phase.prompt.md` |
| "resume" / "resume from <phase>" | Follow `.github/prompts/b2s-resume.prompt.md` |
| "rerun" / "redo last" / "rerun last action" | Follow `.github/prompts/b2s-rerun-last-action.prompt.md` |
| "b2s-help" / "help" / "b2s-help <phase or action>" | Follow `.github/prompts/b2s-help.prompt.md` |

## Hard stop — before writing any file outside `input/` in an initiative workspace

Use the staged `.b2s` workflow. Do not follow `.flow/` event buckets and do not use `.brs2spec2` dispatch prompts.

## Hard stop — when staged workflow is blocked or inconsistent

Do NOT invent artifacts or modify state freehand.
Stop and use the staged repair or reset prompts only when the user explicitly triggers them.

## Input boundary rule

`initiatives/<id>/input/` is the only folder you may write to directly without running the workflow first. Everything outside `input/` is produced by staged `.b2s` actions only.

## No menus, no permission requests

Do not ask "Proceed?" between stages. Do not offer choices between framework steps. Run continuously until a genuine stop condition is reached.

## Machine-file contract — enforced by the engine

The engine owns all files under `.b2s/state/` and `.b2s/tmp/` in every initiative workspace. Do not write to these paths directly.

- **`workflow-state.json`** — read-only for agents. Use CLI commands to change state.
- **`execution-log.jsonl`** — engine-written only. Every entry is fingerprinted; fabricated entries are detected on the next `dispatch-next` call.
- **CLI output files** (`next-step.json`, `current-inputs.json`, `current-validation.yaml`, `current-state-update.json`, `current-gate.json`) — engine-written only.
- **Gate approval** — run `approve-current-gate` or `reject-current-gate` via the CLI. Do not edit `awaiting_human` or `current_gate` by hand.

Violations are surfaced as `integrity_warnings` in `dispatch-next` output.
