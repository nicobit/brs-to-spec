# Next Phase Plan - Scripted Enforcement First

## Why this version

The `with-scripts/` proposal was directionally correct, but it mixed two
different improvement goals:

- move the orchestrator mechanics into scripts
- harden validation for intake and requirements artifacts

This package merges them into one plan with a clearer priority order.

## Main diagnosis

The framework does not mainly fail because templates are missing instructions.
It fails when the LLM is trusted to perform deterministic mechanics that it can:

- skip
- improvise
- fabricate
- partially execute

That is why the same family of failures keeps repeating:

- `read_from` files not actually read
- result files created without valid queue history
- event files recreated instead of moved
- state files drifting away from queue truth
- validation notes claiming checks that were never mechanically performed

## Strategic objective

Move the enforcement boundary so that:

- scripts produce authoritative mechanical evidence
- prompts consume that evidence and write only content that requires judgment

## Recommended rollout

### Slice A - engine correctness

Deliver first:

1. `instantiate-event`
2. `collect-inputs`
3. `move-event`
4. `check-integrity`

This addresses the biggest sources of chain corruption.

### Slice B - validation correctness

Deliver next:

1. `validate-result`
2. `validate-artifact-counts`
3. `validate-no-placeholders`
4. template `must_include` anchoring

This addresses fabricated validation and weak result contracts.

### Slice C - state and maintenance

Deliver after the first two slices are stable:

1. `update-state`
2. `repair-processing`
3. `repair-chain`
4. `reset-to-phase`

## Design decisions

- Use Python for the engine core.
- Prefer standard library first.
- Keep commands small and composable.
- Use the existing event/result/state schemas where possible.
- Do not rewrite business artifacts in repair/reset commands.
- Use fixed output files for script decisions, not stdout-only control flow.

## Script output contract

Commands that produce authoritative decisions must write structured files that
the dispatcher reads back as gating inputs.

Recommended locations:

- `.flow/events/processing/<event_id>-inputs.json`
- `.flow/events/processing/<event_id>-integrity-check.yaml`
- `.flow/events/processing/<event_id>-result-check.yaml`
- `.flow/events/processing/<event_id>-artifact-counts.yaml`
- `.flow/events/processing/<event_id>-placeholder-check.yaml`
- `.flow/events/processing/<event_id>-state-update.json`
- `.flow/state/integrity-check.yaml` for workspace-wide pre-dispatch scans

Dispatcher rule:

- if a required script output file is missing, malformed, or reports failure,
  the dispatcher must stop or fail the event at that boundary
- prompts should not merely say "treat this as authoritative"
- prompts should say "read this required file and gate the next step on its
  contents"

## Success criteria

The enhancement is successful when:

- runtime events are always template-instantiated by script
- every `read_from` entry generates machine-written evidence
- queue transitions are real moves
- orphan result files are detectable and blocking
- result validation can fail even if the LLM wrote `status: pass`
- workflow state can be rebuilt from authoritative queue/result facts
