# Enhancement 6.3 — Add Repository Execution Guard and Fix "Candidate" Framing

## Problem

### Problem 1 — Overconfident framing in coding-prompt.md

The current `coding-prompt.md` template has:

```markdown
## Files to touch
```

This framing implies the framework knows which files need to change. It does not. For any initiative where `input/codebase-context.md` or the repo descriptor does not exist, the file paths are guessed from `design.md` narrative — which itself is derived from architecture and BRS, not from reading the actual repository.

Even when repo descriptors exist (Case B), the module map describes folder-level structure, not specific file names. The coding agent must inspect the actual repository to confirm which file to edit.

The correct framing is **candidate** — a starting point the agent must verify and revise, not a confirmed list.

### Problem 2 — No stop condition before implementation

There is no instruction in `coding-prompt.md` telling the coding agent to verify repo reality before touching files. A coding agent that reads only the `coding-prompt.md` and immediately starts editing will:
- Create files in paths that don't exist
- Follow patterns that have been superseded
- Skip validation commands that don't work in this environment
- Modify files that are excluded (migrations, startup, etc.)

A repository execution guard — a mandatory pre-implementation checklist — prevents all of these failures.

---

## What needs to change

### Change 1 — `.brs2spec/templates/openspec-handoff/coding-prompt.md`

**Rename section heading:**

```
## Files to touch
```
→
```
## Candidate files to touch
```

**Update the section comment:**

```markdown
## Candidate files to touch

<!-- Source: design.md "What this story touches" + repo descriptor module map (if available) -->
<!-- These are CANDIDATES derived from architecture and design — not confirmed facts. -->
<!-- Before editing: verify the file exists and the path is correct in the actual repository. -->
<!-- If actual structure differs: revise this list and note the change before proceeding. -->
<!-- Change type: create | modify | delete -->

| File path | Change type | Reason |
|---|---|---|
| {{src/path/to/file}} | create / modify / delete | {{one-line reason}} |
```

**Add `## Repository execution guard` section before "Goal":**

```markdown
## Repository execution guard

> **Run this check BEFORE modifying any file.**
> This package was generated from architecture and design artifacts — it has not seen the actual repository.
> The file paths, module names, and commands below are candidates. Verify before implementing.

Before touching any code:

1. **Inspect repository structure** — confirm the actual folder layout matches the module map (in `openspec/by-repository/{{alias}}/repo-context.md` if it exists, or in `input/repositories/{{alias}}.md`).
2. **Confirm candidate files** — check that each file listed in "Candidate files to touch" exists (for modify/delete) or that its parent folder exists (for create).
3. **Run build command** — confirm the unmodified codebase builds cleanly before making any change.
4. **Run test command** — confirm existing tests pass before making any change.
5. **Verify exclusions** — confirm that files listed in "What you must NOT do" are still present and still excluded.
6. **Check open questions** — if this story has open questions in `story.md`, confirm all blocking questions are resolved before implementing.

**Stop and report to the human if:**
- The actual folder structure does not match what is described in the module map — implementation against wrong structure produces wrong results.
- The build fails on the unmodified codebase — there may be a pre-existing issue that must be resolved first.
- A file listed for modification does not exist — the design assumption may be wrong.
- A validation command cannot be run — note why and ask for the correct command before proceeding.
- An open question in this story is still unresolved and blocking.

After completing the guard: proceed with implementation in the order specified in "Tasks".
```

**Update Definition of done — add guard item as first item:**

```markdown
## Definition of done

- [ ] Repository execution guard completed — repo structure confirmed, build clean, tests passing before changes
- [ ] All tasks in the Tasks section implemented
- [ ] All AC-NNN acceptance criteria pass as stated above
- [ ] All BDD scenarios listed above pass
- [ ] All AR-NNN rules respected — no forbidden patterns introduced
- [ ] All BR-NNN rules enforced in the implemented code
- [ ] Only files listed in "Candidate files to touch" modified (or revised list documented) — no out-of-scope changes
- [ ] All validation commands run and pass
- [ ] Tests added for each AC-NNN
```

---

### Change 2 — `.brs2spec/skills/5-handoff/01-create-openspec-change-for-active-deliverable.md`

**Update coding-prompt.md Sections to populate:**

Change:
```
- **Files to touch** — translate the "What this story touches" paragraph from `design.md` into a structured table...
```

To:
```
- **Candidate files to touch** — translate the "What this story touches" paragraph from `design.md` into a structured table of candidate file paths, change type (create/modify/delete), and one-line reason; label clearly as candidates; if `input/repositories/{{alias}}.md` exists (Case B), cross-reference with the module map section to use accurate folder paths; if `input/codebase-context.md` exists (Case A), cross-reference with the folder structure section; if neither exists, derive from design.md narrative and add note: `<!-- Paths estimated from design.md — verify in actual repository before editing. -->`
```

**Update coding-prompt.md Sections — add execution guard as first item:**
```
- **Repository execution guard** — always present; always the first section after the frontmatter; tells the coding agent to verify repo structure, build, tests, and exclusions before touching any file; includes stop conditions for repo mismatch, build failure, missing files, and unresolved blocking questions
```

**Update self-review checklist:**

Change:
```
- [ ] Every `coding-prompt.md` has a "Files to touch" table with at least one row (or an explicit "<!-- no files identified -->" note)
```
To:
```
- [ ] Every `coding-prompt.md` has a "Candidate files to touch" table with at least one row (or an explicit "<!-- no files identified -->" note)
- [ ] Every `coding-prompt.md` has a "Repository execution guard" section as the first section after the frontmatter
```

---

### Change 3 — `brs-to-spec-run-workflow.md` stage 13 done criteria

Update:

**Current:** `coding-prompt.md lists BR-NNN, AR-NNN, SCN-NNN, forbidden patterns, files-to-touch table, and validation commands`

**Change to:** `coding-prompt.md has repository execution guard (first section), BR-NNN, AR-NNN, SCN-NNN, forbidden patterns, candidate-files-to-touch table, and validation commands`

---

## Implementation steps

1. Open `.brs2spec/templates/openspec-handoff/coding-prompt.md`:
   - Add `## Repository execution guard` section as first section after frontmatter header
   - Rename `## Files to touch` → `## Candidate files to touch`
   - Update comment block in that section
   - Update Definition of done: add guard as first item; update files-to-touch reference to "Candidate files"

2. Open `.brs2spec/skills/5-handoff/01-create-openspec-change-for-active-deliverable.md`:
   - Update coding-prompt.md Sections to populate: rename files-to-touch; add execution guard as first item
   - Update self-review checklist: rename files-to-touch item; add execution guard item

3. Open `.brs2spec/brs-to-spec-run-workflow.md`:
   - Update stage 13 done criteria: add execution guard; rename files-to-touch to candidate-files-to-touch

## Quality bar

After this change:
- Every coding-prompt.md (per-story and per-repo) has a mandatory execution guard as the first operational section.
- "Files to touch" is correctly framed as candidate throughout — template, skill, workflow runner.
- No coding agent can read coding-prompt.md and proceed directly to implementation without first verifying the repository.
- Stop conditions are explicit — the agent knows when to stop and report rather than continue with wrong assumptions.
