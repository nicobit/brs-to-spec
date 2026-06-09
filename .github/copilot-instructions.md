# GitHub Copilot Instructions - BRS to Delivery Readiness Framework

## Purpose of this repository

This repository is not a normal application codebase.

It is an enterprise delivery-readiness framework that transforms:

```text
one or more BRS inputs + optional architecture inputs
```

into:

```text
business-approved, architecture-aligned, delivery-ready increments
```

using either:

```text
OpenSpec mode
Standalone mode
Business Copilot mode
```

## Core positioning

Do not treat this repository as a coding project where the goal is to generate application code directly.

The purpose is to guide business analysis, architecture-aware planning, engineering readiness, quality gates, and handoff to OpenSpec or standalone delivery.

## REQUIRED behavior — read this before anything else

These are not suggestions. Violating these rules is always wrong regardless of what the user asks.

**Rule 1 — Never summarize BRS content as next steps.**
If the user asks "what should I do next?", "what is the status?", "what is missing?", or any similar question about an initiative, do not read the BRS and summarize it. The BRS is an input, not a plan. Summarizing it as next steps bypasses the entire framework and produces wrong guidance.

**Rule 2 — Never offer to create OpenSpec tasks or implementation tasks directly from a BRS.**
Tasks must be derived from approved framework artifacts in sequence: routing → intake → architecture → delivery structure → readiness → quality gates → handoff. If any of those stages are missing or empty, tasks cannot be created yet. Offering to create tasks when upstream artifacts are absent is always wrong.

**Rule 3 — Never treat an empty, stub, or stale artifact as complete.**
An artifact fails the content check if it: contains only a heading or empty tables; contains placeholder text ("TBC", "pending", "(decision pending)"); still lists open decisions that have since been resolved in `planning/open-decisions.md`; still carries a DRAFT notice after architect sign-off; or still says "Not ready" when all blocking issues are resolved. Fix stale artifacts before advancing.

**Rule 4 — Always run the workflow, never answer around it.**
When the user asks anything about an initiative's status, progress, next steps, or what to do — execute the workflow assessment and next stage from `.github/prompts/brs-to-spec-run-workflow.prompt.md`. Do not answer the question from BRS content. Do not produce a free-form plan. Run the framework.

**Rule 6 — Never advance past a stage with a failing artifact.**
Before moving to the next stage, verify the current stage artifact passes its done criteria (see workflow prompt Step 2). A thin delivery structure with one story per feature, a readiness check that still says Not ready when blockers are resolved, or quality gate stubs with no real content all fail their done criteria. Fix them first.

**Rule 7 — Run the stale artifact check before every stage assessment. This means reading and inspecting file content, not just listing file names.**

Every time the workflow is triggered, before reporting any stage as current or blocked:

Step 1 — Read `planning/open-decisions.md`. Find every row where Status = Resolved.

Step 2 — For each Resolved row, physically open and read each file listed in the Home artifact column. Do not assume an artifact is current because it exists. Read its content.

Step 3 — Check whether the file still contains the resolved decision as open, pending, TBC, or unresolved. Specific checks:
- `input/architecture.md`: Open Decisions table must not list D-001..D-005 as open. DRAFT notice must be gone if OD-006 is Resolved. If still DRAFT or still showing open decisions → stale → fix now.
- `architecture/architecture-rules.md`: Must not contain AR-OPEN-001 or AR-OPEN-002 as open items if OD-001 and OD-002 are Resolved → stale → promote to binding rules now.
- `engineering-readiness/readiness-check.md`: If all blocking issues listed in it are resolved in the register, the Not ready decision is stale → re-evaluate readiness now.
- `planning/delivery-structure.md`: Every feature must have ≥2 user stories. If any feature has only one story → incomplete → rebuild before advancing.
- `engineering-readiness/initiative-context.md`: Must exist with real content before handoff. If missing → generate it now.

Step 4 — Fix every stale or incomplete artifact found in Step 3 before doing anything else.

Step 5 — Only after all stale artifacts are fixed: proceed to stage assessment.

Never list an artifact as "completed / present" without having read its content in this session. A file name in a directory listing is not evidence of completeness.

**Rule 5 — Never produce a free-form implementation plan from BRS content.**
Responses like "here are your next steps: 1. finalize BRS, 2. implement API, 3. add tests" are framework violations. Every next step must come from a framework artifact, not from reading the BRS directly.

## Initiative workspace rule

Operate inside one initiative workspace at a time.

The standard workspace shape is:

```text
initiatives/<initiative-id>-<slug>/
```

All workflow paths are relative to the active initiative workspace.

The canonical source set for an initiative starts with:

```text
input/brs.md or input/brs/*.md
input/architecture.md or input/architecture/*.md
input/input-package.md
```

Start with `input/brs.md` and `input/architecture.md`. Expand to folders only when the same initiative genuinely has multiple source documents.

At the start of an initiative, architecture input often provides high-level solution context:

```text
systems
containers
integrations
platform boundaries
high-level constraints
```

Use that context early, but do not assume it already resolves initiative-specific delivery design.

## Entry mode rule

Before selecting delivery mode and execution mode, identify the most likely entry mode:

```text
BRS-first
existing-system enhancement
small change / bug fix
large modular initiative
```

Entry mode does not replace routing.

It helps choose the right starting pattern and likely first prompt.

Use the normal framework routing after entry mode is identified.

If the entry mode is `existing-system enhancement`, surface brownfield impact early.

When existing-system impact is material, create and use:

```text
architecture/existing-system-impact.md
```

to capture:

```text
affected components
compatibility and regression risk
contract or schema impact
existing behavior that must remain stable
rollout / rollback sensitivity
operational dependencies
```

## Workflow state file rule

`planning/workflow-state.json` is a compact machine-readable snapshot of the initiative's current stage, artifact statuses, stale artifacts, and next action. Read it first on every session to avoid scanning full artifact content unnecessarily.

**Reading the state file:**
- If `planning/workflow-state.json` exists and `state_validated` = true: use it as the starting point. Trust `stale_artifacts`, `open_decisions`, and `next_action` as a fast-path hint.
- Do not blindly trust it. Always verify the `next_action` artifact with a quick content check before executing. If the content check disagrees, trust the content check and update the state file.
- If the file does not exist or `state_validated` = false: ignore it and run the full stale check and stage assessment.

**Updating the state file:**
- After completing any stage, update `planning/workflow-state.json` using `.brs2spec/3-planning-and-modular-delivery/01-maintain-workflow-state.md`.
- Set `state_validated` = true only after physically reading every artifact's content, not just checking existence.
- Never set an artifact status to `complete` based on file existence alone.

**Status values in the state file:**
`missing` / `stub` / `stale` / `incomplete` / `complete` / `not-triggered` / `triggered-incomplete` / `triggered-complete`

If `stale_artifacts` is non-empty, fix those artifacts before doing anything else — even if the state file suggests a later stage is the current blocker.

## Open decisions register rule

`planning/open-decisions.md` is the single place to check what is open, who owns it, and what it blocks.

- Never scan individual artifacts (architecture-review, readiness-check, etc.) to answer "what decisions are still open?" — always read `planning/open-decisions.md` first.
- Every time a workflow stage creates a new open decision, update `planning/open-decisions.md` immediately.
- Every time a human provides an answer to a decision, update `planning/open-decisions.md` immediately (set Status to Resolved, add Resolution summary and date) and update the home artifact.
- Before advancing to handoff, check the Blocking decisions summary in `planning/open-decisions.md`. If any decision is Open or In progress AND Blocking = Yes, the workflow must not advance.
- When asked "what decisions are still open?", "what is blocking us?", "what do we need from the PO?" — read `planning/open-decisions.md` and answer from it. Do not re-scan artifacts.

## Source of truth hierarchy

Respect this order within the active initiative workspace:

```text
1.  input/brs.md or input/brs/*.md
2.  input/architecture.md or input/architecture/*.md
3.  input/input-package.md
4.  business-intake/business-intake-summary.md
5.  planning/delivery-structure.md
6.  architecture/architecture-review.md
7.  architecture/architecture-rules.md
8.  planning/open-decisions.md       ← single source of truth for all open decisions
9.  planning/delivery-increments.md when the initiative uses Modular Delivery
10. planning/traceability-matrix.md
11. engineering-readiness/readiness-check.md
12. quality-gates/*.md
13. openspec/changes/... or standalone-delivery/...
14. perspectives/agile-planning/gitlab-planning-view.md
15. implementation and review helper outputs
```

The Agile / GitLab Planning View is a projection only. It is not the source of truth.

Implementation summaries, review comments, and reviewer prompt outputs are downstream helper artifacts only.

User stories are business context and traceability only.

OpenSpec or standalone tasks are the engineering implementation contract.

Epic / Feature / User Story structure should be defined in `planning/delivery-structure.md` early enough to guide architecture refinement before handoff prompts derive implementation tasks.

## Artifact consumer and downstream-use rule

For every major artifact you generate or update, be able to state:

```text
primary consumer
primary purpose or decision
downstream artifact or workflow that depends on it
what should be referenced instead of duplicated
```

Apply this especially to:

```text
business-intake summary
architecture review
delivery structure
readiness check
quality-gate artifacts
delivery spec or design
tasks
GitLab Planning View
```

If an artifact feels framework-shaped but has no obvious consumer or downstream use, tighten it before moving on.

The same applies to optional visuals:

```text
add a visual only when it materially improves clarity for the primary consumer
do not create a visual just because the template allows one
do not let a missing non-critical visual block progress when the text is already clear enough
```

## Coding-agent boundary

Do not start coding from raw source inputs.

Code implementation should begin only when the active initiative workspace has:

```text
engineering-readiness/readiness-check.md
required quality gates completed or explicitly accepted as risk
openspec/changes/D1-.../tasks.md
or standalone-delivery/D1-.../tasks.md
```

If `quality-gates/ready-for-copilot-checklist.md` exists, use it as the final implementation gate.

## Where to write new human-provided information

When a user has new information from a conversation — a vendor call, a PO decision, a Legal answer, an architect choice — and asks where to put it:

The answer is always `input/input-package.md`, in the **Decisions and Clarifications Received** section.

That section is the designated landing place for all human-provided input that is not captured in a formal document. It is read by every downstream prompt as a first-class input.

Do not tell the user to edit the BRS, the architecture draft, or any other artifact directly. Do not tell the user to wait until a later stage. Direct them to `input/input-package.md` immediately.

When the workflow runs next, it will pick up the new entries automatically and incorporate them into the next stage artifact.

## Consolidation rule for multiple source files

When multiple BRS or architecture files exist:

```text
analyze all files in the relevant input folder
preserve source document names and section references
record overlap, conflicts, and assumptions in input/input-package.md
do not silently merge conflicting statements without noting the conflict
```

## Architecture input rule

Before running the architecture review, check `input/architecture.md`:

- If it is **missing, empty, or a stub** (e.g. contains only "No architecture document provided" or a blank template): run `.brs2spec/0-input-preparation/04-draft-architecture-from-brs.md` to generate a draft from the BRS. Save it to `input/architecture.md` marked as DRAFT. Then proceed to the architecture review.
- If it contains a **DRAFT notice**: proceed to architecture review but flag to the user that the draft requires architect validation before the output is treated as authoritative.
- If it contains **real architecture content** with no draft notice: proceed to architecture review normally.

Never run the architecture review against an empty or stub architecture input. Never skip architecture draft generation silently.

## Architecture constraint rule

If the architecture input defines a constraint, do not override it unless explicitly marked as:

```text
conflict
open decision
accepted deviation
```

Do not invent architecture.

Treat the initial architecture input as high-level solution context unless the evidence clearly makes initiative-specific decisions explicit.

Later architecture review and rules should refine what that context means for the initiative's slices, contracts, readiness, and handoff.

## Workflow rule

Before creating implementation tasks, verify that the workflow has passed through:

```text
input preparation
routing
business intake
delivery planning
initiative-specific architecture review and rules
engineering readiness
required Conditional Quality Gates
```

Readiness should consume approved delivery shape plus initiative-specific architecture refinement.

Do not let readiness or handoff compensate for vague planning or unresolved architecture by inventing missing delivery decisions.
Do not block readiness or handoff only because an optional visual is absent when the text evidence is already strong enough.

For small changes, Fast Path may go directly to OpenSpec or standalone handoff, but only if the change is already clear.

## Stage-transition rule

At any point, be able to state:

```text
current stage
completed artifacts
missing artifacts
next prompt
risk if skipped
```

Use this transition model:

```text
input preparation -> intake
intake -> early delivery shape
early delivery shape -> architecture refinement
architecture refinement -> readiness
readiness -> quality gates
quality gates -> handoff
handoff -> implementation
implementation -> review
```

If the current stage or next prompt is unclear, re-establish workflow status before generating more artifacts.

## Delivery modes

Use the smallest safe delivery mode:

```text
Fast Path
Standard Path
Enterprise Path
Enterprise + Modular Delivery
```

Do not automatically choose Enterprise + Modular for every request.

## Small-change rule

If the change is narrow, first ask whether a small-change path is appropriate.

A small-change path may still require:

```text
readiness
triggered quality gates
one approved handoff artifact set
one-task-at-a-time implementation
```

Do not treat Fast Path as permission to skip control points that are still required by risk.

Do not force small changes to produce diagrams by default.

## Execution modes

OpenSpec is the default downstream, but it is not mandatory.

Choose one:

```text
OpenSpec
Standalone
Business Copilot
```

Use Standalone mode when the team does not use OpenSpec.

## Conditional Quality Gates

Quality gates are not optional.

They are conditional:

```text
not always required
but mandatory when triggered
```

If `engineering-readiness/readiness-check.md` marks a gate as:

```text
Triggered = Yes
Required = Yes
```

then the corresponding gate artifact must be created before the required-before stage.

Common gates:

```text
BDD scenarios
test strategy
QA review
architecture review
security review
release readiness review
API contract
data contract
event contract
threat model
observability plan
```

## Implementation rule

When using a coding agent:

```text
implement one task at a time
read the active initiative artifacts first
inspect existing similar code before changing files
update tests with behavior changes
return assumptions, risks, and open questions
```

Do not implement future tasks in the same pass.

Handoff artifacts must derive from:

```text
approved delivery shape
initiative-specific architecture refinement and rules
readiness decisions
triggered quality gates
traceability evidence
```

If those upstream artifacts are weak, stop and strengthen them before creating implementation tasks.

If a complex boundary or interaction is still too hard to understand in text alone, say that clearer visual support is needed instead of silently proceeding.

## Review rule

After implementation, use the review prompts under:

```text
.brs2spec/9-reviewers/
```

Treat review prompts as implementation review surfaces, not as replacements for artifact-generation quality gates.

## Agile / GitLab Planning View rule

The GitLab Planning View maps delivery artifacts to:

```text
Epic
Feature / Issue
User Story
Task / Checklist
Milestone
Labels
```

but must not redefine:

```text
requirements
architecture constraints
acceptance criteria
quality gates
implementation tasks
```

Always include source artifact paths and source IDs or source file names.

Use the planning view as one team-facing Delivery Planning View that can include Agile breakdown, Engineering Notes, Enablement Needs, and GitLab mapping without creating a second workflow.

The primary consumers are the delivery team, Product Owner, and planning-tool maintainers.

The downstream use is coordination in GitLab, Jira, Azure DevOps, or a similar planning tool.

Do not duplicate requirements, architecture truth, acceptance truth, or implementation task truth into the planning view.

## User story format

When creating user story projections, use the classic format:

```text
As a <persona>,
I want <capability>,
so that <business value>.
```

But do not duplicate full acceptance criteria as the source of truth. Reference the acceptance source instead:

```text
BDD scenarios
delivery spec
OpenSpec tasks
standalone validation plan
traceability matrix
```

Do not implement from user stories alone.

Use linked user stories for business context and validation traceability.

Use one approved OpenSpec or standalone task as the implementation unit.

## Output quality

All outputs must be:

```text
evidence-based
traceable
decision-oriented
risk-aware
actionable
reviewable
```

Before proceeding to the next workflow step, also evaluate:

```text
Is the artifact good enough for its intended consumer?
Does it support the next decision or handoff clearly?
Is the evidence concrete enough?
Is it still too generic, repetitive, or vague?
```

If the artifact is formally complete but operationally weak, improve it before moving on.

Avoid generic statements like:

```text
Looks good.
Add tests.
Security should be considered.
Architecture is aligned.
```

Prefer:

```text
Control area | Status | Evidence | Gap / Risk | Required action | Owner | Required before
```

## Do not

Do not:

- generate application code directly from raw BRS sources
- create tasks for the whole initiative at once
- ignore the architecture input
- call triggered quality gates optional
- duplicate source-of-truth content in the planning view
- invent GitLab issue IDs
- invent missing requirements, architecture decisions, or acceptance criteria
- mix outputs from different initiative workspaces
- treat standalone mode as lower quality than OpenSpec mode

## Intent recognition rule

Any message that matches the intent below must trigger the full workflow execution behavior described in `.github/prompts/brs-to-spec-run-workflow.prompt.md` — not just a status report.

Do not wait for the user to name a specific prompt. Recognize the intent and act.

Trigger phrases and their intent:

| User says (examples) | Intent | First artifact to read |
|---|---|---|
| "what is the next step?" | read open-decisions register, then assess workspace | `planning/open-decisions.md` |
| "what is the status of this initiative?" | read open-decisions register, then assess workspace | `planning/open-decisions.md` |
| "what should I do next?" | read open-decisions register, then assess workspace | `planning/open-decisions.md` |
| "what is blocking us?" | read open-decisions register and report blocking summary | `planning/open-decisions.md` |
| "what decisions are still open?" | read open-decisions register and report all Open rows | `planning/open-decisions.md` |
| "what do we need from the PO?" | read open-decisions register, filter by Product owner | `planning/open-decisions.md` |
| "what do we need from the architect?" | read open-decisions register, filter by Architect owner | `planning/open-decisions.md` |
| "continue the workflow" | execute next incomplete stage | stage assessment |
| "what's next for I001?" | read open-decisions register, then assess named workspace | `planning/open-decisions.md` |
| "run the framework" | execute workflow from current stage | stage assessment |
| "pick up where we left off" | find first incomplete stage and execute it | stage assessment |
| "check the initiative" | read open-decisions register, then assess workspace | `planning/open-decisions.md` |
| "what is missing?" | read open-decisions register, then assess workspace | `planning/open-decisions.md` |
| "accept all quality gates" | change Status to Accepted in all triggered gate artifacts, update workflow-state.json, advance workflow | all `quality-gates/*.md` with Status ≠ Accepted |
| "accept all gates and continue" | same as above | all `quality-gates/*.md` with Status ≠ Accepted |
| "accept all and continue" | same as above | all `quality-gates/*.md` with Status ≠ Accepted |

When any of these intents is detected:

1. Identify the active initiative workspace from context or by asking once if ambiguous.
2. **Read `planning/open-decisions.md` first** — if it exists and has blocking open decisions, report the blocking summary before doing anything else.
3. If all blocking decisions are resolved (or no register exists yet): apply the content check — an artifact that exists but is empty or stub-only is treated as missing.
4. Find the first incomplete stage in the workflow sequence.
5. Execute that stage fully — generate the artifact, do not produce a skeleton.
6. Re-assess and continue to the next stage automatically.
7. Stop only when a genuine stop condition is reached (missing input, Not ready decision, human-required gate, ambiguous scope).

**Never answer a "next step" or "status" question by reading raw artifacts (BRS, architecture-review, readiness-check) first. Always go to `planning/open-decisions.md` first.**

## Required behavior in Copilot Chat

When asked anything about an initiative — status, next steps, what to do, what is missing, continue, check, review — follow this sequence without deviation:

1. Identify the active initiative workspace from context. Ask once if ambiguous.
2. **Read `planning/open-decisions.md`.** If it has blocking open decisions (Status = Open or In progress, Blocking = Yes), report the blocking summary table and stop. Do not proceed to stage execution while blocking decisions are open.
3. **Run the stale artifact check.** For every Resolved decision in the register, open the home artifacts listed in that row and verify they no longer show the decision as open, pending, or TBC. If any home artifact is stale, fix it now — before assessing which stage is next. Do not skip this step because the workflow appears to be at a late stage.
4. After fixing stale artifacts: check every stage artifact against its done criteria — not just existence. Empty, stub-only, or stale = incomplete.
5. Find the first stage that is incomplete.
6. Execute that stage fully. Generate a complete artifact, not a skeleton.
7. After completing the stage, re-assess and execute the next stage.
8. Continue automatically until a genuine stop condition is reached.
9. Stop conditions: blocking decisions unresolved, stale artifacts cannot be fixed without human input, readiness is Not ready and blockers are genuinely unresolved, a gate requires human sign-off, scope is ambiguous and cannot be resolved from existing artifacts.
8. When stopping, state exactly what is missing and what the user must provide before the workflow can continue.

## Forbidden responses

Never produce any of the following in response to any question:

- A bulleted list of next steps derived from reading the BRS
- "Here is what I recommend you do next: ..."
- "Shall I convert the FRs into tasks?"
- "You should now implement X, Y, Z"
- A free-form plan that bypasses the framework stages
- Any OpenSpec or standalone-delivery artifact when routing, intake, or readiness are missing or empty
- A numbered menu of options at the end of a response ("If you want, I can: 1... 2... 3... Which should I do next?")
- "Which should I do next?"
- "What would you like me to do?"
- "Shall I proceed with X or Y?"
- Any offer of a choice between actions you could determine yourself from context
- "I can [do X] — tell me if you want me to do that now"
- Answering "what is the next step?" by reading raw artifacts (BRS, architecture-review, readiness-check) without first reading `planning/open-decisions.md`
- Reporting only one blocking decision when the open-decisions register has multiple blocking decisions open
- Creating handoff artifacts (proposal, design, tasks) while `engineering-readiness/initiative-context.md` is missing
- Creating handoff artifacts while any upstream artifact is stale (resolved decisions not reflected, DRAFT notice not cleared, Not ready not re-evaluated)
- Accepting a delivery structure where any feature has only one user story
- Creating folders not in the allowed workspace structure (e.g. `engineering-readiness/runbooks/`, `engineering-readiness/observability/`)
- Presenting sub-tasks within a quality gate as a menu of options ("which of these should I do next?")
- Stopping after completing a quality gate to ask about implementation details instead of moving to the next gate
- Marking a quality gate as complete in `planning/workflow-state.json` unless `Status: Accepted` appears in the gate artifact Metadata
- Telling the user to obtain named sign-offs or fill in a sign-off table — the acceptance model requires only changing Status to Accepted
- Adding a `## Sign-off` section with a table of `| Name | Role | Date | Status | Comment |` columns to any gate artifact — this pattern is explicitly forbidden; the only acceptance mechanism is `Status: Accepted` in Metadata
- Appending any sign-off table, signature block, or "Copilot cannot perform the acceptance on your behalf" message to a gate artifact — these must be removed if present
- Adding `automation`, `auto_mark_gates_on_evidence`, or any self-invented field to `planning/workflow-state.json`
- Auto-advancing a gate to complete based on evidence file presence alone — Status must be Accepted in the artifact

**When "accept all quality gates" (or "accept all gates and continue" / "accept all and continue") is detected:**

1. Read each triggered gate artifact in `quality-gates/` that does not already have `Status: Accepted` in its Metadata.
2. In each artifact: change the `Status` field in the Metadata table to `Accepted`. Remove any `## Sign-off` section if present. Do not add any other section.
3. Update `planning/workflow-state.json`: set every triggered gate's status to `triggered-complete`.
4. Set `next_action` to `handoff`.
5. Report: which gates were accepted, what the next stage is. Do not offer a menu.

If you catch yourself about to produce any of the above, stop.

When you have completed what was asked — answer the question, execute the stage, scaffold the artifacts — stop. Do not append a menu. Do not solicit a follow-up choice. If the next action is obvious from the workflow state, do it. If it genuinely requires human input, state exactly what is needed in one sentence and stop.

## Execution priority order

When multiple incomplete items exist, always work through them in this fixed order. Never ask which one to do first.

```
1. Fix stale artifacts          — input/architecture.md, architecture-rules.md, readiness-check.md
2. Fix incomplete artifacts     — planning/delivery-structure.md (≥2 stories per feature)
3. Generate missing artifacts   — engineering-readiness/initiative-context.md (if missing)
4. Complete quality gates       — in this order: security-review → data-contract → api-contract → observability-plan
5. Handoff                      — proposal → design → tasks (only when all above are done)
```

Within each group, pick the first item in the list and complete it fully before moving to the next. Do not jump to a later group because an earlier item requires human input — scaffold the blocker, state what is needed, then move to the next item in the same group.

**Completing a quality gate means:** the `Status` field in the gate artifact's Metadata section has been changed to `Accepted` (not `In progress`), and all checklist items are ticked or explicitly recorded as accepted risk. The git commit records who accepted and when — no separate sign-off line is required.

Copilot cannot mark a gate as complete. Copilot cannot auto-promote a gate based on evidence files being present. Copilot cannot set `status: "complete"` in `planning/workflow-state.json` for any quality gate unless the Metadata Status field in the artifact reads `Accepted`.

If checklist items are done but Status is still `In progress`: prompt the user to change Status to `Accepted` in the artifact, then update the workflow state. Do not change it yourself without the user's explicit instruction.

**Stopping correctly when multiple items remain:**

After completing a stage, re-assess. If the next item in the priority order can be done with available information — do it immediately. If it cannot (requires human sign-off, missing vendor data, legal approval) — scaffold what can be scaffolded, state in one sentence what the human must provide, then move to the next item in the priority order that *can* be done.

Never stop because one item needs human input when other items in the same or earlier group can be completed now. Never present those remaining items as a menu — just execute the next one.

## Initiative workspace structure rule

The framework defines a fixed folder structure for each initiative workspace. Do not create new top-level folders or subfolders that are not part of the framework structure.

Allowed paths within an initiative workspace:

```
input/
input/brs.md or input/brs/
input/architecture.md or input/architecture/
input/input-package.md
input/contracts/
routing/
business-intake/
architecture/
planning/
engineering-readiness/
quality-gates/
openspec/changes/<deliverable>/
standalone-delivery/<deliverable>/
perspectives/
```

Do not create:
- `engineering-readiness/runbooks/` — runbooks belong inside `quality-gates/observability-plan.md` as inline content or linked evidence, not a separate folder
- `engineering-readiness/observability/` — observability artifacts belong in `quality-gates/observability-plan.md`
- Any folder not listed above

If supporting evidence (templates, runbooks, alert rules) is needed for a quality gate, embed it inside the gate artifact or reference it as an attachment note. Do not create new subfolders to house it.

