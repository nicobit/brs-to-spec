# State And Gate Model

## Purpose

This document defines the compact `.b2s` state contract that later prompts must
implement consistently.

## Required `workflow-state.json` fields

- `initiative_id`
- `current_stage`
- `delivery_mode`
- `execution_mode`
- `project_type`
- `last_completed_action`
- `next_action`
- `active_action`
- `artifact_status`
- `quality_gates_triggered`
- `optional_artifacts_requested`
- `open_decisions`
- `blocking_decisions`
- `awaiting_human`
- `current_gate`
- `blocked_reason`
- `state_validated`
- `last_updated`

## Recommended gate fields

When a human gate is active:

- `awaiting_human: true`
- `current_gate.gate_id`
- `current_gate.action_id`
- `current_gate.artifact_path`
- `current_gate.status`
- `current_gate.owner`

Example:

```json
{
  "awaiting_human": true,
  "current_gate": {
    "gate_id": "business-intake-review",
    "action_id": "create-business-intake-summary",
    "artifact_path": "business-intake/business-intake-summary.md",
    "status": "waiting_human",
    "owner": "product-owner"
  },
  "blocked_reason": "waiting for product owner review"
}
```

## Artifact status values

Recommended allowed values:

- `missing`
- `draft`
- `ai_validated`
- `accepted`
- `failed`
- `stale`

## Active action rule

For the first implementation:

- `active_action` is either `null` or exactly one action ID
- parallel active actions are out of scope

## Gate transitions

- action passes artifact generation -> `ai_validated`
- if no human gate is required -> next action may be selected
- if human gate is required -> `awaiting_human: true`
- gate approved -> artifact becomes `accepted`
- gate rejected -> artifact may remain `draft` or become `failed`, and blocking state is recorded
