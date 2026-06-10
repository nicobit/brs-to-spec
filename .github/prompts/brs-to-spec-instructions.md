# BRS to Spec Framework — Behavioral Instructions

> **Usage**: Reference this file from any agent system to activate the full framework behavioral rules.
>
> - **GitHub Copilot** (`copilot-instructions.md`): `#file:.github/prompts/brs-to-spec-instructions.md`
> - **Claude Code** (`CLAUDE.md` or `agents.md`): `<include path=".github/prompts/brs-to-spec-instructions.md" />`
> - **Cursor** (`.cursorrules`): `@.github/prompts/brs-to-spec-instructions.md`
> - **Codex** (`AGENTS.md`): Add the contents inline or reference with `# File: .github/prompts/brs-to-spec-instructions.md`

---

## Purpose of this framework

This is an enterprise delivery-readiness framework that transforms:

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

Do not treat any repository using this framework as a coding project where the goal is to generate application code directly.

The purpose is to guide business analysis, architecture-aware planning, engineering readiness, quality gates, and handoff to OpenSpec or standalone delivery.

---

## REQUIRED behavior — read this before anything else

These are not suggestions. Violating these rules is always wrong regardless of what the user asks.

**Rule 1 — Never summarize BRS content as next steps.**
If the user asks "what should I do next?", "what is the status?", "what is missing?", or any similar question about an initiative, do not read the BRS and summarize it. The BRS is an input, not a plan. Summarizing it as next steps bypasses the entire framework and produces wrong guidance.

**Rule 2 — Never offer to create OpenSpec tasks or implementation tasks directly from a BRS.**
Tasks must be derived from approved framework artifacts in sequence: routing → intake → architecture → delivery structure → readiness → quality gates → handoff. If any of those stages are missing or empty, tasks cannot be created yet.

**Rule 3 — Never treat an empty, stub, or stale artifact as complete.**
An artifact fails the content check if it: contains only a heading or empty tables; contains placeholder text ("TBC", "pending", "(decision pending)"); still lists open decisions that have since been resolved in `planning/open-decisions.md`; still carries a DRAFT notice after architect sign-off; or still says "Not ready" when all blocking issues are resolved.

**Rule 4 — Always run the workflow, never answer around it.**
When the user asks anything about an initiative's status, progress, next steps, or what to do — execute the workflow assessment and next stage from `.github/prompts/brs-to-spec-run-workflow.prompt.md`. Do not answer the question from BRS content. Do not produce a free-form plan.

**Rule 5 — Never produce a free-form implementation plan from BRS content.**
Responses like "here are your next steps: 1. finalize BRS, 2. implement API, 3. add tests" are framework violations. Every next step must come from a framework artifact, not from reading the BRS directly.

**Rule 6 — Never advance past a stage with a failing artifact.**
Before moving to the next stage, verify the current stage artifact passes its done criteria. A thin delivery structure, a readiness check that still says Not ready when blockers are resolved, or quality gate stubs with no real content all fail their done criteria.

**Rule 7 — Run the stale artifact check before every stage assessment.**
This means reading and inspecting file content, not just listing file names.

Every time the workflow is triggered, before reporting any stage as current or blocked:

Step 1 — Read `planning/open-decisions.md`. Find every row where Status = Resolved.

Step 2 — For each Resolved row, physically open and read each file listed in the Home artifact column.

Step 3 — Check whether the file still contains the resolved decision as open, pending, TBC, or unresolved. Specific checks:
- `input/architecture.md`: Open Decisions table must not list resolved decisions as open. DRAFT notice must be gone if the relevant decision is Resolved.
- `architecture/architecture-rules.md`: Must not contain open items if corresponding decisions are Resolved.
- `engineering-readiness/readiness-check.md`: If all blocking issues listed in it are resolved, the Not ready decision is stale — re-evaluate readiness now.
- `planning/delivery-structure.md`: Every feature must have at least one well-formed user story.
- `engineering-readiness/initiative-context.md`: Must exist with real content before handoff.

Step 4 — Fix every stale or incomplete artifact found in Step 3 before doing anything else.

Step 5 — Only after all stale artifacts are fixed: proceed to stage assessment.

---

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

## Entry mode rule

Before selecting delivery mode and execution mode, identify the most likely entry mode:

```text
BRS-first
existing-system enhancement
small change / bug fix
large modular initiative
```

If the entry mode is `existing-system enhancement`, surface brownfield impact early by creating and using `architecture/existing-system-impact.md`.

## Workflow state file rule

`planning/workflow-state.json` is a compact machine-readable snapshot of the initiative's current stage, artifact statuses, stale artifacts, and next action.

- If it exists and `state_validated` = true: use it as the starting point but verify the `next_action` artifact with a quick content check before executing.
- If it does not exist: auto-initialise it before doing anything else.
- If `state_validated` = false: ignore it as a fast path and run the full stale check.
- After completing any stage, update it using `.brs2spec/3-planning-and-modular-delivery/01-maintain-workflow-state.md`.
- Never set an artifact status to `complete` based on file existence alone.

## Open decisions register rule

`planning/open-decisions.md` is the single place to check what is open, who owns it, and what it blocks.

- Never scan individual artifacts to answer "what decisions are still open?" — always read `planning/open-decisions.md` first.
- Every time a workflow stage creates a new open decision, update `planning/open-decisions.md` immediately.
- Before advancing to handoff, check the Blocking decisions summary. If any decision is Open or In progress AND Blocking = Yes, the workflow must not advance.

## Source of truth hierarchy

```text
1.  input/brs.md or input/brs/*.md
2.  input/architecture.md or input/architecture/*.md
3.  input/input-package.md
4.  business-intake/business-intake-summary.md
5.  planning/delivery-structure.md (draft — epics and features)
6.  architecture/architecture-review.md
7.  architecture/architecture-rules.md
8.  planning/open-decisions.md       ← single source of truth for all open decisions
9.  planning/delivery-structure.md (confirmed — full stories, arch constraints reflected)
10. planning/delivery-increments.md when the initiative uses Modular Delivery
11. planning/traceability-matrix.md
12. engineering-readiness/readiness-check.md
13. quality-gates/*.md
14. input/repositories/*.md (optional — consumed at handoff stage only)
15. openspec/changes/... or standalone-delivery/...
16. perspectives/agile-planning/gitlab-planning-view.md
17. implementation and review helper outputs
```

## Coding-agent boundary

Code implementation should begin only when the active initiative workspace has:

```text
engineering-readiness/readiness-check.md
required quality gates completed or explicitly accepted as risk
openspec/changes/D1-.../tasks.md or standalone-delivery/D1-.../tasks.md
```

## Where to write new human-provided information

When a user has new information (vendor call, PO decision, Legal answer, architect choice), the answer is always `input/input-package.md`, in the **Decisions and Clarifications Received** section.

Do not tell the user to edit the BRS, the architecture draft, or any other artifact directly.

## Architecture input rule

Before running the architecture review, check `input/architecture.md`:

- If **missing, empty, or a stub**: run `.brs2spec/0-input-preparation/04-draft-architecture-from-brs.md` to generate a draft. Save to `input/architecture.md` marked as DRAFT.
- If it contains a **DRAFT notice**: proceed to architecture review but flag that the draft requires architect validation.
- If it contains **real architecture content** with no draft notice: proceed to architecture review normally.

## Workflow rule

Before creating implementation tasks, verify that the workflow has passed through:

```text
input preparation → routing → business intake → delivery planning
→ initiative-specific architecture review and rules → engineering readiness
→ required Conditional Quality Gates
```

## Stage-transition rule

```text
input preparation → intake
intake → early delivery shape
early delivery shape → architecture refinement
architecture refinement → readiness
readiness → quality gates
quality gates → handoff
handoff → implementation
implementation → review
```

## Delivery modes

Use the smallest safe delivery mode:

```text
Fast Path
Standard Path
Enterprise Path
Enterprise + Modular Delivery
```

## Execution modes

Choose one:

```text
OpenSpec
Standalone
Business Copilot
```

## Conditional Quality Gates

Quality gates are conditional — not always required, but mandatory when triggered.

If `engineering-readiness/readiness-check.md` marks a gate as Triggered = Yes / Required = Yes, the corresponding gate artifact must be created before the required-before stage.

Common gates:

```text
BDD scenarios, test strategy, QA review, architecture review, security review,
release readiness review, API contract, data contract, event contract,
threat model, observability plan
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

## Stage sequence — strict gate chain

```
1.  routing/routing-decision.md
2.  business-intake/business-intake-summary.md      ← requires (1)
3.  input/architecture.md                           ← draft if missing
4.  planning/delivery-structure.md  (DRAFT)         ← requires (2)
5.  architecture/architecture-review.md             ← requires (2)(4 draft)
6.  architecture/architecture-rules.md              ← requires (5)
7.  planning/open-decisions.md                      ← requires (5)(6)
8.  engineering-readiness/readiness-check.md        ← requires (5)(6)(7)
9.  planning/delivery-structure.md  (CONFIRMED)     ← requires (8) decision = Ready
10. planning/open-decisions.md update               ← requires (8)
11. engineering-readiness/initiative-context.md     ← requires (9)
12. quality-gates/<triggered gates>                 ← requires (11); Status: Accepted
13. openspec/changes/ handoff                       ← requires (12); 0 blocking decisions
```

**Hard gates — never cross without prior artifact:**
- Do not execute business intake (2) without routing decision (1)
- Do not execute architecture review (5) without business intake (2) and draft delivery-structure (4)
- Do not execute engineering readiness (8) without architecture review (5), architecture rules (6), and open decisions (7)
- Do not execute delivery structure confirmed (9) without readiness decision = Ready in (8)
- Do not execute handoff (13) without all triggered gates Accepted and 0 blocking open decisions

## Execution priority order

```
1. Fix stale artifacts
2. Fix incomplete artifacts
3. Generate missing artifacts
4. Complete quality gates       — security-review → data-contract → api-contract → observability-plan
5. Handoff                      — dependency-graph.md first, then one folder per user story
```

## Prompt file execution rule

When a stage lists a `prompt:` path, open and read that file before generating the artifact. Do not generate from memory.

**The handoff format is not negotiable:**
- `openspec/changes/dependency-graph.md` generated first
- One folder per user story named `F-XXX.X-<slug>/`
- If `input/repositories/` has descriptor files: each story folder has one subfolder per repo touched; `proposal.md`, `design.md`, `tasks.md`, and `specs/` live inside each repo subfolder
- If `input/repositories/` is empty or missing: flat structure — those files live directly inside the story folder

## Intent recognition rule

Any of the following intents must trigger the full workflow execution from `.github/prompts/brs-to-spec-run-workflow.prompt.md`:

| User says (examples) | First artifact to read |
|---|---|
| "what is the next step?" | `planning/open-decisions.md` |
| "what is the status of this initiative?" | `planning/open-decisions.md` |
| "what is blocking us?" | `planning/open-decisions.md` |
| "what decisions are still open?" | `planning/open-decisions.md` |
| "continue the workflow" | stage assessment |
| "run the framework" | stage assessment |
| "pick up where we left off" | stage assessment |
| "create a BRS" / "write a BRS" | `.brs2spec/templates/input/brs.md` |
| "accept all quality gates" | all `quality-gates/*.md` with Status ≠ Accepted |
| "create the handoff" / "create openspec handoff" | `planning/delivery-structure.md` |

When detected: identify active workspace → read `planning/open-decisions.md` → fix stale artifacts → find first incomplete stage → execute it fully → re-assess → continue until a genuine stop condition.

## Required behavior in chat

When asked anything about an initiative — status, next steps, what to do, what is missing, continue, check, review — follow this sequence without deviation:

1. Identify the active initiative workspace. Ask once if ambiguous.
2. Read `planning/open-decisions.md`. If it has blocking open decisions, report the blocking summary and stop.
3. Run the stale artifact check. Fix stale artifacts before assessing which stage is next.
4. Check every stage artifact against its done criteria — not just existence.
5. Find the first stage that is incomplete.
6. Execute that stage fully. Generate a complete artifact, not a skeleton.
7. After completing the stage, re-assess and execute the next stage.
8. Continue automatically until a genuine stop condition is reached.
9. Stop conditions: blocking decisions unresolved, stale artifacts cannot be fixed without human input, readiness is Not ready and blockers are genuinely unresolved, a gate requires human sign-off, scope is ambiguous.
10. Terminal stage: if `workflow-state.json` has `current_stage: "complete"`, the workflow is finished. State: "The brs-to-spec workflow for this initiative is complete. The handoff is at `openspec/changes/<deliverable>/`."
11. When stopping, state exactly what is missing and what the user must provide.

## Forbidden responses

Never produce any of the following:

- A bulleted list of next steps derived from reading the BRS
- "Here is what I recommend you do next: ..."
- "Shall I convert the FRs into tasks?"
- A free-form plan that bypasses the framework stages
- Any OpenSpec or standalone-delivery artifact when routing, intake, or readiness are missing or empty
- A numbered menu of options at the end of a response
- "Which should I do next?" / "What would you like me to do?" / "Shall I proceed with X or Y?"
- Any offer of a choice between actions you could determine yourself from context
- "Would you like me to scaffold X now?" / "Should I generate X?" / "Shall I create X now?"
- Answering "what is the next step?" by reading raw artifacts without first reading `planning/open-decisions.md`
- Generating the confirmed `planning/delivery-structure.md` before `engineering-readiness/readiness-check.md` exists with decision = Ready
- Generating `architecture/architecture-review.md` before `business-intake/business-intake-summary.md` and a draft `planning/delivery-structure.md` both exist
- Generating `engineering-readiness/readiness-check.md` before `architecture/architecture-review.md` and `architecture/architecture-rules.md` both exist
- Generating any artifact simultaneously with the artifact that gates it
- Creating handoff artifacts while any upstream artifact is stale
- A `## Sign-off` section with a name/role/date/status table — the only acceptance mechanism is `Status: Accepted` in Metadata
- Adding `automation` or `auto_mark_gates_on_evidence` fields to `planning/workflow-state.json`
- Auto-advancing a gate to complete based on evidence file presence alone

**When "accept all quality gates" is detected:**
1. Read each triggered gate artifact in `quality-gates/` that does not already have `Status: Accepted`.
2. In each artifact: change the `Status` field in Metadata to `Accepted`. Remove any `## Sign-off` section.
3. Update `planning/workflow-state.json`: set every triggered gate's status to `triggered-complete`.
4. Set `next_action` to `handoff`.
5. Report which gates were accepted and what the next stage is.

## Output quality

All outputs must be evidence-based, traceable, decision-oriented, risk-aware, actionable, and reviewable.

Before proceeding to the next workflow step, evaluate:
- Is the artifact good enough for its intended consumer?
- Does it support the next decision or handoff clearly?
- Is the evidence concrete enough?

Avoid generic statements like "Looks good", "Add tests", "Security should be considered", "Architecture is aligned."

Prefer structured evidence:

```text
Control area | Status | Evidence | Gap / Risk | Required action | Owner | Required before
```

## Do not

- Generate application code directly from raw BRS sources
- Create tasks for the whole initiative at once
- Ignore the architecture input
- Call triggered quality gates optional
- Duplicate source-of-truth content in the planning view
- Invent missing requirements, architecture decisions, or acceptance criteria
- Mix outputs from different initiative workspaces
- Treat standalone mode as lower quality than OpenSpec mode

## Initiative workspace structure rule

Allowed paths within an initiative workspace:

```
input/
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
- `engineering-readiness/runbooks/` — embed inside `quality-gates/observability-plan.md`
- `engineering-readiness/observability/` — belongs in `quality-gates/observability-plan.md`
- Any folder not listed above
