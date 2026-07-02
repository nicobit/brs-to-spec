# Workflow Type: b2s-dynamic

## Status

Active adaptive workflow.

This workflow type is a self-contained dynamic orchestration loop. It does not
inherit the `b2s-flow` action catalog at runtime and should be evaluated on its
own behavior.

## Purpose

`b2s-dynamic` is for initiatives where the best next refinement step should be
chosen iteration by iteration as the AI learns more about:

- architecture boundaries
- repository ownership
- UI scope
- integration complexity
- planning readiness
- implementation blockers

The core design principle is:

`adaptive gap-closing + developer-facing artifacts + strict traceability`

## Current Scope

This workflow currently provides:

- workflow registration
- workflow-local definition files
- a two-action adaptive loop:
  - `orchestrate-dynamic-iteration`
  - `finalize-dynamic-initiative`
- one developer-facing artifact per iteration
- a single orchestration ledger at `orchestration/iteration-log.md`
- dynamic-only next-step selector branching
- initiative-local workflow loading
- tests that protect selector and workflow loading behavior

This workflow is intentionally opinionated:

- it must not create orchestration meta-artifacts beyond the iteration log
- it must decide the next highest-value implementation gap itself
- it may produce requirements, architecture, quality, or coding-package
  artifacts, but only when they close the current blocker

## Loop Model

The loop works like this:

1. Read the BRS and every existing output artifact.
2. Identify the single most important developer-blocking gap.
3. Produce exactly one artifact that closes that gap.
4. Append the gap, artifact, and next-gap decision to the iteration log.
5. Repeat until a coding agent can implement every capability without asking a
   clarifying question.

Closure then produces `orchestration/implementation-roadmap.md`.

## When To Use

Use this only when:

- the initiative is uncertainty-heavy
- the team wants the AI to choose the next artifact dynamically
- a fixed decomposition sequence would overproduce artifacts or lock the team
  too early
- the goal is implementation completeness, not template completeness

Do not use this when the team already wants the predictable staged structure of
`b2s-flow`.

## Positioning

- `fast-path`
  - small well-understood changes
- `b2s-flow`
  - structured staged decomposition with explicit architecture and planning gates
- `b2s-dynamic`
  - independent adaptive orchestration for high-uncertainty initiatives where
    the AI should decide what artifact is actually needed next
