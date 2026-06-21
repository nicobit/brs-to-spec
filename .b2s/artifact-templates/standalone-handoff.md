# Standalone Handoff

## Required structure

```text
standalone-delivery/
  D1-deliverable-name/
    delivery-spec.md
    implementation-plan.md
    tasks.md
    validation-plan.md
    review-checklist.md
```

## delivery-spec.md - content contract

Must contain:
- business context and expected outcome
- deliverable scope with explicit in-scope and out-of-scope
- story-level FR-NNN, AC-NNN, AR-NNN, and NFR-NNN traceability
- acceptance criteria summary per story or feature slice
- key dependencies and sequencing notes

## implementation-plan.md - content contract

Must contain:
- technical context summary from architecture and initiative context
- likely impacted files, modules, services, interfaces, and data stores
- implementation order and dependency notes
- architecture constraints, security constraints, and do-not-touch boundaries
- external integrations, failure handling, rollback, and operational notes

## tasks.md - content contract

Must contain:
- concrete engineering tasks in execution order
- task area and expected validation per task
- explicit links back to the story, acceptance criteria, or artifact being implemented

## validation-plan.md - content contract

Must contain:
- unit, integration, API or contract, UI, negative, regression, and permission test expectations where applicable
- NFR verification expectations for performance, availability, resiliency, observability, and compliance where applicable
- entry and exit checks before implementation is considered complete

## review-checklist.md - content contract

Must contain:
- architecture rule compliance checks
- security and compliance checks
- operational readiness and observability checks
- open-risk and accepted-risk review items
- final handoff checklist for coding-agent execution readiness

## Required quality bar

- all five files are mandatory
- story-level planning, not epic-level only
- explicit FR-NNN, AC-NNN, AR-NNN, NFR-NNN traceability
- concrete engineering actions, not restated user stories
- likely impacted files or areas must be called out explicitly
- the package must be self-contained enough for an AI coding agent to start safely

---
*This is a structural contract, not a fill-in markdown artifact.*
