---
description: Create OpenSpec handoff for the active deliverable.
---

# Create OpenSpec Handoff

Work inside the active feature workspace.

Use:

```text
prompts/5-handoff/01-create-openspec-change-for-active-deliverable.md
templates/openspec-handoff/
```

## Preconditions

Before creating OpenSpec handoff, verify:

```text
engineering-readiness/readiness-check.md exists
required quality gates are completed or explicitly accepted as risk
active deliverable is clear
```

## Output

Create:

```text
openspec/changes/D1-<deliverable-name>/
  proposal.md
  design.md
  tasks.md
```

Do not create tasks for the whole BRS.
