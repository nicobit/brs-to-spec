"""Workspace helpers for the staged `.b2s` engine."""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
from typing import Any

import yaml


FRAMEWORK_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = FRAMEWORK_ROOT.parent

ACTION_STATUSES_COMPLETE = {"ai_validated", "accepted"}
ACTION_STATUSES_TERMINAL = ACTION_STATUSES_COMPLETE | {"failed"}

DEFAULT_OUTPUTS = {
    "next-step": ".b2s/state/next-step.json",
    "collect-inputs": ".b2s/tmp/current-inputs.json",
    "validate-artifact": ".b2s/tmp/current-validation.yaml",
    "update-state": ".b2s/tmp/current-state-update.json",
    "repair-state": ".b2s/tmp/current-state-update.json",
    "reset-to-phase": ".b2s/tmp/current-state-update.json",
    "run-action": ".b2s/tmp/run-action.json",
    "retry-action": ".b2s/tmp/current-state-update.json",
    "rerun-last-action": ".b2s/tmp/rerun-last-action.json",
    "approve-current-gate": ".b2s/tmp/current-gate.json",
    "reject-current-gate": ".b2s/tmp/current-gate.json",
}


def technical_specs_root(workspace_root: Path) -> Path:
    return workspace_root / "technical-specifications"


def resolve_workspace_root(path: Path | None) -> Path:
    """Return a concrete initiative workspace root."""
    if path is None:
        raise ValueError(
            "Workspace discovery is not implemented. Pass --workspace-root to every .b2s engine command."
        )
    workspace_root = path.resolve()
    if not workspace_root.exists():
        raise FileNotFoundError(f"Workspace root does not exist: {workspace_root}")
    return workspace_root


def runtime_root(workspace_root: Path) -> Path:
    return workspace_root / ".b2s"


def state_dir(workspace_root: Path) -> Path:
    return runtime_root(workspace_root) / "state"


def tmp_dir(workspace_root: Path) -> Path:
    return runtime_root(workspace_root) / "tmp"


def execution_log_path(workspace_root: Path) -> Path:
    return state_dir(workspace_root) / "execution-log.jsonl"


def backups_dir(workspace_root: Path) -> Path:
    return state_dir(workspace_root) / "backups"


def ensure_runtime_layout(workspace_root: Path) -> None:
    """Create runtime folders and seed default state files when missing."""
    state_directory = state_dir(workspace_root)
    tmp_directory = tmp_dir(workspace_root)
    backup_directory = backups_dir(workspace_root)
    state_directory.mkdir(parents=True, exist_ok=True)
    tmp_directory.mkdir(parents=True, exist_ok=True)
    backup_directory.mkdir(parents=True, exist_ok=True)

    template_state = FRAMEWORK_ROOT / "templates" / "state" / "workflow-state.json"
    runtime_state = state_directory / "workflow-state.json"
    if not runtime_state.exists():
        shutil.copyfile(template_state, runtime_state)

    template_decisions = FRAMEWORK_ROOT / "templates" / "state" / "open-decisions.md"
    runtime_decisions = state_directory / "open-decisions.md"
    if not runtime_decisions.exists():
        shutil.copyfile(template_decisions, runtime_decisions)

    runtime_execution_log = execution_log_path(workspace_root)
    if not runtime_execution_log.exists():
        runtime_execution_log.write_text("", encoding="utf-8")


def load_json_file(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json_file(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def load_yaml_file(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def save_yaml_file(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def load_state(workspace_root: Path) -> dict[str, Any]:
    ensure_runtime_layout(workspace_root)
    state = load_json_file(state_dir(workspace_root) / "workflow-state.json")
    state.setdefault("artifact_status", {})
    state.setdefault("action_status", {})
    state.setdefault("quality_gates_triggered", [])
    state.setdefault("optional_artifacts_requested", [])
    state.setdefault("current_gate", None)
    return state


def save_state(workspace_root: Path, state: dict[str, Any]) -> None:
    save_json_file(state_dir(workspace_root) / "workflow-state.json", state)


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def _next_execution_entry_id(path: Path) -> str:
    if not path.exists():
        return "RUN-00001"
    line_count = 0
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                line_count += 1
    return f"RUN-{line_count + 1:05d}"


def append_execution_log(
    workspace_root: Path,
    *,
    command: str,
    overall: str,
    action_id: str | None = None,
    details: dict[str, Any] | None = None,
) -> None:
    ensure_runtime_layout(workspace_root)
    state = load_state(workspace_root)
    path = execution_log_path(workspace_root)
    entry = {
        "entry_id": _next_execution_entry_id(path),
        "timestamp": _timestamp(),
        "command": command,
        "overall": overall,
        "initiative_id": state.get("initiative_id"),
        "action_id": action_id,
        "current_stage": state.get("current_stage"),
        "active_action": state.get("active_action"),
        "next_action": state.get("next_action"),
        "awaiting_human": state.get("awaiting_human"),
        "blocked_reason": state.get("blocked_reason"),
        "state_validated": state.get("state_validated"),
    }
    if details:
        entry["details"] = details
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=True) + "\n")


def resolve_output_path(command: str, workspace_root: Path, output: Path | None) -> Path:
    if output is not None:
        if output.is_absolute():
            return output.resolve()
        return (workspace_root / output).resolve()
    relative = DEFAULT_OUTPUTS[command]
    return (workspace_root / relative).resolve()


def active_workflow_source(workspace_root: Path) -> str:
    """Return 'local' if initiative has its own workflow files, 'central' otherwise."""
    local = workspace_root / ".b2s" / "workflow" / "stage-actions.yaml"
    return "local" if local.exists() else "central"


def _resolve_workflow_path(filename: str, workspace_root: Path | None) -> Path:
    """Return initiative-local workflow file if present, otherwise central framework file."""
    if workspace_root is not None:
        local = workspace_root / ".b2s" / "workflow" / filename
        if local.exists():
            return local
    return FRAMEWORK_ROOT / "workflow" / filename


def load_stage_actions(
    workspace_root: Path | None = None,
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    payload = load_yaml_file(_resolve_workflow_path("stage-actions.yaml", workspace_root))
    actions = payload["actions"]
    by_id = {action["action_id"]: action for action in actions}
    return actions, by_id


def load_workflow_definition(
    workspace_root: Path | None = None,
) -> dict[str, Any]:
    return load_yaml_file(_resolve_workflow_path("workflow-definition.yaml", workspace_root))


def action_output_paths(action: dict[str, Any]) -> list[str]:
    outputs = action.get("outputs", {})
    paths = []
    primary = outputs.get("primary")
    if primary:
        paths.append(primary)
    paths.extend(outputs.get("secondary", []))
    return paths


def artifact_exists(workspace_root: Path, relative_path: str) -> bool:
    artifact_path = workspace_root / relative_path
    if relative_path.endswith("/"):
        return artifact_path.exists() and artifact_path.is_dir()
    if artifact_path.is_dir():
        return True
    return artifact_path.exists()


def resolve_input_pattern(workspace_root: Path, pattern: str) -> tuple[bool, list[str]]:
    if "*" in pattern or "?" in pattern:
        matches = sorted(
            path.relative_to(workspace_root).as_posix()
            for path in workspace_root.glob(pattern)
        )
        return bool(matches), matches
    exists = artifact_exists(workspace_root, pattern)
    matches = [pattern] if exists else []
    return exists, matches


def read_action_id_from_state_or_args(
    state: dict[str, Any],
    action_id: str | None,
) -> str:
    if action_id:
        return action_id
    if state.get("active_action"):
        return state["active_action"]
    if state.get("next_action"):
        return state["next_action"]
    raise ValueError("No action ID was provided and workflow state has no active or next action.")
