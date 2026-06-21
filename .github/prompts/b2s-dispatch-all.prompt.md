---
description: Continue the staged .b2s workflow until a stop condition is reached.
---

**You** are the executor. Follow `.b2s/prompts/run-workflow.md` step by step.

## Execution Loop

1. Read `.b2s/prompts/run-workflow.md` in full.
2. Follow its Execution Sequence for the active initiative workspace.
3. After each action completes (step 19 of the sequence), **loop back to step 3** (run `next-step` again) and continue with the next action.
4. Keep looping until a stop condition:
   - Workflow complete (`selected_action` is null)
   - Human gate opened — handle it (see Gate Handling below)
   - Validation fails after 3 retries
   - Required input missing
   - Explicit blocker

## Per-Item Actions

When `next-step` returns `current_item` (e.g., `"E-001"`):
- This is a per-item action — the engine will select the SAME action multiple times, once per item
- Generate output for ONLY the `current_item` the engine gives you
- After `update-state`, loop back to step 3 — the engine will give you the next item
- The action is complete only when the engine stops returning it (all items done)
- Do NOT try to process all items in one pass

## Gate Handling

When a human gate is opened (`awaiting_human: true`):

1. Present the artifact for review (as described in run-workflow.md step 18).
2. Ask the user: **approve** or **reject**.
3. When the user responds:
   - **approve**: run `python .b2s/scripts/b2s_cli.py approve-current-gate --workspace-root <WORKSPACE_ROOT>`, then **continue the loop** (go back to step 3 of this prompt).
   - **reject**: run `python .b2s/scripts/b2s_cli.py reject-current-gate --workspace-root <WORKSPACE_ROOT> --reason "<reason>"`, then stop.

Do NOT tell the user to run CLI commands manually. Run them yourself.

## CLI Commands Are Mandatory

Every "Run" step in run-workflow.md means: execute the Python CLI via your shell tool. Do NOT skip commands, fabricate output files, or write state manually. The engine produces machine files — you read them.

## Reporting

After stopping, report:
- How many actions completed
- What artifacts were produced
- What caused the stop (or "workflow complete")

**Do not offer menus, choices, or follow-up options.** Stop and report only.
