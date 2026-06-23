"""Validation helpers for staged `.b2s` artifacts."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Callable

from b2s_engine import workspace


Validator = Callable[[Path, Path], list[dict[str, str]]]
ProfileValidator = Callable[[Path, Path, dict[str, Any], str], list[dict[str, str]]]
NamedRuleValidator = Callable[[Path, Path, dict[str, Any], str, list[dict[str, str]]], dict[str, str]]


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _source_texts(workspace_root: Path) -> list[str]:
    paths = []
    primary = workspace_root / "input" / "brs.md"
    if primary.exists():
        paths.append(primary)
    wildcard_dir = workspace_root / "input" / "brs"
    if wildcard_dir.exists():
        paths.extend(sorted(wildcard_dir.glob("*.md")))
    return [_read_text(path) for path in paths]


def _source_text(workspace_root: Path) -> str:
    return "\n".join(_source_texts(workspace_root))


def _result(name: str, target: str, passed: bool, detail: str) -> dict[str, str]:
    return {
        "name": name,
        "target": target,
        "result": "pass" if passed else "fail",
        "detail": detail,
    }


def _named_rule_result(
    rule_name: str,
    target: str,
    passed: bool,
    detail: str,
    *,
    severity: str,
) -> dict[str, str]:
    return {
        "name": "named_validation_rule",
        "rule_name": rule_name,
        "severity": severity,
        "target": target,
        "result": "pass" if passed else "fail",
        "detail": detail,
    }


def _contains(path: Path, needle: str, name: str, detail: str) -> list[dict[str, str]]:
    text = _read_text(path)
    passed = needle in text
    return [_result(name, path.name, passed, detail if passed else f"missing `{needle}`")]


def _matches(path: Path, pattern: str, name: str, detail: str) -> list[dict[str, str]]:
    text = _read_text(path)
    passed = re.search(pattern, text, flags=re.MULTILINE) is not None
    return [_result(name, path.name, passed, detail if passed else f"pattern not found: {pattern}")]


def _non_empty_file(path: Path, workspace_root: Path | None = None) -> list[dict[str, str]]:
    text = _read_text(path).strip()
    return [
        _result(
            "non_empty_file",
            path.name,
            bool(text),
            "artifact has content" if text else "artifact is empty",
        )
    ]


def _non_empty_directory(path: Path, workspace_root: Path | None = None) -> list[dict[str, str]]:
    children = [child for child in path.iterdir()]
    return [
        _result(
            "non_empty_directory",
            path.name,
            bool(children),
            "directory contains generated artifacts" if children else "directory is empty",
        )
    ]


def _count_pattern(text: str, pattern: str) -> int:
    return len(re.findall(pattern, text, flags=re.MULTILINE))


def _has_heading(text: str, heading: str) -> bool:
    return heading in text


def _table_row_count(text: str, id_pattern: str) -> int:
    return _count_pattern(text, rf"^\|\s*{id_pattern}\s*\|")


def _contains_any(text: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, text, flags=re.MULTILINE | re.IGNORECASE) for pattern in patterns)


def _line_items_after_heading(text: str, heading: str) -> list[str]:
    pattern = re.compile(rf"(?ms)^{re.escape(heading)}\s*(.*?)(?=^## |\Z)")
    match = pattern.search(text)
    if not match:
        return []
    block = match.group(1)
    return [line.strip() for line in block.splitlines() if line.strip()]


def _section_block(text: str, heading: str) -> str:
    pattern = re.compile(rf"(?ms)^{re.escape(heading)}\s*(.*?)(?=^## |\Z)")
    match = pattern.search(text)
    return match.group(1) if match else ""


def _section_table_rows(text: str, heading: str) -> list[list[str]]:
    block = _section_block(text, heading)
    rows: list[list[str]] = []
    for line in block.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        if re.match(r"^\|(?:\s*:?-{3,}:?\s*\|)+\s*$", stripped):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if cells and all(cell.replace("-", "").strip() == "" for cell in cells):
            continue
        rows.append(cells)
    _KNOWN_HEADERS = {
        "field", "value", "id", "constraint", "rationale", "source",
        "question", "owner", "unknown", "impact", "discovery path",
        "assumption", "if false, then",
        # Initiative-Architecture Fit — template columns
        "feature area", "existing components touched",
        "new components / boundaries", "contract changes", "blast radius",
        # Initiative-Architecture Fit — common LLM-generated columns
        "proposed component", "fit", "rationale", "owner",
        # Brownfield Impact
        "component", "change type", "consumers", "backward compatible?",
        "migration required", "rollback possible",
        # Quality Attribute Assessment — template columns
        "attribute", "requirement (from brs)", "assessment", "risk",
        # Quality Attribute Assessment — common LLM-generated columns
        "target", "evidence",
        # Architecture Constraints — common LLM-generated columns
        "violation consequence", "mitigation",
        # Open Decisions
        "decision", "status", "default assumption", "required before",
        # Known Unknowns
        "discovery path",
    }
    if rows and all(cell.lower() in _KNOWN_HEADERS for cell in rows[0]):
        rows = rows[1:]
    return rows


def _normalize_text(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", " ", (value or "").lower())
    return re.sub(r"\s+", " ", normalized).strip()


def _normalized_title(value: str) -> str:
    return _normalize_text(value)


def _keywords(value: str) -> set[str]:
    stopwords = {
        "a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
        "has", "have", "if", "in", "is", "it", "of", "on", "or", "so",
        "that", "the", "their", "then", "there", "this", "to", "when",
        "with", "within", "shall", "should", "must", "can", "will",
        "system", "user", "users",
    }
    return {
        token for token in _normalize_text(value).split()
        if len(token) >= 4 and token not in stopwords
    }


def _canonical_requirements(workspace_root: Path) -> dict[str, dict[str, Any]]:
    req_path = workspace_root / "requirements" / "atomic-requirements.md"
    if not req_path.exists():
        return {}

    text = _read_text(req_path)
    pattern = re.compile(
        r"^###\s+((?:FR|REQ|NFR|C)-\d{3})\s+[—-]\s+(.+?)\n(.*?)(?=^###\s+(?:FR|REQ|NFR|C)-\d{3}\s+[—-]\s+|\Z)",
        flags=re.MULTILINE | re.DOTALL,
    )
    requirements: dict[str, dict[str, Any]] = {}

    for match in pattern.finditer(text):
        req_id = match.group(1).strip()
        title = match.group(2).strip()
        block = match.group(3)

        def _field(label: str) -> str:
            field_match = re.search(
                rf"^\|\s*{re.escape(label)}\s*\|\s*(.*?)\s*\|$",
                block,
                flags=re.MULTILINE,
            )
            return field_match.group(1).strip() if field_match else ""

        requirement_text_match = re.search(
            r"####\s+Requirement Text\s*(.*?)(?=^####\s+|\Z)",
            block,
            flags=re.MULTILINE | re.DOTALL,
        )
        requirement_text = requirement_text_match.group(1).strip() if requirement_text_match else ""

        blocking_questions = _field("Blocking Questions")
        ambiguities = _field("Ambiguities")
        signature_source = " ".join(
            part for part in [
                title,
                _field("Actor"),
                _field("Business Object"),
                _field("Trigger / Event"),
                _field("Expected Outcome"),
                requirement_text,
            ] if part
        )
        requirements[req_id] = {
            "id": req_id,
            "title": title,
            "normalized_title": _normalized_title(title),
            "actor": _field("Actor"),
            "business_object": _field("Business Object"),
            "trigger": _field("Trigger / Event"),
            "expected_outcome": _field("Expected Outcome"),
            "text": requirement_text,
            "ambiguities": ambiguities,
            "blocking_questions": blocking_questions,
            "keywords": _keywords(signature_source),
        }

    if requirements:
        return requirements

    # Fallback for older requirement formats.
    fallback_ids = sorted(set(re.findall(r"(?:FR|REQ|NFR|C)-\d{3}", text)))
    return {
        req_id: {
            "id": req_id,
            "title": req_id,
            "normalized_title": _normalized_title(req_id),
            "actor": "",
            "business_object": "",
            "trigger": "",
            "expected_outcome": "",
            "text": "",
            "ambiguities": "",
            "blocking_questions": "",
            "keywords": {req_id.lower().replace("-", "")},
        }
        for req_id in fallback_ids
    }


def _all_requirement_ids(workspace_root: Path) -> set[str]:
    """Return all known requirement IDs: canonical headings plus any
    FR/NFR/C IDs referenced in the atomic-requirements body text."""
    canonical = set(_canonical_requirements(workspace_root))
    req_path = workspace_root / "requirements" / "atomic-requirements.md"
    if req_path.exists():
        _REQ_REF_RE = r"(?<![A-Za-z])(?:FR|REQ|NFR|C)-\d{3}"
        all_refs = set(re.findall(_REQ_REF_RE, _read_text(req_path)))
        canonical |= all_refs
    return canonical


def _extract_requirement_titles_from_story(text: str) -> dict[str, str]:
    titles: dict[str, str] = {}
    rows = _section_table_rows(text, "## Linked Requirements")
    for row in rows:
        if len(row) < 2:
            continue
        req_id = row[0].strip()
        if re.fullmatch(r"(?:FR|REQ|NFR|C)-\d{3}", req_id):
            titles[req_id] = row[1].strip()
    return titles


def _extract_requirement_titles_from_epic(text: str) -> dict[str, str]:
    titles: dict[str, str] = {}
    rows = _section_table_rows(text, "## Source Traceability")
    for row in rows:
        if len(row) < 3:
            continue
        if row[0].strip().lower() != "requirement":
            continue
        req_id = row[1].strip()
        if re.fullmatch(r"(?:FR|REQ|NFR|C)-\d{3}", req_id):
            titles[req_id] = row[2].strip()
    return titles


def _extract_requirement_titles_from_coverage(text: str) -> dict[str, str]:
    titles: dict[str, str] = {}
    rows = _section_table_rows(text, "## Full Coverage Matrix")
    for row in rows:
        if len(row) < 2:
            continue
        req_id = row[0].strip()
        if re.fullmatch(r"(?:FR|REQ|NFR|C)-\d{3}", req_id):
            titles[req_id] = row[1].strip()
    return titles


def _artifact_requirement_pairs(path: Path) -> dict[str, str]:
    if path.is_dir():
        pairs: dict[str, str] = {}
        for epic_dir in sorted([d for d in path.iterdir() if d.is_dir() and d.name.startswith("E-")]):
            epic_md = epic_dir / "epic.md"
            if epic_md.exists():
                pairs.update(_extract_requirement_titles_from_epic(_read_text(epic_md)))
            stories_dir = epic_dir / "stories"
            if stories_dir.exists():
                for story_file in sorted(stories_dir.glob("S-*.md")):
                    if story_file.name.endswith(".prompt.md"):
                        continue
                    pairs.update(_extract_requirement_titles_from_story(_read_text(story_file)))
        return pairs

    text = _read_text(path)
    if path.name == "fr-coverage.md":
        return _extract_requirement_titles_from_coverage(text)
    return {}


def _all_requirement_references_in_artifact(path: Path) -> set[str]:
    _REQ_REF_RE = r"(?<![A-Za-z])(?:FR|REQ|NFR|C)-\d{3}"
    if path.is_dir():
        refs: set[str] = set()
        for child in path.rglob("*.md"):
            refs.update(re.findall(_REQ_REF_RE, _read_text(child)))
        return refs
    return set(re.findall(_REQ_REF_RE, _read_text(path)))


def _selected_epic_ids(workspace_root: Path, fallback_to_all: bool = True) -> list[str]:
    selected_path = workspace_root / "input" / "selected-epics.md"
    if selected_path.exists():
        selected = re.findall(r"\bE-\d{3}\b", _read_text(selected_path))
        if selected:
            return sorted(dict.fromkeys(selected))
    if not fallback_to_all:
        return []
    epics_dir = workspace_root / "epics"
    if not epics_dir.exists():
        return []
    return sorted({
        match.group(1)
        for child in epics_dir.iterdir()
        if child.is_dir()
        for match in [re.match(r"(E-\d{3})", child.name)]
        if match
    })


_PLACEHOLDER_PATTERNS = [
    r"\[fill in\]",
    r"Goal Title",
    r"Actor Name",
    r"\[role\]",
    r"\[goal\]",
    r"\[benefit\]",
    # slash-separated option lists that were copied verbatim from the template
    r"\b(?:High|Medium|Low)\s*/\s*(?:High|Medium|Low)",
    r"\bPerformance\s*/\s*Security",
    r"\bTechnical\s*/\s*Regulatory",
    r"\bCritical\s*/\s*High\s*/\s*Medium",
    r"\bOpen\s*/\s*Mitigated\s*/\s*Accepted",
    r"\bFix\s*/\s*Merge\s*/\s*Release",
    r"\bBRS section\s*/\s*intake reference",
]


def _section_non_placeholder(text: str, heading: str) -> bool:
    lines = _line_items_after_heading(text, heading)
    meaningful = []
    for line in lines:
        if line.startswith("|---"):
            continue
        # all-empty table row
        if line.startswith("|") and re.search(r"\|\s*\|\s*$", line):
            continue
        # known placeholder markers
        if any(re.search(p, line, flags=re.IGNORECASE) for p in _PLACEHOLDER_PATTERNS):
            continue
        meaningful.append(line)
    return bool(meaningful)


def _normalized_profile_name(action: dict[str, Any]) -> str | None:
    profile = action.get("validation_profile")
    if not profile:
        return None
    return str(profile).strip()


def _artifact_criticality(action: dict[str, Any]) -> str:
    return str(action.get("artifact_criticality") or "low").strip()


def _required_sections(action: dict[str, Any]) -> list[str]:
    return list(action.get("required_sections") or [])


def _required_tables(action: dict[str, Any]) -> list[str]:
    return list(action.get("required_tables") or [])


def _forbidden_placeholders(action: dict[str, Any]) -> list[str]:
    return list(action.get("forbidden_placeholders") or [])


def _profile_dispatch_check(
    path: Path,
    *,
    dispatch: str,
    detail: str,
    passed: bool = True,
) -> dict[str, str]:
    return _result("validation_dispatch", path.name, passed, f"{dispatch}: {detail}")


def _has_minimum_headings(text: str, minimum: int = 2) -> bool:
    return len(re.findall(r"^##\s+", text, flags=re.MULTILINE)) >= minimum


def _has_any_table(text: str) -> bool:
    return bool(re.search(r"^\|.+\|$", text, flags=re.MULTILINE))


def _placeholders_absent(text: str, extra_patterns: list[str] | None = None) -> bool:
    patterns = list(_PLACEHOLDER_PATTERNS)
    if extra_patterns:
        patterns.extend(extra_patterns)
    return not any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns)


def _check_passed(checks: list[dict[str, str]], name: str) -> bool:
    return any(check.get("name") == name and check.get("result") == "pass" for check in checks)


def _any_check_passed(checks: list[dict[str, str]], names: list[str]) -> bool:
    return any(_check_passed(checks, name) for name in names)


def _cell_is_populated(value: str) -> bool:
    text = (value or "").strip()
    if not text:
        return False
    if text in {"{{initiative_id}}", "{{date}}"}:
        return False
    if text in {
        "Low / Medium / High",
        "Yes / No",
        "Modified / Removed / New boundary",
        "BRS feature area",
        "BRS section / architecture input",
    }:
        return False
    return _placeholders_absent(text)


def _required_sections_present(path: Path, sections: list[str]) -> list[dict[str, str]]:
    checks = []
    for heading in sections:
        checks.extend(_contains(path, heading, f"has_{heading.strip('# ').lower().replace(' ', '_')}", f"{heading} section present"))
    return checks


def _required_tables_present(text: str, path: Path, tables: list[str]) -> list[dict[str, str]]:
    checks = []
    for table in tables:
        pattern = rf"(?m)^\|\s*{re.escape(table)}\s*\|"
        checks.append(
            _result(
                f"has_table_{table.lower().replace(' ', '_')}",
                path.name,
                bool(re.search(pattern, text)),
                f"table row for `{table}` present",
            )
        )
    return checks


def _validate_profile_basic_file(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
) -> list[dict[str, str]]:
    if path.is_dir():
        return [_profile_dispatch_check(path, dispatch="profile", detail="basic-file")] + _non_empty_directory(path)
    return [_profile_dispatch_check(path, dispatch="profile", detail="basic-file")] + _non_empty_file(path)


def _validate_profile_structured_document(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
) -> list[dict[str, str]]:
    if path.is_dir():
        return [_profile_dispatch_check(path, dispatch="profile", detail="structured-document")] + _non_empty_directory(path)

    text = _read_text(path)
    checks = [_profile_dispatch_check(path, dispatch="profile", detail="structured-document")]
    checks.extend(_non_empty_file(path))
    checks.extend(_required_sections_present(path, _required_sections(action)))
    checks.extend(_required_tables_present(text, path, _required_tables(action)))
    checks.append(
        _result(
            "has_minimum_headings",
            path.name,
            _has_minimum_headings(text),
            "document contains multiple section headings",
        )
    )
    checks.append(
        _result(
            "has_structured_content",
            path.name,
            _has_any_table(text) or len(text.splitlines()) >= 8,
            "document includes a table or enough content to be structured",
        )
    )
    checks.append(
        _result(
            "placeholders_absent",
            path.name,
            _placeholders_absent(text, _forbidden_placeholders(action)),
            "document does not contain known placeholder markers",
        )
    )
    return checks


def _validate_profile_catalog(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
) -> list[dict[str, str]]:
    checks = _validate_profile_structured_document(path, workspace_root, action, artifact_path)
    if path.is_dir():
        return checks

    text = _read_text(path)
    checks.append(
        _result(
            "has_catalog_rows",
            path.name,
            bool(re.search(r"^\|\s*[A-Z]{2,}(?:-[A-Z]+)?-\d{3}\s*\|", text, flags=re.MULTILINE)),
            "catalog contains at least one typed identifier row",
        )
    )
    return checks


def _validate_architecture_review_sections(path: Path, workspace_root: Path, text: str) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []
    required_sections = [
        "## Metadata",
        "## Initiative-Architecture Fit",
        "## Architecture Constraints",
        "## Brownfield Impact",
        "## Quality Attribute Assessment",
        "## Open Decisions",
        "## Active Assumptions",
        "## Known Unknowns",
    ]
    checks.extend(_required_sections_present(path, required_sections))

    fit_rows = _section_table_rows(text, "## Initiative-Architecture Fit")
    fit_populated = any(len(row) >= 5 and all(_cell_is_populated(cell) for cell in row[:5]) for row in fit_rows)
    checks.append(
        _result(
            "fit_section_populated",
            path.name,
            fit_populated,
            "initiative-architecture fit contains at least one populated feature-area row",
        )
    )

    constraint_rows = _section_table_rows(text, "## Architecture Constraints")
    constraints_populated = any(len(row) >= 5 and all(_cell_is_populated(cell) for cell in row[:5]) for row in constraint_rows)
    checks.append(
        _result(
            "constraints_have_rationale_and_consequence",
            path.name,
            constraints_populated,
            "architecture constraints include populated rationale and violation consequence",
        )
    )

    brownfield_rows = _section_table_rows(text, "## Brownfield Impact")
    brownfield_populated = "Greenfield - no brownfield impact" in text or any(
        len(row) >= 6 and _cell_is_populated(row[0]) and _cell_is_populated(row[1]) for row in brownfield_rows
    )
    regression_surface = bool(re.search(r"(?mi)^\*\*Regression surface:\*\*\s*(?!which existing functionality is at risk and why\b).+", text))
    rollback_sensitivity = bool(re.search(r"(?mi)^\*\*Rollback sensitivity:\*\*\s*(?!Low / Medium / High - reason\b).+", text))
    checks.append(
        _result(
            "brownfield_impact_explicit",
            path.name,
            brownfield_populated and regression_surface and rollback_sensitivity,
            "brownfield impact is explicitly assessed with regression surface and rollback sensitivity",
        )
    )

    quality_rows = _section_table_rows(text, "## Quality Attribute Assessment")
    quality_map = {
        row[0]: row for row in quality_rows
        if row and row[0] not in {"Attribute", "attribute"}
    }
    required_quality = ["Performance", "Security", "Scalability", "Availability"]
    quality_populated = all(
        attribute in quality_map
        and len(quality_map[attribute]) >= 3
        and all(_cell_is_populated(cell) for cell in quality_map[attribute][:3])
        for attribute in required_quality
    )
    checks.append(
        _result(
            "quality_attributes_populated",
            path.name,
            quality_populated,
            "quality attribute rows are populated for performance, security, scalability, and availability",
        )
    )

    upstream_gap_count = 0
    gaps_path = workspace_root / "business-analysis" / "gaps-and-questions.md"
    if gaps_path.exists():
        upstream_gap_count = _table_row_count(_read_text(gaps_path), r"GAP-\d{3}")
    decision_rows = _section_table_rows(text, "## Open Decisions")
    populated_decisions = [
        row for row in decision_rows if len(row) >= 5 and all(_cell_is_populated(cell) for cell in row[:5])
    ]
    checks.append(
        _result(
            "open_decisions_present_when_upstream_gaps_exist",
            path.name,
            upstream_gap_count == 0 or bool(populated_decisions),
            "open decisions are populated when upstream gaps exist",
        )
    )

    assumption_rows = _section_table_rows(text, "## Active Assumptions")
    populated_assumptions = any(len(row) >= 3 and all(_cell_is_populated(cell) for cell in row[:3]) for row in assumption_rows)
    checks.append(
        _result(
            "assumptions_include_if_false_then",
            path.name,
            populated_assumptions,
            "active assumptions include populated If False, Then consequences",
        )
    )

    unknown_rows = _section_table_rows(text, "## Known Unknowns")
    populated_unknowns = any(len(row) >= 3 and all(_cell_is_populated(cell) for cell in row[:3]) for row in unknown_rows)
    checks.append(
        _result(
            "known_unknowns_populated",
            path.name,
            populated_unknowns,
            "known unknowns include populated impact and discovery path",
        )
    )

    meaningful_lines = [line for line in text.splitlines() if line.strip()]
    placeholder_summary = bool(re.search(r"(?i)minimal placeholder|architecture review completed\.", text))
    checks.append(
        _result(
            "not_summary_only",
            path.name,
            len(meaningful_lines) >= 25 and not placeholder_summary,
            "architecture review is not merely a short placeholder summary",
        )
    )
    return checks


def _validate_profile_analytical_review(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
) -> list[dict[str, str]]:
    checks = _validate_profile_structured_document(path, workspace_root, action, artifact_path)
    if path.is_dir():
        return checks

    text = _read_text(path)
    checks.append(
        _result(
            "has_analysis_signals",
            path.name,
            bool(re.search(r"\b(risk|constraint|decision|assumption|impact|quality)\b", text, flags=re.IGNORECASE)),
            "review contains analytical vocabulary signals",
        )
    )
    if artifact_path == "architecture/architecture-review.md":
        checks.extend(_validate_architecture_review_sections(path, workspace_root, text))
    return checks


def _validate_profile_artifact_package(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
) -> list[dict[str, str]]:
    checks = [_profile_dispatch_check(path, dispatch="profile", detail="artifact-package")]
    checks.extend(_non_empty_directory(path) if path.is_dir() else _non_empty_file(path))
    if path.is_dir():
        checks.append(
            _result(
                "has_package_members",
                path.name,
                any(path.iterdir()),
                "package contains at least one generated member",
            )
        )
    return checks


def _validate_routing_decision(path: Path, workspace_root: Path) -> list[dict[str, str]]:
    text = _read_text(path)
    checks = []
    checks.extend(_non_empty_file(path))
    checks.extend(_contains(path, "## Decision Summary", "has_decision_summary", "decision summary section present"))
    checks.append(
        _result(
            "delivery_mode_present",
            path.name,
            bool(re.search(r"\|\s*Delivery mode\s*\|\s*(OpenSpec|Standalone|FastPath|BusinessCopilot)\s*\|", text)),
            "delivery mode row uses an allowed value",
        )
    )
    checks.append(
        _result(
            "execution_mode_present",
            path.name,
            bool(re.search(r"\|\s*Execution mode\s*\|\s*(Enterprise|Enterprise\+Modular|Standard)\s*\|", text)),
            "execution mode row uses an allowed value",
        )
    )
    return checks


def _validate_business_intake_summary(path: Path, workspace_root: Path) -> list[dict[str, str]]:
    text = _read_text(path)
    source = _source_text(workspace_root)
    checks = []
    checks.extend(_non_empty_file(path))
    for heading in ["## Executive Summary", "## Requirements", "## PO Review Checklist"]:
        checks.extend(_contains(path, heading, f"has_{heading.split()[-1].lower()}", f"{heading} section present"))
    checks.extend(_matches(path, r"\|\s*FR-\d{3}\s*\|", "has_requirement_rows", "requirements table includes FR rows"))
    source_requirement_count = _count_pattern(source, r"^\s*(?:[-*]\s*)?(?:FR|REQ)-\d{3}\b") + _count_pattern(
        source, r"\|\s*(?:FR|REQ)-\d{3}\s*\|"
    )
    summary_requirement_count = _table_row_count(text, r"FR-\d{3}")
    checks.append(
        _result(
            "requirements_not_too_small",
            path.name,
            not (source_requirement_count >= 2 and summary_requirement_count <= 1),
            "requirements coverage is not suspiciously tiny for the BRS size",
        )
    )
    source_has_objectives = _contains_any(
        source,
        [r"^##\s+Objectives", r"^\|\s*OBJ-\d{3}\s*\|", r"objective", r"goal"],
    )
    summary_objective_count = _table_row_count(text, r"OBJ-\d{3}")
    checks.append(
        _result(
            "objectives_present_when_in_source",
            path.name,
            not source_has_objectives or summary_objective_count > 0,
            "objectives are present when the BRS contains objectives or goals",
        )
    )
    source_has_unresolved = _contains_any(source, [r"\bTBD\b", r"open question", r"^##\s+Open Questions?", r"^\|\s*OQ-\d{3}\s*\|"])
    summary_gap_count = _table_row_count(text, r"GAP-\d{3}") + _table_row_count(text, r"OQ-\d{3}")
    checks.append(
        _result(
            "gaps_present_when_source_has_questions",
            path.name,
            not source_has_unresolved or summary_gap_count > 0,
            "gaps are present when the BRS contains unresolved questions",
        )
    )
    checks.append(
        _result(
            "not_template_only",
            path.name,
            not _contains_any(text, [r"generated to satisfy", r"\[fill in\]", r"Goal Title", r"Actor Name"]),
            "artifact is not placeholder-only or template-derived filler",
        )
    )
    return checks


def _validate_requirements_catalog(path: Path, workspace_root: Path) -> list[dict[str, str]]:
    text = _read_text(path)
    source = _source_text(workspace_root)
    checks = []
    checks.extend(_non_empty_file(path))
    for heading in ["## Functional Requirements", "## Non-Functional Requirements", "## Constraints"]:
        checks.extend(_contains(path, heading, f"has_{heading.split()[-1].lower()}", f"{heading} section present"))
    checks.extend(_matches(path, r"\|\s*FR-\d{3}\s*\|", "has_fr_rows", "functional requirements include FR rows"))
    source_requirement_count = _count_pattern(source, r"^\s*(?:[-*]\s*)?(?:FR|REQ)-\d{3}\b") + _count_pattern(
        source, r"\|\s*(?:FR|REQ)-\d{3}\s*\|"
    )
    fr_row_count = _table_row_count(text, r"FR-\d{3}")
    checks.append(
        _result(
            "fr_not_too_small",
            path.name,
            not (source_requirement_count >= 2 and fr_row_count <= 1),
            "functional requirements coverage is not suspiciously tiny for the BRS size",
        )
    )
    checks.append(
        _result(
            "fr_not_template_only",
            path.name,
            not any(re.search(p, text, flags=re.IGNORECASE) for p in _PLACEHOLDER_PATTERNS),
            "functional requirements contain no template placeholder text",
        )
    )
    checks.append(
        _result(
            "nfr_section_not_empty",
            path.name,
            _section_non_placeholder(text, "## Non-Functional Requirements"),
            "non-functional requirements section contains real populated content",
        )
    )
    checks.append(
        _result(
            "constraints_section_not_empty",
            path.name,
            _section_non_placeholder(text, "## Constraints"),
            "constraints section contains real populated content",
        )
    )
    return checks


def _validate_use_cases_markdown(path: Path, workspace_root: Path) -> list[dict[str, str]]:
    text = _read_text(path)
    checks = []
    checks.extend(_non_empty_file(path))
    checks.extend(_contains(path, "```mermaid", "has_mermaid", "mermaid diagram block present"))
    checks.extend(_contains(path, "graph LR", "has_graph_lr", "use-case diagram uses graph LR"))
    checks.extend(_matches(path, r"\|\s*UC-\d{3}\s*\|", "has_uc_catalog_rows", "UC catalog includes UC rows"))
    checks.append(
        _result(
            "has_actor_node",
            path.name,
            bool(re.search(r"^\s*[A-Za-z][A-Za-z0-9_]*\s*(?:\(\[.*?\]\)|-->)", text, flags=re.MULTILINE)),
            "markdown use-case diagram includes at least one actor-like node or actor connection",
        )
    )
    uc_count = _table_row_count(text, r"UC-\d{3}")
    requirements_path = workspace_root / "business-analysis" / "requirements.md"
    if requirements_path.exists():
        requirements_text = _read_text(requirements_path)
        fr_count = _table_row_count(requirements_text, r"FR-\d{3}")
        # Minimum expected UCs: ceil(fr_count / 4), floored at 1.
        # e.g. 15 FRs → min 4 UCs; 6 FRs → min 2 UCs; 3 FRs → min 1 UC.
        min_expected_ucs = max(1, (fr_count + 3) // 4)
        checks.append(
            _result(
                "uc_coverage_not_too_shallow",
                path.name,
                uc_count >= min_expected_ucs,
                f"use-case count ({uc_count}) is proportional to FR count ({fr_count}); expected at least {min_expected_ucs}",
            )
        )
    return checks


def _validate_entity_model(path: Path, workspace_root: Path) -> list[dict[str, str]]:
    text = _read_text(path)
    checks = []
    checks.extend(_non_empty_file(path))
    checks.extend(_contains(path, "## Entity Catalog", "has_entity_catalog", "Entity Catalog section present"))
    checks.extend(_matches(path, r"\|\s*ENT-\d{3}\s*\|", "has_ent_rows", "entity catalog includes ENT-NNN rows"))
    checks.extend(_contains(path, "```mermaid", "has_er_diagram", "ER diagram block present"))
    ent_count = _table_row_count(text, r"ENT-\d{3}")
    requirements_path = workspace_root / "business-analysis" / "requirements.md"
    if requirements_path.exists():
        requirements_text = _read_text(requirements_path)
        fr_count = _table_row_count(requirements_text, r"FR-\d{3}")
        # Minimum expected entities: ceil(fr_count / 5), floored at 2.
        # e.g. 15 FRs → min 3 ENTs; 10 FRs → min 2 ENTs.
        min_expected_ents = max(2, (fr_count + 4) // 5)
        checks.append(
            _result(
                "entity_count_not_too_small",
                path.name,
                ent_count >= min_expected_ents,
                f"entity count ({ent_count}) is proportional to FR count ({fr_count}); expected at least {min_expected_ents}",
            )
        )
    # Every ENT in the catalog should have a detail section
    catalog_ids = re.findall(r"^\|\s*(ENT-\d{3})\s*\|", text, flags=re.MULTILINE)
    detail_ids = re.findall(r"^###\s+(ENT-\d{3})", text, flags=re.MULTILINE)
    missing_details = [eid for eid in catalog_ids if eid not in detail_ids]
    checks.append(
        _result(
            "all_entities_have_detail_sections",
            path.name,
            not missing_details,
            "all ENT-NNN catalog entries have a detail section" if not missing_details
            else f"missing detail sections for: {missing_details}",
        )
    )
    return checks


def _validate_use_cases_puml(path: Path, workspace_root: Path) -> list[dict[str, str]]:
    text = _read_text(path)
    checks = []
    checks.extend(_non_empty_file(path))
    checks.extend(_contains(path, "@startuml", "has_startuml", "PlantUML start marker present"))
    checks.extend(_contains(path, "@enduml", "has_enduml", "PlantUML end marker present"))
    checks.extend(_matches(path, r"UC-\d{3}", "has_uc_identifiers", "PlantUML includes UC identifiers"))
    checks.append(
        _result(
            "has_actor_declaration",
            path.name,
            bool(re.search(r"^\s*actor\s+", text, flags=re.MULTILINE)),
            "PlantUML includes at least one actor declaration",
        )
    )
    markdown_path = workspace_root / "business-analysis" / "use-cases.md"
    if markdown_path.exists():
        markdown_text = _read_text(markdown_path)
        markdown_uc_count = _table_row_count(markdown_text, r"UC-\d{3}")
        puml_uc_count = _count_pattern(text, r"UC-\d{3}")
        checks.append(
            _result(
                "uc_count_consistent_with_markdown",
                path.name,
                markdown_uc_count == 0 or puml_uc_count >= markdown_uc_count,
                "PlantUML contains at least the markdown UC identifiers",
            )
        )
    return checks


def _validate_atomic_requirements(path: Path, workspace_root: Path) -> list[dict[str, str]]:
    text = _read_text(path)
    source = _source_text(workspace_root)
    checks = []
    checks.extend(_non_empty_file(path))

    for heading in ["## Requirement Catalogue", "## Open Questions", "## Assumptions"]:
        checks.extend(_contains(path, heading, f"has_{heading.split()[-1].lower()}", f"{heading} section present"))

    checks.extend(_matches(path, r"\|\s*(?:FR|REQ)-\d{3}\s*\|", "has_req_rows", "requirement catalogue includes typed rows"))

    source_fr_count = _count_pattern(source, r"\*\*FR-\d{3}\*\*")
    if source_fr_count == 0:
        source_fr_count = _count_pattern(source, r"(?:^|\|)\s*FR-\d{3}\s*(?:\||\s)")
    artifact_req_count = _count_pattern(text, r"^###\s+(?:REQ|FR)-\d{3}\b")
    if artifact_req_count == 0:
        artifact_req_count = _table_row_count(text, r"(?:FR|REQ)-\d{3}")

    if source_fr_count >= 4:
        min_expected = max(2, source_fr_count // 2)
        checks.append(
            _result(
                "req_count_proportional_to_source",
                path.name,
                artifact_req_count >= min_expected,
                f"extracted {artifact_req_count} requirements from {source_fr_count} BRS FRs (minimum {min_expected})"
                if artifact_req_count >= min_expected
                else f"only {artifact_req_count} requirements extracted from {source_fr_count} BRS FRs — expected at least {min_expected}; likely incomplete extraction",
            )
        )
    elif source_fr_count >= 2:
        checks.append(
            _result(
                "req_count_not_too_small",
                path.name,
                artifact_req_count >= 2,
                f"extracted {artifact_req_count} requirements from {source_fr_count} BRS FRs",
            )
        )

    checks.append(
        _result(
            "req_not_template_only",
            path.name,
            _placeholders_absent(text),
            "requirements contain no template placeholder text",
        )
    )
    return checks


def _validate_delivery_skeleton(path: Path, workspace_root: Path) -> list[dict[str, str]]:
    text = _read_text(path)
    checks = []
    checks.extend(_non_empty_file(path))

    is_light = "## Epic Summary" in text or "## Epic Dependency Summary" in text
    if is_light:
        for heading in ["## Epic and Feature Hierarchy", "## Requirement Coverage"]:
            checks.extend(_contains(path, heading, f"has_{heading.strip('# ').lower().replace(' ', '_')}", f"{heading} section present"))
    else:
        for heading in ["## Story Count Assertion", "## Epic and Feature Hierarchy", "## Story Index", "## Requirement Coverage Summary"]:
            checks.extend(_contains(path, heading, f"has_{heading.strip('# ').lower().replace(' ', '_')}", f"{heading} section present"))

    epic_count = _count_pattern(text, r"^###\s+E-\d{3}\b")
    checks.append(
        _result(
            "has_epics",
            path.name,
            epic_count >= 1,
            f"skeleton defines {epic_count} epic(s)",
        )
    )

    feature_count = _count_pattern(text, r"^\|\s*F-\d{3}\s*\|")
    checks.append(
        _result(
            "has_features",
            path.name,
            feature_count >= 1,
            f"skeleton defines {feature_count} feature(s)",
        )
    )

    req_path = workspace_root / "requirements" / "atomic-requirements.md"
    if req_path.exists():
        req_text = _read_text(req_path)
        req_ids = set(re.findall(r"(?:FR|REQ)-\d{3}", req_text))
        coverage_section = "## Requirement Coverage" if is_light else "## Requirement Coverage Summary"
        skeleton_req_ids = set(re.findall(r"(?:FR|REQ)-\d{3}", _section_block(text, coverage_section)))
        if len(req_ids) >= 2:
            coverage = len(skeleton_req_ids & req_ids) / len(req_ids)
            checks.append(
                _result(
                    "skeleton_req_coverage",
                    path.name,
                    coverage >= 0.9,
                    f"skeleton covers {len(skeleton_req_ids & req_ids)}/{len(req_ids)} requirements ({coverage:.0%})"
                    if coverage >= 0.9
                    else f"skeleton only covers {len(skeleton_req_ids & req_ids)}/{len(req_ids)} requirements ({coverage:.0%}) — expected at least 90%",
                )
            )

    checks.append(
        _result(
            "skeleton_no_placeholders",
            path.name,
            _placeholders_absent(text),
            "skeleton contains no template placeholder text",
        )
    )
    return checks


def _validate_fr_coverage_report(path: Path, workspace_root: Path) -> list[dict[str, str]]:
    text = _read_text(path)
    checks = []
    checks.extend(_non_empty_file(path))

    for heading in ["## Coverage Summary", "## Full Coverage Matrix"]:
        checks.extend(_contains(path, heading, f"has_{heading.strip('# ').lower().replace(' ', '_')}", f"{heading} section present"))

    coverage_match = re.search(r"\|\s*Coverage percentage\s*\|\s*(\d+)%?\s*\|", text)
    if coverage_match:
        pct = int(coverage_match.group(1))
        checks.append(
            _result(
                "coverage_percentage_acceptable",
                path.name,
                pct >= 90,
                f"coverage percentage is {pct}%" if pct >= 90
                else f"coverage percentage is only {pct}% — expected at least 90%; likely missing stories for requirements",
            )
        )
    else:
        covered_rows = _count_pattern(text, r"\|\s*Covered\s*\|")
        not_covered_rows = _count_pattern(text, r"\|\s*\*\*Not Covered\*\*\s*\|")
        total = covered_rows + not_covered_rows
        if total >= 2:
            pct = (covered_rows * 100) // total
            checks.append(
                _result(
                    "coverage_percentage_acceptable",
                    path.name,
                    pct >= 90,
                    f"calculated coverage: {covered_rows}/{total} ({pct}%)" if pct >= 90
                    else f"calculated coverage: only {covered_rows}/{total} ({pct}%) — expected at least 90%",
                )
            )

    req_path = workspace_root / "requirements" / "atomic-requirements.md"
    if req_path.exists():
        req_text = _read_text(req_path)
        req_ids = set(re.findall(r"(?:FR|REQ|NFR)-\d{3}", req_text))
        matrix_ids = set(re.findall(r"(?:FR|REQ|NFR)-\d{3}", _section_block(text, "## Full Coverage Matrix")))
        if len(req_ids) >= 2:
            missing = req_ids - matrix_ids
            checks.append(
                _result(
                    "all_reqs_in_matrix",
                    path.name,
                    len(missing) == 0,
                    f"all {len(req_ids)} requirements appear in coverage matrix"
                    if len(missing) == 0
                    else f"{len(missing)} requirements missing from coverage matrix: {sorted(missing)[:10]}",
                )
            )

    checks.append(
        _result(
            "fr_coverage_no_placeholders",
            path.name,
            _placeholders_absent(text),
            "coverage report contains no template placeholder text",
        )
    )
    return checks


def _validate_readiness_check(path: Path, workspace_root: Path) -> list[dict[str, str]]:
    text = _read_text(path)
    checks = []
    checks.extend(_non_empty_file(path))
    for heading in ["## Core Checklist", "## Gate Trigger Decisions", "## Readiness Decision"]:
        checks.extend(_contains(path, heading, f"has_{heading.split()[-1].lower()}", f"{heading} section present"))
    checks.extend(_matches(path, r"\|\s*Readiness score\s*\|", "has_readiness_score", "readiness score row present"))
    checklist_has_values = bool(
        re.search(r"\|\s*\d+\s*\|.*\|\s*(Pass|Fail|N/A)\s*\|", text, flags=re.MULTILINE)
        or re.search(r"^- \[[ xX]\]\s+", text, flags=re.MULTILINE)
    )
    checks.append(
        _result(
            "core_checklist_has_values",
            path.name,
            checklist_has_values,
            "core checklist contains real pass/fail-style values",
        )
    )
    gate_rows = re.findall(
        r"^\|\s*([^|]+?)\s*\|\s*(Yes|No)\s*\|\s*([^|]*?)\s*\|\s*(Yes|No)\s*\|",
        text,
        flags=re.MULTILINE,
    )
    checks.append(
        _result(
            "gate_rows_present",
            path.name,
            bool(gate_rows),
            "gate trigger table contains explicit Yes/No rows",
        )
    )
    _ARTIFACT_EXISTENCE_PATTERNS = re.compile(
        r"(?i)not yet created|to be defined|to be created|TBD|TODO|"
        r"not yet produced|will be created|to be determined|pending creation|"
        r"not yet available|to be done|not created yet"
    )
    no_with_blank_reason = False
    no_with_existence_reason = False
    bad_gate_names: list[str] = []
    for gate_name, triggered, reason, _required in gate_rows:
        if triggered != "No":
            continue
        stripped = reason.strip()
        if not stripped:
            no_with_blank_reason = True
            bad_gate_names.append(f"{gate_name.strip()} (blank)")
        elif _ARTIFACT_EXISTENCE_PATTERNS.search(stripped):
            no_with_existence_reason = True
            bad_gate_names.append(f"{gate_name.strip()} (artifact-existence)")
    checks.append(
        _result(
            "no_gates_have_justification",
            path.name,
            not no_with_blank_reason,
            'every "No" gate row includes a non-empty justification',
        )
    )
    checks.append(
        _result(
            "no_gates_justify_by_need_not_existence",
            path.name,
            not no_with_existence_reason,
            'every "No" gate justification explains why the initiative does not need the gate'
            if not no_with_existence_reason
            else f'"No" justification must explain why the gate is not needed, not that the artifact '
                 f'does not exist yet — offending gates: {bad_gate_names}',
        )
    )
    checks.append(
        _result(
            "readiness_score_is_numeric",
            path.name,
            bool(re.search(r"\|\s*Readiness score\s*\|\s*\d+\s*(?:/\s*100)?\s*\|", text)),
            "readiness score contains a real numeric value",
        )
    )
    checks.append(
        _result(
            "decision_is_populated",
            path.name,
            bool(re.search(r"\|\s*Decision\s*\|\s*(?!\s*\|).+\|", text)),
            "decision row is populated",
        )
    )
    return checks


def _validate_bdd_directory(path: Path, workspace_root: Path) -> list[dict[str, str]]:
    checks = []
    checks.extend(_non_empty_directory(path))
    all_files = sorted(path.glob("*.md"))
    feature_files = [f for f in all_files if re.match(r"^F-\d+", f.name)]
    wrong_files = [f for f in all_files if not re.match(r"^F-\d+", f.name)]
    checks.append(
        _result(
            "has_feature_files",
            path.name,
            bool(feature_files),
            "directory contains F-NNN.md feature files" if feature_files
            else f"no F-NNN.md files found — got {[f.name for f in all_files]} instead; each feature must be a separate F-NNN.md file",
        )
    )
    if wrong_files:
        checks.append(
            _result(
                "no_wrongly_named_files",
                path.name,
                False,
                f"unexpected file(s) {[f.name for f in wrong_files]} — BDD output must be F-NNN.md files, not a single scenarios.md or similar",
            )
        )
    if feature_files:
        for feature_file in feature_files:
            sample = _read_text(feature_file)
            has_gherkin = "```gherkin" in sample and "Scenario:" in sample
            checks.append(
                _result(
                    "has_gherkin",
                    feature_file.name,
                    has_gherkin,
                    "feature file contains full Gherkin scenarios" if has_gherkin
                    else f"{feature_file.name}: no ```gherkin block with Scenario: found",
                )
            )
            has_then = bool(re.search(r"^\s+Then\s", sample, re.MULTILINE))
            checks.append(
                _result(
                    "gherkin_has_then",
                    feature_file.name,
                    has_then,
                    "Gherkin scenarios have Then clauses" if has_then
                    else f"{feature_file.name}: no Then clause found — scenarios must have observable outcomes",
                )
            )
    return checks


def _validate_use_case_specs_directory(path: Path, workspace_root: Path) -> list[dict[str, str]]:
    """Validator for business-analysis/use-cases/ — expects one UC-NNN.md file per use case."""
    checks = []
    checks.extend(_non_empty_directory(path))
    uc_files = sorted(path.glob("UC-*.md"))
    checks.append(
        _result(
            "has_uc_detail_files",
            path.name,
            bool(uc_files),
            "directory contains UC-NNN.md detail files" if uc_files else "no UC-NNN.md files found — wrong structure (got sub-folders instead of UC-NNN.md files?)",
        )
    )
    story_folders = [child for child in path.iterdir() if child.is_dir()]
    checks.append(
        _result(
            "no_story_subfolders",
            path.name,
            not story_folders,
            "directory contains flat UC-NNN.md files as expected" if not story_folders else f"found story sub-folders ({[f.name for f in story_folders]}) — use-case specs must be flat UC-NNN.md files, not OpenSpec story folders",
        )
    )

    _UC_REQUIRED_SECTIONS = [
        "## Overview",
        "## Preconditions",
        "## Main Success Scenario",
        "## Alternative Flows",
        "## Postconditions",
        "## FR Sources",
    ]

    for uc_file in uc_files:
        text = _read_text(uc_file)
        label = uc_file.name

        for heading in _UC_REQUIRED_SECTIONS:
            tag = heading.strip("# ").lower().replace(" ", "_")
            checks.append(
                _result(
                    f"uc_has_{tag}",
                    label,
                    heading in text,
                    f"{label}: {heading} section present" if heading in text
                    else f"{label}: missing required section '{heading}'",
                )
            )

        has_overview_table = bool(re.search(
            r"\|\s*Use Case ID\s*\|", text, flags=re.IGNORECASE
        ))
        checks.append(
            _result(
                "uc_has_overview_table",
                label,
                has_overview_table,
                f"{label}: overview table with Use Case ID present" if has_overview_table
                else f"{label}: missing overview table (expected '| Use Case ID | UC-NNN |' row)",
            )
        )

        has_scenario_table = bool(re.search(
            r"^\|\s*\d+\s*\|", text, flags=re.MULTILINE
        ))
        checks.append(
            _result(
                "uc_main_scenario_is_table",
                label,
                has_scenario_table,
                f"{label}: main scenario uses step table format" if has_scenario_table
                else f"{label}: main scenario must use '| Step | Actor | Action |' table, not a numbered list",
            )
        )

        alt_section = _section_block(text, "## Alternative Flows")
        has_alt_content = bool(re.search(r"###\s+A\d+:", alt_section))
        checks.append(
            _result(
                "uc_has_alternative_flow_content",
                label,
                has_alt_content,
                f"{label}: alternative flows section contains at least one A1: flow" if has_alt_content
                else f"{label}: alternative flows section is empty or missing 'A1:' sub-heading",
            )
        )

        has_postcondition_success = bool(re.search(
            r"\*\*Success:?\*\*", text, flags=re.IGNORECASE
        ))
        checks.append(
            _result(
                "uc_postconditions_structured",
                label,
                has_postcondition_success,
                f"{label}: postconditions include Success section" if has_postcondition_success
                else f"{label}: postconditions must include '**Success:**' and '**Failure:**' sub-sections",
            )
        )

        has_fr_trace = bool(re.search(r"FR-\d{3}", text))
        checks.append(
            _result(
                "uc_has_fr_trace",
                label,
                has_fr_trace,
                f"{label}: traces to at least one FR-NNN" if has_fr_trace
                else f"{label}: no FR-NNN reference found — use case must trace to requirements",
            )
        )

        meaningful_lines = [line for line in text.splitlines() if line.strip()]
        checks.append(
            _result(
                "uc_not_stub",
                label,
                len(meaningful_lines) >= 20,
                f"{label}: has {len(meaningful_lines)} lines of content" if len(meaningful_lines) >= 20
                else f"{label}: only {len(meaningful_lines)} lines — too shallow, expected at least 20 meaningful lines per use case",
            )
        )

    uc_md = workspace_root / "business-analysis" / "use-cases.md"
    if uc_md.exists():
        catalog_count = _table_row_count(_read_text(uc_md), r"UC-\d{3}")
        checks.append(
            _result(
                "uc_file_count_matches_catalog",
                path.name,
                catalog_count == 0 or len(uc_files) >= catalog_count,
                f"UC detail file count ({len(uc_files)}) matches catalog ({catalog_count})",
            )
        )
    return checks


def _validate_story_package_directory(path: Path, workspace_root: Path) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []
    story_files = sorted(path.rglob("story.md"))
    if not story_files:
        checks.append(_result("story_has_id", path.name, False, "no story.md files found in specs/"))
        return checks

    _GENERIC_ACTORS = re.compile(
        r"As a\s+\*{0,2}(user|person|someone|actor)\b",
        re.IGNORECASE,
    )
    _GENERIC_TITLE_PATTERNS = [
        "Story 1", "Story 2", "Implement feature", "Implement functionality",
        "TBD", "TODO", "{{",
    ]
    _GENERIC_THEN = re.compile(
        r"^\s+Then\s+(it works|it succeeds|the feature works|success|done)\s*$",
        re.IGNORECASE | re.MULTILINE,
    )
    _PLACEHOLDER = re.compile(r"\{\{|\}\}|(?<!\w)NNN(?!\w)|(?<!\w)XXX(?!\w)|TBD|TODO|\[actor\]|\[capability\]")

    for story_file in story_files:
        label = story_file.parent.name
        try:
            text = _read_text(story_file)
        except OSError:
            checks.append(_result("story_has_id", label, False, f"{label}/story.md: could not read file"))
            continue

        lines = text.splitlines()
        first_heading = next((l for l in lines if l.startswith("# ")), "")

        # story_has_id — accept both F-NNN.N (specs/ structure) and S-NNN.N (epics/ structure)
        _story_id_re = r"[FS]-\d{3}\.\d+"
        checks.append(_result(
            "story_has_id", label,
            bool(re.search(_story_id_re, first_heading)),
            f"{label}/story.md: first heading contains story ID" if re.search(_story_id_re, first_heading)
            else f"{label}/story.md: first heading does not contain a story ID (S-NNN.N or F-NNN.N)",
        ))

        # story_not_generic_title
        generic_hit = next((p for p in _GENERIC_TITLE_PATTERNS if p in first_heading), None)
        checks.append(_result(
            "story_not_generic_title", label,
            generic_hit is None,
            f"{label}/story.md: title is specific" if generic_hit is None
            else f"{label}/story.md: title contains generic text '{generic_hit}'",
        ))

        # story_has_actor
        has_as_a = "As a" in text or "As an" in text
        has_generic = bool(_GENERIC_ACTORS.search(text))
        checks.append(_result(
            "story_has_actor", label,
            has_as_a and not has_generic,
            f"{label}/story.md: user story has a named, non-generic actor" if (has_as_a and not has_generic)
            else f"{label}/story.md: missing named actor — 'As a user/person/someone/actor' is too generic",
        ))

        # story_has_business_outcome
        checks.append(_result(
            "story_has_business_outcome", label,
            "so that" in text,
            f"{label}/story.md: user story has a business outcome (so that ...)" if "so that" in text
            else f"{label}/story.md: missing 'so that' business outcome in user story",
        ))

        # story_has_requirements_link
        checks.append(_result(
            "story_has_requirements_link", label,
            bool(re.search(r"FR-\d{3}", text)),
            f"{label}/story.md: links to at least one FR-NNN requirement" if re.search(r"FR-\d{3}", text)
            else f"{label}/story.md: no FR-NNN requirement reference found",
        ))

        # story_has_acceptance_criteria
        ac_match = re.search(r"^## 4\. Acceptance Criteria", text, re.MULTILINE)
        if ac_match:
            after_ac = text[ac_match.end():]
            next_section = re.search(r"^##\s", after_ac, re.MULTILINE)
            ac_body = after_ac[:next_section.start()] if next_section else after_ac
            ac_lines = [l for l in ac_body.splitlines() if l.strip()]
            ac_ok = len(ac_lines) >= 2
        else:
            ac_ok = False
        checks.append(_result(
            "story_has_acceptance_criteria", label, ac_ok,
            f"{label}/story.md: Section 4 Acceptance Criteria has content" if ac_ok
            else f"{label}/story.md: missing or empty '## 4. Acceptance Criteria' section",
        ))

        # story_has_bdd_scenarios
        has_gherkin = "```gherkin" in text
        checks.append(_result(
            "story_has_bdd_scenarios", label, has_gherkin,
            f"{label}/story.md: contains at least one Gherkin block" if has_gherkin
            else f"{label}/story.md: no ```gherkin block found — BDD scenarios are required",
        ))

        # story_bdd_has_then
        if has_gherkin:
            gherkin_blocks = re.findall(r"```gherkin(.*?)```", text, re.DOTALL)
            has_then = any(
                re.search(r"^\s{2,}Then\s", block, re.MULTILINE)
                for block in gherkin_blocks
            )
            checks.append(_result(
                "story_bdd_has_then", label, has_then,
                f"{label}/story.md: Gherkin scenarios have Then clauses" if has_then
                else f"{label}/story.md: Gherkin block found but no 'Then' clause — not valid Gherkin",
            ))

            # story_bdd_not_generic (warn only)
            has_generic_then = any(
                bool(_GENERIC_THEN.search(block)) for block in gherkin_blocks
            )
            if has_generic_then:
                checks.append({
                    "name": "story_bdd_not_generic",
                    "target": label,
                    "result": "warn",
                    "detail": f"{label}/story.md: Then clause contains vague outcome ('it works', 'it succeeds', etc.)",
                })

        # story_has_implementation_context
        ic_match = re.search(r"^## 6\. Implementation Context", text, re.MULTILINE)
        if ic_match:
            after_ic = text[ic_match.end():]
            next_section = re.search(r"^##\s", after_ic, re.MULTILINE)
            ic_body = after_ic[:next_section.start()] if next_section else after_ic
            ic_lines = [l for l in ic_body.splitlines() if l.strip()]
            ic_ok = len(ic_lines) >= 3
        else:
            ic_ok = False
        checks.append(_result(
            "story_has_implementation_context", label, ic_ok,
            f"{label}/story.md: Section 6 Implementation Context has content" if ic_ok
            else f"{label}/story.md: missing or empty '## 6. Implementation Context' section (need 3+ lines)",
        ))

        # story_has_coding_prompt
        has_coding_prompt = bool(re.search(r"^## 12\. Coding-Agent Prompt", text, re.MULTILINE))
        checks.append(_result(
            "story_has_coding_prompt", label, has_coding_prompt,
            f"{label}/story.md: Section 12 Coding-Agent Prompt present" if has_coding_prompt
            else f"{label}/story.md: missing '## 12. Coding-Agent Prompt' section",
        ))

        # coding_prompt_has_constraints
        if has_coding_prompt:
            cp_match = re.search(r"^## 12\. Coding-Agent Prompt", text, re.MULTILINE)
            cp_body = text[cp_match.end():] if cp_match else ""
            has_constraints = any(
                kw in cp_body.lower() for kw in ["constraint", "must not", "do not touch"]
            )
            checks.append(_result(
                "coding_prompt_has_constraints", label, has_constraints,
                f"{label}/story.md: coding prompt includes constraints" if has_constraints
                else f"{label}/story.md: coding prompt missing constraints ('constraint', 'must not', or 'do not touch')",
            ))

            # coding_prompt_has_tests
            has_tests = "test" in cp_body.lower()
            checks.append(_result(
                "coding_prompt_has_tests", label, has_tests,
                f"{label}/story.md: coding prompt mentions tests" if has_tests
                else f"{label}/story.md: coding prompt does not mention tests",
            ))

        # story_no_placeholders
        placeholder_match = _PLACEHOLDER.search(text)
        checks.append(_result(
            "story_no_placeholders", label,
            placeholder_match is None,
            f"{label}/story.md: no unfilled placeholders found" if placeholder_match is None
            else f"{label}/story.md: unfilled placeholder found: '{placeholder_match.group()}'",
        ))

    return checks


def _validate_specs_directory(path: Path, workspace_root: Path) -> list[dict[str, str]]:
    checks = []
    checks.extend(_non_empty_directory(path))
    dependency_graph = path / "dependency-graph.md"
    checks.append(
        _result(
            "has_dependency_graph",
            dependency_graph.name,
            dependency_graph.exists(),
            "dependency graph exists",
        )
    )
    story_folders = [child for child in path.iterdir() if child.is_dir()]
    checks.append(
        _result(
            "has_story_folders",
            path.name,
            bool(story_folders),
            "specs directory contains story folders" if story_folders else "specs directory has no story folders",
        )
    )
    if story_folders:
        first = story_folders[0]
        required = ["story.md", "design.md", "tasks.md", "coding-prompt.md"]
        for filename in required:
            checks.append(
                _result(
                    f"has_{filename.replace('.', '_')}",
                    first.name,
                    (first / filename).exists(),
                    f"{filename} exists in sample story folder",
                )
            )
    return checks


def _validate_exposed_api_spec_directory(path: Path, workspace_root: Path) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []
    checks.extend(_non_empty_directory(path))
    spec_files = sorted(path.glob("*.md"))
    if not spec_files:
        return checks

    for spec_file in spec_files:
        text = _read_text(spec_file)
        label = spec_file.name

        checks.append(_result(
            "exposed_api_has_endpoints",
            label,
            bool(re.search(r"\|\s*EP-\d+\s*\|\s*(GET|POST|PUT|PATCH|DELETE)\s*\|\s*/v\d+/", text)),
            f"{label}: endpoint catalog contains a METHOD and /v1/ path row",
        ))

        auth_row = re.search(r"\|\s*Auth mechanism\s*\|\s*([^|]+?)\s*\|", text, flags=re.IGNORECASE)
        auth_ok = bool(auth_row) and _cell_is_populated(auth_row.group(1)) if auth_row else False
        checks.append(_result(
            "exposed_api_has_auth",
            label,
            auth_ok,
            f"{label}: Auth mechanism row is present and populated",
        ))

        contract_row = re.search(
            r"\|\s*Contract mode\s*\|\s*(product|internal|coordinated)\s*\|",
            text,
            flags=re.IGNORECASE,
        )
        checks.append(_result(
            "exposed_api_has_contract_mode",
            label,
            bool(contract_row),
            f"{label}: Contract mode row contains a valid value (product/internal/coordinated)",
        ))

        sla_section = re.search(r"^##\s+SLA", text, flags=re.MULTILINE | re.IGNORECASE)
        sla_has_row = False
        if sla_section:
            after_sla = text[sla_section.end():]
            next_section = re.search(r"^##\s", after_sla, flags=re.MULTILINE)
            sla_body = after_sla[:next_section.start()] if next_section else after_sla
            sla_has_row = bool(re.search(r"^\|\s*EP-\d+\s*\|", sla_body, flags=re.MULTILINE))
        checks.append(_result(
            "exposed_api_has_sla",
            label,
            sla_has_row,
            f"{label}: SLA section contains at least one EP-NNN row",
        ))

        checks.append(_result(
            "exposed_api_no_placeholders",
            label,
            _placeholders_absent(text, extra_patterns=[r"\{\{", r"\}\}", r"\bNNN\b", r"\bTBD\b", r"\bTODO\b"]),
            f"{label}: no unfilled placeholder markers",
        ))

        checks.append(_result(
            "exposed_api_has_story_ref",
            label,
            bool(re.search(r"[FS]-\d{3}\.\d+", text)),
            f"{label}: endpoint table references at least one story (S-NNN.N or F-NNN.N)",
        ))

    return checks


def _validate_consumed_api_spec_directory(path: Path, workspace_root: Path) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []
    checks.extend(_non_empty_directory(path))
    spec_files = sorted(path.glob("*.md"))
    if not spec_files:
        return checks

    for spec_file in spec_files:
        text = _read_text(spec_file)
        label = spec_file.name

        checks.append(_result(
            "consumed_api_has_endpoints",
            label,
            bool(re.search(r"\|\s*EP-\d+\s*\|", text)),
            f"{label}: contains at least one endpoint row",
        ))

        auth_row = re.search(r"\|\s*Auth mechanism\s*\|\s*([^|]+?)\s*\|", text, flags=re.IGNORECASE)
        auth_ok = bool(auth_row) and _cell_is_populated(auth_row.group(1)) if auth_row else False
        checks.append(_result(
            "consumed_api_has_auth",
            label,
            auth_ok,
            f"{label}: Auth mechanism row is present and populated",
        ))

        fallback_row = re.search(r"\|\s*Fallback behaviour\s*\|\s*([^|]+?)\s*\|", text, flags=re.IGNORECASE)
        fallback_ok = (
            bool(fallback_row)
            and _cell_is_populated(fallback_row.group(1))
            and not re.search(r"\bTBD\b", fallback_row.group(1), flags=re.IGNORECASE)
        ) if fallback_row else False
        checks.append(_result(
            "consumed_api_has_fallback",
            label,
            fallback_ok,
            f"{label}: Fallback behaviour row is present with an actionable value (not TBD)",
        ))

        checks.append(_result(
            "consumed_api_has_pii_section",
            label,
            bool(re.search(r"^##.*PII", text, flags=re.MULTILINE | re.IGNORECASE)),
            f"{label}: PII and Data Residency section is present",
        ))

        checks.append(_result(
            "consumed_api_no_placeholders",
            label,
            _placeholders_absent(text, extra_patterns=[r"\{\{", r"\}\}", r"\bNNN\b", r"\bTBD\b", r"\bTODO\b"]),
            f"{label}: no unfilled placeholder markers",
        ))

    return checks


def _validate_integration_spec_directory(path: Path, workspace_root: Path) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []
    checks.extend(_non_empty_directory(path))
    spec_files = sorted(path.glob("*.md"))
    if not spec_files:
        return checks

    for spec_file in spec_files:
        text = _read_text(spec_file)
        label = spec_file.name

        timeout_row = re.search(r"\|\s*Timeout per request\s*\|\s*([^|]+?)\s*\|", text, flags=re.IGNORECASE)
        timeout_ok = bool(timeout_row) and bool(re.search(r"\d+", timeout_row.group(1))) if timeout_row else False
        checks.append(_result(
            "integration_has_timeout",
            label,
            timeout_ok,
            f"{label}: Timeout per request row contains a numeric value (ms)",
        ))

        retry_row = re.search(r"\|\s*Max retries\s*\|\s*([^|]+?)\s*\|", text, flags=re.IGNORECASE)
        retry_ok = bool(retry_row) and bool(re.search(r"\d+", retry_row.group(1))) if retry_row else False
        checks.append(_result(
            "integration_has_retry",
            label,
            retry_ok,
            f"{label}: Max retries row contains a numeric value",
        ))

        fallback_row = re.search(r"\|\s*Fallback behaviour\s*\|\s*([^|]+?)\s*\|", text, flags=re.IGNORECASE)
        fallback_ok = (
            bool(fallback_row)
            and _cell_is_populated(fallback_row.group(1))
            and not re.search(r"\bTBD\b", fallback_row.group(1), flags=re.IGNORECASE)
        ) if fallback_row else False
        checks.append(_result(
            "integration_has_fallback",
            label,
            fallback_ok,
            f"{label}: Fallback behaviour row is present and not TBD",
        ))

        has_success_event = bool(re.search(r"\|\s*Success event\s*\|\s*([^|]+?)\s*\|", text, flags=re.IGNORECASE))
        has_failure_event = bool(re.search(r"\|\s*Failure event\s*\|\s*([^|]+?)\s*\|", text, flags=re.IGNORECASE))
        checks.append(_result(
            "integration_has_events",
            label,
            has_success_event and has_failure_event,
            f"{label}: Success event and Failure event rows are both present",
        ))

        checks.append(_result(
            "integration_no_placeholders",
            label,
            _placeholders_absent(text, extra_patterns=[r"\{\{", r"\}\}", r"\bNNN\b", r"\bTBD\b", r"\bTODO\b"]),
            f"{label}: no unfilled placeholder markers",
        ))

    return checks


def _validate_standalone_directory(path: Path, workspace_root: Path) -> list[dict[str, str]]:
    checks = []
    checks.extend(_non_empty_directory(path))
    deliverables = [child for child in path.iterdir() if child.is_dir()]
    checks.append(
        _result(
            "has_deliverable_folder",
            path.name,
            bool(deliverables),
            "standalone delivery contains a deliverable folder" if deliverables else "no deliverable folder found",
        )
    )
    if deliverables:
        first = deliverables[0]
        required = [
            "delivery-spec.md",
            "implementation-plan.md",
            "tasks.md",
            "validation-plan.md",
            "review-checklist.md",
        ]
        for filename in required:
            checks.append(
                _result(
                    f"has_{filename.replace('.', '_').replace('-', '_')}",
                    first.name,
                    (first / filename).exists(),
                    f"{filename} exists in sample deliverable folder",
                )
            )
    return checks


def _validate_review_package(path: Path, workspace_root: Path) -> list[dict[str, str]]:
    checks = []
    checks.extend(_non_empty_directory(path))
    checks.append(
        _result(
            "has_status",
            path.name,
            (path / "status.md").exists(),
            "review-package contains status.md",
        )
    )
    return checks


def _validate_directory_default(path: Path, workspace_root: Path) -> list[dict[str, str]]:
    return _non_empty_directory(path)


def _validate_file_default(path: Path, workspace_root: Path) -> list[dict[str, str]]:
    return _non_empty_file(path)


# ---------------------------------------------------------------------------
# Template-driven validation
# ---------------------------------------------------------------------------

def _parse_template_contract(template_path: Path) -> dict[str, Any]:
    """Extract structural contract from an artifact template.

    Returns a dict with:
      headings: list of '## Heading' strings found in the template
      tables: dict mapping heading -> list of column-name lists (one per table in that section)
      has_tables: bool
      line_count: int (meaningful lines in the template)
    """
    text = _read_text(template_path)
    lines = text.splitlines()

    headings: list[str] = []
    tables: dict[str, list[list[str]]] = {}
    current_heading: str | None = None

    for line in lines:
        stripped = line.strip()
        if re.match(r"^##\s+", stripped) and not re.match(r"^###\s+", stripped):
            current_heading = stripped
            headings.append(current_heading)
            tables.setdefault(current_heading, [])
            continue

        if not stripped.startswith("|") or current_heading is None:
            continue
        if re.match(r"^\|(?:\s*:?-{3,}:?\s*\|)+\s*$", stripped):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if cells and all(cell.replace("-", "").strip() == "" for cell in cells):
            continue
        is_header = any(
            re.search(r"\{\{", cell) or "/" in cell or cell in {"", "…"}
            for cell in cells
        )
        if not is_header:
            tables[current_heading].append(cells)
        elif not tables[current_heading]:
            tables[current_heading].append(cells)

    return {
        "headings": headings,
        "tables": tables,
        "has_tables": any(bool(cols) for cols in tables.values()),
        "line_count": len([l for l in lines if l.strip()]),
    }


def _is_template_placeholder_cell(value: str) -> bool:
    """Return True if a cell value looks like an unfilled template placeholder."""
    text = value.strip()
    if not text:
        return True
    if re.search(r"\{\{", text):
        return True
    if re.search(r"\|", text) and "/" in text:
        return True
    if text in {"…", "..."}:
        return True
    return False


def _validate_from_template(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
) -> list[dict[str, str]]:
    """Validate an artifact against its template's structural contract."""
    template_ref = _artifact_template_ref(action)
    if not template_ref:
        return _non_empty_file(path)

    template_path = workspace.FRAMEWORK_ROOT / Path(template_ref).relative_to(".b2s") \
        if template_ref.startswith(".b2s/") else workspace.FRAMEWORK_ROOT.parent / template_ref
    if not template_path.exists():
        return [_result(
            "template_exists", path.name, False,
            f"artifact_template_ref '{template_ref}' not found at {template_path}",
        )]

    contract = _parse_template_contract(template_path)
    text = _read_text(path)
    checks: list[dict[str, str]] = []

    checks.extend(_non_empty_file(path))

    for heading in contract["headings"]:
        if re.search(r"\{\{", heading):
            continue
        tag = heading.strip("# ").lower().replace(" ", "_")
        found = heading in text
        checks.append(_result(
            f"tmpl_section_{tag}", path.name, found,
            f"{heading} section present" if found
            else f"missing section '{heading}' required by template",
        ))

    if contract["has_tables"]:
        checks.append(_result(
            "tmpl_has_tables", path.name, _has_any_table(text),
            "artifact contains at least one table" if _has_any_table(text)
            else "template requires tables but artifact contains none",
        ))

    for heading, col_lists in contract["tables"].items():
        if not col_lists:
            continue
        expected_cols = col_lists[0]
        if all(_is_template_placeholder_cell(c) for c in expected_cols):
            continue

        section_text = _section_block(text, heading)
        if not section_text.strip():
            continue

        section_rows = []
        for line in section_text.splitlines():
            s = line.strip()
            if not s.startswith("|"):
                continue
            if re.match(r"^\|(?:\s*:?-{3,}:?\s*\|)+\s*$", s):
                continue
            cells = [cell.strip() for cell in s.strip("|").split("|")]
            if cells and not all(cell.replace("-", "").strip() == "" for cell in cells):
                section_rows.append(cells)

        data_rows = [r for r in section_rows if len(r) >= 2]
        prose_lines = [
            l for l in section_text.splitlines()
            if l.strip() and not l.strip().startswith("|") and not l.strip().startswith("---")
        ]
        has_table_content = len(data_rows) >= 2
        has_prose_content = len(prose_lines) >= 2
        checks.append(_result(
            f"tmpl_table_populated_{heading.strip('# ').lower().replace(' ', '_')}",
            path.name,
            has_table_content or has_prose_content,
            f"'{heading}' has content (table rows: {len(data_rows)}, prose lines: {len(prose_lines)})"
            if has_table_content or has_prose_content
            else f"'{heading}' needs a populated table or meaningful prose, found {len(data_rows)} table rows and {len(prose_lines)} prose lines",
        ))

    expected_min_lines = max(20, contract["line_count"] // 2)
    meaningful = len([l for l in text.splitlines() if l.strip()])
    checks.append(_result(
        "tmpl_content_depth", path.name,
        meaningful >= expected_min_lines,
        f"artifact has {meaningful} lines (minimum {expected_min_lines})" if meaningful >= expected_min_lines
        else f"artifact too shallow: {meaningful} lines, expected at least {expected_min_lines} based on template",
    ))

    checks.append(_result(
        "tmpl_placeholders_absent", path.name,
        _placeholders_absent(text, _forbidden_placeholders(action)),
        "no known placeholder markers found",
    ))

    return checks


def _rule_requirement_has_id(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> dict[str, str]:
    text = _read_text(path)
    has_fr = bool(re.search(r"^\|\s*FR-\d{3}\s*\|", text, flags=re.MULTILINE))
    has_nfr = bool(re.search(r"^\|\s*NFR-\d{3}\s*\|", text, flags=re.MULTILINE))
    has_constraint = bool(re.search(r"^\|\s*C-\d{3}\s*\|", text, flags=re.MULTILINE))
    passed = has_fr and has_nfr and has_constraint
    return _named_rule_result(
        "requirement_has_id",
        artifact_path,
        passed,
        "functional, non-functional, and constraint rows all use typed identifiers",
        severity="required",
    )


def _rule_requirement_is_testable(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> dict[str, str]:
    passed = (
        _check_passed(base_checks, "fr_not_template_only")
        and _check_passed(base_checks, "nfr_section_not_empty")
        and _check_passed(base_checks, "constraints_section_not_empty")
    )
    return _named_rule_result(
        "requirement_is_testable",
        artifact_path,
        passed,
        "requirements content is populated and avoids template-only wording",
        severity="required",
    )


def _rule_architecture_lists_impacted_systems(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> dict[str, str]:
    return _named_rule_result(
        "architecture_lists_impacted_systems",
        artifact_path,
        _any_check_passed(
            base_checks,
            ["fit_section_populated", "tmpl_table_populated_initiative-architecture_fit"],
        ),
        "architecture review lists impacted systems or feature-area fit explicitly",
        severity="required",
    )


def _rule_architecture_lists_constraints(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> dict[str, str]:
    return _named_rule_result(
        "architecture_lists_constraints",
        artifact_path,
        _any_check_passed(
            base_checks,
            [
                "constraints_have_rationale_and_consequence",
                "tmpl_table_populated_architecture_constraints",
            ],
        ),
        "architecture review lists constraints with rationale and consequence",
        severity="required",
    )


def _rule_architecture_lists_risks(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> dict[str, str]:
    passed = _any_check_passed(
        base_checks,
        ["quality_attributes_populated", "tmpl_table_populated_quality_attribute_assessment"],
    )
    return _named_rule_result(
        "architecture_lists_risks",
        artifact_path,
        passed,
        "architecture review contains explicit risk-bearing quality and analysis content",
        severity="required",
    )


def _rule_readiness_has_decision(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> dict[str, str]:
    passed = _check_passed(base_checks, "decision_is_populated") and _check_passed(
        base_checks,
        "readiness_score_is_numeric",
    )
    return _named_rule_result(
        "readiness_has_decision",
        artifact_path,
        passed,
        "readiness artifact contains a populated decision and numeric score",
        severity="required",
    )


def _rule_contract_has_schema_definitions(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> dict[str, str]:
    text = _read_text(path)
    passed = False
    for heading in ["## Schema Definitions", "## Event Definitions"]:
        if heading in text and _section_non_placeholder(text, heading):
            passed = True
            break
    return _named_rule_result(
        "contract_has_schema_definitions",
        artifact_path,
        passed,
        "contract includes a populated schema or event definitions section",
        severity="required",
    )


def _rule_nfr_assessment_has_ids(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> dict[str, str]:
    text = _read_text(path)
    passed = bool(re.search(r"^\|\s*NFR-\d{3}\s*\|", text, flags=re.MULTILINE))
    return _named_rule_result(
        "nfr_assessment_has_ids",
        artifact_path,
        passed,
        "nfr assessment includes typed NFR identifiers",
        severity="required",
    )


def _rule_nfr_assessment_covers_core_domains(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> dict[str, str]:
    text = _read_text(path)
    headings = [
        "## Security",
        "## Availability",
        "## Resiliency",
        "## Observability",
        "## Supportability",
        "## Scalability",
        "## Compliance",
    ]
    passed = all(heading in text and _section_non_placeholder(text, heading) for heading in headings)
    return _named_rule_result(
        "nfr_assessment_covers_core_domains",
        artifact_path,
        passed,
        "nfr assessment covers all required enterprise NFR domains",
        severity="required",
    )


def _rule_nfr_assessment_has_decision(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> dict[str, str]:
    text = _read_text(path)
    passed = "## Decision" in text and _section_non_placeholder(text, "## Decision")
    return _named_rule_result(
        "nfr_assessment_has_decision",
        artifact_path,
        passed,
        "nfr assessment includes an explicit delivery decision",
        severity="required",
    )


def _rule_all_source_requirements_present(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> dict[str, str]:
    req_ids = _all_requirement_ids(workspace_root)
    referenced = _all_requirement_references_in_artifact(path)
    missing = sorted(req_ids - referenced)
    return _named_rule_result(
        "all_source_requirements_present",
        artifact_path,
        len(missing) == 0,
        f"all {len(req_ids)} canonical requirements are referenced"
        if len(missing) == 0
        else f"{len(missing)} canonical requirements are missing: {missing[:10]}",
        severity="required",
    )


def _rule_no_unknown_requirement_references(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> dict[str, str]:
    req_ids = _all_requirement_ids(workspace_root)
    referenced = _all_requirement_references_in_artifact(path)
    unknown = sorted(referenced - req_ids)
    return _named_rule_result(
        "no_unknown_requirement_references",
        artifact_path,
        len(unknown) == 0,
        "all referenced requirement IDs exist in atomic requirements"
        if len(unknown) == 0
        else f"unknown requirement references found: {unknown[:10]}",
        severity="required",
    )


def _rule_requirement_title_consistency(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> dict[str, str]:
    canonical = _canonical_requirements(workspace_root)
    artifact_pairs = _artifact_requirement_pairs(path)
    mismatches: list[str] = []
    for req_id, artifact_title in artifact_pairs.items():
        canonical_req = canonical.get(req_id)
        if canonical_req is None:
            continue
        if not artifact_title.strip():
            mismatches.append(f"{req_id} has blank downstream title")
            continue
        if _normalized_title(artifact_title) != canonical_req["normalized_title"]:
            mismatches.append(
                f"{req_id} title mismatch: downstream='{artifact_title}' canonical='{canonical_req['title']}'"
            )
    return _named_rule_result(
        "requirement_title_consistency",
        artifact_path,
        len(mismatches) == 0,
        "downstream requirement titles match canonical titles"
        if len(mismatches) == 0
        else "; ".join(mismatches[:5]),
        severity="required",
    )


def _rule_requirement_semantics_preserved(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> dict[str, str]:
    if not path.is_dir():
        return _named_rule_result(
            "requirement_semantics_preserved",
            artifact_path,
            True,
            "semantic preservation is checked on epic/story directories only",
            severity="required",
        )

    canonical = _canonical_requirements(workspace_root)
    failures: list[str] = []

    for epic_dir in sorted([d for d in path.iterdir() if d.is_dir() and d.name.startswith("E-")]):
        stories_dir = epic_dir / "stories"
        if not stories_dir.exists():
            continue
        for story_file in sorted(stories_dir.glob("S-*.md")):
            if story_file.name.endswith(".prompt.md"):
                continue
            text = _read_text(story_file)
            story_titles = _extract_requirement_titles_from_story(text)
            semantic_text = "\n".join(
                [
                    _section_block(text, "## User Story"),
                    _section_block(text, "## Business Context"),
                    _section_block(text, "## Acceptance Criteria"),
                ]
            )
            story_tokens = _keywords(semantic_text)
            for req_id in story_titles:
                canonical_req = canonical.get(req_id)
                if canonical_req is None:
                    continue
                req_keywords = canonical_req["keywords"]
                if not req_keywords:
                    continue
                overlap = req_keywords & story_tokens
                minimum = 1 if len(req_keywords) < 4 else 2
                if len(overlap) < minimum:
                    failures.append(
                        f"{epic_dir.name}/{story_file.name} lacks semantic overlap for {req_id}"
                    )

    return _named_rule_result(
        "requirement_semantics_preserved",
        artifact_path,
        len(failures) == 0,
        "story behavior preserves linked requirement semantics"
        if len(failures) == 0
        else "; ".join(failures[:5]),
        severity="required",
    )


def _rule_open_questions_propagated(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> dict[str, str]:
    canonical = _canonical_requirements(workspace_root)
    propagated_failures: list[str] = []

    if path.is_dir():
        story_text_by_req: dict[str, str] = {}
        for epic_dir in sorted([d for d in path.iterdir() if d.is_dir() and d.name.startswith("E-")]):
            stories_dir = epic_dir / "stories"
            if not stories_dir.exists():
                continue
            for story_file in sorted(stories_dir.glob("S-*.md")):
                if story_file.name.endswith(".prompt.md"):
                    continue
                text = _read_text(story_file)
                for req_id in _extract_requirement_titles_from_story(text):
                    story_text_by_req[req_id] = story_text_by_req.get(req_id, "") + "\n" + text

        for req_id, requirement in canonical.items():
            unresolved = " ".join([
                v for v in [
                    requirement.get("blocking_questions", ""),
                    requirement.get("ambiguities", ""),
                ] if v.strip().lower() not in ("", "none", "n/a", "—", "-")
            ]).strip()
            if not unresolved:
                continue
            story_text = story_text_by_req.get(req_id, "")
            if not story_text:
                continue
            has_open_questions_section = "## Open Questions" in story_text
            overlap = _keywords(unresolved) & _keywords(_section_block(story_text, "## Open Questions"))
            if not has_open_questions_section or not overlap:
                propagated_failures.append(f"{req_id} has unresolved questions not propagated to stories")
    else:
        text = _read_text(path)
        for req_id, requirement in canonical.items():
            unresolved = " ".join([
                v for v in [
                    requirement.get("blocking_questions", ""),
                    requirement.get("ambiguities", ""),
                ] if v.strip().lower() not in ("", "none", "n/a", "—", "-")
            ]).strip()
            if not unresolved:
                continue
            if req_id not in text:
                continue
            row_match = re.search(
                rf"^\|\s*{re.escape(req_id)}\s*\|.*$",
                text,
                flags=re.MULTILINE,
            )
            row_text = row_match.group(0) if row_match else ""
            overlap = _keywords(unresolved) & _keywords(row_text)
            if not overlap:
                propagated_failures.append(f"{req_id} unresolved questions are not surfaced in coverage report")

    return _named_rule_result(
        "open_questions_propagated",
        artifact_path,
        len(propagated_failures) == 0,
        "open questions and ambiguities are propagated downstream"
        if len(propagated_failures) == 0
        else "; ".join(propagated_failures[:5]),
        severity="required",
    )


def _rule_coverage_claim_matches_evidence(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> dict[str, str]:
    text = _read_text(path)
    rows = _section_table_rows(text, "## Full Coverage Matrix")
    matrix_rows = [
        row for row in rows
        if len(row) >= 9 and re.fullmatch(r"(?:FR|REQ|NFR|C)-\d{3}", row[0].strip())
    ]
    story_files = set()
    for story_file in (workspace_root / "epics").rglob("S-*.md"):
        if story_file.is_file() and not story_file.name.endswith(".prompt.md"):
            m = re.match(r"(S-\d{3}\.\d+)", story_file.stem)
            if m:
                story_files.add(m.group(1))
    covered = 0
    mismatches: list[str] = []
    for row in matrix_rows:
        req_id = row[0].strip()
        story_id = row[5].strip()
        status = row[8].strip()
        if status == "Covered":
            if story_id == "—" or story_id not in story_files:
                mismatches.append(f"{req_id} marked Covered but story '{story_id}' is missing")
            else:
                covered += 1

    declared_total_match = re.search(
        r"\|\s*Total requirements \(from atomic-requirements\)\s*\|\s*(\d+)\s*\|",
        text,
    )
    declared_covered_match = re.search(
        r"\|\s*Covered by at least one story\s*\|\s*(\d+)\s*\|",
        text,
    )
    declared_pct_match = re.search(
        r"\|\s*Coverage percentage\s*\|\s*(\d+)%\s*\|",
        text,
    )
    declared_total = int(declared_total_match.group(1)) if declared_total_match else len(matrix_rows)
    declared_covered = int(declared_covered_match.group(1)) if declared_covered_match else covered
    declared_pct = int(declared_pct_match.group(1)) if declared_pct_match else (covered * 100 // declared_total if declared_total else 100)
    computed_pct = (covered * 100 // len(matrix_rows)) if matrix_rows else 100

    passed = (
        not mismatches
        and declared_total == len(matrix_rows)
        and declared_covered == covered
        and declared_pct == computed_pct
    )
    detail = (
        f"coverage summary matches evidence ({covered}/{len(matrix_rows)} covered, {computed_pct}%)"
        if passed
        else "; ".join(
            mismatches[:3]
            + [
                f"declared total={declared_total} computed total={len(matrix_rows)}",
                f"declared covered={declared_covered} computed covered={covered}",
                f"declared pct={declared_pct}% computed pct={computed_pct}%",
            ]
        )
    )
    return _named_rule_result(
        "coverage_claim_matches_evidence",
        artifact_path,
        passed,
        detail,
        severity="required",
    )


def _rule_selected_epics_have_implementation_contracts(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> dict[str, str]:
    selected = _selected_epic_ids(workspace_root)
    missing = [
        epic_id for epic_id in selected
        if not any(
            child.is_dir()
            and child.name.startswith(epic_id)
            and (child / "implementation-contract.md").exists()
            for child in path.iterdir()
        )
    ]
    return _named_rule_result(
        "selected_epics_have_implementation_contracts",
        artifact_path,
        len(selected) > 0 and len(missing) == 0,
        f"implementation contracts exist for selected epics: {selected}"
        if selected and len(missing) == 0
        else f"missing implementation contracts for epic(s): {missing or selected}",
        severity="required",
    )


def _rule_selected_epics_have_coding_handoffs(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> dict[str, str]:
    selected = _selected_epic_ids(workspace_root)
    missing = [
        epic_id for epic_id in selected
        if not any(
            child.is_dir()
            and child.name.startswith(epic_id)
            and (child / "coding-handoff.md").exists()
            for child in path.iterdir()
        )
    ]
    return _named_rule_result(
        "selected_epics_have_coding_handoffs",
        artifact_path,
        len(selected) > 0 and len(missing) == 0,
        f"coding handoffs exist for selected epics: {selected}"
        if selected and len(missing) == 0
        else f"missing coding handoffs for epic(s): {missing or selected}",
        severity="required",
    )


NAMED_RULES: dict[str, NamedRuleValidator] = {
    "requirement_has_id": _rule_requirement_has_id,
    "requirement_is_testable": _rule_requirement_is_testable,
    "all_source_requirements_present": _rule_all_source_requirements_present,
    "no_unknown_requirement_references": _rule_no_unknown_requirement_references,
    "requirement_title_consistency": _rule_requirement_title_consistency,
    "requirement_semantics_preserved": _rule_requirement_semantics_preserved,
    "open_questions_propagated": _rule_open_questions_propagated,
    "coverage_claim_matches_evidence": _rule_coverage_claim_matches_evidence,
    "architecture_lists_impacted_systems": _rule_architecture_lists_impacted_systems,
    "architecture_lists_constraints": _rule_architecture_lists_constraints,
    "architecture_lists_risks": _rule_architecture_lists_risks,
    "readiness_has_decision": _rule_readiness_has_decision,
    "contract_has_schema_definitions": _rule_contract_has_schema_definitions,
    "nfr_assessment_has_ids": _rule_nfr_assessment_has_ids,
    "nfr_assessment_covers_core_domains": _rule_nfr_assessment_covers_core_domains,
    "nfr_assessment_has_decision": _rule_nfr_assessment_has_decision,
    "selected_epics_have_implementation_contracts": _rule_selected_epics_have_implementation_contracts,
    "selected_epics_have_coding_handoffs": _rule_selected_epics_have_coding_handoffs,
}


def _run_named_validation_rules(
    action: dict[str, Any],
    path: Path,
    workspace_root: Path,
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> list[dict[str, str]]:
    rules = action.get("validation_rules") or {}
    results: list[dict[str, str]] = []

    for severity in ("required", "optional"):
        for rule_name in list(rules.get(severity, []) or []):
            validator = NAMED_RULES.get(rule_name)
            if validator is None:
                results.append(
                    _named_rule_result(
                        rule_name,
                        artifact_path,
                        False,
                        f"unknown named validation rule: {rule_name}",
                        severity=severity,
                    )
                )
                continue

            result = validator(path, workspace_root, action, artifact_path, base_checks)
            result["severity"] = severity
            results.append(result)

    return results


def _validate_epic_folders_directory(path: Path, workspace_root: Path) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []
    checks.extend(_non_empty_directory(path))

    state = workspace.load_state(workspace_root)
    current_item = state.get("current_item")

    epic_dirs = sorted([d for d in path.iterdir() if d.is_dir() and d.name.startswith("E-")])
    flat_files = sorted([f for f in path.iterdir() if f.is_file() and f.name.startswith("E-")])

    if current_item:
        epic_dirs = [d for d in epic_dirs if d.name.startswith(current_item)]
        if not epic_dirs:
            checks.append(
                _result(
                    "current_item_folder_exists",
                    path.name,
                    False,
                    f"no folder found for current_item '{current_item}' — expected epics/{current_item}-<slug>/",
                )
            )
            return checks

    if flat_files and not epic_dirs:
        checks.append(
            _result(
                "has_epic_subdirectories",
                path.name,
                False,
                f"epics/ contains flat files ({[f.name for f in flat_files[:5]]}) instead of E-NNN subdirectories — "
                f"each epic must be a folder (epics/E-001-<slug>/) containing epic.md and stories/",
            )
        )
        return checks

    checks.append(
        _result(
            "has_epic_subdirectories",
            path.name,
            bool(epic_dirs),
            f"epics/ contains {len(epic_dirs)} epic subdirectories" if epic_dirs
            else "epics/ has no E-NNN subdirectories",
        )
    )

    for epic_dir in epic_dirs:
        label = epic_dir.name

        epic_md = epic_dir / "epic.md"
        checks.append(
            _result(
                "epic_has_overview",
                label,
                epic_md.exists(),
                f"{label}/epic.md present" if epic_md.exists()
                else f"{label}/epic.md missing — every epic folder must contain epic.md",
            )
        )

        contract = epic_dir / "implementation-contract.md"
        checks.append(
            _result(
                "epic_has_contract",
                label,
                contract.exists(),
                f"{label}/implementation-contract.md present" if contract.exists()
                else f"{label}/implementation-contract.md missing — every epic folder must contain an implementation contract",
            )
        )

        if contract.exists():
            ct = _read_text(contract)
            ct_lines = len([l for l in ct.splitlines() if l.strip()])
            checks.append(
                _result(
                    "contract_has_depth",
                    label,
                    ct_lines >= 15,
                    f"{label}/implementation-contract.md: {ct_lines} lines of content" if ct_lines >= 15
                    else f"{label}/implementation-contract.md: only {ct_lines} lines — contract must include relevant data/API/event/rules sections",
                )
            )

            has_data = "## Data Entities" in ct
            has_api = "## API Surface" in ct
            has_events = "## Events" in ct
            has_any_section = has_data or has_api or has_events or "## Business Rules" in ct
            checks.append(
                _result(
                    "contract_has_sections",
                    label,
                    has_any_section,
                    f"{label}/implementation-contract.md: has implementation sections (data={has_data}, api={has_api}, events={has_events})"
                    if has_any_section
                    else f"{label}/implementation-contract.md: no relevant sections found — must include at least one of: Data Entities, API Surface, Events, Business Rules",
                )
            )

            if has_data:
                has_er = "```mermaid" in ct and "erDiagram" in ct
                checks.append(
                    _result(
                        "contract_data_has_er_diagram",
                        label,
                        has_er,
                        f"{label}: Data Entities section has Mermaid ER diagram" if has_er
                        else f"{label}: Data Entities section missing erDiagram — must include Mermaid ER diagram when data entities are defined",
                    )
                )

            if has_api:
                has_openapi = "```yaml" in ct and "openapi" in ct
                checks.append(
                    _result(
                        "contract_api_has_openapi",
                        label,
                        has_openapi,
                        f"{label}: API Surface section has OpenAPI YAML spec" if has_openapi
                        else f"{label}: API Surface section missing OpenAPI YAML — must include ```yaml openapi spec when APIs are defined",
                    )
                )

        coding_handoff = epic_dir / "coding-handoff.md"
        if coding_handoff.exists():
            handoff_text = _read_text(coding_handoff)
            handoff_lines = len([line for line in handoff_text.splitlines() if line.strip()])
            checks.append(
                _result(
                    "coding_handoff_has_depth",
                    label,
                    handoff_lines >= 12,
                    f"{label}/coding-handoff.md has {handoff_lines} lines of content" if handoff_lines >= 12
                    else f"{label}/coding-handoff.md is too shallow - expected implementation-ready detail",
                )
            )

        epic_id = re.match(r"(E-\d{3})", label)
        epic_id_str = epic_id.group(1) if epic_id else None
        skeleton_path = workspace_root / "planning" / "delivery-skeleton.md"
        if epic_id_str and skeleton_path.exists():
            skeleton_text = _read_text(skeleton_path)
            coverage_section = _section_block(skeleton_text, "## Requirement Coverage")
            epic_reqs: set[str] = set()
            for row_match in re.finditer(
                rf"^\|\s*((?:FR|REQ|NFR)-\d{{3}})\s*\|.*?\|\s*{re.escape(epic_id_str)}\s*\|",
                coverage_section,
                flags=re.MULTILINE,
            ):
                epic_reqs.add(row_match.group(1))

            if epic_reqs:
                story_reqs: set[str] = set()
                for story_file in sorted((epic_dir / "stories").glob("S-*.md")) if (epic_dir / "stories").exists() else []:
                    if story_file.name.endswith(".prompt.md"):
                        continue
                    story_text = _read_text(story_file)
                    story_reqs.update(re.findall(r"(?:FR|REQ|NFR)-\d{3}", story_text))

                missing_reqs = epic_reqs - story_reqs
                checks.append(
                    _result(
                        "epic_stories_cover_requirements",
                        label,
                        len(missing_reqs) == 0,
                        f"{label}: stories cover all {len(epic_reqs)} requirements from skeleton"
                        if len(missing_reqs) == 0
                        else f"{label}: stories missing {len(missing_reqs)} requirements from skeleton: {sorted(missing_reqs)[:10]}",
                    )
                )

        stories_dir = epic_dir / "stories"
        checks.append(
            _result(
                "epic_has_stories_dir",
                label,
                stories_dir.exists() and stories_dir.is_dir(),
                f"{label}/stories/ directory present" if stories_dir.exists()
                else f"{label}/stories/ directory missing — each epic must have a stories/ subfolder",
            )
        )

        if stories_dir.exists() and stories_dir.is_dir():
            story_files = sorted([f for f in stories_dir.glob("S-*.md") if not f.name.endswith(".prompt.md")])

            checks.append(
                _result(
                    "epic_has_story_files",
                    label,
                    bool(story_files),
                    f"{label}/stories/ has {len(story_files)} story file(s)" if story_files
                    else f"{label}/stories/ has no S-NNN.N-*.md story files",
                )
            )

            for story_file in story_files:
                text = _read_text(story_file)
                slabel = f"{label}/{story_file.name}"

                has_gherkin = "```gherkin" in text
                checks.append(
                    _result(
                        "story_has_gherkin_ac",
                        slabel,
                        has_gherkin,
                        f"{story_file.name}: has Gherkin AC" if has_gherkin
                        else f"{story_file.name}: no ```gherkin block — AC must use Given/When/Then",
                    )
                )

                gherkin_blocks = re.findall(r"```gherkin(.*?)```", text, re.DOTALL)
                scenario_count = sum(
                    len(re.findall(r"^\s*Scenario:", block, re.MULTILINE))
                    for block in gherkin_blocks
                )

                # Determine minimum scenarios based on story complexity
                story_layers_match = re.search(r"\|\s*Layers?\s*\|\s*([^|]+)\|", text, re.IGNORECASE)
                story_layer_count = 0
                if story_layers_match:
                    story_layer_count = len([
                        l.strip() for l in re.split(r"[,/]", story_layers_match.group(1))
                        if l.strip().lower() not in ("", "draft", "must", "should", "could")
                    ])
                story_req_count = len(set(re.findall(
                    r"(?<![A-Za-z])(?:FR|REQ|NFR|C)-\d{3}", text
                )))
                has_integration = bool(re.search(r"(?i)integrat|external|adapter|circuit.breaker|timeout|fallback", text))
                has_state_machine = bool(re.search(r"(?i)state.?machine|stateDiagram|status.*transition|→|->.*status", text))

                if has_integration or has_state_machine:
                    min_scenarios = 4
                    complexity = "integration/state"
                elif story_layer_count >= 2 or story_req_count >= 2:
                    min_scenarios = 3
                    complexity = "multi-layer/multi-req"
                else:
                    min_scenarios = 3
                    complexity = "standard"

                checks.append(
                    _result(
                        "story_has_minimum_ac",
                        slabel,
                        scenario_count >= min_scenarios,
                        f"{story_file.name}: {scenario_count} Gherkin scenarios (minimum {min_scenarios} for {complexity})"
                        if scenario_count >= min_scenarios
                        else f"{story_file.name}: only {scenario_count} Gherkin scenario(s) — need at least {min_scenarios} for {complexity} story (happy path + negative + boundary/auth/integration)",
                    )
                )

                has_criticality = bool(re.search(r"\[critical\]|\[important\]|\[standard\]", text))
                has_automation = bool(re.search(r"\[automate\]|\[manual\]|\[automate-later\]", text))
                if scenario_count >= 2 and not (has_criticality and has_automation):
                    missing_tags = []
                    if not has_criticality:
                        missing_tags.append("criticality ([critical]/[important]/[standard])")
                    if not has_automation:
                        missing_tags.append("automation ([automate]/[manual]/[automate-later])")
                    checks.append(
                        _result(
                            "story_ac_has_tags",
                            slabel,
                            False,
                            f"{story_file.name}: AC missing tags: {', '.join(missing_tags)}",
                        )
                    )

            all_story_layers: set[str] = set()
            for story_file in story_files:
                stext = _read_text(story_file)
                slbl = f"{label}/{story_file.name}"

                layers_match = re.search(r"\|\s*Layers?\s*\|\s*([^|]+)\|", stext, re.IGNORECASE)
                if layers_match:
                    layer_text = layers_match.group(1).strip()
                    for layer in re.split(r"[,/]", layer_text):
                        normalized = layer.strip().lower()
                        if normalized and normalized not in ("draft", "must", "should", "could"):
                            all_story_layers.add(normalized)
                checks.append(
                    _result(
                        "story_has_layers",
                        slbl,
                        bool(layers_match) and len(layers_match.group(1).strip()) > 2,
                        f"{story_file.name}: layers declared" if layers_match and len(layers_match.group(1).strip()) > 2
                        else f"{story_file.name}: missing Layers field in metadata — must declare which layers (Frontend/Backend/Infrastructure/Integration) this story touches",
                    )
                )

                story_req_ids = set(re.findall(r"(?:FR|REQ|NFR)-\d{3}", stext))
                if len(story_req_ids) > 5:
                    checks.append(
                        _result(
                            "story_invest_small",
                            slbl,
                            False,
                            f"{story_file.name}: covers {len(story_req_ids)} requirements — likely too large (INVEST: Small). Consider splitting.",
                        )
                    )

                if layers_match:
                    layer_list = [l.strip().lower() for l in re.split(r"[,/]", layers_match.group(1)) if l.strip().lower() not in ("draft", "must", "should", "could", "")]
                    if len(layer_list) > 3:
                        checks.append(
                            _result(
                                "story_slicing_layers",
                                slbl,
                                False,
                                f"{story_file.name}: touches {len(layer_list)} layers ({', '.join(layer_list)}) — consider splitting to 1-2 layers per story",
                            )
                        )

                actor_match = re.search(r"\|\s*Actor\s*\|\s*([^|]+)\|", stext, re.IGNORECASE)
                if actor_match:
                    actor_text = actor_match.group(1).strip()
                    actor_count = len([a for a in re.split(r"[,/]", actor_text) if a.strip() and a.strip().lower() not in ("system",)])
                    if actor_count > 2:
                        checks.append(
                            _result(
                                "story_slicing_actors",
                                slbl,
                                False,
                                f"{story_file.name}: has {actor_count} actors — a story should focus on one actor goal. Consider splitting.",
                            )
                        )

                has_business_context = bool(re.search(r"(?i)##\s*business context", stext))
                checks.append(
                    _result(
                        "story_invest_valuable",
                        slbl,
                        has_business_context,
                        f"{story_file.name}: has Business Context section (INVEST: Valuable)" if has_business_context
                        else f"{story_file.name}: missing '## Business Context' section (INVEST: Valuable) — story must explain WHY it matters",
                    )
                )

                has_user_story = bool(re.search(r"(?i)##\s*user story", stext))
                user_story_text = ""
                if has_user_story:
                    user_story_text = _section_block(stext, "## User Story")
                checks.append(
                    _result(
                        "story_has_user_story",
                        slbl,
                        has_user_story and len(user_story_text.strip()) >= 20,
                        f"{story_file.name}: has User Story section with description" if has_user_story and len(user_story_text.strip()) >= 20
                        else f"{story_file.name}: missing or too brief '## User Story' section — must include 'As a... I want... so that...' with meaningful detail",
                    )
                )

            for story_file in story_files:
                stext2 = _read_text(story_file)
                slbl2 = f"{label}/{story_file.name}"

                has_impl_guidance = bool(re.search(r"(?i)##\s*implementation guidance", stext2))
                checks.append(
                    _result(
                        "story_has_implementation_guidance",
                        slbl2,
                        has_impl_guidance,
                        f"{story_file.name}: has Implementation Guidance section" if has_impl_guidance
                        else f"{story_file.name}: missing '## Implementation Guidance' — must reference the implementation contract",
                    )
                )

                has_test_table = bool(re.search(r"(?i)##\s*test expectations", stext2))
                checks.append(
                    _result(
                        "story_has_test_expectations",
                        slbl2,
                        has_test_table,
                        f"{story_file.name}: has Test Expectations section" if has_test_table
                        else f"{story_file.name}: missing '## Test Expectations' — must specify which test types to write",
                    )
                )

    skeleton_path = workspace_root / "planning" / "delivery-skeleton.md"
    if skeleton_path.exists():
        skel_text = _read_text(skeleton_path)
        declared_layers: set[str] = set()
        layers_section = _section_block(skel_text, "## Application Layers")
        for layer_name in ("frontend", "backend", "infrastructure", "integration"):
            if re.search(rf"(?i)\|\s*{layer_name}.*?\|\s*yes\s*\|", layers_section):
                declared_layers.add(layer_name)

        if declared_layers:
            all_epic_layers: set[str] = set()
            for epic_dir in epic_dirs:
                stories_path = epic_dir / "stories"
                if stories_path.exists():
                    for sf in stories_path.glob("S-*.md"):
                        if not sf.name.startswith("S-") or sf.name.endswith(".prompt.md"):
                            continue
                        st = _read_text(sf)
                        lm = re.search(r"\|\s*Layers?\s*\|\s*([^|]+)\|", st, re.IGNORECASE)
                        if lm:
                            for part in re.split(r"[,/]", lm.group(1)):
                                all_epic_layers.add(part.strip().lower())

            missing_layers = declared_layers - all_epic_layers
            checks.append(
                _result(
                    "layers_coverage",
                    path.name,
                    len(missing_layers) == 0,
                    f"all declared layers covered by stories ({sorted(declared_layers)})"
                    if len(missing_layers) == 0
                    else f"declared layers not covered by any story: {sorted(missing_layers)} — skeleton declares these layers but no story touches them",
                )
            )

    return checks


VALIDATORS_BY_ARTIFACT = {
    "routing/routing-decision.md": _validate_routing_decision,
    "business-intake/business-intake-summary.md": _validate_business_intake_summary,
    "business-analysis/requirements.md": _validate_requirements_catalog,
    "requirements/atomic-requirements.md": _validate_atomic_requirements,
    "planning/delivery-skeleton.md": _validate_delivery_skeleton,
    "planning/fr-coverage.md": _validate_fr_coverage_report,
    "business-analysis/use-cases.md": _validate_use_cases_markdown,
    "business-analysis/use-cases.puml": _validate_use_cases_puml,
    "business-analysis/entity-model.md": _validate_entity_model,
    "business-analysis/use-cases/": _validate_use_case_specs_directory,
    "engineering-readiness/readiness-check.md": _validate_readiness_check,
    "quality-gates/bdd/": _validate_bdd_directory,
    "specs/": _validate_story_package_directory,
    "technical-specifications/api/exposed/": _validate_exposed_api_spec_directory,
    "technical-specifications/api/consumed/": _validate_consumed_api_spec_directory,
    "technical-specifications/integrations/": _validate_integration_spec_directory,
    "standalone-delivery/": _validate_standalone_directory,
    "review-package/": _validate_review_package,
    "epics/": _validate_epic_folders_directory,
}

PROFILE_VALIDATORS: dict[str, ProfileValidator] = {
    "basic-file": _validate_profile_basic_file,
    "structured-document": _validate_profile_structured_document,
    "catalog": _validate_profile_catalog,
    "analytical-review": _validate_profile_analytical_review,
    "artifact-package": _validate_profile_artifact_package,
}


def _validate_disallowed_fallback(
    path: Path,
    action: dict[str, Any],
    artifact_path: str,
) -> list[dict[str, str]]:
    criticality = _artifact_criticality(action)
    return [
        _profile_dispatch_check(
            path,
            dispatch="configuration-fail",
            detail=f"no validation profile or dedicated validator for {artifact_path} (criticality: {criticality})",
            passed=False,
        )
    ]


def _artifact_template_ref(action: dict[str, Any]) -> str:
    return str(action.get("artifact_template_ref") or "")


def _is_human_gated(action: dict[str, Any]) -> bool:
    return bool((action.get("human_gate") or {}).get("required"))


def _artifact_paths_for(action: dict[str, Any]) -> list[str]:
    return workspace.action_output_paths(action)


def _downstream_consumer_count(
    artifact_path: str,
    actions_by_id: dict[str, dict[str, Any]],
    *,
    source_action_id: str,
) -> int:
    count = 0
    for action_id, action in actions_by_id.items():
        if action_id == source_action_id:
            continue
        inputs = action.get("inputs", {})
        patterns = list(inputs.get("required", [])) + list(inputs.get("optional", []))
        if artifact_path in patterns:
            count += 1
    return count


def _looks_analytical_artifact(action: dict[str, Any], artifact_path: str) -> bool:
    joined = " ".join(
        [
            artifact_path,
            str(action.get("action_id") or ""),
            str(action.get("title") or ""),
            _artifact_template_ref(action),
        ]
    ).lower()
    tokens = [
        "review",
        "readiness",
        "strategy",
        "observability",
        "contract",
        "architecture",
        "threat",
        "security",
    ]
    return any(token in joined for token in tokens)


STRUCTURAL_CONTRACT_REQUIRED_ACTIONS = {
    "review-initial-architecture",
    "create-architecture-rules",
    "create-delivery-structure",
    "create-traceability-matrix",
    "check-engineering-readiness",
    "generate-initiative-context",
    "create-security-review",
    "create-test-strategy",
    "create-api-contract",
    "create-data-contract",
    "create-event-contract",
    "create-observability-plan",
}


def _audit_validation_coverage(
    action: dict[str, Any],
    actions_by_id: dict[str, dict[str, Any]],
    artifact_path: str,
    dispatch: str,
) -> list[dict[str, str]]:
    checks = []
    profile = _normalized_profile_name(action)
    criticality = _artifact_criticality(action)
    downstream_consumers = _downstream_consumer_count(
        artifact_path,
        actions_by_id,
        source_action_id=action["action_id"],
    )
    analytical_hint = _looks_analytical_artifact(action, artifact_path)

    findings: list[str] = []

    if _is_human_gated(action) and profile == "basic-file":
        findings.append("human-gated artifact uses basic-file validation")

    if criticality in {"high", "critical"} and not profile and dispatch not in {"dedicated", "template"}:
        findings.append(f"{criticality}-criticality artifact lacks explicit validation profile")

    if downstream_consumers >= 3 and dispatch == "fallback":
        findings.append(
            f"artifact is consumed by {downstream_consumers} downstream actions but resolves to fallback validation"
        )

    if downstream_consumers >= 3 and profile == "basic-file" and dispatch not in {"dedicated", "template"}:
        findings.append(
            f"artifact is consumed by {downstream_consumers} downstream actions but only uses basic-file validation"
        )

    if analytical_hint and dispatch == "fallback":
        findings.append("analytical or authority artifact is treated as generic non-empty validation")

    if (
        dispatch == "profile"
        and action["action_id"] in STRUCTURAL_CONTRACT_REQUIRED_ACTIONS
        and criticality in {"high", "critical"}
        and profile in {"structured-document", "catalog", "analytical-review"}
    ):
        if not _required_sections(action) and not _artifact_template_ref(action):
            findings.append(
                f"{criticality}-criticality {profile} artifact lacks required_sections structural contract"
            )

    if findings:
        for finding in findings:
            checks.append(
                _result(
                    "validation_audit",
                    artifact_path,
                    False,
                    finding,
                )
            )
        return checks

    checks.append(
        _result(
            "validation_audit",
            artifact_path,
            True,
            f"validation coverage is acceptable (dispatch={dispatch}, downstream_consumers={downstream_consumers})",
        )
    )
    return checks


def _validator_for_artifact(
    action: dict[str, Any],
    artifact_path: str,
    path: Path,
) -> tuple[str, Callable[..., list[dict[str, str]]]]:
    if artifact_path in VALIDATORS_BY_ARTIFACT:
        return "dedicated", VALIDATORS_BY_ARTIFACT[artifact_path]

    if not path.is_dir() and _artifact_template_ref(action):
        return "template", _validate_from_template

    profile = _normalized_profile_name(action)
    if profile:
        validator = PROFILE_VALIDATORS.get(profile)
        if validator is None:
            return "configuration-fail", _validate_disallowed_fallback
        return "profile", validator

    if _artifact_criticality(action) in {"high", "critical"}:
        return "configuration-fail", _validate_disallowed_fallback

    if path.is_dir():
        return "fallback", _validate_directory_default
    return "fallback", _validate_file_default


def run(args: object) -> None:
    workspace_root = workspace.resolve_workspace_root(args.workspace_root)
    state = workspace.load_state(workspace_root)
    action_id = workspace.read_action_id_from_state_or_args(state, getattr(args, "action_id", None))
    _, actions_by_id = workspace.load_stage_actions(workspace_root)
    action = actions_by_id[action_id]

    checks = []
    failures = []
    advisories = []
    named_rule_results = []
    artifact_paths = workspace.action_output_paths(action)

    for artifact_path in artifact_paths:
        path = workspace_root / artifact_path
        exists = workspace.artifact_exists(workspace_root, artifact_path)
        check = {
            "name": "file_exists",
            "target": artifact_path,
            "result": "pass" if exists else "fail",
            "detail": "artifact exists" if exists else "artifact missing",
        }
        checks.append(check)
        if not exists:
            failures.append(f"Missing artifact: {artifact_path}")
            continue

        dispatch, validator = _validator_for_artifact(action, artifact_path, path)
        if dispatch in ("profile", "template"):
            validator_checks = validator(path, workspace_root, action, artifact_path)
        elif dispatch == "configuration-fail":
            validator_checks = validator(path, action, artifact_path)
        else:
            validator_checks = validator(path, workspace_root)
        validator_checks = [_profile_dispatch_check(path, dispatch=dispatch, detail=artifact_path, passed=dispatch != "configuration-fail")] + validator_checks
        validator_checks.extend(_audit_validation_coverage(action, actions_by_id, artifact_path, dispatch))
        checks.extend(validator_checks)
        for validator_check in validator_checks:
            if validator_check["result"] == "fail":
                failures.append(
                    f"{artifact_path}: {validator_check['name']} failed - {validator_check['detail']}"
                )

        rule_checks = _run_named_validation_rules(action, path, workspace_root, artifact_path, validator_checks)
        checks.extend(rule_checks)
        named_rule_results.extend(rule_checks)
        for rule_check in rule_checks:
            if rule_check["result"] != "fail":
                continue
            if rule_check.get("severity") == "required":
                failures.append(
                    f"{artifact_path}: {rule_check['rule_name']} failed - {rule_check['detail']}"
                )
            else:
                advisories.append(
                    f"{artifact_path}: {rule_check['rule_name']} advisory - {rule_check['detail']}"
                )

    result = {
        "overall": "pass" if not failures else "fail",
        "action_id": action_id,
        "artifact_path": artifact_paths[0] if artifact_paths else None,
        "checks": checks,
        "named_rule_results": named_rule_results,
        "failures": failures,
        "advisories": advisories,
    }
    workspace.save_yaml_file(
        workspace.resolve_output_path("validate-artifact", workspace_root, args.output),
        result,
    )
    workspace.append_execution_log(
        workspace_root,
        command="validate-artifact",
        overall=result["overall"],
        action_id=action_id,
        details={
            "artifact_path": result["artifact_path"],
            "failure_count": len(failures),
        },
    )
