# Output File Contracts

## Purpose

These contracts define the machine-readable files that the `.b2s` orchestrator
must consume. Later prompts must implement these shapes instead of inventing
their own.

## `next-step.json`

```json
{
  "overall": "pass",
  "selected_action": "create-business-intake-summary",
  "selected_stage": "2-business-intake",
  "reason": "routing complete and required inputs present",
  "blocking_reason": null,
  "ready_actions": ["create-business-intake-summary"]
}
```

## `current-inputs.json`

```json
{
  "overall": "pass",
  "action_id": "create-business-intake-summary",
  "required_inputs": [
    {"path": "input/brs.md", "exists": true}
  ],
  "optional_inputs": [],
  "missing_required_inputs": [],
  "read_evidence": []
}
```

## `current-validation.yaml`

```yaml
overall: pass
action_id: create-business-intake-summary
artifact_path: business-intake/business-intake-summary.md
checks:
  - name: file_exists
    result: pass
    detail: artifact exists
failures: []
```

## `current-state-update.json`

```json
{
  "overall": "pass",
  "action_id": "create-business-intake-summary",
  "previous_state_summary": {
    "current_stage": "0-routing",
    "next_action": "create-business-intake-summary"
  },
  "applied_changes": {
    "current_stage": "2-business-intake",
    "artifact_status": {
      "business-intake/business-intake-summary.md": "ai_validated"
    }
  },
  "next_action": "create-requirements",
  "gate_state": null
}
```

## `current-gate.json`

```json
{
  "overall": "pass",
  "gate_id": "business-intake-review",
  "artifact_path": "business-intake/business-intake-summary.md",
  "decision": "approved",
  "blocking_reason": null
}
```

## Rule

These are minimum fields, not illustrative prose examples.

Any implementation prompt that changes these shapes must update this file first.
