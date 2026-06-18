# Enterprise BRS to Delivery Readiness Framework

**From enterprise BRS to AI-safe engineering handoff.**

> Personas do not own the process. Artifacts own the process. Personas execute registered skills against artifacts.

`brs-to-spec` is the missing upstream layer before OpenSpec, GitHub Copilot, Codex, or any AI-assisted delivery tool. It transforms one or more raw **Business Requirements Specification (BRS)** documents, plus optional architecture source material, into business-approved, architecture-aligned, delivery-ready increments — structured so that an AI coding agent can implement safely, one story at a time.

## What problem does this solve?

Enterprise delivery fails when AI coding agents are pointed at raw BRS documents. A real initiative carries ambiguity, implicit assumptions, architecture constraints, regulatory expectations, and cross-team dependencies that no coding agent can resolve from a Word file. This framework creates the controlled path between business intent and safe engineering execution.

OpenSpec is the default engineering downstream, but it is not mandatory. The framework also supports standalone execution, Microsoft 365 Copilot / Copilot Studio business intake, and GitHub Copilot / VS Code guided delivery workflows.

## Start here

**New to the framework?** Read [`docs/00-5-minute-quickstart.md`](docs/00-5-minute-quickstart.md) first (under 5 minutes).

**Not sure which prompt to run?** See [`docs/01-what-do-i-run.md`](docs/01-what-do-i-run.md) for the full lookup table.

Run the workflow runner at the start of every session:

```text
.brs2spec/brs-to-spec-run-workflow.md
```

It detects where you are, executes the next stage, and continues automatically until a genuine human decision is required. No menus, no permission requests.

## How it works

```text
BRS + Architecture → Routing → Business Intake → Architecture Review → Delivery Structure → Engineering Readiness → Quality Gates (if triggered) → Handoff
```

Each stage produces a traceable artifact. The workflow runner loads `.brs2spec/module-index.md`, reads `state/workflow-state.json`, checks content (not just file existence), selects the correct persona skill, and re-assesses automatically.

## Example output

See `initiatives/I001-customer-onboarding/` for a complete worked example. Key files:

- `state/workflow-state.json` — machine-readable stage tracker
- `planning/delivery-structure.md` — epics, features, user stories with traceability
- `openspec/changes/dependency-graph.md` — wave-ordered story execution plan
- `openspec/changes/F-001.1-onboarding-submission/` — one self-contained story folder

## Persona skill registry

The framework is organized around personas and skills. The orchestrator selects the next skill based on workflow state, missing or stale artifacts, risk triggers, and delivery mode.

See [`.brs2spec/module-index.md`](.brs2spec/module-index.md) for the skill index and routing tables. See [`.brs2spec/module-full.md`](.brs2spec/module-full.md) for full persona definitions and per-skill detail. See [`docs/01-what-do-i-run.md`](docs/01-what-do-i-run.md) for the quick-lookup table.

---

**Full workflow guide:** [`HOW_TO_USE.md`](HOW_TO_USE.md)
**5-minute quickstart:** [`docs/00-5-minute-quickstart.md`](docs/00-5-minute-quickstart.md)
**What do I run?** [`docs/01-what-do-i-run.md`](docs/01-what-do-i-run.md)
**Entry modes:** [`docs/18-entry-modes.md`](docs/18-entry-modes.md)
**Delivery and execution modes:** [`docs/02-delivery-and-execution-modes.md`](docs/02-delivery-and-execution-modes.md)
**Small-change paths:** [`docs/20-small-change-paths.md`](docs/20-small-change-paths.md)
**Skill index (quick routing):** [`.brs2spec/module-index.md`](.brs2spec/module-index.md)
**Skill registry (full detail):** [`.brs2spec/module-full.md`](.brs2spec/module-full.md)
