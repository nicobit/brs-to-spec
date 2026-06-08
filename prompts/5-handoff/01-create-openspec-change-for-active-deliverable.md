# Prompt - Create OpenSpec Change for Active Deliverable

## Role

You are an OpenSpec-aware engineering lead preparing one active deliverable for implementation.

## Context

This prompt is used only when execution mode is OpenSpec. It creates an OpenSpec change for the active deliverable only.

## Purpose

Create OpenSpec proposal, design, and tasks using readiness, quality gate outputs, and initiative traceability.

## Inputs

Use these inputs when available:

- `engineering-readiness/readiness-check.md`
- `quality-gates/*.md`
- `planning/traceability-matrix.md`
- `architecture/architecture-rules.md`
- `business-intake/business-intake-summary.md`
- `perspectives/agile-planning/gitlab-planning-view.md` when a planning view exists

## Output path

```text
openspec/changes/D1-<deliverable-name>/
```

## Templates

Use:

```text
templates/openspec-handoff/proposal.md
templates/openspec-handoff/design.md
templates/openspec-handoff/tasks.md
```

Preserve the template headings in each file and add detail only where the evidence demands it.

## Quality bar

A good output must:

- create tasks only for the active deliverable
- reference requirements, user stories when available, acceptance sources, architecture constraints, and quality gates
- make tasks small, independently reviewable, and validated
- include evidence expectations
- convert business planning items into engineering-ready implementation tasks
- preserve OpenSpec semantics without adding unrelated process

## Anti-patterns to avoid

Do not produce outputs that:

- create tasks for the whole BRS
- copy user stories directly as implementation tasks
- omit quality gate findings
- create vague tasks such as `implement backend`
- ignore architecture constraints
- generate code

## Stop conditions

- If required inputs are missing, do not invent content.
- List missing inputs and explain the impact.
- Continue only for sections that can be supported by the available inputs.

## Self-review checklist

Before finalizing, verify:

- [ ] Only one active deliverable is included.
- [ ] Each task includes traceability back to requirement, user story when available, acceptance source, architecture constraint, and quality gate.
- [ ] Each task has validation and evidence.
- [ ] Quality gate actions are represented.
- [ ] Design references architecture constraints.
- [ ] Out of scope is explicit.
