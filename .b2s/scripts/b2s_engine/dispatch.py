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
    "primary_output",
    "secondary_outputs",
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


def _resolve_skill_prompt(action: dict[str, Any], workspace_root: Path, prompt_placeholders: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return skill prompt path and rendered content when available."""
    skill_ref = action.get("skill_ref", "")
    # skill_ref is repo-root-relative (e.g. ".b2s/skills/..."), FRAMEWORK_ROOT is .b2s/
    repo_root = workspace.REPO_ROOT
    skill_path = (repo_root / skill_ref).resolve() if skill_ref else None
    prompt_text = None
    rendered_prompt = None
    if skill_path and skill_path.exists():
        prompt_text = skill_path.read_text(encoding="utf-8")
        rendered_prompt = _render_prompt_text(prompt_text, prompt_placeholders or {})
    return {
        "skill_ref": skill_ref,
        "skill_path": str(skill_path) if skill_path else None,
        "skill_exists": skill_path.exists() if skill_path else False,
        "skill_text": prompt_text,
        "rendered_skill_text": rendered_prompt,
    }


def _collect_inputs(action: dict[str, Any], workspace_root: Path) -> dict[str, Any]:
    """Resolve required and optional inputs for an action."""
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

    prompt_placeholders = {
        "required_inputs": [entry["path"] for entry in required_inputs],
        "optional_inputs": [entry["path"] for entry in optional_inputs],
        "resolved_required_inputs": inputs_module._flatten_resolved_paths(required_inputs),
        "resolved_optional_inputs": inputs_module._flatten_resolved_paths(optional_inputs),
        "primary_output": action.get("outputs", {}).get("primary"),
        "secondary_outputs": list(action.get("outputs", {}).get("secondary", [])),
    }

    return {
        "required_inputs": required_inputs,
        "optional_inputs": optional_inputs,
        "missing_required_inputs": missing_required,
        "inputs_ready": not missing_required,
        "prompt_placeholders": prompt_placeholders,
    }


def _action_summary(action: dict[str, Any], workspace_root: Path) -> dict[str, Any]:
    collected = _collect_inputs(action, workspace_root)
    skill = _resolve_skill_prompt(action, workspace_root, collected["prompt_placeholders"])
    output_paths = workspace.action_output_paths(action)
    return {
        "action_id": action["action_id"],
        "title": action.get("title", ""),
        "stage_id": action.get("stage_id", ""),
        "persona": action.get("persona", ""),
        "skill_ref": skill["skill_ref"],
        "skill_path": skill["skill_path"],
        "skill_exists": skill["skill_exists"],
        "artifact_template_ref": action.get("artifact_template_ref", ""),
        "output_paths": output_paths,
        "required_inputs": collected["required_inputs"],
        "optional_inputs": collected["optional_inputs"],
        "missing_required_inputs": collected["missing_required_inputs"],
        "inputs_ready": collected["inputs_ready"],
        "prompt_placeholders": collected["prompt_placeholders"],
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


def build_plan(workspace_root: Path) -> dict[str, Any]:
    """Build and return an execution plan dict for the current workflow state."""
    current_state = workspace.load_state(workspace_root)
    _, actions_by_id = workspace.load_stage_actions(workspace_root)

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

    # --- gate check ---
    if current_state.get("awaiting_human"):
        gate = current_state.get("current_gate") or {}
        return {
            "status": STATUS_GATE,
            "initiative_id": current_state.get("initiative_id"),
            "current_stage": current_state.get("current_stage"),
            "gate_id": gate.get("gate_id"),
            "gate_owner": gate.get("owner"),
            "artifact_path": gate.get("artifact_path"),
            "message": (
                f"Waiting for {gate.get('owner', 'human')} to review "
                f"artifact `{gate.get('artifact_path', '(unknown)')}`. "
                "Run `approve-current-gate` or `reject-current-gate` to continue."
            ),
            "next_cli_commands": [
                f"python .b2s/scripts/b2s_cli.py approve-current-gate --workspace-root <path>",
                f"python .b2s/scripts/b2s_cli.py reject-current-gate --workspace-root <path>",
            ],
            "action": None,
        }

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
        if workflow_type_warning:
            plan["workflow_type_warning"] = workflow_type_warning
        return plan

    # --- ready ---
    action_id = selection["selected_action"]
    action = actions_by_id[action_id]
    summary = _action_summary(action, workspace_root)
    workspace_str = str(workspace_root)

    after_skill_commands = [
        f"python .b2s/scripts/b2s_cli.py validate-artifact --workspace-root \"{workspace_str}\"",
        f"python .b2s/scripts/b2s_cli.py update-state --workspace-root \"{workspace_str}\"",
        f"python .b2s/scripts/b2s_cli.py dispatch-next --workspace-root \"{workspace_str}\"",
    ]

    plan = {
        "status": STATUS_READY,
        "initiative_id": current_state.get("initiative_id"),
        "current_stage": selection["selected_stage"],
        "workflow_source": workspace.active_workflow_source(workspace_root),
        "message": (
            f"Ready to execute `{action_id}` - {summary['title']}. "
            f"Load skill prompt at `{summary['skill_ref']}` and execute it, "
            "then run validate-artifact -> update-state -> dispatch-next."
        ),
        "action": summary,
        "after_skill_commands": after_skill_commands,
        "next_cli_commands": after_skill_commands,
    }
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
        print(f"\n  Run one of:")
        for cmd in plan["next_cli_commands"]:
            print(f"    {cmd}")

    elif status == STATUS_BLOCKED:
        print(f"\n  Blocking reason: {plan.get('blocking_reason')}")

    if plan.get("workflow_type_warning"):
        print(f"\n  [WARNING] {plan['workflow_type_warning']}")

    print()
