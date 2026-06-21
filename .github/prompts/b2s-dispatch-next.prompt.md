---
description: Run exactly one staged .b2s action for the active initiative workspace, then stop and report.
---

**You** are the executor. Follow `.b2s/prompts/run-workflow.md` step by step.

1. Read `.b2s/prompts/run-workflow.md` in full.
2. Follow its Execution Sequence for the active initiative workspace.
3. Branch handling (step 5):
   - Branch A: action is ready — execute it (one action only)
   - Branch B: workflow complete — report and stop
   - Branch C: blocked — run Blocked Diagnosis Protocol before reporting

4. If the action is per-item (`current_item` present in `next-step.json`):
   - Process ONLY the `current_item` the engine gives you
   - After `update-state`, stop and report (dispatch-next runs one item only)

5. Stop after exactly one action completes (or one item for per-item actions).

## Gate Handling

When a human gate is opened (`awaiting_human: true`):

1. Present the artifact for review.
2. Ask the user: **approve** or **reject**.
3. When the user responds:
   - **approve**: run `python .b2s/scripts/b2s_cli.py approve-current-gate --workspace-root <WORKSPACE_ROOT>`, then stop and report.
   - **reject**: run `python .b2s/scripts/b2s_cli.py reject-current-gate --workspace-root <WORKSPACE_ROOT> --reason "<reason>"`, then stop.

Do NOT tell the user to run CLI commands manually. Run them yourself.

## CLI Commands Are Mandatory

Every "Run" step in run-workflow.md means: execute the Python CLI via your shell tool. Do NOT skip commands, fabricate output files, or write state manually.

## Reporting

Report: which action ran, what artifact was produced, what `next_action` is.

**Do not offer menus, choices, or follow-up options. Stop and report only.**
