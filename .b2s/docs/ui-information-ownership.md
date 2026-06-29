# UI Information Ownership

## Purpose

This document defines the canonical ownership of UI-related information across the framework to prevent information loss, duplication, and drift.

## Canonical sources

### `architecture/ui-specification.md`

Canonical source for:

- application inventory
- route tree
- page ownership
- route guards and authorization behavior
- page-level fields, validation, actions, states, and user flows
- UI-to-API bindings
- UI-specific open questions and blocking dependencies
- FR-to-UI traceability

### `architecture/solution-decisions.md`

Canonical source for:

- repository ownership
- application ownership when architecturally decided
- frontend technology decisions when confirmed
- auth platform decisions when confirmed
- create-new vs modify-existing decisions
- deployment and component ownership

### `epics/*/implementation-contract.md`

This artifact is an epic-scoped extract and refinement of upstream truth.
It must not originate new initiative-level UI facts unless they come from explicit clarification input.

### `epics/*/stories/*.md`

Stories own story slicing, acceptance behavior, and scoped delivery detail for the epic.
They must not invent new initiative-level UI structure or page truth.

### `epics/*/coding-handoff.md`

This artifact is a self-contained delivery copy for implementation.
It must not become a new source of truth for UI behavior.

## Anti-drift rules

- A UI fact must have one canonical home.
- Downstream artifacts may copy or scope UI facts, but must not silently redefine them.
- If an epic clarification changes a UI fact, the change must reference the originating `UIQ-*` or clarification record.
- When two artifacts disagree, the canonical source wins unless an explicit scoped clarification overrides it.
