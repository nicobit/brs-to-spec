"""Selector helpers for the v2 `b2s-dynamic` adaptive loop."""

from __future__ import annotations

from pathlib import Path
import re
from typing import Any

from b2s_engine import workspace


def _iteration_log_path(workspace_root: Path) -> Path:
    return workspace_root / "orchestration" / "iteration-log.md"


def _iteration_log_says_continue(workspace_root: Path) -> bool | None:
    """Return True/False from the last Continue row, or None if log is missing."""
    log_path = _iteration_log_path(workspace_root)
    if not log_path.exists():
        return None
    text = log_path.read_text(encoding="utf-8", errors="replace")
    matches = re.findall(r"\|\s*Continue\s*\|\s*(.*?)\s*\|", text, re.IGNORECASE)
    if not matches:
        return True
    last_value = matches[-1].strip().lower()
    if last_value.startswith("no"):
        return False
    return True


def select_next_dynamic_action(
    workspace_root: Path,
    state: dict[str, Any],
) -> dict[str, Any]:
    """Iterate with orchestrate-dynamic-iteration until the log says stop."""
    action_status = state.get("action_status", {})
    current_stage = state.get("current_stage") or "0-dynamic-loop"

    if current_stage == "1-dynamic-closure":
        if action_status.get("finalize-dynamic-initiative") not in workspace.ACTION_STATUSES_COMPLETE:
            return {
                "overall": "pass",
                "selected_action": "finalize-dynamic-initiative",
                "selected_stage": "1-dynamic-closure",
                "reason": "iteration loop complete — produce implementation roadmap",
                "blocking_reason": None,
                "ready_actions": ["finalize-dynamic-initiative"],
            }
        return {
            "overall": "pass",
            "selected_action": None,
            "selected_stage": "1-dynamic-closure",
            "reason": "initiative complete — all artifacts produced",
            "blocking_reason": None,
            "ready_actions": [],
        }

    should_continue = _iteration_log_says_continue(workspace_root)
    if should_continue is False:
        return {
            "overall": "pass",
            "selected_action": "finalize-dynamic-initiative",
            "selected_stage": "1-dynamic-closure",
            "reason": "iteration log set continue: no — moving to closure",
            "blocking_reason": None,
            "ready_actions": ["finalize-dynamic-initiative"],
        }

    return {
        "overall": "pass",
        "selected_action": "orchestrate-dynamic-iteration",
        "selected_stage": "0-dynamic-loop",
        "reason": "run next adaptive iteration",
        "blocking_reason": None,
        "ready_actions": ["orchestrate-dynamic-iteration"],
    }


def build_dynamic_next_step_preview(workspace_root: Path) -> dict[str, Any]:
    workspace_root = workspace.resolve_workspace_root(workspace_root)
    state = workspace.load_state(workspace_root)
    return select_next_dynamic_action(workspace_root, state)
