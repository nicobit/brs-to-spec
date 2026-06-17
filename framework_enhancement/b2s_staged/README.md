# .b2s Staged Framework Analysis

## Purpose

This folder analyzes how to build a new staged framework in `.b2s/` that:

- keeps the lighter staged-orchestrator model of `_.brs2spec`
- produces the same artifact outputs expected by `.brs2spec2`
- reuses the newer `.brs2spec2` artifact-generation prompts where possible
- avoids the full event queue (`pending/processing/done/failed`) as the primary execution model

## Documents

- `00-summary.md` - main conclusion and recommendation
- `01-current-state-comparison.md` - staged vs event-based comparison
- `02-b2s-target-architecture.md` - recommended `.b2s` design
- `03-reuse-map-from-brs2spec2.md` - what to reuse from `.brs2spec2`
- `04-gap-analysis-and-required-work.md` - what must change or be added
- `05-implementation-sequence.md` - suggested implementation order

## Bottom line

Yes, a staged `.b2s` framework is feasible.

The best path is not to port `.brs2spec2` events into `.b2s`.
The best path is to:

1. keep a compact stage/state engine
2. reuse `.brs2spec2` skill prompts and artifact templates for output quality
3. move deterministic orchestration and validation into scripts
4. derive "next step" from stage state and artifact truth rather than from per-event queue files
