# Implementation Sequence

## Recommended strategy

Build `.b2s` as a fresh target instead of trying to mutate `.brs2spec2` into a
staged engine.

## Phase 1 - Define the `.b2s` contracts

Create:

- `.b2s/workflow/workflow-definition.yaml`
- `.b2s/workflow/stage-actions.yaml`
- `.b2s/templates/state/workflow-state.json`
- `.b2s/templates/state/open-decisions.md`

Goal:

- make the staged engine executable on paper before coding scripts

## Phase 2 - Port the reusable artifact layer

Copy and adapt:

- `.brs2spec2/artifact-templates/` -> `.b2s/artifact-templates/`
- selected `.brs2spec2/skills/` -> `.b2s/skills/`

Adaptations:

- replace event language with stage-action language
- remove result-file references from artifact-generation prompts
- preserve output shape and quality bar

## Phase 3 - Build the staged script engine

Implement:

- `next-step`
- `collect-inputs`
- `validate-artifact`
- `validate-result`
- `update-state`
- `repair-state`
- `reset-to-phase`

Goal:

- enforce deterministic mechanics without event queues

## Phase 4 - Build the orchestrator prompt

Create:

- `.b2s/prompts/run-workflow.md`

Behavior:

- read compact state
- call `next-step`
- call `collect-inputs`
- load one active skill prompt
- generate artifact
- call validation
- call state update
- loop or stop

## Phase 5 - Add gate handling

Implement:

- accept/reject current gate
- artifact status transitions
- stage blocking behavior

## Phase 6 - Add repair/reset and resume flows

Create:

- `.b2s/prompts/repair-state.md`
- `.b2s/prompts/reset-to-phase.md`
- `.b2s/prompts/resume-from-phase.md`

## Recommended first thin slice

If you want the smallest valuable prototype, implement only:

1. routing
2. business intake
3. requirements catalog
4. one planning artifact
5. readiness check

This is enough to prove:

- staged orchestration works
- `.brs2spec2` prompts can be reused
- compact state can replace event queues

## Decision

The best `.b2s` path is:

- staged orchestration from `_.brs2spec`
- artifact quality from `.brs2spec2`
- script enforcement from the newer flow-engine improvement work

That gives you a realistic alternative to the token-heavier event model without
going back to the weaker older staged implementation unchanged.
