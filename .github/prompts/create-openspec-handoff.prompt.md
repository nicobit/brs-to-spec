---
description: Create OpenSpec handoff — one folder per user story with dependency graph showing execution order and parallelism.
---

# Create OpenSpec Handoff

Work inside the active initiative workspace.

Use:

```text
.brs2spec/5-handoff/01-create-openspec-change-for-active-deliverable.md
templates/openspec-handoff/
```

## Preconditions

Before creating OpenSpec handoff, verify:

```text
planning/workflow-state.json              current_stage = handoff or complete
engineering-readiness/readiness-check.md  decision = Ready
quality-gates/security-review.md          Status: Accepted
quality-gates/api-contract.md             Status: Accepted
quality-gates/data-contract.md            Status: Accepted
quality-gates/observability-plan.md       Status: Accepted
```

If any gate is not Accepted, stop and report which gate is blocking.

## Output

**Step 1 — dependency graph (generate this first):**

```text
openspec/changes/dependency-graph.md
```

Shows all user stories grouped into waves (parallel execution groups), dependency arrows between stories, and a Mermaid diagram. The engineering lead reads this to assign work.

**Step 2 — one folder per user story:**

```text
openspec/changes/{{F-XXX.X}}-{{slug}}/
  proposal.md          user story, dependencies, AC, constraints, reference table
  design.md            only what this story touches: API, data, integrations, observability
  tasks.md             tasks for this story only + done criteria
  specs/
    api.md             only endpoints this story creates or modifies (delete if none)
    data.md            only table changes this story introduces (delete if none)
    observability.md   only signals this story must emit (delete if none)
```

Generate all stories in wave order without stopping between them.

## Key rules

- Dependency graph first — before any story folder
- One folder per user story (`F-XXX.X`) — not per increment
- Each folder is self-contained: engineer implements from `design.md` + `tasks.md` + `specs/` only
- `specs/` files are deleted when not applicable to the story
- Do not generate `gitlab-issues.md` or any planning-tool export
- Do not generate code
- Do not stop after the first story — continue until all stories have a folder

## After generating

Tell the engineer:
1. Read `openspec/changes/dependency-graph.md` first — it shows who starts when and what can run in parallel
2. Copy each story folder into the target code repository as work is assigned
3. Run `/opsx:apply` per story folder to start implementation
