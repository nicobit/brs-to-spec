"""Workspace helpers for the staged `.b2s` engine."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
from typing import Any

import yaml

from b2s_engine import action_contract


FRAMEWORK_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = FRAMEWORK_ROOT.parent

_ENGINE_SALT = "b2s-engine-v2-integrity"

ACTION_STATUSES_COMPLETE = {"ai_validated", "accepted"}
ACTION_STATUSES_TERMINAL = ACTION_STATUSES_COMPLETE | {"failed"}
ACTION_STATUS_IN_PROGRESS = "in_progress"
ACTION_STATUS_WAVE_COMPLETE = "wave_complete"

# Action lifecycle phases — enforced ordering within a single action execution.
LIFECYCLE_IDLE = "idle"
LIFECYCLE_DISPATCHED = "dispatched"
LIFECYCLE_INPUTS_COLLECTED = "inputs_collected"
LIFECYCLE_VALIDATED = "validated"

LIFECYCLE_ORDER = [LIFECYCLE_IDLE, LIFECYCLE_DISPATCHED, LIFECYCLE_INPUTS_COLLECTED, LIFECYCLE_VALIDATED]

DEFAULT_OUTPUTS = {
    "next-step": ".b2s/state/next-step.json",
    "collect-inputs": ".b2s/tmp/current-inputs.json",
    "validate-artifact": ".b2s/tmp/current-validation.yaml",
    "update-state": ".b2s/tmp/current-state-update.json",
    "repair-state": ".b2s/tmp/current-state-update.json",
    "reset-to-phase": ".b2s/tmp/current-state-update.json",
    "finalize-action": ".b2s/tmp/finalize-action.json",
    "run-action": ".b2s/tmp/run-action.json",
    "reopen-action": ".b2s/tmp/run-action.json",
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
    path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")


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
    state.setdefault("action_item_status", {})
    state.setdefault("current_item", None)
    state.setdefault("quality_gates_triggered", [])
    state.setdefault("optional_artifacts_requested", [])
    state.setdefault("current_gate", None)
    state.setdefault("dynamic_goal", None)
    state.setdefault("dynamic_macro_phase", None)
    state.setdefault("dynamic_gap_backlog", [])
    state.setdefault("dynamic_focus_area", None)
    state.setdefault("dynamic_iteration_count", 0)
    state.setdefault("dynamic_last_assessment", None)
    state.setdefault("dynamic_last_selected_action", None)
    state.setdefault("dynamic_stop_reason", None)
    state.setdefault("dynamic_confidence", None)
    state.setdefault("dynamic_repeat_gap_count", 0)
    state.setdefault("current_wave", 0)
    if "action_lifecycle_phase" not in state:
        if state.get("active_action"):
            state["action_lifecycle_phase"] = LIFECYCLE_INPUTS_COLLECTED
        else:
            state["action_lifecycle_phase"] = LIFECYCLE_IDLE
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


def _compute_engine_fingerprint(
    entry_id: str,
    command: str,
    action_id: str | None,
    timestamp: str,
) -> str:
    payload = f"{_ENGINE_SALT}:{entry_id}:{command}:{action_id or ''}:{timestamp}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def _verify_entry_fingerprint(entry: dict[str, Any]) -> bool:
    fp = entry.get("engine_fingerprint")
    if not fp:
        return False
    expected = _compute_engine_fingerprint(
        entry.get("entry_id", ""),
        entry.get("command", ""),
        entry.get("action_id"),
        entry.get("timestamp", ""),
    )
    return fp == expected


def verify_execution_log(workspace_root: Path) -> list[dict[str, str]]:
    """Check every execution log entry for a valid engine fingerprint.

    Returns a list of issues for entries that are missing or have invalid
    fingerprints — indicating they were written outside the engine.
    """
    entries = _load_execution_log(workspace_root)
    issues: list[dict[str, str]] = []
    for entry in entries:
        if not _verify_entry_fingerprint(entry):
            issues.append({
                "entry_id": entry.get("entry_id", "unknown"),
                "command": entry.get("command", "unknown"),
                "action_id": entry.get("action_id"),
                "issue": "fabricated",
                "detail": (
                    f"log entry '{entry.get('entry_id')}' for command "
                    f"'{entry.get('command')}' has no valid engine fingerprint "
                    f"— it was written outside the b2s engine"
                ),
            })
    return issues


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
    entry_id = _next_execution_entry_id(path)
    ts = _timestamp()
    entry = {
        "entry_id": entry_id,
        "timestamp": ts,
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
        "engine_fingerprint": _compute_engine_fingerprint(entry_id, command, action_id, ts),
    }
    if details:
        entry["details"] = details
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=True) + "\n")


def check_lifecycle_phase(
    state: dict[str, Any],
    required_phase: str,
    command: str,
) -> str | None:
    """Return an error message if the current lifecycle phase prevents running ``command``.

    Returns None when the phase is acceptable.
    Only enforced when the state has an ``active_action`` — otherwise the
    command is assumed to be a standalone invocation (e.g. tests, manual runs)
    and the check is skipped.
    """
    if not state.get("active_action"):
        return None
    current = state.get("action_lifecycle_phase")
    if current is None:
        return None
    required_idx = LIFECYCLE_ORDER.index(required_phase) if required_phase in LIFECYCLE_ORDER else -1
    current_idx = LIFECYCLE_ORDER.index(current) if current in LIFECYCLE_ORDER else -1
    if current_idx < required_idx:
        return (
            f"Cannot run `{command}`: action lifecycle phase is '{current}' "
            f"but must be at least '{required_phase}'. "
            f"Run the preceding step first."
        )
    return None


def advance_lifecycle_phase(state: dict[str, Any], new_phase: str) -> None:
    """Set the lifecycle phase. Use LIFECYCLE_IDLE to reset after update-state."""
    state["action_lifecycle_phase"] = new_phase


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


def _workflow_type_for_workspace(workspace_root: Path | None) -> str | None:
    if workspace_root is None:
        return None

    record_path = workspace_root / ".b2s" / "workflow" / "workflow-type.json"
    if record_path.exists():
        try:
            payload = load_json_file(record_path)
        except Exception:
            payload = {}
        workflow_type = payload.get("workflow_type")
        if workflow_type:
            return workflow_type

    state_path = state_dir(workspace_root) / "workflow-state.json"
    if state_path.exists():
        try:
            payload = load_json_file(state_path)
        except Exception:
            payload = {}
        workflow_type = payload.get("workflow_type")
        if workflow_type:
            return workflow_type

    return None


def load_stage_actions(
    workspace_root: Path | None = None,
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    payload = load_yaml_file(_resolve_workflow_path("stage-actions.yaml", workspace_root))
    actions = action_contract.normalize_actions(payload["actions"])
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


def _parse_elaboration_waves(workspace_root: Path) -> list[list[str]] | None:
    """Parse elaboration-plan.md and return a list of waves, each a list of epic IDs.

    Supports two formats:
    1. Single table with a Wave column: ``| Wave 1 | E-001 — ... | ... |``
    2. Separate heading + table per wave: ``### Wave 1 — ...`` followed by
       a table whose rows contain epic IDs.

    Returns None if the elaboration plan does not exist or has no parseable waves.
    """
    import re as _re
    plan_path = workspace_root / "planning" / "elaboration-plan.md"
    if not plan_path.exists():
        return None
    text = plan_path.read_text(encoding="utf-8")

    # --- Strategy 1: single table with Wave column ---
    in_table = False
    waves: list[list[str]] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("|") and "Wave" in stripped and "Epic" in stripped and "Rationale" in stripped:
            in_table = True
            continue
        if in_table and stripped.startswith("|---"):
            continue
        if in_table and stripped.startswith("|"):
            cells = [c.strip() for c in stripped.split("|")]
            cells = [c for c in cells if c]
            if len(cells) >= 2 and _re.search(r"[Ww]ave", cells[0]):
                epic_ids = _re.findall(r"E-\d{3}", cells[1])
                if epic_ids:
                    waves.append(epic_ids)
        elif in_table and not stripped.startswith("|"):
            in_table = False

    if waves:
        return waves

    # --- Strategy 2: separate ### Wave N headings with tables ---
    current_wave_epics: list[str] = []
    in_wave = False
    for line in text.splitlines():
        stripped = line.strip()
        if _re.match(r"^#{2,3}\s+[Ww]ave\s+\d+", stripped):
            if current_wave_epics:
                waves.append(current_wave_epics)
                current_wave_epics = []
            in_wave = True
            epic_ids_in_heading = _re.findall(r"E-\d{3}", stripped)
            current_wave_epics.extend(epic_ids_in_heading)
            continue
        if in_wave and stripped.startswith("|"):
            if stripped.startswith("|---"):
                continue
            cells = [c.strip() for c in stripped.split("|")]
            cells = [c for c in cells if c]
            if cells:
                first_cell_ids = _re.findall(r"E-\d{3}", cells[0])
                for eid in first_cell_ids:
                    if eid not in current_wave_epics:
                        current_wave_epics.append(eid)
        elif in_wave and stripped.startswith("#"):
            if current_wave_epics:
                waves.append(current_wave_epics)
                current_wave_epics = []
            in_wave = False

    if current_wave_epics:
        waves.append(current_wave_epics)

    return waves if waves else None


def current_wave_index(state: dict[str, Any]) -> int:
    """Return the 0-based wave index from state, defaulting to 0."""
    return state.get("current_wave", 0)


def items_for_wave(workspace_root: Path, wave_index: int) -> list[str]:
    """Return the epic IDs for a specific wave, or all items if no waves defined."""
    waves = _parse_elaboration_waves(workspace_root)
    if not waves:
        return []
    if wave_index < len(waves):
        return waves[wave_index]
    return []


def total_waves(workspace_root: Path) -> int:
    """Return the total number of waves, or 0 if no elaboration plan."""
    waves = _parse_elaboration_waves(workspace_root)
    return len(waves) if waves else 0


def all_wave_items(workspace_root: Path) -> list[str]:
    """Return all item IDs across all waves in wave order."""
    waves = _parse_elaboration_waves(workspace_root)
    if not waves:
        return []
    result: list[str] = []
    for wave in waves:
        result.extend(wave)
    return result


def resolve_item_folder(workspace_root: Path, item_id: str | None) -> str | None:
    """Resolve a bare item ID (e.g. 'E-002') to its actual folder path under epics/.

    Scans ``epics/`` for a directory whose name starts with the item ID.
    When multiple matches exist (e.g. ``E-002`` and ``E-002-ai-pre-screening``),
    prefers the slugged variant (``E-002-<slug>``) over the bare ID folder.
    Returns the workspace-relative POSIX path (e.g. 'epics/E-002-ai-pre-screening/') or
    None if no matching folder exists or no item_id is given.
    """
    if not item_id:
        return None
    epics_dir = workspace_root / "epics"
    if not epics_dir.is_dir():
        return None
    candidates = [
        entry for entry in sorted(epics_dir.iterdir())
        if entry.is_dir() and entry.name.startswith(item_id)
    ]
    if not candidates:
        return None
    # Prefer the slugged folder (E-002-<slug>) over the bare ID (E-002)
    slugged = [c for c in candidates if c.name != item_id]
    winner = slugged[0] if slugged else candidates[0]
    return winner.relative_to(workspace_root).as_posix() + "/"


def extract_items_from_source(workspace_root: Path, source_path: str, pattern: str) -> list[str]:
    """Extract item IDs from a source file using a regex pattern."""
    import re as _re
    full_path = workspace_root / source_path
    if not full_path.exists():
        return []
    text = full_path.read_text(encoding="utf-8")
    matches = _re.findall(pattern, text, flags=_re.MULTILINE)
    seen: set[str] = set()
    ordered: list[str] = []
    for match in matches:
        item_id = match.strip() if isinstance(match, str) else match[0].strip()
        if item_id not in seen:
            seen.add(item_id)
            ordered.append(item_id)
    return ordered


def order_items_by_wave(
    workspace_root: Path,
    items: list[str],
) -> list[str]:
    """Re-order items according to elaboration plan wave sequence.

    Items appearing in earlier waves come first. Items not mentioned in
    any wave are appended at the end in their original order.
    If no elaboration plan exists, returns items unchanged.
    """
    waves = _parse_elaboration_waves(workspace_root)
    if not waves:
        return items

    item_set = set(items)
    ordered: list[str] = []
    seen: set[str] = set()
    for wave in waves:
        for epic_id in wave:
            if epic_id in item_set and epic_id not in seen:
                ordered.append(epic_id)
                seen.add(epic_id)
    for item in items:
        if item not in seen:
            ordered.append(item)
    return ordered


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


def resolve_policy_reference(pattern: str) -> tuple[bool, list[str]]:
    """Resolve a framework-level policy reference."""
    if pattern.startswith(".b2s/"):
        candidate = REPO_ROOT / pattern
        exists = candidate.exists()
        return exists, [pattern] if exists else []
    candidate = REPO_ROOT / pattern
    exists = candidate.exists()
    return exists, [pattern] if exists else []


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


def _load_execution_log(workspace_root: Path) -> list[dict[str, Any]]:
    path = execution_log_path(workspace_root)
    if not path.exists():
        return []
    entries: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped:
            entries.append(json.loads(stripped))
    return entries


def _logged_commands_for_action(
    log_entries: list[dict[str, Any]],
    action_id: str,
) -> set[str]:
    return {
        entry["command"]
        for entry in log_entries
        if entry.get("action_id") == action_id
        and entry.get("overall") == "pass"
    }


_STATE_SETTING_COMMANDS = {
    "update-state",
    "approve-current-gate",
    "repair-state",
    "run-action",
    "retry-action",
    "rerun-last-action",
}


def check_state_integrity(
    workspace_root: Path,
    state: dict[str, Any],
) -> list[dict[str, str]]:
    """Detect action statuses that have no execution-log evidence or missing artifacts.

    Also checks execution log entries for valid engine fingerprints.

    Returns a list of issues found. Each issue is a dict with keys:
      action_id, status, issue, detail
    """
    log_entries = _load_execution_log(workspace_root)
    _, actions_by_id = load_stage_actions(workspace_root)
    action_status = state.get("action_status", {})
    issues: list[dict[str, str]] = []

    fingerprint_issues = verify_execution_log(workspace_root)
    issues.extend(fingerprint_issues)

    verified_entries = [e for e in log_entries if _verify_entry_fingerprint(e)]

    for action_id, status in list(action_status.items()):
        if status not in ACTION_STATUSES_COMPLETE:
            continue
        if action_id not in actions_by_id:
            continue

        logged = _logged_commands_for_action(verified_entries, action_id)
        has_engine_evidence = bool(logged & _STATE_SETTING_COMMANDS)

        action = actions_by_id[action_id]
        outputs = action_output_paths(action)
        missing_artifacts = [
            ap for ap in outputs
            if not artifact_exists(workspace_root, ap)
        ]

        if not has_engine_evidence and missing_artifacts:
            issues.append({
                "action_id": action_id,
                "status": status,
                "issue": "ghost",
                "detail": (
                    f"action '{action_id}' is '{status}' but has no verified engine log entry "
                    f"and artifact(s) missing: {missing_artifacts}"
                ),
            })
        elif not has_engine_evidence:
            issues.append({
                "action_id": action_id,
                "status": status,
                "issue": "unlogged",
                "detail": (
                    f"action '{action_id}' is '{status}' but has no verified engine log entry "
                    f"(artifacts exist on disk — status may have been set outside the engine)"
                ),
            })
        elif missing_artifacts:
            issues.append({
                "action_id": action_id,
                "status": status,
                "issue": "missing_artifact",
                "detail": (
                    f"action '{action_id}' is '{status}' with engine log, "
                    f"but artifact(s) missing: {missing_artifacts}"
                ),
            })

    return issues


def repair_ghost_actions(
    workspace_root: Path,
    state: dict[str, Any],
    issues: list[dict[str, str]],
) -> list[str]:
    """Remove state entries for ghost/missing-artifact actions. Returns repaired action IDs."""
    repaired: list[str] = []
    _, actions_by_id = load_stage_actions(workspace_root)

    for issue in issues:
        if issue["issue"] not in ("ghost", "missing_artifact"):
            continue
        action_id = issue["action_id"]
        state.get("action_status", {}).pop(action_id, None)

        action = actions_by_id.get(action_id, {})
        for ap in action_output_paths(action):
            state.get("artifact_status", {}).pop(ap, None)

        human_gate = action.get("human_gate") or {}
        gate_id = human_gate.get("gate_id")
        if gate_id:
            gate_action_id = f"gate-{gate_id}"
            state.get("action_status", {}).pop(gate_action_id, None)

        repaired.append(action_id)

    return repaired
