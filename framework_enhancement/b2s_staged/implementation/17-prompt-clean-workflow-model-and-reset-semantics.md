# Prompt 17 - Clean Workflow Model and Reset Semantics

## Goal

Align the staged YAML model with the actual engine behavior and remove fragile
or misleading semantics.

## Files to modify

- `.b2s/workflow/stage-actions.yaml`
- `.b2s/scripts/b2s_engine/next_step.py`
- `.b2s/scripts/b2s_engine/reset.py`
- `.b2s/scripts/b2s_engine/state.py`
- optionally `.b2s/templates/state/open-decisions.md` and related state-writing
  logic
- `.b2s/tests/test_engine_runtime.py`
- `.b2s/tests/test_engine_maintenance.py`

## Required work

### A. Gate action cleanup

Resolve the gate-on-gate ambiguity.

Implement this explicit short-term model:

- gate actions remain explicit status ids in the workflow model
- gate actions are not normal executable artifact-generation actions
- gate action entries must not declare nested `human_gate.required: true`
- the source artifact action owns gate opening
- gate decision commands own gate closing

### B. `blocked_by_stage`

Implement it in `next_step.py`.

Required behavior:

- add an explicit `_blocked_by_stage_satisfied()` check
- evaluate stage dependencies deterministically from current staged state
- do not leave `blocked_by_stage` as silent dead config

### C. `on_fail.raise_decision`

Remove it from the schema for now.

Do not implement partial open-decision persistence in this prompt.

Required behavior:

- remove or neutralize `on_fail.raise_decision` declarations from
  `stage-actions.yaml`
- keep `open-decisions.md` as a placeholder artifact only until a later prompt
  explicitly designs and implements decision persistence

### D. Reset stage semantics

In `reset.py`, make reset behavior depend on semantic stage id rather than only
array position.

Specifically:

- resetting to `0-routing` must always clear routing-derived fields
- behavior must remain correct even if stage order changes later

### E. Stage completeness semantics

In `next_step.stage_is_complete()`:

- document whether condition-failing actions are intentionally treated as
  optional
- keep condition-failing actions treated as optional for now
- add an explicit code comment documenting that current behavior
- do not change stage completeness semantics in this prompt beyond making them
  explicit and tested

## Constraints

- reduce ambiguity rather than adding more abstract config
- keep behavior explainable from YAML plus engine code
- if a declared feature is not implemented, remove the declaration rather than
  letting it mislead future authors
- this prompt should end with one unambiguous staged model, not multiple
  alternative designs

## Verification

Verify:

1. gate modeling is no longer ambiguous
2. `blocked_by_stage` is either enforced or absent; in this prompt it must be
   enforced
3. `on_fail.raise_decision` is no longer misleadingly declared
3. resetting to `0-routing` clears routing-derived state by stage identity
4. stage completeness behavior for conditional actions is explicit and tested
