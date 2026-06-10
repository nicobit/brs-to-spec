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
4. `input/repositories/` — **if this folder exists**, read every `.md` file in it; each file describes one repository and its file name (without extension) is the subfolder name used in the handoff output; if the folder does not exist or is empty, skip and use the flat folder structure (no repo subfolders)
5. `engineering-readiness/initiative-context.md` — scope, integrations, constraints
6. `architecture/architecture-review.md` — initiative-specific constraints and open decisions; map each constraint to the stories it affects
7. `architecture/architecture-rules.md` — binding rules (AR-NNN IDs) engineers must follow; reference specific rule IDs in each story's constraints table
8. `input/architecture.md` — deployment topology, integration decisions
9. `quality-gates/bdd-scenarios.md` — BDD scenarios (SCN-NNN) grouped by story ID; copy the scenario IDs into each story's proposal.md BDD section
10. `quality-gates/security-review.md` — security checklist and accepted risks
11. `quality-gates/api-contract.md` — API surface, auth, error codes, contracts
12. `quality-gates/data-contract.md` — schema, PII mapping, retention, residency
13. `quality-gates/observability-plan.md` — telemetry catalog, alert rules, runbooks

**Reading rule:** read ALL inputs before generating the first story folder. Do not generate story-by-story while reading — read everything first, then generate. This ensures architecture constraints and BDD scenarios are correctly distributed across stories.

## Mermaid syntax rules — mandatory for all diagrams

- **Never use HTML tags in node labels.** `<br/>`, `<b>`, `<i>` cause parse errors. Use ` / ` or ` — ` as separators.
  Wrong: `F001_1["Story name<br/>(React)"]`
  Correct: `F001_1["Story name (React)"]`
- **Always quote node labels that contain parentheses, commas, slashes, or spaces.**
  Correct: `F001_1["F-001.1 — Story name"]`
  Wrong: `F001_1[F-001.1 — Story name]`
- **`graph LR` node IDs must use only letters, digits, and underscores** — replace hyphens and dots with underscores: `F-001.1` → `F001_1`.
- **`sequenceDiagram` participant names with spaces must be quoted:** `participant "API Gateway"` not `participant API Gateway`.
- **Never put raw parentheses inside `[]` without wrapping the whole label in double quotes.**

## Step 1 — generate the dependency graph first

Before creating any story folder, generate:

```
openspec/changes/dependency-graph.md
```

Use `.brs2spec/templates/openspec-handoff/dependency-graph.md`.

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

For every user story in `delivery-structure.md`, in wave order, create one folder. The internal structure depends on whether `input/repositories/` exists:

---

### Case A — no `input/repositories/` folder (or folder is empty)

Flat structure, same as before:

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

---

### Case B — `input/repositories/` exists and contains at least one descriptor file

One subfolder per repository that this story touches. The subfolder name is the descriptor file name without its `.md` extension (e.g. `input/repositories/api.md` → subfolder `api/`).

```
openspec/changes/{{F-XXX.X}}-{{slug}}/
  dependency-graph.md   ← story-level dependency graph (same as Case A; only the cross-repo one lives here)
  {{repo-a}}/
    proposal.md         ← story scope scoped to this repo's changes only
    design.md           ← only what this story changes in this repo
    tasks.md            ← tasks for this repo only + done criteria referencing SCN-NNN
    specs/
      api.md            ← only endpoints this repo creates or modifies (delete if none)
      data.md           ← only schema changes in this repo (delete if none)
      observability.md  ← only signals this repo emits (delete if none)
  {{repo-b}}/
    proposal.md
    design.md
    tasks.md
    specs/
      ...
```

#### Inferring which repos a story touches

Read each repo descriptor in `input/repositories/`. Apply the following inference in order — stop at the first match:

1. **Primary signal — Functional areas list:** if the descriptor has a `## Functional areas` section, check whether the story's FR-NNN appears in that list. If yes, this repo gets a subfolder for this story. If no, move to step 2.
2. **Fallback — Responsibility description:** if the story's AC or FR references capabilities described in the repo's `## Responsibility` section (API endpoints, database tables, UI views, background jobs), include the repo.
3. **Architecture fallback:** if the architecture assigns this story's functional area to this repo (e.g. via an AR-NNN rule or topology note), include the repo.

Include only repos where at least one criterion matched. A story that is purely a backend API change does not get a `ui/` subfolder. A story that only changes the UI does not get a `db/` subfolder. When uncertain between two repos, include both and add an open question to the story's `proposal.md`.

#### Per-repo proposal.md scope

Each `{{repo}}/proposal.md` describes only the changes in that repo:
- **Repository scope line** — fill the "Repository scope" line at the top of the template with the descriptor file name (without `.md`) as `{{repo-name}}` and the story ID as `{{F-XXX.X}}`; e.g. `This proposal covers the \`api\` repository slice of story F-001.1.` Remove this line entirely in Case A (flat structure).
- "What changes in this repo" — bullet list scoped to this repo's responsibilities
- AC table — only ACs that this repo's changes satisfy
- BDD scenarios — only SCN-NNN scenarios that test this repo's behavior
- Out of scope — what this story does NOT change in this specific repo
- Dependencies — on other repos' outputs; **uncomment and fill the cross-repo dependency table** in the template for any intra-story repo dependency that applies (e.g. `ui` depends on `api` for the endpoint contract); leave the table commented out only if this repo has no intra-story dependency on another repo

#### Per-repo tasks.md scope

Each `{{repo}}/tasks.md`:
- **Repository scope line** — fill the same way as proposal.md: descriptor file name as `{{repo-name}}`, story ID as `{{F-XXX.X}}`; remove the line in Case A.
- Tasks scoped to this repo's work only — no tasks from other repos' subfolders
- Done criteria references the cross-repo dependency: "notify `{{other-repo}}` team when this repo's contract is stable" where applicable

#### Cross-repo dependency note in dependency-graph.md

When Case B applies, the story-level `dependency-graph.md` (at `openspec/changes/dependency-graph.md`) gains a cross-repo section listing, for each story: which repo subfolder depends on which other repo subfolder (e.g. `F-001.1/ui` depends on `F-001.1/api` contract being stable).

---

Use templates from `.brs2spec/templates/openspec-handoff/` for all `proposal.md`, `design.md`, `tasks.md`, and `specs/` files regardless of case.

After completing one story folder, immediately continue to the next — do not stop between stories.

## Output rules

### Folder structure decision (repeat of Step 2 — apply consistently)

Check once at the start: does `input/repositories/` contain at least one `.md` file? If yes → Case B (repo subfolders) for every story. If no → Case A (flat) for every story. Do not mix cases across stories in the same handoff.

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
- Using repo subfolders when `input/repositories/` does not exist or is empty — only add subfolders when repo descriptors are present
- Using flat structure when `input/repositories/` exists with at least one descriptor — the subfolder structure is mandatory in that case
- Creating a repo subfolder for a repo that the story does not touch — infer from story AC, BRS, and architecture; do not create empty or placeholder repo subfolders
- Using a subfolder name that does not match the descriptor file name (e.g. using `backend/` when the descriptor file is `api.md`)
- Mixing Case A and Case B across stories in the same handoff run

## Stop conditions

If any required input is missing or a quality gate is not Accepted: list what is missing, state the impact, stop.
If a story has an unresolvable dependency (blocked by a story with missing input): generate the graph and all unblocked stories, then stop and state which stories are blocked and why.

## Self-review checklist

Before finalising, verify:
- [ ] `dependency-graph.md` exists and covers all stories with wave grouping and Mermaid diagram
- [ ] Folder structure is consistent: all stories use Case A (flat) or all use Case B (repo subfolders) — never mixed
- [ ] If Case B: every repo subfolder name matches the corresponding `input/repositories/` descriptor file name (without `.md`)
- [ ] If Case B: no empty or placeholder repo subfolders — only repos the story actually touches have a subfolder
- [ ] If Case B: cross-repo dependencies are noted in `dependency-graph.md`
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
