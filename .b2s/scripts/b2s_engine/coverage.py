"""Deterministic coverage computation for the `.b2s` engine.

Reads atomic-requirements.md and story files on disk, cross-references
them, and produces a coverage data structure. No LLM involved — pure
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
    """Scan all story files and extract their linked requirements."""
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
            story_id = story_id_match.group(1) if story_id_match else story_file.stem

            feature_num = re.match(r"S-(\d{3})", story_id)
            feature_id = f"F-{feature_num.group(1)}" if feature_num else story_id

            linked_reqs: list[str] = []
            linked_block = _section_block(text, "## Linked Requirements")
            if linked_block:
                # Table format: | ID | Requirement |
                for line in linked_block.splitlines():
                    if line.strip().startswith("|"):
                        cells = [c.strip() for c in line.split("|")]
                        for cell in cells:
                            ids = re.findall(r"(?:FR|REQ|NFR|C)-\d{3}", cell)
                            linked_reqs.extend(ids)
                # Bullet format: - REQ-001, REQ-002, FR-001
                for line in linked_block.splitlines():
                    if line.strip().startswith("-"):
                        ids = re.findall(r"(?:FR|REQ|NFR|C)-\d{3}", line)
                        linked_reqs.extend(ids)

            if not linked_reqs:
                # Fallback: scan for requirement traceability sections or
                # inline references (handles format drift from templates)
                for heading in ("## Requirements", "## Linked REQs"):
                    block = _section_block(text, heading)
                    if block:
                        linked_reqs.extend(re.findall(
                            r"(?<![A-Za-z])(?:FR|REQ|NFR|C)-\d{3}", block
                        ))
                if not linked_reqs:
                    # Last resort: scan lines that look like traceability
                    for line in text.splitlines():
                        stripped = line.strip()
                        if re.match(r"(?i)(?:requirement|traceability|linked|covers)", stripped):
                            linked_reqs.extend(re.findall(
                                r"(?<![A-Za-z])(?:FR|REQ|NFR|C)-\d{3}", stripped
                            ))
                        elif stripped.startswith("-") and re.search(r"(?:FR|REQ|NFR|C)-\d{3}", stripped):
                            ids = re.findall(r"(?<![A-Za-z])(?:FR|REQ|NFR|C)-\d{3}", stripped)
                            if ids and len(stripped) < 120:
                                linked_reqs.extend(ids)

            linked_reqs = list(dict.fromkeys(linked_reqs))

            has_open_questions = "## Open Questions" in text

            stories.append({
                "story_id": story_id,
                "feature_id": feature_id,
                "epic_id": epic_id,
                "file_path": story_file.relative_to(workspace_root).as_posix(),
                "linked_requirements": linked_reqs,
                "has_open_questions_section": has_open_questions,
            })

    return stories


def _extract_fr_to_req_mapping(workspace_root: Path) -> dict[str, str]:
    """Extract the Source FR → REQ mapping table from atomic-requirements.md.

    Returns {FR-NNN: REQ-NNN, ...} for transitive coverage resolution.
    """
    req_path = workspace_root / "requirements" / "atomic-requirements.md"
    if not req_path.exists():
        return {}

    text = _read_text(req_path)
    mapping_block = _section_block(text, "## Source FR → REQ Mapping")
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


def compute_coverage(workspace_root: Path) -> dict[str, Any]:
    """Compute the full coverage data from files on disk.

    Returns a JSON-serializable dict with:
    - canonical_requirements: list of {id, title}
    - stories: list of {story_id, epic_id, feature_id, linked_requirements, ...}
    - fr_to_req_mapping: {FR-NNN: REQ-NNN} for transitive coverage
    - coverage_matrix: list of {req_id, title, status, epic, feature, story, ...}
    - summary: {total, covered, not_covered, coverage_pct}
    """
    requirements = _extract_canonical_requirements(workspace_root)
    stories = _scan_story_files(workspace_root)
    open_questions = _extract_open_questions(workspace_root)
    fr_to_req = _extract_fr_to_req_mapping(workspace_root)

    # Build reverse index: req_id → list of stories covering it
    req_to_stories: dict[str, list[dict[str, Any]]] = {}
    for story in stories:
        for req_id in story["linked_requirements"]:
            req_to_stories.setdefault(req_id, []).append(story)

    # Separate REQ-level (canonical) requirements from FR/NFR source entries
    canonical_ids = {r["id"] for r in requirements if r["id"].startswith("REQ-")}
    source_ids = {r["id"] for r in requirements if not r["id"].startswith("REQ-")}

    matrix: list[dict[str, str]] = []
    covered_count = 0

    for req in requirements:
        req_id = req["id"]
        title = req["title"]

        # Direct coverage: a story links to this ID
        covering_stories = req_to_stories.get(req_id, [])

        # Transitive coverage for FR/NFR: if FR-001 maps to REQ-001 and REQ-001 is covered
        mapped_req = fr_to_req.get(req_id)
        if not covering_stories and mapped_req:
            covering_stories = req_to_stories.get(mapped_req, [])

        if covering_stories:
            primary = covering_stories[0]
            has_oq = req_id in open_questions
            if not has_oq and mapped_req:
                has_oq = mapped_req in open_questions
            oq_propagated = "N/A"
            if has_oq:
                oq_propagated = "Yes" if primary["has_open_questions_section"] else "No"

            evidence = f"Linked in {primary['file_path']}"
            if mapped_req and req_id != mapped_req:
                evidence = f"Via {mapped_req} -> {primary['file_path']}"

            matrix.append({
                "req_id": req_id,
                "title": title,
                "epic": primary["epic_id"],
                "feature": primary["feature_id"],
                "story": primary["story_id"],
                "open_questions_propagated": oq_propagated,
                "evidence": evidence,
                "status": "Covered",
            })
            covered_count += 1
        else:
            has_oq = req_id in open_questions
            matrix.append({
                "req_id": req_id,
                "title": title,
                "epic": "—",
                "feature": "—",
                "story": "—",
                "open_questions_propagated": "Yes" if has_oq else "N/A",
                "evidence": "No story links to this requirement",
                "status": "Not Covered",
            })

    total = len(matrix)
    not_covered = total - covered_count
    pct = (covered_count * 100 // total) if total else 100

    return {
        "canonical_requirements": [r for r in requirements],
        "stories": stories,
        "fr_to_req_mapping": fr_to_req,
        "open_questions_by_req": {k: v for k, v in open_questions.items()},
        "coverage_matrix": matrix,
        "summary": {
            "total": total,
            "covered": covered_count,
            "not_covered": not_covered,
            "coverage_pct": pct,
        },
    }
