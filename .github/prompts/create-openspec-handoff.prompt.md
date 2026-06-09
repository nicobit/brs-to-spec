---
description: Create OpenSpec handoff for the active delivery increment (proposal, design, tasks, specs/).
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
planning/workflow-state.json        current_stage = handoff
engineering-readiness/readiness-check.md   decision = Ready
quality-gates/security-review.md    Status: Accepted
quality-gates/api-contract.md       Status: Accepted
quality-gates/data-contract.md      Status: Accepted
quality-gates/observability-plan.md Status: Accepted
```

If any gate is not Accepted, stop and report which gate is blocking.

## Output

Create one folder per active delivery increment:

```text
openspec/changes/{{deliverable-id}}-{{slug}}/
  proposal.md          why, scope, constraints, reference table
  design.md            self-contained technical context (API, data, integrations, observability)
  tasks.md             ordered implementation checklist with full traceability
  specs/
    api.md             distilled API surface and integration contracts for this increment
    data.md            distilled data model changes, PII mapping, migration notes
    observability.md   mandatory telemetry signals, alerts, runbook references
```

## Key rules

- One folder per increment — generate all increments defined in `planning/delivery-structure.md` in sequence, each in its own folder (`D1-<slug>/`, `D2-<slug>/`, etc.). Do not stop after D1.
- `design.md` must be self-contained: engineer implements from `design.md` + `tasks.md` + `specs/` only
- `specs/` distils the relevant slice of each gate artifact — do not inline the full gate content
- Do not generate `gitlab-issues.md` or any planning-tool export
- Do not generate code

## After generating

Tell the engineer:
1. Copy the `openspec/changes/{{deliverable-id}}-{{slug}}/` folder into the target code repository
2. Run `/opsx:apply` in the code repository to start implementation
3. The `specs/` folder travels with the handoff folder — it is the engineer's reference during coding
