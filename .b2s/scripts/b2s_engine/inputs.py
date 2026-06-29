"""Input resolution for staged `.b2s` actions."""

from __future__ import annotations

from typing import Any

from b2s_engine import coverage, workspace


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


COMPUTED_INPUT_GENERATORS: dict[str, Any] = {
    "coverage": lambda ws, _item: (
        coverage.compute_coverage(ws),
        "computed-coverage.json",
    ),
    "epic_context": lambda ws, item: (
        _compute_epic_context(ws, item),
        "computed-epic-context.json",
    ),
    "epic_clarifications": lambda ws, item: (
        _compute_epic_clarifications(ws, item),
        "computed-epic-clarifications.json",
    ),
    "solution_design_clarifications": lambda ws, _item: (
        _compute_solution_design_clarifications(ws),
        "computed-solution-design-clarifications.json",
    ),
}


def _compute_epic_context(workspace_root, current_item: str | None) -> dict[str, Any]:
    """Extract only the requirements, skeleton section, and system mappings
    relevant to the current epic. Reduces input tokens from ~29k to ~8-10k."""
    from b2s_engine import epic_context
    return epic_context.compute_epic_context(workspace_root, current_item)


def _compute_epic_clarifications(workspace_root, current_item: str | None) -> dict[str, Any]:
    relative_path = f"input/clarifications/{current_item}.yaml" if current_item else None
    if not current_item or not relative_path:
        return {
            "current_item": current_item,
            "exists": False,
            "path": None,
            "data": None,
        }

    clarification_path = workspace_root / relative_path
    if not clarification_path.exists():
        return {
            "current_item": current_item,
            "exists": False,
            "path": relative_path,
            "data": None,
        }

    return {
        "current_item": current_item,
        "exists": True,
        "path": relative_path,
        "data": workspace.load_yaml_file(clarification_path),
    }


def _compute_solution_design_clarifications(workspace_root) -> dict[str, Any]:
    relative_path = "input/clarifications/solution-design.yaml"
    clarification_path = workspace_root / relative_path
    if not clarification_path.exists():
        return {
            "exists": False,
            "path": relative_path,
            "data": None,
        }

    return {
        "exists": True,
        "path": relative_path,
        "data": workspace.load_yaml_file(clarification_path),
    }


def generate_computed_inputs(
    action: dict[str, Any],
    workspace_root,
    current_item: str | None = None,
) -> list[str]:
    """Generate computed inputs declared in the action's ``computed_inputs`` list.

    Returns a list of workspace-relative paths to the generated files.
    Both ``run()`` (the CLI entry point) and ``dispatch._collect_inputs()``
    call this so that computed data is always produced regardless of code path.
    """
    computed: list[str] = []
    for key in action.get("computed_inputs", []):
        generator = COMPUTED_INPUT_GENERATORS.get(key)
        if generator is None:
            continue
        data, filename = generator(workspace_root, current_item)
        out_path = workspace.tmp_dir(workspace_root) / filename
        workspace.save_json_file(out_path, data)
        computed.append(out_path.relative_to(workspace_root).as_posix())
    return computed


def collect_action_inputs(action: dict[str, Any], workspace_root, current_item: str | None = None) -> dict[str, Any]:
    """Resolve business inputs and policy inputs for an action."""
    required_inputs = _resolve_patterns(workspace_root, list(action.get("inputs", {}).get("required", [])))
    optional_inputs = _resolve_patterns(workspace_root, list(action.get("inputs", {}).get("optional", [])))
    policy_inputs = _resolve_policy_patterns(list(action.get("policy_refs", [])))

    missing_required = [entry["path"] for entry in required_inputs if not entry["exists"]]
    missing_policies = [entry["path"] for entry in policy_inputs if not entry["exists"]]

    artifact_template_ref = action.get("artifact_template_ref")
    item_folder = workspace.resolve_item_folder(workspace_root, current_item)
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
        "item_folder": item_folder,
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

    phase_error = workspace.check_lifecycle_phase(state, workspace.LIFECYCLE_DISPATCHED, "collect-inputs")
    if phase_error:
        raise RuntimeError(phase_error)

    _, actions_by_id = workspace.load_stage_actions(workspace_root)
    action = actions_by_id[action_id]
    current_item = state.get("current_item")
    collected = collect_action_inputs(action, workspace_root, current_item=current_item)
    computed_inputs = generate_computed_inputs(action, workspace_root, current_item=current_item)

    workspace.advance_lifecycle_phase(state, workspace.LIFECYCLE_INPUTS_COLLECTED)
    workspace.save_state(workspace_root, state)

    result = {
        "overall": collected["overall"],
        "action_id": action_id,
        "required_inputs": collected["required_inputs"],
        "optional_inputs": collected["optional_inputs"],
        "policy_inputs": collected["policy_inputs"],
        "missing_required_inputs": collected["missing_required_inputs"],
        "missing_policy_inputs": collected["missing_policy_inputs"],
        "prompt_placeholders": collected["prompt_placeholders"],
        "computed_inputs": computed_inputs,
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
