# Enhancement 7.3 — Enforce Correct OpenSpec Handoff Structure

## Problem

On the I005 run, the orchestrator produced the following files as the OpenSpec handoff:

```
specs/openapi/openapi.yaml
specs/json-schemas/entities.json
specs/examples/explainability-trace.json
openspec/handoff/README.md
openspec/handoff/manifest.md
```

The correct output of the OpenSpec handoff skill is **one folder per confirmed user story**:

```
specs/F-001.1-<slug>/story.md
specs/F-001.1-<slug>/design.md
specs/F-001.1-<slug>/tasks.md
specs/F-001.1-<slug>/coding-prompt.md
specs/F-001.2-<slug>/story.md
... (one folder per F-XXX.X story)
specs/dependency-graph.md
```

Two framework violations occurred:
1. The orchestrator generated the handoff **inline** (directly writing files) instead of loading and executing the `skills/5-handoff/01-create-openspec-change-for-active-deliverable.md` skill prompt. The orchestrator's own rule says "if a persona skill exists for the required work, invoke that skill instead."
2. The orchestrator wrote files to `openspec/handoff/` — a path that does not exist in the allowed workspace structure. The allowed output path for OpenSpec handoff is `specs/`.

The hard stop in the handoff skill (Step 2) requires counting F-XXX.X IDs and creating exactly that many folders. This check was never run because the skill was never invoked.

Additionally, the API contract artifacts (`openapi.yaml`, `entities.json`) were placed in `specs/` — which is the handoff output path. This path collision means the handoff and the API contract gate output occupied the same folder, making it impossible to distinguish framework handoff from gate artifacts.

---

## What needs to change

### Change 1 — Add a skill-invocation gate to the orchestrator before writing handoff artifacts

**Location:** `brs-to-spec-run-workflow.md`, Step 5 (Pre-generation gate check), the "For handoff (`specs/`)" section.

**Add as the first bullet, before all existing handoff pre-checks:**

```markdown
**Skill invocation check — runs before any other handoff check:**
- [ ] Confirm you have loaded and are executing `.brs2spec/skills/5-handoff/01-create-openspec-change-for-active-deliverable.md`.
  - If you are about to write files to `specs/` or `standalone-delivery/` without having loaded this skill prompt:
    **STOP.** Do not create any files. Load the skill prompt first, read all its inputs in the order it specifies, then follow its Step 1 and Step 2 exactly.
  - Inline generation — writing story folders, design files, or tasks directly from the orchestrator without loading the skill prompt — is a framework violation. The handoff skill contains gate checks, story-count assertions, and output-format rules that cannot be replicated inline.
```

---

### Change 2 — Add a forbidden-path guard for `openspec/`

**Location:** `brs-to-spec-run-workflow.md`, Step 5, append to the "For handoff (`specs/`)" section as a new block after the repository descriptors check.

**New block:**

```markdown
**Forbidden output path check — runs after all other handoff checks:**
- [ ] Verify that no file is about to be written to `openspec/` (at any depth: `openspec/handoff/`, `openspec/changes/`, `openspec/by-repository/`, etc.).
  - `openspec/` is not a valid workspace path. It does not appear in the allowed workspace structure.
  - The correct output path for OpenSpec handoff artifacts is `specs/`.
  - If any planned output path starts with `openspec/`: stop, discard those planned paths, redirect to `specs/`.
  - **Why:** `openspec/` was a legacy path name used in earlier framework versions. It was replaced by `specs/`. Writing to `openspec/` creates orphan artifacts that are invisible to the orchestrator's stage gate chain.
```

---

### Change 3 — Add a pre-generation story-count assertion to the handoff skill

**Location:** `skills/5-handoff/01-create-openspec-change-for-active-deliverable.md`, Step 2, before "generate one folder per user story."

**The existing hard stop text (preserved):**
```
> **HARD STOP before creating any folder:**
> 1. Count the `F-XXX.X` story IDs in `planning/delivery-structure.md`. Write that number down.
> 2. You must create exactly that many folders…
> 3. Never create a folder named after the deliverable or the epic…
> 4. If you are uncertain whether to create one folder or many — the answer is always many…
```

**Add immediately after the existing hard stop block:**

```markdown
> **Story-count assertion — run before creating the first folder:**
>
> 1. List every `F-XXX.X` ID found in `planning/delivery-structure.md` (or the delivery structure folder). Write the list explicitly: `F-001.1, F-001.2, F-002.1, ...`
> 2. Count them. Write the count: `N stories found.`
> 3. Confirm: `I will create exactly N folders: specs/F-001.1-<slug>/, specs/F-001.2-<slug>/, ...`
> 4. Do not begin creating folders until this assertion is written out.
>
> **If the delivery structure is corrupt (multiple versions concatenated):**
> - Do not attempt to extract story IDs from a corrupt delivery-structure file.
> - Stop. State: "planning/delivery-structure.md is corrupt (multiple concatenated versions). Execute repair-workspace-state.md before running the handoff."
> - Do not create any folder. Do not write any file.
>
> **If the delivery structure is in draft state (epics/features only, no F-XXX.X story IDs):**
> - Do not proceed to handoff.
> - Stop. State: "planning/delivery-structure.md is still at draft stage — no F-XXX.X story IDs found. Execute stage 9 (delivery-structure-confirmed) first."
> - Do not create any folder. Do not write any file.
```

---

### Change 4 — Clarify the API contract gate output path to prevent collision with handoff path

**Location:** `skills/4-engineering-readiness/quality-gates/create-api-contract.md` — add an output path note.

> This change is a clarification only — the API contract gate artifact belongs at `quality-gates/api-contract.md`, not at `specs/openapi/openapi.yaml`. The `specs/` path is reserved exclusively for OpenSpec handoff story folders and `dependency-graph.md`. Any API-level schema, OpenAPI document, or JSON schema produced as a quality gate artifact must be placed inside `quality-gates/api-contract.md` as an inline section or linked from it — not in a separate file under `specs/`.

**Location:** add to the Output path section of `skills/4-engineering-readiness/quality-gates/create-api-contract.md`:

```markdown
## Output path

```text
quality-gates/api-contract.md
```

> **Path note:** Do not write OpenAPI documents, JSON schemas, or contract examples to `specs/`. The `specs/` directory is reserved for OpenSpec handoff story folders. API schemas produced as part of this gate belong inline in `quality-gates/api-contract.md` (as fenced code blocks) or as links to files in `quality-gates/schemas/`. Writing gate artifacts to `specs/` collides with handoff output and makes the gate invisible to the stage gate chain.
```

---

### Change 5 — Add a workspace path validation rule to `agent-instructions.md`

**Location:** "Framework bypass prevention" section, after the existing allowed-paths block.

**Add:**

```markdown
**Handoff output path rule:** `specs/` contains only:
- `specs/dependency-graph.md`
- `specs/F-XXX.X-<slug>/` — one subfolder per confirmed user story, each containing `story.md`, `design.md`, `tasks.md`, `coding-prompt.md`

Nothing else belongs in `specs/`. API schemas, OpenAPI documents, JSON schemas, and gate-level artifacts belong in `quality-gates/`. A file in `specs/` that is not a story folder or the dependency graph is a misplaced artifact — move it to the correct path before the handoff stage runs.
```

---

## Implementation steps

1. Open `.brs2spec/brs-to-spec-run-workflow.md`.
   - In Step 5, "For handoff (`specs/`)" section: insert the skill-invocation check from Change 1 as the very first bullet.
   - In Step 5, "For handoff (`specs/`)" section: append the forbidden-path guard from Change 2 after the repository descriptors check.

2. Open `.brs2spec/skills/5-handoff/01-create-openspec-change-for-active-deliverable.md`.
   - In Step 2, after the existing HARD STOP block: insert the story-count assertion from Change 3.

3. Open `.brs2spec/skills/4-engineering-readiness/quality-gates/create-api-contract.md`.
   - Add or update the Output path section with the path note from Change 4.

4. Open `.brs2spec/agent-instructions.md`.
   - In "Framework bypass prevention", after the allowed-paths block: insert the handoff output path rule from Change 5.

---

## Quality bar

After these changes:

- The orchestrator cannot generate any handoff file without first loading the handoff skill prompt.
- No file is ever written to `openspec/` — the path is explicitly forbidden and redirected.
- The handoff skill writes out a complete list of F-XXX.X IDs and confirms the folder count before creating a single folder. A corrupt or draft delivery structure stops the handoff cold.
- API contract gate artifacts (OpenAPI, JSON schema) live in `quality-gates/` — not in `specs/`. Path collision between gate artifacts and story folders is impossible.
- `specs/` contains only story folders (`F-XXX.X-slug/`) and `dependency-graph.md`.
