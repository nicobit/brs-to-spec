# Enhancement 6 — Repository-Aware Handoff and Execution Safety

## Context

Enhancement 6 is the third iteration of targeted improvements. It responds to the analysis in `input.md`, which correctly identifies the framework's remaining gap: the OpenSpec handoff produces a by-story output only, and the coding-prompt.md makes overconfident claims about file paths and validation commands derived from metadata the framework does not actually have.

The framework already has:
- `input/repositories/` — per-repo descriptor files (Case B handoff); file name drives subfolder name
- `input/codebase-context.md` — single-repo flat context (Enhancement 5.4)
- `coding-prompt.md` — "Files to touch" and "Validation commands" sections (Enhancement 5.3)

What is still missing:
1. The repository descriptor template is thin — no technology stack detail, no module map, no build/test commands, no coding standards. The handoff can split by repo but cannot put accurate implementation guidance into each repo's coding-prompt.md.
2. The OpenSpec handoff produces only a by-story view. A coding agent running inside one repository needs a by-repository view: all story slices for that repo in one place, in implementation sequence.
3. The coding-prompt.md frames "Files to touch" and "Validation commands" as confirmed facts. When the framework hasn't seen the codebase, they are candidates. The coding agent inside the real repo must verify before touching anything.
4. There is no repository execution guard — a checklist the coding agent runs *before* modifying code to verify repo reality matches the package assumptions.

## What Enhancement 6 does NOT do

- Does not add a formal Stage 3 repository intelligence phase. The `input/repositories/` optional pattern stays — it is non-blocking and user-controlled.
- Does not change the OpenSpec by-story folder structure — it adds to it.
- Does not touch the standalone delivery skill.
- Does not change the workflow runner stage numbering.

## Enhancements

### Enhancement 6.1 — Enrich the repository descriptor template

**Problem:** `input/repositories/_template.md` is thin. It has identity, technology (5 fields), functional areas, responsibility, API contract surface, relevant constraints, and notes. It does not include module map, build/test commands, coding standards, or explicit "do not touch" areas.

**Solution:** Replace the template with a richer version that adds:
- `## Module map` — key folders with one-line responsibilities
- `## Build and test commands` — exact commands; these are copied verbatim into coding-prompt.md
- `## Coding standards` — patterns to follow with example locations
- `## Files and areas not to touch` — explicit exclusions for this repo

This makes `codebase-context.md` (Enhancement 5.4) redundant for multi-repo initiatives — the per-repo descriptor covers the same information at higher fidelity. The `codebase-context.md` template remains valid for single-repo initiatives without a `repositories/` folder.

**Files changed:**
- `.brs2spec/templates/repositories/_template.md` — replace with enriched version

---

### Enhancement 6.2 — Add by-repository output to OpenSpec handoff

**Problem:** The OpenSpec handoff produces `openspec/changes/F-XXX.X-slug/` — one folder per story. When an initiative spans three repos, the engineer for `api` must open 15 story folders, find the `api/` subfolder in each, and mentally reconstruct their own work list. That is not how coding agents work.

**Solution:** After generating all by-story folders, generate a by-repository index at:

```
openspec/by-repository/
  REPO-alias/
    repo-context.md       ← repo profile + tech stack + coding standards + do-not-touch areas
    stories-in-scope.md   ← all story slices allocated to this repo, in wave order
    coding-prompt.md      ← aggregated AI-ready prompt: all stories, all tasks, all constraints, all validation commands
```

The alias is the descriptor file name (without `.md`), same as the subfolder name in Case B story folders. `repo-context.md` is derived from `input/repositories/<alias>.md`. `stories-in-scope.md` is derived from the wave order in `openspec/changes/dependency-graph.md`. `coding-prompt.md` is the repo-level synthesis file.

This output is only generated in Case B (when `input/repositories/` exists). Case A (flat) has no by-repository view because the initiative is single-repo — the by-story view is already the repo view.

**Files changed:**
- `.brs2spec/skills/5-handoff/01-create-openspec-change-for-active-deliverable.md` — add Step 3: generate by-repository output
- `.brs2spec/templates/openspec-handoff/by-repository/repo-context.md` — new template
- `.brs2spec/templates/openspec-handoff/by-repository/stories-in-scope.md` — new template
- `.brs2spec/templates/openspec-handoff/by-repository/coding-prompt.md` — new template

---

### Enhancement 6.3 — Add repository execution guard to coding-prompt.md

**Problem:** The coding agent reading `coding-prompt.md` has no instruction to verify that the repository it is about to modify matches the package assumptions. When the framework hasn't seen the actual source code, file paths and module names in the package are candidates — not confirmed facts.

**Solution:** Add a `## Repository execution guard` section to `coding-prompt.md` (per-story, Case B only). This section tells the agent:

1. Before touching any file: verify the repository structure matches the repo-context.md profile.
2. Confirm or revise the "Files to touch" list based on what actually exists.
3. Confirm build/test commands actually work in this environment.
4. If the repository profile does not match reality: stop and report before implementing.

Also rename the section heading from `## Files to touch` to `## Candidate files to touch` to accurately reflect that these are framework-derived estimates, not confirmed facts.

**Files changed:**
- `.brs2spec/templates/openspec-handoff/coding-prompt.md` — add execution guard section; rename files-to-touch heading
- `.brs2spec/skills/5-handoff/01-create-openspec-change-for-active-deliverable.md` — update coding-prompt.md generation rules and checklist

---

### Enhancement 6.4 — Wire enriched repository descriptors into handoff generation

**Problem:** The handoff skill currently reads `input/repositories/<alias>.md` only to decide *which repos a story touches* (functional areas and responsibility sections). It does not read the build/test commands or coding standards when generating coding-prompt.md. Enhancement 5.3 added "Validation commands" sourced from `input/codebase-context.md` — but for Case B the source should be the per-repo `build-test-commands` section in the descriptor.

**Solution:** Update the handoff skill so that in Case B:
- `coding-prompt.md` "Validation commands" comes from the repo descriptor `## Build and test commands` section (not from `codebase-context.md`)
- `coding-prompt.md` "What you must NOT do" merges AR-NNN forbidden patterns + repo descriptor `## Files and areas not to touch`
- `coding-prompt.md` "Candidate files to touch" cross-references the repo descriptor `## Module map` for accurate folder paths

For Case A (flat), `codebase-context.md` remains the source — no change.

**Files changed:**
- `.brs2spec/skills/5-handoff/01-create-openspec-change-for-active-deliverable.md` — update coding-prompt.md generation rules for Case B

---

## Implementation order

1. Enhancement 6.1 — enrich repository descriptor template (foundation for all others)
2. Enhancement 6.3 — add execution guard + rename files-to-touch in coding-prompt template
3. Enhancement 6.4 — wire enriched descriptors into handoff skill generation rules
4. Enhancement 6.2 — add by-repository output (most structural change; benefits from 6.1 + 6.3 + 6.4 being done first)

## Quality bar after Enhancement 6

- A developer fills one `input/repositories/<alias>.md` per repo — it is the single source of truth for that repo's structure, patterns, commands, and exclusions.
- Every per-story `coding-prompt.md` (Case B) has accurate module-map-derived file paths, verbatim build/test commands from the descriptor, and a repository execution guard section.
- Every repo gets a `openspec/by-repository/<alias>/` folder with a unified view of all its story slices and a single repo-level coding-prompt.md.
- The coding agent always verifies repo reality before touching files — the execution guard is non-negotiable.
- `codebase-context.md` (Case A) and per-repo descriptors (Case B) are complementary and consistent — they cover the same concerns at different granularities.
