---
description: Implement one approved task from the active deliverable — loads initiative context first.
---

# Implement One Task

Work inside the active initiative workspace.

Follow:

```text
.brs2spec/8-copilot-implementation/01-implement-one-task.md
```

## Preconditions

Before coding, verify these exist:

```text
engineering-readiness/initiative-context.md
engineering-readiness/readiness-check.md
standalone-delivery/D1-<deliverable-name>/tasks.md
or openspec/changes/D1-<deliverable-name>/tasks.md
```

If `initiative-context.md` is missing, run the `generate-initiative-context` prompt first.

## Rule

Implement exactly one task.

Do not implement future tasks in the same pass.

Do not implement directly from raw BRS inputs.

## Output

```text
code changes
test changes
implementation summary (in PR/MR description or reviews/implementation/task-<id>-implementation-summary.md)
```
