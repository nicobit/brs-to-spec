"""list-actions — show all actions for an initiative with their current status."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from b2s_engine import workspace


_STATUS_LABEL = {
    "accepted": "accepted",
    "ai_validated": "ai_validated",
    "failed": "failed",
    "not_run": "not_run",
}

_STATUS_SYMBOL = {
    "accepted": "[+]",
    "ai_validated": "[>]",
    "failed": "[x]",
    "not_run": "[ ]",
}


def _conditions_pass(action: dict[str, Any], state: dict[str, Any]) -> bool:
    conditions = action.get("conditions") or []
    if not conditions:
        return True
    delivery_mode = state.get("delivery_mode", "")
    execution_mode = state.get("execution_mode", "")
    quality_gates = state.get("quality_gates_triggered") or []
    for cond in conditions:
        if "in quality_gates_triggered" in cond:
            gate = cond.split(" in ")[0].strip()
            if gate not in quality_gates:
                return False
        elif "delivery_mode ==" in cond:
            val = cond.split("==")[1].strip().strip("'\"")
            if delivery_mode != val:
                return False
        elif "execution_mode ==" in cond:
            val = cond.split("==")[1].strip().strip("'\"")
            if execution_mode != val:
                return False
    return True


def run(args: Any) -> None:
    workspace_root = workspace.resolve_workspace_root(
        getattr(args, "workspace_root", None)
    )

    actions, _ = workspace.load_stage_actions(workspace_root)

    state_path = workspace_root / ".b2s" / "state" / "workflow-state.json"
    state: dict[str, Any] = {}
    if state_path.exists():
        state = json.loads(state_path.read_text(encoding="utf-8"))

    action_status: dict[str, str] = state.get("action_status", {})
    next_action: str | None = state.get("next_action")
    current_stage: str | None = state.get("current_stage")

    filter_stage: str | None = getattr(args, "stage_id", None)

    result: list[dict[str, Any]] = []
    current_stage_id = None

    for action in actions:
        stage_id = action.get("stage_id", "")
        if filter_stage and stage_id != filter_stage:
            continue

        action_id = action.get("action_id", "")
        status = action_status.get(action_id, "not_run")
        skipped = not _conditions_pass(action, state)
        is_next = action_id == next_action
        human_gate = bool((action.get("human_gate") or {}).get("required"))

        entry = {
            "stage_id": stage_id,
            "action_id": action_id,
            "title": action.get("title", ""),
            "status": "skipped" if skipped else status,
            "is_next": is_next,
            "human_gate": human_gate,
            "output": action.get("outputs", {}).get("primary", ""),
        }
        result.append(entry)

    output_path = getattr(args, "output", None)
    if output_path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps({"actions": result, "current_stage": current_stage, "next_action": next_action}, indent=2),
            encoding="utf-8",
        )

    # Human-readable output
    last_stage = None
    for entry in result:
        if entry["stage_id"] != last_stage:
            print(f"\n## {entry['stage_id']}")
            last_stage = entry["stage_id"]
        symbol = _STATUS_SYMBOL.get(entry["status"], "[ ]")
        marker = " <-- next" if entry["is_next"] else ""
        gate = " [gate]" if entry["human_gate"] else ""
        print(f"  {symbol} {entry['action_id']}{gate}{marker}")
        if entry["status"] == "skipped":
            print(f"       (skipped - conditions not met for this initiative)")

    print(f"\nCurrent stage : {current_stage or '—'}")
    print(f"Next action   : {next_action or '—'}")
    print()
    print("Legend: [+] accepted  [>] ai_validated  [x] failed  [ ] not_run")
