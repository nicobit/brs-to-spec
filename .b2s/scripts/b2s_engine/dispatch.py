"""dispatch-next — emit an execution plan for the next ready action.

This command does NOT execute the skill itself (that requires an AI agent).
It produces a JSON plan that tells the caller:
  - which action is ready
  - which skill prompt to load and execute
  - which inputs are available
  - what to run next (validate-artifact → update-state) after the skill completes

Stop conditions (awaiting_human, no ready action, workflow complete) are
surfaced as distinct statuses so callers can branch on them.
"""

from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Any

from b2s_engine import inputs as inputs_module
from b2s_engine import next_step, workspace


# --------------------------------------------------------------------------- #
# Internal helpers                                                             #
# --------------------------------------------------------------------------- #


SUPPORTED_PROMPT_PLACEHOLDERS = {
    "required_inputs",
    "optional_inputs",
    "resolved_required_inputs",
    "resolved_optional_inputs",
    "resolved_policy_inputs",
    "primary_output",
    "secondary_outputs",
    "prompt_family",
    "template_mode",
    "current_item",
    "item_folder",
}


def _render_placeholder_value(value: Any) -> str:
    if isinstance(value, list):
        if not value:
            return "[]"
        return "\n".join(f"- {item}" for item in value)
    return str(value)


def _render_prompt_text(text: str, placeholders: dict[str, Any]) -> str:
    pattern = re.compile(r"\{(" + "|".join(re.escape(name) for name in sorted(SUPPORTED_PROMPT_PLACEHOLDERS)) + r")\}")

    def repl(match: re.Match[str]) -> str:
        key = match.group(1)
        if key not in placeholders:
            raise ValueError(f"Missing prompt placeholder: {key}")
        return _render_placeholder_value(placeholders[key])

    return pattern.sub(repl, text)


def _skill_file_details(skill_ref: str) -> tuple[Path | None, bool]:
    if not skill_ref:
        return None, False
    skill_path = (workspace.REPO_ROOT / skill_ref).resolve()
    return skill_path, skill_path.exists()


def _resolve_skill_prompt(action: dict[str, Any], workspace_root: Path, prompt_placeholders: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return skill prompt path and rendered content when available."""
    skill_ref = action.get("skill_ref", "")
    prompt_family = str(action.get("prompt_family") or "b2s")
    fallback_skill_ref = str((action.get("compatibility") or {}).get("fallback_skill_ref") or "")
    skill_path, skill_exists = _skill_file_details(skill_ref)
    prompt_text = None
    rendered_prompt = None

    resolved_skill_ref = skill_ref
    resolved_skill_path = skill_path
    fallback_used = False

    if not skill_exists and fallback_skill_ref:
        fallback_path, fallback_exists = _skill_file_details(fallback_skill_ref)
        if fallback_exists:
            resolved_skill_ref = fallback_skill_ref
            resolved_skill_path = fallback_path
            skill_exists = True
            fallback_used = True

    if not skill_exists:
        if prompt_family != "b2s":
            raise FileNotFoundError(
                f"Skill prompt for family '{prompt_family}' not found: '{skill_ref}'. "
                "Provide a valid skill_ref or compatibility.fallback_skill_ref."
            )
        raise FileNotFoundError(f"Skill prompt not found: '{skill_ref}'")

    if resolved_skill_path and resolved_skill_path.exists():
        prompt_text = resolved_skill_path.read_text(encoding="utf-8")
        rendered_prompt = _render_prompt_text(prompt_text, prompt_placeholders or {})
    return {
        "skill_ref": resolved_skill_ref,
        "skill_path": str(resolved_skill_path) if resolved_skill_path else None,
        "skill_exists": skill_exists,
        "requested_skill_ref": skill_ref,
        "fallback_skill_ref": fallback_skill_ref or None,
        "fallback_used": fallback_used,
        "prompt_family": prompt_family,
        "skill_text": prompt_text,
        "rendered_skill_text": rendered_prompt,
    }


def _collect_inputs(action: dict[str, Any], workspace_root: Path, current_item: str | None = None) -> dict[str, Any]:
    """Resolve required and optional inputs for an action."""
    collected = inputs_module.collect_action_inputs(action, workspace_root, current_item=current_item)
    computed_inputs = inputs_module.generate_computed_inputs(action, workspace_root, current_item=current_item)
    return {
        "required_inputs": collected["required_inputs"],
        "optional_inputs": collected["optional_inputs"],
        "policy_inputs": collected["policy_inputs"],
        "missing_required_inputs": collected["missing_required_inputs"],
        "missing_policy_inputs": collected["missing_policy_inputs"],
        "inputs_ready": collected["overall"] == "pass",
        "prompt_placeholders": collected["prompt_placeholders"],
        "computed_inputs": computed_inputs,
    }


def _action_summary(action: dict[str, Any], workspace_root: Path, current_item: str | None = None) -> dict[str, Any]:
    collected = _collect_inputs(action, workspace_root, current_item=current_item)
    skill = _resolve_skill_prompt(action, workspace_root, collected["prompt_placeholders"])
    output_paths = workspace.action_output_paths(action)
    return {
        "action_id": action["action_id"],
        "title": action.get("title", ""),
        "stage_id": action.get("stage_id", ""),
        "persona": action.get("persona", ""),
        "prompt_family": skill["prompt_family"],
        "skill_ref": skill["skill_ref"],
        "requested_skill_ref": skill["requested_skill_ref"],
        "fallback_skill_ref": skill["fallback_skill_ref"],
        "fallback_used": skill["fallback_used"],
        "skill_path": skill["skill_path"],
        "skill_exists": skill["skill_exists"],
        "artifact_template_ref": action.get("artifact_template_ref", ""),
        "output_paths": output_paths,
        "required_inputs": collected["required_inputs"],
        "optional_inputs": collected["optional_inputs"],
        "policy_inputs": collected["policy_inputs"],
        "missing_required_inputs": collected["missing_required_inputs"],
        "missing_policy_inputs": collected["missing_policy_inputs"],
        "inputs_ready": collected["inputs_ready"],
        "prompt_placeholders": collected["prompt_placeholders"],
        "computed_inputs": collected["computed_inputs"],
        "rendered_skill_text": skill["rendered_skill_text"],
        "has_human_gate": bool((action.get("human_gate") or {}).get("required")),
        "gate_owner": (action.get("human_gate") or {}).get("owner"),
    }


# --------------------------------------------------------------------------- #
# Status values                                                                #
# --------------------------------------------------------------------------- #

STATUS_READY = "ready"           # action is ready; skill prompt should be executed
STATUS_BLOCKED = "blocked"       # prerequisites or inputs not satisfied
STATUS_GATE = "awaiting_gate"    # human review required before continuing
STATUS_COMPLETE = "complete"     # workflow is fully complete


# --------------------------------------------------------------------------- #
# Public entry point                                                           #
# --------------------------------------------------------------------------- #


def _check_gate_receipt(workspace_root: Path, current_state: dict[str, Any]) -> str | None:
    """If last_completed_action is a gate, verify the engine wrote a receipt."""
    last = current_state.get("last_completed_action", "")
    if not last or not last.startswith("gate-"):
        return None
    if current_state.get("awaiting_human"):
        return None

    receipt_path = workspace.tmp_dir(workspace_root) / "current-gate.json"
    if not receipt_path.exists():
        return (
            f"Gate '{last}' was marked complete but no engine receipt found at "
            f"'.b2s/tmp/current-gate.json'. The gate may have been approved "
            f"outside the b2s engine. Run `repair-state` or re-approve via "
            f"`approve-current-gate`."
        )
    return None


def _clarification_wait_message(gate: dict[str, Any], current_state: dict[str, Any]) -> str:
    clarification_file = gate.get("clarification_file")
    rerun_action = gate.get("rerun_action")
    gate_id = gate.get("gate_id")
    if gate_id == "epic-clarification":
        current_item = gate.get("current_item") or current_state.get("current_item", "(unknown)")
        return (
            f"Waiting for {gate.get('owner', 'human')} to provide clarification answers "
            f"for epic `{current_item}`. "
            f"Record answers in `{clarification_file or 'input/clarifications/<epic>.yaml'}` "
            f"then approve the gate to rerun `{rerun_action or 'create-epic-shells'}`."
        )
    return (
        f"Waiting for {gate.get('owner', 'human')} to provide clarification answers "
        f"for solution design blockers. Record answers in "
        f"`{clarification_file or 'input/clarifications/solution-design.yaml'}` "
        f"then approve the gate to rerun `{rerun_action or 'create-solution-decisions'}`."
    )


def build_plan(workspace_root: Path) -> dict[str, Any]:
    """Build and return an execution plan dict for the current workflow state."""
    current_state = workspace.load_state(workspace_root)
    _, actions_by_id = workspace.load_stage_actions(workspace_root)

    # --- state integrity audit ---
    integrity_issues = workspace.check_state_integrity(workspace_root, current_state)

    # --- gate receipt verification ---
    gate_integrity_error = _check_gate_receipt(workspace_root, current_state)

    # --- workflow type mismatch check ---
    workflow_type_warning = None
    current_type = current_state.get("workflow_type")
    recommended_type = current_state.get("workflow_type_recommended")
    if current_type and recommended_type and current_type != recommended_type:
        workflow_type_warning = (
            f"Workflow type mismatch: running '{current_type}' "
            f"but route-initiative recommends '{recommended_type}'. "
            f"Re-initialise with --workflow-type {recommended_type} to switch."
        )

    # --- blocked by gate integrity failure ---
    if gate_integrity_error:
        plan = {
            "status": STATUS_BLOCKED,
            "initiative_id": current_state.get("initiative_id"),
            "current_stage": current_state.get("current_stage"),
            "blocking_reason": gate_integrity_error,
            "message": f"Gate integrity check failed: {gate_integrity_error}",
            "next_cli_commands": [
                f"python .b2s/scripts/b2s_cli.py repair-state --workspace-root <path>",
            ],
            "action": None,
        }
        if integrity_issues:
            plan["integrity_warnings"] = integrity_issues
        if workflow_type_warning:
            plan["workflow_type_warning"] = workflow_type_warning
        return plan

    # --- gate check ---
    if current_state.get("awaiting_human"):
        gate = current_state.get("current_gate") or {}
        interaction_mode = gate.get("interaction_mode")
        next_commands = [
            f"python .b2s/scripts/b2s_cli.py approve-current-gate --workspace-root <path>",
            f"python .b2s/scripts/b2s_cli.py reject-current-gate --workspace-root <path>",
        ]
        if interaction_mode == "collect_answers":
            message = _clarification_wait_message(gate, current_state)
        else:
            message = (
                f"Waiting for {gate.get('owner', 'human')} to review "
                f"artifact `{gate.get('artifact_path', '(unknown)')}`. "
                "Run `approve-current-gate` or `reject-current-gate` to continue."
            )
        plan = {
            "status": STATUS_GATE,
            "initiative_id": current_state.get("initiative_id"),
            "current_stage": current_state.get("current_stage"),
            "gate_id": gate.get("gate_id"),
            "gate_owner": gate.get("owner"),
            "artifact_path": gate.get("artifact_path"),
            "review_summary": gate.get("review_summary"),
            "interaction_mode": interaction_mode,
            "clarification_file": gate.get("clarification_file"),
            "message": message,
            "next_cli_commands": next_commands,
            "action": None,
        }
        if integrity_issues:
            plan["integrity_warnings"] = integrity_issues
        return plan

    # --- select next action ---
    selection = next_step.select_next_action(workspace_root, current_state)

    # save next-step output (keeps execution log consistent)
    current_state["current_stage"] = selection["selected_stage"]
    current_state["active_action"] = selection["selected_action"]
    current_state["next_action"] = selection["selected_action"]
    current_state["state_validated"] = selection["overall"] == "pass"
    from datetime import datetime, timezone
    current_state["last_updated"] = datetime.now(timezone.utc).isoformat()
    if selection["overall"] == "fail":
        current_state["blocked_reason"] = selection["blocking_reason"]
    else:
        current_state["blocked_reason"] = None
    if selection["selected_action"]:
        workspace.advance_lifecycle_phase(current_state, workspace.LIFECYCLE_DISPATCHED)
    else:
        workspace.advance_lifecycle_phase(current_state, workspace.LIFECYCLE_IDLE)
    workspace.save_state(workspace_root, current_state)
    workspace.append_execution_log(
        workspace_root,
        command="dispatch-next",
        overall=selection["overall"],
        action_id=selection.get("selected_action"),
        details={
            "selected_stage": selection.get("selected_stage"),
            "reason": selection.get("reason"),
            "blocking_reason": selection.get("blocking_reason"),
        },
    )

    # --- workflow complete ---
    if selection["overall"] == "pass" and selection["selected_action"] is None:
        plan = {
            "status": STATUS_COMPLETE,
            "initiative_id": current_state.get("initiative_id"),
            "current_stage": selection["selected_stage"],
            "message": "All workflow actions are complete. No further steps required.",
            "next_cli_commands": [],
            "action": None,
        }
        if integrity_issues:
            plan["integrity_warnings"] = integrity_issues
        if workflow_type_warning:
            plan["workflow_type_warning"] = workflow_type_warning
        return plan

    # --- blocked ---
    if selection["overall"] == "fail":
        plan = {
            "status": STATUS_BLOCKED,
            "initiative_id": current_state.get("initiative_id"),
            "current_stage": selection["selected_stage"],
            "blocking_reason": selection["blocking_reason"],
            "message": f"Workflow is blocked: {selection['blocking_reason']}",
            "next_cli_commands": [],
            "action": None,
        }
        if integrity_issues:
            plan["integrity_warnings"] = integrity_issues
        if workflow_type_warning:
            plan["workflow_type_warning"] = workflow_type_warning
        return plan

    # --- ready ---
    action_id = selection["selected_action"]
    action = actions_by_id[action_id]

    current_item = selection.get("current_item")
    if current_item is not None:
        current_state["current_item"] = current_item
        workspace.save_state(workspace_root, current_state)

    summary = _action_summary(action, workspace_root, current_item=current_item)

    workspace.advance_lifecycle_phase(current_state, workspace.LIFECYCLE_INPUTS_COLLECTED)
    workspace.save_state(workspace_root, current_state)

    workspace_str = str(workspace_root)

    after_skill_commands = [
        f"python .b2s/scripts/b2s_cli.py validate-artifact --workspace-root \"{workspace_str}\"",
        f"python .b2s/scripts/b2s_cli.py update-state --workspace-root \"{workspace_str}\"",
        f"python .b2s/scripts/b2s_cli.py dispatch-next --workspace-root \"{workspace_str}\"",
    ]

    item_msg = f" [item: {current_item}]" if current_item else ""
    pending = selection.get("pending_items", [])
    total = selection.get("total_items")
    progress_msg = f" ({total - len(pending)}/{total} items done)" if total else ""

    plan = {
        "status": STATUS_READY,
        "initiative_id": current_state.get("initiative_id"),
        "current_stage": selection["selected_stage"],
        "workflow_source": workspace.active_workflow_source(workspace_root),
        "message": (
            f"Ready to execute `{action_id}` - {summary['title']}{item_msg}{progress_msg}. "
            f"Load {summary['prompt_family']} skill prompt at `{summary['skill_ref']}` and execute it, "
            "then run validate-artifact -> update-state -> dispatch-next."
        ),
        "action": summary,
        "after_skill_commands": after_skill_commands,
        "next_cli_commands": after_skill_commands,
    }
    if current_item is not None:
        plan["current_item"] = current_item
        plan["pending_items"] = pending
        plan["total_items"] = total
    if integrity_issues:
        plan["integrity_warnings"] = integrity_issues
    if workflow_type_warning:
        plan["workflow_type_warning"] = workflow_type_warning
    return plan


def run(args: object) -> None:
    workspace_root = workspace.resolve_workspace_root(args.workspace_root)
    plan = build_plan(workspace_root)

    # Write plan to output file
    out_path = workspace_root / ".b2s" / "tmp" / "dispatch-next.json"
    if getattr(args, "output", None):
        out_path = args.output
    workspace.save_json_file(out_path, plan)

    # Print human-readable summary
    status = plan["status"]
    initiative = plan.get("initiative_id", "")
    stage = plan.get("current_stage", "")

    print(f"\n[dispatch-next] {initiative}  stage={stage}  status={status}")
    print(f"  {plan['message']}")

    if status == STATUS_READY:
        action = plan["action"]
        print(f"\n  Skill prompt : {action['skill_ref']}")
        print(f"  Skill path   : {action['skill_path']}")
        if not action["inputs_ready"]:
            print(f"  MISSING INPUTS: {action['missing_required_inputs']}")
        print(f"  Outputs      : {action['output_paths']}")
        print(f"\n  After executing the skill, run:")
        for cmd in plan["after_skill_commands"]:
            print(f"    {cmd}")

    elif status == STATUS_GATE:
        print(f"\n  Gate        : {plan.get('gate_id')}")
        print(f"  Owner       : {plan.get('gate_owner')}")
        print(f"  Artifact    : {plan.get('artifact_path')}")
        if plan.get("interaction_mode") == "collect_answers":
            print(f"  Clarify via : {plan.get('clarification_file')}")
        summary = plan.get("review_summary") or {}
        if summary:
            print(f"\n  Review summary:")
            if plan.get("interaction_mode") == "collect_answers":
                if plan.get("gate_id") == "epic-clarification":
                    print(f"    Epic ID                        : {summary.get('epic_id')}")
                print(f"    Blocking questions             : {summary.get('question_count', 0)}")
                print(f"    No blockers                    : {summary.get('no_blockers', False)}")
            else:
                print(f"    Total epics                    : {summary.get('total_epics', 0)}")
                print(f"    Total stories                  : {summary.get('total_stories', 0)}")
                print(f"    Stories with 2+ AC             : {summary.get('stories_with_2_plus_acceptance_criteria', 0)}")
                print(f"    Stories with open questions    : {summary.get('stories_with_open_questions', 0)}")
                print(f"    Not Ready stories              : {summary.get('not_ready_stories', 0)}")
                print(f"    Unknown requirement refs       : {summary.get('unknown_requirement_references', 0)}")
                print(f"    Requirement title mismatches   : {summary.get('requirement_title_mismatches', 0)}")
                print(f"    Coverage/semantic warnings     : {summary.get('coverage_or_semantic_warnings', 0)}")
        print(f"\n  Run one of:")
        for cmd in plan["next_cli_commands"]:
            print(f"    {cmd}")

    elif status == STATUS_BLOCKED:
        print(f"\n  Blocking reason: {plan.get('blocking_reason')}")

    if plan.get("integrity_warnings"):
        print(f"\n  [INTEGRITY] {len(plan['integrity_warnings'])} issue(s) detected:")
        for issue in plan["integrity_warnings"]:
            print(f"    - [{issue.get('issue', 'unknown')}] {issue.get('detail', '')}")

    if plan.get("workflow_type_warning"):
        print(f"\n  [WARNING] {plan['workflow_type_warning']}")

    print()
