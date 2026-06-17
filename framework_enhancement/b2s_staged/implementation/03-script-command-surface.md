# Script Command Surface

## Required commands

### `next-step`

Determines the next executable stage action from workflow state and artifact
truth.

Output:

- `.b2s/state/next-step.json`

Required fields:

- `overall`
- `selected_action`
- `selected_stage`
- `reason`
- `blocking_reason`
- `ready_actions`

### `collect-inputs`

Resolves required and optional inputs for the selected action and writes an
authoritative input bundle.

Output:

- `.b2s/tmp/current-inputs.json`

Required fields:

- `overall`
- `action_id`
- `required_inputs`
- `optional_inputs`
- `missing_required_inputs`
- `read_evidence`

### `validate-artifact`

Checks produced artifacts against mechanical rules:

- existence
- placeholder detection
- count checks
- required IDs

Output:

- `.b2s/tmp/current-validation.yaml`

Required fields:

- `overall`
- `action_id`
- `artifact_path`
- `checks`
- `failures`

### `update-state`

Updates workflow state and decision counts after validated execution.

Output:

- `.b2s/tmp/current-state-update.json`

Required fields:

- `overall`
- `action_id`
- `previous_state_summary`
- `applied_changes`
- `next_action`
- `gate_state`

### `repair-state`

Rescans artifacts and rebuilds state truth.

Recommended output:

- `.b2s/tmp/current-state-update.json`

### `reset-to-phase`

Backs up and rewinds staged state.

Recommended output:

- `.b2s/tmp/current-state-update.json`

### `approve-current-gate`

Marks the active gate as accepted and advances state.

Recommended output:

- `.b2s/tmp/current-gate.json`

### `reject-current-gate`

Rejects the active gate and records blocking state.

Recommended output:

- `.b2s/tmp/current-gate.json`

## Common rule

Dispatcher/orchestrator prompts should gate on written output files, not on
stdout-only summaries.

## Missing-file rule

For every command whose output is required by the orchestrator:

- missing output file -> stop/fail
- malformed output file -> stop/fail
- `overall: fail` -> stop/fail
- `overall: pass` -> proceed
