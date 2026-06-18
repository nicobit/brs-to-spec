# Prompt - Create Standalone Delivery Package

## Role

You are an engineering lead preparing a disciplined standalone delivery package when OpenSpec is not used.

## Context

This prompt is used only when execution mode is Standalone. Standalone mode must not be lower quality than OpenSpec mode.

## Purpose

Create a delivery package with scope, design approach, tasks, validation, review checklist, and initiative traceability.

Derive the handoff from approved delivery shape plus initiative-specific architecture refinement, not from vague planning alone.

## Inputs

Use these inputs when available:

- `engineering-readiness/readiness-check.md`
- `quality-gates/*.md`
- `planning/delivery-structure.md`
- `planning/traceability-matrix.md`
- `architecture/architecture-review.md`
- `architecture/architecture-rules.md`
- `business-intake/business-intake-summary.md`
- `perspectives/agile-planning/gitlab-planning-view.md` when a planning view exists

## Output path

```text
standalone-delivery/D1-<deliverable-name>/
```

## Mandatory output files

All five files are required. Do not skip any:

```text
standalone-delivery/D1-<deliverable-name>/
  delivery-spec.md       ← scope, requirements covered, architecture constraints, quality gates, risks
  implementation-plan.md ← story-by-story breakdown with one section per F-XXX.X story
  tasks.md               ← one task block per story per engineering concern (API, data, observability, security)
  validation-plan.md     ← one validation task per AC-NNN; references SCN-NNN BDD scenarios
  review-checklist.md    ← reviewer checklist tied to gate artifacts and architecture rules
```

## Reading rule

**Read ALL inputs before writing any file.** Derive the task list from `planning/delivery-structure.md` user stories (`F-XXX.X`). If delivery-structure has no `F-XXX.X` stories — only epics or bullet points — stop immediately: go back and run `skills/3-planning-and-modular-delivery/03-create-delivery-structure.md` first. Do not invent tasks from epics.

## Templates

Use:

```text
.brs2spec/templates/standalone-delivery/delivery-spec.md
.brs2spec/templates/standalone-delivery/implementation-plan.md
.brs2spec/templates/standalone-delivery/tasks.md
.brs2spec/templates/standalone-delivery/validation-plan.md
.brs2spec/templates/standalone-delivery/review-checklist.md
```

Preserve all template headings. Every task block in `tasks.md` must have all required fields filled — a task with a blank `Related requirement` or blank `Evidence expected` is a stub and fails the quality bar.
Add an optional compact interaction, sequence, or focused flow view in `delivery-spec.md` only when it materially improves implementation or review clarity for the active deliverable.

## Quality bar

A good output must:

- make standalone mode disciplined and reviewable
- include quality gates and accepted risks
- make tasks small and validation-oriented
- include evidence expected for each task
- convert business planning items into engineering-ready implementation tasks
- reference requirements, user stories when available, acceptance sources, architecture constraints, and quality gates
- derive engineering tasks from approved user stories plus architecture, readiness, and quality-gate constraints
- use architecture review and architecture rules to make initiative-specific constraints explicit in the delivery package
- keep delivery-spec acceptance references pointed at source validation artifacts instead of duplicating full acceptance text
- state out of scope clearly
- avoid generic delivery-package prose that does not change implementation or review behavior
- keep any optional visual in `delivery-spec.md` tightly scoped to the active deliverable
- do not treat an optional visual as required unless the interaction or boundary is still too unclear without it

## Anti-patterns to avoid

Do not produce outputs that:

- treat standalone as informal notes
- skip validation because OpenSpec is not used
- copy user stories directly as implementation tasks
- create broad tasks without evidence
- ignore required quality gates
- invent architecture
- proceed when delivery shape or architecture refinement is still too weak to support engineering handoff

## Stop conditions

- If required inputs are missing, do not invent content.
- List missing inputs and explain the impact.
- Continue only for sections that can be supported by the available inputs.

## Self-review checklist

Before finalizing, verify:

- [ ] All 5 output files are present: `delivery-spec.md`, `implementation-plan.md`, `tasks.md`, `validation-plan.md`, `review-checklist.md`
- [ ] `implementation-plan.md` has one section per `F-XXX.X` user story — not per epic, not per area
- [ ] Every task in `tasks.md` has: `Related requirement` (FR-NNN), `Related user story` (F-XXX.X), `Acceptance / validation reference` (AC-NNN), `Architecture constraint` (AR-NNN if applicable), `Evidence expected` — no field is blank
- [ ] `validation-plan.md` has one validation task per AC-NNN from the stories in scope; each references its SCN-NNN BDD scenario(s) or states "BDD not triggered"
- [ ] `delivery-spec.md` Requirements Covered table references all FR-NNN IDs from the stories in scope
- [ ] `delivery-spec.md` Architecture Constraints table references AR-NNN rule IDs — not generic descriptions
- [ ] Quality gates are reflected with their `Status: Accepted` confirmation
- [ ] Review checklist entries are tied to specific gate artifacts and AR-NNN rules
- [ ] No task merely restates a user story or epic — every task is a concrete engineering action
- [ ] Engineering can implement from this package without opening any other artifact
