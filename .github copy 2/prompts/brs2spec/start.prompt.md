---
description: Safe start entry point. Route to v2 new-initiative or v1 start flow based on whether an active initiative already exists.
---

Before running anything:

1. Read `.github/copilot-instructions.md`
2. Scan `initiatives/`

Route as follows:

- **No initiative exists yet:** execute `.brs2spec2/prompts/new-initiative.md`
- **Active initiative has `.flow/`:** do not use the legacy v1 starter; execute `.brs2spec2/prompts/dispatch-next.md`
- **Active initiative has no `.flow/` but has v1 state:** execute `.brs2spec/00-start.md`

Never run `.brs2spec/00-start.md` against a v2 initiative.
