---
description: Continue the staged .b2s workflow until a stop condition is reached.
---

**You** are the executor. Do not write scripts, do not call CLI commands in a loop, do not delegate to Python.

1. Read the file `.b2s/prompts/run-workflow.md` in full.
2. Follow its Execution Sequence yourself, step by step, for the active initiative workspace.
3. Continue staged execution — repeating the sequence from step 2 of the workflow — until one of these stop conditions is reached:
   - workflow is complete (`selected_action` is null)
   - a human gate is opened (`awaiting_human: true`)
   - validation fails and cannot be self-corrected
   - a required input is missing
   - an explicit blocker is surfaced
4. After stopping, report: how many actions completed, what artifacts were produced, and what caused the stop (or "workflow complete").

**Do not offer menus, choices, or follow-up options after stopping.** Do not ask "Would you like...". Stop and report only.
