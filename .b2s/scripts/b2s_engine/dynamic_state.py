"""Helpers for additive `b2s-dynamic` state management."""

from __future__ import annotations

from copy import deepcopy
from typing import Any


DYNAMIC_STATE_DEFAULTS: dict[str, Any] = {
    "dynamic_goal": None,
    "dynamic_macro_phase": None,
    "dynamic_gap_backlog": [],
    "dynamic_focus_area": None,
    "dynamic_iteration_count": 0,
    "dynamic_last_assessment": None,
    "dynamic_last_selected_action": None,
    "dynamic_stop_reason": None,
    "dynamic_confidence": None,
    "dynamic_repeat_gap_count": 0,
}

DYNAMIC_ORCHESTRATOR_ACTION_IDS = {
    "orchestrate-dynamic-iteration",
    "finalize-dynamic-initiative",
}


def ensure_dynamic_state_defaults(state: dict[str, Any]) -> dict[str, Any]:
    """Populate additive dynamic state fields when missing.

    Safe for all workflow types because the fields are additive and ignored
    unless `workflow_type == "b2s-dynamic"`.
    """
    for key, value in DYNAMIC_STATE_DEFAULTS.items():
        if key not in state:
            state[key] = deepcopy(value)
    return state


def is_dynamic_workflow(state: dict[str, Any]) -> bool:
    return state.get("workflow_type") == "b2s-dynamic"


def is_dynamic_orchestrator_action(action_id: str | None) -> bool:
    return action_id in DYNAMIC_ORCHESTRATOR_ACTION_IDS


def should_return_to_dynamic_assessment(
    state: dict[str, Any],
    action_id: str | None,
    *,
    awaiting_human: bool = False,
    rerun_action: str | None = None,
) -> bool:
    if not is_dynamic_workflow(state):
        return False
    if awaiting_human or rerun_action:
        return False
    return not is_dynamic_orchestrator_action(action_id)


def reset_dynamic_orchestration_cycle(
    state: dict[str, Any],
    actions_by_id: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Clear dynamic orchestrator action and artifact statuses for a new loop cycle."""
    for action_id in DYNAMIC_ORCHESTRATOR_ACTION_IDS:
        state.get("action_status", {}).pop(action_id, None)
        if not actions_by_id:
            continue
        action = actions_by_id.get(action_id) or {}
        outputs = action.get("outputs", {})
        primary = outputs.get("primary")
        if primary:
            state.get("artifact_status", {}).pop(primary, None)
        for artifact_path in outputs.get("secondary", []):
            state.get("artifact_status", {}).pop(artifact_path, None)
    return state


def dynamic_loop_start_stage_id(
    actions_by_id: dict[str, dict[str, Any]] | None = None,
) -> str:
    """Return the correct loop-entry stage for the active dynamic workflow flavor."""
    return "0-dynamic-loop"


def dynamic_state_snapshot(state: dict[str, Any]) -> dict[str, Any]:
    """Return only the dynamic subset of workflow state."""
    ensured = ensure_dynamic_state_defaults(dict(state))
    return {key: deepcopy(ensured[key]) for key in DYNAMIC_STATE_DEFAULTS}


def update_dynamic_state(state: dict[str, Any], **changes: Any) -> dict[str, Any]:
    """Apply updates to the dynamic subset of state only."""
    ensure_dynamic_state_defaults(state)
    for key, value in changes.items():
        if key not in DYNAMIC_STATE_DEFAULTS:
            raise KeyError(f"Unknown dynamic state field: {key}")
        state[key] = value
    return state
