# Workflow Type: b2s-dynamic

## Status

Experimental scaffold.

This workflow type introduces the framework shape for dynamic, loop-based
BRS-to-spec orchestration without changing existing workflow behavior.

It is intentionally additive and limited in scope.

## Purpose

`b2s-dynamic` is for initiatives where the best next refinement step may need to
change as the team learns more about:

- architecture boundaries
- repository ownership
- UI scope
- integration complexity
- planning readiness

The core design principle is:

`stable artifacts + stable validation + dynamic orchestration`

## Current Scope

This scaffold currently provides:

- workflow registration
- workflow-local definition files
- dynamic orchestration artifact templates
- dynamic orchestrator skill prompts
- a dedicated dynamic runner prompt
- dynamic-only next-step selector branching
- additive dynamic workflow state tracking
- dynamic specialist-action fallback to the `b2s-flow` action catalog
- tests that protect file loading and reference integrity

This scaffold does not yet introduce:

- full end-to-end dynamic orchestration behavior
- replacement of `b2s-flow`

## When To Use

Use this only when:

- you are intentionally evaluating dynamic orchestration
- the initiative is uncertainty-heavy
- you accept experimental workflow behavior

Do not use this as the default answer for normal work.

## Positioning

- `fast-path`
  - small well-understood changes
- `agile-delivery-light-flow`
  - lean staged planning
- `b2s-flow`
  - serious staged BRS-to-spec work
- `b2s-dynamic`
  - experimental loop-based orchestration for high-uncertainty initiatives
