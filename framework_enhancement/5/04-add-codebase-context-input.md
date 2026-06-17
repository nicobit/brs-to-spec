# Enhancement 5.4 — Add Codebase Context Input

## Problem

The framework has no structured place for the user to describe the existing repository. Without this:
- `coding-prompt.md` file paths are guessed from `design.md` narrative
- Validation commands are derived from the technology stack name — not from what actually works in the project
- Coding agents may follow wrong patterns, use wrong folder conventions, or touch files they shouldn't

This is **user-provided information** — the framework cannot scan a repository autonomously. It belongs in `input/` as `input/codebase-context.md`, written by a developer who knows the repo.

---

## What needs to change

### Change 1 — Create `input/codebase-context.md` template

Create `.brs2spec/templates/input-preparation/codebase-context.md`:

```markdown
# Codebase Context

> **Owner:** Engineering Lead / Developer
> **Purpose:** Describe the existing repository so coding agents know where to work, which patterns to follow, and how to validate their output.
> **When to fill:** Before handoff generation. Can be filled incrementally — partial information is better than none.

## Repository overview

<!-- Brief description of the repository — what it does, its main layers, and its technology stack -->

| Field | Value |
|---|---|
| Repository name | |
| Primary language / framework | |
| Architecture style | e.g. Layered / Clean / Hexagonal / Microservices |
| Database technology | |
| Test framework | |
| Build tool | |

## Folder structure

<!-- Key folders only — not every directory. Focus on where new code will likely go. -->

```text
src/
  Api/             — HTTP controllers and request/response models
  Application/     — use cases, commands, queries
  Domain/          — entities, value objects, domain rules
  Infrastructure/  — DB, external service adapters
tests/
  Unit/
  Integration/
  E2E/
```

## Patterns to follow

<!-- Coding patterns, naming conventions, and structural rules the AI must respect -->
<!-- Be specific — "use the repository pattern" is not enough; name the base class or interface -->

| Pattern | Description | Example location |
|---|---|---|
| Command pattern | All write operations go through a Command + Handler | `src/Application/Onboarding/CreateOnboardingCommand.cs` |
| Repository pattern | Data access via IRepository<T> | `src/Infrastructure/Repositories/` |

## Files and areas NOT to touch

<!-- Explicit exclusions — files that must not be modified by the coding agent -->

| Path / area | Reason |
|---|---|
| `src/Infrastructure/Migrations/` | DB migrations are managed manually — do not auto-generate |
| `src/Api/Program.cs` | Startup config — requires architect review before change |

## Existing capabilities map

<!-- Which business capabilities already exist and where their code lives -->
<!-- Fill only for capabilities relevant to this initiative -->

| Capability | Module / path |
|---|---|
| Customer authentication | `src/Application/Auth/` + `src/Api/Controllers/AuthController.cs` |
| Notification sending | `src/Infrastructure/Notifications/` |

## Validation commands

<!-- Exact commands to run after implementation to verify the output is correct -->
<!-- These are copied verbatim into coding-prompt.md for each story -->

```bash
# Build
dotnet build

# Unit tests
dotnet test tests/Unit/ --logger "console;verbosity=normal"

# Integration tests (requires running DB)
dotnet test tests/Integration/ --filter Category=Integration

# Lint / format check
dotnet format --verify-no-changes
```

## Known constraints

<!-- Any additional constraints a coding agent must know that are not in architecture-rules.md -->
<!-- e.g. third-party SDK versions, deprecated patterns still in use, pending migrations -->

- {{constraint}}
```

---

### Change 2 — `skills/5-handoff/01-create-openspec-change-for-active-deliverable.md`

**Add to the Inputs section:**

```
15. `input/codebase-context.md` — **if exists**: repo structure, patterns to follow, files not to touch, existing capabilities map, validation commands; used to populate `coding-prompt.md` files-to-touch table and validation commands section; if missing, note the gap in dependency-graph.md preamble
```

**Add to the coding-prompt.md generation rules:**

```
### Codebase context propagation

If `input/codebase-context.md` exists:
- Files to touch table: cross-reference the "Existing capabilities map" and "Folder structure" sections to derive accurate file paths for this story; do not invent paths not consistent with the repo structure
- Validation commands: copy the "Validation commands" section verbatim into every coding-prompt.md — do not vary per story
- What you must NOT do: merge the "Files and areas NOT to touch" entries from codebase-context.md with the AR-NNN forbidden patterns — list all in the "What you must NOT do" section
- Known constraints: add any entries from the "Known constraints" section that apply to this story's scope

If `input/codebase-context.md` does not exist:
- Files to touch: derive from design.md narrative only; add a note: `<!-- Paths estimated from design.md — no codebase-context.md found. Verify before editing. -->`
- Validation commands: derive from technology stack in initiative-context.md; add a note: `<!-- Commands estimated from tech stack — verify against actual project. -->`
```

**Add to the self-review checklist:**

```
- [ ] If `input/codebase-context.md` exists: file paths in coding-prompt.md "Files to touch" are consistent with the repo structure described there
- [ ] If `input/codebase-context.md` exists: validation commands copied verbatim — not paraphrased
- [ ] If `input/codebase-context.md` missing: gap noted in dependency-graph.md preamble
```

---

### Change 3 — `brs-to-spec-run-workflow.md` Step 0 input quality assessment

Add a new row to the key input artifacts table in Step 0:

```
| `input/codebase-context.md` | Check if exists | Has repo structure, patterns, validation commands? | If missing: surface to user once at handoff stage — "No codebase-context.md found. File paths and validation commands in coding-prompt.md will be estimated. Create `input/codebase-context.md` for accurate handoff." Do not block handoff — note the gap. |
```

---

### Change 4 — `brs-to-spec-run-workflow.md` Step 5 pre-generation gate check (handoff block)

Add a soft check (not a hard blocker):

```
- [ ] Check whether `input/codebase-context.md` exists. If it does not: surface once — "No codebase-context.md found. File paths and validation commands will be estimated from design.md and initiative-context.md. To get accurate file paths in coding-prompt.md, create input/codebase-context.md before proceeding." Then continue — this is a quality warning, not a hard gate.
```

---

### Change 5 — `agent-instructions.md` Allowed paths

Add `input/codebase-context.md` to the list of user-writable paths:

The boundary rule states: "users own `input/`; the framework owns everything else." `codebase-context.md` in `input/` is consistent with this rule — no change needed to the boundary rule itself. But it should be mentioned explicitly in the Input boundary rule section as an example of a valid user-authored input file.

---

## Implementation steps

1. Create `.brs2spec/templates/input-preparation/codebase-context.md` with the template above
2. Open `.brs2spec/skills/5-handoff/01-create-openspec-change-for-active-deliverable.md`:
   - Add item 15 to the Inputs section
   - Add "Codebase context propagation" subsection to coding-prompt.md generation rules
   - Add three items to the self-review checklist
3. Open `.brs2spec/brs-to-spec-run-workflow.md`:
   - Add `input/codebase-context.md` row to Step 0 input quality table
   - Add soft check in Step 5 handoff pre-generation gate

## Quality bar

After this change:
- A developer fills `input/codebase-context.md` once per initiative — it is the single source of truth for repo structure and validation commands
- Every `coding-prompt.md` has accurate file paths (not guessed) and runnable validation commands (not inferred from tech stack name)
- The framework never blocks handoff for missing codebase context — it surfaces a warning and proceeds
- "Files and areas NOT to touch" from codebase context are merged into the "What you must NOT do" section of every relevant coding-prompt.md
