---
applyTo: "initiatives/**,examples/**/initiatives/**"
---

# BRS to Spec Framework

This is an enterprise delivery-readiness framework. It transforms BRS inputs into business-approved, architecture-aligned, delivery-ready increments via a staged workflow. Do not treat it as a coding project.

## Hard rules — never violate regardless of what the user asks

**Rule 1 — Never summarize BRS content as next steps.**
The BRS is an input, not a plan. When asked "what should I do next?" or "what is the status?", do not read the BRS and summarize it. Run the workflow.

**Rule 2 — Never create tasks directly from a BRS.**
Tasks require: routing → intake → architecture → delivery structure → readiness → quality gates → handoff. If any stage artifact is missing, tasks cannot be created yet.

**Rule 3 — Never treat an empty, stub, or stale artifact as complete.**
Fails if: heading-only or empty tables; placeholder text ("TBC", "pending"); open decisions already resolved in `planning/open-decisions.md`; DRAFT notice after architect sign-off; "Not ready" when all blockers are resolved.

**Rule 4 — Always run the workflow, never answer around it.**
Any question about status, next steps, progress, or what to do → open and execute `.brs2spec/brs-to-spec-run-workflow.md`. Do not answer from BRS content.

**Rule 5 — Never produce a free-form plan from BRS content.**
Every next step must come from a framework artifact, not from reading the BRS.

**Rule 6 — Never advance past a stage with a failing artifact.**
Verify done criteria before advancing. Stub artifacts fail.

**Rule 7 — Run the stale artifact check before every stage assessment.**
Read content, not just filenames. Before any stage assessment: read `planning/open-decisions.md`, find Resolved rows, open every home artifact listed, verify it no longer shows that decision as open. Fix stale artifacts before proceeding.

## Workspace

One initiative at a time. Standard shape: `initiatives/<id>-<slug>/`. All paths relative to the active workspace.

New human-provided information (PO decision, vendor answer, legal input) → `input/input-package.md`, section "Decisions and Clarifications Received". Never tell the user to edit the BRS or architecture directly.

## Coding boundary

Do not start implementation until the workspace has: `engineering-readiness/readiness-check.md`, required quality gates accepted, and `openspec/changes/.../tasks.md` or `standalone-delivery/.../tasks.md`.

## Intent triggers and persona routing

Named personas bypass the orchestrator and load only their own prompt. Orchestrator triggers run the full workflow.

| User says | Action |
|---|---|
| "what is the next step?" / "what should I do?" / "what is the status?" | Read `planning/open-decisions.md` first, then run `.brs2spec/brs-to-spec-run-workflow.md` |
| "what is blocking us?" / "what decisions are open?" | Read `planning/open-decisions.md` and report |
| "continue" / "run the framework" / "pick up where we left off" / `@orchestrator` | Run `.brs2spec/brs-to-spec-run-workflow.md` from current stage |
| "create a BRS" / "write a BRS" | Run `.brs2spec/0-intake/00-create-brs.md` |
| "accept all quality gates" / "accept all and continue" | Set `Status: Accepted` in each triggered gate, update workflow-state.json, advance |
| "create the handoff" / "generate the handoff" / `@engineering-lead` | Run `.brs2spec/5-handoff/01-create-openspec-change-for-active-deliverable.md` |
| `@architect` / "review the architecture" / "create architecture rules" | Run `.brs2spec/3-planning-and-modular-delivery/01-review-initial-architecture.md` |
| `@delivery-lead` / "define the delivery structure" / "create user stories" | Run `.brs2spec/3-planning-and-modular-delivery/03-create-delivery-structure.md` |
| `@qa` / "create BDD scenarios" / "write acceptance tests" | Run `.brs2spec/4-engineering-readiness/quality-gates/create-bdd-scenarios.md` |
| `@reviewer` / "review the code" / "do a security review" | Run the relevant prompt from `.brs2spec/9-reviewers/` |

## Workspace structure — allowed paths only

```
input/          routing/         business-intake/    architecture/
planning/       engineering-readiness/               quality-gates/
openspec/changes/<deliverable>/                      standalone-delivery/<deliverable>/
perspectives/
```

Never create `engineering-readiness/runbooks/`, `engineering-readiness/observability/`, or any folder not listed above.
