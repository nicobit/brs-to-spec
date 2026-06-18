from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path


EVENT_FILE_RE = re.compile(r"^(EVT-\d{5})-.*\.yaml$")
CANONICAL_RESULT_FILE_RE = re.compile(r"^(EVT-\d{5})-result\.yaml$")
LEGACY_RESULT_FILE_RE = re.compile(r"^(EVT-\d{5})-.*-result\.yaml$")
EVENT_ID_RE = re.compile(r"(EVT-\d{5})")


def require_yaml():
    spec = importlib.util.find_spec("yaml")
    if spec is None:
        print("PyYAML is required for this audit script.", file=sys.stderr)
        raise SystemExit(2)
    import yaml  # type: ignore

    return yaml


def load_yaml(path: Path):
    yaml = require_yaml()
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def event_id_from_event_filename(path: Path) -> str | None:
    match = EVENT_FILE_RE.match(path.name)
    return match.group(1) if match else None


def event_id_from_result_filename(path: Path) -> tuple[str | None, bool]:
    match = CANONICAL_RESULT_FILE_RE.match(path.name)
    if match:
        return match.group(1), True
    match = LEGACY_RESULT_FILE_RE.match(path.name)
    if match:
        return match.group(1), False
    return None, False


def result_requires_validation_notes(event: dict) -> tuple[bool, int, bool]:
    must_include = event.get("must_include") or []
    validation_rules = event.get("validation_rules") or {}
    has_natural_language = bool(validation_rules.get("natural_language"))
    required = bool(must_include) or has_natural_language
    expected_count = len(must_include) + (1 if has_natural_language else 0)
    return required, expected_count, has_natural_language


def extract_event_id(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    match = EVENT_ID_RE.search(value)
    return match.group(1) if match else None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit one v2 .flow workspace for queue/state/result integrity."
    )
    parser.add_argument("workspace", help="Path to the initiative workspace root.")
    args = parser.parse_args()

    root = Path(args.workspace).resolve()
    flow_root = root / ".flow"
    state_path = flow_root / "state" / "workflow-state.json"
    log_path = flow_root / "state" / "event-log.jsonl"
    events_root = flow_root / "events"

    findings: list[str] = []

    if not state_path.exists():
        print(f"Missing workflow state: {state_path}", file=sys.stderr)
        return 2

    state = json.loads(state_path.read_text(encoding="utf-8"))

    event_files_by_status: dict[str, dict[str, Path]] = {
        "pending": {},
        "processing": {},
        "done": {},
        "failed": {},
    }
    result_files_by_status: dict[str, dict[str, Path]] = {
        "pending": {},
        "processing": {},
        "done": {},
        "failed": {},
    }

    all_event_ids: dict[str, list[str]] = {}

    for status in event_files_by_status:
        folder = events_root / status
        if not folder.exists():
            findings.append(f"missing folder: .flow/events/{status}")
            continue
        for path in folder.glob("*.yaml"):
            result_id, canonical = event_id_from_result_filename(path)
            if result_id:
                result_files_by_status[status][result_id] = path
                if not canonical:
                    findings.append(
                        f"{status}/{path.name} uses legacy result naming; rename to {result_id}-result.yaml"
                    )
                continue
            event_id = event_id_from_event_filename(path)
            if event_id:
                event_files_by_status[status][event_id] = path
                all_event_ids.setdefault(event_id, []).append(status)

    for event_id, statuses in sorted(all_event_ids.items()):
        if len(statuses) > 1:
            findings.append(
                f"{event_id} exists in multiple event folders: {', '.join(statuses)}"
            )

    pending_ids = sorted(event_files_by_status["pending"].keys())
    active_ids = sorted(state.get("active_events", []))
    if pending_ids != active_ids:
        findings.append(
            "active_events mismatch: "
            f"workflow-state has {active_ids}, pending folder has {pending_ids}"
        )

    last_completed = state.get("last_completed_event")
    if last_completed and last_completed not in event_files_by_status["done"]:
        findings.append(
            f"last_completed_event {last_completed} not present in .flow/events/done/"
        )

    if event_files_by_status["processing"] and result_files_by_status["processing"] == {}:
        findings.append("processing/ contains event files without result files")

    for status in ["done", "failed"]:
        for event_id, event_path in sorted(event_files_by_status[status].items()):
            result_path = result_files_by_status[status].get(event_id)
            if result_path is None:
                findings.append(
                    f"{status}/{event_path.name} missing canonical result file {event_id}-result.yaml"
                )
                continue

            event = load_yaml(event_path) or {}
            result = load_yaml(result_path) or {}

            if result.get("event_id") != event_id:
                findings.append(
                    f"{result_path.name} event_id mismatch: expected {event_id}, found {result.get('event_id')}"
                )

            needs_notes, expected_count, has_natural_language = result_requires_validation_notes(event)
            notes = result.get("validation_notes")

            if status == "done" and result.get("status") != "pass":
                findings.append(f"{event_id} is in done/ but result status is {result.get('status')}")
            if status == "failed" and result.get("status") != "fail":
                findings.append(f"{event_id} is in failed/ but result status is {result.get('status')}")

            if needs_notes:
                if not isinstance(notes, list) or not notes:
                    findings.append(
                        f"{event_id} passed through {status}/ without required validation_notes"
                    )
                else:
                    if len(notes) != expected_count:
                        findings.append(
                            f"{event_id} validation_notes count mismatch: expected {expected_count}, found {len(notes)}"
                        )
                    if has_natural_language:
                        nl_entries = [
                            note
                            for note in notes
                            if str((note or {}).get("rule", "")).startswith("natural_language:")
                        ]
                        if len(nl_entries) != 1:
                            findings.append(
                                f"{event_id} missing exactly one natural_language validation entry"
                            )

    artifact_status = state.get("artifact_status", {})
    for artifact_path, meta in sorted(artifact_status.items()):
        produced_by = meta.get("produced_by")
        if produced_by and produced_by not in all_event_ids:
            findings.append(
                f"artifact_status[{artifact_path}] references missing producer event {produced_by}"
            )

    if log_path.exists():
        seen_log_ids: dict[str, int] = {}
        for lineno, line in enumerate(log_path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                findings.append(f"event-log line {lineno} is not valid JSON: {exc}")
                continue
            event_id = extract_event_id(record.get("event_id")) or extract_event_id(
                record.get("event")
            )
            if event_id:
                seen_log_ids[event_id] = seen_log_ids.get(event_id, 0) + 1
        for event_id, count in sorted(seen_log_ids.items()):
            if count > 1:
                findings.append(f"event-log has {count} entries for {event_id}")

    if findings:
        print(f"Audit FAILED for {root}")
        for finding in findings:
            print(f"- {finding}")
        return 1

    print(f"Audit OK for {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
