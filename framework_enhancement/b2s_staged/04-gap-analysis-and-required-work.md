# Gap Analysis And Required Work

## Gap 1 - `.brs2spec2` output quality is tied to event metadata

Problem:

Many `.brs2spec2` strengths are encoded in event templates:

- `read_from`
- `write_to`
- `must_include`
- `validation_rules`
- `on_success`
- `on_failure`

If `.b2s` removes events, these rules need a new home.

Required work:

- create `.b2s/workflow/stage-actions.yaml`
- for each action, define:
  - `action_id`
  - `persona`
  - `skill_ref`
  - `artifact_template_ref`
  - `inputs.required`
  - `inputs.optional`
  - `outputs.primary`
  - `outputs.secondary`
  - `must_include`
  - `validation_rules`
  - `blocked_by_stage`
  - `blocked_by_action`
  - `human_gate`

## Gap 2 - staged orchestration needs stronger enforcement than old `_.brs2spec`

Problem:

`_.brs2spec` kept a compact state model, but trusted the model too much for:

- selecting next work
- reading required inputs honestly
- validating completeness
- updating state faithfully

Required work:

- add scripts for:
  - `next-step`
  - `collect-inputs`
  - `validate-artifact`
  - `validate-result`
  - `update-state`
  - `reset-to-phase`
  - `repair-state`

## Gap 3 - business-analysis output model differs between branches

Problem:

`_.brs2spec` and `.brs2spec2` do not always use the same artifact set or paths.

Examples:

- `.brs2spec2` has `business-analysis/requirements.md` as the first stage-2b anchor
- `_.brs2spec` business-analysis flow is older and less centered on a requirements catalog
- `.brs2spec2` has explicit `use-cases.puml` and richer event split

Required work:

- adopt `.brs2spec2` artifact set as the `.b2s` target truth
- update staged orchestration to expect those outputs
- retire older staged artifact expectations where they conflict

## Gap 4 - stage graph must be extracted from event graph

Problem:

`.brs2spec2/workflow/workflow-definition.yaml` is stage-based at the top level,
but its executable semantics depend on event templates.

Required work:

- derive a staged action graph from the current event graph
- support parallelizable actions logically, but execute serially by default
- preserve conditions such as:
  - `project_type == brownfield`
  - quality gates triggered from readiness
  - optional post-handoff artifacts

## Gap 5 - WAIT_HUMAN must become stage-state, not queue-state

Problem:

The current event engine models human review as explicit WAIT_HUMAN events.

Required work:

- in `.b2s`, represent this using:
  - `artifact_status`
  - `current_gate`
  - `awaiting_human`
  - `blocked_reason`

- add commands such as:
  - `approve-current-gate`
  - `reject-current-gate`

## Gap 6 - prompt adaptation work is still needed

Problem:

Even reusable `.brs2spec2` prompts still mention event assumptions in places:

- result-file expectations
- event identity
- routing through dispatcher semantics

Required work:

- adapt reusable prompts to a `.b2s` interface
- replace event language with action language
- replace `read_from` assumptions with input-bundle assumptions
- keep artifact-generation instructions intact

## Gap 7 - state schema needs to be redesigned, not copied

Problem:

The old staged state is too weak, and the event state is too heavy.

Required work:

- define a new `.b2s/state/workflow-state.json` schema
- include:
  - current stage
  - next action
  - artifact statuses
  - validation timestamps
  - gate status
  - triggered optional work
  - blocking decisions

## Gap 8 - repair/reset logic must be rethought

Problem:

Event-engine repair means queue repair.
Stage-engine repair means artifact/state reconciliation.

Required work:

- define repair as:
  - rescan artifacts
  - recompute artifact statuses
  - recompute current stage
  - recompute next action

- define reset as:
  - back up state
  - downgrade downstream artifact statuses
  - set next action to the requested phase boundary

## Gap 9 - acceptance tests need a staged fixture set

Problem:

The current phase-2 event-script plan assumes queue/event fixtures.

Required work:

- define staged fixtures under `.b2s/tests/fixtures/`
- test:
  - missing BRS
  - stale intake summary
  - missing requirements artifact
  - readiness gate not accepted
  - optional quality gate triggered
  - handoff stale after upstream change
