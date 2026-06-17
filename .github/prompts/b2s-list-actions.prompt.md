---
description: List all staged actions for the active initiative with their current status (not_run / ai_validated / accepted / failed / skipped).
---

Read and follow `.b2s/prompts/list-actions.md` exactly.

If the user passed an initiative ID (e.g. `I021`) or a phase filter (e.g. `planning`), resolve the workspace root from the initiative ID and pass the phase as `--stage-id` to the CLI command as described in the prompt.

Do not run any other command. Do not write any files. Stop after printing the action list.
