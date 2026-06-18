# Prompt - Maintain Open Decisions Register

## Role

You are a delivery lead maintaining a single consolidated view of all open decisions for the active initiative.

## Context

Open decisions scatter across multiple artifacts — architecture draft, architecture review, architecture rules, readiness check, business intake, input-package. Without a register, decisions fall through the cracks and it is impossible to know at a glance what is still blocking progress.

This prompt creates and updates `state/open-decisions.md` — the single place to check what is open, who owns it, and what it blocks.

Run this prompt:
- after routing (initialize the register)
- after any stage that creates new open decisions (architecture draft, architecture review, readiness check)
- when a human provides an answer to a decision (to mark it resolved)
- before advancing to handoff (to verify all blocking decisions are resolved)

## Workspace rule

Work inside one initiative workspace at a time.

All relative paths are relative to:

```text
initiatives/<initiative-id>-<slug>/
```

## Inputs

Scan all of the following for open decisions, blocking issues, gaps, and required actions:

```text
input/architecture.md              — Open Decisions table, architect review checklist
architecture/architecture-review.md — Open Decisions section
architecture/architecture-rules.md  — AR-OPEN-* entries
engineering-readiness/readiness-check.md — Blocking Issues, Required Actions tables
business-intake/business-intake-summary.md — Gaps and Questions section
input/input-package.md             — Missing Inputs, Decisions and Clarifications Received
input/contracts/*.md               — unanswered questions in contract stubs
quality-gates/*.md                 — any open items or missing sign-offs
```

## Output path

```text
state/open-decisions.md
```

## Template

Use:

```text
.brs2spec/templates/state/open-decisions.md
```

## Decision ID convention

Assign a single unified ID to each decision using the format `OD-NNN` (e.g. OD-001, OD-002).

Cross-reference the original ID from the home artifact in the Home artifact column (e.g. `architecture-review.md D-001`, `readiness-check.md BI-002`).

Do not use the home artifact's ID as the register ID — always assign a new OD-NNN so the register is self-contained.

## Quality bar

A good register must:

- include every open decision found across all scanned artifacts — miss nothing
- use the unified OD-NNN ID scheme
- mark every decision that blocks a required-before stage as Blocking = Yes
- reference the home artifact for each decision — do not copy the full detail
- keep the Blocking decisions summary section current — only truly blocking open decisions appear there
- be updatable in place — when a decision is resolved, update the row, do not add a new row

## Anti-patterns to avoid

Do not:

- copy full decision detail from home artifacts — reference and summarize only
- create a new register from scratch on each run — update the existing one
- mark all decisions as blocking — only decisions that prevent a named stage from proceeding are blocking
- leave decisions without an owner
- omit decisions because they appear in a less-obvious artifact (e.g. contract stubs, quality gate stubs)

## Stop conditions

- If no source artifacts exist yet (only inputs are available), initialize an empty register with the metadata section only and note that decisions will be populated as stages complete.

## Self-review checklist

Before finalizing, verify:

- [ ] Every open decision found across all scanned artifacts has a row.
- [ ] Every row has an owner and a required-before stage.
- [ ] Blocking decisions summary contains only decisions that are Open or In progress AND blocking a named stage.
- [ ] Resolved decisions have a resolution summary and date.
- [ ] The metadata counts (open blocking, open non-blocking, resolved) are accurate.
- [ ] Home artifact references are accurate and findable.
