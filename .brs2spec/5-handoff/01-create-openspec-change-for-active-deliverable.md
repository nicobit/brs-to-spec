# Prompt — Create OpenSpec Handoff per User Story

## Role

You are an engineering lead preparing a complete OpenSpec handoff for an initiative.
The output is one self-contained folder per user story — an engineer (or AI coding agent via `/opsx:apply`) picks up one folder and implements exactly one user story without opening any other artifact.

## When to use

Only when `execution_mode` is `OpenSpec` and all of the following are true:
- `engineering-readiness/readiness-check.md` exists and decision is `Ready`
- All triggered quality gates have `Status: Accepted` in their Metadata
- User stories are defined in `planning/delivery-structure.md`

## Inputs — read in this order before writing any file

1. `planning/workflow-state.json` — confirm current stage is `handoff` or `complete`
2. `planning/delivery-structure.md` — epics, features, user stories (`F-XXX.X`), increment grouping; derive the full story list from here
3. `input/brs.md` or `input/brs/*.md` — acceptance criteria (AC-NNN IDs) and functional requirements (FR-NNN); copy AC text verbatim into proposal.md, do not paraphrase
4. `engineering-readiness/initiative-context.md` — scope, integrations, constraints
5. `architecture/architecture-review.md` — initiative-specific constraints and open decisions; map each constraint to the stories it affects
6. `architecture/architecture-rules.md` — binding rules (AR-NNN IDs) engineers must follow; reference specific rule IDs in each story's constraints table
7. `input/architecture.md` — deployment topology, integration decisions
8. `quality-gates/bdd-scenarios.md` — BDD scenarios (SCN-NNN) grouped by story ID; copy the scenario IDs into each story's proposal.md BDD section
9. `quality-gates/security-review.md` — security checklist and accepted risks
10. `quality-gates/api-contract.md` — API surface, auth, error codes, contracts
11. `quality-gates/data-contract.md` — schema, PII mapping, retention, residency
12. `quality-gates/observability-plan.md` — telemetry catalog, alert rules, runbooks

**Reading rule:** read ALL inputs before generating the first story folder. Do not generate story-by-story while reading — read everything first, then generate. This ensures architecture constraints and BDD scenarios are correctly distributed across stories.

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
- User story verbatim from `delivery-structure.md` — As a / I want / so that — do not paraphrase
- Requirement ID (FR-NNN) and AC location pointing to `input/brs.md` section or AC-NNN IDs
- "Why now" — one sentence linking to the business driver or the story that unblocks this one
- What changes — bullet list of concrete system changes (endpoint name, table name, signal name); no implementation detail
- Dependencies table — filled from the dependency graph: depends-on, parallel-with, blocks
- AC table — copy each AC-NNN criterion verbatim from the BRS; add "How to verify" and "Evidence expected" and "BDD scenario(s)"; a vague paraphrase of the AC is a quality failure
- BDD scenarios table — list every SCN-NNN from `quality-gates/bdd-scenarios.md` that covers this story; include type and one-line summary; if BDD gate was not triggered write "not triggered"
- Out of scope — explicit list of what this story does NOT do; at minimum one item
- Constraints — only AR-NNN rules from `architecture/architecture-rules.md` that directly affect this story; reference the rule ID, not a generic restatement
- Reference table — paths to gate artifacts and what specifically to read there for this story

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
- Each implementation task must carry: requirement (FR-NNN), AC (AC-NNN), architecture constraint (AR-NNN if applicable), data tables touched, API endpoints touched, events to emit, evidence expected — omit only fields that genuinely do not apply
- Validation tasks: one per AC-NNN; each validation task references the BDD scenario(s) (SCN-NNN) it executes
- Done criteria must include: "All BDD scenarios SCN-NNN … pass" (list the specific IDs from proposal.md); a generic "tests pass" is a quality failure
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
- Paraphrasing AC instead of copying the verbatim criterion from the BRS — a developer cannot implement against a paraphrase
- Writing a vague AC table row ("UI shows progress") when the BRS has a specific testable criterion — use the specific criterion
- Referencing architecture constraints generically ("follow security rules") without citing the AR-NNN rule ID
- Omitting the BDD scenarios section from proposal.md — even "not triggered" must be stated explicitly
- Writing done criteria as "all tests pass" — the specific SCN-NNN IDs that must pass must be listed
- Copying the user story directly as a task — derive engineering tasks from story + architecture + gate constraints
- Ignoring architecture rules in task definitions
- Stopping after the first story — continue until all stories have a folder
- Generating the handoff before reading ALL inputs — reading inputs story-by-story causes architecture constraints to be missed
- Generating `gitlab-issues.md` or any planning-tool export
- Generating code

## Stop conditions

If any required input is missing or a quality gate is not Accepted: list what is missing, state the impact, stop.
If a story has an unresolvable dependency (blocked by a story with missing input): generate the graph and all unblocked stories, then stop and state which stories are blocked and why.

## Self-review checklist

Before finalising, verify:
- [ ] `dependency-graph.md` exists and covers all stories with wave grouping and Mermaid diagram
- [ ] One folder per user story — no increment-level folders
- [ ] Each `proposal.md` has the user story verbatim (not paraphrased)
- [ ] Each `proposal.md` AC table uses verbatim AC-NNN criteria from the BRS — not summaries
- [ ] Each `proposal.md` has a BDD scenarios section (SCN-NNN IDs or "not triggered")
- [ ] Each `proposal.md` has an out-of-scope section
- [ ] Each `proposal.md` constraints table cites AR-NNN rule IDs — not generic descriptions
- [ ] Each `proposal.md` has the dependency table filled (depends-on, parallel-with, blocks)
- [ ] Each `tasks.md` done criteria lists specific SCN-NNN IDs that must pass
- [ ] Each `design.md` omits sections that don't apply to its story
- [ ] Each task has: requirement (FR-NNN), AC (AC-NNN), evidence expected; architecture constraint (AR-NNN) and telemetry if applicable
- [ ] `specs/` files deleted when not applicable to the story
- [ ] No tasks for out-of-scope features
- [ ] No generated code
