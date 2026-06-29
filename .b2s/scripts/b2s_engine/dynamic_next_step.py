"""Standalone selector helpers for the experimental `b2s-dynamic` workflow."""

from __future__ import annotations

from pathlib import Path
import re
from typing import Any

from b2s_engine import dynamic_state, workspace


_SEVERITY_ORDER = {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3,
}

_DYNAMIC_GAP_CATEGORIES = {
    "requirements_gap",
    "architecture_gap",
    "repository_mapping_gap",
    "ui_gap",
    "integration_gap",
    "contract_gap",
    "solution_design_gap",
    "planning_gap",
    "readiness_gap",
    "human_clarification_gap",
}

_DYNAMIC_ELIGIBLE_ACTIONS = {
    "create-atomic-requirements",
    "review-initial-architecture",
    "create-architecture-rules",
    "analyze-technical-landscape",
    "map-requirements-to-systems",
    "create-ui-specification",
    "create-solution-decisions",
    "resolve-solution-design-open-questions",
    "create-delivery-skeleton",
    "create-elaboration-plan",
    "create-epic-shells",
}

_DYNAMIC_ALLOWED_ACTIONS_BY_MACRO_PHASE = {
    "requirements-and-architecture": {
        "create-atomic-requirements",
        "review-initial-architecture",
        "create-architecture-rules",
        "analyze-technical-landscape",
        "map-requirements-to-systems",
    },
    "solution-design": {
        "create-ui-specification",
        "create-solution-decisions",
        "resolve-solution-design-open-questions",
    },
    "planning-and-epic-shaping": {
        "create-delivery-skeleton",
        "create-elaboration-plan",
        "create-epic-shells",
    },
    "handoff-readiness": set(),
}

_MAX_TOTAL_ITERATIONS = 8
_MAX_REPEATED_TOP_GAP = 2


def _dynamic_assessment_path(workspace_root: Path) -> Path:
    return workspace_root / "orchestration" / "dynamic-gap-assessment.md"


def _dynamic_next_action_decision_path(workspace_root: Path) -> Path:
    return workspace_root / "orchestration" / "dynamic-next-action-decision.md"


def _dynamic_stop_decision_path(workspace_root: Path) -> Path:
    return workspace_root / "orchestration" / "dynamic-stop-decision.md"


def _clean_cell(value: str) -> str:
    return value.strip().strip("`").strip()


def _parse_suggested_actions(value: str) -> list[str]:
    parts = re.split(r"[,/]|(?:\s+or\s+)", value, flags=re.IGNORECASE)
    actions: list[str] = []
    seen: set[str] = set()
    for part in parts:
        candidate = _clean_cell(part)
        if not candidate or candidate in seen:
            continue
        seen.add(candidate)
        actions.append(candidate)
    return actions


def _markdown_row_value(markdown_text: str, label: str) -> str | None:
    pattern = re.compile(rf"(?mi)^\|\s*{re.escape(label)}\s*\|\s*([^|]+?)\s*\|")
    match = pattern.search(markdown_text)
    return match.group(1).strip() if match else None


def _parse_ranked_gaps(markdown_text: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    in_table = False

    for raw_line in markdown_text.splitlines():
        line = raw_line.strip()
        if not in_table:
            if line == "## Ranked Gaps":
                in_table = True
            continue

        if not line:
            continue
        if line.startswith("## "):
            break
        if not line.startswith("|"):
            continue

        cells = [_clean_cell(cell) for cell in line.split("|")[1:-1]]
        if len(cells) != 6:
            continue
        if cells[0] == "Gap ID" or all(set(cell) <= {"-"} for cell in cells if cell):
            continue

        rows.append(
            {
                "gap_id": cells[0],
                "category": cells[1],
                "severity": cells[2].lower(),
                "summary": cells[3],
                "evidence": cells[4],
                "suggested_actions": _parse_suggested_actions(cells[5]),
            }
        )

    rows.sort(key=lambda row: (_SEVERITY_ORDER.get(row["severity"], 99), row["gap_id"]))
    return rows


def _top_gap(gaps: list[dict[str, Any]]) -> dict[str, Any] | None:
    return gaps[0] if gaps else None


def _allowed_actions_for_macro_phase(macro_phase: str | None) -> set[str]:
    if not macro_phase:
        return set(_DYNAMIC_ELIGIBLE_ACTIONS)
    return _DYNAMIC_ALLOWED_ACTIONS_BY_MACRO_PHASE.get(macro_phase, set())


def read_dynamic_gap_assessment(workspace_root: Path) -> dict[str, Any]:
    path = _dynamic_assessment_path(workspace_root)
    if not path.exists():
        return {
            "overall": "fail",
            "path": path,
            "reason": "dynamic gap assessment artifact is missing",
            "gaps": [],
        }

    text = path.read_text(encoding="utf-8")
    gaps = _parse_ranked_gaps(text)
    invalid_categories = sorted(
        {gap["category"] for gap in gaps if gap["category"] not in _DYNAMIC_GAP_CATEGORIES}
    )
    if invalid_categories:
        return {
            "overall": "fail",
            "path": path,
            "reason": (
                "dynamic gap assessment contains unsupported categories: "
                + ", ".join(invalid_categories)
            ),
            "gaps": gaps,
        }
    macro_phase = _markdown_row_value(text, "Current macro phase")
    confidence = _markdown_row_value(text, "Assessment confidence")
    return {
        "overall": "pass",
        "path": path,
        "reason": None,
        "macro_phase": macro_phase,
        "confidence": confidence.lower() if confidence else None,
        "gaps": gaps,
    }


def read_dynamic_next_action_decision(workspace_root: Path) -> dict[str, Any]:
    path = _dynamic_next_action_decision_path(workspace_root)
    if not path.exists():
        return {
            "overall": "fail",
            "path": path,
            "reason": "dynamic next-action decision artifact is missing",
        }

    text = path.read_text(encoding="utf-8")
    return {
        "overall": "pass",
        "path": path,
        "reason": None,
        "selected_action": _markdown_row_value(text, "Selected action"),
        "macro_phase": _markdown_row_value(text, "Current macro phase"),
        "primary_gap": _markdown_row_value(text, "Primary gap addressed"),
        "confidence": (_markdown_row_value(text, "Decision confidence") or "").lower() or None,
    }


def read_dynamic_stop_decision(workspace_root: Path) -> dict[str, Any]:
    path = _dynamic_stop_decision_path(workspace_root)
    if not path.exists():
        return {
            "overall": "fail",
            "path": path,
            "reason": "dynamic stop decision artifact is missing",
        }

    text = path.read_text(encoding="utf-8")
    return {
        "overall": "pass",
        "path": path,
        "reason": None,
        "outcome": (_markdown_row_value(text, "Outcome") or "").lower() or None,
        "macro_phase": _markdown_row_value(text, "Current macro phase"),
        "confidence": (_markdown_row_value(text, "Decision confidence") or "").lower() or None,
        "stop_reason": _markdown_row_value(text, "Stop reason"),
    }


def select_next_dynamic_action(
    workspace_root: Path,
    state: dict[str, Any],
) -> dict[str, Any]:
    ensured_state = dynamic_state.ensure_dynamic_state_defaults(dict(state))
    if not dynamic_state.is_dynamic_workflow(ensured_state):
        return {
            "overall": "fail",
            "selected_action": None,
            "selected_stage": ensured_state.get("current_stage"),
            "reason": None,
            "blocking_reason": "workflow is not `b2s-dynamic`",
            "ready_actions": [],
        }

    action_status = ensured_state.get("action_status", {})
    current_stage = ensured_state.get("current_stage") or "0-dynamic-assessment"

    if current_stage == "0-dynamic-assessment" and action_status.get("assess-dynamic-gaps") not in workspace.ACTION_STATUSES_COMPLETE:
        return {
            "overall": "pass",
            "selected_action": "assess-dynamic-gaps",
            "selected_stage": "0-dynamic-assessment",
            "reason": "run the dynamic assessment stage",
            "blocking_reason": None,
            "ready_actions": ["assess-dynamic-gaps"],
            "dynamic_gap_backlog": ensured_state.get("dynamic_gap_backlog", []),
        }

    assessment = read_dynamic_gap_assessment(workspace_root)
    if assessment["overall"] != "pass":
        if "missing" in (assessment.get("reason") or ""):
            return {
                "overall": "pass",
                "selected_action": "assess-dynamic-gaps",
                "selected_stage": "0-dynamic-assessment",
                "reason": "bootstrap dynamic workflow by creating the initial gap assessment",
                "blocking_reason": None,
                "ready_actions": ["assess-dynamic-gaps"],
                "dynamic_gap_backlog": [],
            }

        selected_stage = ensured_state.get("current_stage") or "0-dynamic-assessment"
        return {
            "overall": "fail",
            "selected_action": None,
            "selected_stage": selected_stage,
            "reason": None,
            "blocking_reason": assessment["reason"],
            "ready_actions": [],
            "dynamic_gap_backlog": [],
        }

    top_gap = _top_gap(assessment["gaps"])
    previous_assessment = ensured_state.get("dynamic_last_assessment") or {}
    repeat_gap_count = int(ensured_state.get("dynamic_repeat_gap_count", 0) or 0)

    if (
        top_gap
        and previous_assessment.get("gap_id") == top_gap["gap_id"]
        and current_stage == "0-dynamic-assessment"
    ):
        repeat_gap_count += 1
    elif top_gap:
        repeat_gap_count = 1

    if int(ensured_state.get("dynamic_iteration_count", 0) or 0) >= _MAX_TOTAL_ITERATIONS:
        return {
            "overall": "fail",
            "selected_action": None,
            "selected_stage": "2-dynamic-stop-review",
            "reason": None,
            "blocking_reason": "iteration_budget",
            "ready_actions": [],
            "dynamic_macro_phase": assessment["macro_phase"],
            "dynamic_confidence": assessment["confidence"],
            "dynamic_gap_backlog": assessment["gaps"],
            "dynamic_stop_reason": "iteration_budget",
            "dynamic_repeat_gap_count": repeat_gap_count,
        }

    if top_gap and repeat_gap_count >= _MAX_REPEATED_TOP_GAP and current_stage == "0-dynamic-assessment":
        return {
            "overall": "fail",
            "selected_action": None,
            "selected_stage": "2-dynamic-stop-review",
            "reason": None,
            "blocking_reason": "no_progress",
            "ready_actions": [],
            "dynamic_macro_phase": assessment["macro_phase"],
            "dynamic_confidence": assessment["confidence"],
            "dynamic_gap_backlog": assessment["gaps"],
            "dynamic_stop_reason": "no_progress",
            "dynamic_repeat_gap_count": repeat_gap_count,
            "dynamic_gap_id": top_gap["gap_id"],
            "dynamic_gap_category": top_gap["category"],
            "dynamic_gap_severity": top_gap["severity"],
        }

    if (
        current_stage in {"0-dynamic-assessment", "1-dynamic-selection"}
        and action_status.get("select-dynamic-next-action") not in workspace.ACTION_STATUSES_COMPLETE
    ):
        return {
            "overall": "pass",
            "selected_action": "select-dynamic-next-action",
            "selected_stage": "1-dynamic-selection",
            "reason": "run the dynamic selection stage",
            "blocking_reason": None,
            "ready_actions": ["select-dynamic-next-action"],
            "dynamic_macro_phase": assessment["macro_phase"],
            "dynamic_confidence": assessment["confidence"],
            "dynamic_gap_backlog": assessment["gaps"],
        }

    if (
        current_stage in {
            "0-dynamic-assessment",
            "1-dynamic-selection",
            "2-dynamic-stop-review",
        }
        and action_status.get("select-dynamic-next-action") in workspace.ACTION_STATUSES_COMPLETE
        and action_status.get("evaluate-dynamic-stop-condition") not in workspace.ACTION_STATUSES_COMPLETE
    ):
        return {
            "overall": "pass",
            "selected_action": "evaluate-dynamic-stop-condition",
            "selected_stage": "2-dynamic-stop-review",
            "reason": "run the dynamic stop review stage",
            "blocking_reason": None,
            "ready_actions": ["evaluate-dynamic-stop-condition"],
            "dynamic_macro_phase": assessment["macro_phase"],
            "dynamic_confidence": assessment["confidence"],
            "dynamic_gap_backlog": assessment["gaps"],
            "dynamic_repeat_gap_count": repeat_gap_count,
        }

    next_action_decision = read_dynamic_next_action_decision(workspace_root)
    if next_action_decision["overall"] != "pass":
        return {
            "overall": "fail",
            "selected_action": None,
            "selected_stage": "1-dynamic-selection",
            "reason": None,
            "blocking_reason": next_action_decision["reason"],
            "ready_actions": [],
            "dynamic_macro_phase": assessment["macro_phase"],
            "dynamic_confidence": assessment["confidence"],
            "dynamic_gap_backlog": assessment["gaps"],
            "dynamic_repeat_gap_count": repeat_gap_count,
        }

    stop_decision = read_dynamic_stop_decision(workspace_root)
    if stop_decision["overall"] != "pass":
        return {
            "overall": "fail",
            "selected_action": None,
            "selected_stage": "2-dynamic-stop-review",
            "reason": None,
            "blocking_reason": stop_decision["reason"],
            "ready_actions": [],
            "dynamic_macro_phase": assessment["macro_phase"],
            "dynamic_confidence": assessment["confidence"],
            "dynamic_gap_backlog": assessment["gaps"],
            "dynamic_repeat_gap_count": repeat_gap_count,
        }

    if stop_decision["outcome"] == "pause_for_human":
        return {
            "overall": "fail",
            "selected_action": None,
            "selected_stage": "2-dynamic-stop-review",
            "reason": None,
            "blocking_reason": stop_decision.get("stop_reason") or "dynamic stop decision requested human pause",
            "ready_actions": [],
            "dynamic_macro_phase": stop_decision["macro_phase"] or assessment["macro_phase"],
            "dynamic_confidence": stop_decision["confidence"] or assessment["confidence"],
            "dynamic_gap_backlog": assessment["gaps"],
            "dynamic_stop_reason": stop_decision.get("stop_reason"),
            "dynamic_repeat_gap_count": repeat_gap_count,
        }

    if stop_decision["outcome"] == "stop":
        return {
            "overall": "pass",
            "selected_action": None,
            "selected_stage": "2-dynamic-stop-review",
            "reason": "dynamic stop decision ended the loop",
            "blocking_reason": None,
            "ready_actions": [],
            "dynamic_macro_phase": stop_decision["macro_phase"] or assessment["macro_phase"],
            "dynamic_confidence": stop_decision["confidence"] or assessment["confidence"],
            "dynamic_gap_backlog": assessment["gaps"],
            "dynamic_stop_reason": stop_decision.get("stop_reason"),
            "dynamic_repeat_gap_count": repeat_gap_count,
        }

    selected_action = next_action_decision.get("selected_action")
    if selected_action not in _DYNAMIC_ELIGIBLE_ACTIONS:
        return {
            "overall": "fail",
            "selected_action": None,
            "selected_stage": "1-dynamic-selection",
            "reason": None,
            "blocking_reason": "dynamic next-action decision selected an unsupported specialist action",
            "ready_actions": [],
            "dynamic_macro_phase": next_action_decision["macro_phase"] or assessment["macro_phase"],
            "dynamic_confidence": next_action_decision["confidence"] or assessment["confidence"],
            "dynamic_gap_backlog": assessment["gaps"],
            "dynamic_repeat_gap_count": repeat_gap_count,
        }

    decision_macro_phase = next_action_decision["macro_phase"] or assessment["macro_phase"]
    allowed_actions = _allowed_actions_for_macro_phase(decision_macro_phase)
    if selected_action not in allowed_actions:
        return {
            "overall": "fail",
            "selected_action": None,
            "selected_stage": "1-dynamic-selection",
            "reason": None,
            "blocking_reason": "dynamic next-action decision selected an action outside the current macro phase",
            "ready_actions": [],
            "dynamic_macro_phase": decision_macro_phase,
            "dynamic_confidence": next_action_decision["confidence"] or assessment["confidence"],
            "dynamic_gap_backlog": assessment["gaps"],
            "dynamic_repeat_gap_count": repeat_gap_count,
        }

    selected_stage = current_stage if current_stage in {
        "0-dynamic-assessment",
        "1-dynamic-selection",
        "2-dynamic-stop-review",
    } else "2-dynamic-stop-review"

    selected_gap = next(
        (
            gap for gap in assessment["gaps"]
            if next_action_decision.get("primary_gap") in {gap["gap_id"], gap["category"]}
        ),
        None,
    )
    return {
        "overall": "pass",
        "selected_action": selected_action,
        "selected_stage": selected_stage,
        "reason": "selected from dynamic next-action decision",
        "blocking_reason": None,
        "ready_actions": [selected_action],
        "dynamic_macro_phase": decision_macro_phase,
        "dynamic_confidence": next_action_decision["confidence"] or stop_decision["confidence"] or assessment["confidence"],
        "dynamic_focus_area": selected_gap["category"] if selected_gap else next_action_decision.get("primary_gap"),
        "dynamic_goal": selected_gap["summary"] if selected_gap else None,
        "dynamic_gap_backlog": assessment["gaps"],
        "dynamic_gap_id": selected_gap["gap_id"] if selected_gap else None,
        "dynamic_gap_category": selected_gap["category"] if selected_gap else None,
        "dynamic_gap_severity": selected_gap["severity"] if selected_gap else None,
        "dynamic_repeat_gap_count": repeat_gap_count,
    }


def build_dynamic_next_step_preview(workspace_root: Path) -> dict[str, Any]:
    workspace_root = workspace.resolve_workspace_root(workspace_root)
    state = workspace.load_state(workspace_root)
    return select_next_dynamic_action(workspace_root, state)
