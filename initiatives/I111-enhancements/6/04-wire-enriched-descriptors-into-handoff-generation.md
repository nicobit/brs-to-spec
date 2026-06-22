# Enhancement 6.4 — Wire Enriched Repository Descriptors into Handoff Generation

## Problem

The handoff skill currently reads `input/repositories/<alias>.md` only to decide *which repos a story touches* (functional areas and responsibility sections). The richer sections added in Enhancement 6.1 — module map, build/test commands, coding standards, files-not-to-touch — are never read during handoff generation.

Concretely:

| Section in descriptor | Currently used by handoff? | Should be used for |
|---|---|---|
| `## Functional areas` | Yes — story→repo assignment | (already correct) |
| `## Responsibility` | Yes — fallback for story→repo assignment | (already correct) |
| `## Technology` | No | repo-context.md; coding-prompt.md header |
| `## Module map` | No | Candidate files to touch (folder-level path accuracy) |
| `## Build and test commands` | No | Validation commands in coding-prompt.md (verbatim) |
| `## Coding standards` | No | repo-context.md; coding-prompt.md "What you must NOT do" supplementary |
| `## Files and areas not to touch` | No | coding-prompt.md "What you must NOT do" merged with AR-NNN |
| `## Relevant constraints` | No | coding-prompt.md AR-NNN rules |
| `## API contract surface` | No | story.md integration points cross-check |

The result: in Case B, "Validation commands" still comes from `input/codebase-context.md` (Enhancement 5.3) or is inferred from the tech stack name — even though each repo descriptor now has exact commands. "What you must NOT do" lists AR-NNN rules but misses repo-specific exclusions. Candidate file paths are derived from design.md prose with no module map guidance.

---

## What needs to change

### Change 1 — Update handoff skill reading rules for Case B

In `.brs2spec/skills/5-handoff/01-create-openspec-change-for-active-deliverable.md`, update the Inputs section item for `input/repositories/`:

**Current:**
```
4. `input/repositories/` — **if this folder exists**, read every `.md` file in it; each file describes one repository and its file name (without extension) is the subfolder name used in the handoff output; if the folder does not exist or is empty, skip and use the flat folder structure (no repo subfolders)
```

**Replace with:**
```
4. `input/repositories/` — **if this folder exists**, read every `.md` file in it before generating any output. Each file describes one repository:
   - File name (without `.md`) = subfolder name in handoff output and alias in `openspec/by-repository/`
   - `## Functional areas` + `## Responsibility` → used to assign stories to repos (primary + fallback signal)
   - `## Technology` → used to populate repo-context.md and coding-prompt.md header
   - `## Module map` → used to derive accurate folder-level candidate file paths in coding-prompt.md "Candidate files to touch"
   - `## Build and test commands` → copied **verbatim** into coding-prompt.md "Validation commands" for every story in this repo; do not infer from tech stack name when descriptor has explicit commands
   - `## Coding standards` → used to populate repo-context.md coding standards table
   - `## Files and areas not to touch` → merged with AR-NNN forbidden patterns into "What you must NOT do" in coding-prompt.md; applies to every story in this repo
   - `## Relevant constraints` → additional AR-NNN rules that apply specifically to this repo; include in coding-prompt.md AR-NNN table alongside global architecture-rules.md rules
   - If the folder does not exist or is empty: skip and use flat structure (Case A)
```

---

### Change 2 — Update coding-prompt.md generation rules in the handoff skill

In the `### coding-prompt.md (per story — mandatory)` section, update the generation rules:

**Update "Candidate files to touch" rule:**

```
- **Candidate files to touch** — translate the "What this story touches" paragraph from `design.md` into a structured table:
  - **Case B (repo descriptor exists):** cross-reference with the `## Module map` section of `input/repositories/{{alias}}.md` to use accurate folder-level paths; if a specific file name cannot be determined from the module map, write the folder path and add a note `<!-- file name to be confirmed in actual repository -->`
  - **Case A (no repo descriptor, codebase-context.md exists):** cross-reference with `## Folder structure` in `input/codebase-context.md`
  - **Case A (no repo descriptor, no codebase-context.md):** derive from design.md narrative only; add note: `<!-- Paths estimated from design.md — no repository descriptor found. Verify in actual repository. -->`
  - Always label as candidates — never present as confirmed paths
```

**Update "Validation commands" rule:**

```
- **Validation commands** — copy verbatim (do not paraphrase):
  - **Case B (repo descriptor exists):** copy from `## Build and test commands` in `input/repositories/{{alias}}.md`; if the section is empty or the descriptor does not exist for this alias: fall back to `input/codebase-context.md`; if both missing: derive from technology field in descriptor and add note: `<!-- Commands estimated from tech stack — verify in actual repository. -->`
  - **Case A:** copy from `## Validation commands` in `input/codebase-context.md` if it exists; otherwise derive from initiative-context.md technology stack with note
```

**Update "What you must NOT do" rule:**

```
- **What you must NOT do** — three sources, merged:
  1. AR-NNN forbidden patterns from `architecture/architecture-rules.md` relevant to this story (existing behavior)
  2. Security-review constraints from `quality-gates/security-review.md` relevant to this story (existing behavior)
  3. **Case B only:** `## Files and areas not to touch` from `input/repositories/{{alias}}.md` — include every entry; these apply to all stories in this repo, not just this one
  - At least one item required; if all three sources are empty, derive from AR-NNN rules that have a "forbidden" or "must not" constraint
```

---

### Change 3 — Update self-review checklist in handoff skill

Add under the coding-prompt.md checklist section:

```
- [ ] Case B: "Validation commands" in every `coding-prompt.md` copied verbatim from repo descriptor `## Build and test commands` — not inferred from tech stack name
- [ ] Case B: "Candidate files to touch" cross-referenced with repo descriptor `## Module map` — not derived from design.md prose only
- [ ] Case B: "What you must NOT do" merges AR-NNN forbidden patterns + repo descriptor `## Files and areas not to touch`
```

---

### Change 4 — Update handoff skill reading rule

In `**Reading rule:**` at the top of the Inputs section, add:

```
For Case B: read ALL repository descriptors fully — not just the Functional areas section — before generating any story folder. The module map, build commands, coding standards, and exclusions affect every story in the repo.
```

---

## Implementation steps

1. Open `.brs2spec/skills/5-handoff/01-create-openspec-change-for-active-deliverable.md`:
   - Replace input item 4 (`input/repositories/`) with expanded version above
   - Update `**Reading rule:**` to include full descriptor reading for Case B
   - Update `coding-prompt.md` sections: candidate files, validation commands, what-not-to-do
   - Add 3 new checklist items for Case B

## Quality bar

After this change, for any Case B initiative:
- Validation commands in every coding-prompt.md are verbatim from the repo descriptor — not a guess.
- Candidate file paths reference the module map folder structure — not invented from design.md prose.
- "What you must NOT do" is complete — global AR-NNN forbidden patterns + repo-specific exclusions.
- The handoff skill reads descriptors fully on first pass — no partial reads that miss build commands or coding standards.
- A coding agent working from coding-prompt.md alone has everything it needs to implement correctly in this repository.
