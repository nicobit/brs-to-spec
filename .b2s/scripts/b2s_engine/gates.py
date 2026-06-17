"""Human gate helpers for staged `.b2s`."""

from __future__ import annotations

from datetime import datetime, timezone

from b2s_engine import next_step, workspace


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def _gate_output(
    gate_id: str,
    artifact_path: str | None,
    decision: str,
    blocking_reason: str | None,
    note: str | None,
) -> dict:
    payload = {
        "overall": "pass",
        "gate_id": gate_id,
        "artifact_path": artifact_path,
        "decision": decision,
        "blocking_reason": blocking_reason,
    }
    if note:
        payload["note"] = note
    return payload


def approve_current_gate(args: object) -> None:
    workspace_root = workspace.resolve_workspace_root(args.workspace_root)
    state = workspace.load_state(workspace_root)
    gate = state.get("current_gate")
    if not gate:
        raise ValueError("No current gate is waiting for approval.")

    artifact_path = gate.get("artifact_path")
    gate_action_id = gate["action_id"]
    source_action_id = gate.get("source_action_id")
    state["awaiting_human"] = False
    state["current_gate"] = None
    state["blocked_reason"] = None
    state["last_completed_action"] = gate_action_id
    state["action_status"][gate_action_id] = "accepted"
    if source_action_id:
        state["action_status"][source_action_id] = "accepted"
    if artifact_path:
        state["artifact_status"][artifact_path] = "accepted"
    state["active_action"] = None
    state["next_action"] = None
    state["last_updated"] = _timestamp()

    preview = next_step.select_next_action(workspace_root, state)
    state["next_action"] = preview.get("selected_action")
    workspace.save_state(workspace_root, state)
    workspace.save_json_file(
        workspace.resolve_output_path("approve-current-gate", workspace_root, args.output),
        _gate_output(gate["gate_id"], artifact_path, "approved", None, getattr(args, "reason", None)),
    )
    workspace.append_execution_log(
        workspace_root,
        command="approve-current-gate",
        overall="pass",
        action_id=source_action_id or gate_action_id,
        details={
            "gate_id": gate["gate_id"],
            "artifact_path": artifact_path,
            "decision": "approved",
            "reason": getattr(args, "reason", None),
            "next_action": state.get("next_action"),
        },
    )

def retry_action(args: object) -> None:
    workspace_root = workspace.resolve_workspace_root(args.workspace_root)
    state = workspace.load_state(workspace_root)
    _, actions_by_id = workspace.load_stage_actions()

    action_id = getattr(args, "action_id", None)
    if not action_id:
        raise ValueError("--action-id is required for retry-action.")

    if action_id not in actions_by_id:
        raise ValueError(f"Unknown action ID: {action_id}")

    current_action_status = state.get("action_status", {}).get(action_id)
    if current_action_status != "failed":
        raise ValueError(
            f"retry-action only reopens failed actions. "
            f"'{action_id}' has status '{current_action_status}'."
        )

    action = actions_by_id[action_id]
    gate_action_id = f"gate-{action.get('human_gate', {}).get('gate_id', '')}"
    if gate_action_id not in actions_by_id:
        gate_action_id = None

    previous_state = {
        "current_stage": state.get("current_stage"),
        "next_action": state.get("next_action"),
    }

    state["action_status"][action_id] = None
    state["action_status"].pop(action_id, None)
    if gate_action_id:
        state["action_status"].pop(gate_action_id, None)

    for artifact_path in workspace.action_output_paths(action):
        state["artifact_status"].pop(artifact_path, None)

    state["awaiting_human"] = False
    state["current_gate"] = None
    state["blocked_reason"] = None
    state["active_action"] = action_id
    state["next_action"] = action_id
    state["last_updated"] = _timestamp()
    state["state_validated"] = True

    workspace.save_state(workspace_root, state)
    workspace.save_json_file(
        workspace.resolve_output_path("retry-action", workspace_root, args.output),
        {
            "overall": "pass",
            "action_id": action_id,
            "previous_state_summary": previous_state,
            "applied_changes": {
                "action_reopened": action_id,
                "gate_cleared": gate_action_id,
                "artifacts_cleared": workspace.action_output_paths(action),
                "next_action": action_id,
            },
            "next_action": action_id,
            "gate_state": None,
        },
    )
    workspace.append_execution_log(
        workspace_root,
        command="retry-action",
        overall="pass",
        action_id=action_id,
        details={
            "gate_cleared": gate_action_id,
            "artifacts_cleared": workspace.action_output_paths(action),
            "next_action": action_id,
        },
    )


def rerun_last_action(args: object) -> None:
    workspace_root = workspace.resolve_workspace_root(args.workspace_root)
    state = workspace.load_state(workspace_root)
    _, actions_by_id = workspace.load_stage_actions()

    action_id = state.get("last_completed_action")
    if not action_id:
        raise ValueError("No last_completed_action recorded in workflow state.")
    if action_id not in actions_by_id:
        raise ValueError(f"Unknown action ID: {action_id}")

    disallowed_statuses = {"accepted"}
    current_status = state.get("action_status", {}).get(action_id)
    if current_status in disallowed_statuses:
        raise ValueError(
            f"rerun-last-action cannot rerun '{action_id}' because it is '{current_status}'. "
            f"Human-accepted actions must be retried via reject-current-gate + retry-action."
        )

    action = actions_by_id[action_id]
    gate_action_id = None
    human_gate = action.get("human_gate") or {}
    if human_gate.get("required"):
        candidate = f"gate-{human_gate.get('gate_id', '')}"
        if candidate in actions_by_id:
            gate_action_id = candidate

    previous_state = {
        "current_stage": state.get("current_stage"),
        "last_completed_action": action_id,
        "action_status": current_status,
    }

    state["action_status"].pop(action_id, None)
    if gate_action_id:
        state["action_status"].pop(gate_action_id, None)

    for artifact_path in workspace.action_output_paths(action):
        state["artifact_status"].pop(artifact_path, None)

    state["awaiting_human"] = False
    state["current_gate"] = None
    state["blocked_reason"] = None
    state["active_action"] = action_id
    state["next_action"] = action_id
    state["last_updated"] = _timestamp()
    state["state_validated"] = True

    workspace.save_state(workspace_root, state)
    workspace.save_json_file(
        workspace.resolve_output_path("rerun-last-action", workspace_root, args.output),
        {
            "overall": "pass",
            "action_id": action_id,
            "previous_state_summary": previous_state,
            "applied_changes": {
                "action_reopened": action_id,
                "gate_cleared": gate_action_id,
                "artifacts_cleared": workspace.action_output_paths(action),
                "next_action": action_id,
            },
            "next_action": action_id,
            "gate_state": None,
        },
    )
    workspace.append_execution_log(
        workspace_root,
        command="rerun-last-action",
        overall="pass",
        action_id=action_id,
        details={
            "gate_cleared": gate_action_id,
            "artifacts_cleared": workspace.action_output_paths(action),
            "next_action": action_id,
        },
    )


def reject_current_gate(args: object) -> None:
    workspace_root = workspace.resolve_workspace_root(args.workspace_root)
    state = workspace.load_state(workspace_root)
    gate = state.get("current_gate")
    if not gate:
        raise ValueError("No current gate is waiting for rejection.")

    artifact_path = gate.get("artifact_path")
    gate_action_id = gate["action_id"]
    source_action_id = gate.get("source_action_id")
    rejection_reason = getattr(args, "reason", None) or "human review rejected the current gate"
    state["awaiting_human"] = False
    state["current_gate"] = None
    state["blocked_reason"] = rejection_reason
    state["last_completed_action"] = gate_action_id
    state["action_status"][gate_action_id] = "failed"
    if source_action_id:
        state["action_status"][source_action_id] = "failed"
    if artifact_path:
        state["artifact_status"][artifact_path] = "failed"
    state["active_action"] = None
    state["next_action"] = None
    state["last_updated"] = _timestamp()
    workspace.save_state(workspace_root, state)
    workspace.save_json_file(
        workspace.resolve_output_path("reject-current-gate", workspace_root, args.output),
        _gate_output(gate["gate_id"], artifact_path, "rejected", rejection_reason, rejection_reason),
    )
    workspace.append_execution_log(
        workspace_root,
        command="reject-current-gate",
        overall="fail",
        action_id=source_action_id or gate_action_id,
        details={
            "gate_id": gate["gate_id"],
            "artifact_path": artifact_path,
            "decision": "rejected",
            "reason": rejection_reason,
        },
    )
