"""Validation helpers for staged `.b2s` artifacts."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Callable
import yaml

from b2s_engine import workspace


Validator = Callable[[Path, Path], list[dict[str, str]]]
ProfileValidator = Callable[[Path, Path, dict[str, Any], str], list[dict[str, str]]]
NamedRuleValidator = Callable[[Path, Path, dict[str, Any], str, list[dict[str, str]]], dict[str, str]]


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _read_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


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


_STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
    "has", "have", "if", "in", "is", "it", "of", "on", "or", "so",
    "that", "the", "their", "then", "there", "this", "to", "when",
    "with", "within", "shall", "should", "must", "can", "will",
    "system", "user", "users",
}


def _key_phrases(value: str) -> set[str]:
    """Extract bigrams and trigrams from normalized text."""
    tokens = _normalize_text(value).split()
    phrases: set[str] = set()
    for n in (2, 3):
        for i in range(len(tokens) - n + 1):
            gram = tokens[i : i + n]
            if all(t in _STOPWORDS or len(t) < 3 for t in gram):
                continue
            phrases.add(" ".join(gram))
    return phrases


def _semantic_overlap_score(
    req: dict[str, Any],
    story_text: str,
) -> tuple[float, list[str]]:
    """Score semantic overlap between a requirement and a story.

    Returns (score 0.0–1.0, list of matching details).
    """
    signature = " ".join(
        part for part in [
            req.get("title", ""),
            req.get("actor", ""),
            req.get("business_object", ""),
            req.get("trigger", ""),
            req.get("expected_outcome", ""),
            req.get("text", ""),
        ] if part
    )
    details: list[str] = []

    req_kw = _keywords(signature)
    story_kw = _keywords(story_text)
    kw_overlap = req_kw & story_kw
    kw_ratio = len(kw_overlap) / max(len(req_kw), 1)

    req_phrases = _key_phrases(signature)
    story_phrases = _key_phrases(story_text)
    phrase_overlap = req_phrases & story_phrases
    phrase_ratio = len(phrase_overlap) / max(len(req_phrases), 1)

    actor = req.get("actor", "").strip()
    actor_score = 0.0
    if actor and actor.lower() not in ("system", "user", "users", "", "—"):
        actor_tokens = _keywords(actor)
        if actor_tokens and actor_tokens & story_kw:
            actor_score = 1.0
            details.append(f"actor '{actor}' found")
    else:
        actor_score = 1.0

    outcome = req.get("expected_outcome", "").strip()
    outcome_score = 0.0
    if outcome and outcome not in ("", "—"):
        outcome_kw = _keywords(outcome)
        if outcome_kw:
            outcome_overlap = outcome_kw & story_kw
            outcome_score = len(outcome_overlap) / max(len(outcome_kw), 1)
            if outcome_overlap:
                details.append(f"outcome keywords matched: {outcome_overlap}")
    else:
        outcome_score = 1.0

    score = (kw_ratio * 0.3) + (phrase_ratio * 0.4) + (actor_score * 0.15) + (outcome_score * 0.15)

    if kw_overlap:
        details.append(f"keyword overlap: {len(kw_overlap)}/{len(req_kw)}")
    if phrase_overlap:
        details.append(f"phrase overlap: {len(phrase_overlap)}/{len(req_phrases)}")

    return score, details


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

    _COMPACT_META_RE = re.compile(
        r"^\*\*Source:\*\*\s*(.+?)\s*\|\s*\*\*Actor:\*\*\s*(.+?)\s*\|\s*\*\*Deps:\*\*\s*(.+?)\s*$",
        flags=re.MULTILINE,
    )
    _COMPACT_AMBIGUITY_RE = re.compile(
        r"^>\s*\*\*Ambiguities?:\*\*\s*(.+)$", flags=re.MULTILINE,
    )
    _COMPACT_BLOCKING_RE = re.compile(
        r"^>\s*\*\*Blocking:\*\*\s*(.+)$", flags=re.MULTILINE,
    )

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

        # Try verbose format first (| Field | Value | tables)
        requirement_text_match = re.search(
            r"####\s+Requirement Text\s*(.*?)(?=^####\s+|\Z)",
            block,
            flags=re.MULTILINE | re.DOTALL,
        )
        requirement_text = requirement_text_match.group(1).strip() if requirement_text_match else ""

        actor = _field("Actor")
        blocking_questions = _field("Blocking Questions")
        ambiguities = _field("Ambiguities")

        # If no verbose fields found, try compact format
        if not actor:
            compact_meta = _COMPACT_META_RE.search(block)
            if compact_meta:
                actor = compact_meta.group(2).strip()

            compact_amb = _COMPACT_AMBIGUITY_RE.search(block)
            if compact_amb:
                ambiguities = compact_amb.group(1).strip()

            compact_blk = _COMPACT_BLOCKING_RE.search(block)
            if compact_blk:
                blocking_questions = compact_blk.group(1).strip()

            # In compact format the EARS text is the block body (excluding metadata and blockquotes)
            if not requirement_text:
                body_lines = []
                for line in block.splitlines():
                    stripped = line.strip()
                    if not stripped:
                        continue
                    if stripped.startswith("|") or stripped.startswith(">") or stripped.startswith("**Source:**"):
                        continue
                    if stripped == "---":
                        continue
                    if stripped.startswith("####"):
                        continue
                    body_lines.append(stripped)
                requirement_text = "\n".join(body_lines)

        signature_source = " ".join(
            part for part in [
                title,
                actor,
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
            "actor": actor,
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


def _source_brs_ids(workspace_root: Path) -> dict[str, set[str]]:
    text = _source_text(workspace_root)
    return {
        "objectives": set(re.findall(r"(?<![A-Za-z])OBJ-\d{3}", text)),
        "functional": set(re.findall(r"(?<![A-Za-z])FR-\d{3}", text)),
        "non_functional": set(re.findall(r"(?<![A-Za-z])NFR-\d{3}", text)),
    }


def _catalog_heading_ids(text: str) -> set[str]:
    return set(re.findall(r"^###\s+((?:OBJ|FR|REQ|NFR|C)-\d{3})\b", text, flags=re.MULTILINE))


def _catalog_entry_blocks(text: str) -> list[tuple[str, str, str]]:
    pattern = re.compile(
        r"^###\s+((?:OBJ|FR|REQ|NFR|C)-\d{3})\s+[â€”-]\s+(.+?)\n(.*?)(?=^###\s+(?:OBJ|FR|REQ|NFR|C)-\d{3}\s+[â€”-]\s+|\Z)",
        flags=re.MULTILINE | re.DOTALL,
    )
    return [
        (match.group(1).strip(), match.group(2).strip(), match.group(3))
        for match in pattern.finditer(text)
    ]


def _canonical_requirement_derivations(workspace_root: Path) -> dict[str, str]:
    req_path = workspace_root / "requirements" / "atomic-requirements.md"
    if not req_path.exists():
        return {}

    text = _read_text(req_path)
    derivations: dict[str, str] = {}
    for req_id, _title, block in _catalog_entry_blocks(text):
        match = re.search(r"^>\s*\*\*Derivation:\*\*\s*(.+)$", block, flags=re.MULTILINE)
        if not match:
            continue
        derivation = match.group(1).strip()
        derivations[req_id] = "inferred" if re.search(r"(?i)\binferred\b", derivation) else "direct"
    return derivations


def _catalog_entries_by_type(text: str) -> dict[str, list[str]]:
    """Parse catalogue entries and classify by their ``| Type | ... |`` field.

    Returns a dict mapping lowercase type labels (``"functional"``,
    ``"non-functional"``, ``"objective"``, ``"constraint"``) to lists of
    heading IDs.  When a catalogue entry uses a ``REQ-NNN`` heading but
    declares ``| Type | Functional |``, it is counted as functional.
    Falls back to prefix-based classification when no Type field is found.
    """
    result: dict[str, list[str]] = {
        "functional": [],
        "non-functional": [],
        "objective": [],
        "constraint": [],
    }
    heading_pattern = re.compile(
        r"^###\s+((?:OBJ|FR|REQ|NFR|C)-\d{3})\b", re.MULTILINE,
    )
    type_field_pattern = re.compile(
        r"^\|\s*Type\s*\|\s*(.+?)\s*\|$", re.MULTILINE,
    )
    matches = list(heading_pattern.finditer(text))
    for i, m in enumerate(matches):
        heading_id = m.group(1)
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[start:end]

        type_match = type_field_pattern.search(block)
        if type_match:
            type_label = type_match.group(1).strip().lower()
            if type_label in ("functional",):
                result["functional"].append(heading_id)
            elif type_label in ("non-functional", "non_functional", "nonfunctional"):
                result["non-functional"].append(heading_id)
            elif type_label in ("objective", "business objective"):
                result["objective"].append(heading_id)
            elif type_label in ("constraint",):
                result["constraint"].append(heading_id)
            else:
                result.setdefault(type_label, []).append(heading_id)
        else:
            if heading_id.startswith("FR-"):
                result["functional"].append(heading_id)
            elif heading_id.startswith("NFR-"):
                result["non-functional"].append(heading_id)
            elif heading_id.startswith("OBJ-"):
                result["objective"].append(heading_id)
            elif heading_id.startswith("C-"):
                result["constraint"].append(heading_id)
            elif heading_id.startswith("REQ-"):
                classified = False
                source_in_title = re.search(r"\(Source:\s*(FR|NFR|OBJ|C)-\d{3}\)", block)
                if source_in_title:
                    prefix = source_in_title.group(1)
                    if prefix == "FR":
                        result["functional"].append(heading_id)
                    elif prefix == "NFR":
                        result["non-functional"].append(heading_id)
                    elif prefix == "OBJ":
                        result["objective"].append(heading_id)
                    elif prefix == "C":
                        result["constraint"].append(heading_id)
                    classified = True
                if not classified:
                    source_line = re.search(
                        r"\*\*Source:\*\*\s*([^|]+)",
                        block,
                    )
                    if source_line:
                        source_val = source_line.group(1)
                        source_prefix = re.search(r"(FR|NFR|OBJ|C)-\d{3}", source_val)
                        if source_prefix:
                            prefix = source_prefix.group(1)
                            if prefix == "FR":
                                result["functional"].append(heading_id)
                            elif prefix == "NFR":
                                result["non-functional"].append(heading_id)
                            elif prefix == "OBJ":
                                result["objective"].append(heading_id)
                            elif prefix == "C":
                                result["constraint"].append(heading_id)
                            classified = True
                if not classified:
                    result["functional"].append(heading_id)

    return result


def _summary_metric_value(text: str, label: str) -> int | None:
    match = re.search(
        rf"^\|\s*{re.escape(label)}\s*\|\s*(\d+)\s*\|$",
        text,
        flags=re.MULTILINE,
    )
    return int(match.group(1)) if match else None


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


def _extract_story_heading_parts(text: str) -> tuple[str | None, str]:
    heading = next((line.strip() for line in text.splitlines() if line.startswith("# ")), "")
    if not heading:
        return None, ""
    match = re.match(r"^#\s+(S-\d{3}\.\d+)\s+[—-]\s+(.+?)\s*$", heading)
    if match:
        return match.group(1), match.group(2).strip()
    story_id_match = re.search(r"(S-\d{3}\.\d+)", heading)
    return (story_id_match.group(1) if story_id_match else None), ""


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
        if stripped.startswith("-") or stripped.startswith("|"):
            req_ids.extend(re.findall(r"(?<![A-Za-z])(?:FR|REQ|NFR|C)-\d{3}", stripped))
    return list(dict.fromkeys(req_ids))


def _extract_story_dependencies(text: str) -> list[str]:
    dependencies: list[str] = []
    rows = _section_table_rows(text, "## Dependencies")
    for row in rows:
        if not row:
            continue
        dependency_id = row[0].strip()
        if dependency_id.lower() == "dependency":
            continue
        if dependency_id:
            dependencies.append(dependency_id)
    return list(dict.fromkeys(dependencies))


def _extract_story_markdown_operation_refs(text: str) -> set[str]:
    refs: set[str] = set()
    for heading in ("## Implementation Guidance", "## UI Behaviour", "## Dependency Contracts"):
        block = _section_block(text, heading)
        if not block:
            continue
        for method, path in re.findall(r"\b(GET|POST|PUT|PATCH|DELETE)\s+(/[A-Za-z0-9{}._~!$&'()*+,;=:@%/\-]+)", block, flags=re.IGNORECASE):
            refs.add(f"{method.upper()} {_normalize_api_path(path)}")
        for path in re.findall(r"(?<![A-Za-z0-9])(/[A-Za-z0-9{}._~!$&'()*+,;=:@%/\-]+)", block):
            refs.add(_normalize_api_path(path))
    return refs


def _is_non_empty_string_list(value: Any) -> bool:
    return isinstance(value, list) and any(isinstance(item, str) and item.strip() for item in value)


def _validate_story_agent_contract_file(
    agent_contract_path: Path,
    story_file: Path,
    story_text: str,
) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []
    target = f"{story_file.name}/{agent_contract_path.name}"

    try:
        data = _read_yaml(agent_contract_path)
    except Exception as exc:
        return [
            _result(
                "story_agent_contract_yaml_parseable",
                target,
                False,
                f"{agent_contract_path.name}: YAML parse failed - {exc}",
            )
        ]

    checks.append(
        _result(
            "story_agent_contract_yaml_parseable",
            target,
            isinstance(data, dict),
            f"{agent_contract_path.name}: parsed as YAML object"
            if isinstance(data, dict)
            else f"{agent_contract_path.name}: YAML root must be a mapping/object",
        )
    )
    if not isinstance(data, dict):
        return checks

    story_id = data.get("story_id")
    title = data.get("title")
    story_type = data.get("story_type")
    layer = data.get("layer")
    req_implemented = data.get("requirements_implemented")
    req_referenced = data.get("requirements_referenced")
    in_scope = data.get("in_scope")
    out_of_scope = data.get("out_of_scope")
    depends_on = data.get("depends_on")
    implementation_contract = data.get("implementation_contract")
    required_tests = data.get("required_tests")

    story_heading = next((line for line in story_text.splitlines() if line.startswith("# ")), "")
    story_heading_id_match = re.search(r"(S-\d{3}\.\d+)", story_heading)
    story_heading_id = story_heading_id_match.group(1) if story_heading_id_match else None

    checks.append(
        _result(
            "story_agent_contract_has_story_id",
            target,
            isinstance(story_id, str) and story_id.strip() != "",
            f"{agent_contract_path.name}: story_id present ({story_id})"
            if isinstance(story_id, str) and story_id.strip()
            else f"{agent_contract_path.name}: missing non-empty story_id",
        )
    )
    checks.append(
        _result(
            "story_agent_contract_story_id_matches_story",
            target,
            isinstance(story_id, str) and story_heading_id is not None and story_id.strip() == story_heading_id,
            f"{agent_contract_path.name}: story_id matches markdown story heading ({story_heading_id})"
            if isinstance(story_id, str) and story_heading_id is not None and story_id.strip() == story_heading_id
            else f"{agent_contract_path.name}: story_id must match markdown story heading ({story_heading_id or 'missing heading ID'})",
        )
    )
    checks.append(
        _result(
            "story_agent_contract_has_title",
            target,
            isinstance(title, str) and len(title.strip()) >= 5,
            f"{agent_contract_path.name}: title present"
            if isinstance(title, str) and len(title.strip()) >= 5
            else f"{agent_contract_path.name}: missing or too-short title",
        )
    )

    allowed_story_types = {
        "frontend-form",
        "frontend-page",
        "backend-endpoint",
        "event-consumer",
        "schema-migration",
        "generic",
        "spike",
    }
    checks.append(
        _result(
            "story_agent_contract_story_type_valid",
            target,
            isinstance(story_type, str) and story_type in allowed_story_types,
            f"{agent_contract_path.name}: story_type '{story_type}' is valid"
            if isinstance(story_type, str) and story_type in allowed_story_types
            else f"{agent_contract_path.name}: story_type must be one of {sorted(allowed_story_types)}",
        )
    )

    allowed_layers = {"frontend", "backend", "infrastructure", "integration"}
    checks.append(
        _result(
            "story_agent_contract_layer_valid",
            target,
            isinstance(layer, str) and layer in allowed_layers,
            f"{agent_contract_path.name}: layer '{layer}' is valid"
            if isinstance(layer, str) and layer in allowed_layers
            else f"{agent_contract_path.name}: layer must be one of {sorted(allowed_layers)}",
        )
    )

    req_id_pattern = re.compile(r"^(?:FR|REQ|NFR|C)-\d{3}$")
    implemented_ok = isinstance(req_implemented, list) and bool(req_implemented) and all(
        isinstance(item, str) and req_id_pattern.fullmatch(item.strip()) for item in req_implemented
    )
    checks.append(
        _result(
            "story_agent_contract_requirements_implemented_valid",
            target,
            implemented_ok,
            f"{agent_contract_path.name}: requirements_implemented contains valid requirement IDs"
            if implemented_ok
            else f"{agent_contract_path.name}: requirements_implemented must be a non-empty list of canonical requirement IDs",
        )
    )

    referenced_ok = isinstance(req_referenced, list) and all(
        isinstance(item, str) and req_id_pattern.fullmatch(item.strip()) for item in req_referenced
    )
    checks.append(
        _result(
            "story_agent_contract_requirements_referenced_valid",
            target,
            referenced_ok,
            f"{agent_contract_path.name}: requirements_referenced contains valid requirement IDs"
            if referenced_ok
            else f"{agent_contract_path.name}: requirements_referenced must be a list of canonical requirement IDs (or empty list)",
        )
    )

    overlap = set(req_implemented or []) & set(req_referenced or [])
    checks.append(
        _result(
            "story_agent_contract_requirement_sets_disjoint",
            target,
            len(overlap) == 0,
            f"{agent_contract_path.name}: implemented and referenced requirement sets are disjoint"
            if len(overlap) == 0
            else f"{agent_contract_path.name}: requirements appear in both implemented and referenced sets: {sorted(overlap)}",
        )
    )

    checks.append(
        _result(
            "story_agent_contract_in_scope_present",
            target,
            _is_non_empty_string_list(in_scope),
            f"{agent_contract_path.name}: in_scope lists concrete behavior"
            if _is_non_empty_string_list(in_scope)
            else f"{agent_contract_path.name}: in_scope must contain at least one concrete behavior",
        )
    )
    checks.append(
        _result(
            "story_agent_contract_out_of_scope_present",
            target,
            _is_non_empty_string_list(out_of_scope),
            f"{agent_contract_path.name}: out_of_scope lists explicit exclusions"
            if _is_non_empty_string_list(out_of_scope)
            else f"{agent_contract_path.name}: out_of_scope must contain at least one explicit exclusion",
        )
    )

    depends_ok = isinstance(depends_on, list) and all(
        isinstance(dep, dict)
        and isinstance(dep.get("story_id"), str)
        and dep.get("story_id", "").strip()
        and isinstance(dep.get("reason"), str)
        and dep.get("reason", "").strip()
        and (
            not dep.get("consumes_contract")
            or (
                isinstance(dep.get("consumes_contract"), dict)
                and (
                    isinstance(dep["consumes_contract"].get("summary"), str)
                    and dep["consumes_contract"].get("summary", "").strip()
                    or isinstance(dep["consumes_contract"].get("type"), str)
                    and dep["consumes_contract"].get("type", "").strip()
                )
            )
        )
        for dep in depends_on
    )
    checks.append(
        _result(
            "story_agent_contract_dependencies_valid",
            target,
            depends_ok,
            f"{agent_contract_path.name}: depends_on entries are structurally valid"
            if depends_ok
            else f"{agent_contract_path.name}: depends_on must be a list of dependency objects with story_id, reason, and consumed contract summary or type",
        )
    )

    impl_ok = isinstance(implementation_contract, dict)
    checks.append(
        _result(
            "story_agent_contract_has_implementation_contract",
            target,
            impl_ok,
            f"{agent_contract_path.name}: implementation_contract object present"
            if impl_ok
            else f"{agent_contract_path.name}: missing implementation_contract object",
        )
    )
    if impl_ok:
        touched_components_ok = _is_non_empty_string_list(implementation_contract.get("touched_components"))
        operations = implementation_contract.get("operations")
        operations_ok = isinstance(operations, list) and any(
            isinstance(op, dict)
            and isinstance(op.get("type"), str)
            and op.get("type", "").strip()
            and isinstance(op.get("target"), str)
            and op.get("target", "").strip()
            for op in operations
        )
        checks.append(
            _result(
                "story_agent_contract_touched_components_present",
                target,
                touched_components_ok,
                f"{agent_contract_path.name}: touched_components populated"
                if touched_components_ok
                else f"{agent_contract_path.name}: implementation_contract.touched_components must list at least one component",
            )
        )
        checks.append(
            _result(
                "story_agent_contract_operations_present",
                target,
                operations_ok,
                f"{agent_contract_path.name}: implementation_contract.operations populated"
                if operations_ok
                else f"{agent_contract_path.name}: implementation_contract.operations must contain at least one operation with type and target",
            )
        )

    tests_ok = isinstance(required_tests, dict) and any(
        _is_non_empty_string_list(required_tests.get(key))
        for key in ("unit", "integration", "api", "e2e", "accessibility")
    )
    checks.append(
        _result(
            "story_agent_contract_required_tests_present",
            target,
            tests_ok,
            f"{agent_contract_path.name}: required_tests contains concrete obligations"
            if tests_ok
            else f"{agent_contract_path.name}: required_tests must contain at least one non-empty test category",
        )
    )

    if story_type == "frontend-form":
        accessibility_ok = isinstance(required_tests, dict) and _is_non_empty_string_list(required_tests.get("accessibility"))
        checks.append(
            _result(
                "story_agent_contract_frontend_form_accessibility_tests",
                target,
                accessibility_ok,
                f"{agent_contract_path.name}: frontend-form includes accessibility tests"
                if accessibility_ok
                else f"{agent_contract_path.name}: frontend-form stories must declare accessibility test obligations",
            )
        )

    if story_type == "backend-endpoint":
        api_tests_ok = isinstance(required_tests, dict) and _is_non_empty_string_list(required_tests.get("api"))
        checks.append(
            _result(
                "story_agent_contract_backend_endpoint_api_tests",
                target,
                api_tests_ok,
                f"{agent_contract_path.name}: backend-endpoint includes API tests"
                if api_tests_ok
                else f"{agent_contract_path.name}: backend-endpoint stories must declare API contract test obligations",
            )
        )

    return checks


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
    # deferred / missing stubs that indicate no real content was generated
    r"\bDEFERRED\b",
    r"\(missing\s*—\s*fill in\b",
    r"\bawaiting\s+\w+\s+text\b",
    r"\bfill in BRS\b",
    r"Preserved\s*—\s*see\b",
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

    checks.extend(
        _matches(
            path,
            r"\|\s*(?:OBJ|FR|REQ|NFR|C)-\d{3}\s*\|",
            "has_req_rows",
            "requirement catalogue includes typed rows",
        )
    )

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
    else:
        # Narrative BRS sources (architecture docs, PRDs, meeting notes) carry no
        # explicit FR-NNN markers, so source_fr_count is 0 and the checks above
        # never fire. Fall back to a content-agnostic structural proxy — heading
        # count and bullet-list item count — so a thin extraction from a large
        # narrative source still gets flagged instead of passing unchecked.
        source_heading_count = _count_pattern(source, r"^#{2,4}\s+\S")
        source_bullet_count = _count_pattern(source, r"^\s*[-*]\s+\S")
        structural_size = source_heading_count + (source_bullet_count // 4)

        if structural_size >= 15:
            min_expected = max(4, structural_size // 8)
            checks.append(
                _result(
                    "req_count_proportional_to_narrative_source",
                    path.name,
                    artifact_req_count >= min_expected,
                    f"extracted {artifact_req_count} requirements from a narrative BRS with "
                    f"{source_heading_count} headings / {source_bullet_count} bullet items "
                    f"(minimum {min_expected})"
                    if artifact_req_count >= min_expected
                    else f"only {artifact_req_count} requirements extracted from a narrative BRS with "
                         f"{source_heading_count} headings / {source_bullet_count} bullet items — "
                         f"expected at least {min_expected}; likely incomplete extraction. Re-run "
                         f"create-atomic-requirements with attention to every BRS section, not just "
                         f"sections that use FR-/NFR- style labels",
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

    _EARS_KEYWORDS = re.compile(
        r"(?:THE SYSTEM SHALL|WHEN .+?,\s*THE SYSTEM SHALL|WHILE .+?,\s*THE SYSTEM SHALL|"
        r"IF .+?,\s*THEN THE SYSTEM SHALL|WHERE .+?,\s*THE SYSTEM SHALL)",
        flags=re.IGNORECASE,
    )
    ears_count = len(_EARS_KEYWORDS.findall(text))
    if source_fr_count >= 4:
        min_ears = max(2, (source_fr_count * 3) // 4)
        checks.append(
            _result(
                "req_has_ears_content",
                path.name,
                ears_count >= min_ears,
                f"found {ears_count} EARS statements (minimum {min_ears} for {source_fr_count} BRS FRs)"
                if ears_count >= min_ears
                else f"only {ears_count} EARS statements found — expected at least {min_ears} for {source_fr_count} BRS FRs; "
                     f"requirements must contain actual EARS notation, not DEFERRED stubs",
            )
        )
    elif source_fr_count >= 1:
        checks.append(
            _result(
                "req_has_ears_content",
                path.name,
                ears_count >= 1,
                f"found {ears_count} EARS statement(s)"
                if ears_count >= 1
                else "no EARS statements found — requirements must use EARS notation (THE SYSTEM SHALL ...)",
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


def _load_computed_coverage(workspace_root: Path) -> dict | None:
    import json
    computed_path = workspace_root / ".b2s" / "tmp" / "computed-coverage.json"
    if not computed_path.exists():
        return None
    try:
        return json.loads(computed_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def _validate_fr_coverage_report(path: Path, workspace_root: Path) -> list[dict[str, str]]:
    text = _read_text(path)
    checks = []
    checks.extend(_non_empty_file(path))

    # Accept both old single-table and new two-table heading formats
    has_old_summary = "## Coverage Summary" in text
    has_planned = "## Planned Coverage Summary" in text
    has_generated = "## Generated Coverage Summary" in text
    has_matrix = "## Full Coverage Matrix" in text

    if has_planned or has_generated:
        for heading in ["## Planned Coverage Summary", "## Generated Coverage Summary", "## Full Coverage Matrix"]:
            checks.extend(_contains(path, heading, f"has_{heading.strip('# ').lower().replace(' ', '_')}", f"{heading} section present"))
    else:
        for heading in ["## Coverage Summary", "## Full Coverage Matrix"]:
            checks.extend(_contains(path, heading, f"has_{heading.strip('# ').lower().replace(' ', '_')}", f"{heading} section present"))

    computed = _load_computed_coverage(workspace_root)

    if computed:
        summary = computed.get("summary", {})
        engine_total = summary.get("total", 0)
        engine_covered = summary.get("covered", 0)
        engine_pct = summary.get("coverage_pct", 0)
        deferred = summary.get("deferred_wave_count", 0)

        gen = computed.get("generated_coverage", {})
        gen_total = gen.get("total", summary.get("in_scope_total", engine_total))
        gen_covered = gen.get("covered", summary.get("in_scope_covered", engine_covered))
        gen_pct = gen.get("pct", summary.get("in_scope_pct", engine_pct))

        checks.append(
            _result(
                "coverage_percentage_acceptable",
                path.name,
                gen_pct >= 90,
                f"generated coverage is {gen_pct}% ({gen_covered}/{gen_total})"
                + (f"; {deferred} requirements deferred to later waves" if deferred else "")
                + (f"; overall {engine_pct}% ({engine_covered}/{engine_total})" if deferred else "")
                if gen_pct >= 90
                else f"generated coverage is only {gen_pct}% ({gen_covered}/{gen_total}) "
                     f"— expected at least 90%"
                     + (f"; {deferred} requirements deferred to later waves" if deferred else "")
                     + f"; overall {engine_pct}% ({engine_covered}/{engine_total})",
            )
        )

        engine_req_ids = {r["id"] for r in computed.get("canonical_requirements", [])}
        matrix_ids = set(re.findall(r"(?:FR|REQ|NFR|C)-\d{3}", _section_block(text, "## Full Coverage Matrix")))
        if engine_req_ids:
            missing = engine_req_ids - matrix_ids
            checks.append(
                _result(
                    "all_reqs_in_matrix",
                    path.name,
                    len(missing) == 0,
                    f"all {len(engine_req_ids)} canonical requirements appear in coverage matrix"
                    if len(missing) == 0
                    else f"{len(missing)} canonical requirements missing from coverage matrix: {sorted(missing)[:10]}",
                )
            )
    else:
        coverage_match = re.search(r"\|\s*Coverage percentage\s*\|\s*(\d+)%?\s*\|", text)
        if coverage_match:
            pct = int(coverage_match.group(1))
            checks.append(
                _result(
                    "coverage_percentage_acceptable",
                    path.name,
                    pct >= 90,
                    f"coverage percentage is {pct}% (no engine data available for cross-check)"
                    if pct >= 90
                    else f"coverage percentage is only {pct}% — expected at least 90%; "
                         f"likely missing stories for requirements (no engine data available for cross-check)",
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

    # "Deferred" is a legitimate coverage term, not a placeholder stub
    coverage_safe_patterns = [
        p for p in _PLACEHOLDER_PATTERNS if p != r"\bDEFERRED\b"
    ]
    checks.append(
        _result(
            "fr_coverage_no_placeholders",
            path.name,
            not any(re.search(p, text, flags=re.IGNORECASE) for p in coverage_safe_patterns),
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

        has_req_trace = bool(re.search(r"(?:FR|REQ|NFR)-\d{3}", text))
        checks.append(
            _result(
                "uc_has_fr_trace",
                label,
                has_req_trace,
                f"{label}: traces to at least one requirement identifier" if has_req_trace
                else f"{label}: no requirement reference (FR-NNN or REQ-NNN) found — use case must trace to requirements",
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
        has_req_link = bool(re.search(r"(?:FR|REQ|NFR)-\d{3}", text))
        checks.append(_result(
            "story_has_requirements_link", label,
            has_req_link,
            f"{label}/story.md: links to at least one requirement identifier" if has_req_link
            else f"{label}/story.md: no requirement reference (FR-NNN or REQ-NNN) found",
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

    # Check for typed identifiers anywhere in the artifact — catalogue
    # headings, catalogue Type fields, or Source Inventory rows.
    by_type = _catalog_entries_by_type(text)
    has_fr_in_catalog = len(by_type.get("functional", [])) > 0
    has_nfr_in_catalog = len(by_type.get("non-functional", [])) > 0
    has_constraint_in_catalog = len(by_type.get("constraint", [])) > 0

    # Also check for typed IDs in table rows (Source Inventory or inline
    # references) — this is the original check that catches cases where
    # the catalogue uses FR-NNN headings without a Type field.
    has_fr_in_rows = bool(re.search(r"^\|\s*FR-\d{3}\s*\|", text, flags=re.MULTILINE))
    has_nfr_in_rows = bool(re.search(r"^\|\s*NFR-\d{3}\s*\|", text, flags=re.MULTILINE))
    has_constraint_in_rows = bool(re.search(r"^\|\s*C-\d{3}\s*\|", text, flags=re.MULTILINE))

    has_functional = has_fr_in_catalog or has_fr_in_rows
    has_non_functional = has_nfr_in_catalog or has_nfr_in_rows
    has_constraint = has_constraint_in_catalog or has_constraint_in_rows

    # Only require a type if the summary claims entries of that type exist.
    summary_functional = _summary_metric_value(text, "Functional")
    summary_non_functional = _summary_metric_value(text, "Non-functional")
    summary_constraints = _summary_metric_value(text, "Constraints")

    missing = []
    if (summary_functional is None or summary_functional > 0) and not has_functional:
        missing.append("functional")
    if (summary_non_functional is None or summary_non_functional > 0) and not has_non_functional:
        missing.append("non-functional")
    if summary_constraints is not None and summary_constraints > 0 and not has_constraint:
        missing.append("constraint")

    passed = len(missing) == 0

    return _named_rule_result(
        "requirement_has_id",
        artifact_path,
        passed,
        "catalogue contains typed requirement identifiers"
        if passed
        else f"catalogue missing entries of type: {', '.join(missing)}",
        severity="required",
    )


def _rule_source_brs_ids_preserved(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> dict[str, str]:
    text = _read_text(path)
    source_ids = _source_brs_ids(workspace_root)
    preserved = _catalog_heading_ids(text) | set(re.findall(r"(?<![A-Za-z])(?:OBJ|FR|NFR|C|REQ)-\d{3}", text))

    missing_fr = sorted(source_ids["functional"] - preserved)
    missing_nfr = sorted(source_ids["non_functional"] - preserved)
    missing_obj = sorted(source_ids["objectives"] - preserved)
    missing = missing_fr + missing_nfr + missing_obj

    return _named_rule_result(
        "source_brs_ids_preserved",
        artifact_path,
        len(missing) == 0,
        (
            f"all source BRS identifiers preserved "
            f"(FR={len(source_ids['functional'])}, NFR={len(source_ids['non_functional'])}, OBJ={len(source_ids['objectives'])})"
        )
        if len(missing) == 0
        else f"missing source BRS identifiers: {missing[:10]}",
        severity="required",
    )


def _rule_atomic_requirements_summary_matches_catalog(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> dict[str, str]:
    text = _read_text(path)
    by_type = _catalog_entries_by_type(text)
    summary_total = _summary_metric_value(text, "Total requirements")
    summary_functional = _summary_metric_value(text, "Functional")
    summary_non_functional = _summary_metric_value(text, "Non-functional")
    summary_objectives = _summary_metric_value(text, "Business objectives")

    actual_functional = len(by_type.get("functional", []))
    actual_non_functional = len(by_type.get("non-functional", []))
    actual_objectives = len(by_type.get("objective", []))
    actual_constraints = len(by_type.get("constraint", []))
    actual_total = actual_functional + actual_non_functional + actual_objectives + actual_constraints

    mismatches: list[str] = []
    if summary_total is not None and summary_total != actual_total:
        mismatches.append(f"summary total={summary_total} actual={actual_total}")
    if summary_functional is not None and summary_functional != actual_functional:
        mismatches.append(f"summary functional={summary_functional} actual={actual_functional}")
    if summary_non_functional is not None and summary_non_functional != actual_non_functional:
        mismatches.append(f"summary non-functional={summary_non_functional} actual={actual_non_functional}")
    if summary_objectives is not None and summary_objectives != actual_objectives:
        mismatches.append(f"summary objectives={summary_objectives} actual={actual_objectives}")

    return _named_rule_result(
        "atomic_requirements_summary_matches_catalog",
        artifact_path,
        len(mismatches) == 0,
        "summary metrics match the actual catalog entries"
        if len(mismatches) == 0
        else "; ".join(mismatches),
        severity="required",
    )


def _rule_atomic_requirements_derivation_visible(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> dict[str, str]:
    text = _read_text(path)
    entries = _catalog_entry_blocks(text)
    if not entries:
        return _named_rule_result(
            "atomic_requirements_derivation_visible",
            artifact_path,
            False,
            "no requirement catalogue entries found",
            severity="required",
        )

    missing_derivation: list[str] = []
    inferred_without_source: list[str] = []
    direct_count = 0
    inferred_count = 0

    for req_id, _title, block in entries:
        match = re.search(r"^>\s*\*\*Derivation:\*\*\s*(.+)$", block, flags=re.MULTILINE)
        if not match:
            missing_derivation.append(req_id)
            continue

        derivation = match.group(1).strip()
        if re.search(r"(?i)\binferred\b", derivation):
            inferred_count += 1
            if not re.search(r"(?<![A-Za-z])(?:OBJ|FR|REQ|NFR|C)-\d{3}", derivation):
                inferred_without_source.append(req_id)
        else:
            direct_count += 1

    passed = not missing_derivation and not inferred_without_source
    detail_parts: list[str] = [
        f"direct={direct_count}",
        f"inferred={inferred_count}",
    ]
    if missing_derivation:
        detail_parts.append(f"missing derivation for {missing_derivation[:5]}")
    if inferred_without_source:
        detail_parts.append(f"inferred entries missing source IDs: {inferred_without_source[:5]}")

    return _named_rule_result(
        "atomic_requirements_derivation_visible",
        artifact_path,
        passed,
        "; ".join(detail_parts),
        severity="required",
    )


def _rule_atomic_requirements_decomposition_traceable(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> dict[str, str]:
    text = _read_text(path)
    entries = _catalog_entry_blocks(text)
    req_entries = [(req_id, block) for req_id, _title, block in entries if req_id.startswith("REQ-")]

    if not req_entries:
        return _named_rule_result(
            "atomic_requirements_decomposition_traceable",
            artifact_path,
            True,
            "no decomposed REQ entries present",
            severity="required",
        )

    mapping_block = _section_block(text, "## Source ID Mapping")
    if not mapping_block.strip():
        return _named_rule_result(
            "atomic_requirements_decomposition_traceable",
            artifact_path,
            False,
            "REQ entries exist but '## Source ID Mapping' is missing",
            severity="required",
        )

    missing_source_metadata: list[str] = []
    missing_mapping_rows: list[str] = []

    for req_id, block in req_entries:
        source_match = re.search(r"^\*\*Source:\*\*\s*(.+?)\s*\|\s*\*\*Actor:\*\*", block, flags=re.MULTILINE)
        source_value = source_match.group(1).strip() if source_match else ""
        source_ids = sorted(set(re.findall(r"(?<![A-Za-z])(?:OBJ|FR|REQ|NFR|C)-\d{3}", source_value)))
        if not source_ids:
            missing_source_metadata.append(req_id)
            continue

        if req_id not in mapping_block:
            missing_mapping_rows.append(req_id)
            continue

        missing_sources_for_req = [source_id for source_id in source_ids if source_id not in mapping_block]
        if missing_sources_for_req:
            missing_mapping_rows.append(f"{req_id}<-{','.join(missing_sources_for_req)}")

    passed = not missing_source_metadata and not missing_mapping_rows
    detail_parts: list[str] = [f"req_children={len(req_entries)}"]
    if missing_source_metadata:
        detail_parts.append(f"REQ entries missing source metadata: {missing_source_metadata[:5]}")
    if missing_mapping_rows:
        detail_parts.append(f"missing source mapping coverage: {missing_mapping_rows[:5]}")

    return _named_rule_result(
        "atomic_requirements_decomposition_traceable",
        artifact_path,
        passed,
        "; ".join(detail_parts),
        severity="required",
    )


def _rule_atomic_requirements_direct_inferred_summary_matches(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> dict[str, str]:
    text = _read_text(path)
    entries = _catalog_entry_blocks(text)

    actual_direct = 0
    actual_inferred = 0
    missing_derivation: list[str] = []

    for req_id, _title, block in entries:
        match = re.search(r"^>\s*\*\*Derivation:\*\*\s*(.+)$", block, flags=re.MULTILINE)
        if not match:
            missing_derivation.append(req_id)
            continue
        derivation = match.group(1).strip()
        if re.search(r"(?i)\binferred\b", derivation):
            actual_inferred += 1
        else:
            actual_direct += 1

    summary_direct = _summary_metric_value(text, "Direct requirements")
    summary_inferred = _summary_metric_value(text, "Inferred requirements")

    mismatches: list[str] = []
    if summary_direct is None:
        mismatches.append("summary metric missing: Direct requirements")
    elif summary_direct != actual_direct:
        mismatches.append(f"summary direct={summary_direct} actual={actual_direct}")

    if summary_inferred is None:
        mismatches.append("summary metric missing: Inferred requirements")
    elif summary_inferred != actual_inferred:
        mismatches.append(f"summary inferred={summary_inferred} actual={actual_inferred}")

    if missing_derivation:
        mismatches.append(f"entries missing derivation: {missing_derivation[:5]}")

    return _named_rule_result(
        "atomic_requirements_direct_inferred_summary_matches",
        artifact_path,
        len(mismatches) == 0,
        "direct/inferred summary metrics match derivation labels"
        if len(mismatches) == 0
        else "; ".join(mismatches),
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
    has_nfr_typed = bool(re.search(r"^\|\s*NFR-\d{3}\s*\|", text, flags=re.MULTILINE))
    has_req_with_nfr_type = bool(
        re.search(r"^\|\s*REQ-\d{3}\s*\|", text, flags=re.MULTILINE)
    ) and bool(
        re.search(r"^\|\s*Type\s*\|\s*Non-[Ff]unctional\s*\|", text, flags=re.MULTILINE)
    )
    passed = has_nfr_typed or has_req_with_nfr_type
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


def _rule_delivery_skeleton_requirement_basis_visible(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> dict[str, str]:
    text = _read_text(path)
    derivations = _canonical_requirement_derivations(workspace_root)
    coverage_rows = _section_table_rows(text, "## Requirement Coverage")
    if not coverage_rows:
        return _named_rule_result(
            "delivery_skeleton_requirement_basis_visible",
            artifact_path,
            False,
            "Requirement Coverage table not found or empty",
            severity="required",
        )

    missing_basis: list[str] = []
    mismatches: list[str] = []
    checked = 0

    for row in coverage_rows:
        if len(row) < 4:
            continue
        req_id = row[0].strip()
        if not re.fullmatch(r"(?:FR|REQ|NFR|C)-\d{3}", req_id):
            continue
        checked += 1
        basis = row[3].strip().lower() if len(row) >= 4 else ""
        if basis not in {"direct", "inferred"}:
            missing_basis.append(req_id)
            continue
        expected = derivations.get(req_id)
        if expected and basis != expected:
            mismatches.append(f"{req_id} basis={basis} expected={expected}")

    passed = checked > 0 and not missing_basis and not mismatches
    details: list[str] = [f"checked={checked}"]
    if missing_basis:
        details.append(f"missing/invalid basis for {missing_basis[:5]}")
    if mismatches:
        details.append(f"basis mismatches: {mismatches[:5]}")

    return _named_rule_result(
        "delivery_skeleton_requirement_basis_visible",
        artifact_path,
        passed,
        "; ".join(details),
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


_SEMANTIC_THRESHOLD = 0.25


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
                    _section_block(text, "## In Scope"),
                ]
            )
            for req_id in story_titles:
                canonical_req = canonical.get(req_id)
                if canonical_req is None:
                    continue
                if not canonical_req.get("keywords"):
                    continue
                score, details = _semantic_overlap_score(canonical_req, semantic_text)
                if score < _SEMANTIC_THRESHOLD:
                    req_title = canonical_req.get("title", "")
                    story_kw = sorted(_keywords(semantic_text))[:8]
                    failures.append(
                        f"{req_id} ({req_title}): story {story_file.name} score "
                        f"{score:.2f} < {_SEMANTIC_THRESHOLD} — "
                        f"story discusses: {', '.join(story_kw[:5])}"
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


def _rule_epic_traceability_basis_visible(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> dict[str, str]:
    if not path.is_dir():
        return _named_rule_result(
            "epic_traceability_basis_visible",
            artifact_path,
            True,
            "epic traceability basis check applies to epic directories only",
            severity="required",
        )

    derivations = _canonical_requirement_derivations(workspace_root)
    failures: list[str] = []
    checked = 0

    for epic_dir in sorted([d for d in path.iterdir() if d.is_dir() and d.name.startswith("E-")]):
        epic_md = epic_dir / "epic.md"
        if not epic_md.exists():
            continue
        rows = _section_table_rows(_read_text(epic_md), "## Source Traceability")
        for row in rows:
            if len(row) < 4:
                continue
            source_type = row[0].strip().lower()
            reference = row[1].strip()
            basis = row[2].strip().lower()
            if source_type != "requirement":
                continue
            if not re.fullmatch(r"(?:FR|REQ|NFR|C)-\d{3}", reference):
                continue
            checked += 1
            expected = derivations.get(reference)
            if basis not in {"direct", "inferred"}:
                failures.append(f"{epic_dir.name}: {reference} missing valid basis")
            elif expected and basis != expected:
                failures.append(f"{epic_dir.name}: {reference} basis={basis} expected={expected}")

    return _named_rule_result(
        "epic_traceability_basis_visible",
        artifact_path,
        checked > 0 and len(failures) == 0,
        f"epic traceability basis is visible for {checked} requirement rows"
        if checked > 0 and len(failures) == 0
        else "; ".join(failures[:6]) if failures else "no epic requirement traceability rows checked",
        severity="required",
    )


def _rule_story_linked_requirements_basis_visible(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> dict[str, str]:
    if not path.is_dir():
        return _named_rule_result(
            "story_linked_requirements_basis_visible",
            artifact_path,
            True,
            "story linked requirement basis check applies to epic directories only",
            severity="required",
        )

    derivations = _canonical_requirement_derivations(workspace_root)
    failures: list[str] = []
    checked = 0

    for epic_dir in sorted([d for d in path.iterdir() if d.is_dir() and d.name.startswith("E-")]):
        stories_dir = epic_dir / "stories"
        if not stories_dir.exists():
            continue
        for story_file in sorted(stories_dir.glob("S-*.md")):
            if story_file.name.endswith(".prompt.md"):
                continue
            rows = _section_table_rows(_read_text(story_file), "## Linked Requirements")
            for row in rows:
                if len(row) < 3:
                    continue
                req_id = row[0].strip()
                basis = row[2].strip().lower()
                if not re.fullmatch(r"(?:FR|REQ|NFR|C)-\d{3}", req_id):
                    continue
                checked += 1
                expected = derivations.get(req_id)
                if basis not in {"direct", "inferred"}:
                    failures.append(f"{story_file.name}: {req_id} missing valid basis")
                elif expected and basis != expected:
                    failures.append(f"{story_file.name}: {req_id} basis={basis} expected={expected}")

    return _named_rule_result(
        "story_linked_requirements_basis_visible",
        artifact_path,
        checked > 0 and len(failures) == 0,
        f"story linked requirement basis is visible for {checked} requirement rows"
        if checked > 0 and len(failures) == 0
        else "; ".join(failures[:6]) if failures else "no story linked requirement rows checked",
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
    matrix_block = _section_block(text, "## Full Coverage Matrix")
    if not matrix_block:
        return _named_rule_result(
            "coverage_claim_matches_evidence",
            artifact_path,
            False,
            "no Full Coverage Matrix section found",
            severity="required",
        )

    # Parse header to find column indices dynamically
    table_lines = [l for l in matrix_block.splitlines() if l.strip().startswith("|")]
    if len(table_lines) < 2:
        return _named_rule_result(
            "coverage_claim_matches_evidence",
            artifact_path,
            False,
            "coverage matrix has no table rows",
            severity="required",
        )

    header_cells = [c.strip().lower() for c in table_lines[0].split("|")]
    header_cells = [c for c in header_cells if c]

    def _find_col(keywords: list[str]) -> int:
        # Prefer exact match over substring match
        for i, cell in enumerate(header_cells):
            if cell in keywords:
                return i
        for i, cell in enumerate(header_cells):
            if any(kw in cell for kw in keywords):
                return i
        return -1

    story_col = _find_col(["story"])
    status_col = _find_col(["status"])
    req_col = 0  # first column is always requirement ID

    if story_col < 0 or status_col < 0:
        return _named_rule_result(
            "coverage_claim_matches_evidence",
            artifact_path,
            False,
            f"cannot find Story or Status column in matrix header: {header_cells}",
            severity="required",
        )

    # Collect known story IDs from disk
    story_files: set[str] = set()
    epics_dir = workspace_root / "epics"
    if epics_dir.exists():
        for story_file in epics_dir.rglob("S-*.md"):
            if story_file.is_file() and not story_file.name.endswith(".prompt.md"):
                m = re.match(r"(S-\d{3}\.\d+)", story_file.stem)
                if m:
                    story_files.add(m.group(1))
                else:
                    story_files.add(story_file.stem)
                # Also extract ID from the file heading
                try:
                    first_line = story_file.read_text(encoding="utf-8").split("\n", 1)[0]
                    hm = re.search(r"(S-\d{3}\.\d+)", first_line)
                    if hm:
                        story_files.add(hm.group(1))
                except Exception:
                    pass

    # Parse data rows
    matrix_rows: list[list[str]] = []
    for line in table_lines[2:]:  # skip header + separator
        cells = [c.strip() for c in line.split("|")]
        cells = [c for c in cells if c != ""]
        if cells and re.fullmatch(r"(?:FR|REQ|NFR|C)-\d{3}", cells[0].strip()):
            matrix_rows.append(cells)

    covered = 0
    in_scope_rows = 0
    mismatches: list[str] = []
    for cells in matrix_rows:
        if len(cells) <= max(story_col, status_col):
            continue
        req_id = cells[req_col].strip()
        raw_story = cells[story_col].strip()
        # Extract story ID from possible markdown link [S-001.0](path)
        link_match = re.search(r"(S-\d{3}\.\d+)", raw_story)
        story_id = link_match.group(1) if link_match else raw_story
        status = cells[status_col].strip().strip("*")  # strip bold markers
        if status != "Deferred":
            in_scope_rows += 1
        if status == "Covered":
            if story_id == "—" or (story_id not in story_files and not any(story_id in sf for sf in story_files)):
                mismatches.append(f"{req_id} marked Covered but story '{story_id}' is missing")
            else:
                covered += 1

    # Check declared summary metrics — accept both old and new heading formats
    uses_generated_summary = "## Generated Coverage Summary" in text
    declared_total_match = (
        re.search(r"\|\s*Total requirements[^|]*\|\s*(\d+)\s*\|", text)
        or re.search(r"\|\s*In-scope requirements[^|]*\|\s*(\d+)\s*\|", text)
    )
    declared_covered_match = re.search(
        r"\|\s*Covered by (?:implementation stories|at least one story)\s*\|\s*(\d+)\s*\|", text,
    )
    declared_pct_match = (
        re.search(r"\|\s*Coverage percentage\s*\|\s*(\d+)%?\s*\|", text)
        or re.search(r"\|\s*Generated coverage\s*\|\s*(\d+)%?\s*\|", text)
    )
    computed_total = in_scope_rows if uses_generated_summary else len(matrix_rows)
    declared_total = int(declared_total_match.group(1)) if declared_total_match else computed_total
    declared_covered = int(declared_covered_match.group(1)) if declared_covered_match else covered
    declared_pct = int(declared_pct_match.group(1)) if declared_pct_match else (covered * 100 // declared_total if declared_total else 100)
    computed_pct = (covered * 100 // computed_total) if computed_total else 100

    passed = (
        not mismatches
        and declared_total == computed_total
        and declared_covered == covered
        and declared_pct == computed_pct
    )
    detail = (
        f"coverage summary matches evidence ({covered}/{computed_total} covered, {computed_pct}%)"
        if passed
        else "; ".join(
            mismatches[:3]
            + [
                f"declared total={declared_total} computed total={computed_total}",
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


def _rule_coverage_classifications_acceptable(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> dict[str, str]:
    computed = _load_computed_coverage(workspace_root)
    if not computed:
        return _named_rule_result(
            "coverage_classifications_acceptable",
            artifact_path,
            True,
            "no computed coverage data available - skipping coverage classification audit",
            severity="required",
        )

    failures: list[str] = []
    for row in computed.get("coverage_matrix", []):
        req_id = str(row.get("req_id") or "")
        title = str(row.get("title") or "")
        scope = str(row.get("scope") or "")
        status = str(row.get("status") or "")
        evidence = str(row.get("evidence") or "")

        if scope == "in_scope" and req_id.startswith(("FR-", "REQ-")) and status in {"Referenced Only", "Spike Only"}:
            failures.append(f"{req_id} ({title}) has weak coverage status '{status}'")

        if status == "Deferred" and not re.search(r"(?i)^Deferred to E-\d{3}.*(?:\:| because )", evidence):
            failures.append(f"{req_id} deferred without explicit rationale: {evidence or 'missing evidence'}")

    return _named_rule_result(
        "coverage_classifications_acceptable",
        artifact_path,
        len(failures) == 0,
        "coverage classifications are implementation-safe"
        if len(failures) == 0
        else "; ".join(failures[:6]),
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


def _rule_all_components_from_architecture_review_present(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> dict[str, str]:
    """Check that the technical landscape covers components from the architecture review."""
    landscape_text = _read_text(path)
    review_path = workspace_root / "architecture" / "architecture-review.md"
    if not review_path.exists():
        return _named_rule_result(
            "all_components_from_architecture_review_present",
            artifact_path,
            True,
            "architecture review not found — skipping cross-check",
            severity="required",
        )
    review_text = _read_text(review_path)
    # Extract component names from architecture review tables (first column after |)
    # Extract component names from the Initiative-Architecture Fit and Brownfield
    # Impact sections.  These are the sections that list actual system components.
    review_components: set[str] = set()

    # Strategy: find the Initiative-Architecture Fit table and extract component
    # names from the data rows (skip header and separator rows).
    fit_match = re.search(
        r"## Initiative-Architecture Fit.*?(?=^## |\Z)",
        review_text,
        flags=re.MULTILINE | re.DOTALL,
    )
    if fit_match:
        fit_text = fit_match.group(0)
        # Find data rows — lines starting with | that are not the header or separator
        fit_rows = [
            line for line in fit_text.splitlines()
            if line.startswith("|")
            and "---" not in line
            and "Feature Area" not in line
            and "Existing Components" not in line
        ]
        for row in fit_rows:
            cells = [c.strip() for c in row.split("|") if c.strip()]
            # Cells 1 and 2 (0-indexed) contain component lists
            for cell in cells[1:3] if len(cells) > 2 else []:
                for name in re.split(r"[,;]", cell):
                    name = re.sub(r"\(.*?\)", "", name).strip()
                    if name and len(name) > 2:
                        review_components.add(name.lower())

    # Also extract from Brownfield Impact Component column (first column)
    brownfield_match = re.search(
        r"## Brownfield Impact.*?(?=^## |\Z)",
        review_text,
        flags=re.MULTILINE | re.DOTALL,
    )
    if brownfield_match:
        brownfield_text = brownfield_match.group(0)
        for m in re.finditer(
            r"^\|\s*([A-Z][A-Za-z0-9 /&-]+?)\s*\|",
            brownfield_text,
            flags=re.MULTILINE,
        ):
            name = m.group(1).strip()
            if name and name.lower() not in ("component", "change type", "consumers"):
                review_components.add(name.lower())

    if not review_components:
        return _named_rule_result(
            "all_components_from_architecture_review_present",
            artifact_path,
            True,
            "no components extracted from architecture review — skipping",
            severity="required",
        )

    landscape_lower = landscape_text.lower()
    _ACCOUNTED_MARKERS = ["needs-clarification", "out-of-scope", "deferred", "not-impacted", "not impacted"]
    missing = []
    for c in review_components:
        if c in landscape_lower:
            continue
        if any(marker in landscape_lower for marker in _ACCOUNTED_MARKERS):
            continue
        missing.append(c)
    missing.sort()
    covered = len(review_components) - len(missing)

    return _named_rule_result(
        "all_components_from_architecture_review_present",
        artifact_path,
        len(missing) == 0,
        f"technical landscape accounts for all {len(review_components)} architecture review components"
        if len(missing) == 0
        else f"technical landscape missing components: {', '.join(missing[:5])} ({covered}/{len(review_components)} accounted for)",
        severity="required",
    )


def _rule_all_functional_requirements_mapped(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> dict[str, str]:
    """Check that the impacted systems map covers all functional requirements."""
    impact_text = _read_text(path)
    canonical = _canonical_requirements(workspace_root)
    if not canonical:
        return _named_rule_result(
            "all_functional_requirements_mapped",
            artifact_path,
            True,
            "no canonical requirements found — skipping",
            severity="required",
        )

    functional_ids = sorted([
        rid for rid, req in canonical.items()
        if rid.startswith("FR-") or req.get("type", "").lower() == "functional"
    ])
    if not functional_ids:
        # Fall back: count all REQ- entries that have functional type via catalog parsing
        req_path = workspace_root / "requirements" / "atomic-requirements.md"
        if req_path.exists():
            by_type = _catalog_entries_by_type(_read_text(req_path))
            functional_ids = sorted(by_type.get("functional", []))

    if not functional_ids:
        return _named_rule_result(
            "all_functional_requirements_mapped",
            artifact_path,
            True,
            "no functional requirements found — skipping",
            severity="required",
        )

    missing = [rid for rid in functional_ids if rid not in impact_text]
    covered = len(functional_ids) - len(missing)

    return _named_rule_result(
        "all_functional_requirements_mapped",
        artifact_path,
        len(missing) == 0,
        f"all {len(functional_ids)} functional requirements appear in the impact map"
        if len(missing) == 0
        else f"missing from impact map: {', '.join(missing[:10])} ({covered}/{len(functional_ids)} covered)",
        severity="required",
    )


def _rule_all_impacted_components_have_decisions(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> dict[str, str]:
    """Check that every component in the impacted systems map has a decision."""
    decisions_text = _read_text(path)
    impact_path = workspace_root / "architecture" / "impacted-systems.md"
    if not impact_path.exists():
        return _named_rule_result(
            "all_impacted_components_have_decisions",
            artifact_path,
            True,
            "impacted systems artifact not found — skipping cross-check",
            severity="required",
        )
    impact_text = _read_text(impact_path)

    impacted: set[str] = set()

    _KNOWN_HEADERS = {
        "requirement", "existing services", "new services", "impacted repos",
        "new apis", "new schemas", "component", "type", "rationale",
        "concern", "affected components", "requirements", "notes",
        "nfr", "impact type", "metric", "value", "field", "dimension",
        "details", "triggered by requirements", "source id", "title / summary",
        "preserved in", "integration changes", "feature", "feature title",
        "requirements covered", "priority", "status", "epic",
    }

    for section_heading in ["## New-Proposed Components", "## Impact Summary Table"]:
        block = _section_block(impact_text, section_heading)
        if not block:
            continue
        rows = _section_table_rows(impact_text, section_heading)
        for row in rows:
            if row and len(row) >= 2:
                name = row[0].strip()
                if name.lower() not in _KNOWN_HEADERS and len(name) > 2:
                    impacted.add(name.lower())

    for heading in ["## Existing Services", "## New Services"]:
        block = _section_block(impact_text, heading)
        if not block:
            continue
        for line in block.splitlines():
            stripped = line.strip()
            if stripped.startswith("- "):
                name = stripped[2:].split("—")[0].split(":")[0].strip()
                if name and len(name) > 2:
                    impacted.add(name.lower())
            elif stripped.startswith("|"):
                cells = [c.strip() for c in stripped.strip("|").split("|")]
                if cells and cells[0].lower() not in _KNOWN_HEADERS and len(cells[0]) > 2:
                    impacted.add(cells[0].lower())

    per_req_sections = re.findall(
        r"^\|\s*Existing services impacted\s*\|\s*(.+?)\s*\|$",
        impact_text,
        flags=re.MULTILINE,
    )
    for cell in per_req_sections:
        for name in re.split(r",\s*", cell):
            name = name.strip()
            if name and name.lower() not in ("none", "n/a", "") and len(name) > 2:
                impacted.add(name.lower())

    if not impacted:
        return _named_rule_result(
            "all_impacted_components_have_decisions",
            artifact_path,
            True,
            "no impacted components extracted — skipping",
            severity="required",
        )

    decisions_lower = decisions_text.lower()
    _ACCOUNTED_MARKERS = ["needs-clarification", "out-of-scope", "deferred", "not-impacted", "not impacted"]
    missing = []
    for c in impacted:
        if c in decisions_lower:
            continue
        if any(marker in decisions_lower for marker in _ACCOUNTED_MARKERS):
            continue
        missing.append(c)
    missing.sort()
    covered = len(impacted) - len(missing)

    return _named_rule_result(
        "all_impacted_components_have_decisions",
        artifact_path,
        len(missing) == 0,
        f"solution decisions account for all {len(impacted)} impacted components"
        if len(missing) == 0
        else f"missing decisions for: {', '.join(missing[:5])} ({covered}/{len(impacted)} accounted for)",
        severity="required",
    )


def _rule_solution_decisions_traceability_complete(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> dict[str, str]:
    text = _read_text(path)
    decision_ids = set(re.findall(r"^\|\s*(SD-\d{3})\s*\|", text, flags=re.MULTILINE))
    traceability_rows = _section_table_rows(text, "## Decision Traceability")
    traced_ids = {
        row[0].strip()
        for row in traceability_rows
        if len(row) >= 1 and re.fullmatch(r"SD-\d{3}", row[0].strip())
    }

    if not decision_ids:
        return _named_rule_result(
            "solution_decisions_traceability_complete",
            artifact_path,
            True,
            "no solution decisions found - skipping traceability completeness check",
            severity="required",
        )

    missing = sorted(decision_ids - traced_ids)
    return _named_rule_result(
        "solution_decisions_traceability_complete",
        artifact_path,
        len(missing) == 0,
        f"traceability covers all {len(decision_ids)} solution decisions"
        if len(missing) == 0
        else f"decisions missing traceability rows: {missing[:10]}",
        severity="required",
    )


def _rule_solution_decisions_inferred_requirements_visible(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> dict[str, str]:
    text = _read_text(path)
    derivations = _canonical_requirement_derivations(workspace_root)
    traceability_rows = _section_table_rows(text, "## Decision Traceability")
    if not traceability_rows:
        return _named_rule_result(
            "solution_decisions_inferred_requirements_visible",
            artifact_path,
            False,
            "Decision Traceability table not found or empty",
            severity="required",
        )

    failures: list[str] = []
    checked = 0
    for row in traceability_rows:
        if len(row) < 3:
            continue
        decision_id = row[0].strip()
        req_cell = row[1].strip()
        basis = row[2].strip().lower()
        if not re.fullmatch(r"SD-\d{3}", decision_id):
            continue
        checked += 1
        req_ids = re.findall(r"(?<![A-Za-z])(?:FR|REQ|NFR|C)-\d{3}", req_cell)
        if not req_ids:
            if basis != "architectural-context":
                failures.append(f"{decision_id} has no requirement IDs but basis={basis}")
            continue

        expected_types = {derivations.get(req_id) for req_id in req_ids if derivations.get(req_id)}
        if "inferred" in expected_types and basis not in {"inferred", "mixed"}:
            failures.append(f"{decision_id} links inferred requirements {req_ids} but basis={basis}")
        elif expected_types == {"direct"} and basis not in {"direct", "mixed"}:
            failures.append(f"{decision_id} links direct requirements {req_ids} but basis={basis}")

    return _named_rule_result(
        "solution_decisions_inferred_requirements_visible",
        artifact_path,
        checked > 0 and len(failures) == 0,
        f"traceability basis is visible for {checked} solution decisions"
        if checked > 0 and len(failures) == 0
        else "; ".join(failures[:6]) if failures else "no decision traceability rows checked",
        severity="required",
    )


def _rule_ui_spec_confirmed_pages_have_page_sections(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> dict[str, str]:
    text = _read_text(path)
    coverage_match = re.search(
        r"## Page Specification Coverage\s*\n((?:\|.*\n)+)", text
    )
    if not coverage_match:
        return _named_rule_result(
            "ui_spec_confirmed_pages_have_page_sections",
            artifact_path,
            False,
            "Page Specification Coverage table not found",
            severity="required",
        )

    confirmed_pages: list[str] = []
    for row in coverage_match.group(1).splitlines():
        cells = [c.strip() for c in row.split("|") if c.strip()]
        if len(cells) < 4:
            continue
        status_cell = cells[3].lower().strip()
        if status_cell in ("confirmed", "full-spec"):
            confirmed_pages.append(cells[2].strip())

    page_sections = {
        m.strip().lower()
        for m in re.findall(r"^###\s+Page:\s*(.+)$", text, flags=re.MULTILINE)
    }
    missing = [p for p in confirmed_pages if p.lower() not in page_sections]

    return _named_rule_result(
        "ui_spec_confirmed_pages_have_page_sections",
        artifact_path,
        len(missing) == 0,
        f"all {len(confirmed_pages)} confirmed pages have page sections"
        if len(missing) == 0
        else f"confirmed pages missing page sections: {', '.join(missing[:5])}",
        severity="required",
    )


def _rule_ui_spec_confirmed_pages_have_required_subsections(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> dict[str, str]:
    text = _read_text(path)
    required_subsections = [
        "layout", "sections", "data binding", "states", "user flow",
        "permissions", "acceptance scenarios",
    ]
    page_sections = re.split(r"^###\s+Page:\s*", text, flags=re.MULTILINE)[1:]
    missing_report: list[str] = []

    for section in page_sections:
        page_name_match = re.match(r"(.+?)$", section.strip(), flags=re.MULTILINE)
        page_name = page_name_match.group(1).strip() if page_name_match else "unknown"
        section_lower = section.lower()
        missing_subs = [s for s in required_subsections if f"#### {s}" not in section_lower]
        if missing_subs:
            missing_report.append(f"{page_name}: {', '.join(missing_subs)}")

    return _named_rule_result(
        "ui_spec_confirmed_pages_have_required_subsections",
        artifact_path,
        len(missing_report) == 0,
        "all page sections have required subsections"
        if len(missing_report) == 0
        else f"pages missing subsections: {'; '.join(missing_report[:3])}",
        severity="required",
    )


def _rule_ui_spec_no_confirmed_when_blockers_exist(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> dict[str, str]:
    text = _read_text(path)

    blocking_routes: set[str] = set()
    questions_match = re.search(
        r"## Open UI Questions\s*\n((?:\|.*\n)+)", text
    )
    if questions_match:
        for row in questions_match.group(1).splitlines():
            cells = [c.strip() for c in row.split("|") if c.strip()]
            if len(cells) >= 6:
                qid = cells[0].strip()
                blocking = cells[5].strip().lower()
                if blocking == "yes" and re.match(r"UIQ-\d+", qid):
                    for r in re.split(r"[,;]", cells[3]):
                        blocking_routes.add(r.strip().lower())

    violations: list[str] = []

    coverage_match = re.search(
        r"## Page Specification Coverage\s*\n((?:\|.*\n)+)", text
    )
    if coverage_match:
        for row in coverage_match.group(1).splitlines():
            cells = [c.strip() for c in row.split("|") if c.strip()]
            if len(cells) >= 4:
                route = cells[1].strip()
                page = cells[2].strip()
                status = cells[3].strip().lower()
                if status == "confirmed" and blocking_routes:
                    for br in blocking_routes:
                        if route.lower() in br or br in route.lower() or page.lower() in br:
                            violations.append(f"{page} ({route})")

    for m in re.finditer(
        r"\*\*Blocking dependencies:\*\*\s*(.+?)$", text, flags=re.MULTILINE
    ):
        deps = m.group(1).strip()
        if deps.lower() != "none" and deps != "—":
            status_match = re.search(
                r"\*\*Specification status:\*\*\s*(.+?)$",
                text[max(0, m.start() - 300):m.start()],
                flags=re.MULTILINE,
            )
            if status_match and status_match.group(1).strip().lower() == "confirmed":
                violations.append(f"page with deps={deps}")

    return _named_rule_result(
        "ui_spec_no_confirmed_when_blockers_exist",
        artifact_path,
        len(violations) == 0,
        "no confirmed pages have blocking questions or dependencies"
        if len(violations) == 0
        else f"confirmed pages with blockers: {', '.join(violations[:5])}",
        severity="required",
    )


def _rule_ui_spec_data_binding_contract_mode_present(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> dict[str, str]:
    text = _read_text(path)
    binding_tables = re.findall(
        r"#### Data Binding\s*\n((?:\|.*\n)+)", text
    )
    if not binding_tables:
        has_no_api = "no api dependency" in text.lower()
        return _named_rule_result(
            "ui_spec_data_binding_contract_mode_present",
            artifact_path,
            has_no_api,
            "no data binding tables found — pages explicitly state no API dependency"
            if has_no_api
            else "no data binding tables and no explicit 'no API dependency' statement",
            severity="required",
        )

    valid_modes = {"confirmed", "partial", "proposed-by-ui-spec", "mock", "unknown"}
    missing_mode: list[str] = []
    for table in binding_tables:
        header_line = table.strip().splitlines()[0] if table.strip() else ""
        if "contract mode" not in header_line.lower():
            missing_mode.append("table missing Contract Mode column")
            continue
        for row in table.strip().splitlines()[2:]:
            cells = [c.strip() for c in row.split("|") if c.strip()]
            if cells:
                last_cell = cells[-1].strip().lower()
                if last_cell not in valid_modes:
                    missing_mode.append(f"{cells[0]}: mode '{cells[-1]}'")

    return _named_rule_result(
        "ui_spec_data_binding_contract_mode_present",
        artifact_path,
        len(missing_mode) == 0,
        "all data binding rows have valid Contract Mode"
        if len(missing_mode) == 0
        else f"contract mode issues: {', '.join(missing_mode[:5])}",
        severity="required",
    )


def _rule_ui_spec_every_inferred_has_open_question(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> dict[str, str]:
    text = _read_text(path)

    question_routes: set[str] = set()
    questions_match = re.search(
        r"## Open UI Questions\s*\n((?:\|.*\n)+)", text
    )
    if questions_match:
        for row in questions_match.group(1).splitlines():
            cells = [c.strip() for c in row.split("|") if c.strip()]
            if len(cells) >= 5 and not cells[0].lower().startswith("id") and "---" not in cells[0]:
                for r in re.split(r"[,;]", cells[3]):
                    route = r.strip().lower()
                    if route:
                        question_routes.add(route)

    inferred_pages: list[str] = []
    coverage_match = re.search(
        r"## Page Specification Coverage\s*\n((?:\|.*\n)+)", text
    )
    if coverage_match:
        for row in coverage_match.group(1).splitlines():
            cells = [c.strip() for c in row.split("|") if c.strip()]
            if len(cells) >= 4 and "---" not in cells[0]:
                route = cells[1].strip().lower()
                page = cells[2].strip()
                status = cells[3].strip().lower()
                if status == "inferred":
                    inferred_pages.append((page, route))

    page_sections = re.split(r"^###\s+Page:\s*", text, flags=re.MULTILINE)[1:]
    inferred_page_names: list[str] = []
    for section in page_sections:
        page_name_match = re.match(r"(.+?)$", section.strip(), flags=re.MULTILINE)
        page_name = page_name_match.group(1).strip() if page_name_match else ""
        if "inferred" in section.lower():
            route_match = re.search(r"\*\*Route:\*\*\s*(.+?)$", section, flags=re.MULTILINE)
            route = route_match.group(1).strip().lower() if route_match else ""
            if (page_name, route) not in inferred_pages:
                inferred_page_names.append((page_name, route))

    all_inferred = inferred_pages + inferred_page_names
    uncovered: list[str] = []
    for page_name, route in all_inferred:
        covered = any(
            route in qr or qr in route
            for qr in question_routes
        ) if route else False
        if not covered and question_routes:
            covered = any(page_name.lower() in qr for qr in question_routes)
        if not covered:
            uncovered.append(f"{page_name} ({route})" if route else page_name)

    if not all_inferred:
        return _named_rule_result(
            "ui_spec_every_inferred_has_open_question",
            artifact_path,
            True,
            "no inferred pages found",
            severity="required",
        )

    return _named_rule_result(
        "ui_spec_every_inferred_has_open_question",
        artifact_path,
        len(uncovered) == 0,
        f"all {len(all_inferred)} inferred pages have matching open questions"
        if len(uncovered) == 0
        else f"inferred pages without matching open questions: {', '.join(uncovered[:5])}",
        severity="required",
    )


def _rule_ui_spec_open_questions_have_required_before(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> dict[str, str]:
    text = _read_text(path)
    questions_match = re.search(
        r"## Open UI Questions\s*\n((?:\|.*\n)+)", text
    )
    if not questions_match:
        return _named_rule_result(
            "ui_spec_open_questions_have_required_before",
            artifact_path,
            True,
            "no open UI questions section found - check not applicable",
            severity="required",
        )

    valid_required_before = {
        "delivery-planning",
        "epic-elaboration",
        "coding-handoff",
        "n/a",
        "—",
        "-",
        "na",
    }
    issues: list[str] = []

    for row in questions_match.group(1).splitlines():
        cells = [c.strip() for c in row.split("|") if c.strip()]
        if len(cells) < 8:
            continue
        if cells[0].lower() == "id" or cells[0].startswith("---"):
            continue
        if not re.match(r"UIQ-\d+", cells[0]):
            continue

        question_id = cells[0]
        blocking = cells[5].strip().lower()
        required_before = cells[6].strip().lower() if len(cells) >= 7 else ""

        if required_before not in valid_required_before:
            issues.append(f"{question_id}: invalid Required Before '{cells[6]}'")
            continue

        if blocking == "yes" and required_before in {"n/a", "—", "-", "na"}:
            issues.append(f"{question_id}: blocking question cannot use Required Before '{cells[6]}'")
        if blocking == "no" and required_before not in {"n/a", "—", "-", "na"}:
            issues.append(f"{question_id}: non-blocking question should use Required Before 'n/a'")

    return _named_rule_result(
        "ui_spec_open_questions_have_required_before",
        artifact_path,
        len(issues) == 0,
        "all open UI questions classify Required Before consistently"
        if len(issues) == 0
        else f"open UI question classification issues: {', '.join(issues[:5])}",
        severity="required",
    )


def _rule_ui_spec_shared_components_match_page_fields(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> dict[str, str]:
    text = _read_text(path)
    components_match = re.search(
        r"## Shared Components\s*\n((?:\|.*\n)+)", text
    )
    if not components_match:
        return _named_rule_result(
            "ui_spec_shared_components_match_page_fields",
            artifact_path,
            True,
            "no shared components section — check not applicable",
            severity="optional",
        )

    mismatches: list[str] = []
    for row in components_match.group(1).splitlines():
        cells = [c.strip() for c in row.split("|") if c.strip()]
        if len(cells) < 4:
            continue
        comp_name = cells[0].strip()
        if comp_name.lower() in ("component", "---"):
            continue
        props_str = cells[3].strip().lower()
        prop_fields = [
            f.strip().rstrip(",")
            for f in re.split(r"[,;:]", props_str)
            if f.strip() and f.strip() not in ("fields", "columns", "data inputs", "props / inputs")
        ]
        used_by = cells[2].strip()
        for page_name in re.split(r"[,;]", used_by):
            page_name = page_name.strip()
            page_match = re.search(
                rf"###\s+Page:\s*{re.escape(page_name)}\s*\n(.*?)(?=\n###\s|\Z)",
                text,
                flags=re.DOTALL,
            )
            if page_match:
                page_text = page_match.group(1).lower()
                for field in prop_fields:
                    if field and field not in page_text:
                        mismatches.append(f"{comp_name}.{field} not in {page_name}")

    return _named_rule_result(
        "ui_spec_shared_components_match_page_fields",
        artifact_path,
        len(mismatches) == 0,
        "shared component props consistent with page fields"
        if len(mismatches) == 0
        else f"component/page field mismatches: {', '.join(mismatches[:5])}",
        severity="optional",
    )


def _rule_ui_spec_no_encoding_mojibake(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> dict[str, str]:
    text = _read_text(path)
    mojibake_sequences = [
        "\xc3\xa2\xc2\x80\xc2\x93",  # en-dash mojibake
        "\xc3\xa2\xc2\x80\xc2\x99",  # right single-quote mojibake
        "\xc3\xa2\xc2\x80\xc2\x9c",  # left double-quote mojibake
        "\xc3\xa2\xc2\x80\xc2\x9d",  # right double-quote mojibake
        "\xc3\xa2\xc2\x86\xc2\x92",  # arrow mojibake
    ]
    mojibake_patterns = [
        r"\xc3[\x80-\xbf]\xc2",  # generic double-encoded UTF-8 pattern
    ]
    found: list[str] = []
    for seq in mojibake_sequences:
        count = text.count(seq)
        if count:
            found.append(f"mojibake-sequence x{count}")
    for pattern in mojibake_patterns:
        matches = re.findall(pattern, text)
        if matches:
            found.append(f"double-encoded-utf8 x{len(matches)}")

    return _named_rule_result(
        "ui_spec_no_encoding_mojibake",
        artifact_path,
        len(found) == 0,
        "no encoding artifacts detected"
        if len(found) == 0
        else f"encoding issues found: {', '.join(found[:5])}",
        severity="required",
    )


def _rule_epic_clarification_request_has_questions_or_explicit_no_blockers(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> dict[str, str]:
    state = workspace.load_state(workspace_root)
    current_item = state.get("current_item")
    if not current_item:
        return _named_rule_result(
            "epic_clarification_request_has_questions_or_explicit_no_blockers",
            artifact_path,
            False,
            "current_item not set for clarification validation",
            severity="required",
        )

    epic_dirs = sorted([d for d in path.iterdir() if d.is_dir() and d.name.startswith(current_item)]) if path.exists() else []
    if not epic_dirs:
        return _named_rule_result(
            "epic_clarification_request_has_questions_or_explicit_no_blockers",
            artifact_path,
            False,
            f"no epic directory found for {current_item}",
            severity="required",
        )

    request_path = epic_dirs[0] / "clarification-request.md"
    if not request_path.exists():
        return _named_rule_result(
            "epic_clarification_request_has_questions_or_explicit_no_blockers",
            artifact_path,
            False,
            f"{epic_dirs[0].name}/clarification-request.md missing",
            severity="required",
        )

    text = _read_text(request_path)
    if "No blocking questions require clarification for this epic." in text:
        return _named_rule_result(
            "epic_clarification_request_has_questions_or_explicit_no_blockers",
            artifact_path,
            True,
            "clarification request explicitly states no blocking questions remain",
            severity="required",
        )

    table_match = re.search(r"## Blocking Questions\s*\n((?:\|.*\n)+)", text)
    if not table_match:
        return _named_rule_result(
            "epic_clarification_request_has_questions_or_explicit_no_blockers",
            artifact_path,
            False,
            "clarification request has neither explicit no-blockers text nor a blocking questions table",
            severity="required",
        )

    row_count = 0
    for row in table_match.group(1).splitlines():
        cells = [c.strip() for c in row.split("|") if c.strip()]
        if len(cells) == 6 and cells[0] != "ID" and not cells[0].startswith("---"):
            row_count += 1

    return _named_rule_result(
        "epic_clarification_request_has_questions_or_explicit_no_blockers",
        artifact_path,
        row_count > 0,
        f"clarification request lists {row_count} blocking question(s)"
        if row_count > 0
        else "blocking questions table is present but contains no question rows",
        severity="required",
    )


_ALLOWED_BLOCKER_TYPES = {
    "missing-evidence",
    "missing-decision",
    "missing-ownership",
    "missing-user-intent",
}


def _rule_epic_clarification_request_blocker_taxonomy_complete(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> dict[str, str]:
    state = workspace.load_state(workspace_root)
    current_item = state.get("current_item")
    if not current_item:
        return _named_rule_result(
            "epic_clarification_request_blocker_taxonomy_complete",
            artifact_path,
            False,
            "current_item not set for clarification validation",
            severity="required",
        )

    epic_dirs = sorted([d for d in path.iterdir() if d.is_dir() and d.name.startswith(current_item)]) if path.exists() else []
    if not epic_dirs:
        return _named_rule_result(
            "epic_clarification_request_blocker_taxonomy_complete",
            artifact_path,
            False,
            f"no epic directory found for {current_item}",
            severity="required",
        )

    request_path = epic_dirs[0] / "clarification-request.md"
    if not request_path.exists():
        return _named_rule_result(
            "epic_clarification_request_blocker_taxonomy_complete",
            artifact_path,
            False,
            f"{epic_dirs[0].name}/clarification-request.md missing",
            severity="required",
        )

    text = _read_text(request_path)
    if "No blocking questions require clarification for this epic." in text:
        return _named_rule_result(
            "epic_clarification_request_blocker_taxonomy_complete",
            artifact_path,
            True,
            "no blockers text present - taxonomy not required",
            severity="required",
        )

    rows = _section_table_rows(text, "## Blocking Questions")
    failures: list[str] = []
    checked = 0
    for row in rows:
        if len(row) < 8 or not row[0].startswith(("UIQ-", "OQ-", "SDQ-")):
            continue
        checked += 1
        blocker_type = row[3].strip().lower()
        why_now = row[5].strip()
        blocks_artifact = row[6].strip()
        if blocker_type not in _ALLOWED_BLOCKER_TYPES:
            failures.append(f"{row[0]} invalid blocker type '{row[3].strip()}'")
        if not _cell_is_populated(why_now):
            failures.append(f"{row[0]} missing 'Why It Matters Now'")
        if not _cell_is_populated(blocks_artifact):
            failures.append(f"{row[0]} missing 'Blocks Next Artifact'")

    return _named_rule_result(
        "epic_clarification_request_blocker_taxonomy_complete",
        artifact_path,
        checked > 0 and len(failures) == 0,
        f"epic clarification blocker taxonomy is complete for {checked} question(s)"
        if checked > 0 and len(failures) == 0
        else "; ".join(failures[:6]) if failures else "no blocker rows found to validate",
        severity="required",
    )


def _rule_solution_design_clarification_request_has_questions_or_explicit_no_blockers(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> dict[str, str]:
    if not path.exists():
        return _named_rule_result(
            "solution_design_clarification_request_has_questions_or_explicit_no_blockers",
            artifact_path,
            False,
            "solution design clarification request artifact missing",
            severity="required",
        )

    text = _read_text(path)
    if "No blocking solution design questions require clarification." in text:
        return _named_rule_result(
            "solution_design_clarification_request_has_questions_or_explicit_no_blockers",
            artifact_path,
            True,
            "clarification request explicitly states no blocking solution design questions remain",
            severity="required",
        )

    table_match = re.search(r"## Blocking Questions\s*\n((?:\|.*\n)+)", text)
    if not table_match:
        return _named_rule_result(
            "solution_design_clarification_request_has_questions_or_explicit_no_blockers",
            artifact_path,
            False,
            "clarification request has neither explicit no-blockers text nor a blocking questions table",
            severity="required",
        )

    row_count = 0
    for row in table_match.group(1).splitlines():
        cells = [c.strip() for c in row.split("|") if c.strip()]
        if len(cells) == 6 and cells[0] != "ID" and not cells[0].startswith("---"):
            row_count += 1

    return _named_rule_result(
        "solution_design_clarification_request_has_questions_or_explicit_no_blockers",
        artifact_path,
        row_count > 0,
        f"clarification request lists {row_count} blocking solution design question(s)"
        if row_count > 0
        else "blocking questions table is present but contains no question rows",
        severity="required",
    )


def _rule_solution_design_clarification_request_blocker_taxonomy_complete(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> dict[str, str]:
    if not path.exists():
        return _named_rule_result(
            "solution_design_clarification_request_blocker_taxonomy_complete",
            artifact_path,
            False,
            "solution design clarification request artifact missing",
            severity="required",
        )

    text = _read_text(path)
    if "No blocking solution design questions require clarification." in text:
        return _named_rule_result(
            "solution_design_clarification_request_blocker_taxonomy_complete",
            artifact_path,
            True,
            "no blockers text present - taxonomy not required",
            severity="required",
        )

    rows = _section_table_rows(text, "## Blocking Questions")
    failures: list[str] = []
    checked = 0
    for row in rows:
        if len(row) < 8 or not row[0].startswith("SDQ-"):
            continue
        checked += 1
        blocker_type = row[3].strip().lower()
        why_now = row[5].strip()
        blocks_artifact = row[6].strip()
        if blocker_type not in _ALLOWED_BLOCKER_TYPES:
            failures.append(f"{row[0]} invalid blocker type '{row[3].strip()}'")
        if not _cell_is_populated(why_now):
            failures.append(f"{row[0]} missing 'Why It Matters Now'")
        if not _cell_is_populated(blocks_artifact):
            failures.append(f"{row[0]} missing 'Blocks Next Artifact'")

    return _named_rule_result(
        "solution_design_clarification_request_blocker_taxonomy_complete",
        artifact_path,
        checked > 0 and len(failures) == 0,
        f"solution design blocker taxonomy is complete for {checked} question(s)"
        if checked > 0 and len(failures) == 0
        else "; ".join(failures[:6]) if failures else "no blocker rows found to validate",
        severity="required",
    )


def _extract_contract_api_paths(contract_text: str) -> set[tuple[str, str]]:
    """Extract (path, method) tuples from the OpenAPI YAML block in an implementation contract."""
    import yaml as _yaml

    yaml_blocks = re.findall(r"```(?:yaml|yml)\s*\n(.*?)```", contract_text, flags=re.DOTALL)
    paths: set[tuple[str, str]] = set()
    for block in yaml_blocks:
        if "paths:" not in block and "openapi" not in block:
            continue
        try:
            data = _yaml.safe_load(block)
        except Exception:
            continue
        if not isinstance(data, dict):
            continue
        paths_section = data.get("paths", {})
        if not isinstance(paths_section, dict):
            continue
        for path_key, methods in paths_section.items():
            if not isinstance(methods, dict):
                continue
            for method in methods:
                if method.lower() in ("get", "post", "put", "patch", "delete", "head", "options"):
                    paths.add((str(path_key), method.lower()))
    return paths


def _normalize_api_path(path: str) -> str:
    """Normalize path parameters for comparison: /score/{arn} → /score/{}"""
    return re.sub(r"\{[^}]*\}", "{}", path.rstrip("/"))


def _extract_agent_yaml_api_refs(data: dict[str, Any]) -> list[tuple[str, str]]:
    """Extract API path references from an agent YAML's implementation_contract section."""
    refs: list[tuple[str, str]] = []
    impl = data.get("implementation_contract", {})
    if not isinstance(impl, dict):
        return refs

    api = impl.get("api", {})
    if isinstance(api, dict):
        api_path = api.get("path", "")
        api_method = api.get("method", "")
        if api_path and api_method:
            refs.append((str(api_path), str(api_method).lower()))

    for op in impl.get("operations", []):
        if not isinstance(op, dict):
            continue
        target = op.get("target", "")
        path = op.get("path", "")
        method = op.get("method", "")
        if path and method:
            refs.append((str(path), str(method).lower()))
        elif isinstance(target, str) and re.match(r"(GET|POST|PUT|PATCH|DELETE)\s+/", target, re.IGNORECASE):
            parts = target.split(None, 1)
            if len(parts) == 2:
                refs.append((parts[1], parts[0].lower()))

    return refs


def _extract_agent_yaml_operation_refs(data: dict[str, Any]) -> set[str]:
    refs: set[str] = set()
    for path, method in _extract_agent_yaml_api_refs(data):
        refs.add(f"{method.upper()} {_normalize_api_path(path)}")

    impl = data.get("implementation_contract", {})
    if not isinstance(impl, dict):
        return refs

    for op in impl.get("operations", []):
        if not isinstance(op, dict):
            continue
        target = op.get("target", "")
        if isinstance(target, str) and target.strip():
            method_path_match = re.match(r"^\s*(GET|POST|PUT|PATCH|DELETE)\s+(.+?)\s*$", target, flags=re.IGNORECASE)
            if method_path_match:
                refs.add(f"{method_path_match.group(1).upper()} {_normalize_api_path(method_path_match.group(2).strip())}")
            else:
                refs.add(target.strip())
    return refs


def _api_path_matches_any(
    candidate: tuple[str, str],
    contract_paths: set[tuple[str, str]],
) -> bool:
    """Check if a candidate (path, method) matches any contract path."""
    cand_path, cand_method = _normalize_api_path(candidate[0]), candidate[1]
    for contract_path, contract_method in contract_paths:
        norm_contract = _normalize_api_path(contract_path)
        if cand_method == contract_method and cand_path == norm_contract:
            return True
        # Also check base path match (ignoring trailing segments)
        cand_segments = [s for s in cand_path.split("/") if s and s != "{}"]
        contract_segments = [s for s in norm_contract.split("/") if s and s != "{}"]
        if cand_segments and contract_segments and cand_segments[0] == contract_segments[0]:
            if cand_method == contract_method:
                return True
    return False


def _rule_agent_yaml_operations_match_contract(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> dict[str, str]:
    """Validate that story agent YAML operations reference endpoints from the implementation contract."""
    import yaml as _yaml

    if not path.is_dir():
        return _named_rule_result(
            "agent_yaml_operations_match_contract",
            artifact_path,
            True,
            "contract cross-validation applies to epic directories only",
            severity="required",
        )

    mismatches: list[str] = []

    for epic_dir in sorted(d for d in path.iterdir() if d.is_dir() and d.name.startswith("E-")):
        contract_path = epic_dir / "implementation-contract.md"
        if not contract_path.exists():
            continue
        contract_text = _read_text(contract_path)
        contract_paths = _extract_contract_api_paths(contract_text)
        if not contract_paths:
            continue

        stories_dir = epic_dir / "stories"
        if not stories_dir.exists():
            continue

        for yaml_file in sorted(stories_dir.glob("S-*.agent.yaml")):
            try:
                data = _yaml.safe_load(yaml_file.read_text(encoding="utf-8"))
            except Exception:
                continue
            if not isinstance(data, dict):
                continue

            agent_refs = _extract_agent_yaml_api_refs(data)
            for ref_path, ref_method in agent_refs:
                if not _api_path_matches_any((ref_path, ref_method), contract_paths):
                    contract_list = sorted(f"{m.upper()} {p}" for p, m in contract_paths)
                    mismatches.append(
                        f"{yaml_file.name}: {ref_method.upper()} {ref_path} "
                        f"not in contract ({', '.join(contract_list)})"
                    )

    return _named_rule_result(
        "agent_yaml_operations_match_contract",
        artifact_path,
        len(mismatches) == 0,
        "all agent YAML operations reference endpoints from implementation contracts"
        if len(mismatches) == 0
        else "; ".join(mismatches[:5]),
        severity="required",
    )


def _rule_story_agent_contract_semantic_equivalence(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> dict[str, str]:
    if not path.is_dir():
        return _named_rule_result(
            "story_agent_contract_semantic_equivalence",
            artifact_path,
            True,
            "story/agent semantic equivalence applies to epic directories only",
            severity="required",
        )

    failures: list[str] = []

    for epic_dir in sorted(d for d in path.iterdir() if d.is_dir() and d.name.startswith("E-")):
        stories_dir = epic_dir / "stories"
        if not stories_dir.exists():
            continue

        for story_file in sorted(stories_dir.glob("S-*.md")):
            if story_file.name.endswith(".prompt.md"):
                continue
            agent_contract = story_file.with_suffix(".agent.yaml")
            if not agent_contract.exists():
                continue

            try:
                data = _read_yaml(agent_contract)
            except Exception:
                continue
            if not isinstance(data, dict):
                continue

            story_text = _read_text(story_file)
            story_id, story_title = _extract_story_heading_parts(story_text)
            story_type = _story_metadata_value(story_text, "Story Type").lower()
            implemented = _extract_story_requirement_ids(story_text, "## Requirements Implemented")
            referenced = _extract_story_requirement_ids(story_text, "## Requirements Referenced")
            markdown_dependencies = _extract_story_dependencies(story_text)
            markdown_operation_refs = _extract_story_markdown_operation_refs(story_text)
            yaml_operation_refs = _extract_agent_yaml_operation_refs(data)

            yaml_title = str(data.get("title") or "").strip()
            yaml_story_type = str(data.get("story_type") or "").strip().lower()
            yaml_implemented = [
                str(item).strip()
                for item in (data.get("requirements_implemented") or [])
                if isinstance(item, str) and item.strip()
            ]
            yaml_referenced = [
                str(item).strip()
                for item in (data.get("requirements_referenced") or [])
                if isinstance(item, str) and item.strip()
            ]
            yaml_dependencies = []
            for dep in data.get("depends_on") or []:
                if isinstance(dep, dict):
                    dep_id = str(dep.get("story_id") or "").strip()
                    if dep_id:
                        yaml_dependencies.append(dep_id)

            pair_label = f"{epic_dir.name}/{story_file.name}"
            pair_failures: list[str] = []

            if story_id and str(data.get("story_id") or "").strip() != story_id:
                pair_failures.append(f"story_id markdown={story_id} yaml={data.get('story_id')}")

            if story_title and _normalize_text(yaml_title) != _normalize_text(story_title):
                pair_failures.append(f"title markdown='{story_title}' yaml='{yaml_title}'")

            if story_type and yaml_story_type != story_type:
                pair_failures.append(f"story_type markdown={story_type} yaml={yaml_story_type or 'missing'}")

            if implemented != yaml_implemented:
                pair_failures.append(
                    f"requirements_implemented markdown={implemented} yaml={yaml_implemented}"
                )

            if referenced != yaml_referenced:
                pair_failures.append(
                    f"requirements_referenced markdown={referenced} yaml={yaml_referenced}"
                )

            if markdown_dependencies != yaml_dependencies:
                pair_failures.append(
                    f"dependencies markdown={markdown_dependencies} yaml={yaml_dependencies}"
                )

            if yaml_operation_refs and markdown_operation_refs and not yaml_operation_refs.issubset(markdown_operation_refs):
                missing_refs = sorted(yaml_operation_refs - markdown_operation_refs)
                pair_failures.append(
                    f"operations missing from markdown context: {missing_refs}"
                )

            if pair_failures:
                failures.append(f"{pair_label}: " + ", ".join(pair_failures))

    return _named_rule_result(
        "story_agent_contract_semantic_equivalence",
        artifact_path,
        len(failures) == 0,
        "all story markdown and agent YAML pairs are semantically aligned"
        if len(failures) == 0
        else "; ".join(failures[:5]),
        severity="required",
    )


def _rule_epic_coding_readiness(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> dict[str, str]:
    """Composite gate: is this epic ready for a coding agent?"""
    import yaml as _yaml

    if not path.is_dir():
        return _named_rule_result(
            "epic_coding_readiness",
            artifact_path,
            True,
            "coding readiness applies to epic directories only",
            severity="required",
        )

    canonical = _canonical_requirements(workspace_root)
    failures: list[str] = []

    for epic_dir in sorted(d for d in path.iterdir() if d.is_dir() and d.name.startswith("E-")):
        epic_label = epic_dir.name

        # 1. Contracts complete
        contract_path = epic_dir / "implementation-contract.md"
        if not contract_path.exists():
            failures.append(f"{epic_label}: missing implementation-contract.md")
            continue
        contract_text = _read_text(contract_path)
        has_data = bool(re.search(r"^##\s+Data Entities", contract_text, re.MULTILINE))
        has_api = bool(re.search(r"^##\s+API Surface", contract_text, re.MULTILINE))
        has_events = bool(re.search(r"^##\s+Events", contract_text, re.MULTILINE))
        if not (has_data or has_api or has_events):
            failures.append(f"{epic_label}: contract lacks Data Entities, API Surface, and Events sections")

        # 2. No unresolved blockers
        oq_block = _section_block(contract_text, "## Open Design Questions") or _section_block(contract_text, "## Open Questions")
        if oq_block:
            blocking_rows = re.findall(
                r"\|\s*(?:OQ|ODQ)-\d+\s*\|[^|]*\|[^|]*(?:implementation\s*start|before\s*coding)[^|]*\|",
                oq_block, re.IGNORECASE,
            )
            if blocking_rows:
                failures.append(
                    f"{epic_label}: {len(blocking_rows)} open question(s) block implementation start"
                )

        # 3. Stories have implementation targets
        stories_dir = epic_dir / "stories"
        if not stories_dir or not stories_dir.exists():
            continue

        contract_paths = _extract_contract_api_paths(contract_text)
        seen_endpoints: dict[str, list[str]] = {}

        for yaml_file in sorted(stories_dir.glob("S-*.agent.yaml")):
            try:
                data = _yaml.safe_load(yaml_file.read_text(encoding="utf-8"))
            except Exception:
                continue
            if not isinstance(data, dict):
                continue

            impl = data.get("implementation_contract", {})
            if not isinstance(impl, dict):
                failures.append(f"{epic_label}/{yaml_file.name}: missing implementation_contract")
                continue

            components = impl.get("touched_components", [])
            if not components or not isinstance(components, list):
                failures.append(f"{epic_label}/{yaml_file.name}: no touched_components")

            operations = impl.get("operations", [])
            if not operations or not isinstance(operations, list):
                failures.append(f"{epic_label}/{yaml_file.name}: no operations")

            # 4. No conflicting endpoints
            agent_refs = _extract_agent_yaml_api_refs(data)
            for ref_path, ref_method in agent_refs:
                key = f"{ref_method.upper()} {_normalize_api_path(ref_path)}"
                seen_endpoints.setdefault(key, []).append(yaml_file.name)

        for endpoint, owners in seen_endpoints.items():
            if len(owners) > 2:
                failures.append(
                    f"{epic_label}: endpoint {endpoint} claimed by {len(owners)} stories: {owners[:3]}"
                )

    return _named_rule_result(
        "epic_coding_readiness",
        artifact_path,
        len(failures) == 0,
        "all epics pass coding readiness checks"
        if len(failures) == 0
        else "; ".join(failures[:8]),
        severity="required",
    )


def _extract_skeleton_epic_titles(workspace_root: Path) -> dict[str, str]:
    """Parse delivery-skeleton.md for ``### E-NNN — Title`` headings.

    Returns ``{epic_id: canonical_title}``.
    """
    skeleton_path = workspace_root / "planning" / "delivery-skeleton.md"
    if not skeleton_path.exists():
        return {}
    text = _read_text(skeleton_path)
    result: dict[str, str] = {}
    for match in re.finditer(r"^###\s+(E-\d{3})\s+[—-]\s+(.+?)$", text, flags=re.MULTILINE):
        result[match.group(1)] = match.group(2).strip()
    return result


def _title_to_slug(title: str) -> str:
    """Normalize a title to a lowercase hyphenated slug for folder comparison."""
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower())
    return slug.strip("-")


def _rule_epic_identity_matches_skeleton(
    path: Path,
    workspace_root: Path,
    action: dict[str, Any],
    artifact_path: str,
    base_checks: list[dict[str, str]],
) -> dict[str, str]:
    if not path.is_dir():
        return _named_rule_result(
            "epic_identity_matches_skeleton",
            artifact_path,
            True,
            "epic identity check applies to epic directories only",
            severity="required",
        )

    skeleton_titles = _extract_skeleton_epic_titles(workspace_root)
    if not skeleton_titles:
        return _named_rule_result(
            "epic_identity_matches_skeleton",
            artifact_path,
            True,
            "no skeleton found — skipping epic identity check",
            severity="required",
        )

    failures: list[str] = []
    for epic_dir in sorted(d for d in path.iterdir() if d.is_dir() and d.name.startswith("E-")):
        epic_id_match = re.match(r"(E-\d{3})", epic_dir.name)
        if not epic_id_match:
            continue
        epic_id = epic_id_match.group(1)
        canonical_title = skeleton_titles.get(epic_id)
        if not canonical_title:
            continue

        folder_slug = epic_dir.name[len(epic_id):].lstrip("-")
        expected_slug = _title_to_slug(canonical_title)
        if folder_slug and expected_slug:
            # Check that the folder slug starts with the first 3 significant words
            expected_words = expected_slug.split("-")[:3]
            folder_words = folder_slug.split("-")[:3]
            if expected_words != folder_words:
                failures.append(
                    f"{epic_id}: folder slug '{folder_slug}' does not match "
                    f"skeleton title '{canonical_title}' (expected slug starting with '{'-'.join(expected_words)}')"
                )

        epic_md = epic_dir / "epic.md"
        if epic_md.exists():
            heading = _read_text(epic_md).split("\n", 1)[0]
            if canonical_title and _normalize_text(canonical_title) not in _normalize_text(heading):
                failures.append(
                    f"{epic_id}: epic.md heading '{heading.strip()}' does not contain "
                    f"canonical title '{canonical_title}'"
                )

    return _named_rule_result(
        "epic_identity_matches_skeleton",
        artifact_path,
        len(failures) == 0,
        "all epic folders and headings match skeleton titles"
        if len(failures) == 0
        else "; ".join(failures[:5]),
        severity="required",
    )


NAMED_RULES: dict[str, NamedRuleValidator] = {
    "requirement_has_id": _rule_requirement_has_id,
    "source_brs_ids_preserved": _rule_source_brs_ids_preserved,
    "atomic_requirements_summary_matches_catalog": _rule_atomic_requirements_summary_matches_catalog,
    "atomic_requirements_derivation_visible": _rule_atomic_requirements_derivation_visible,
    "atomic_requirements_decomposition_traceable": _rule_atomic_requirements_decomposition_traceable,
    "atomic_requirements_direct_inferred_summary_matches": _rule_atomic_requirements_direct_inferred_summary_matches,
    "requirement_is_testable": _rule_requirement_is_testable,
    "all_source_requirements_present": _rule_all_source_requirements_present,
    "no_unknown_requirement_references": _rule_no_unknown_requirement_references,
    "requirement_title_consistency": _rule_requirement_title_consistency,
    "requirement_semantics_preserved": _rule_requirement_semantics_preserved,
    "epic_traceability_basis_visible": _rule_epic_traceability_basis_visible,
    "story_linked_requirements_basis_visible": _rule_story_linked_requirements_basis_visible,
    "open_questions_propagated": _rule_open_questions_propagated,
    "coverage_claim_matches_evidence": _rule_coverage_claim_matches_evidence,
    "coverage_classifications_acceptable": _rule_coverage_classifications_acceptable,
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
    "delivery_skeleton_requirement_basis_visible": _rule_delivery_skeleton_requirement_basis_visible,
    "all_components_from_architecture_review_present": _rule_all_components_from_architecture_review_present,
    "all_functional_requirements_mapped": _rule_all_functional_requirements_mapped,
    "all_impacted_components_have_decisions": _rule_all_impacted_components_have_decisions,
    "solution_decisions_traceability_complete": _rule_solution_decisions_traceability_complete,
    "solution_decisions_inferred_requirements_visible": _rule_solution_decisions_inferred_requirements_visible,
    "ui_spec_confirmed_pages_have_page_sections": _rule_ui_spec_confirmed_pages_have_page_sections,
    "ui_spec_confirmed_pages_have_required_subsections": _rule_ui_spec_confirmed_pages_have_required_subsections,
    "ui_spec_no_confirmed_when_blockers_exist": _rule_ui_spec_no_confirmed_when_blockers_exist,
    "ui_spec_data_binding_contract_mode_present": _rule_ui_spec_data_binding_contract_mode_present,
    "ui_spec_every_inferred_has_open_question": _rule_ui_spec_every_inferred_has_open_question,
    "ui_spec_open_questions_have_required_before": _rule_ui_spec_open_questions_have_required_before,
    "ui_spec_shared_components_match_page_fields": _rule_ui_spec_shared_components_match_page_fields,
    "ui_spec_no_encoding_mojibake": _rule_ui_spec_no_encoding_mojibake,
    "epic_clarification_request_has_questions_or_explicit_no_blockers": _rule_epic_clarification_request_has_questions_or_explicit_no_blockers,
    "epic_clarification_request_blocker_taxonomy_complete": _rule_epic_clarification_request_blocker_taxonomy_complete,
    "solution_design_clarification_request_has_questions_or_explicit_no_blockers": _rule_solution_design_clarification_request_has_questions_or_explicit_no_blockers,
    "solution_design_clarification_request_blocker_taxonomy_complete": _rule_solution_design_clarification_request_blocker_taxonomy_complete,
    "epic_identity_matches_skeleton": _rule_epic_identity_matches_skeleton,
    "story_agent_contract_semantic_equivalence": _rule_story_agent_contract_semantic_equivalence,
    "agent_yaml_operations_match_contract": _rule_agent_yaml_operations_match_contract,
    "epic_coding_readiness": _rule_epic_coding_readiness,
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
    active_action = state.get("active_action") or ""
    _PRE_STORY_ACTIONS = {
        "create-epic-shells",
        "resolve-epic-open-questions",
        "gate-epic-clarification",
    }
    action_status = state.get("action_status", {})
    inferred_action = active_action
    if not inferred_action:
        for pre_action in _PRE_STORY_ACTIONS:
            if action_status.get(pre_action) == "in_progress":
                inferred_action = pre_action
                break
    skip_story_checks = inferred_action in _PRE_STORY_ACTIONS

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

    if skip_story_checks:
        for epic_dir in epic_dirs:
            stories_dir = epic_dir / "stories"
            if stories_dir.exists() and any(stories_dir.glob("S-*.md")):
                story_files = sorted(f.name for f in stories_dir.glob("S-*.md") if not f.name.endswith(".prompt.md"))
                checks.append(
                    _result(
                        "no_premature_story_files",
                        epic_dir.name,
                        True,
                        f"advisory: {epic_dir.name}/stories/ contains {len(story_files)} story file(s) "
                        f"but the current action ({inferred_action}) must not create stories — "
                        f"these will be overwritten by create-epic-stories",
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

            if epic_reqs and not skip_story_checks:
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

        # Check story count against feature count from delivery skeleton
        if epic_id_str and skeleton_path.exists() and not skip_story_checks:
            skeleton_text_for_features = _read_text(skeleton_path) if "skeleton_text" not in dir() else skeleton_text
            epic_section = re.search(
                rf"### {re.escape(epic_id_str)}\b.*?(?=^### E-\d{{3}}|\Z)",
                skeleton_text_for_features,
                flags=re.MULTILINE | re.DOTALL,
            )
            if epic_section:
                feature_count = len(re.findall(
                    r"^\|\s*F-\d{3}\s*\|",
                    epic_section.group(0),
                    flags=re.MULTILINE,
                ))
                story_count = len(sorted(
                    [f for f in (epic_dir / "stories").glob("S-*.md") if not f.name.endswith(".prompt.md")]
                )) if (epic_dir / "stories").exists() else 0

                if feature_count > 0:
                    checks.append(
                        _result(
                            "stories_match_feature_count",
                            label,
                            story_count >= feature_count,
                            f"{label}: {story_count} stories for {feature_count} features"
                            if story_count >= feature_count
                            else f"{label}: only {story_count} story(ies) for {feature_count} features — "
                                 f"each feature (F-NNN) must produce at least one story",
                        )
                    )

        if skip_story_checks:
            continue

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

                _st_match = re.search(r"\|\s*Story Type\s*\|\s*([^|]+)\|", text, re.IGNORECASE)
                _st_value = _st_match.group(1).strip().lower() if _st_match else ""
                _is_spike = _st_value in ("spike", "poc", "e2e", "exploration")

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

                if _is_spike:
                    min_scenarios = 1
                    complexity = "spike/poc"
                elif has_integration or has_state_machine:
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

                story_type_match = re.search(r"\|\s*Story Type\s*\|\s*([^|]+)\|", stext, re.IGNORECASE)
                story_type_value = story_type_match.group(1).strip().lower() if story_type_match else ""
                checks.append(
                    _result(
                        "story_has_story_type",
                        slbl,
                        bool(story_type_match) and len(story_type_value) > 2,
                        f"{story_file.name}: story type declared as '{story_type_value}'"
                        if story_type_match and len(story_type_value) > 2
                        else f"{story_file.name}: missing Story Type field in metadata - must declare a concrete story archetype",
                    )
                )
                is_spike = story_type_value in ("spike", "poc", "e2e", "exploration")

                has_req_implemented = bool(re.search(r"(?i)##\s*requirements implemented", stext))
                checks.append(
                    _result(
                        "story_has_requirements_implemented",
                        slbl,
                        has_req_implemented,
                        f"{story_file.name}: has Requirements Implemented section"
                        if has_req_implemented
                        else f"{story_file.name}: missing '## Requirements Implemented' - must declare which requirements this story directly implements",
                    )
                )

                has_req_referenced = bool(re.search(r"(?i)##\s*requirements referenced", stext))
                checks.append(
                    _result(
                        "story_has_requirements_referenced",
                        slbl,
                        has_req_referenced,
                        f"{story_file.name}: has Requirements Referenced section"
                        if has_req_referenced
                        else f"{story_file.name}: missing '## Requirements Referenced' - must declare requirements mentioned or depended on but not owned",
                    )
                )

                has_in_scope = bool(re.search(r"(?i)##\s*in scope", stext))
                checks.append(
                    _result(
                        "story_has_in_scope",
                        slbl,
                        has_in_scope,
                        f"{story_file.name}: has In Scope section"
                        if has_in_scope
                        else f"{story_file.name}: missing '## In Scope' - must list concrete behavior this story implements",
                    )
                )

                story_req_ids = set(re.findall(r"(?:FR|REQ|NFR)-\d{3}", stext))
                if not is_spike and len(story_req_ids) > 5:
                    checks.append(
                        _result(
                            "story_invest_small",
                            slbl,
                            False,
                            f"{story_file.name}: covers {len(story_req_ids)} requirements — likely too large (INVEST: Small). Consider splitting.",
                        )
                    )

                if not is_spike and layers_match:
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

                if not is_spike:
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

                has_dependency_contracts = bool(re.search(r"(?i)##\s*dependency contracts", stext2))
                checks.append(
                    _result(
                        "story_has_dependency_contracts",
                        slbl2,
                        has_dependency_contracts,
                        f"{story_file.name}: has Dependency Contracts section"
                        if has_dependency_contracts
                        else f"{story_file.name}: missing '## Dependency Contracts' - must declare consumed contracts when dependencies exist",
                    )
                )

                has_required_tests = bool(re.search(r"(?i)##\s*required tests", stext2))
                checks.append(
                    _result(
                        "story_has_required_tests",
                        slbl2,
                        has_required_tests,
                        f"{story_file.name}: has Required Tests section"
                        if has_required_tests
                        else f"{story_file.name}: missing '## Required Tests' - must state concrete minimum tests for completion",
                    )
                )

                agent_contract = story_file.with_suffix(".agent.yaml")
                checks.append(
                    _result(
                        "story_has_agent_contract",
                        slbl2,
                        agent_contract.exists(),
                        f"{story_file.name}: paired agent contract present ({agent_contract.name})"
                        if agent_contract.exists()
                        else f"{story_file.name}: missing paired agent contract {agent_contract.name}",
                    )
                )
                if agent_contract.exists():
                    checks.extend(_validate_story_agent_contract_file(agent_contract, story_file, stext2))

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


def _validate_ui_specification(path: Path, workspace_root: Path) -> list[dict[str, str]]:
    text = _read_text(path)
    checks = []
    checks.extend(_non_empty_file(path))

    if "no frontend applications identified" in text.lower():
        checks.append(
            _result(
                "ui_spec_skip_acknowledged",
                path.name,
                True,
                "no frontend applications — UI spec correctly minimal",
            )
        )
        return checks

    landscape_path = workspace_root / "architecture" / "technical-landscape.md"
    if landscape_path.exists():
        landscape_text = _read_text(landscape_path).lower()
        frontend_keywords = [
            "portal", "dashboard", "ui", "web app", "frontend",
            "next.js", "react", "angular", "vue", "static web app",
        ]
        frontend_apps: list[str] = []
        for line in _read_text(landscape_path).splitlines():
            if any(kw in line.lower() for kw in frontend_keywords):
                name_match = re.match(r"^[-*]\s*(.+?)(?:\s*[—:|\(]|$)", line.strip())
                if name_match:
                    frontend_apps.append(name_match.group(1).strip())
                table_match = re.match(r"^\|\s*(.+?)\s*\|", line.strip())
                if table_match and not name_match:
                    candidate = table_match.group(1).strip()
                    if candidate.lower() not in {"component", "type", "repository", "technology", "status"}:
                        frontend_apps.append(candidate)

        if frontend_apps:
            text_lower = text.lower()
            covered = [app for app in frontend_apps if app.lower() in text_lower]
            missing = [app for app in frontend_apps if app.lower() not in text_lower]
            checks.append(
                _result(
                    "ui_spec_covers_all_apps",
                    path.name,
                    len(missing) == 0,
                    f"UI spec covers all {len(frontend_apps)} frontend apps from technical landscape"
                    if len(missing) == 0
                    else f"UI spec missing apps: {', '.join(missing[:5])} ({len(covered)}/{len(frontend_apps)} covered)",
                )
            )

    app_sections = re.findall(r"^##\s+(?:Application:\s*|Per Application:\s*)(.+)$", text, flags=re.MULTILINE)
    if not app_sections:
        app_sections = re.findall(r"^##\s+(.+?)\s*(?:Portal|Dashboard|App|UI)\s*$", text, flags=re.MULTILINE | re.IGNORECASE)
    checks.append(
        _result(
            "ui_spec_has_app_sections",
            path.name,
            len(app_sections) >= 1,
            f"UI spec defines {len(app_sections)} application section(s)"
            if app_sections
            else "UI spec has no application sections — expected '## Application: ...' or named app headings",
        )
    )

    page_sections = re.findall(r"^###\s+Page:\s*(.+)$", text, flags=re.MULTILINE)
    checks.append(
        _result(
            "ui_spec_has_pages",
            path.name,
            len(page_sections) >= 2,
            f"UI spec defines {len(page_sections)} page(s)"
            if len(page_sections) >= 2
            else f"UI spec has only {len(page_sections)} page(s) — a multi-app initiative needs more page definitions",
        )
    )

    has_routes = bool(re.search(r"(?:Route|route).*?/[a-z]", text))
    checks.append(
        _result(
            "ui_spec_has_routes",
            path.name,
            has_routes,
            "UI spec includes route definitions"
            if has_routes
            else "UI spec has no route definitions — pages must specify their URL routes",
        )
    )

    has_form_fields = bool(re.search(r"\|\s*(?:Field|field)\s*\|", text) and re.search(r"\|\s*(?:Type|type)\s*\|", text))
    checks.append(
        _result(
            "ui_spec_has_form_fields",
            path.name,
            has_form_fields,
            "UI spec includes form field definitions with types"
            if has_form_fields
            else "UI spec has no form field table — forms must specify fields with types and validation",
        )
    )

    has_states = bool(re.search(r"(?i)(?:loading|empty|error|success)\s*(?:→|->|:|\|)", text))
    checks.append(
        _result(
            "ui_spec_has_states",
            path.name,
            has_states,
            "UI spec defines page/component states"
            if has_states
            else "UI spec missing state definitions — each page must define loading/error/success behavior",
        )
    )

    has_data_binding = bool(re.search(r"(?i)(?:data binding|endpoint|api|/api/v\d)", text))
    checks.append(
        _result(
            "ui_spec_has_data_binding",
            path.name,
            has_data_binding,
            "UI spec includes data binding / API endpoint references"
            if has_data_binding
            else "UI spec missing data binding — pages must specify which API endpoints they call",
        )
    )

    has_traceability = bool(re.search(r"(?i)(?:traceability|FR-\d{3}.*(?:page|component|app))", text))
    checks.append(
        _result(
            "ui_spec_has_traceability",
            path.name,
            has_traceability,
            "UI spec includes FR traceability"
            if has_traceability
            else "UI spec missing traceability — every UI-bearing FR must map to a page/component",
        )
    )

    fr_refs = set(re.findall(r"(?:FR|REQ)-\d{3}", text))
    checks.append(
        _result(
            "ui_spec_covers_multiple_frs",
            path.name,
            len(fr_refs) >= 3,
            f"UI spec references {len(fr_refs)} requirements"
            if len(fr_refs) >= 3
            else f"UI spec only references {len(fr_refs)} requirement(s) — should cover all UI-bearing FRs",
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
    "architecture/ui-specification.md": _validate_ui_specification,
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


def validate_action(
    workspace_root: Path,
    state: dict | None = None,
    action_id: str | None = None,
) -> dict:
    """Run validation for the active action. Returns the validation result dict.

    This is the pure logic extracted from ``run()`` so that other commands
    (e.g. ``finalize-action``) can invoke validation programmatically.
    """
    if state is None:
        state = workspace.load_state(workspace_root)
    if action_id is None:
        action_id = workspace.read_action_id_from_state_or_args(state, None)

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

    return {
        "overall": "pass" if not failures else "fail",
        "action_id": action_id,
        "artifact_path": artifact_paths[0] if artifact_paths else None,
        "checks": checks,
        "named_rule_results": named_rule_results,
        "failures": failures,
        "advisories": advisories,
    }


def run(args: object) -> None:
    workspace_root = workspace.resolve_workspace_root(args.workspace_root)
    state = workspace.load_state(workspace_root)
    action_id = workspace.read_action_id_from_state_or_args(state, getattr(args, "action_id", None))

    phase_error = workspace.check_lifecycle_phase(state, workspace.LIFECYCLE_DISPATCHED, "validate-artifact")
    if phase_error:
        raise RuntimeError(phase_error)

    result = validate_action(workspace_root, state, action_id)

    workspace.save_yaml_file(
        workspace.resolve_output_path("validate-artifact", workspace_root, args.output),
        result,
    )

    workspace.advance_lifecycle_phase(state, workspace.LIFECYCLE_VALIDATED)
    workspace.save_state(workspace_root, state)

    workspace.append_execution_log(
        workspace_root,
        command="validate-artifact",
        overall=result["overall"],
        action_id=action_id,
        details={
            "artifact_path": result["artifact_path"],
            "failure_count": len(result["failures"]),
            "failures": result["failures"],
        },
    )
