---
description: Re-execute a specific named action for the active initiative, discarding its current artifact and regenerating from scratch.
---

**You** are the executor. Do not modify state manually. Do not copy or patch the previous artifact.

Use this when you want to redo a specific action by name — not just the last one.

**Cannot be used** when the action status is `accepted` (human-approved). In that case use `reject-current-gate` first, then `run-action`.

Read and follow `.b2s/prompts/run-action.md` exactly.

The user must supply an action ID (e.g. `create-bdd-scenarios`) and optionally an initiative ID (e.g. `I021`). If the action ID is missing or ambiguous, run `list-actions` for the initiative and ask the user to confirm before proceeding.
