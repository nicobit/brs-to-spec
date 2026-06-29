"""Reset helpers for staged `.b2s`."""

from __future__ import annotations

from datetime import datetime, timezone
import json

from b2s_engine import workspace


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def run(args: object) -> None:
    workspace_root = workspace.resolve_workspace_root(args.workspace_root)
    state = workspace.load_state(workspace_root)
    workflow = workspace.load_workflow_definition(workspace_root)
    _, actions_by_id = workspace.load_stage_actions(workspace_root)
    stages = workflow["stages"]
    stage_ids = [stage["id"] for stage in stages]
    target_stage = getattr(args, "stage_id", None) or stage_ids[0]
    if target_stage not in stage_ids:
        raise ValueError(f"Unknown stage ID: {target_stage}")

    backup_path = workspace.backups_dir(workspace_root) / f"workflow-state-{_timestamp().replace(':', '-')}.json"
    backup_path.write_text(json.dumps(state, indent=2), encoding="utf-8")

    target_index = stage_ids.index(target_stage)
    stage_actions_to_reset = set()
    for stage in stages[target_index:]:
        stage_actions_to_reset.update(stage.get("actions", []))

    for action_id in stage_actions_to_reset:
        action = actions_by_id[action_id]
        for artifact_path in workspace.action_output_paths(action):
            state.get("artifact_status", {}).pop(artifact_path, None)
        state.get("action_status", {}).pop(action_id, None)

    first_stage_actions = stages[target_index]["actions"]
    next_action = None
    for action_id in first_stage_actions:
        if not action_id.startswith("gate-"):
            next_action = action_id
            break

    state["current_stage"] = target_stage
    state["active_action"] = None
    state["next_action"] = next_action
    state["awaiting_human"] = False
    state["current_gate"] = None
    state["blocked_reason"] = None
    state["state_validated"] = True
    state["last_updated"] = _timestamp()
    if target_stage == "0-routing":
        state["last_completed_action"] = None
        state["delivery_mode"] = None
        state["execution_mode"] = None
        state["quality_gates_triggered"] = []
    workspace.advance_lifecycle_phase(state, workspace.LIFECYCLE_IDLE)
    workspace.save_state(workspace_root, state)
    workspace.save_json_file(
        workspace.resolve_output_path("reset-to-phase", workspace_root, args.output),
        {
            "overall": "pass",
            "action_id": None,
            "previous_state_summary": {"current_stage": None, "next_action": None},
            "applied_changes": {
                "current_stage": target_stage,
                "backup_path": backup_path.relative_to(workspace_root).as_posix(),
            },
            "next_action": next_action,
            "gate_state": None,
        },
    )
    workspace.append_execution_log(
        workspace_root,
        command="reset-to-phase",
        overall="pass",
        details={
            "target_stage": target_stage,
            "next_action": next_action,
            "backup_path": backup_path.relative_to(workspace_root).as_posix(),
        },
    )
