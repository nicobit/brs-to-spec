# Skill — Create OpenSpec Handoff

## Identity

| Field | Value |
|---|---|
| skill_id | eng-create-openspec-handoff |
| persona | engineering-lead |
| event_types | CREATE_OPENSPEC_HANDOFF |
| produces | specs/ (folder with one subfolder per story) |

## When this skill is used

Only when `execution_mode` is `OpenSpec` and:
- `engineering-readiness/readiness-check.md` exists and decision is `Ready`
- All triggered quality gates have `Status: Accepted`
- User stories are defined in `planning/delivery-structure.md` with F-XXX.X IDs

## Role for this task

You are an engineering lead preparing a complete OpenSpec handoff. The output is one self-contained folder per user story — an engineer or AI coding agent picks up one folder and implements exactly one user story without needing any other artifact.

## Prerequisites check

Before starting, verify:
- [ ] `engineering-readiness/readiness-check.md` is `Ready`
- [ ] All triggered quality gates are `Accepted`
- [ ] `planning/delivery-structure.md` has F-XXX.X story IDs
- [ ] `engineering-readiness/initiative-context.md` exists
- [ ] `architecture/architecture-rules.md` exists

## Instructions

### Step 1 — Story count assertion (HARD STOP)

Before creating any folder:
1. List every F-XXX.X ID from `planning/delivery-structure.md`
2. Count them and write the count
3. Confirm: "I will create exactly N folders"
4. Do NOT begin until this assertion is written

If the delivery structure is corrupt or has no F-XXX.X IDs: stop with a specific error.

### Step 2 — Read ALL inputs before generating the first folder

Read everything before writing anything:
1. `planning/delivery-structure.md` — story list
2. `input/brs.md` — AC-NNN verbatim text
3. `input/repositories/*.md` — if exists, determines Case A vs Case B
4. `engineering-readiness/initiative-context.md`
5. `architecture/architecture-review.md`
6. `architecture/architecture-rules.md`
7. `business-analysis/business-rules.md` — BR-NNN
8. `quality-gates/security-review.md`, `api-contract.md`, `data-contract.md`, `observability-plan.md`, `bdd/` — as applicable

### Step 3 — Generate dependency graph first

Create `specs/dependency-graph.md` showing wave groupings and story dependencies before any story folder.

### Step 4 — Generate one folder per story (in wave order)

**Case A** (no `input/repositories/` folder): flat structure
```
specs/F-XXX.X-slug/
  story.md     design.md     tasks.md
  specs/
    api.md     data.md     observability.md
  coding-prompt.md
```

**Case B** (`input/repositories/` exists with at least one .md file): one subfolder per repo the story touches
```
specs/F-XXX.X-slug/
  {repo-a}/story.md  design.md  tasks.md  specs/  coding-prompt.md
  {repo-b}/story.md  design.md  tasks.md  specs/  coding-prompt.md
```

Do not mix cases across stories.

### Step 5 — Per-story content rules

**story.md**: user story verbatim (As/I want/so that), AC-NNN verbatim from BRS, full Gherkin BDD blocks (not summary tables), out-of-scope list, AR-NNN constraints, dependency table, carried-forward context from initiative-context.md

**design.md**: "What this story touches" naming specific components; API surface table; data model changes table; integration points table; architecture constraints table (AR-NNN IDs); observability requirements table; no prose-only design.md

**tasks.md**: task IDs OS-F-XXX.X-NNN; each task has FR-NNN, AC-NNN, AR-NNN, evidence expected; done criteria lists specific SCN-NNN IDs

**coding-prompt.md** (generated last): synthesis file; Goal, BR-NNN rules, AR-NNN rules, AC-NNN testable list, SCN-NNN list, Repository execution guard (always first section), tasks verbatim, candidate files table, validation commands, must NOT do list, definition of done checklist

### Step 6 — Post-generation

After all folders created: run story count check. Update `workflow-state.json` only after count matches.

## Done criteria

- [ ] Story count check: N folders = N stories in delivery-structure.md
- [ ] `specs/dependency-graph.md` exists with all stories and a Mermaid diagram
- [ ] Every story folder has story.md, design.md, tasks.md, specs/, coding-prompt.md
- [ ] Every story.md has full Gherkin blocks (not summary tables)
- [ ] Every coding-prompt.md has Repository execution guard as first section
- [ ] No story covers more than one F-XXX.X ID
- [ ] Result file written with `status: pass` and `artifacts_written` listing `specs/`

## Stop conditions

- If required inputs missing or quality gates not Accepted: stop, list what is missing.
- If delivery structure has no F-XXX.X story IDs: stop.
- If story count assertion fails after generation: continue generating missing folders before marking done.
