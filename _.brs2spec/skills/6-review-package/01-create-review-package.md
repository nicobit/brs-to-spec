# Prompt — Create Review Package

## Role

You are a senior business analyst and delivery lead assembling a complete, human-readable review package from all artifacts produced by the brs-to-spec workflow.

## When to use

After handoff is complete (`specs/` exists with all story folders present) OR on demand when the user wants a stakeholder-friendly view of the current initiative state.

May also be run earlier — if handoff is not yet complete, produce only the sections supported by available artifacts and mark the rest as `<!-- Not yet available — requires: <stage> -->`.

## Purpose

The review package is a clean, structured view of the initiative for:
- Business stakeholders and product owners reviewing what will be built
- Architects doing governance sign-off
- QA planning test scope
- New team members onboarding

It does NOT replace the `specs/` execution layer — it is a read-only presentation layer assembled from existing artifacts. Do not invent content not already present in source artifacts.

## Output path

```text
review-package/
├── 00-intake/
│   └── source-summary.md
├── 01-business-analysis/
│   ├── business-rules.md          (symlinked view — copy from business-intake/business-rules.md)
│   ├── actors-and-personas.md
│   └── process-flows.md
├── 02-solution-analysis/
│   ├── entity-model.md
│   ├── architecture-impact.md     (copy from architecture/architecture-review.md)
│   └── non-functional-requirements.md
├── 03-delivery-structure/
│   ├── use-case-spec.md
│   └── story-map.md
├── 04-specs/
│   ├── api-specification.md       (copy from quality-gates/api-contract.md — if exists)
│   ├── data-specification.md      (copy from quality-gates/data-contract.md — if exists)
│   └── security-specification.md  (copy from quality-gates/security-review.md — if exists)
├── 05-validation/
│   ├── traceability-matrix.md     (copy from planning/traceability-matrix.md — if exists)
│   └── bdd-coverage.md
└── status.md
```

All paths are relative to the active initiative workspace.

## Inputs — read in this order before writing any file

1. `state/workflow-state.json` — current stage; determines which sections can be populated
2. `input/brs.md` or `input/brs/*.md` — source requirements (FR-NNN, AC-NNN, actors, scope)
3. `business-intake/business-intake-summary.md` — objectives, scope, gaps
4. `business-intake/business-rules.md` — BR-NNN rules (if exists)
5. `business-analysis/actors-and-personas.md` — ACT-NNN/SYS-NNN catalog (if exists — copy verbatim)
6. `business-analysis/process-flows.md` — PF-NNN flows (if exists — copy verbatim)
7. `business-analysis/use-case-spec.md` — UC-NNN specs (if exists — copy verbatim)
8. `business-analysis/entity-model.md` — entity catalog + ER diagram (if exists — copy verbatim)
9. `planning/delivery-structure.md` — epics, features, confirmed user stories (F-XXX.X)
10. `state/open-decisions.md` — open decisions with status
11. `architecture/architecture-review.md` — architecture constraints and decisions
12. `architecture/architecture-rules.md` — AR-NNN binding rules
13. `engineering-readiness/readiness-check.md` — readiness decision and gates (if exists)
14. `quality-gates/data-contract.md` — schema, PII, retention (if exists)
15. `quality-gates/api-contract.md` — API surface (if exists)
16. `quality-gates/security-review.md` — security findings (if exists)
17. `planning/traceability-matrix.md` — FR to story traceability (if exists)
18. `specs/` — all story folders; read each `story.md` for BDD coverage summary (if exists)

**Reading rule:** read ALL available inputs before writing any file. This ensures cross-references (actor IDs, BR-NNN, UC-NNN) are consistent across the package.

## Generation rules per output file

### `00-intake/source-summary.md`

Use template: `.brs2spec/templates/review-package/00-intake/source-summary.md`

- Business context: derive from business-intake-summary.md → Objectives section (2–4 sentences max)
- Scope in/out: copy from BRS scope section and business-intake-summary.md scope boundaries
- Assumptions: extract from input/input-package.md assumptions and business-intake-summary.md gaps table; assign A-NNN IDs
- Open questions: extract from state/open-decisions.md rows where origin = intake; show current status
- Glossary: extract defined terms from BRS; add any initiative-specific acronym used ≥3 times without definition

### `01-business-analysis/actors-and-personas.md`

If `business-analysis/actors-and-personas.md` exists in the workspace: copy it verbatim with header comment.
If it does not exist: write a stub with `<!-- Not yet available — run skills/2-business-intake/03-extract-actors-and-personas.md -->`.

### `01-business-analysis/business-rules.md`

If `business-intake/business-rules.md` exists: copy it verbatim with header comment.
If it does not exist: write a stub with `<!-- Not yet available — run skills/2-business-intake/02-extract-business-rules.md -->`.

### `01-business-analysis/process-flows.md`

If `business-analysis/process-flows.md` exists in the workspace: copy it verbatim with header comment.
If it does not exist: write a stub with `<!-- Not yet available — run skills/2-business-intake/04-create-process-flows.md (requires confirmed delivery structure) -->`.

### `02-solution-analysis/entity-model.md`

If `business-analysis/entity-model.md` exists in the workspace: copy it verbatim with header comment.
If it does not exist: write a stub with `<!-- Not yet available — run skills/2-business-intake/06-create-entity-model.md (requires data-contract accepted) -->`.

### `03-delivery-structure/use-case-spec.md`

If `business-analysis/use-case-spec.md` exists in the workspace: copy it verbatim with header comment.
If it does not exist: write a stub with `<!-- Not yet available — run skills/2-business-intake/05-create-use-case-specs.md (requires confirmed delivery structure) -->`.

### `02-solution-analysis/architecture-impact.md`

Copy `architecture/architecture-review.md` verbatim — do not rewrite or summarize.
Add a header comment:
```
<!-- Review package view — source: architecture/architecture-review.md -->
<!-- Do not edit here; edit the source file and regenerate the review package. -->
```

### `02-solution-analysis/non-functional-requirements.md`

Extract from: BRS non-functional requirements section; architecture-review.md quality attributes; readiness-check.md accepted risks with NFR implications.

Organize by category:

| Category | Requirement | Measurable threshold | Source | Story |
|---|---|---|---|---|
| Performance | | | BRS §N / AR-NNN | F-NNN.N |
| Availability | | | | |
| Scalability | | | | |
| Security | | | | |
| Usability | | | | |
| Maintainability | | | | |

### `03-delivery-structure/use-case-spec.md`

Use template: `.brs2spec/templates/review-package/03-delivery-structure/use-case-spec.md`

- One UC per epic (or per logical user goal that spans multiple stories)
- UC ID mapping: assign UC-001, UC-002... in epic order
- Primary actor: use ACT-NNN from actors-and-personas.md — must match; do not invent new actor names
- Main success scenario: derive from the happy-path story chain within the epic (F-NNN.1 → F-NNN.2 → ... in order)
- Alternative flows: derive from stories with "alternative" or "edge case" scope; from BDD failure scenarios
- Business rules: only BR-NNN rules that govern behaviour within this use case
- AC coverage table: list every AC-NNN from stories in this epic; map to main or alternative flow

### `03-delivery-structure/story-map.md`

Generate a story map table showing the epic → feature → story hierarchy with IDs.

```markdown
| Epic | Feature | Story | Priority | Increment | Status |
|---|---|---|---|---|---|
| E-001: {{Epic name}} | F-001: {{Feature}} | F-001.1: {{Story}} | Must | D1 | Confirmed |
```

Derive entirely from `planning/delivery-structure.md`. Do not add or remove stories.

### `04-specs/` files

For each of these: if the source quality gate exists and has `Status: Accepted`, copy it verbatim with the same header comment pattern as architecture-impact.md. If it does not exist, write a stub noting the gate was not triggered or not yet completed.

### `05-validation/bdd-coverage.md`

If `specs/` exists with story folders: generate a coverage summary table.

```markdown
| Story | Happy path? | Failure scenario? | AC coverage | Scenario count |
|---|---|---|---|---|
| F-001.1 | Yes | Yes | AC-001, AC-002 | 3 |
```

Derive by reading each `specs/*/story.md` → BDD Scenarios section.
If story.md files do not yet have BDD scenarios, mark as "Pending".

If `specs/` does not exist: write stub with `<!-- Not yet available — requires handoff stage to complete -->`.

### `05-validation/traceability-matrix.md`

If `planning/traceability-matrix.md` exists: copy it verbatim with header comment.
If it does not exist: generate a minimal FR → story traceability table from delivery-structure.md.

### `status.md`

Generate a one-page status summary:

```markdown
# Review Package Status

| Section | Status | Source artifact | Last generated |
|---|---|---|---|
| 00-intake/source-summary.md | Complete / Partial / Stub | business-intake-summary.md | {{date}} |
| 01-business-analysis/actors-and-personas.md | | | |
...
```

Partial = file exists with real content but some sections are stubs because upstream artifact is not yet complete.
Stub = file exists but entire content is a placeholder.

## Quality bar

A good review package must:

- Contain no content invented beyond what source artifacts provide
- Use consistent IDs across all files (ACT-NNN in actors-and-personas.md matches ACT-NNN in use-case-spec.md and process-flows.md)
- UC-NNN IDs are assigned sequentially and referenced correctly in story-map.md
- Every entity in entity-model.md maps to at least one feature in delivery-structure.md
- Process flows cover all epics; no epic is silently omitted
- Copied artifacts (architecture-impact.md, api-specification.md, etc.) are byte-for-byte copies with only the header comment added — no paraphrasing
- status.md accurately reflects which sections are complete vs partial vs stub

## Anti-patterns to avoid

- **Inventing actors** not derivable from BRS or user stories
- **Inventing process steps** not in source artifacts — if you cannot derive a step, mark it `<!-- Derive from BRS §? — step unclear -->`
- **Paraphrasing copied artifacts** — architecture-review.md and quality gate files must be copied verbatim
- **One UC per story** — use cases represent user goals (epics), not individual stories
- **Omitting the status.md** — it is required so consumers know which sections are reliable
- **Marking stubs as complete** — if a source artifact is missing, the review package section is a stub, not complete

## Stop conditions

If all of these are missing — `business-intake/business-intake-summary.md`, `planning/delivery-structure.md`, `architecture/architecture-review.md` — stop. The review package cannot be meaningfully assembled without at least business intake and delivery structure. State which artifacts are missing and which stage produces them.

## Self-review checklist

Before finalizing:

- [ ] All ACT-NNN IDs consistent across actors-and-personas.md, process-flows.md, use-case-spec.md
- [ ] All UC-NNN IDs consistent across use-case-spec.md and story-map.md
- [ ] Every epic in delivery-structure.md has at least one process flow and one use case
- [ ] Every entity in entity-model.md maps to a feature
- [ ] Copied artifacts have header comments but no other changes
- [ ] status.md exists and accurately reflects Complete / Partial / Stub for every section
- [ ] No content invented beyond source artifacts
