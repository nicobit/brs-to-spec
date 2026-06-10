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

## Templates

Use:

```text
.brs2spec/templates/standalone-delivery/delivery-spec.md
.brs2spec/templates/standalone-delivery/implementation-plan.md
.brs2spec/templates/standalone-delivery/tasks.md
.brs2spec/templates/standalone-delivery/validation-plan.md
.brs2spec/templates/standalone-delivery/review-checklist.md
```

Preserve the template headings in each file and add detail only where the evidence demands it.
Keep each artifact compact and implementation-focused. Prefer referenced evidence over repeated source text.
Add an optional compact interaction, sequence, or focused flow view in `delivery-spec.md` only when it materially improves implementation or review clarity for the active deliverable.
Do not add a visual that merely restates simple scope or task tables.

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

- [ ] Delivery spec includes scope and constraints.
- [ ] Tasks include traceability back to requirement, user story when available, acceptance source, architecture constraint, and quality gate.
- [ ] Tasks include validation and evidence.
- [ ] Quality gates are reflected.
- [ ] Delivery package clearly consumes approved delivery shape plus initiative-specific architecture refinement.
- [ ] Review checklist is complete.
- [ ] Standalone output is usable by engineering.
- [ ] Engineering can act on the package without needing to reconstruct missing scope or constraints.
