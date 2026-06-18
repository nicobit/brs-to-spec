"""Input collection — resolves read_from entries and emits machine-written read_evidence."""

from __future__ import annotations

import glob as glob_module
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .workspace import resolve_path, WorkspaceError


class InputError(Exception):
    pass


def collect_inputs(
    workspace: Path,
    event: dict,
    output_path: Path,
) -> dict:
    """
    Resolve all read_from entries for the event relative to the workspace root.
    Writes the result to output_path as JSON.
    Returns the bundle dict.

    The bundle contains:
      - event_id
      - read_evidence: list of evidence entries (one per read_from item)
      - missing_required: list of paths that are required but missing
      - overall: "pass" | "fail"
    """
    event_id = event.get("event_id", "UNKNOWN")
    read_from: list[str] = event.get("read_from") or []
    required_inputs: list[str] = event.get("required_inputs") or []

    evidence: list[dict] = []
    missing_required: list[str] = []

    for entry in read_from:
        is_required = entry in required_inputs
        evidence_entry = _resolve_entry(workspace, entry, is_required)
        evidence.append(evidence_entry)
        if is_required and not evidence_entry.get("exists", False) and not evidence_entry.get("matched_files"):
            missing_required.append(entry)

    overall = "fail" if missing_required else "pass"

    bundle: dict[str, Any] = {
        "event_id": event_id,
        "collected_at": _now_iso(),
        "read_evidence": evidence,
        "missing_required": missing_required,
        "overall": overall,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(bundle, indent=2), encoding="utf-8")

    return bundle


def _resolve_entry(workspace: Path, entry: str, is_required: bool) -> dict:
    read_at = _now_iso()

    # glob pattern
    if any(c in entry for c in ("*", "?", "[")):
        return _resolve_glob(workspace, entry, is_required, read_at)

    # plain path
    try:
        resolved = resolve_path(workspace, entry)
    except WorkspaceError as e:
        return {
            "path": entry,
            "required": is_required,
            "exists": False,
            "error": str(e),
            "read_at": read_at,
        }

    if not resolved.exists():
        return {
            "path": entry,
            "required": is_required,
            "exists": False,
            "read_at": read_at,
        }

    lines, bytes_, first_nonempty = _file_metadata(resolved)
    return {
        "path": entry,
        "required": is_required,
        "exists": True,
        "lines": lines,
        "bytes": bytes_,
        "first_nonempty_line": first_nonempty,
        "read_at": read_at,
    }


def _resolve_glob(workspace: Path, pattern: str, is_required: bool, read_at: str) -> dict:
    abs_pattern = str(workspace / pattern)
    matched = sorted(glob_module.glob(abs_pattern, recursive=True))
    rel_matched = [str(Path(m).relative_to(workspace)) for m in matched]

    return {
        "path": pattern,
        "required": is_required,
        "matched_files": rel_matched,
        "read_at": read_at,
    }


def _file_metadata(path: Path) -> tuple[int, int, str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    all_lines = text.splitlines()
    line_count = len(all_lines)
    byte_count = len(text.encode("utf-8"))
    first_nonempty = next((l.strip() for l in all_lines if l.strip()), "")
    return line_count, byte_count, first_nonempty


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
