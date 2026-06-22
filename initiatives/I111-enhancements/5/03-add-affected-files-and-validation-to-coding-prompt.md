# Enhancement 5.3 — Add Affected Files and Validation Commands to coding-prompt.md

## Problem

The current `coding-prompt.md` template tells the coding agent:
- What to build (goal)
- What rules constrain it (BR-NNN, AR-NNN)
- What the acceptance criteria are (AC-NNN)
- Which BDD scenarios to pass (SCN-NNN)
- What tasks to execute
- What it must NOT do

It does not tell the agent:
- **Which files to touch** — the agent must infer this from `design.md` narrative; for brownfield work it will often guess wrong
- **How to verify its own output** — "tests pass" in the DoD is not executable; the agent needs the exact commands

Both gaps leave room for the agent to invent its own approach, which is exactly what the framework is designed to prevent.

---

## What needs to change

### Change 1 — `.brs2spec/templates/openspec-handoff/coding-prompt.md`

Add two new sections between "Tasks" and "What you must NOT do":

```markdown
## Files to touch

<!-- Source: design.md "What this story touches" section — translate to structured table -->
<!-- If input/codebase-context.md exists: cross-reference with known repo structure -->
<!-- Change type: create | modify | delete -->

| File path | Change type | Reason |
|---|---|---|
| {{src/path/to/file}} | create / modify / delete | {{one-line reason — e.g. "new endpoint for this story"}} |

## Validation commands

<!-- Source: input/codebase-context.md validation-commands section if it exists -->
<!-- If codebase-context.md does not exist: derive from initiative technology stack in initiative-context.md -->
<!-- Run these commands after implementation. If they fail, fix before declaring done. -->

```bash
{{command 1 — e.g. dotnet build}}
{{command 2 — e.g. dotnet test --filter Category=Unit}}
{{command 3 — e.g. npm run lint}}
```

If a command cannot be run in the current environment, note why and report to the human.
```

**Updated Definition of done section** — add two new items:

```markdown
## Definition of done

- [ ] All tasks in the Tasks section implemented
- [ ] All AC-NNN acceptance criteria pass as stated above
- [ ] All BDD scenarios listed above pass
- [ ] All AR-NNN rules respected — no forbidden patterns introduced
- [ ] All BR-NNN rules enforced in the implemented code
- [ ] Only files listed in "Files to touch" modified — no out-of-scope changes
- [ ] All validation commands run and pass
- [ ] Tests added for each AC-NNN
```

---

### Change 2 — `skills/5-handoff/01-create-openspec-change-for-active-deliverable.md`

In the `### coding-prompt.md (per story — mandatory)` section, update the "Sections to populate" list:

**Add after "Tasks":**

```
- **Files to touch** — translate the "What this story touches" paragraph from `design.md` into a structured table of file paths, change type (create/modify/delete), and one-line reason; if `input/codebase-context.md` exists, cross-reference with the repo structure section to use accurate file paths
- **Validation commands** — copy from `input/codebase-context.md` validation-commands section if it exists; if it does not exist, derive from the technology stack in `engineering-readiness/initiative-context.md` (e.g. `dotnet test` for .NET, `npm run test` for Node); if the stack cannot be determined, write a placeholder with a note
```

**Update the self-review checklist for coding-prompt.md:**

```
- [ ] Every `coding-prompt.md` has a "Files to touch" table with at least one row (or explicit "no files identified" note)
- [ ] Every `coding-prompt.md` has a "Validation commands" section with runnable commands or an explicit gap note
```

---

### Change 3 — `brs-to-spec-run-workflow.md` stage 13 done criteria

Update:

**Current:** `coding-prompt.md lists BR-NNN, AR-NNN, SCN-NNN, and forbidden patterns`

**Change to:** `coding-prompt.md lists BR-NNN, AR-NNN, SCN-NNN, forbidden patterns, files-to-touch table, and validation commands`

---

## Implementation steps

1. Open `.brs2spec/templates/openspec-handoff/coding-prompt.md`
   - Add "Files to touch" section after Tasks
   - Add "Validation commands" section after Files to touch
   - Update Definition of done checklist

2. Open `.brs2spec/skills/5-handoff/01-create-openspec-change-for-active-deliverable.md`
   - Add "Files to touch" and "Validation commands" to the coding-prompt.md Sections to populate list
   - Add two items to the self-review checklist

3. Open `.brs2spec/brs-to-spec-run-workflow.md`
   - Update stage 13 done criteria

## Quality bar

After this change:
- A coding agent reading only `coding-prompt.md` knows which files to open, what to change in each, and which commands to run to verify its work
- "Files to touch" is a structured table, not prose — the agent does not need to parse paragraphs
- "Validation commands" are executable — not "ensure tests pass"
- The DoD explicitly checks that no out-of-scope files were modified
