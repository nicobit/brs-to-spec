---
description: Run the correct BRS-to-spec workflow for the active initiative. Use v2 dispatch for `.flow/` workspaces and the legacy runner only for true v1 workspaces.
---

Before running anything:

1. Read `.github/copilot-instructions.md`
2. Detect the active initiative version
   - if the workspace has `.flow/` → it is v2
   - if the workspace has `state/workflow-state.json` but no `.flow/` → it is v1

Then route as follows:

- **v2 initiative:** execute `.brs2spec2/prompts/dispatch-next.md` for the active initiative workspace
- **v1 initiative:** execute `.brs2spec/brs-to-spec-run-workflow.md` for the active initiative workspace

Never run `.brs2spec/brs-to-spec-run-workflow.md` on a v2 initiative.
