"""Input resolution for staged `.b2s` actions."""

from __future__ import annotations

from typing import Any

from b2s_engine import workspace


def _flatten_resolved_paths(entries: list[dict[str, object]]) -> list[str]:
    resolved: list[str] = []
    for entry in entries:
        for match in entry.get("matches", []):
            if isinstance(match, str):
                resolved.append(match)
    return resolved


def _resolve_patterns(workspace_root, patterns: list[str]) -> list[dict[str, object]]:
    resolved = []
    for pattern in patterns:
        exists, matches = workspace.resolve_input_pattern(workspace_root, pattern)
        resolved.append({"path": pattern, "exists": exists, "matches": matches})
    return resolved


def _resolve_policy_patterns(patterns: list[str]) -> list[dict[str, object]]:
    resolved = []
    for pattern in patterns:
        exists, matches = workspace.resolve_policy_reference(pattern)
        resolved.append({"path": pattern, "exists": exists, "matches": matches})
    return resolved


def collect_action_inputs(action: dict[str, Any], workspace_root, current_item: str | None = None) -> dict[str, Any]:
    """Resolve business inputs and policy inputs for an action."""
    required_inputs = _resolve_patterns(workspace_root, list(action.get("inputs", {}).get("required", [])))
    optional_inputs = _resolve_patterns(workspace_root, list(action.get("inputs", {}).get("optional", [])))
    policy_inputs = _resolve_policy_patterns(list(action.get("policy_refs", [])))

    missing_required = [entry["path"] for entry in required_inputs if not entry["exists"]]
    missing_policies = [entry["path"] for entry in policy_inputs if not entry["exists"]]

    artifact_template_ref = action.get("artifact_template_ref")
    prompt_placeholders = {
        "required_inputs": [entry["path"] for entry in required_inputs],
        "optional_inputs": [entry["path"] for entry in optional_inputs],
        "resolved_required_inputs": _flatten_resolved_paths(required_inputs),
        "resolved_optional_inputs": _flatten_resolved_paths(optional_inputs),
        "resolved_policy_inputs": _flatten_resolved_paths(policy_inputs),
        "primary_output": action.get("outputs", {}).get("primary"),
        "secondary_outputs": list(action.get("outputs", {}).get("secondary", [])),
        "artifact_template_ref": artifact_template_ref,
        "prompt_family": action.get("prompt_family"),
        "template_mode": action.get("template_mode"),
        "current_item": current_item,
    }

    return {
        "required_inputs": required_inputs,
        "optional_inputs": optional_inputs,
        "policy_inputs": policy_inputs,
        "missing_required_inputs": missing_required,
        "missing_policy_inputs": missing_policies,
        "overall": "pass" if not missing_required and not missing_policies else "fail",
        "prompt_placeholders": prompt_placeholders,
    }


def run(args: object) -> None:
    workspace_root = workspace.resolve_workspace_root(args.workspace_root)
    state = workspace.load_state(workspace_root)
    action_id = workspace.read_action_id_from_state_or_args(state, getattr(args, "action_id", None))
    _, actions_by_id = workspace.load_stage_actions(workspace_root)
    action = actions_by_id[action_id]
    collected = collect_action_inputs(action, workspace_root)

    result = {
        "overall": collected["overall"],
        "action_id": action_id,
        "required_inputs": collected["required_inputs"],
        "optional_inputs": collected["optional_inputs"],
        "policy_inputs": collected["policy_inputs"],
        "missing_required_inputs": collected["missing_required_inputs"],
        "missing_policy_inputs": collected["missing_policy_inputs"],
        "prompt_placeholders": collected["prompt_placeholders"],
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
            "missing_required_inputs": collected["missing_required_inputs"],
            "missing_policy_inputs": collected["missing_policy_inputs"],
            "required_input_count": len(collected["required_inputs"]),
            "optional_input_count": len(collected["optional_inputs"]),
            "policy_input_count": len(collected["policy_inputs"]),
        },
    )
