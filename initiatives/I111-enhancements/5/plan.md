# Framework Enhancement 5 — Earlier Business Analysis, Codebase Awareness, Executable Handoff

## Problem statement

Four gaps remain after enhancement 4:

1. **Process flows and use cases created too late.** Both skills hard-require confirmed F-XXX.X stories. This means the delivery lead shapes stories without knowing the full process flows — and process flows often reveal missing stories or wrong story boundaries. They should exist as drafts before delivery structure is drafted, then be confirmed/completed after stories are confirmed.

2. **Handoff has no file-level guidance.** `coding-prompt.md` tells the agent what to build and what rules apply, but not *where* in the codebase to build it. For brownfield initiatives an agent without file paths invents its own structure. A structured `affected-files` section inside `coding-prompt.md` closes this gap.

3. **Handoff has no validation commands.** The definition of done says "tests pass" but does not say how to run them. An autonomous agent must be told the exact commands to execute. A `validation-commands` section in `coding-prompt.md` closes this gap.

4. **No codebase context input.** The framework has no place for the user to describe the existing repository — its structure, patterns to follow, conventions, and areas not to touch. This is user-provided information (the framework cannot scan a repo autonomously), so it belongs in `input/` as `input/codebase-context.md`. The handoff skill then reads it and propagates relevant content into each `coding-prompt.md`.

## What this enhancement does NOT do

- Does not add new phases or personas
- Does not require 33 stages
- Does not make codebase discovery a framework-generated artifact — it is always user-provided
- Does not restructure process flows or use cases — it adds a draft mode to both existing skills

## Four targeted changes

| # | File | Change type | Effort |
|---|---|---|---|
| 1 | `01-add-draft-mode-to-process-flows.md` | Add draft mode to process flows skill + resequence in workflow | Medium |
| 2 | `02-add-draft-mode-to-use-cases.md` | Add draft mode to use cases skill + resequence in workflow | Medium |
| 3 | `03-add-affected-files-and-validation-to-coding-prompt.md` | Add affected-files table + validation-commands to coding-prompt template and handoff skill | Low |
| 4 | `04-add-codebase-context-input.md` | Add `input/codebase-context.md` as user-provided input; wire into handoff skill and coding-prompt | Low |

## Recommended implementation order

1 → 2 → 3 → 4

Changes 1 and 2 touch the workflow runner sequencing and skill stop conditions.
Changes 3 and 4 are purely additive to existing templates and skill inputs.

---

## Enhancement 1 — Draft process flows before delivery structure

**Core idea:** the process flows skill gets a **draft mode** that works from epics (not confirmed F-XXX.X stories), and a **confirmed mode** that works from confirmed stories. Draft mode runs at stage 2d (after actors). Confirmed mode stays at 9b (after confirmed stories).

**Why two modes work:** at draft stage the flow uses epic names and BRS narrative to identify the main path, decision points, and alternative branches. It marks story references as `<!-- to be linked after delivery structure is confirmed -->`. At confirmed stage (9b) it enriches the draft with F-XXX.X IDs, AC-NNN references, and correct step ordering derived from story dependencies.

## Enhancement 2 — Draft use cases before delivery structure

**Core idea:** same pattern as process flows. Use case skill gets a draft mode (stage 2e, after actors + draft process flows) and confirmed mode (stage 9c, after confirmed stories + confirmed process flows). Draft mode works from epics and BRS objectives. Confirmed mode enriches with F-XXX.X IDs and AC-NNN coverage.

## Enhancement 3 — Affected files and validation commands in coding-prompt

**Core idea:** add two sections to `coding-prompt.md` template:
- `## Files to touch` — structured table: file path, change type (create/modify/delete), reason; derived from `design.md` "What this story touches" section
- `## Validation commands` — copy from `input/codebase-context.md` validation-commands section; the agent runs these after implementation to verify its own output

## Enhancement 4 — Codebase context input

**Core idea:** `input/codebase-context.md` is a user-provided file (not framework-generated) that captures the existing repository structure, patterns, conventions, and validation commands. The handoff skill reads it when present and propagates:
- validation commands → `coding-prompt.md` validation section
- patterns to follow / not to follow → supplements the "What you must NOT do" section
- repo structure overview → informs the affected-files table in design.md and coding-prompt.md
