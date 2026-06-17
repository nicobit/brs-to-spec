# Proposed Wave 4: Multi-Agent Execution Readiness

This document proposes a fourth wave of framework evolution focused on making the framework more compatible with downstream multi-agent execution systems.

It builds on the existing three-wave model without changing the framework's core identity.

## Purpose of Wave 4

Wave 4 is not about turning the framework into a multi-agent runtime.

It is about making the framework a stronger upstream control plane for multi-agent execution.

That means improving the framework so downstream orchestrators can consume its handoff packages with less ambiguity, less inference, and lower coordination risk.

## Positioning

The first three waves move the framework toward a more context-driven AI operating model:

- Wave 1: core context mechanics
- Wave 2: operational grounding and resilience
- Wave 3: usability, examples, and learning loops

Wave 4 would extend that model into distributed execution readiness.

In simple terms:

- Waves 1 to 3 make the framework better at preparing AI work
- Wave 4 makes the framework better at preparing AI work for parallel and multi-agent execution

## Why Wave 4 makes sense

As AI-assisted engineering matures, many teams will not stop at one coding agent working on one task at a time.

They will increasingly want:

- parallel implementation
- specialized agent roles
- multi-repo execution
- persistent work coordination
- execution recovery and monitoring

Those concerns belong to execution systems such as `gastown`.

But the quality of upstream work shaping becomes even more important in that world.

That is why a Wave 4 focused on multi-agent execution readiness is strategically consistent with the framework.

## Wave 4 objective

Make the framework's handoff and execution-contract layer more graph-aware, concurrency-aware, repo-aware, and conflict-aware so that downstream multi-agent systems can execute work with less guesswork.

## Proposed Wave 4 scope

Wave 4 should focus on these enhancement themes:

1. multi-agent-ready handoff structure
2. execution topology metadata
3. agent-role-aware execution packaging
4. stronger multi-repo execution slicing
5. execution-risk and merge-risk visibility
6. execution feedback return paths

## Proposed Wave 4 backlog

### 4.1 Multi-agent-ready handoff structure

Define handoff expectations that explicitly identify:

- independent tasks
- blocked tasks
- partially parallelizable tasks
- unsafe concurrency areas

Outcome:

- downstream runtimes can dispatch work more safely and accurately

### 4.2 Execution topology metadata

Add metadata or structure describing:

- dependency edges
- parallel groups
- sequential groups
- checkpoint boundaries
- review-before-continue stages

Outcome:

- handoff becomes execution-graph aware instead of list-only

### 4.3 Agent-role-aware execution packaging

Extend packaging and retrieval so downstream systems can prepare packages for different agent roles such as:

- coding agent
- reviewer agent
- architecture-check agent
- gate-validation agent
- test-generation agent

Outcome:

- context packages better match the role of the executing agent

### 4.4 Multi-repo and workstream execution slicing

Strengthen the framework's ability to describe:

- repo-local tasks
- repo-to-repo dependencies
- shared-contract coordination points
- merge-ordering expectations

Outcome:

- multi-repo implementation becomes easier to coordinate safely

### 4.5 Merge-risk and conflict-risk visibility

Add guidance for surfacing:

- shared-file hotspots
- shared-module overlap
- contract-change blast radius
- rollout-sensitive overlap

Outcome:

- parallel work can be planned with more realistic collision awareness

### 4.6 Execution feedback return path

Define how downstream execution outcomes should return upstream as framework learning inputs, especially:

- repeated merge conflicts
- repeated blocker types
- repeated decomposition failures
- repeated architecture exceptions

Outcome:

- framework refinement becomes informed by actual distributed execution behavior

## Suggested sequence inside Wave 4

Recommended order:

1. `4.1` multi-agent-ready handoff structure
2. `4.2` execution topology metadata
3. `4.3` agent-role-aware execution packaging
4. `4.4` multi-repo and workstream execution slicing
5. `4.5` merge-risk and conflict-risk visibility
6. `4.6` execution feedback return path

Reasoning:

- handoff shape and topology come first because they define the execution surface
- role-aware packaging builds on the Wave 1 context model plus the new execution surface
- multi-repo slicing and risk visibility refine execution realism
- feedback loops become most useful once the framework is actually being consumed in a multi-agent way

## Dependency on earlier waves

Wave 4 depends heavily on earlier work:

- Wave 1 provides packaging, precedence, freshness, and retrieval
- Wave 2 provides brownfield grounding and nuance preservation
- Wave 3 provides role views, examples, and feedback maturity

Without those foundations, Wave 4 would risk becoming shallow execution metadata without strong context discipline behind it.

## What Wave 4 should not include

Wave 4 should not make the framework responsible for:

- agent session persistence
- scheduling and dispatch
- worktree management
- watchdog and recovery infrastructure
- runtime merge automation

Those are runtime-layer concerns.

The framework should remain the control plane, not the agent orchestration engine.

## Expected benefits

If Wave 4 is implemented well, the framework should become:

- more compatible with multi-agent execution systems
- more useful for large modular initiatives
- stronger in multi-repo implementation planning
- safer for parallel execution
- more realistic about merge and sequencing risk

## Risks of doing Wave 4 badly

Wave 4 would be a mistake if it:

- dilutes the framework's upstream identity
- adds heavy runtime concepts directly into the framework core
- replaces clear artifact governance with orchestration-specific complexity
- tries to compete with multi-agent runtimes instead of complementing them

## Recommended interpretation

Wave 4 should be treated as:

- an extension of the handoff and execution-contract layer
- a compatibility layer for downstream multi-agent systems
- a maturity step for large-scale AI-assisted engineering

It should not be treated as a pivot away from the framework's core mission.

## Summary judgment

A proposed Wave 4 focused on multi-agent execution readiness is sensible and strategically aligned.

It fits the direction of the framework because it strengthens the point where governed work leaves the framework and enters execution.

The key design rule is simple:

Make the framework more ready for multi-agent execution.
Do not make it become the multi-agent execution runtime.
