"""Select the next executable stage action for `.b2s`."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from b2s_engine import workspace


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def _normalize_gate_token(value: str) -> str:
    return value.strip().upper().replace(" ", "_")


def _gate_action_optional(action_id: str, actions_by_id: dict[str, dict[str, Any]]) -> bool:
    for action in actions_by_id.values():
        human_gate = action.get("human_gate") or {}
        gate_id = human_gate.get("gate_id")
        if gate_id and f"gate-{gate_id}" == action_id:
            return not human_gate.get("required", False)
    return False


def evaluate_condition(
    condition: str,
    state: dict[str, Any],
    workspace_root: Any,
    actions_by_id: dict[str, dict[str, Any]],
) -> bool:
    text = condition.strip()
    action_status = state.get("action_status", {})
    optional_requested = set(state.get("optional_artifacts_requested", []))
    triggered_gates = {_normalize_gate_token(item) for item in state.get("quality_gates_triggered", [])}

    if text == "always":
        return True
    if " and " in text:
        return all(
            evaluate_condition(part.strip(), state, workspace_root, actions_by_id)
            for part in text.split(" and ")
        )
    if " or " in text:
        return any(
            evaluate_condition(part.strip(), state, workspace_root, actions_by_id)
            for part in text.split(" or ")
        )
    if text.endswith(" not empty"):
        field = text.replace(" not empty", "").strip()
        return bool(state.get(field))
    if text.endswith(" does not exist"):
        path = text.replace(" does not exist", "").strip()
        return not workspace.artifact_exists(workspace_root, path)
    if " accepted or gate not required" in text:
        action_id = text.replace(" accepted or gate not required", "").strip()
        return action_status.get(action_id) == "accepted" or _gate_action_optional(action_id, actions_by_id)
    if text.endswith(" accepted"):
        action_id = text.replace(" accepted", "").strip()
        return action_status.get(action_id) == "accepted"
    if " >= " in text:
        field, raw_value = [part.strip() for part in text.split(">=", 1)]
        try:
            threshold = int(raw_value)
            value = int(state.get(field, 0) or 0)
        except ValueError:
            return False
        return value >= threshold
    if " in quality_gates_triggered" in text:
        token = text.replace(" in quality_gates_triggered", "").strip()
        return _normalize_gate_token(token) in triggered_gates
    if " in optional_artifacts_requested" in text:
        token = text.replace(" in optional_artifacts_requested", "").strip()
        return token in optional_requested
    if " in [" in text:
        field, raw_values = [part.strip() for part in text.split(" in ", 1)]
        values = raw_values.strip("[]")
        allowed = {item.strip() for item in values.split(",") if item.strip()}
        return str(state.get(field)) in allowed
    if " == true" in text:
        field = text.replace(" == true", "").strip()
        return bool(state.get(field)) or field in optional_requested
    if " == " in text:
        field, expected = [part.strip() for part in text.split("==", 1)]
        return str(state.get(field)) == expected
    return False


def action_is_complete(action_id: str, state: dict[str, Any]) -> bool:
    return state.get("action_status", {}).get(action_id) in workspace.ACTION_STATUSES_COMPLETE


def _required_inputs_present(action: dict[str, Any], workspace_root: Any) -> bool:
    for pattern in action.get("inputs", {}).get("required", []):
        exists, _ = workspace.resolve_input_pattern(workspace_root, pattern)
        if not exists:
            return False
    return True


def _conditions_pass(
    action: dict[str, Any],
    state: dict[str, Any],
    workspace_root: Any,
    actions_by_id: dict[str, dict[str, Any]],
) -> bool:
    return all(
        evaluate_condition(condition, state, workspace_root, actions_by_id)
        for condition in action.get("conditions", [])
    )


def _blocked_by_actions_satisfied(action: dict[str, Any], state: dict[str, Any]) -> bool:
    return all(action_is_complete(action_id, state) for action_id in action.get("blocked_by_action", []))


def _blocked_by_stage_satisfied(
    action: dict[str, Any],
    state: dict[str, Any],
    actions_by_id: dict[str, dict[str, Any]],
    workspace_root: Any = None,
) -> bool:
    required_stages = action.get("blocked_by_stage", [])
    if not required_stages:
        return True
    workflow = workspace.load_workflow_definition(workspace_root)
    stages_by_id = {stage["id"]: stage for stage in workflow["stages"]}
    for stage_id in required_stages:
        stage = stages_by_id.get(stage_id)
        if stage is None:
            continue
        for stage_action_id in stage.get("actions", []):
            stage_action = actions_by_id.get(stage_action_id)
            if stage_action is None:
                continue
            if action_is_complete(stage_action_id, state):
                continue
            # Skip condition-failing actions — same logic as stage_is_complete
            if workspace_root is not None and not _conditions_pass(
                stage_action, state, workspace_root, actions_by_id
            ):
                continue
            return False
    return True


def stage_is_complete(
    stage: dict[str, Any],
    state: dict[str, Any],
    workspace_root: Any,
    actions_by_id: dict[str, dict[str, Any]],
) -> bool:
    # Condition-failing actions are intentionally treated as optional for stage
    # completeness: if an action's conditions are not met, it is assumed it does
    # not apply to this initiative configuration and is skipped.  This means a
    # stage can be complete even when conditional actions were never run.
    for action_id in stage.get("actions", []):
        action = actions_by_id[action_id]
        if action_is_complete(action_id, state):
            continue
        if not _conditions_pass(action, state, workspace_root, actions_by_id):
            continue
        return False
    return True


def _eligible_action(
    action: dict[str, Any],
    state: dict[str, Any],
    workspace_root: Any,
    actions_by_id: dict[str, dict[str, Any]],
) -> bool:
    action_id = action["action_id"]
    if action_id.startswith("gate-"):
        return False
    if action_is_complete(action_id, state):
        return False
    if not _blocked_by_actions_satisfied(action, state):
        return False
    if not _blocked_by_stage_satisfied(action, state, actions_by_id, workspace_root):
        return False
    if not _conditions_pass(action, state, workspace_root, actions_by_id):
        return False
    if not _required_inputs_present(action, workspace_root):
        return False
    return True


def select_next_action(
    workspace_root: Any,
    state: dict[str, Any],
) -> dict[str, Any]:
    workflow = workspace.load_workflow_definition(workspace_root)
    _, actions_by_id = workspace.load_stage_actions(workspace_root)
    stages = workflow["stages"]
    stage_ids = [stage["id"] for stage in stages]
    current_stage = state.get("current_stage") or stage_ids[0]

    if state.get("awaiting_human"):
        return {
            "overall": "fail",
            "selected_action": None,
            "selected_stage": current_stage,
            "reason": None,
            "blocking_reason": state.get("blocked_reason") or "waiting for human gate approval",
            "ready_actions": [],
        }

    start_index = stage_ids.index(current_stage) if current_stage in stage_ids else 0
    index = start_index
    while index < len(stages):
        stage = stages[index]
        for action_id in stage.get("actions", []):
            action = actions_by_id[action_id]
            if _eligible_action(action, state, workspace_root, actions_by_id):
                return {
                    "overall": "pass",
                    "selected_action": action_id,
                    "selected_stage": stage["id"],
                    "reason": "all prerequisites satisfied and required inputs are present",
                    "blocking_reason": None,
                    "ready_actions": [action_id],
                }

        if not stage_is_complete(stage, state, workspace_root, actions_by_id):
            return {
                "overall": "fail",
                "selected_action": None,
                "selected_stage": stage["id"],
                "reason": None,
                "blocking_reason": f"stage `{stage['id']}` is incomplete but no executable action is currently ready",
                "ready_actions": [],
            }

        next_stage_id = None
        for transition in stage.get("next_stages", []):
            if evaluate_condition(transition["condition"], state, workspace_root, actions_by_id):
                next_stage_id = transition["id"]
                break
        if next_stage_id is None:
            return {
                "overall": "pass",
                "selected_action": None,
                "selected_stage": stage["id"],
                "reason": "workflow complete",
                "blocking_reason": None,
                "ready_actions": [],
            }

        index = stage_ids.index(next_stage_id)

    return {
        "overall": "pass",
        "selected_action": None,
        "selected_stage": current_stage,
        "reason": "workflow complete",
        "blocking_reason": None,
        "ready_actions": [],
    }


def run(args: object) -> None:
    workspace_root = workspace.resolve_workspace_root(args.workspace_root)
    state = workspace.load_state(workspace_root)

    issues = workspace.check_state_integrity(workspace_root, state)
    repairable = [i for i in issues if i["issue"] in ("ghost", "missing_artifact")]
    if repairable:
        repaired = workspace.repair_ghost_actions(workspace_root, state, repairable)
        workspace.save_state(workspace_root, state)
        workspace.append_execution_log(
            workspace_root,
            command="next-step",
            overall="pass",
            details={
                "integrity_check": "auto-repaired",
                "repaired_actions": repaired,
                "issues": [i["detail"] for i in repairable],
            },
        )

    result = select_next_action(workspace_root, state)

    state["current_stage"] = result["selected_stage"]
    state["active_action"] = result["selected_action"]
    state["next_action"] = result["selected_action"]
    state["state_validated"] = result["overall"] == "pass"
    state["last_updated"] = _timestamp()
    if result["overall"] == "fail":
        state["blocked_reason"] = result["blocking_reason"]
    else:
        state["blocked_reason"] = None
    workspace.save_state(workspace_root, state)
    workspace.save_json_file(
        workspace.resolve_output_path("next-step", workspace_root, args.output),
        result,
    )
    workspace.append_execution_log(
        workspace_root,
        command="next-step",
        overall=result["overall"],
        action_id=result.get("selected_action"),
        details={
            "selected_stage": result.get("selected_stage"),
            "ready_actions": result.get("ready_actions", []),
            "reason": result.get("reason"),
            "blocking_reason": result.get("blocking_reason"),
        },
    )
