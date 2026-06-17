# Flow Engine Improvements — Phase 2 (With Scripts)

## Purpose

Phase 1 strengthens the flow engine through prompts, schemas, and dispatcher rules.
That improves auditability, but it still depends on the AI faithfully executing a
text protocol.

Phase 2 moves the deterministic parts of the engine into scripts so the framework can:

- resolve paths consistently
- read inputs deterministically
- generate machine-verifiable `read_evidence`
- instantiate runtime events from templates without dropping fields
- enforce queue transitions (`pending -> processing -> done/failed`) as real moves
- validate result-file contracts before state updates
- repair stale queue/state mechanically

This phase does **not** replace AI-authored artifacts. The AI still writes business
artifacts. Scripts take over the orchestration mechanics around those artifacts.

## Scope

Phase 2 focuses on the **engine/orchestrator layer**, not the artifact-generation layer.

### Move to scripts

- workspace discovery
- event-template instantiation
- input resolution and evidence capture
- queue transitions
- result-contract validation
- state updates
- processing/pending repair
- chain repair
- reset/rebuild flows

### Keep prompt-driven

- writing business-intake summaries
- writing requirements catalogs
- diagrams, rules, gaps, planning artifacts
- architecture and delivery artifacts

## Deliverables in this folder

- `00-phase-2-plan.md` — goals, principles, and rollout
- `01-script-architecture.md` — proposed script boundaries and responsibilities
- `02-command-surface.md` — CLI commands and their behavior
- `03-data-contracts.md` — files exchanged between scripts and prompts
- `04-rollout-strategy.md` — incremental adoption plan
- `05-implementation-plan.md` — ordered execution plan
- `06-prompt-scaffold-python-engine.md` — create the script package
- `07-prompt-instantiate-event-script.md` — implement event instantiation
- `08-prompt-collect-inputs-script.md` — implement input reading + read_evidence
- `09-prompt-move-event-script.md` — implement queue moves
- `10-prompt-validate-result-script.md` — implement result contract validation
- `11-prompt-update-state-script.md` — implement state/log/decision updates
- `12-prompt-wire-prompts-to-scripts.md` — wire prompt layer to scripts
- `13-prompt-repair-script-commands.md` — implement repair/reset commands

## Design principle

**Scripts own truth about mechanics. Prompts own judgment about content.**

If a task can be expressed as deterministic filesystem/state logic, it should move to
scripts. If a task requires interpretation or synthesis from BRS/business context, it
can remain prompt-driven, but should consume machine-prepared inputs and emit
machine-checkable outputs.
