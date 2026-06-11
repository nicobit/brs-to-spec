# BRS to Spec Framework — Copilot Instructions

Framework behavioral rules are in `.github/instructions/brs-to-spec.instructions.md`,
scoped to `initiatives/**` via `applyTo` frontmatter.

This file is intentionally minimal. Do not add project rules here —
the framework has no project-specific coding conventions of its own.

## Framework activation — always active

Whenever the user mentions an initiative, asks about status, next steps, what to do, or anything related to a BRS or delivery workflow — even if no `initiatives/` file is open — apply the rules from `.github/instructions/brs-to-spec.instructions.md` in full.

Specifically:
- Read `.brs2spec/module-index.md` first.
- Do not answer from BRS content. Run the workflow.
- Do not invent next steps. Run `.brs2spec/brs-to-spec-run-workflow.md`.
- Do not create artifacts outside the allowed workspace paths.
- Never create tasks directly from a BRS.

## Hard stop — before creating any file or folder

**Before creating, editing, or deleting any file or folder inside `initiatives/`:**

1. STOP. Do not create anything yet.
2. Identify the active initiative workspace (`initiatives/<id>-<slug>/`).
3. Check whether `planning/workflow-state.json` exists in that workspace.
4. Read `.brs2spec/module-index.md`.
5. Run `.brs2spec/brs-to-spec-run-workflow.md`.

Only create files that the workflow runner explicitly instructs you to create, at the path it specifies.

**Creating files speculatively, inventing folder structures, or scaffolding artifacts not produced by a framework skill is a framework violation. Stop and run the workflow instead.**

## Hard stop — before answering "what should I do?" or "what is next?"

Do not read the BRS and summarize it. Do not invent a plan. Do not present options.

1. Read `planning/workflow-state.json` if it exists.
2. Run `.brs2spec/brs-to-spec-run-workflow.md`.

The workflow runner will determine and execute the next step. Your job is to run it, not to answer around it.
