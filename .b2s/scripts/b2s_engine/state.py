"""Workflow state helpers for staged `.b2s`."""

from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone
import re
from typing import Callable

from b2s_engine import dynamic_state, next_step, workspace


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def _markdown_row_value(text: str, label: str) -> str | None:
    pattern = re.compile(rf"(?mi)^\|\s*{re.escape(label)}\s*\|\s*([^|]+?)\s*\|")
    match = pattern.search(text)
    return match.group(1).strip() if match else None


def _parse_routing_fields(workspace_root, state: dict) -> None:
    path = workspace_root / "routing" / "routing-decision.md"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    delivery_mode = _markdown_row_value(text, "Delivery mode")
    execution_mode = _markdown_row_value(text, "Execution mode")
    if delivery_mode and delivery_mode in {"OpenSpec", "Standalone", "FastPath", "BusinessCopilot"}:
        state["delivery_mode"] = delivery_mode
    if execution_mode and execution_mode in {"Enterprise", "Enterprise+Modular", "Standard"}:
        state["execution_mode"] = execution_mode
    workflow_type_recommended = _markdown_row_value(text, "Recommended workflow type")
    if workflow_type_recommended in {
        "enterprise-modular",
        "technical-spec-modular",
        "agile-delivery-flow",
        "agile-delivery-light-flow",
        "b2s-flow",
        "b2s-dynamic",
        "fast-path",
    }:
        state["workflow_type_recommended"] = workflow_type_recommended


def _parse_readiness_fields(workspace_root, state: dict) -> None:
    path = workspace_root / "engineering-readiness" / "readiness-check.md"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    score = _markdown_row_value(text, "Readiness score")
    if score:
        match = re.search(r"(\d+)", score)
        if match:
            state["readiness_score"] = int(match.group(1))

    api_contract_mode = _markdown_row_value(text, "API contract mode")
    valid_modes = {"product", "internal", "coordinated"}
    if api_contract_mode and api_contract_mode.lower() in valid_modes:
        state["api_contract_mode"] = api_contract_mode.lower()
    elif "api_contract_mode" not in state or state["api_contract_mode"] is None:
        state["api_contract_mode"] = "internal"

    gate_map = {
        "BDD Scenarios": "BDD",
        "Test Strategy": "TEST_STRATEGY",
        "Security Review": "SECURITY_REVIEW",
        "API Contract": "API_CONTRACT",
        "Data Contract": "DATA_CONTRACT",
        "Event Contract": "EVENT_CONTRACT",
        "Observability Plan": "OBSERVABILITY_PLAN",
    }
    triggered = []
    for display, token in gate_map.items():
        pattern = re.compile(
            rf"(?mi)^\|\s*{re.escape(display)}\s*\|\s*(Yes|No)\s*\|\s*.*?\|\s*(Yes|No)\s*\|"
        )
        match = pattern.search(text)
        if match and match.group(1).strip() == "Yes":
            triggered.append(token)
    state["quality_gates_triggered"] = triggered


def _gate_action_id_for(action: dict, actions_by_id: dict) -> str | None:
    human_gate = action.get("human_gate") or {}
    gate_id = human_gate.get("gate_id")
    if not gate_id:
        return None
    candidate = f"gate-{gate_id}"
    if candidate in actions_by_id:
        return candidate
    return None


def _apply_artifact_statuses(state: dict, action: dict, status: str) -> None:
    for artifact_path in workspace.action_output_paths(action):
        state["artifact_status"][artifact_path] = status


def _required_inputs_present(action: dict, workspace_root) -> bool:
    for pattern in action.get("inputs", {}).get("required", []):
        exists, _ = workspace.resolve_input_pattern(workspace_root, pattern)
        if not exists:
            return False
    return True


def _conditions_pass(
    action: dict,
    state: dict,
    workspace_root,
    actions_by_id: dict,
) -> bool:
    return all(
        next_step.evaluate_condition(condition, state, workspace_root, actions_by_id)
        for condition in action.get("conditions", [])
    )


def _all_outputs_exist(action: dict, workspace_root) -> bool:
    outputs = workspace.action_output_paths(action)
    return bool(outputs) and all(
        workspace.artifact_exists(workspace_root, artifact_path) for artifact_path in outputs
    )


def _artifact_status_from_previous(previous_state: dict, action: dict) -> str | None:
    statuses = [
        previous_state.get("artifact_status", {}).get(artifact_path)
        for artifact_path in workspace.action_output_paths(action)
    ]
    if any(status == "accepted" for status in statuses):
        return "accepted"
    if any(status == "failed" for status in statuses):
        return "failed"
    return None


def _items_for_action(action: dict, state: dict, workspace_root) -> list[str]:
    """Return items for the current wave (used for selecting the next item)."""
    wave_idx = workspace.current_wave_index(state)
    wave_items = workspace.items_for_wave(workspace_root, wave_idx)
    if wave_items:
        return wave_items
    return workspace.extract_items_from_source(
        workspace_root,
        action["item_source"],
        action["item_pattern"],
    )


def _all_items_for_action(action: dict, workspace_root) -> list[str]:
    """Return all items across all waves (used for completeness checking)."""
    all_wave = workspace.all_wave_items(workspace_root)
    if all_wave:
        return all_wave
    return workspace.extract_items_from_source(
        workspace_root,
        action["item_source"],
        action["item_pattern"],
    )


def _apply_gate_acceptance_to_action(
    state: dict,
    action: dict,
    action_id: str,
    accepted_status: str,
    current_item: str | None,
    workspace_root: Path,
) -> None:
    _apply_artifact_statuses(state, action, accepted_status)
    if action.get("iteration_mode") == "per_item":
        if current_item:
            item_key = f"{action_id}#{current_item}"
            state.setdefault("action_item_status", {})[item_key] = accepted_status
        all_items = _all_items_for_action(action, workspace_root)
        all_done = all(
            state["action_item_status"].get(f"{action_id}#{item}") in workspace.ACTION_STATUSES_COMPLETE
            for item in all_items
        )
        state["action_status"][action_id] = accepted_status if all_done else workspace.ACTION_STATUS_IN_PROGRESS
    else:
        state["action_status"][action_id] = accepted_status


def _should_auto_accept_gate(gate_state: dict | None) -> bool:
    if not gate_state:
        return False
    if gate_state.get("interaction_mode") != "collect_answers":
        return False
    summary = gate_state.get("review_summary") or {}
    return bool(summary.get("no_blockers"))


def _candidate_gate_payload(
    action: dict,
    actions_by_id: dict,
    action_id: str,
    current_item: str | None = None,
) -> dict | None:
    gate_action_id = _gate_action_id_for(action, actions_by_id)
    if not gate_action_id:
        return None
    outputs = workspace.action_output_paths(action)
    artifact_path = outputs[0] if outputs else None
    human_gate = action.get("human_gate") or {}
    gate_state = {
        "gate_id": action["human_gate"]["gate_id"],
        "action_id": gate_action_id,
        "source_action_id": action_id,
        "artifact_path": artifact_path,
        "status": "waiting_human",
        "owner": action["human_gate"]["owner"],
    }
    if current_item:
        gate_state["current_item"] = current_item
    interaction_mode = human_gate.get("interaction_mode")
    if interaction_mode:
        gate_state["interaction_mode"] = interaction_mode
    rerun_action = human_gate.get("rerun_action")
    if rerun_action:
        gate_state["rerun_action"] = rerun_action
    clarification_file_pattern = human_gate.get("clarification_file")
    if clarification_file_pattern:
        gate_state["clarification_file"] = (
            clarification_file_pattern.replace("{current_item}", current_item)
            if current_item and "{current_item}" in clarification_file_pattern
            else clarification_file_pattern
        )
    return gate_state


def _epic_review_summary(workspace_root: Path, validation_result: dict | None = None) -> dict:
    epics_dir = workspace_root / "epics"
    summary = {
        "total_epics": 0,
        "total_stories": 0,
        "stories_with_2_plus_acceptance_criteria": 0,
        "stories_with_open_questions": 0,
        "not_ready_stories": 0,
        "unknown_requirement_references": 0,
        "requirement_title_mismatches": 0,
        "coverage_or_semantic_warnings": 0,
    }
    if not epics_dir.exists():
        return summary

    epic_dirs = sorted([d for d in epics_dir.iterdir() if d.is_dir() and d.name.startswith("E-")])
    summary["total_epics"] = len(epic_dirs)

    for epic_dir in epic_dirs:
        epic_md = epic_dir / "epic.md"
        if epic_md.exists():
            epic_text = epic_md.read_text(encoding="utf-8")
            summary["not_ready_stories"] += len(
                re.findall(r"\|\s*[FS]-\d{3}\.\d+\s*\|.*?\|\s*Not Ready\s*\|", epic_text, flags=re.MULTILINE)
            )

        stories_dir = epic_dir / "stories"
        if not stories_dir.exists():
            continue
        story_files = sorted([f for f in stories_dir.glob("S-*.md") if not f.name.endswith(".prompt.md")])
        summary["total_stories"] += len(story_files)
        for story_file in story_files:
            text = story_file.read_text(encoding="utf-8")
            scenario_count = len(re.findall(r"^\s*Scenario:", text, flags=re.MULTILINE))
            if scenario_count >= 2:
                summary["stories_with_2_plus_acceptance_criteria"] += 1
            if re.search(r"^\|\s*OQ-\d{3}\s*\|", text, flags=re.MULTILINE):
                summary["stories_with_open_questions"] += 1

    named_rule_results = list((validation_result or {}).get("named_rule_results", []) or [])
    for item in named_rule_results:
        if item.get("result") != "fail":
            continue
        rule_name = item.get("rule_name")
        if rule_name == "no_unknown_requirement_references":
            summary["unknown_requirement_references"] += 1
        elif rule_name == "requirement_title_consistency":
            summary["requirement_title_mismatches"] += 1
        elif rule_name in {
            "coverage_claim_matches_evidence",
            "requirement_semantics_preserved",
            "open_questions_propagated",
        }:
            summary["coverage_or_semantic_warnings"] += 1

    return summary


def _epic_clarification_summary(workspace_root: Path, validation_result: dict | None = None) -> dict:
    state = workspace.load_state(workspace_root)
    current_item = state.get("current_item")
    summary = {
        "epic_id": current_item,
        "question_count": 0,
        "clarification_file": f"input/clarifications/{current_item}.yaml" if current_item else None,
        "questions": [],
        "no_blockers": False,
    }
    if not current_item:
        return summary

    epics_dir = workspace_root / "epics"
    epic_dirs = sorted([d for d in epics_dir.iterdir() if d.is_dir() and d.name.startswith(current_item)]) if epics_dir.exists() else []
    if not epic_dirs:
        return summary
    request_path = epic_dirs[0] / "clarification-request.md"
    if not request_path.exists():
        return summary

    text = request_path.read_text(encoding="utf-8")
    if "No blocking questions require clarification for this epic." in text:
        summary["no_blockers"] = True
        return summary

    table_match = re.search(r"## Blocking Questions\s*\n((?:\|.*\n)+)", text)
    if not table_match:
        return summary

    for row in table_match.group(1).splitlines():
        cells = [c.strip() for c in row.split("|") if c.strip()]
        if len(cells) != 6 or cells[0] == "ID" or cells[0].startswith("---"):
            continue
        summary["questions"].append({
            "question_id": cells[0],
            "route": cells[1],
            "page": cells[2],
            "prompt": cells[3],
            "impact": cells[4],
            "required_for": cells[5],
        })
    summary["question_count"] = len(summary["questions"])
    return summary


def _solution_design_clarification_summary(
    workspace_root: Path,
    validation_result: dict | None = None,
) -> dict:
    request_path = workspace_root / "architecture" / "solution-design-clarification-request.md"
    summary = {
        "question_count": 0,
        "clarification_file": "input/clarifications/solution-design.yaml",
        "questions": [],
        "no_blockers": False,
    }
    if not request_path.exists():
        return summary

    text = request_path.read_text(encoding="utf-8")
    if "No blocking solution design questions require clarification." in text:
        summary["no_blockers"] = True
        return summary

    table_match = re.search(r"## Blocking Questions\s*\n((?:\|.*\n)+)", text)
    if not table_match:
        return summary

    for row in table_match.group(1).splitlines():
        cells = [c.strip() for c in row.split("|") if c.strip()]
        if len(cells) != 6 or cells[0] == "ID" or cells[0].startswith("---"):
            continue
        summary["questions"].append({
            "question_id": cells[0],
            "component": cells[1],
            "decision_area": cells[2],
            "prompt": cells[3],
            "impact": cells[4],
            "required_for": cells[5],
        })
    summary["question_count"] = len(summary["questions"])
    return summary


GateSummaryBuilder = Callable[[Path, dict | None], dict]


GATE_SUMMARY_BUILDERS: dict[str, GateSummaryBuilder] = {
    "epic-review": _epic_review_summary,
    "epic-clarification": _epic_clarification_summary,
    "solution-design-review": _solution_design_clarification_summary,
}


def _augment_gate_payload(
    workspace_root: Path,
    gate_state: dict,
    validation_result: dict | None = None,
) -> dict:
    gate_id = gate_state.get("gate_id")
    builder = GATE_SUMMARY_BUILDERS.get(gate_id)
    if builder:
        gate_state["review_summary"] = builder(workspace_root, validation_result)
    return gate_state


def _build_state_update_result(
    action_id: str,
    previous_state: dict,
    state: dict,
    gate_state: dict | None,
) -> dict:
    return {
        "overall": "pass",
        "action_id": action_id,
        "previous_state_summary": {
            "current_stage": previous_state.get("current_stage"),
            "next_action": previous_state.get("next_action"),
        },
        "applied_changes": {
            "current_stage": state.get("current_stage"),
            "artifact_status": state.get("artifact_status"),
        },
        "next_action": state.get("next_action"),
        "gate_state": gate_state,
    }


def run(args: object) -> None:
    workspace_root = workspace.resolve_workspace_root(args.workspace_root)
    state = workspace.load_state(workspace_root)

    phase_error = workspace.check_lifecycle_phase(state, workspace.LIFECYCLE_VALIDATED, "update-state")
    if phase_error:
        raise RuntimeError(phase_error)

    previous_state = {
        "current_stage": state.get("current_stage"),
        "next_action": state.get("next_action"),
    }
    action_id = workspace.read_action_id_from_state_or_args(state, getattr(args, "action_id", None))
    _, actions_by_id = workspace.load_stage_actions(workspace_root)
    action = actions_by_id[action_id]
    validation_result = workspace.load_yaml_file(
        workspace.resolve_output_path("validate-artifact", workspace_root, None)
    )

    gate_state = None

    # Safety check: even if validation passed, verify the primary artifact exists on disk
    if validation_result.get("overall") == "pass" and not _all_outputs_exist(action, workspace_root):
        missing = [
            ap for ap in workspace.action_output_paths(action)
            if not workspace.artifact_exists(workspace_root, ap)
        ]
        validation_result["overall"] = "fail"
        validation_result.setdefault("failures", []).append(
            f"Primary artifact(s) missing from disk: {missing}"
        )

    if validation_result.get("overall") != "pass":
        _apply_artifact_statuses(state, action, action["status_model"]["artifact_on_fail"])
        state["action_status"][action_id] = action["status_model"]["artifact_on_fail"]
        state["active_action"] = None
        state["next_action"] = None
        state["blocked_reason"] = "; ".join(validation_result.get("failures", [])) or "artifact validation failed"
        state["last_updated"] = _timestamp()
        workspace.advance_lifecycle_phase(state, workspace.LIFECYCLE_IDLE)
        workspace.save_state(workspace_root, state)
        result = _build_state_update_result(action_id, previous_state, state, gate_state)
        result["overall"] = "fail"
        workspace.save_json_file(
            workspace.resolve_output_path("update-state", workspace_root, args.output),
            result,
        )
        workspace.append_execution_log(
            workspace_root,
            command="update-state",
            overall=result["overall"],
            action_id=action_id,
            details={
                "gate_state": gate_state,
                "failure_count": len(validation_result.get("failures", [])),
            },
        )
        return

    artifact_status = action["status_model"]["artifact_on_pass"]
    _apply_artifact_statuses(state, action, artifact_status)

    iteration_mode = action.get("iteration_mode")
    current_item = state.get("current_item")

    if iteration_mode == "per_item":
        if current_item:
            item_key = f"{action_id}#{current_item}"
            state.setdefault("action_item_status", {})[item_key] = artifact_status

        all_items = _all_items_for_action(action, workspace_root)

        all_done = all(
            state["action_item_status"].get(f"{action_id}#{item}") in workspace.ACTION_STATUSES_COMPLETE
            for item in all_items
        )

        if all_done:
            state["action_status"][action_id] = artifact_status
            state["last_completed_action"] = action_id
        else:
            state["action_status"][action_id] = workspace.ACTION_STATUS_IN_PROGRESS
        state["current_item"] = None
    else:
        state["action_status"][action_id] = artifact_status
        state["last_completed_action"] = action_id

    state["active_action"] = None
    state["next_action"] = None
    state["blocked_reason"] = None
    state["last_updated"] = _timestamp()
    state["state_validated"] = True

    for key, value in (action.get("on_pass", {}).get("update_state") or {}).items():
        state[key] = value

    _parse_routing_fields(workspace_root, state)
    _parse_readiness_fields(workspace_root, state)

    gate_action_id = _gate_action_id_for(action, actions_by_id)
    if (action.get("human_gate") or {}).get("required") and gate_action_id:
        human_gate = action.get("human_gate") or {}
        gate_state = {
            "gate_id": human_gate["gate_id"],
            "action_id": gate_action_id,
            "source_action_id": action_id,
            "artifact_path": workspace.action_output_paths(action)[0] if workspace.action_output_paths(action) else None,
            "status": "waiting_human",
            "owner": human_gate["owner"],
        }
        if current_item:
            gate_state["current_item"] = current_item
        if human_gate.get("interaction_mode"):
            gate_state["interaction_mode"] = human_gate["interaction_mode"]
        if human_gate.get("rerun_action"):
            gate_state["rerun_action"] = human_gate["rerun_action"]
        clarification_file = human_gate.get("clarification_file")
        if clarification_file:
            gate_state["clarification_file"] = (
                clarification_file.replace("{current_item}", current_item)
                if current_item and "{current_item}" in clarification_file
                else clarification_file
            )
        gate_state = _augment_gate_payload(workspace_root, gate_state, validation_result)
        if _should_auto_accept_gate(gate_state):
            accepted_status = action["status_model"]["artifact_on_gate_accept"]
            _apply_gate_acceptance_to_action(
                state,
                action,
                action_id,
                accepted_status,
                current_item,
                workspace_root,
            )
            state["awaiting_human"] = False
            state["current_gate"] = None
            state["blocked_reason"] = None
            state["action_status"][gate_action_id] = "accepted"
            state["last_completed_action"] = gate_action_id
            gate_state = None
        else:
            state["awaiting_human"] = True
            state["current_gate"] = gate_state
            state["blocked_reason"] = f"waiting for {human_gate['owner']} review"
            state["action_status"][gate_action_id] = "waiting_human"
    else:
        state["awaiting_human"] = False
        state["current_gate"] = None

    if dynamic_state.should_return_to_dynamic_assessment(
        state,
        action_id,
        awaiting_human=state.get("awaiting_human", False),
    ):
        dynamic_state.reset_dynamic_orchestration_cycle(state, actions_by_id)
        state["current_stage"] = dynamic_state.dynamic_loop_start_stage_id(actions_by_id)
        state["dynamic_stop_reason"] = None

    if not state.get("awaiting_human"):
        preview = next_step.select_next_action(workspace_root, state)
        state["next_action"] = preview.get("selected_action")
        if preview.get("overall") == "fail":
            state["blocked_reason"] = preview.get("blocking_reason")

    workspace.advance_lifecycle_phase(state, workspace.LIFECYCLE_IDLE)
    workspace.save_state(workspace_root, state)
    result = _build_state_update_result(action_id, previous_state, state, gate_state)
    workspace.save_json_file(
        workspace.resolve_output_path("update-state", workspace_root, args.output),
        result,
    )
    workspace.append_execution_log(
        workspace_root,
        command="update-state",
        overall=result["overall"],
        action_id=action_id,
        details={
            "gate_state": gate_state,
            "next_action": result.get("next_action"),
        },
    )

def finalize_action(args: object) -> None:
    """Validate the current artifact and, if it passes, update workflow state.

    Combines ``validate-artifact`` + ``update-state`` into a single command so
    the orchestrating LLM only needs to call one CLI command after generating
    an artifact.  On validation failure the command returns the failure details
    without updating state — the LLM should fix the artifact and call
    ``finalize-action`` again.
    """
    from b2s_engine import validation as validation_module

    workspace_root = workspace.resolve_workspace_root(args.workspace_root)
    state = workspace.load_state(workspace_root)
    action_id = workspace.read_action_id_from_state_or_args(state, getattr(args, "action_id", None))

    current_phase = state.get("action_lifecycle_phase", workspace.LIFECYCLE_IDLE)
    if current_phase == workspace.LIFECYCLE_VALIDATED:
        workspace.advance_lifecycle_phase(state, workspace.LIFECYCLE_DISPATCHED)
        workspace.save_state(workspace_root, state)

    phase_error = workspace.check_lifecycle_phase(state, workspace.LIFECYCLE_DISPATCHED, "finalize-action")
    if phase_error:
        raise RuntimeError(phase_error)

    validation_result = validation_module.validate_action(workspace_root, state, action_id)

    workspace.advance_lifecycle_phase(state, workspace.LIFECYCLE_VALIDATED)
    workspace.save_state(workspace_root, state)

    workspace.append_execution_log(
        workspace_root,
        command="validate-artifact",
        overall=validation_result["overall"],
        action_id=action_id,
        details={
            "artifact_path": validation_result["artifact_path"],
            "failure_count": len(validation_result["failures"]),
            "failures": validation_result["failures"],
        },
    )

    workspace.save_yaml_file(
        workspace.resolve_output_path("validate-artifact", workspace_root, None),
        validation_result,
    )

    if validation_result["overall"] != "pass":
        result = {
            "status": "validation_failed",
            "action_id": action_id,
            "validation": {
                "overall": "fail",
                "failure_count": len(validation_result["failures"]),
                "failures": validation_result["failures"],
                "advisories": validation_result["advisories"],
            },
            "state_update": None,
            "gate": None,
            "continue": False,
        }
        out_path = workspace.resolve_output_path("finalize-action", workspace_root, getattr(args, "output", None))
        workspace.save_json_file(out_path, result)
        print(f"\n[finalize-action] validation FAILED — {len(validation_result['failures'])} failure(s)")
        for f in validation_result["failures"]:
            print(f"  • {f}")
        print("\nFix the artifact and run finalize-action again.")
        return

    previous_state = {
        "current_stage": state.get("current_stage"),
        "next_action": state.get("next_action"),
    }
    _, actions_by_id = workspace.load_stage_actions(workspace_root)
    action = actions_by_id[action_id]

    gate_state = None
    artifact_status = action["status_model"]["artifact_on_pass"]
    _apply_artifact_statuses(state, action, artifact_status)

    iteration_mode = action.get("iteration_mode")
    current_item = state.get("current_item")

    if iteration_mode == "per_item":
        if current_item:
            item_key = f"{action_id}#{current_item}"
            state.setdefault("action_item_status", {})[item_key] = artifact_status

        all_items = _all_items_for_action(action, workspace_root)
        all_done = all(
            state["action_item_status"].get(f"{action_id}#{item}") in workspace.ACTION_STATUSES_COMPLETE
            for item in all_items
        )

        if all_done:
            state["action_status"][action_id] = artifact_status
            state["last_completed_action"] = action_id
        else:
            state["action_status"][action_id] = workspace.ACTION_STATUS_IN_PROGRESS
        state["current_item"] = None
    else:
        state["action_status"][action_id] = artifact_status
        state["last_completed_action"] = action_id

    state["active_action"] = None
    state["next_action"] = None
    state["blocked_reason"] = None
    state["last_updated"] = _timestamp()
    state["state_validated"] = True

    for key, value in (action.get("on_pass", {}).get("update_state") or {}).items():
        state[key] = value

    _parse_routing_fields(workspace_root, state)
    _parse_readiness_fields(workspace_root, state)

    gate_action_id = _gate_action_id_for(action, actions_by_id)
    if (action.get("human_gate") or {}).get("required") and gate_action_id:
        human_gate = action.get("human_gate") or {}
        gate_state = {
            "gate_id": human_gate["gate_id"],
            "action_id": gate_action_id,
            "source_action_id": action_id,
            "artifact_path": workspace.action_output_paths(action)[0] if workspace.action_output_paths(action) else None,
            "status": "waiting_human",
            "owner": human_gate["owner"],
        }
        if current_item:
            gate_state["current_item"] = current_item
        if human_gate.get("interaction_mode"):
            gate_state["interaction_mode"] = human_gate["interaction_mode"]
        if human_gate.get("rerun_action"):
            gate_state["rerun_action"] = human_gate["rerun_action"]
        clarification_file = human_gate.get("clarification_file")
        if clarification_file:
            gate_state["clarification_file"] = (
                clarification_file.replace("{current_item}", current_item)
                if current_item and "{current_item}" in clarification_file
                else clarification_file
            )
        gate_state = _augment_gate_payload(workspace_root, gate_state, validation_result)
        if _should_auto_accept_gate(gate_state):
            accepted_status = action["status_model"]["artifact_on_gate_accept"]
            _apply_gate_acceptance_to_action(
                state, action, action_id, accepted_status, current_item, workspace_root,
            )
            state["awaiting_human"] = False
            state["current_gate"] = None
            state["blocked_reason"] = None
            state["action_status"][gate_action_id] = "accepted"
            state["last_completed_action"] = gate_action_id
            gate_state = None
        else:
            state["awaiting_human"] = True
            state["current_gate"] = gate_state
            state["blocked_reason"] = f"waiting for {human_gate['owner']} review"
            state["action_status"][gate_action_id] = "waiting_human"
    else:
        state["awaiting_human"] = False
        state["current_gate"] = None

    if dynamic_state.should_return_to_dynamic_assessment(
        state, action_id, awaiting_human=state.get("awaiting_human", False),
    ):
        dynamic_state.reset_dynamic_orchestration_cycle(state, actions_by_id)
        state["current_stage"] = dynamic_state.dynamic_loop_start_stage_id(actions_by_id)
        state["dynamic_stop_reason"] = None

    if not state.get("awaiting_human"):
        preview = next_step.select_next_action(workspace_root, state)
        state["next_action"] = preview.get("selected_action")
        if preview.get("overall") == "fail":
            state["blocked_reason"] = preview.get("blocking_reason")

    workspace.advance_lifecycle_phase(state, workspace.LIFECYCLE_IDLE)
    workspace.save_state(workspace_root, state)

    per_item_boundary = False
    if iteration_mode == "per_item":
        items = _items_for_action(action, state, workspace_root)
        remaining = [
            item for item in items
            if state.get("action_item_status", {}).get(f"{action_id}#{item}") not in workspace.ACTION_STATUSES_COMPLETE
        ]
        per_item_boundary = len(remaining) > 0

    result = {
        "status": "gate_pending" if state.get("awaiting_human") else (
            "complete" if state.get("next_action") is None else "continue"
        ),
        "action_id": action_id,
        "validation": {
            "overall": "pass",
            "failure_count": 0,
            "failures": [],
            "advisories": validation_result["advisories"],
        },
        "state_update": {
            "action_id": action_id,
            "next_action": state.get("next_action"),
            "current_stage": state.get("current_stage"),
        },
        "gate": gate_state,
        "continue": not state.get("awaiting_human") and state.get("next_action") is not None,
        "per_item_boundary": per_item_boundary,
    }

    out_path = workspace.resolve_output_path("finalize-action", workspace_root, getattr(args, "output", None))
    workspace.save_json_file(out_path, result)

    workspace.append_execution_log(
        workspace_root,
        command="update-state",
        overall="pass",
        action_id=action_id,
        details={
            "gate_state": gate_state,
            "next_action": state.get("next_action"),
        },
    )

    status = result["status"]
    print(f"\n[finalize-action] {status}")
    if status == "gate_pending":
        print(f"  Gate: {gate_state.get('gate_id')} — waiting for {gate_state.get('owner')}")
    elif status == "continue":
        print(f"  Next action: {state.get('next_action')}")
    elif status == "complete":
        print("  Workflow complete — no further actions.")
    if per_item_boundary:
        print(f"  Per-item boundary: more items remain for {action_id}.")


def repair_state(args: object) -> None:
    workspace_root = workspace.resolve_workspace_root(args.workspace_root)
    state = workspace.load_state(workspace_root)
    previous_state = {
        "current_stage": state.get("current_stage"),
        "next_action": state.get("next_action"),
        "action_status": dict(state.get("action_status", {})),
        "artifact_status": dict(state.get("artifact_status", {})),
    }
    actions, actions_by_id = workspace.load_stage_actions(workspace_root)

    _parse_routing_fields(workspace_root, state)
    _parse_readiness_fields(workspace_root, state)
    rebuilt_action_status = {}
    rebuilt_artifact_status = {}
    current_gate = None
    last_completed_action = None

    for action in actions:
        action_id = action["action_id"]
        if action_id.startswith("gate-"):
            continue
        if action.get("stage_id") == "human-triggered":
            continue
        if not _all_outputs_exist(action, workspace_root):
            continue

        candidate_state = {
            **state,
            "action_status": rebuilt_action_status,
            "artifact_status": rebuilt_artifact_status,
        }
        if not all(
            next_step.action_is_complete(blocking_action, candidate_state)
            for blocking_action in action.get("blocked_by_action", [])
        ):
            continue
        if not _required_inputs_present(action, workspace_root):
            continue
        if not _conditions_pass(action, candidate_state, workspace_root, actions_by_id):
            continue

        previous_action_status = previous_state["action_status"].get(action_id)
        previous_artifact_status = _artifact_status_from_previous(previous_state, action)
        human_gate = action.get("human_gate") or {}
        gate_action_id = _gate_action_id_for(action, actions_by_id)

        if human_gate.get("required") and gate_action_id:
            previous_gate_status = previous_state["action_status"].get(gate_action_id)
            if (
                previous_gate_status == "accepted"
                or previous_action_status == "accepted"
                or previous_artifact_status == "accepted"
            ):
                source_status = "accepted"
                gate_status = "accepted"
                artifact_status = "accepted"
                last_completed_action = gate_action_id
            elif (
                previous_gate_status == "failed"
                or previous_action_status == "failed"
                or previous_artifact_status == "failed"
            ):
                source_status = "failed"
                gate_status = "failed"
                artifact_status = "failed"
                last_completed_action = gate_action_id
            else:
                source_status = action["status_model"]["artifact_on_pass"]
                gate_status = "waiting_human"
                artifact_status = source_status
                if current_gate is None:
                    current_gate = _augment_gate_payload(
                        workspace_root,
                        _candidate_gate_payload(action, actions_by_id, action_id, state.get("current_item")),
                    )
                last_completed_action = action_id

            rebuilt_action_status[action_id] = source_status
            rebuilt_action_status[gate_action_id] = gate_status
            for artifact_path in workspace.action_output_paths(action):
                rebuilt_artifact_status[artifact_path] = artifact_status
            continue

        rebuilt_action_status[action_id] = action["status_model"]["artifact_on_pass"]
        for artifact_path in workspace.action_output_paths(action):
            rebuilt_artifact_status[artifact_path] = action["status_model"]["artifact_on_pass"]
        last_completed_action = action_id

    state["action_status"] = rebuilt_action_status
    state["artifact_status"] = rebuilt_artifact_status
    state["last_completed_action"] = last_completed_action
    state["active_action"] = None

    if current_gate:
        state["awaiting_human"] = True
        state["current_gate"] = current_gate
        state["current_stage"] = actions_by_id[current_gate["source_action_id"]]["stage_id"]
        state["next_action"] = None
        state["blocked_reason"] = f"waiting for {current_gate['owner']} review"
    else:
        workflow = workspace.load_workflow_definition(workspace_root)
        state["current_stage"] = workflow["stages"][0]["id"]
        state["awaiting_human"] = False
        state["current_gate"] = None
        state["blocked_reason"] = None
        preview = next_step.select_next_action(workspace_root, state)
        state["current_stage"] = preview.get("selected_stage") or state.get("current_stage")
        state["next_action"] = preview.get("selected_action")
        if preview.get("overall") == "fail":
            state["blocked_reason"] = preview.get("blocking_reason")

    state["state_validated"] = True
    state["last_updated"] = _timestamp()
    workspace.advance_lifecycle_phase(state, workspace.LIFECYCLE_IDLE)
    workspace.save_state(workspace_root, state)
    workspace.save_json_file(
        workspace.resolve_output_path("repair-state", workspace_root, args.output),
        {
            "overall": "pass",
            "action_id": state.get("active_action"),
            "previous_state_summary": {
                "current_stage": previous_state.get("current_stage"),
                "next_action": previous_state.get("next_action"),
            },
            "applied_changes": {
                "state_validated": True,
                "current_stage": state.get("current_stage"),
                "repaired_action_count": len(rebuilt_action_status),
                "repaired_artifact_count": len(rebuilt_artifact_status),
            },
            "next_action": state.get("next_action"),
            "gate_state": state.get("current_gate"),
        },
    )
    workspace.append_execution_log(
        workspace_root,
        command="repair-state",
        overall="pass",
        action_id=state.get("active_action"),
        details={
            "repaired_action_count": len(rebuilt_action_status),
            "repaired_artifact_count": len(rebuilt_artifact_status),
            "next_action": state.get("next_action"),
            "gate_state": state.get("current_gate"),
        },
    )
