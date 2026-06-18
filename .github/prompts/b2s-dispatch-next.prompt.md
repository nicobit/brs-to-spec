---
description: Run exactly one staged .b2s action for the active initiative workspace, then stop and report.
---

**You** are the executor. Do not write scripts, do not call CLI commands in a loop, do not delegate to Python.

1. Read `.b2s/prompts/run-workflow.md` in full.
2. Follow its Execution Sequence step by step for the active initiative workspace.
3. Step 5 of that sequence has three branches (A / B / C). You must identify which branch applies and follow it exactly:
   - Branch A: action is ready — execute it
   - Branch B: workflow complete — report and stop
   - Branch C: blocked — you MUST run the Blocked Diagnosis Protocol (step 6) before reporting anything

4. **Critical for Branch C:** the `blocked_reason` names the SYMPTOM stage (e.g. "stage 6-review-package is incomplete"). The CAUSE is always an earlier prerequisite stage. You must look up `blocked_by_stage` on the symptom stage's actions in `stage-actions.yaml` to find the cause stage, then diagnose actions there — not in the symptom stage.

5. If all actions in the cause stage appear `already_done` but the engine still reports blocked, run `repair-state --workspace-root WORKSPACE_ROOT` to rebuild state from disk, then restart from step 3 of the Execution Sequence.

6. Stop after exactly one action completes, one recovery completes, or a genuine stop condition is reached.
7. Report: which stage was the symptom, which was the cause, what action ran or was recovered, what artifact was produced, and what `next_action` is.

**Reporting "blocked" without completing the Blocked Diagnosis Protocol is always wrong.**
**Do not offer menus, choices, or follow-up options. Stop and report only.**
