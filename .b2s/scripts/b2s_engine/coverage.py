"""Deterministic coverage computation for the `.b2s` engine.

Reads atomic-requirements.md and story files on disk, cross-references
them, and produces a coverage data structure. No LLM involved - pure
file parsing. The output is saved as JSON so the agent can format it
into fr-coverage.md without hallucinating the mapping.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _section_block(text: str, heading: str) -> str:
    pattern = re.compile(
        rf"^{re.escape(heading)}\s*\n(.*?)(?=^## |\Z)",
        flags=re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def _story_metadata_value(text: str, field: str) -> str:
    pattern = re.compile(
        rf"^\|\s*{re.escape(field)}\s*\|\s*(.*?)\s*\|$",
        flags=re.MULTILINE | re.IGNORECASE,
    )
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def _extract_story_requirement_ids(text: str, heading: str) -> list[str]:
    block = _section_block(text, heading)
    if not block:
        return []
    req_ids: list[str] = []
    for line in block.splitlines():
        stripped = line.strip()
        if stripped.startswith("|") or stripped.startswith("-"):
            req_ids.extend(re.findall(r"(?<![A-Za-z])(?:FR|REQ|NFR|C)-\d{3}", stripped))
    return list(dict.fromkeys(req_ids))


def _is_spike_story_type(story_type: str) -> bool:
    return story_type.strip().lower() in {"spike", "poc", "e2e", "exploration"}


def _extract_canonical_requirements(workspace_root: Path) -> list[dict[str, str]]:
    req_path = workspace_root / "requirements" / "atomic-requirements.md"
    if not req_path.exists():
        return []

    text = _read_text(req_path)
    pattern = re.compile(
        r"^###\s+((?:FR|REQ|NFR|C)-\d{3})\s+[—-]\s+(.+?)$",
        flags=re.MULTILINE,
    )
    requirements: list[dict[str, str]] = []
    seen: set[str] = set()
    for match in pattern.finditer(text):
        req_id = match.group(1).strip()
        title = match.group(2).strip()
        if req_id not in seen:
            seen.add(req_id)
            requirements.append({"id": req_id, "title": title})
    return requirements


def _extract_open_questions(workspace_root: Path) -> dict[str, list[str]]:
    """Return {req_id: [question_text, ...]} for requirements with unresolved questions."""
    req_path = workspace_root / "requirements" / "atomic-requirements.md"
    if not req_path.exists():
        return {}

    text = _read_text(req_path)
    oq_block = _section_block(text, "## Open Questions")
    if not oq_block:
        return {}

    result: dict[str, list[str]] = {}
    for line in oq_block.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.split("|")]
        cells = [c for c in cells if c]
        if len(cells) < 4:
            continue
        if cells[0].startswith("OQ-") or cells[0].startswith("---"):
            if cells[0].startswith("---"):
                continue
            question = cells[1]
            source_req = cells[2]
            req_ids = re.findall(r"(?:REQ|FR|NFR|C)-\d{3}", source_req)
            for rid in req_ids:
                result.setdefault(rid, []).append(question)
    return result


def _scan_story_files(workspace_root: Path) -> list[dict[str, Any]]:
    """Scan all story files and extract their requirement semantics."""
    epics_dir = workspace_root / "epics"
    if not epics_dir.exists():
        return []

    stories: list[dict[str, Any]] = []
    for epic_dir in sorted(d for d in epics_dir.iterdir() if d.is_dir() and d.name.startswith("E-")):
        epic_id_match = re.match(r"(E-\d{3})", epic_dir.name)
        epic_id = epic_id_match.group(1) if epic_id_match else epic_dir.name

        stories_dir = epic_dir / "stories"
        if not stories_dir.exists():
            continue

        for story_file in sorted(stories_dir.glob("S-*.md")):
            if story_file.name.endswith(".prompt.md"):
                continue

            text = _read_text(story_file)
            story_id_match = re.match(r"(S-\d{3}\.\d+)", story_file.stem)
            if not story_id_match:
                heading_match = re.search(r"^#\s+(S-\d{3}\.\d+)", text, flags=re.MULTILINE)
                if heading_match:
                    story_id_match = heading_match
            story_id = story_id_match.group(1) if story_id_match else story_file.stem

            feature_num = re.match(r"S-(\d{3})", story_id)
            feature_id = f"F-{feature_num.group(1)}" if feature_num else story_id

            story_type = _story_metadata_value(text, "Story Type").lower()
            implemented_reqs = _extract_story_requirement_ids(text, "## Requirements Implemented")
            referenced_reqs = _extract_story_requirement_ids(text, "## Requirements Referenced")
            linked_reqs = implemented_reqs + [req for req in referenced_reqs if req not in implemented_reqs]

            if not linked_reqs:
                for heading in ("## Linked Requirements", "## Requirements", "## Linked REQs"):
                    block = _section_block(text, heading)
                    if not block:
                        continue
                    linked_reqs.extend(re.findall(r"(?<![A-Za-z])(?:FR|REQ|NFR|C)-\d{3}", block))

            linked_reqs = list(dict.fromkeys(linked_reqs))
            has_open_questions = "## Open Questions" in text

            stories.append({
                "story_id": story_id,
                "feature_id": feature_id,
                "epic_id": epic_id,
                "file_path": story_file.relative_to(workspace_root).as_posix(),
                "story_type": story_type,
                "is_spike": _is_spike_story_type(story_type),
                "implemented_requirements": implemented_reqs,
                "referenced_requirements": referenced_reqs,
                "linked_requirements": linked_reqs,
                "has_open_questions_section": has_open_questions,
            })

    return stories


def _extract_fr_to_req_mapping(workspace_root: Path) -> dict[str, str]:
    """Extract the Source FR -> REQ mapping table from atomic-requirements.md."""
    req_path = workspace_root / "requirements" / "atomic-requirements.md"
    if not req_path.exists():
        return {}

    text = _read_text(req_path)
    mapping_block = _section_block(text, "## Source FR -> REQ Mapping")
    if not mapping_block:
        mapping_block = _section_block(text, "## Source FR → REQ Mapping")
    if not mapping_block:
        return {}

    result: dict[str, str] = {}
    for line in mapping_block.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.split("|")]
        cells = [c for c in cells if c]
        if len(cells) < 2:
            continue
        fr_id = cells[0]
        req_id = cells[1]
        if re.fullmatch(r"(?:FR|NFR)-\d{3}", fr_id) and re.fullmatch(r"REQ-\d{3}", req_id):
            result[fr_id] = req_id
    return result


def _extract_skeleton_requirement_assignments(workspace_root: Path) -> dict[str, dict[str, str]]:
    """Parse the delivery skeleton Requirement Coverage table."""
    skeleton_path = workspace_root / "planning" / "delivery-skeleton.md"
    if not skeleton_path.exists():
        return {}

    text = _read_text(skeleton_path)
    block = _section_block(text, "## Requirement Coverage")
    if not block:
        block = _section_block(text, "## Requirement Coverage Summary")
    if not block:
        return {}

    mapping: dict[str, dict[str, str]] = {}
    for line in block.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.split("|")]
        cells = [c for c in cells if c]
        if len(cells) < 3:
            continue
        req_id = cells[0]
        feature_id = cells[1] if len(cells) > 1 else ""
        epic_id = cells[2] if len(cells) > 2 else ""
        status = cells[3] if len(cells) > 3 else ""
        if re.fullmatch(r"(?:FR|REQ|NFR|C)-\d{3}", req_id) and re.match(r"E-\d{3}", epic_id):
            mapping[req_id] = {
                "feature": feature_id,
                "epic": epic_id,
                "status": status,
            }
    return mapping


def _extract_skeleton_req_to_epic(workspace_root: Path) -> dict[str, str]:
    assignments = _extract_skeleton_requirement_assignments(workspace_root)
    return {
        req_id: details["epic"]
        for req_id, details in assignments.items()
        if details.get("epic")
    }


def _elaborated_epics(workspace_root: Path) -> set[str]:
    """Return the set of epic IDs that have been elaborated (have story files)."""
    epics_dir = workspace_root / "epics"
    if not epics_dir.exists():
        return set()

    elaborated: set[str] = set()
    for epic_dir in epics_dir.iterdir():
        if not epic_dir.is_dir() or not epic_dir.name.startswith("E-"):
            continue
        epic_id_match = re.match(r"(E-\d{3})", epic_dir.name)
        if not epic_id_match:
            continue
        stories_dir = epic_dir / "stories"
        if stories_dir.exists() and any(stories_dir.glob("S-*.md")):
            elaborated.add(epic_id_match.group(1))
    return elaborated


def _suggest_traceability_fixes(
    uncovered: list[dict[str, str]],
    stories: list[dict[str, Any]],
    requirements: list[dict[str, str]],
    req_to_epic: dict[str, str],
) -> list[dict[str, str]]:
    """Return honest advisory fixes rather than traceability-gaming patches."""
    stories_by_epic: dict[str, list[dict[str, Any]]] = {}
    for story in stories:
        stories_by_epic.setdefault(story["epic_id"], []).append(story)

    fixes: list[dict[str, str]] = []
    for item in uncovered:
        req_id = item["req_id"]
        assigned_epic = item.get("assigned_epic", "")
        if assigned_epic == "—" or not assigned_epic:
            fixes.append({
                "req_id": req_id,
                "title": item["title"],
                "action": "no_epic_assigned",
                "reason": "requirement has no epic assignment in delivery skeleton",
            })
            continue

        epic_stories = stories_by_epic.get(assigned_epic, [])
        if not epic_stories:
            fixes.append({
                "req_id": req_id,
                "title": item["title"],
                "action": "no_stories_in_epic",
                "assigned_epic": assigned_epic,
                "reason": f"epic {assigned_epic} has no story files",
            })
            continue

        best_story = max(epic_stories, key=lambda s: len(s["linked_requirements"]))
        weak_status = item.get("status", "")
        if weak_status == "Referenced Only":
            fixes.append({
                "req_id": req_id,
                "title": item["title"],
                "action": "needs_implementation_story",
                "target_story_file": best_story["file_path"],
                "target_story_id": best_story["story_id"],
                "assigned_epic": assigned_epic,
                "reason": f"{req_id} is only referenced today; add or split a real implementation story in {assigned_epic}",
            })
            continue

        if weak_status == "Spike Only":
            fixes.append({
                "req_id": req_id,
                "title": item["title"],
                "action": "needs_non_spike_implementation_story",
                "target_story_file": best_story["file_path"],
                "target_story_id": best_story["story_id"],
                "assigned_epic": assigned_epic,
                "reason": f"{req_id} is only carried by spike/POC coverage; create a non-spike implementation story in {assigned_epic}",
            })
            continue

        fixes.append({
            "req_id": req_id,
            "title": item["title"],
            "action": "needs_implementation_story",
            "target_story_file": best_story["file_path"],
            "target_story_id": best_story["story_id"],
            "assigned_epic": assigned_epic,
            "reason": f"no story implements {req_id}; create or split a story in {assigned_epic} (candidate context: {best_story['file_path']})",
        })

    return fixes


def compute_coverage(workspace_root: Path) -> dict[str, Any]:
    """Compute the full coverage data from files on disk."""
    requirements = _extract_canonical_requirements(workspace_root)
    stories = _scan_story_files(workspace_root)
    open_questions = _extract_open_questions(workspace_root)
    fr_to_req = _extract_fr_to_req_mapping(workspace_root)
    req_assignments = _extract_skeleton_requirement_assignments(workspace_root)
    req_to_epic = {
        req_id: details["epic"]
        for req_id, details in req_assignments.items()
        if details.get("epic")
    }
    elaborated = _elaborated_epics(workspace_root)

    req_to_implemented_stories: dict[str, list[dict[str, Any]]] = {}
    req_to_referenced_stories: dict[str, list[dict[str, Any]]] = {}
    for story in stories:
        for req_id in story["implemented_requirements"]:
            req_to_implemented_stories.setdefault(req_id, []).append(story)
        for req_id in story["referenced_requirements"]:
            req_to_referenced_stories.setdefault(req_id, []).append(story)

    def _candidate_stories(req_id: str, source: dict[str, list[dict[str, Any]]]) -> list[tuple[dict[str, Any], str]]:
        candidates: list[tuple[dict[str, Any], str]] = []
        for story in source.get(req_id, []):
            candidates.append((story, req_id))
        mapped_req = fr_to_req.get(req_id)
        if mapped_req:
            for story in source.get(mapped_req, []):
                candidates.append((story, mapped_req))

        deduped: list[tuple[dict[str, Any], str]] = []
        seen: set[tuple[str, str]] = set()
        for story, via_req in candidates:
            key = (story["story_id"], via_req)
            if key in seen:
                continue
            seen.add(key)
            deduped.append((story, via_req))
        return deduped

    matrix: list[dict[str, str]] = []
    covered_count = 0
    in_scope_total = 0
    in_scope_covered = 0
    deferred_wave_count = 0
    referenced_only_count = 0
    spike_only_count = 0
    hard_gap_count = 0

    for req in requirements:
        req_id = req["id"]
        title = req["title"]

        assignment = req_assignments.get(req_id, {})
        assigned_epic = assignment.get("epic", "")
        assignment_status = assignment.get("status", "")
        assignment_feature = assignment.get("feature", "")
        explicit_deferred = bool(re.search(r"(?i)\bdefer(red)?\b|\blater wave\b", assignment_status))

        implemented_candidates = _candidate_stories(req_id, req_to_implemented_stories)
        non_spike_implemented = [(story, via_req) for story, via_req in implemented_candidates if not story.get("is_spike")]
        spike_implemented = [(story, via_req) for story, via_req in implemented_candidates if story.get("is_spike")]
        referenced_candidates = _candidate_stories(req_id, req_to_referenced_stories)

        status = "Not Covered"
        scope = "in_scope"
        evidence = "No story implements this requirement"
        elaboration_status = "elaborated" if assigned_epic in elaborated else ("planned" if assigned_epic else "unassigned")
        primary_story: dict[str, Any] | None = None
        evidence_via_req = req_id

        if non_spike_implemented:
            primary_story, evidence_via_req = non_spike_implemented[0]
            status = "Covered"
            evidence = f"Implemented in {primary_story['file_path']}"
        elif spike_implemented:
            primary_story, evidence_via_req = spike_implemented[0]
            status = "Spike Only"
            evidence = f"Implemented only in spike story {primary_story['file_path']}"
        elif referenced_candidates:
            primary_story, evidence_via_req = referenced_candidates[0]
            status = "Referenced Only"
            evidence = f"Only referenced in {primary_story['file_path']}"
        elif explicit_deferred and assigned_epic and assigned_epic not in elaborated:
            status = "Deferred"
            scope = "deferred_wave"
            deferred_wave_count += 1
            reason = assignment_status.strip()
            evidence = f"Deferred to {assigned_epic}: {reason}" if reason else f"Deferred to {assigned_epic}"
            elaboration_status = "planned"
        else:
            if assigned_epic:
                evidence = "No story implements this requirement"
                elaboration_status = "planned" if assigned_epic not in elaborated else "elaborated"
            else:
                evidence = "No epic or story owns this requirement"
                elaboration_status = "unassigned"

        if evidence_via_req != req_id and primary_story is not None:
            evidence = f"Via {evidence_via_req} -> {evidence}"

        if scope == "in_scope":
            in_scope_total += 1

        if primary_story is not None:
            has_oq = req_id in open_questions
            if not has_oq and evidence_via_req != req_id:
                has_oq = evidence_via_req in open_questions
            oq_propagated = "N/A"
            if has_oq:
                oq_propagated = "Yes" if primary_story["has_open_questions_section"] else "No"

            matrix.append({
                "req_id": req_id,
                "title": title,
                "epic": primary_story["epic_id"],
                "feature": primary_story["feature_id"],
                "story": primary_story["story_id"],
                "open_questions_propagated": oq_propagated,
                "evidence": evidence,
                "status": status,
                "scope": scope,
                "elaboration_status": "elaborated",
            })
            if status == "Covered":
                covered_count += 1
                in_scope_covered += 1
            elif status == "Referenced Only":
                referenced_only_count += 1
            elif status == "Spike Only":
                spike_only_count += 1
        else:
            has_oq = req_id in open_questions
            matrix.append({
                "req_id": req_id,
                "title": title,
                "epic": assigned_epic or "—",
                "feature": assignment_feature or "—",
                "story": "—",
                "open_questions_propagated": "Yes" if has_oq else "N/A",
                "evidence": evidence,
                "status": status,
                "scope": scope,
                "elaboration_status": elaboration_status,
            })
            if status == "Not Covered" and scope == "in_scope":
                hard_gap_count += 1

    total = len(matrix)
    not_covered = total - covered_count - deferred_wave_count
    pct = (covered_count * 100 // total) if total else 100
    in_scope_not_covered = in_scope_total - in_scope_covered
    in_scope_pct = (in_scope_covered * 100 // in_scope_total) if in_scope_total else 100
    weak_coverage_count = referenced_only_count + spike_only_count

    planned_assigned = sum(1 for r in requirements if req_to_epic.get(r["id"]))
    planned_unassigned = len(requirements) - planned_assigned
    planned_pct = (planned_assigned * 100 // len(requirements)) if requirements else 100

    uncovered_in_scope = [
        {
            "req_id": row["req_id"],
            "title": row["title"],
            "assigned_epic": row["epic"],
            "status": row["status"],
        }
        for row in matrix
        if row["status"] != "Covered" and row["scope"] == "in_scope"
    ]

    suggested_fixes = _suggest_traceability_fixes(
        uncovered_in_scope,
        stories,
        requirements,
        req_to_epic,
    )

    return {
        "canonical_requirements": [r for r in requirements],
        "stories": stories,
        "fr_to_req_mapping": fr_to_req,
        "open_questions_by_req": {k: v for k, v in open_questions.items()},
        "coverage_matrix": matrix,
        "elaborated_epics": sorted(elaborated),
        "req_to_epic_mapping": req_to_epic,
        "summary": {
            "total": total,
            "covered": covered_count,
            "not_covered": not_covered,
            "coverage_pct": pct,
            "in_scope_total": in_scope_total,
            "in_scope_covered": in_scope_covered,
            "in_scope_not_covered": in_scope_not_covered,
            "in_scope_pct": in_scope_pct,
            "deferred_wave_count": deferred_wave_count,
            "referenced_only_count": referenced_only_count,
            "spike_only_count": spike_only_count,
            "weak_coverage_count": weak_coverage_count,
            "hard_gap_count": hard_gap_count,
        },
        "planned_coverage": {
            "total": len(requirements),
            "assigned": planned_assigned,
            "unassigned": planned_unassigned,
            "pct": planned_pct,
        },
        "generated_coverage": {
            "total": in_scope_total,
            "covered": in_scope_covered,
            "not_covered": in_scope_not_covered,
            "pct": in_scope_pct,
            "referenced_only_count": referenced_only_count,
            "spike_only_count": spike_only_count,
            "weak_coverage_count": weak_coverage_count,
            "hard_gap_count": hard_gap_count,
            "uncovered_requirements": uncovered_in_scope,
        },
        "suggested_fixes": suggested_fixes,
    }
