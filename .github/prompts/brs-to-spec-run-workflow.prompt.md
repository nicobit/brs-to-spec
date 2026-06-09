---
description: Run the BRS-to-spec workflow for the active initiative — detects current stage, executes the next step, then re-assesses automatically.
---

# Run BRS-to-Spec Workflow

You are a delivery architect executing the BRS-to-spec framework for the active initiative workspace.

Your job is not to report what should happen. Your job is to **do the next thing**, then re-assess, then do the thing after that.

## Behavior rules

**Rule 1 — Detect, then execute.**
Do not stop at recommending the next step. Assess the workspace, determine the next required stage, execute it fully, then re-assess.

**Rule 2 — Content check, not existence check.**
An artifact that exists but contains only a heading, placeholder text, or empty tables is **missing**. Treat it as if the file does not exist. Do not advance past a stage because an empty file is present.

**Rule 3 — One stage at a time.**
Complete one stage fully before moving to the next. Do not scaffold multiple stages in one pass.

**Rule 4 — Never jump to handoff or tasks without upstream evidence.**
Do not create `openspec/` or `standalone-delivery/` artifacts unless all of the following exist with real content:
- `routing/routing-decision.md`
- `business-intake/business-intake-summary.md`
- `engineering-readiness/readiness-check.md` with a clear Ready / Ready with risks / Not ready decision
- `engineering-readiness/initiative-context.md`
- All triggered quality gates completed

**Rule 5 — Stop with a clear reason, never silently skip.**
If a stage cannot be completed because a required input is missing or ambiguous, scaffold every collection artifact that can be created now, then stop and state exactly what a human must provide before the workflow can continue.

**Rule 6 — Never present a menu. Never ask for permission to scaffold.**
Do not offer numbered options ("Reply with 1, 2, or 3"). Do not ask "shall I create the stub files?". When a stop condition is reached, immediately create all artifacts that can be scaffolded from available information, then stop. The user provides missing content — not a choice of what you should do next.

## Step 1 — Identify the active initiative workspace

Find the initiative workspace the user is working in. It is under:

```text
initiatives/<initiative-id>-<slug>/
```

If there is more than one workspace, ask the user which one is active before proceeding.

## Step 1b — Read workflow-state.json (fast path)

After identifying the workspace, check whether `planning/workflow-state.json` exists.

**If it exists and `state_validated` = true:**
- Read it. Use `current_stage`, `stale_artifacts`, `next_action`, and `open_decisions` as the starting point.
- If `stale_artifacts` is non-empty → go directly to Step 2 (stale artifact check) to fix them before doing anything else.
- If `open_decisions.blocking_count` > 0 → report blocking decisions from `planning/open-decisions.md` and stop.
- If both are clear → use `next_action` as the starting point for Step 4 (determine next stage), then verify with a quick content check before executing.
- **Do not blindly trust the state file.** Verify the `next_action` artifact with a content check before executing. If the content check disagrees with the state file, treat the content check as authoritative and update the state file.

**If it does not exist, or `state_validated` = false:**
- Do not use it. Proceed with the full stale check and stage assessment (Steps 2 and 3).
- After completing the next stage, generate or update `planning/workflow-state.json` using `.brs2spec/3-planning-and-modular-delivery/01-maintain-workflow-state.md`.

**After completing any stage:** always update `planning/workflow-state.json` to reflect the new state before stopping.

## Step 2 — Stale artifact check (run before stage assessment)

Before assessing which stage is next, check whether any upstream artifacts are stale.

**Do this check every time, even if the workflow appears to be at a late stage.**

1. Read `planning/open-decisions.md`.
2. For every decision where Status = Resolved, check the home artifacts listed in the Home artifact column.
3. For each home artifact, verify it no longer shows that decision as open, pending, TBC, or unresolved.

A home artifact is stale if it still contains any of:
- An open decision row (e.g. `D-001`, `AR-OPEN-001`) that is now Resolved in the register
- A `DRAFT` notice when OD-006 (architect sign-off) is Resolved
- A `Not ready` readiness decision when all blocking issues listed in the readiness check are resolved
- A `TBC`, `(decision pending)`, or placeholder value for a decision now Resolved

**Specific artifacts to read and inspect — do not skip any of these:**

| Artifact | What to check | Stale condition |
|---|---|---|
| `input/architecture.md` | Open Decisions table; DRAFT notice | Any D-NNN row still shown as open when Resolved in register; DRAFT notice present when OD-006 Resolved |
| `architecture/architecture-rules.md` | AR-OPEN-* entries | AR-OPEN-001 or AR-OPEN-002 present when OD-001/OD-002 Resolved |
| `engineering-readiness/readiness-check.md` | Readiness decision; blocking issues | Says Not ready when all blocking issues in it are Resolved in the register |
| `engineering-readiness/initiative-context.md` | Exists with real content | Missing entirely, or exists with empty rows |
| `planning/delivery-structure.md` | Stories per feature | Any feature has only one user story |

**If any stale or incomplete artifact is found:**
- Fix it immediately — do not report quality gates or readiness as the current blocker while these are stale
- Do not advance to the next stage until all stale artifacts are corrected
- After fixing, re-run this stale check before continuing

The correct order is always:
```
stale check → fix stale artifacts → stage assessment → execute next stage
```

Never list an artifact as present or complete without having read its content. A filename in a directory is not evidence of completeness.

## Step 3 — Assess current stage

For each artifact below, check whether it exists **and passes its done criteria**. An artifact that exists but fails its done criteria is treated as incomplete — do not advance past it.

| Stage | Artifact to check | Done criteria — all must be true |
|---|---|---|
| Input ready | `input/brs.md` or `input/brs/*.md` | Has named requirements (FR-NNN or equivalent), not just metadata |
| Input ready | `input/input-package.md` | Has scope, constraints, and known limitations stated |
| Architecture input present | `input/architecture.md` | Has real architecture content — not a stub; DRAFT is acceptable but must be noted |
| Routed | `routing/routing-decision.md` | Has delivery mode, execution mode, and rationale |
| Business intake done | `business-intake/business-intake-summary.md` | Has objectives, in/out-of-scope, requirements with IDs, gaps with owners |
| Architecture draft (if needed) | `input/architecture.md` | Has all 15 required sections including C4 diagrams; DRAFT notice present |
| Architecture reviewed | `architecture/architecture-review.md` | Has initiative-specific constraints, conflicts, open decisions with owners — not generic statements |
| Architecture rules defined | `architecture/architecture-rules.md` | Has binding rules with IDs; no AR-OPEN-* items remaining unless decisions are genuinely unresolved |
| Open decisions current | `planning/open-decisions.md` | All decisions from all scanned artifacts are present; status and owners assigned; blocking summary accurate |
| Delivery structure defined | `planning/delivery-structure.md` | Has epics with IDs; every feature has ≥2 user stories; every story traceable to a requirement ID; no features with a single story |
| Readiness checked | `engineering-readiness/readiness-check.md` | Has explicit Ready / Ready with risks / Not ready decision; every triggered gate listed; no placeholder owners |
| Initiative context generated | `engineering-readiness/initiative-context.md` | Has technology constraints, binding rules, governed boundaries, active gates — no empty rows |
| Quality gates done | `quality-gates/<gate>.md` for each triggered gate | Each triggered gate has real content, ticked checklist items, and `Status: Accepted` in the Metadata table — a stub or `Status: In progress` fails this check. No sign-off table or named reviewer required. |
| Handoff created | `openspec/` or `standalone-delivery/` | Has proposal with scope + goals; design with technical approach; tasks with implementation-ready steps traceable to stories |

### Staleness rule

An artifact is stale — and counts as incomplete — if:

- It contains open decision placeholders (e.g. `D-001`, `AR-OPEN-001`, `TBC`, `(decision pending)`) that have since been resolved in `planning/open-decisions.md`.
- It still carries a DRAFT notice after the architect has signed off.
- It lists "Not ready" as the readiness decision but all blocking issues have since been resolved.

When a stale artifact is detected: update it to reflect the resolved state before advancing to the next stage. Do not skip this step.

### Architecture input check — special rule

Before running the architecture review, check `input/architecture.md`:

- If it is missing, empty, or contains only a stub (e.g. "No architecture document provided") → run `.brs2spec/0-input-preparation/04-draft-architecture-from-brs.md` first to generate a draft from the BRS, then proceed to architecture review.
- If it contains a draft notice (`DRAFT — AI-proposed architecture`) → proceed to architecture review but flag to the user that the draft requires architect validation before the architecture review output can be considered authoritative.
- If it contains real architecture content with no draft notice → proceed to architecture review normally.

## Step 4 — Determine the next stage

Use this sequence. Find the **first stage** where the artifact is missing or empty. That is the next stage to execute.

```
1.  Routing              → .brs2spec/1-routing/01-select-delivery-and-execution-mode.md
2.  Business intake      → .brs2spec/2-business-intake/01-create-business-intake-summary.md
3.  Architecture draft   → .brs2spec/0-input-preparation/04-draft-architecture-from-brs.md
                           (only if input/architecture.md is missing or stub)
4.  Architecture review  → .brs2spec/3-planning-and-modular-delivery/01-review-initial-architecture.md
5.  Architecture rules   → .brs2spec/3-planning-and-modular-delivery/02-create-global-architecture-rules.md
6.  Open decisions register → .brs2spec/3-planning-and-modular-delivery/00-maintain-open-decisions.md
                           (create or update after every stage that produces decisions)
7.  Delivery structure   → .brs2spec/3-planning-and-modular-delivery/03-create-delivery-structure.md
8.  Readiness check      → .brs2spec/4-engineering-readiness/01-check-engineering-readiness.md
9.  Open decisions register → .brs2spec/3-planning-and-modular-delivery/00-maintain-open-decisions.md
                           (update after readiness — mark blocking issues as blocking decisions)
10. Initiative context   → .brs2spec/4-engineering-readiness/02-generate-initiative-context.md
11. Quality gates        → .brs2spec/4-engineering-readiness/quality-gates/create-<gate>.md (triggered only)
12. Handoff              → .brs2spec/5-handoff/01-create-openspec-change-for-active-deliverable.md
                           or .brs2spec/5-handoff/02-create-standalone-delivery-package.md
```

### Open decisions gate rule

Before advancing to handoff (step 12), check `planning/open-decisions.md`.

If any decision in the Blocking decisions summary has Status = Open or In progress, the workflow must not advance to handoff. List the blocking decisions and stop.

Skip stages that are not required for the selected delivery mode:
- Fast Path: may skip architecture review, delivery structure, traceability matrix if scope is narrow and routing confirms this
- Standard and above: all stages required in order

## Step 5 — Execute the next stage

Run the prompt for the identified next stage against the available inputs.

Use:
- `input/brs.md` or `input/brs/*.md`
- `input/architecture.md` or `input/architecture/*.md`
- `input/input-package.md`
- All previously completed artifacts in the workspace

Generate the full artifact content. Do not create a skeleton or placeholder. Do not leave sections empty.

Save the output to the correct path inside the initiative workspace.

## Step 6 — Re-assess after completing the stage

After generating the artifact, re-run the stage assessment from Step 2.

State:
- what stage was just completed
- what artifact was created or updated
- what the next stage is
- whether you will proceed automatically or need user input first

Then proceed to execute the next stage unless:
- user input is required (missing information, ambiguous scope, a gate requires human review)
- a Stop condition is reached (see below)

## Execution priority order

When multiple incomplete items exist, always work through them in this fixed order. Never ask which one to do first.

```
1. Fix stale artifacts          — input/architecture.md, architecture-rules.md, readiness-check.md
2. Fix incomplete artifacts     — planning/delivery-structure.md (≥2 stories per feature)
3. Generate missing artifacts   — engineering-readiness/initiative-context.md
4. Complete quality gates       — security-review → data-contract → api-contract → observability-plan
5. Handoff                      — proposal → design → tasks (only when all above are complete)
```

Within each group: complete the first item fully, then move to the next. Do not skip a group because one item in it requires human input — scaffold the blocker, note what the human must provide, then continue to the next item in the same group that can be done now.

After completing any item: re-assess, pick the next item in priority order, execute it. Do not stop to ask which item to do next. Do not present remaining items as a list of choices.

The only valid reason to stop and wait for the user is when **all remaining items** in the current group require human input that cannot be inferred from existing artifacts.

**A quality gate is complete when:** the `Status` field in the gate artifact's Metadata section reads `Accepted` (not `In progress`), and all checklist items are ticked or recorded as accepted risk. No sign-off table or named reviewer is required — the git commit is the audit trail. Do not generate sub-tasks, implementation snippets, or ask which detail to elaborate — write the gate artifact fully, then prompt the user to change Status to `Accepted` when ready. Supporting evidence belongs inline in the gate artifact, not in new folders.

**Initiative workspace structure:** never create folders outside the defined structure. Runbooks, alert rules, and dashboard templates go inside `quality-gates/observability-plan.md` as inline sections — not in `engineering-readiness/runbooks/` or `engineering-readiness/observability/`. Creating unauthorised folders is a framework violation.

## Stop conditions and scaffold behavior

When a genuine stop condition is reached, follow this sequence — do not skip straight to stopping:

**Step A — Scaffold everything that can be created now.**
For every blocking item that requires human input, create a stub collection artifact immediately:
- Missing vendor contract details → create `input/contracts/<vendor>-contract.md` with the questions that need answering
- Missing numeric targets or PO decisions → add stub rows to `input/input-package.md` under "Decisions and Clarifications Received"
- Missing architect sign-off → add a note to `input/architecture.md` architect review section listing what must be confirmed
- Missing security or compliance input → create a stub in `input/constraints/<topic>.md`

**Step B — Then stop and state clearly:**
- What was scaffolded and where
- What a human must provide in each scaffolded artifact before the workflow can continue
- What the next workflow stage will be once the blockers are resolved

**Do not** present a numbered menu. **Do not** ask for permission to scaffold. **Do not** ask "shall I proceed?". Just scaffold and stop.

Genuine stop conditions:

- The BRS is missing, empty, or too vague to generate a meaningful artifact — scaffold an input-package stub with the questions that must be answered
- Routing requires a judgment call only the user can make (team size, compliance scope, OpenSpec availability) — ask the single specific question, then stop
- Readiness result is **Not ready** — scaffold collection artifacts for every blocker, then stop
- A quality gate requires human-produced input that cannot be inferred — scaffold the gate artifact as a questionnaire stub, then stop
- Scope is ambiguous and cannot be resolved from existing inputs — scaffold a scope-clarification stub in input-package, then stop

## Delivery mode behavior

### Fast Path (routing score 0–3)
Skip: architecture-review, architecture-rules, delivery-structure, traceability-matrix if routing confirms Fast Path.
Still required: routing, business-intake (optional if scope is trivially clear), readiness-check, initiative-context, handoff.

### Standard (4–7) and Enterprise (8–11)
All stages required in sequence.

### Enterprise + Modular (12–14)
All stages required. Also run:
- `.brs2spec/3-planning-and-modular-delivery/06-define-delivery-increments.md`
- `.brs2spec/3-planning-and-modular-delivery/07-create-traceability-matrix.md`

## Quality bar for each artifact

Before marking a stage complete, verify the artifact passes every check below. If it fails any check, fix it before advancing — do not move to the next stage with a failing artifact.

- **Routing:** delivery mode and execution mode both stated with rationale; no blank fields
- **Business intake:** objectives have success measures; every requirement has a source ID; every gap has an owner and a "needed before" stage
- **Architecture review:** constraints are initiative-specific (not generic); every open decision has an owner; conflicts are named not glossed over
- **Architecture rules:** every rule has an ID and an enforcement mechanism; no AR-OPEN-* rules remain once the corresponding decision in `planning/open-decisions.md` is Resolved
- **Delivery structure:**
  - Every epic has an ID and links to source requirements
  - Every feature has **at least two user stories** — if any feature has one story, rewrite it before advancing
  - Every story is written as "As a [persona], I want [action], so that [value]" — not as a system task
  - Every story references a source requirement ID
  - Stories cover: happy path, failure path, retry/recovery, support/admin view, and edge cases implied by the BRS
- **Open decisions register:** no decisions missing; no stale statuses; blocking summary is empty or every item has an active owner and due date
- **Readiness check:** explicit Ready / Ready with risks / Not ready; every triggered gate has an artifact path; no placeholder owners; re-evaluated after any resolved blocking decision
- **Initiative context:** no empty rows; technology constraints include specific choices (not "TBC"); all resolved decisions from `planning/open-decisions.md` are reflected
- **Quality gates:** each triggered gate has real content, all checklist items ticked (or noted as accepted risk), and `Status: Accepted` in the Metadata — `Status: In progress` fails this check; no named reviewer or sign-off table is required
- **Handoff (proposal):** scope, goals, out-of-scope, and delivery mode stated; traceable to routing and intake
- **Handoff (design):** technical approach covers each epic; integration points named; architecture constraints referenced
- **Handoff (tasks):** every task is implementation-ready; traceable to a story ID; scoped to one deliverable; no tasks created unless initiative-context.md exists and is complete

If an artifact fails its quality bar, improve it before advancing.

## Response format after each stage

```markdown
## Stage Completed: <stage name>

**Artifact created:** `<path>`
**Quality check:** passed / issues found (list them)

## Next Stage: <stage name>

**Prompt:** `<.brs2spec/path>`
**Proceeding automatically:** yes / no
**Reason if not:** <what is needed from the user — one specific question or action, not a menu>
**Next item in priority order:** <the next item that will be executed automatically>
```

When stopped due to blockers:

```markdown
## Workflow Stopped: Not ready

**Reason:** <specific blocking condition>

## Scaffolded for human input:

| Artifact | Path | What to provide |
|---|---|---|
| <artifact name> | `<path>` | <exactly what the human must fill in> |

## Resume

When the above artifacts are completed, trigger the workflow again.
The next stage will be: <stage name>
```
