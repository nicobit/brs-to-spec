# Flow Engine Improvements - Next

## Purpose

This folder turns the earlier `with-scripts/` proposal into a tighter, ordered
implementation package for the next enhancement cycle.

It combines two threads:

- the broader phase-2 move of deterministic flow-engine mechanics into scripts
- the intake validation work that exposed where prompt-only enforcement still fails

## Recommended approach

Use a two-layer rollout:

1. Add script-owned mechanics first where the answer is fully deterministic.
2. Keep artifact writing prompt-driven, but force prompts to consume
   machine-prepared inputs and machine-written validation outputs.

## Output convention

Script outputs should not rely on stdout-only consumption.

Use a fixed-file convention instead:

- event-scoped outputs go under `.flow/events/processing/`
- state or queue-wide outputs go under `.flow/state/`
- the dispatcher must read those files as required inputs before proceeding

This makes script results part of the workflow data flow rather than advisory
console output.

## What changes first

Start with the mechanics that caused the observed failures:

- runtime event instantiation from templates
- authoritative input collection and `read_evidence`
- real queue moves instead of recreate/copy behavior
- integrity checks for orphan result files
- result-file and artifact-count validation

## What stays prompt-driven

- business interpretation
- writing summaries, requirements, diagrams, rules, and plans
- semantic explanations of genuine gaps

## Files in this folder

- `00-next-phase-plan.md` - consolidated direction and design decisions
- `01-scope-and-boundaries.md` - what scripts own vs what prompts own
- `02-command-roadmap.md` - target command surface
- `03-implementation-sequence.md` - ordered delivery plan
- `04-acceptance-and-test-strategy.md` - how to verify each slice
- `05-prompt-scaffold-engine-core.md`
- `06-prompt-implement-runtime-instantiation.md`
- `07-prompt-implement-input-collection.md`
- `08-prompt-implement-queue-and-integrity.md`
- `09-prompt-implement-result-validation.md`
- `10-prompt-implement-state-updates.md`
- `11-prompt-anchor-template-validation.md`
- `12-prompt-wire-dispatcher-to-scripts.md`
- `13-prompt-add-repair-and-reset.md`

## Core principle

Scripts should own anything that can be derived mechanically from files, paths,
templates, and queue state. Prompts should own only synthesis and judgment.
