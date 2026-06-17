"""list-actions — show all actions for an initiative with their current status."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from b2s_engine import workspace


_STATUS_SYMBOL = {
    "accepted": "[+]",
    "ai_validated": "[~]",
    "failed": "[!]",
    "not_run": "[-]",
    "skipped": "[/]",
}

# Mermaid node style per status
_MERMAID_STYLE = {
    "accepted": "fill:#4caf50,color:#fff,stroke:#388e3c",
    "ai_validated": "fill:#2196f3,color:#fff,stroke:#1565c0",
    "failed": "fill:#f44336,color:#fff,stroke:#b71c1c",
    "not_run": "fill:#eeeeee,color:#333,stroke:#9e9e9e",
    "skipped": "fill:#ffffff,color:#aaa,stroke:#ccc,stroke-dasharray:4",
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


def _safe_id(action_id: str) -> str:
    """Convert action_id to a valid Mermaid node ID."""
    return re.sub(r"[^a-zA-Z0-9_]", "_", action_id)


def _build_diagram(result: list[dict[str, Any]], current_stage: str | None, next_action: str | None) -> str:
    lines = [
        "```mermaid",
        "%%{init: {'theme': 'base'}}%%",
        "flowchart TD",
        "  %% Colors: green=accepted  blue=ai_validated  red=failed  grey=not_run  dashed=skipped",
        "  classDef accepted fill:#4caf50,color:#fff,stroke:#388e3c",
        "  classDef ai_validated fill:#2196f3,color:#fff,stroke:#1565c0",
        "  classDef failed fill:#f44336,color:#fff,stroke:#b71c1c",
        "  classDef not_run fill:#eeeeee,color:#333,stroke:#9e9e9e",
        "  classDef skipped fill:#fff,color:#bbb,stroke:#ccc,stroke-dasharray:4",
        "  classDef next_action fill:#ff9800,color:#fff,stroke:#e65100",
    ]

    # Group by stage
    stages: dict[str, list[dict[str, Any]]] = {}
    for entry in result:
        stages.setdefault(entry["stage_id"], []).append(entry)

    class_lines: list[str] = []

    for stage_id, entries in stages.items():
        is_current = stage_id == current_stage
        stage_label = f">> {stage_id}" if is_current else stage_id
        lines.append(f'  subgraph {_safe_id(stage_id)}["{stage_label}"]')
        for entry in entries:
            nid = _safe_id(entry["action_id"])
            label_parts = [entry["action_id"]]
            if entry["is_next"]:
                label_parts.append("NEXT")
            if entry["human_gate"]:
                label_parts.append("gate")
            label = " | ".join(label_parts)
            shape_open, shape_close = ("([", "])") if entry["human_gate"] else ("[", "]")
            lines.append(f'    {nid}{shape_open}"{label}"{shape_close}')
            css_class = "next_action" if entry["is_next"] else entry["status"]
            class_lines.append(f"  class {nid} {css_class}")
        lines.append("  end")

    # Stage-to-stage arrows (in order of first appearance)
    stage_ids = list(stages.keys())
    for i in range(len(stage_ids) - 1):
        lines.append(f"  {_safe_id(stage_ids[i])} --> {_safe_id(stage_ids[i+1])}")

    lines.extend(class_lines)
    lines.append("```")
    return "\n".join(lines)


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

    diagram_mode = getattr(args, "diagram", False)

    if diagram_mode:
        print(_build_diagram(result, current_stage, next_action))
        print(f"\nCurrent stage : {current_stage or '—'}")
        print(f"Next action   : {next_action or '—'} (orange)")
        print("green=accepted  blue=ai_validated  orange=next  grey=not_run  dashed=skipped  red=failed")
        return

    # Text list output
    last_stage = None
    for entry in result:
        if entry["stage_id"] != last_stage:
            print(f"\n## {entry['stage_id']}")
            last_stage = entry["stage_id"]
        symbol = _STATUS_SYMBOL.get(entry["status"], "    ")
        marker = " <-- next" if entry["is_next"] else ""
        gate = " [gate]" if entry["human_gate"] else ""
        skip_note = "  (conditions not met)" if entry["status"] == "skipped" else ""
        print(f"  {symbol}  {entry['action_id']}{gate}{marker}{skip_note}")

    print(f"\nCurrent stage : {current_stage or '—'}")
    print(f"Next action   : {next_action or '—'}")
    print()
    print("Legend: [+] accepted  [~] ai_validated  [!] failed  [-] not_run  [/] skipped")
