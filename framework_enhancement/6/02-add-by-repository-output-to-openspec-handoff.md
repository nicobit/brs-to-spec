# Enhancement 6.2 — Add By-Repository Output to OpenSpec Handoff

## Problem

The OpenSpec handoff produces `openspec/changes/F-XXX.X-slug/` — one folder per story. For multi-repo Case B initiatives, this means:

- The engineer for `api` must open 12 story folders, navigate into `api/` in each, read a story.md, a design.md, and a tasks.md — then mentally reconstruct what they need to do across those 12 stories.
- A coding agent handed one `openspec/changes/` folder has no clean entry point per repo — it must traverse the whole tree.
- There is no single place where the api engineer can read "here are all the stories you own, in implementation sequence, with your constraints and your validation commands."

The by-story output is correct for business traceability. It is not the right working surface for repo-level implementation.

## Solution

After generating all by-story folders, generate a by-repository index. This is only relevant for Case B (multi-repo, `input/repositories/` exists). For Case A (flat), the by-story output is already the repo view.

```
openspec/by-repository/
  {{alias}}/
    repo-context.md       — repo identity, tech stack, module map, coding standards, do-not-touch areas
    stories-in-scope.md   — all story slices for this repo in wave order with traceability
    coding-prompt.md      — aggregated AI-ready prompt: all stories, all tasks, all constraints, all commands
```

The alias is the descriptor file name without `.md` — same as the subfolder name in Case B story folders (e.g. `api`, `ui`, `db`).

---

## What needs to change

### Change 1 — New templates

#### `.brs2spec/templates/openspec-handoff/by-repository/repo-context.md`

```markdown
# Repository Context — {{alias}}

> Source: `input/repositories/{{alias}}.md`
> Generated for initiative: {{initiative ID}} — {{initiative name}}
> This file is the entry point for a coding agent working in this repository.
> Read this file before opening any story file.

## Repository identity

| Field | Value |
|---|---|
| Repository name | {{from descriptor}} |
| Alias | {{alias}} |
| Remote URL / path | {{from descriptor}} |
| Owning team | {{from descriptor}} |

## Technology stack

| Field | Value |
|---|---|
| Language | {{from descriptor}} |
| Framework | {{from descriptor}} |
| Runtime | {{from descriptor}} |
| Database | {{from descriptor}} |
| Infrastructure | {{from descriptor}} |

## Module map

<!-- Source: input/repositories/{{alias}}.md ## Module map -->

| Folder | Responsibility |
|---|---|
| {{folder}} | {{responsibility}} |

## Coding standards

<!-- Source: input/repositories/{{alias}}.md ## Coding standards -->

| Pattern | Rule | Example location |
|---|---|---|
| {{pattern}} | {{rule}} | {{example}} |

## Files and areas not to touch

<!-- Source: input/repositories/{{alias}}.md ## Files and areas not to touch -->
<!-- These apply to ALL stories in this repo — not just one story. -->

| Path / area | Reason |
|---|---|
| {{path}} | {{reason}} |

## Architecture rules that apply to this repository

<!-- Source: architecture/architecture-rules.md + input/repositories/{{alias}}.md ## Relevant constraints -->
<!-- Only AR-NNN rules that specifically govern this repository's implementation. -->

| Rule | Text | Enforcement |
|---|---|---|
| {{AR-NNN}} | {{rule text}} | {{how to enforce}} |

## Stories in scope

> See `stories-in-scope.md` for the full story list with wave ordering.
> See `coding-prompt.md` for the aggregated AI-ready implementation prompt.
```

#### `.brs2spec/templates/openspec-handoff/by-repository/stories-in-scope.md`

```markdown
# Stories in Scope — {{alias}}

> All story slices allocated to this repository, in wave (implementation) order.
> Derived from `openspec/changes/dependency-graph.md` waves and `openspec/changes/F-XXX.X-*/{{alias}}/` subfolders.
> For full business context per story: open `openspec/changes/F-XXX.X-slug/{{alias}}/story.md`.

## Wave order

<!-- Stories from the same wave can run in parallel within this repo. -->
<!-- A wave starts only when all stories in the previous wave are complete and deployed. -->

### Wave 1 — can start immediately

| Story | Title | FR | AC count | Story folder |
|---|---|---|---|---|
| F-XXX.X | {{story title}} | FR-NNN | N | `openspec/changes/F-XXX.X-slug/{{alias}}/` |

### Wave 2 — starts when Wave 1 is deployed

| Story | Title | FR | AC count | Depends on | Story folder |
|---|---|---|---|---|---|
| F-XXX.X | {{story title}} | FR-NNN | N | F-XXX.X | `openspec/changes/F-XXX.X-slug/{{alias}}/` |

<!-- Add more waves as needed. -->

## Cross-repo dependencies

> Intra-story dependencies where this repo's slice must wait for another repo's slice.
> Source: `openspec/changes/dependency-graph.md` § Cross-repo dependencies.

| Story | This repo waits for | Reason |
|---|---|---|
| F-XXX.X | {{other-alias}} | {{e.g. UI integration requires stable API contract}} |

## Story count

- Total stories in scope for this repo: {{N}}
- Wave 1: {{N}} stories
- Wave 2: {{N}} stories
```

#### `.brs2spec/templates/openspec-handoff/by-repository/coding-prompt.md`

```markdown
---
Repository: {{alias}}
Initiative: {{initiative ID}} — {{initiative name}}
Generated: {{YYYY-MM-DD}}
Stories covered: {{F-XXX.X, F-XXX.X, …}}
---

# Repository Coding Prompt — {{alias}}

> You are working in the `{{alias}}` repository.
> This prompt covers ALL stories allocated to this repository for this initiative.
> Work through stories in wave order (Wave 1 first, then Wave 2, etc.).
> Complete all tasks in one story before starting the next within the same wave.
> Stories in the same wave may be started in parallel if team capacity allows.

## Repository execution guard

> **Run this check BEFORE modifying any file.**

Before touching any code:

1. Inspect the actual repository structure — confirm it matches the module map in `repo-context.md`.
2. Confirm or revise the candidate files listed in each story's "Candidate files to touch" section.
3. Run the build command — confirm it succeeds on the unmodified codebase.
4. Run the test command — confirm existing tests pass before your changes.
5. Verify that "Files and areas not to touch" in `repo-context.md` still matches the real repository.
6. Check whether any open question in any story's `story.md` is still unresolved — do not implement a story with an unresolved blocking question.

**Stop and report if any of the following is true:**
- The actual repository structure does not match the module map — report the mismatch before implementing.
- The build command fails on the unmodified codebase — do not proceed until resolved.
- A "Files and areas not to touch" path does not exist — confirm the exclusion is still valid.
- A required module, folder, or class from the candidate files list cannot be found — revise the list and report.

## Repository context summary

| Field | Value |
|---|---|
| Language | {{from descriptor}} |
| Framework | {{from descriptor}} |
| Runtime | {{from descriptor}} |

Full repository profile: `openspec/by-repository/{{alias}}/repo-context.md`

## Architecture rules that constrain this repository

<!-- Source: architecture/architecture-rules.md + input/repositories/{{alias}}.md ## Relevant constraints -->

| Rule | Text | How to enforce |
|---|---|---|
| {{AR-NNN}} | {{rule text}} | {{enforcement}} |

## Business rules in scope for this repository

<!-- Source: business-intake/business-rules.md — only rules that affect this repo's implementation -->

| Rule | Text | Enforcement |
|---|---|---|
| {{BR-NNN}} | {{rule text}} | {{how to enforce in code}} |

## Stories — Wave 1

<!-- One section per story in Wave 1. Complete all Wave 1 stories before starting Wave 2. -->

### F-XXX.X — {{story title}}

**Goal:** {{one sentence from the "so that" clause}}
**FR:** {{FR-NNN}}
**Story folder:** `openspec/changes/F-XXX.X-slug/{{alias}}/`

#### Acceptance criteria

| AC | Verifiable statement |
|---|---|
| AC-NNN | {{testable outcome}} |

#### BDD scenarios to make pass

- SCN-NNN: {{scenario title}}

#### Tasks

<!-- Source: openspec/changes/F-XXX.X-slug/{{alias}}/tasks.md — copied verbatim -->

{{tasks}}

#### Candidate files to touch

<!-- Source: openspec/changes/F-XXX.X-slug/{{alias}}/design.md + repo-context.md ## Module map -->
<!-- These are candidates — verify they exist before editing. Revise if the actual structure differs. -->

| File path | Change type | Reason |
|---|---|---|
| {{src/path/to/file}} | create / modify / delete | {{reason}} |

---

## Stories — Wave 2

<!-- One section per story in Wave 2. Start only after Wave 1 is deployed. -->

---

## Validation commands

<!-- Source: input/repositories/{{alias}}.md ## Build and test commands — copied verbatim -->
<!-- Run after each story is implemented. All commands must pass before marking a story done. -->

```bash
{{commands verbatim from descriptor}}
```

## What you must NOT do

<!-- Source: AR-NNN forbidden patterns + input/repositories/{{alias}}.md ## Files and areas not to touch -->
<!-- Applies to ALL stories in this repo. -->

- {{forbidden pattern or area}} ({{AR-NNN or "repo constraint"}})

## Definition of done — per story

For each story, done means ALL of the following:
- [ ] All tasks in the story's tasks.md implemented
- [ ] All AC-NNN acceptance criteria pass as stated above
- [ ] All BDD scenarios for this story pass
- [ ] All AR-NNN rules respected — no forbidden patterns introduced
- [ ] All BR-NNN rules enforced in the implemented code
- [ ] Only files in the "Candidate files to touch" list modified — no out-of-scope changes
- [ ] All validation commands run and pass
- [ ] Tests added for each AC-NNN

## Definition of done — this repository (all stories)

- [ ] All Wave 1 stories done and deployed before starting Wave 2
- [ ] All stories in all waves done
- [ ] Cross-repo dependencies signalled — notify dependent repos when this repo's contract is stable (see `stories-in-scope.md` § Cross-repo dependencies)
```

---

### Change 2 — Update `skills/5-handoff/01-create-openspec-change-for-active-deliverable.md`

**Add Step 3 — Generate by-repository output (Case B only):**

After Step 2 (all story folders generated), add:

```
## Step 3 — Generate by-repository output (Case B only)

> Skip this step entirely if Case A (flat) — `input/repositories/` does not exist or is empty.

For every repository alias found in `input/repositories/`, create:

```
openspec/by-repository/{{alias}}/
  repo-context.md
  stories-in-scope.md
  coding-prompt.md
```

**repo-context.md:** use template `.brs2spec/templates/openspec-handoff/by-repository/repo-context.md`. Populate from `input/repositories/{{alias}}.md`. Include all sections: identity, technology, module map, coding standards, files-not-to-touch, AR-NNN rules. If a section is missing from the descriptor: note the gap with `<!-- Missing from descriptor — fill input/repositories/{{alias}}.md to improve accuracy. -->` and leave the section stub.

**stories-in-scope.md:** use template `.brs2spec/templates/openspec-handoff/by-repository/stories-in-scope.md`. Enumerate every F-XXX.X story that has a `{{alias}}/` subfolder in `openspec/changes/`. Group by wave from `dependency-graph.md`. Include cross-repo dependencies from `dependency-graph.md` § Cross-repo dependencies where this alias appears.

**coding-prompt.md:** use template `.brs2spec/templates/openspec-handoff/by-repository/coding-prompt.md`. This is the synthesis file for the entire repo:
- Repository execution guard section — mandatory; never omit
- Architecture rules: only AR-NNN that apply to this repo (from repo descriptor `## Relevant constraints` + architecture-rules.md)
- Business rules: only BR-NNN that affect this repo's implementation
- One `## Stories — Wave N` section per wave; within each wave, one subsection per story
- Each story subsection: goal, AC table (from story folder), BDD scenario IDs (from story folder), tasks (copied verbatim from story folder tasks.md), candidate files to touch (from story folder design.md cross-referenced with repo descriptor module map)
- Validation commands: copied verbatim from repo descriptor `## Build and test commands`
- What you must NOT do: AR-NNN forbidden patterns + repo descriptor `## Files and areas not to touch`
- Definition of done: per-story checklist + per-repo checklist

**Reading rule for Step 3:** read all relevant story folders before generating any by-repository file. Do not generate story-by-story while reading.
```

**Add to self-review checklist (Case B only):**

```
- [ ] `openspec/by-repository/` exists with one subfolder per repo alias in `input/repositories/`
- [ ] Each `by-repository/{{alias}}/repo-context.md` populated from `input/repositories/{{alias}}.md` — gaps noted inline
- [ ] Each `by-repository/{{alias}}/stories-in-scope.md` covers all F-XXX.X stories that have a `{{alias}}/` subfolder
- [ ] Each `by-repository/{{alias}}/coding-prompt.md` has the repository execution guard section — never omitted
- [ ] Each `by-repository/{{alias}}/coding-prompt.md` validation commands copied verbatim from descriptor — not paraphrased
- [ ] Stories in `stories-in-scope.md` grouped by wave order consistent with `dependency-graph.md`
```

**Update the output structure description in the skill:**

Add to the Case B description:
```
After all story folders are generated, also produce:

openspec/by-repository/
  {{alias-1}}/
    repo-context.md
    stories-in-scope.md
    coding-prompt.md
  {{alias-2}}/
    ...
```

---

### Change 3 — Update `brs-to-spec-run-workflow.md` stage 13 done criteria

Update stage 13:

**Current:** `dependency-graph.md first; all story folders present; each folder contains story.md + design.md + tasks.md + coding-prompt.md; tasks traceable to stories; coding-prompt.md lists BR-NNN, AR-NNN, SCN-NNN, forbidden patterns, files-to-touch table, and validation commands`

**Add:** `; if Case B: openspec/by-repository/ exists with one subfolder per repo alias, each containing repo-context.md + stories-in-scope.md + coding-prompt.md with repository execution guard`

---

### Change 4 — Update `workflow-overview.md` stage 13 description

Add to stage 13 action column: `; if multi-repo (Case B): also generates openspec/by-repository/ with per-repo context, story list, and aggregated coding-prompt.md including execution guard`

---

## Implementation steps

1. Create `.brs2spec/templates/openspec-handoff/by-repository/repo-context.md` with template above
2. Create `.brs2spec/templates/openspec-handoff/by-repository/stories-in-scope.md` with template above
3. Create `.brs2spec/templates/openspec-handoff/by-repository/coding-prompt.md` with template above
4. Update `.brs2spec/skills/5-handoff/01-create-openspec-change-for-active-deliverable.md`:
   - Add Step 3 after Step 2
   - Add Case B folder structure to output description
   - Add 6 checklist items to self-review
5. Update `.brs2spec/brs-to-spec-run-workflow.md` stage 13 done criteria
6. Update `workflow-overview.md` stage 13 description

## Quality bar

After this change:
- Every multi-repo initiative produces both a by-story view and a by-repository view in the same OpenSpec output.
- A coding agent can be handed `openspec/by-repository/api/` and work without opening any story folder.
- The repo-level coding-prompt.md always starts with the repository execution guard — no implementation happens before repo reality is confirmed.
- Wave ordering is preserved — the agent knows what to implement first and what unblocks what.
