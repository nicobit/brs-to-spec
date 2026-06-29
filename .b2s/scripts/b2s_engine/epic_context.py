"""Computed input: epic-scoped context for per-item epic elaboration.

Extracts only the requirements, skeleton section, impacted systems,
and solution decisions relevant to a single epic. Reduces input tokens
from ~29k to ~8-10k per invocation.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _section_between_headings(text: str, start_pattern: str, level: str = "###") -> str:
    escaped = re.escape(start_pattern)
    if level == "###":
        stop = r"^#{2,3}\s+"
    else:
        stop = rf"^{level}\s+"
    pattern = re.compile(
        rf"^{level}\s+{escaped}.*?\n(.*?)(?={stop}|\Z)",
        flags=re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    if not match:
        return ""
    return match.group(0).strip()


def _extract_epic_requirements(skeleton_text: str, epic_id: str) -> list[str]:
    epic_section = _section_between_headings(skeleton_text, epic_id)
    if not epic_section:
        return []
    return re.findall(r"(?:REQ|FR|NFR|C)-\d{3}", epic_section)


def _extract_epic_skeleton_section(skeleton_text: str, epic_id: str) -> str:
    return _section_between_headings(skeleton_text, epic_id)


def _filter_requirements(req_text: str, req_ids: set[str]) -> str:
    if not req_ids:
        return ""
    lines = []
    pattern = re.compile(
        r"^###\s+((?:FR|REQ|NFR|C)-\d{3})\s+[—-]\s+(.+?)\n(.*?)(?=^###\s+(?:FR|REQ|NFR|C)-\d{3}\s+[—-]\s+|\Z)",
        flags=re.MULTILINE | re.DOTALL,
    )
    for match in pattern.finditer(req_text):
        req_id = match.group(1).strip()
        if req_id in req_ids:
            lines.append(match.group(0).strip())
    return "\n\n".join(lines)


def _filter_impacted_systems(impact_text: str, req_ids: set[str]) -> str:
    if not req_ids:
        return ""
    lines = []
    pattern = re.compile(
        r"^###\s+((?:REQ|FR|NFR)-\d{3})\s+[—-].*?\n(.*?)(?=^###\s+(?:REQ|FR|NFR)-\d{3}\s+[—-]|\Z)",
        flags=re.MULTILINE | re.DOTALL,
    )
    for match in pattern.finditer(impact_text):
        req_id = match.group(1).strip()
        if req_id in req_ids:
            lines.append(match.group(0).strip())

    cross_cutting = _section_between_headings(impact_text, "Cross-Cutting Concerns", level="##")
    if cross_cutting:
        lines.append(cross_cutting)

    new_proposed = _section_between_headings(impact_text, "New-Proposed Components", level="##")
    if new_proposed:
        lines.append(new_proposed)

    return "\n\n".join(lines)


def _filter_solution_decisions(decisions_text: str, req_ids: set[str]) -> str:
    if not req_ids:
        return ""
    sections = []

    for heading in [
        "## Key Decisions", "## Service Decisions", "## API Decisions",
        "## UI Decisions", "## Data Decisions", "## Integration Decisions",
        "## Infrastructure Decisions", "## Repository Summary",
        "## Architecture Rule Compliance",
    ]:
        section = _section_between_headings(decisions_text, heading.lstrip("# "), level="##")
        if section:
            sections.append(section)

    open_decisions = _section_between_headings(decisions_text, "Open Decisions", level="##")
    if open_decisions:
        sections.append(open_decisions)

    return "\n\n".join(sections)


def compute_epic_context(workspace_root: Path, current_item: str | None) -> dict[str, Any]:
    if not current_item:
        return {"epic_id": None, "note": "no current_item provided"}

    epic_id = current_item
    result: dict[str, Any] = {"epic_id": epic_id}

    skeleton_path = workspace_root / "planning" / "delivery-skeleton.md"
    if skeleton_path.exists():
        skeleton_text = _read_text(skeleton_path)
        req_ids_list = _extract_epic_requirements(skeleton_text, epic_id)
        req_ids = set(req_ids_list)
        section = _extract_epic_skeleton_section(skeleton_text, epic_id)
        result["epic_skeleton_section"] = section
        result["epic_requirement_ids"] = sorted(req_ids)
        title_match = re.match(
            rf"^###\s+{re.escape(epic_id)}\s+[—-]\s+(.+?)$",
            section, flags=re.MULTILINE,
        )
        result["canonical_title"] = title_match.group(1).strip() if title_match else None
    else:
        req_ids = set()
        result["epic_skeleton_section"] = ""
        result["epic_requirement_ids"] = []
        result["canonical_title"] = None

    req_path = workspace_root / "requirements" / "atomic-requirements.md"
    if req_path.exists() and req_ids:
        result["filtered_requirements"] = _filter_requirements(_read_text(req_path), req_ids)
    else:
        result["filtered_requirements"] = ""

    impact_path = workspace_root / "architecture" / "impacted-systems.md"
    if impact_path.exists() and req_ids:
        result["filtered_impacted_systems"] = _filter_impacted_systems(_read_text(impact_path), req_ids)
    else:
        result["filtered_impacted_systems"] = ""

    decisions_path = workspace_root / "architecture" / "solution-decisions.md"
    if decisions_path.exists():
        result["filtered_solution_decisions"] = _filter_solution_decisions(_read_text(decisions_path), req_ids)
    else:
        result["filtered_solution_decisions"] = ""

    return result
