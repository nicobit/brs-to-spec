# Rollout Strategy

## Phase 2A — Script assist, prompt still orchestrates

Prompts call scripts for:

- event instantiation
- input collection
- queue moves
- result validation

The dispatcher prompt still sequences the work, but scripts perform the mechanics.

### Benefits

- low migration risk
- retains current prompt-driven flow shape
- removes the most failure-prone manual mechanics first

## Phase 2B — Script-first orchestrator core

Move the orchestration backbone into a script:

- dispatcher selects event
- script performs Step 0–10 mechanics
- AI produces artifact/result content only
- script validates result and updates state

### Benefits

- much stronger enforcement
- less opportunity for mixed-version queue behavior
- easier automated testing

## Phase 2C — Prompt minimization

At this stage prompts become narrower:

- “Here is the input bundle”
- “Write artifact X”
- “Return structured outcome Y”

Everything else is script-owned.

## Recommended first implementation

If only three scripts are introduced first, choose:

1. `instantiate-event`
2. `collect-inputs`
3. `move-event`

Why these three first:

- they address the most common and costly observed failures
- they are highly deterministic
- they provide immediate value without rewriting the whole engine

## Risks

### Risk: partial migration creates duplicated logic

Mitigation:

- define a single source of truth per responsibility
- once a script owns a mechanic, remove the prompt ambiguity around that mechanic

### Risk: script outputs drift from schemas

Mitigation:

- make scripts emit exactly the same field names as engine schemas
- validate script outputs against the same contracts used by the dispatcher

### Risk: too much script complexity too early

Mitigation:

- keep commands small
- do not build a monolithic engine executable first
- introduce script ownership in slices

## Decision

Phase 2 should begin as **script-assisted orchestration**, not a full engine rewrite.
That gives the framework deterministic enforcement quickly while preserving the current
prompt-based artifact-generation model.
