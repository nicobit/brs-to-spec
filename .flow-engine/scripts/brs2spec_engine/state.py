"""State updates — workflow-state.json, event-log.jsonl, open-decisions.md."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .workspace import workflow_state_path, event_log_path, state_dir


class StateError(Exception):
    pass


def load_workflow_state(workspace: Path) -> dict:
    path = workflow_state_path(workspace)
    if not path.exists():
        raise StateError(f"workflow-state.json not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def update_state(
    workspace: Path,
    event: dict,
    result: dict,
    output_path: Path,
) -> dict:
    """
    Update workflow-state.json and append to event-log.jsonl based on the
    validated event and result. Writes a machine-readable summary to output_path.
    Returns the summary dict.
    """
    event_id = event.get("event_id", "UNKNOWN")
    status = result.get("status", "fail")
    artifacts_written: list[str] = result.get("artifacts_written") or []
    now = _now_iso()

    state = load_workflow_state(workspace)

    # update active_events
    active: list[str] = state.get("active_events") or []
    if event_id in active:
        active.remove(event_id)

    # update last_completed_event / failed_events
    if status == "pass":
        state["last_completed_event"] = event_id
        failed: list[str] = state.get("failed_events") or []
        if event_id in failed:
            failed.remove(event_id)
        state["failed_events"] = failed
    else:
        failed = state.get("failed_events") or []
        if event_id not in failed:
            failed.append(event_id)
        state["failed_events"] = failed

    state["active_events"] = active

    # update artifact_status
    artifact_status: dict = state.get("artifact_status") or {}
    artifact_result_status = _artifact_status_for(event, status)
    for artifact_path in artifacts_written:
        entry = artifact_status.get(artifact_path) or {}
        entry["status"] = artifact_result_status
        entry["produced_by"] = event_id
        entry["last_updated"] = now
        if status == "pass":
            entry["accepted_at"] = now
        artifact_status[artifact_path] = entry
    state["artifact_status"] = artifact_status
    state["last_updated"] = now

    # write workflow-state.json
    wf_path = workflow_state_path(workspace)
    wf_path.write_text(json.dumps(state, indent=2), encoding="utf-8")

    # append event-log.jsonl (guard against duplicates)
    log_path = event_log_path(workspace)
    _append_event_log(log_path, event, result, now)

    # handle open_decisions_raised
    decisions_written: list[str] = []
    open_decisions = result.get("open_decisions_raised") or []
    if open_decisions:
        decisions_written = _write_decisions(workspace, event_id, open_decisions, now)

    summary = {
        "command": "update-state",
        "event_id": event_id,
        "status": status,
        "artifact_status_updated": list(artifacts_written),
        "decisions_written": decisions_written,
        "updated_at": now,
        "overall": "pass",
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def _artifact_status_for(event: dict, result_status: str) -> str:
    event_type = event.get("event_type", "")
    if result_status != "pass":
        return "failed"
    if event_type in ("WAIT_HUMAN", "ROUTE_INITIATIVE"):
        return "accepted"
    return "ai_validated"


def _append_event_log(log_path: Path, event: dict, result: dict, now: str) -> None:
    event_id = event.get("event_id", "UNKNOWN")

    # guard against duplicates
    if log_path.exists():
        existing = log_path.read_text(encoding="utf-8")
        for line in existing.splitlines():
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
                if entry.get("event_id") == event_id:
                    return  # already logged — do not duplicate
            except json.JSONDecodeError:
                continue

    log_entry = {
        "event_id": event_id,
        "event_type": event.get("event_type", ""),
        "action": event.get("action", ""),
        "persona": event.get("persona", ""),
        "status": result.get("status", ""),
        "completed_at": result.get("completed_at", now),
        "artifacts_written": result.get("artifacts_written") or [],
    }

    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")


def _write_decisions(
    workspace: Path,
    event_id: str,
    decisions: list,
    now: str,
) -> list[str]:
    decisions_path = state_dir(workspace) / "open-decisions.md"
    existing = decisions_path.read_text(encoding="utf-8") if decisions_path.exists() else ""

    # find last DEC-AUTO-NNN
    last_num = 0
    for m in re.finditer(r"DEC-AUTO-(\d+)", existing):
        last_num = max(last_num, int(m.group(1)))

    written: list[str] = []
    new_lines: list[str] = []

    for decision in decisions:
        if not isinstance(decision, dict):
            continue
        last_num += 1
        dec_id = f"DEC-AUTO-{last_num:03d}"
        blocking = decision.get("blocking", False)
        new_lines.append(
            f"\n## {dec_id}\n\n"
            f"**Question:** {decision.get('question', '')}\n"
            f"**Owner:** {decision.get('owner', '')}\n"
            f"**Blocking:** {blocking}\n"
            f"**Raised by:** {event_id}\n"
            f"**Raised at:** {now}\n"
        )
        if decision.get("source"):
            new_lines.append(f"**Source:** {decision['source']}\n")
        written.append(dec_id)

    if new_lines:
        decisions_path.parent.mkdir(parents=True, exist_ok=True)
        with decisions_path.open("a", encoding="utf-8") as f:
            f.writelines(new_lines)

    return written


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
