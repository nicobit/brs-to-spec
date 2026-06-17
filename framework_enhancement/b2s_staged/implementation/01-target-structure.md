# Target Structure

## Framework root

Recommended `.b2s/` structure:

```text
.b2s/
  agent-instructions.md
  module-index.md
  workflow/
    workflow-definition.yaml
    stage-actions.yaml
  prompts/
    run-workflow.md
    reset-to-phase.md
    resume-from-phase.md
    repair-state.md
  skills/
    architect/
    delivery-lead/
    engineering-lead/
    orchestrator/
    product-owner/
    qa-analyst/
    reviewer/
    security-reviewer/
  artifact-templates/
  templates/
    state/
      workflow-state.json
      open-decisions.md
  scripts/
    b2s_cli.py
    b2s_engine/
      __init__.py
      workspace.py
      next_step.py
      inputs.py
      validation.py
      state.py
      reset.py
      gates.py
  tests/
    fixtures/
      sample-initiative/
      missing-brs/
      pending-gate/
      stale-downstream/
```

## Initiative-local state

Recommended initiative-local `.b2s/` state:

```text
initiatives/<id>-<slug>/
  .b2s/
    state/
      workflow-state.json
      open-decisions.md
      run-log.jsonl
    tmp/
      next-step.json
      current-inputs.json
      current-validation.yaml
      current-state-update.json
      current-gate.json
```

## Why this shape

- separates framework code from initiative state
- keeps runtime artifacts compact
- supports prompt gating on script outputs
- avoids the `.flow/events/` queue model
- establishes a stable test and fixture surface from the start
