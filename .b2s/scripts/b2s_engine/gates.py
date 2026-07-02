"""Human gate helpers for staged `.b2s`."""

from __future__ import annotations

from datetime import datetime, timezone

from b2s_engine import dynamic_state, next_step, workspace


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


def _items_for_action(action: dict, state: dict, workspace_root) -> list[str]:
    wave_idx = workspace.current_wave_index(state)
    wave_items = workspace.items_for_wave(workspace_root, wave_idx)
    if wave_items:
        return wave_items
    return workspace.extract_items_from_source(
        workspace_root,
        action["item_source"],
        action["item_pattern"],
    )


def _apply_gate_acceptance_to_source_action(
    workspace_root,
    state: dict,
    source_action_id: str | None,
    actions_by_id: dict,
    current_item: str | None,
) -> None:
    if not source_action_id:
        return
    action = actions_by_id.get(source_action_id)
    if not action:
        state["action_status"][source_action_id] = "accepted"
        return

    accepted_status = action["status_model"]["artifact_on_gate_accept"]
    if action.get("iteration_mode") == "per_item":
        if current_item:
            item_key = f"{source_action_id}#{current_item}"
            state.setdefault("action_item_status", {})[item_key] = accepted_status
        items = _items_for_action(action, state, workspace_root)
        all_done = all(
            state.get("action_item_status", {}).get(f"{source_action_id}#{item}") in workspace.ACTION_STATUSES_COMPLETE
            for item in items
        )
        state["action_status"][source_action_id] = accepted_status if all_done else workspace.ACTION_STATUS_IN_PROGRESS
        return

    state["action_status"][source_action_id] = accepted_status


def _advance_wave_if_needed(
    workspace_root,
    state: dict,
    gate_action_id: str,
    actions_by_id: dict,
) -> dict | None:
    """After a gate approval, check if this gate guards a wave-iterated stage.

    If the current wave is not the last, advance to the next wave and reset
    the stage's actions so they can re-execute. Returns a summary dict or None.
    """
    wave_idx = workspace.current_wave_index(state)
    wave_count = workspace.total_waves(workspace_root)
    if wave_count <= 0 or wave_idx >= wave_count - 1:
        return None

    gate_action = actions_by_id.get(gate_action_id, {})
    gate_stage_id = gate_action.get("stage_id")
    if not gate_stage_id:
        return None

    workflow = workspace.load_workflow_definition(workspace_root)
    stage = None
    for s in workflow.get("stages", []):
        if s["id"] == gate_stage_id:
            stage = s
            break
    if stage is None:
        return None

    has_per_item = any(
        actions_by_id.get(aid, {}).get("iteration_mode") == "per_item"
        for aid in stage.get("actions", [])
    )
    if not has_per_item:
        return None

    next_wave = wave_idx + 1
    state["current_wave"] = next_wave

    # Only reset per-item actions that need to re-run for the next wave.
    # Non-per-item actions (validate-fr-coverage, gate-epic-review) run once
    # after all waves complete and must not be reset by wave advancement.
    reset_actions = []
    for aid in stage.get("actions", []):
        action_def = actions_by_id.get(aid, {})
        if action_def.get("iteration_mode") != "per_item":
            continue
        if aid in state.get("action_status", {}):
            state["action_status"].pop(aid, None)
            reset_actions.append(aid)
        for ap in workspace.action_output_paths(action_def):
            state["artifact_status"].pop(ap, None)

    return {
        "advanced_from_wave": wave_idx,
        "advanced_to_wave": next_wave,
        "total_waves": wave_count,
        "reset_actions": reset_actions,
        "stage_id": gate_stage_id,
    }


def approve_current_gate(args: object) -> None:
    workspace_root = workspace.resolve_workspace_root(args.workspace_root)
    state = workspace.load_state(workspace_root)
    _, actions_by_id = workspace.load_stage_actions(workspace_root)
    gate = state.get("current_gate")
    if not gate:
        raise ValueError("No current gate is waiting for approval.")

    artifact_path = gate.get("artifact_path")
    gate_action_id = gate["action_id"]
    source_action_id = gate.get("source_action_id")
    rerun_action = gate.get("rerun_action")
    gate_current_item = gate.get("current_item") or state.get("current_item")
    state["awaiting_human"] = False
    state["current_gate"] = None
    state["blocked_reason"] = None
    state["last_completed_action"] = gate_action_id
    state["action_status"][gate_action_id] = "accepted"
    _apply_gate_acceptance_to_source_action(
        workspace_root,
        state,
        source_action_id,
        actions_by_id,
        gate_current_item,
    )
    if artifact_path:
        state["artifact_status"][artifact_path] = "accepted"
    state["active_action"] = None
    state["next_action"] = None
    state["last_updated"] = _timestamp()

    wave_advance = _advance_wave_if_needed(
        workspace_root, state, gate_action_id, actions_by_id,
    )

    if rerun_action and rerun_action in actions_by_id:
        action = actions_by_id[rerun_action]
        state["action_status"].pop(rerun_action, None)
        if gate_current_item:
            state["current_item"] = gate_current_item
            state.get("action_item_status", {}).pop(f"{rerun_action}#{gate_current_item}", None)
        for artifact_path in workspace.action_output_paths(action):
            state["artifact_status"].pop(artifact_path, None)
        state["active_action"] = rerun_action
        state["next_action"] = rerun_action
        workspace.advance_lifecycle_phase(state, workspace.LIFECYCLE_IDLE)
        workspace.save_state(workspace_root, state)
        gate_result = _gate_output(gate["gate_id"], artifact_path, "approved", None, getattr(args, "reason", None))
        gate_result["next_action"] = rerun_action
        workspace.save_json_file(
            workspace.resolve_output_path("approve-current-gate", workspace_root, args.output),
            gate_result,
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
                "next_action": rerun_action,
                "current_item": gate_current_item,
            },
        )
        return

    if dynamic_state.should_return_to_dynamic_assessment(
        state,
        source_action_id,
        awaiting_human=False,
        rerun_action=rerun_action,
    ):
        dynamic_state.reset_dynamic_orchestration_cycle(state, actions_by_id)
        state["current_stage"] = dynamic_state.dynamic_loop_start_stage_id(actions_by_id)
        state["dynamic_stop_reason"] = None

    preview = next_step.select_next_action(workspace_root, state)
    state["next_action"] = preview.get("selected_action")
    workspace.advance_lifecycle_phase(state, workspace.LIFECYCLE_IDLE)
    workspace.save_state(workspace_root, state)
    gate_result = _gate_output(gate["gate_id"], artifact_path, "approved", None, getattr(args, "reason", None))
    if wave_advance:
        gate_result["wave_advance"] = wave_advance
    workspace.save_json_file(
        workspace.resolve_output_path("approve-current-gate", workspace_root, args.output),
        gate_result,
    )
    log_details: dict = {
        "gate_id": gate["gate_id"],
        "artifact_path": artifact_path,
        "decision": "approved",
        "reason": getattr(args, "reason", None),
        "next_action": state.get("next_action"),
    }
    if wave_advance:
        log_details["wave_advance"] = wave_advance
    workspace.append_execution_log(
        workspace_root,
        command="approve-current-gate",
        overall="pass",
        action_id=source_action_id or gate_action_id,
        details=log_details,
    )


def retry_action(args: object) -> None:
    workspace_root = workspace.resolve_workspace_root(args.workspace_root)
    state = workspace.load_state(workspace_root)
    _, actions_by_id = workspace.load_stage_actions(workspace_root)

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
    workspace.advance_lifecycle_phase(state, workspace.LIFECYCLE_IDLE)

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
    _, actions_by_id = workspace.load_stage_actions(workspace_root)

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
    workspace.advance_lifecycle_phase(state, workspace.LIFECYCLE_IDLE)

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


def run_action(args: object) -> None:
    """Clear a named action and set it as next_action so the skill re-executes it."""
    workspace_root = workspace.resolve_workspace_root(args.workspace_root)
    state = workspace.load_state(workspace_root)
    _, actions_by_id = workspace.load_stage_actions(workspace_root)

    action_id = getattr(args, "action_id", None)
    if not action_id:
        raise ValueError("--action-id is required for run-action.")
    if action_id not in actions_by_id:
        raise ValueError(f"Unknown action ID: {action_id}")

    current_status = state.get("action_status", {}).get(action_id, "not_run")
    if current_status == "accepted":
        raise ValueError(
            f"run-action cannot rerun '{action_id}' because it is 'accepted' (human-approved). "
            f"Use reject-current-gate first, then run-action."
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
        "next_action": state.get("next_action"),
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
    workspace.advance_lifecycle_phase(state, workspace.LIFECYCLE_IDLE)

    workspace.save_state(workspace_root, state)
    workspace.save_json_file(
        workspace.resolve_output_path("run-action", workspace_root, args.output),
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
        command="run-action",
        overall="pass",
        action_id=action_id,
        details={
            "previous_status": current_status,
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
    workspace.advance_lifecycle_phase(state, workspace.LIFECYCLE_IDLE)
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
