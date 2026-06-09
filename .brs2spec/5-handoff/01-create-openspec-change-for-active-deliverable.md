# Prompt — Create OpenSpec Handoff per User Story

## Role

You are an engineering lead preparing a complete OpenSpec handoff for an initiative.
The output is one self-contained folder per user story — an engineer (or AI coding agent via `/opsx:apply`) picks up one folder and implements exactly one user story without opening any other artifact.

## When to use

Only when `execution_mode` is `OpenSpec` and all of the following are true:
- `engineering-readiness/readiness-check.md` exists and decision is `Ready`
- All triggered quality gates have `Status: Accepted` in their Metadata
- User stories are defined in `planning/delivery-structure.md`

## Inputs — read in this order

1. `planning/workflow-state.json` — confirm current stage is `handoff` or `complete`
2. `planning/delivery-structure.md` — epics, features, user stories (`F-XXX.X`), and increment grouping
3. `engineering-readiness/initiative-context.md` — scope, integrations, constraints
4. `architecture/architecture-rules.md` — binding rules engineers must follow
5. `input/architecture.md` — deployment topology, integration decisions
6. `quality-gates/security-review.md` — security checklist and accepted risks
7. `quality-gates/api-contract.md` — API surface, auth, error codes, contracts
8. `quality-gates/data-contract.md` — schema, PII mapping, retention, residency
9. `quality-gates/observability-plan.md` — telemetry catalog, alert rules, runbooks

## Step 1 — generate the dependency graph first

Before creating any story folder, generate:

```
openspec/changes/dependency-graph.md
```

Use `templates/openspec-handoff/dependency-graph.md`.

To build the graph:
1. List all user stories (`F-XXX.X`) from `delivery-structure.md`
2. Group them into waves based on:
   - Increment grouping from `delivery-structure.md` (D1 stories before D2 stories, etc.)
   - Shared schema dependencies (a story that creates a table blocks stories that read it)
   - Shared API dependencies (a story that creates an endpoint blocks stories that consume it)
3. Within a wave: stories that share no schema or API dependency can run in parallel
4. Generate a Mermaid `graph LR` diagram showing the dependency arrows
5. Add parallelism notes for stories in the same wave that share a component

## Step 2 — generate one folder per user story

For every user story in `delivery-structure.md`, in wave order, create:

```
openspec/changes/{{F-XXX.X}}-{{slug}}/
  proposal.md        ← story, dependencies, AC, constraints, reference table
  design.md          ← only what this story touches: API, data, integrations, observability
  tasks.md           ← ordered tasks for this story only + done criteria
  specs/
    api.md           ← only endpoints/webhooks this story creates or modifies (delete if none)
    data.md          ← only table changes this story introduces (delete if none)
    observability.md ← only signals this story must emit (delete if none)
```

Use templates from `templates/openspec-handoff/`.

After completing one story folder, immediately continue to the next — do not stop between stories.

## Output rules

### dependency-graph.md
- Waves are the primary structure — one wave per row group
- Every story appears exactly once
- Dependencies table explains WHY each dependency exists (shared table, shared endpoint, logical ordering)
- Mermaid diagram generated from the waves — use `graph LR`, one arrow per dependency
- Parallelism notes call out stories in the same wave that share a component and need coordination

### proposal.md (per story)
- User story verbatim from `delivery-structure.md` — As a / I want / so that
- Requirement ID and AC location
- "Why now" — one sentence linking to the business driver or the story that unblocks this one
- What changes — bullet list of concrete system changes, no implementation detail
- Dependencies table — filled from the dependency graph: depends-on, parallel-with, blocks
- AC table — each criterion with how to verify and evidence expected
- Constraints — only rules that apply to this story
- Reference table — paths to gate artifacts for full detail

### design.md (per story)
- Scoped to this story only — omit any section that does not apply
- "What this story touches" — one paragraph naming components, boundaries, data stores
- API surface — only endpoints this story creates or modifies; reference `specs/api.md`
- Data model — only tables this story creates or modifies; reference `specs/data.md`
- Integration points — only external calls this story makes
- Architecture constraints — only rules that directly affect this story
- Security decisions — only concerns relevant to this story
- Observability — only signals this story must emit; reference `specs/observability.md`
- Sequence diagram — only if async flow is genuinely hard to follow from text
- Open questions — items blocking this specific story

### tasks.md (per story)
- Tasks scoped to this story only — no tasks from other stories
- Task IDs use story prefix: `OS-F-XXX.X-NNN`
- Each task: requirement, AC, architecture constraint, data tables, API endpoints, events to emit, evidence expected
- Omit fields that don't apply to a task (e.g. no "Data" if task has no schema changes)
- Done criteria — short list of conditions, not implementation steps
- Reference `dependency-graph.md` for between-story ordering

### specs/ files (per story)
- `specs/api.md`: only endpoints this story touches. Delete if story has no API changes.
- `specs/data.md`: only table changes this story introduces. Delete if story has no schema changes.
- `specs/observability.md`: only signals this story emits. Delete if story emits nothing.
- Each file is thin — if a story touches one endpoint and one table, each spec file has one section

## Quality bar

A good output:
- `dependency-graph.md` is the first thing an engineering lead reads — it tells them who starts when
- Each story folder can be handed to an engineer or `/opsx:apply` with no additional context
- `design.md` + `tasks.md` + `specs/` are sufficient to implement the story — no gate artifacts needed
- Tasks are small enough to review in one PR
- Every task traces to a requirement, AC, and evidence expectation
- Telemetry emission is mandatory in every task that touches an instrumented component
- `specs/` files are thin — only the slice this story needs

## Anti-patterns

- Generating one folder per increment instead of one per user story
- Mixing tasks from multiple stories into one folder
- Leaving `specs/api.md` in a folder for a story with no API changes — delete it
- Generating a design.md with sections for the full initiative instead of this story
- Creating vague tasks (`implement backend`, `add tests`, `handle errors`)
- Copying the user story directly as a task — derive engineering tasks from story + architecture + gate constraints
- Ignoring architecture rules in task definitions
- Stopping after the first story — continue until all stories have a folder
- Generating `gitlab-issues.md` or any planning-tool export
- Generating code

## Stop conditions

If any required input is missing or a quality gate is not Accepted: list what is missing, state the impact, stop.
If a story has an unresolvable dependency (blocked by a story with missing input): generate the graph and all unblocked stories, then stop and state which stories are blocked and why.

## Self-review checklist

Before finalising, verify:
- [ ] `dependency-graph.md` exists and covers all stories with wave grouping and Mermaid diagram
- [ ] One folder per user story — no increment-level folders
- [ ] Each `proposal.md` has the dependency table filled (depends-on, parallel-with, blocks)
- [ ] Each `design.md` omits sections that don't apply to its story
- [ ] Each task has: requirement, AC, evidence expected; telemetry if applicable
- [ ] `specs/` files deleted when not applicable to the story
- [ ] No tasks for out-of-scope features
- [ ] No generated code
