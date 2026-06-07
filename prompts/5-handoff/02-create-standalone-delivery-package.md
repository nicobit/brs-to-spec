# Prompt — Create Standalone Delivery Package

## Role

You are an engineering lead preparing a disciplined standalone delivery package when OpenSpec is not used.

## Context

This prompt is used only when execution mode is Standalone. Standalone mode must not be lower quality than OpenSpec mode.

## Purpose

Create a delivery package with scope, design approach, tasks, validation and review checklist.

## Inputs

Use these inputs when available:

- `engineering-readiness/readiness-check.md`
- `quality-gates/*.md`
- `planning/traceability-matrix.md`
- `architecture/global-architecture-rules.md`
- `business-intake/business-intake-summary.md`

## Output path

```text
standalone-delivery/D1-<deliverable-name>/
```

## Required output structure

```markdown
# Standalone Delivery Package

## delivery-spec.md

### Purpose

### Scope

### Out of Scope

### Requirements Covered

### Architecture Constraints

### Acceptance Criteria

### Quality Gates Applied

## implementation-plan.md

### Design Approach

### Components Affected

### API / Data / Event Impact

### Security Considerations

### Observability

### Dependencies

### Risks

## tasks.md

### Implementation Tasks

- [ ] Task 1 — <small validated task>
  - Related requirement:
  - Related architecture constraint:
  - Related quality gate:
  - Validation:
  - Evidence expected:
  - Owner:

### Validation Tasks

### Documentation Tasks

### Review Tasks

## validation-plan.md

### Automated Validation

### Manual Validation

### Regression Validation

### Security Validation

### Evidence Required

### Exit Criteria

## review-checklist.md

### QA Review

### Architecture Review

### Security Review

### Release Readiness

### Final Decision
```

## Quality bar

A good output must:

- make standalone mode disciplined and reviewable
- include quality gates and accepted risks
- make tasks small and validation-oriented
- include evidence expected for each task
- state out of scope clearly

## Anti-patterns to avoid

Do not produce outputs that:

- treat standalone as informal notes
- skip validation because OpenSpec is not used
- create broad tasks without evidence
- ignore required quality gates
- invent architecture

## Stop conditions

- If required inputs are missing, do not invent content.
- List missing inputs and explain the impact.
- Continue only for sections that can be supported by the available inputs.

## Self-review checklist

Before finalizing, verify:

- [ ] Delivery spec includes scope and constraints.
- [ ] Tasks include validation and evidence.
- [ ] Quality gates are reflected.
- [ ] Review checklist is complete.
- [ ] Standalone output is usable by engineering.
