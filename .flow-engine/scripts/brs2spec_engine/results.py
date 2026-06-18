"""Result file validation — schema checks, read_evidence counts, contradiction detection."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
    _YAML_AVAILABLE = True
except ImportError:
    _YAML_AVAILABLE = False

try:
    import json
    _JSON_AVAILABLE = True
except ImportError:
    _JSON_AVAILABLE = False


class ResultValidationError(Exception):
    pass


def load_yaml_file(path: Path) -> Any:
    if not path.exists():
        raise ResultValidationError(f"File not found: {path}")
    text = path.read_text(encoding="utf-8")
    if _YAML_AVAILABLE:
        return yaml.safe_load(text)
    raise ResultValidationError("PyYAML is not installed. Run: pip install pyyaml")


def validate_result(
    result_path: Path,
    event: dict,
    output_path: Path,
) -> dict:
    """
    Validate the result file contract before Step 17 (move to done/failed).
    Writes structured output to output_path.
    Returns the check bundle dict.
    """
    checks: list[dict] = []

    try:
        result = load_yaml_file(result_path)
    except ResultValidationError as e:
        return _write_output(output_path, "validate-result", checks=[
            _check("result_file_readable", "fail", str(e))
        ], overall="fail")

    if not isinstance(result, dict):
        return _write_output(output_path, "validate-result", checks=[
            _check("result_file_readable", "fail", "Result file is not a YAML mapping")
        ], overall="fail")

    # check 1 — status
    status = result.get("status")
    if status in ("pass", "fail"):
        checks.append(_check("status_field_valid", "pass", f"status: {status}"))
    elif status is None:
        checks.append(_check("status_field_valid", "fail", "status field is missing"))
    else:
        checks.append(_check(
            "status_field_valid", "fail",
            f"status is '{status}' — must be 'pass' or 'fail'"
        ))

    # check 2 — event_id
    event_id = result.get("event_id", "")
    expected_id = event.get("event_id", "")
    if re.match(r"^EVT-\d{5}$", str(event_id)) and event_id == expected_id:
        checks.append(_check("event_id_valid", "pass", f"event_id: {event_id}"))
    else:
        checks.append(_check(
            "event_id_valid", "fail",
            f"event_id '{event_id}' missing or does not match expected '{expected_id}'"
        ))

    # check 3 — completed_at
    if result.get("completed_at"):
        checks.append(_check("completed_at_present", "pass", str(result["completed_at"])))
    else:
        checks.append(_check("completed_at_present", "fail", "completed_at is missing"))

    # check 4 — artifacts_written
    artifacts = result.get("artifacts_written")
    if isinstance(artifacts, list):
        checks.append(_check(
            "artifacts_written_valid", "pass",
            f"{len(artifacts)} artifact(s) listed"
        ))
        # suspicious: pass with no artifacts (only ok for WAIT_HUMAN / ROUTE_INITIATIVE)
        event_type = event.get("event_type", "")
        if status == "pass" and len(artifacts) == 0 and event_type not in (
            "WAIT_HUMAN", "ROUTE_INITIATIVE"
        ):
            checks.append(_check(
                "artifacts_written_nonempty", "fail",
                f"status is pass but artifacts_written is empty for event_type {event_type}"
            ))
        else:
            checks.append(_check("artifacts_written_nonempty", "pass", "ok"))
    else:
        checks.append(_check(
            "artifacts_written_valid", "fail",
            "artifacts_written is missing or not a list"
        ))

    # check 5 — read_evidence count
    read_from: list = event.get("read_from") or []
    read_evidence: list = result.get("read_evidence") or []
    if read_from:
        expected_count = len(read_from)
        actual_count = len(read_evidence)
        if actual_count >= expected_count:
            checks.append(_check(
                "read_evidence_count", "pass",
                f"read_from has {expected_count} entries; read_evidence has {actual_count}"
            ))
        else:
            checks.append(_check(
                "read_evidence_count", "fail",
                f"read_from has {expected_count} entries but read_evidence has {actual_count}. "
                f"Step 10 was not fully executed."
            ))
    else:
        checks.append(_check("read_evidence_count", "pass", "no read_from entries — skipped"))

    # check 6 — validation_notes count
    must_include: list = event.get("must_include") or []
    has_natural_language = bool(
        event.get("validation_rules", {}) and
        event["validation_rules"].get("natural_language")
    )
    validation_notes: list = result.get("validation_notes") or []
    expected_notes = len(must_include) + (1 if has_natural_language else 0)
    if expected_notes > 0:
        actual_notes = len(validation_notes)
        if actual_notes >= expected_notes:
            checks.append(_check(
                "validation_notes_count", "pass",
                f"expected {expected_notes}, found {actual_notes}"
            ))
        else:
            checks.append(_check(
                "validation_notes_count", "fail",
                f"event has {len(must_include)} must_include item(s) "
                f"{'+ natural_language rule ' if has_natural_language else ''}"
                f"but validation_notes has only {actual_notes} entries"
            ))
    else:
        checks.append(_check("validation_notes_count", "pass", "no must_include — skipped"))

    # check 5b — read_evidence first_nonempty_line present for existing files
    missing_fnl: list[str] = []
    for entry in read_evidence:
        if not isinstance(entry, dict):
            continue
        if entry.get("exists") is True and "matched_files" not in entry:
            if not entry.get("first_nonempty_line"):
                missing_fnl.append(str(entry.get("path", "?")))
    if missing_fnl:
        checks.append(_check(
            "read_evidence_first_nonempty_line", "fail",
            f"read_evidence entries for existing files are missing first_nonempty_line: "
            + ", ".join(missing_fnl)
            + ". This field is required — it enables contradiction detection."
        ))
    else:
        checks.append(_check(
            "read_evidence_first_nonempty_line", "pass",
            "all read_evidence entries for existing files have first_nonempty_line"
        ))

    # check 6b — validation_notes rule anchoring
    # Each validation_notes entry must contain a meaningful substring of its must_include item.
    # Freehand labels ("FR COMPLETENESS") that share no words with the must_include text fail.
    if must_include and validation_notes:
        anchoring_failures = _check_validation_notes_anchoring(must_include, validation_notes)
        if anchoring_failures:
            checks.append(_check(
                "validation_notes_anchored", "fail",
                f"{len(anchoring_failures)} validation_notes entry(ies) do not match any "
                f"must_include item. Entries must quote or paraphrase the must_include text — "
                f"freehand labels are not acceptable. Unmatched entries: "
                + "; ".join(f'"{e}"' for e in anchoring_failures)
            ))
        else:
            checks.append(_check(
                "validation_notes_anchored", "pass",
                f"all {len(must_include)} must_include items have a matching validation_notes entry"
            ))
    else:
        checks.append(_check("validation_notes_anchored", "pass", "no must_include — skipped"))

    # check 7a — fabricated failure: content-quality claim with no read_evidence
    fabricated = _check_fabricated_failure(result, read_from, read_evidence)
    if fabricated:
        checks.append(_check("no_fabricated_failure", "fail", fabricated))
    else:
        checks.append(_check("no_fabricated_failure", "pass", "no fabricated failure detected"))

    # check 7b — contradiction: exists in read_evidence but failure claims missing
    contradiction = _check_contradiction(result, read_evidence)
    if contradiction:
        checks.append(_check("no_contradiction", "fail", contradiction))
    else:
        checks.append(_check("no_contradiction", "pass", "no contradictions detected"))

    overall = "pass" if all(c["result"] == "pass" for c in checks) else "fail"
    return _write_output(output_path, "validate-result", checks, overall)


def _check_validation_notes_anchoring(must_include: list, validation_notes: list) -> list[str]:
    """
    For each validation_notes entry, verify its rule: field shares meaningful tokens
    with at least one must_include item. Returns list of unmatched rule: values.

    Matching strategy (lenient — avoids false positives from paraphrasing):
    - Normalise both strings to lowercase tokens (words ≥ 4 chars, strip punctuation).
    - An entry matches a must_include item if they share at least 2 tokens.
    - If the entry rule: starts with "natural_language:" it is exempt (Step 16 entry).
    """
    import string

    def tokens(text: str) -> set[str]:
        t = text.lower().translate(str.maketrans("", "", string.punctuation))
        return {w for w in t.split() if len(w) >= 4}

    must_token_sets = [tokens(item) for item in must_include]
    unmatched: list[str] = []

    for note in validation_notes:
        if not isinstance(note, dict):
            continue
        rule_text = str(note.get("rule", ""))
        if rule_text.lower().startswith("natural_language"):
            continue  # Step 16 entry — exempt
        rule_tokens = tokens(rule_text)
        matched = any(
            len(rule_tokens & must_tokens) >= 2
            for must_tokens in must_token_sets
        )
        if not matched:
            unmatched.append(rule_text[:80])

    return unmatched


_CONTENT_QUALITY_PHRASES = [
    "no extractable", "brs is empty", "brs has no content",
    "insufficient", "no requirements found", "source file does not contain",
    "input is insufficient", "no content", "no extractable requirements",
    "no extractable content", "source file has no",
]


def _check_fabricated_failure(result: dict, read_from: list, read_evidence: list) -> str:
    """
    Detect fabricated failures: status:fail with a content-quality claim but no read_evidence.
    Returns a description string if fabrication is detected, else empty string.
    """
    if result.get("status") != "fail":
        return ""
    if not read_from:
        return ""
    if read_evidence:
        return ""  # read_evidence present — handled by contradiction check

    reason = str(result.get("failure_reason", "")).lower()
    if not reason:
        return ""

    if any(p in reason for p in _CONTENT_QUALITY_PHRASES):
        return (
            "fabricated failure: failure_reason makes a content-quality claim "
            f"('{result.get('failure_reason', '')}') but read_evidence is absent "
            f"and read_from has {len(read_from)} entries. "
            "Step 10 was not executed — the inputs were never read. "
            "Move event back to pending/ and re-run dispatch-next."
        )
    return ""


def _check_contradiction(result: dict, read_evidence: list[dict]) -> str:
    """
    Detect contradictions between read_evidence and failure_reason.
    Returns a description string if a contradiction is found, else empty string.
    """
    if result.get("status") != "fail":
        return ""
    reason = str(result.get("failure_reason", "")).lower()
    if not reason:
        return ""

    emptiness_phrases = [
        "no extractable", "brs is empty", "brs has no content",
        "insufficient", "no requirements found", "source file does not contain",
        "input is insufficient", "no content",
    ]
    is_emptiness_claim = any(p in reason for p in emptiness_phrases)
    is_missing_claim = "missing" in reason or "not found" in reason or "does not exist" in reason

    for entry in read_evidence:
        if not isinstance(entry, dict):
            continue
        path = entry.get("path", "")
        if not path:
            continue

        if is_emptiness_claim and entry.get("exists") is True:
            lines = entry.get("lines", 0)
            first = entry.get("first_nonempty_line", "")
            if lines > 20:
                return (
                    f"generic emptiness claim rejected: failure_reason claims no content "
                    f"but read_evidence shows '{path}' exists with {lines} lines. "
                    f"First line: '{first}'. Re-run with a specific failure_reason."
                )
            if first:
                return (
                    f"contradictory failure: read_evidence shows first_nonempty_line "
                    f"'{first}' for '{path}' but failure_reason claims the file was empty."
                )

        if is_missing_claim and entry.get("exists") is True:
            return (
                f"contradictory failure: read_evidence shows '{path}' exists "
                f"but failure_reason claims it was missing."
            )

    return ""


def validate_artifact_counts(
    workspace: Path,
    brs_path: Path,
    artifact_path: Path,
    output_path: Path,
) -> dict:
    """
    Compare FR-NNN and NFR-NNN IDs between the BRS source and the produced artifact.
    Writes structured output to output_path.
    """
    checks: list[dict] = []

    brs_frs, brs_nfrs = _extract_ids_from_brs(brs_path)
    art_frs, art_nfrs = _extract_ids_from_artifact(artifact_path)

    missing_frs = sorted(brs_frs - art_frs)
    missing_nfrs = sorted(brs_nfrs - art_nfrs)

    if not missing_frs:
        checks.append(_check(
            "fr_count_match", "pass",
            f"BRS: {len(brs_frs)} FR IDs. Artifact: {len(art_frs)} FR rows. All present."
        ))
    else:
        checks.append(_check(
            "fr_count_match", "fail",
            f"BRS contains {len(brs_frs)} FR IDs but artifact has {len(art_frs)} FR rows. "
            f"Missing: {', '.join(missing_frs)}"
        ))

    if not missing_nfrs:
        checks.append(_check(
            "nfr_count_match", "pass",
            f"BRS: {len(brs_nfrs)} NFR IDs. Artifact: {len(art_nfrs)} NFR rows. All present."
        ))
    else:
        checks.append(_check(
            "nfr_count_match", "fail",
            f"BRS contains {len(brs_nfrs)} NFR IDs but artifact has {len(art_nfrs)} NFR rows. "
            f"Missing: {', '.join(missing_nfrs)}"
        ))

    overall = "pass" if all(c["result"] == "pass" for c in checks) else "fail"
    return _write_output(output_path, "validate-artifact-counts", checks, overall)


def validate_no_placeholders(
    artifact_path: Path,
    output_path: Path,
    allowed_sections: list[str] | None = None,
) -> dict:
    """
    Scan an artifact for placeholder strings outside allowed sections.
    Writes structured output to output_path.
    """
    _PLACEHOLDER_RE = re.compile(
        r"\b(TBD|TODO|PLACEHOLDER)\b|\[fill\s+in\]|\[INSERT\]|\[TBD\]",
        re.IGNORECASE,
    )
    _ALLOWED_HEADERS = {"gaps and questions", "open questions", "open items"}
    if allowed_sections:
        _ALLOWED_HEADERS.update(s.lower() for s in allowed_sections)

    checks: list[dict] = []
    hits: list[str] = []

    text = artifact_path.read_text(encoding="utf-8", errors="replace")
    in_allowed_section = False

    for i, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        # detect section header
        if stripped.startswith("#"):
            header_text = stripped.lstrip("#").strip().lower()
            in_allowed_section = any(h in header_text for h in _ALLOWED_HEADERS)
        if not in_allowed_section and _PLACEHOLDER_RE.search(line):
            hits.append(f"Line {i}: {line.rstrip()}")

    if hits:
        checks.append(_check(
            "no_placeholder_strings", "fail",
            f"Found {len(hits)} placeholder(s):\n" + "\n".join(hits)
        ))
    else:
        checks.append(_check("no_placeholder_strings", "pass", "No placeholder strings found."))

    overall = "pass" if not hits else "fail"
    return _write_output(output_path, "validate-no-placeholders", checks, overall)


def _extract_ids_from_brs(path: Path) -> tuple[set[str], set[str]]:
    """Extract **FR-NNN** and **NFR-NNN** bold IDs from the BRS source."""
    text = path.read_text(encoding="utf-8", errors="replace")
    frs = set(re.findall(r"\*\*(FR-\d+)\*\*", text))
    nfrs = set(re.findall(r"\*\*(NFR-\d+)\*\*", text))
    # also catch table rows like | NFR-001 |
    frs |= set(re.findall(r"(?:^|\|)\s*(FR-\d+)\s*(?:\||$)", text, re.MULTILINE))
    nfrs |= set(re.findall(r"(?:^|\|)\s*(NFR-\d+)\s*(?:\||$)", text, re.MULTILINE))
    return frs, nfrs


def _extract_ids_from_artifact(path: Path) -> tuple[set[str], set[str]]:
    """Extract FR-NNN and NFR-NNN IDs from table rows in the produced artifact."""
    text = path.read_text(encoding="utf-8", errors="replace")
    frs = set(re.findall(r"(?:^|\|)\s*(FR-\d+)\s*(?:\||$)", text, re.MULTILINE))
    nfrs = set(re.findall(r"(?:^|\|)\s*(NFR-\d+)\s*(?:\||$)", text, re.MULTILINE))
    return frs, nfrs


def _check(name: str, result: str, detail: str) -> dict:
    return {"name": name, "result": result, "detail": detail}


def _write_output(
    output_path: Path,
    command: str,
    checks: list[dict],
    overall: str,
) -> dict:
    from datetime import datetime, timezone
    bundle = {
        "command": command,
        "ran_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "checks": checks,
        "overall": overall,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        import yaml
        text = yaml.dump(bundle, default_flow_style=False, allow_unicode=True)
    except ImportError:
        import json
        text = json.dumps(bundle, indent=2)

    output_path.write_text(text, encoding="utf-8")
    return bundle
