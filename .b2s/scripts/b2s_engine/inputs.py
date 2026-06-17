"""Input resolution for staged `.b2s` actions."""

from __future__ import annotations

from b2s_engine import workspace


def run(args: object) -> None:
    workspace_root = workspace.resolve_workspace_root(args.workspace_root)
    state = workspace.load_state(workspace_root)
    action_id = workspace.read_action_id_from_state_or_args(state, getattr(args, "action_id", None))
    _, actions_by_id = workspace.load_stage_actions()
    action = actions_by_id[action_id]

    required_inputs = []
    optional_inputs = []
    missing_required = []

    for pattern in action.get("inputs", {}).get("required", []):
        exists, matches = workspace.resolve_input_pattern(workspace_root, pattern)
        entry = {"path": pattern, "exists": exists, "matches": matches}
        required_inputs.append(entry)
        if not exists:
            missing_required.append(pattern)

    for pattern in action.get("inputs", {}).get("optional", []):
        exists, matches = workspace.resolve_input_pattern(workspace_root, pattern)
        optional_inputs.append({"path": pattern, "exists": exists, "matches": matches})

    result = {
        "overall": "pass" if not missing_required else "fail",
        "action_id": action_id,
        "required_inputs": required_inputs,
        "optional_inputs": optional_inputs,
        "missing_required_inputs": missing_required,
        "read_evidence": [],
    }
    workspace.save_json_file(
        workspace.resolve_output_path("collect-inputs", workspace_root, args.output),
        result,
    )
    workspace.append_execution_log(
        workspace_root,
        command="collect-inputs",
        overall=result["overall"],
        action_id=action_id,
        details={
            "missing_required_inputs": missing_required,
            "required_input_count": len(required_inputs),
            "optional_input_count": len(optional_inputs),
        },
    )
