# Prompt � Create OpenSpec Handoff per User Story

## Role

You are an engineering lead preparing a complete OpenSpec handoff for an initiative.
The output is one self-contained folder per user story � an engineer (or AI coding agent via `/opsx:apply`) picks up one folder and implements exactly one user story without opening any other artifact.

## When to use

Only when `execution_mode` is `OpenSpec` and all of the following are true:
- `engineering-readiness/readiness-check.md` exists and decision is `Ready`
- All triggered quality gates have `Status: Accepted` in their Metadata
- User stories are defined in `planning/delivery-structure.md`

## Inputs � read in this order before writing any file

> Context packaging: apply the handoff generation profile from `.brs2spec/agent-instructions.md` ? **Context packaging for downstream AI tasks**. Items 1�7 below are required; items 8�13 follow the authoritative/optional rules in that profile.

1. `state/workflow-state.json` � confirm current stage is `handoff` or `complete`
2. `planning/delivery-structure.md` � epics, features, user stories (`F-XXX.X`), increment grouping; derive the full story list from here
3. `input/brs.md` or `input/brs/*.md` � acceptance criteria (AC-NNN IDs) and functional requirements (FR-NNN); copy AC text verbatim into story.md, do not paraphrase
4. `input/repositories/` � **if this folder exists**, read every `.md` file in it **fully** before generating any output. Each file describes one repository:
   - File name (without `.md`) = subfolder name in handoff output and alias in `specs/by-repository/`
   - `## Functional areas` + `## Responsibility` ? used to assign stories to repos (primary + fallback signal)
   - `## Technology` ? used to populate repo-context.md and coding-prompt.md header
   - `## Module map` ? used to derive accurate folder-level candidate file paths in coding-prompt.md "Candidate files to touch"
   - `## Build and test commands` ? copied **verbatim** into coding-prompt.md "Validation commands" for every story in this repo; do not infer from tech stack name when descriptor has explicit commands
   - `## Coding standards` ? used to populate repo-context.md coding standards table
   - `## Files and areas not to touch` ? merged with AR-NNN forbidden patterns into "What you must NOT do" in coding-prompt.md; applies to every story in this repo
   - `## Relevant constraints` ? repo-specific AR-NNN rules; include in coding-prompt.md AR-NNN table alongside global architecture-rules.md rules
   - If the folder does not exist or is empty: skip and use flat structure (Case A)
5. `engineering-readiness/initiative-context.md` � scope, integrations, constraints
6. `architecture/architecture-review.md` � initiative-specific constraints and open decisions; map each constraint to the stories it affects
7. `architecture/architecture-rules.md` � **AUTHORITATIVE**: binding rules (AR-NNN IDs) engineers must follow; reference specific rule IDs in each story's constraints table; these override any conflicting note in design.md or delivery-structure.md
8. `business-intake/business-rules.md` � **if present**: BR-NNN rules with BRS source refs; reference matching BR-NNN IDs in each story's constraints table alongside AR-NNN rules; also used to populate `coding-prompt.md` business rules section
9. `input/architecture.md` � deployment topology, integration decisions
10. `quality-gates/security-review.md` � **AUTHORITATIVE**: security checklist and accepted risks
11. `quality-gates/api-contract.md` � **AUTHORITATIVE**: API surface, auth, error codes, contracts
12. `quality-gates/data-contract.md` � **AUTHORITATIVE**: schema, PII mapping, retention, residency
13. `quality-gates/observability-plan.md` � **AUTHORITATIVE**: telemetry catalog, alert rules, runbooks
14. `quality-gates/bdd/F-NNN.md` � **if BDD gate triggered**: SCN-NNN scenario IDs per feature; used to populate `coding-prompt.md` BDD section for each story
15. `input/codebase-context.md` � **if exists**: repo structure, patterns to follow, files not to touch, existing capabilities map, validation commands; used to populate `coding-prompt.md` files-to-touch table and validation commands section; if missing, note the gap in dependency-graph.md preamble

**Reading rule:** read ALL inputs before generating the first story folder. Do not generate story-by-story while reading � read everything first, then generate. This ensures architecture constraints and AR-NNN rules are correctly distributed across stories. For Case B: read ALL repository descriptors fully � not just the Functional areas section � before generating any story folder. The module map, build commands, coding standards, and exclusions affect every story in the repo.

**Fast Path:** items 8�13 may not exist. Skip any that are missing; note the omission in the dependency-graph.md preamble. Items 1�7 are still required.

## Mermaid syntax rules

> Apply the canonical Mermaid syntax rules and self-review checklist from `.brs2spec/agent-instructions.md` ? **Mermaid syntax rules � canonical source**. Do not duplicate them here.
>
> Dependency graph node IDs follow the story ID convention: replace hyphens and dots with underscores � `F-001.1` ? `F001_1`. For repo-subfolder nodes append underscore + repo name: `F001_1_api`.

## Step 1 � generate the dependency graph first

Before creating any story folder, generate:

```
specs/dependency-graph.md
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

## Step 2 � generate one folder per user story

> **HARD STOP before creating any folder:**
> 1. Count the `F-XXX.X` story IDs in `planning/delivery-structure.md`. Write that number down.
> 2. You must create exactly that many folders � one per story ID, named `F-XXX.X-<slug>/`.
> 3. **Never create a folder named after the deliverable or the epic** (e.g. `core-loan-origination-intake/`, `F-001-applicant-intake/`). Those are wrong. Every folder name must start with a story ID: `F-001.1-`, `F-001.2-`, etc.
> 4. If you are uncertain whether to create one folder or many � the answer is always many: one per `F-XXX.X` story ID, no exceptions.

> **Story-count assertion � run before creating the first folder:**
>
> 1. List every `F-XXX.X` ID found in `planning/delivery-structure.md` (or the delivery structure folder). Write the list explicitly: `F-001.1, F-001.2, F-002.1, ...`
> 2. Count them. Write the count: `N stories found.`
> 3. Confirm: `I will create exactly N folders: specs/F-001.1-<slug>/, specs/F-001.2-<slug>/, ...`
> 4. Do not begin creating folders until this assertion is written out.
>
> **If the delivery structure is corrupt (multiple versions concatenated):**
> - Do not attempt to extract story IDs from a corrupt delivery-structure file.
> - Stop. State: `planning/delivery-structure.md is corrupt (multiple concatenated versions). Execute repair-workspace-state.md before running the handoff.`
> - Do not create any folder. Do not write any file.
>
> **If the delivery structure is in draft state (epics/features only, no F-XXX.X story IDs):**
> - Do not proceed to handoff.
> - Stop. State: `planning/delivery-structure.md is still at draft stage � no F-XXX.X story IDs found. Execute stage 9 (delivery-structure-confirmed) first.`
> - Do not create any folder. Do not write any file.

**Default is Case A (single-repo, flat).** Only switch to Case B if `input/repositories/` exists and contains at least one `.md` file. When Case A applies, do not mention repositories, repo descriptors, or multi-repo concepts anywhere in the output � they are irrelevant.

For every user story in `delivery-structure.md`, in wave order, create one folder. The internal structure depends on whether `input/repositories/` exists:

---

### Case A � no `input/repositories/` folder (or folder is empty)

Flat structure, same as before:

```
specs/{{F-XXX.X}}-{{slug}}/
  story.md           ? user story, AC (verbatim), full BDD Gherkin, dependencies, constraints
  design.md          ? only what this story touches: API, data, integrations, observability
  tasks.md           ? ordered tasks for this story only + done criteria
  specs/
    api.md           ? only endpoints/webhooks this story creates or modifies (delete if none)
    data.md          ? only table changes this story introduces (delete if none)
    observability.md ? only signals this story must emit (delete if none)
```

---

### Case B � `input/repositories/` exists and contains at least one descriptor file

One subfolder per repository that this story touches. The subfolder name is the descriptor file name without its `.md` extension (e.g. `input/repositories/api.md` ? subfolder `api/`).

```
specs/{{F-XXX.X}}-{{slug}}/
  dependency-graph.md   ? story-level dependency graph (same as Case A; only the cross-repo one lives here)
  {{repo-a}}/                  <- same files as Case A, scoped to this repo's slice
    story.md            ? story scope scoped to this repo's changes only (AC + full BDD Gherkin for this repo's behavior)
    design.md           ? only what this story changes in this repo
    tasks.md            ? tasks for this repo only + done criteria referencing SCN-NNN
    coding-prompt.md    ? synthesis file for this repo's slice (same structure as Case A)
    specs/
      api.md            ? only endpoints this repo creates or modifies (delete if none)
      data.md           ? only schema changes in this repo (delete if none)
      observability.md  ? only signals this repo emits (delete if none)
  {{repo-b}}/                  <- same structure
    story.md
    design.md
    tasks.md
    coding-prompt.md
    specs/
      ...
```

#### Inferring which repos a story touches

Read each repo descriptor in `input/repositories/`. Apply the following inference in order � stop at the first match:

1. **Primary signal � Functional areas list:** if the descriptor has a `## Functional areas` section, check whether the story's FR-NNN appears in that list. If yes, this repo gets a subfolder for this story. If no, move to step 2.
2. **Fallback � Responsibility description:** if the story's AC or FR references capabilities described in the repo's `## Responsibility` section (API endpoints, database tables, UI views, background jobs), include the repo.
3. **Architecture fallback:** if the architecture assigns this story's functional area to this repo (e.g. via an AR-NNN rule or topology note), include the repo.

Include only repos where at least one criterion matched. A story that is purely a backend API change does not get a `ui/` subfolder. A story that only changes the UI does not get a `db/` subfolder. When uncertain between two repos, include both and add an open question to the story's `story.md`.

#### Per-repo story.md scope

Each `{{repo}}/story.md` describes only the changes and acceptance in that repo:
- **Repository scope line** � fill the "Repository scope" line at the top of the template with the descriptor file name (without `.md`) as `{{repo-name}}` and the story ID as `{{F-XXX.X}}`; e.g. `This story covers the \`api\` repository slice of story F-001.1.` Remove this line entirely in Case A (flat structure).
- AC table � only ACs that this repo's changes satisfy
- BDD scenarios � full Gherkin only for scenarios that test this repo's behavior (not all scenarios for the story)
- Out of scope � what this story does NOT change in this specific repo
- Dependencies � on other repos' outputs; **uncomment and fill the cross-repo dependency table** in the template for any intra-story repo dependency that applies; leave the table commented out only if this repo has no intra-story dependency on another repo

#### Per-repo tasks.md scope

Each `{{repo}}/tasks.md`:
- **Repository scope line** � fill the same way as story.md: descriptor file name as `{{repo-name}}`, story ID as `{{F-XXX.X}}`; remove the line in Case A.
- Tasks scoped to this repo's work only � no tasks from other repos' subfolders
- Done criteria references the cross-repo dependency: "notify `{{other-repo}}` team when this repo's contract is stable" where applicable

#### Cross-repo dependency note in dependency-graph.md

When Case B applies, the story-level `dependency-graph.md` (at `specs/dependency-graph.md`) gains a cross-repo section listing, for each story: which repo subfolder depends on which other repo subfolder (e.g. `F-001.1/ui` depends on `F-001.1/api` contract being stable).

---

Use templates from `.brs2spec/templates/openspec-handoff/` for all `story.md`, `design.md`, `tasks.md`, and `specs/` files regardless of case.

After completing one story folder, immediately continue to the next � do not stop between stories.

**If context limits require stopping mid-generation:** before stopping, update `workflow-state.json` with:
- `specs/handoff` status: `incomplete`
- note listing exactly which F-XXX.X folders have been generated and which remain
- `next_action.stage`: `handoff-resume`
- `next_action.reason`: "Handoff partially generated � N of M stories complete. Resume by generating remaining stories: [list IDs]"

This allows the next session to resume from the correct point without regenerating completed folders. Never mark the handoff as `complete` or `state_validated: true` until the story count check passes.

## Output rules

### Folder structure decision (repeat of Step 2 � apply consistently)

Check once at the start: does `input/repositories/` contain at least one `.md` file? If yes ? Case B (repo subfolders) for every story. If no ? Case A (flat) for every story, no by-repository output. Do not mix cases across stories in the same handoff.

**Case B full output structure:**
```
specs/
  dependency-graph.md
  F-XXX.X-slug/               ← story is the outer unit
    {{alias-a}}/              ← repo slice inside the story
      story.md  design.md  tasks.md  specs/  coding-prompt.md
    {{alias-b}}/
      story.md  design.md  tasks.md  specs/  coding-prompt.md
  F-XXX.Y-slug/
    ...
```

### dependency-graph.md
- Waves are the primary structure � one wave per row group
- Every story appears exactly once
- Dependencies table explains WHY each dependency exists (shared table, shared endpoint, logical ordering)
- Mermaid diagram generated from the waves � use `graph LR`, one arrow per dependency
- Parallelism notes call out stories in the same wave that share a component and need coordination

### story.md (per story)
- User story verbatim from `delivery-structure.md` � As a / I want / so that � do not paraphrase
- Requirement ID (FR-NNN) and "Why now" � one sentence linking to the business driver or the story that unblocks this one
- What changes � bullet list of concrete system changes (endpoint name, table name, signal name); no implementation detail
- Dependencies table � filled from the dependency graph: depends-on, parallel-with, blocks
- **AC table** � copy each AC-NNN criterion verbatim from the BRS; add "Verified by" (SCN-NNN or "Manual review"); a vague paraphrase of the AC is a quality failure
- **BDD scenarios � full Gherkin here, not a pointer to another file.** Write each scenario as: metadata block (Requirement FR-NNN, AC AC-NNN, Scenario type, Priority) + a `\`\`\`gherkin` block with at least one Given, When, Then. A summary table with no Gherkin blocks is a stub.
  - Minimum: one happy-path + one failure scenario per story
  - High-risk stories (async, RBAC, dry-run, state transitions, export): see create-bdd-scenarios.md for minimum counts
  - Each AC must be covered by at least one scenario or explicitly noted as "Manual review"
  - `Given` � state the world before the action; `When` � one action only; `Then` � observable outcome only; `And` � extends nearest Given/When/Then
  - Every scenario's AC field must be the specific AC it validates � not a shared generic AC-NNN across all scenarios in the story
- Out of scope � explicit list of what this story does NOT do; at minimum one item
- Constraints � only AR-NNN rules from `architecture/architecture-rules.md` that directly affect this story; reference the rule ID, not a generic restatement
- **Carried-forward context** � if `engineering-readiness/initiative-context.md` has a non-empty Carried-Forward Context section, copy any rows relevant to this story. Active assumptions that affect this story's implementation must be visible to the engineer before they start.
- Reference table � paths to gate artifacts and what specifically to read there for this story

### design.md (per story)
- Scoped to this story only � omit any section that does not apply
- **"What this story touches"** � one paragraph naming the specific services, tables, and system boundaries this story changes. Must name names � not "the backend service" but the actual service/module name.
- **API surface table** � required for any story that creates or modifies an endpoint; populate Method, Path, Purpose, Auth, Request, Response columns; link to `specs/api.md`; do not write a sentence in place of the table
- **Data model changes table** � required for any story that creates or modifies a table or schema; populate Table, Change, Key columns, PII?, Encryption columns; link to `specs/data.md`; do not describe the migration in prose instead of the table
- **Integration points table** � required for any story that calls an external service or adapter (T24, HMRC, DocuSign, alerting, etc.); populate Integration, Protocol, Auth, Async?, Idempotency columns; a story calling an external service that has no integration table is a quality failure
- **Architecture constraints table** � required for every story; cite specific AR-NNN rule IDs; at minimum one row per AR-NNN rule that constrains this story's implementation; "follow AR rules" without a specific rule ID is a quality failure
- **Security decisions table** � required for any story that handles PII, tokens, credentials, or RBAC; at minimum one row per security concern
- **Observability requirements table** � required for any story touching an instrumented component; populate Signal, Type, Emitted when, Labels, Gate reference; reference the gate artifact that mandated this signal; omit only if the story genuinely emits nothing and state that explicitly
- **Sequence diagram** � only if async flow or multi-service path is genuinely hard to follow from text; delete the section if not needed
- **Open questions** � required if any design decision is unresolved before coding starts; delete only if none remain
- A design.md that contains only prose paragraphs and no tables is a stub � this is a quality failure regardless of how much text is written

### tasks.md (per story)
- Tasks scoped to this story only � no tasks from other stories
- Task IDs use story prefix: `OS-F-XXX.X-NNN`
- Each implementation task must carry: requirement (FR-NNN), AC (AC-NNN), architecture constraint (AR-NNN if applicable), data tables touched, API endpoints touched, events to emit, evidence expected � omit only fields that genuinely do not apply
- Validation tasks: one per AC-NNN; each validation task references the BDD scenario(s) (SCN-NNN) it executes
- Done criteria must include: "All BDD scenarios SCN-NNN � pass" (list the specific IDs from story.md); a generic "tests pass" is a quality failure
- Reference `dependency-graph.md` for between-story ordering

### specs/ files (per story)
- `specs/api.md`: only endpoints this story touches. Delete if story has no API changes.
- `specs/data.md`: only table changes this story introduces. Delete if story has no schema changes.
- `specs/observability.md`: only signals this story emits. Delete if story emits nothing.
- Each file is thin � if a story touches one endpoint and one table, each spec file has one section

### coding-prompt.md (per story � mandatory)

Generate `coding-prompt.md` **last** for each story folder, after `story.md`, `design.md`, and `tasks.md` are complete. Use template `.brs2spec/templates/openspec-handoff/coding-prompt.md`.

This is a synthesis file � it aggregates constraints already written in the other files into a single artifact a coding agent can read without opening any other file.

**Sections to populate:**

- **Goal** � one sentence copied from the "so that" clause of `story.md`
- **Business rules** � every BR-NNN from `business-intake/business-rules.md` whose impacted features include this story's F-XXX.X; if none apply write `Business rules: none apply � [reason]`
- **Architecture rules** � every AR-NNN from the story's constraints table in `story.md`
- **Acceptance criteria (testable)** � copy AC-NNN rows from `story.md`; restate any vague AC as a verifiable outcome
- **BDD scenarios to make pass** � SCN-NNN IDs from `quality-gates/bdd/F-NNN.md` for this story; write `BDD gate not triggered for this initiative` if not triggered
- **Repository execution guard** � always the first section after the frontmatter; tells the coding agent to verify repo structure, build, tests, and exclusions before touching any file; includes stop conditions for repo mismatch, build failure, missing files, and unresolved blocking questions; never omit
- **Tasks** � copy from `tasks.md` verbatim
- **Candidate files to touch** � translate the "What this story touches" paragraph from `design.md` into a structured table of candidate file paths, change type (create/modify/delete), and one-line reason; label clearly as candidates:
  - **Case B (repo descriptor exists):** cross-reference with `## Module map` in `input/repositories/{{alias}}.md` to use accurate folder-level paths; if a specific file name cannot be determined, write the folder path and add `<!-- file name to be confirmed in actual repository -->`
  - **Case A, codebase-context.md exists:** cross-reference with `## Folder structure` in `input/codebase-context.md`
  - **Case A, no codebase-context.md:** derive from design.md narrative only; add note: `<!-- Paths estimated from design.md � no repository descriptor found. Verify in actual repository. -->`
- **Validation commands** � copy verbatim (never paraphrase or infer from tech stack name when explicit commands are available):
  - **Case B:** copy from `## Build and test commands` in `input/repositories/{{alias}}.md`; if that section is empty: fall back to `input/codebase-context.md`; if both missing: derive from technology field and add note: `<!-- Commands estimated from tech stack � verify in actual repository. -->`
  - **Case A:** copy from `## Validation commands` in `input/codebase-context.md` if it exists; otherwise derive from initiative-context.md technology stack with note
- **What you must NOT do** � three sources, all merged:
  1. AR-NNN forbidden patterns from `architecture/architecture-rules.md` relevant to this story
  2. Security-review constraints from `quality-gates/security-review.md` relevant to this story
  3. **Case B only:** every entry from `## Files and areas not to touch` in `input/repositories/{{alias}}.md`; these apply to all stories in this repo
  - At least one item required
- **Definition of done** � fixed checklist: execution guard completed; all tasks done; all AC pass; all BDD scenarios pass; all AR-NNN respected; all BR-NNN enforced; only candidate files modified (or revised list documented); all validation commands run and pass; tests added per AC

## Quality bar

A good output:
- `dependency-graph.md` is the first thing an engineering lead reads � it tells them who starts when
- Each story folder can be handed to an engineer or `/opsx:apply` with no additional context
- `design.md` + `tasks.md` + `specs/` are sufficient to implement the story � no gate artifacts needed
- `coding-prompt.md` is present in every story folder and is self-contained � a coding agent reads only this file to understand goal, constraints, ACs, scenarios, tasks, and DoD
- Tasks are small enough to review in one PR
- Every task traces to a requirement, AC, and evidence expectation
- Telemetry emission is mandatory in every task that touches an instrumented component
- `specs/` files are thin � only the slice this story needs

## Anti-patterns

- **Generating one folder for the whole deliverable** (e.g. `core-loan-origination-intake/story.md` covering all stories) � this is always wrong; every folder must be named `F-XXX.X-<slug>/`
- Generating one folder per epic or feature instead of one per user story (`F-001-applicant-intake/` is wrong; `F-001.1-submit-application/` is correct)
- Generating one folder per increment instead of one per user story
- Mixing tasks from multiple stories into one folder
- Leaving `specs/api.md` in a folder for a story with no API changes � delete it
- Generating a design.md with sections for the full initiative instead of this story
- Writing a design.md with only 1�3 lines of prose � this is a stub; every applicable table must be populated
- Writing "Design overview: �" as a paragraph instead of filling the structured tables � prose replaces tables is a quality failure
- Omitting the integration points table when the story calls an external service (T24, HMRC KYC, DocuSign, alerting channel, etc.)
- Omitting the architecture constraints table or writing it as "follows AR rules" without specific AR-NNN IDs
- Omitting the observability requirements table for any story that modifies an instrumented component
- Writing a single generic row per table (e.g. one row saying "any needed columns") instead of the actual columns and values
- Creating vague tasks (`implement backend`, `add tests`, `handle errors`)
- **Generating "short stories" or "brief proposals"** � every story.md must be complete per the output rules above; length is not a goal but every required section must be present and filled
- **Generating a "tasks index" at the handoff root** � there is no root-level tasks.md in OpenSpec; tasks live inside each story folder only
- Writing placeholder AC ("PO to provide", "TBD", "Placeholder AC-NNN") � if the AC is not in the BRS, add an open question row, do not use a placeholder
- Paraphrasing AC instead of copying the verbatim criterion from the BRS � a developer cannot implement against a paraphrase
- Writing a vague AC table row ("UI shows progress") when the BRS has a specific testable criterion � use the specific criterion
- Referencing architecture constraints generically ("follow security rules") without citing the AR-NNN rule ID
- Writing a BDD summary table (SCN-NNN | type | description) with no Gherkin blocks � the Gherkin is the deliverable, not the index
- Writing only a happy-path scenario and skipping failure/negative scenarios
- Sharing the same AC-NNN across all scenarios in a story � each scenario must reference the specific AC it validates
- Writing done criteria as "all tests pass" � the specific SCN-NNN IDs that must pass must be listed
- Copying the user story directly as a task � derive engineering tasks from story + architecture + gate constraints
- Ignoring architecture rules in task definitions
- **Stopping before all stories have a folder and marking handoff complete** � the handoff is incomplete until every F-XXX.X story from delivery-structure.md has its own folder; generating 7 of 22 and claiming done is a quality failure
- **Declaring `next_action: handoff-complete` or `state_validated: true` before all story folders exist and pass the self-review checklist** � update workflow-state.json only after every story folder is present
- Generating the handoff before reading ALL inputs � reading inputs story-by-story causes architecture constraints to be missed
- Generating `gitlab-issues.md`, CSV exports, notification files, or any planning-tool export
- Generating code
- Ending with a menu of options ("pick one", "which should I do?") � the framework runs continuously; if more work remains, do it
- Using repo subfolders when `input/repositories/` does not exist or is empty � only add subfolders when repo descriptors are present
- Using flat structure when `input/repositories/` exists with at least one descriptor � the subfolder structure is mandatory in that case
- Creating a repo subfolder for a repo that the story does not touch � infer from story AC, BRS, and architecture; do not create empty or placeholder repo subfolders
- Using a subfolder name that does not match the descriptor file name (e.g. using `backend/` when the descriptor file is `api.md`)
- Mixing Case A and Case B across stories in the same handoff run

## Stop conditions

If any required input is missing or a quality gate is not Accepted: list what is missing, state the impact, stop.
If a story has an unresolvable dependency (blocked by a story with missing input): generate the graph and all unblocked stories, then stop and state which stories are blocked and why.

## Self-review checklist

Before finalising, verify:
- [ ] **Story count check:** count the `F-XXX.X` folders generated. Count the `F-XXX.X` story IDs in `planning/delivery-structure.md`. The two counts must match exactly. If they do not, the handoff is incomplete � continue generating the missing folders before updating `workflow-state.json`.
- [ ] `dependency-graph.md` exists and covers all stories with wave grouping and Mermaid diagram
- [ ] Folder structure is consistent: all stories use Case A (flat) or all use Case B (repo subfolders) � never mixed
- [ ] If Case B: every repo subfolder name matches the corresponding `input/repositories/` descriptor file name (without `.md`)
- [ ] If Case B: no empty or placeholder repo subfolders � only repos the story actually touches have a subfolder
- [ ] If Case B: cross-repo dependencies are noted in `dependency-graph.md`
- [ ] One folder per user story � no increment-level folders
- [ ] Each `story.md` has the user story verbatim (not paraphrased)
- [ ] Each `story.md` AC table uses verbatim AC-NNN criteria from the BRS � not summaries
- [ ] Each `story.md` has full Gherkin blocks (Given/When/Then) � not just a summary table
- [ ] Each `story.md` has at least one happy-path and one failure/negative BDD scenario
- [ ] Each `story.md` scenario metadata block has the specific AC-NNN it validates � not a shared generic AC
- [ ] Each `story.md` has an out-of-scope section
- [ ] Each `story.md` constraints table cites AR-NNN rule IDs � not generic descriptions
- [ ] Each `story.md` has the dependency table filled (depends-on, parallel-with, blocks)
- [ ] Each `story.md` carries forward active assumptions from `initiative-context.md` that affect this story � not silently omitted
- [ ] Each `tasks.md` done criteria lists specific SCN-NNN IDs that must pass
- [ ] Each `design.md` omits sections that don't apply to its story
- [ ] Each `design.md` "What this story touches" names specific components, not "the backend"
- [ ] Each `design.md` has the integration points table populated for every story that calls an external service
- [ ] Each `design.md` architecture constraints table cites specific AR-NNN IDs � not generic descriptions
- [ ] Each `design.md` observability table is populated for any story touching an instrumented component
- [ ] No `design.md` consists of only prose paragraphs with no tables � if any table is applicable and missing, the design.md is a stub
- [ ] Each task has: requirement (FR-NNN), AC (AC-NNN), evidence expected; architecture constraint (AR-NNN) and telemetry if applicable
- [ ] `specs/` files deleted when not applicable to the story
- [ ] No tasks for out-of-scope features
- [ ] No generated code
- [ ] Mermaid self-review checklist from `agent-instructions.md` applied to the dependency graph diagram
- [ ] Every story folder contains `coding-prompt.md`
- [ ] Every `coding-prompt.md` has a "Repository execution guard" section as the first section after the frontmatter � never omitted
- [ ] Every `coding-prompt.md` has a Goal (from "so that" clause), at least one BR-NNN row or explicit "none apply" note, at least one AR-NNN row, testable AC rows, SCN-NNN list or "not triggered" note, tasks copied verbatim, at least one "must NOT do" item, and a definition of done checklist
- [ ] Every `coding-prompt.md` has a "Candidate files to touch" table with at least one row (or an explicit "<!-- no files identified -->" note)
- [ ] Every `coding-prompt.md` has a "Validation commands" section with runnable commands or an explicit gap note
- [ ] Case B: "Validation commands" copied verbatim from repo descriptor `## Build and test commands` � not inferred from tech stack name
- [ ] Case B: "Candidate files to touch" cross-referenced with repo descriptor `## Module map` � not derived from design.md prose only
- [ ] Case B: "What you must NOT do" merges AR-NNN forbidden patterns + repo descriptor `## Files and areas not to touch`
- [ ] Case A: if `input/codebase-context.md` missing: gap noted in dependency-graph.md preamble
