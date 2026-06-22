# `.b2s` Target Architecture

## Core design

`.b2s` should be a staged engine with compact state and script-owned mechanics.

Suggested workspace shape:

```text
.b2s/
  agent-instructions.md
  workflow/
    workflow-definition.yaml
    stage-actions.yaml
  prompts/
    run-workflow.md
    reset-to-phase.md
    resume-from-phase.md
    repair-state.md
  skills/
    ...
  artifact-templates/
    ...
  scripts/
    b2s_cli.py
    b2s_engine/
      workspace.py
      next_step.py
      inputs.py
      validation.py
      state.py
      reset.py
```

Initiative workspace shape:

```text
initiatives/<id>-<slug>/
  input/
  business-intake/
  business-analysis/
  architecture/
  planning/
  engineering-readiness/
  quality-gates/
  specs/ or standalone-delivery/
  review-package/
  .b2s/
    state/
      workflow-state.json
      open-decisions.md
      run-log.jsonl
    tmp/
      current-inputs.json
      current-validation.yaml
      current-state-update.json
```

## Execution model

The orchestrator loop should be:

1. Resolve active initiative workspace
2. Read compact state
3. Run `next-step`
4. Run `collect-inputs`
5. Load the mapped prompt for that stage action
6. Generate the artifact
7. Run validation scripts
8. Run `update-state`
9. Reassess

## Primary unit of work

The unit of work should be a **stage action**, for example:

- `route-initiative`
- `create-business-intake-summary`
- `create-requirements`
- `create-use-case-diagram`
- `create-delivery-structure`

These are not runtime event files. They are action IDs in the stage graph.

## State model

Suggested `workflow-state.json` fields:

- `initiative_id`
- `current_stage`
- `delivery_mode`
- `execution_mode`
- `project_type`
- `last_completed_action`
- `next_action`
- `artifact_status`
- `quality_gates_triggered`
- `optional_artifacts_requested`
- `open_decisions`
- `blocking_decisions`
- `state_validated`
- `last_updated`

## Why this is enough

This gives `.b2s`:

- restartability
- reset/resume support
- artifact truth tracking
- lower overhead than persistent event queues

without requiring:

- event instantiation
- queue movement logic
- event/result duplication
- queue repair semantics

## Recommended script outputs

- `.b2s/state/next-step.json`
- `.b2s/tmp/current-inputs.json`
- `.b2s/tmp/current-validation.yaml`
- `.b2s/tmp/current-state-update.json`

These should be gating inputs for the orchestrator prompt.
