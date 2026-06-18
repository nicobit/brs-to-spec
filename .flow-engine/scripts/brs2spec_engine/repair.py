"""Repair and reset commands — processing repair, chain repair, phase reset."""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from .workspace import (
    pending_dir, processing_dir, done_dir, failed_dir,
    workflow_state_path, state_dir,
)

try:
    import yaml
    _YAML_AVAILABLE = True
except ImportError:
    _YAML_AVAILABLE = False


class RepairError(Exception):
    pass


# ---------------------------------------------------------------------------
# check-integrity
# ---------------------------------------------------------------------------

def check_integrity_impl(workspace: Path, output_path: Path) -> dict:
    """
    Inspect all queue buckets for integrity violations.

    Checks:
    - Orphan result files in done/ (result file with no matching event file)
    - Orphan result files in processing/ (result file with no matching event file)
    - Done events with no separate result file (bypass: result embedded or missing entirely)
    - Done events whose event file contains an embedded result: block (self-declared pass)
    - artifact_status entries in workflow-state.json that reference unknown events
    """
    d_dir = done_dir(workspace)
    p_dir = processing_dir(workspace)

    orphan_results: list[dict] = []
    processing_orphans: list[dict] = []
    missing_result_files: list[dict] = []
    embedded_results: list[dict] = []
    artifact_status_inconsistencies: list[dict] = []

    # Check done/ for orphan result files
    if d_dir.is_dir():
        result_files = sorted(d_dir.glob("*-result.yaml"))
        for rf in result_files:
            event_id = _extract_event_id(rf.stem.replace("-result", ""))
            event_matches = [
                f for f in d_dir.glob(f"{event_id}-*.yaml")
                if "-result" not in f.stem
            ]
            if not event_matches:
                orphan_results.append({
                    "result_file": rf.name,
                    "event_id": event_id,
                    "bucket": "done",
                    "reason": "result file present but no matching event file in done/",
                })

    # Check done/ event files for missing result files and embedded results
    if d_dir.is_dir():
        for event_file in sorted(d_dir.glob("EVT-*.yaml")):
            if "-result" in event_file.stem:
                continue
            event_id = _extract_event_id(event_file.stem)

            # check 1: separate result file must exist (naming: EVT-NNNNN-*-result.yaml)
            result_matches = [
                f for f in d_dir.glob(f"{event_id}-*.yaml")
                if "-result" in f.stem
            ]
            if not result_matches:
                # check whether result is embedded in the event file itself
                try:
                    data = _load_yaml(event_file)
                    has_embedded = isinstance(data, dict) and "result" in data
                    event_type = data.get("event_type", "") if isinstance(data, dict) else ""
                except Exception:
                    has_embedded = False
                    event_type = ""

                missing_result_files.append({
                    "event_file": event_file.name,
                    "event_id": event_id,
                    "event_type": event_type,
                    "has_embedded_result": has_embedded,
                    "reason": (
                        "done/ event file has result: block embedded inside it — "
                        "Steps 15/16-G were bypassed; result was self-declared without validation"
                        if has_embedded else
                        "done/ event file has no corresponding result file — "
                        "dispatcher Steps 15-17 were not executed"
                    ),
                })

            # check 2: event file must NOT contain a result: key (even if result file exists)
            else:
                try:
                    data = _load_yaml(event_file)
                    if isinstance(data, dict) and "result" in data:
                        embedded_results.append({
                            "event_file": event_file.name,
                            "event_id": event_id,
                            "reason": "event file contains embedded result: block — "
                                      "result must be a separate *-result.yaml file; "
                                      "embedded results bypass validate-result (Step 16-G)",
                        })
                except Exception:
                    pass

    # Check processing/ for orphan result files
    if p_dir.is_dir():
        result_files = sorted(p_dir.glob("*-result.yaml"))
        for rf in result_files:
            event_id = _extract_event_id(rf.stem.replace("-result", ""))
            event_matches = [
                f for f in p_dir.glob(f"{event_id}-*.yaml")
                if "-result" not in f.stem
            ]
            if not event_matches:
                processing_orphans.append({
                    "result_file": rf.name,
                    "event_id": event_id,
                    "bucket": "processing",
                    "reason": "result file present but no matching event file in processing/",
                })

    # Check artifact_status in workflow-state.json
    state_path = workflow_state_path(workspace)
    if state_path.exists():
        try:
            state = json.loads(state_path.read_text(encoding="utf-8"))
            artifact_status = state.get("artifact_status", {})
            all_event_ids: set[str] = set()
            for bucket_fn in (done_dir, pending_dir, processing_dir, failed_dir):
                bd = bucket_fn(workspace)
                if bd.is_dir():
                    for f in bd.glob("EVT-*.yaml"):
                        if "-result" not in f.stem:
                            eid = _extract_event_id(f.stem)
                            all_event_ids.add(eid)
            for artifact_key, entry in artifact_status.items():
                if not isinstance(entry, dict):
                    continue
                produced_by = entry.get("produced_by")
                if produced_by and produced_by not in all_event_ids:
                    artifact_status_inconsistencies.append({
                        "artifact": artifact_key,
                        "event_id": produced_by,
                        "reason": "artifact_status.produced_by references event not found in any bucket",
                    })
        except Exception as e:
            artifact_status_inconsistencies.append({"reason": f"could not parse workflow-state.json: {e}"})

    has_failures = bool(
        orphan_results or missing_result_files or embedded_results
    )
    overall = "fail" if has_failures else ("warn" if processing_orphans else "pass")

    bundle = {
        "command": "check-integrity",
        "ran_at": _now_iso(),
        "overall": overall,
        "orphan_results": orphan_results,
        "missing_result_files": missing_result_files,
        "embedded_results": embedded_results,
        "processing_orphans": processing_orphans,
        "artifact_status_inconsistencies": artifact_status_inconsistencies,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    _write_yaml(output_path, bundle)
    return bundle


# ---------------------------------------------------------------------------
# repair-processing
# ---------------------------------------------------------------------------

def repair_processing(workspace: Path, output_path: Path) -> dict:
    """
    Inspect processing/ and deterministically move or clean stale event/result
    combinations. Writes structured output to output_path.

    Rules (same as dispatcher Step 3):
    - Event AND result in done/ → delete stale copies from processing/
    - Event in failed/ → delete stale copies from processing/
    - Event NOT in done/failed/, result in processing/ with status:pass → move to done/
    - Event NOT in done/failed/, result in processing/ with status:fail → move to failed/
    - Event NOT in done/failed/, NO result in processing/ → move event back to pending/
    """
    p_dir = processing_dir(workspace)
    d_dir = done_dir(workspace)
    f_dir = failed_dir(workspace)
    pe_dir = pending_dir(workspace)

    actions: list[dict] = []

    if not p_dir.is_dir():
        return _write_output(output_path, "repair-processing", actions, "pass")

    # pass 0 — orphan result files in processing/ (result exists, no event file)
    for result_file in sorted(p_dir.glob("*-result.yaml")):
        event_id = _extract_event_id(result_file.stem.replace("-result", ""))
        event_files_in_p = [f for f in p_dir.glob(f"{event_id}-*.yaml") if "-result" not in f.stem]
        if not event_files_in_p:
            result_status = _read_result_status(result_file)
            in_done = bool(list(d_dir.glob(f"{event_id}-*.yaml"))) if d_dir.is_dir() else False
            in_failed = bool(list(f_dir.glob(f"{event_id}-*.yaml"))) if f_dir.is_dir() else False
            if in_done or in_failed:
                result_file.unlink(missing_ok=True)
                actions.append({"event_id": event_id, "action": "deleted_orphan_result",
                                "reason": "event already in done/ or failed/ — stale result in processing/"})
            else:
                # orphan result with no event file and not in done/failed — delete it
                result_file.unlink(missing_ok=True)
                actions.append({"event_id": event_id, "action": "deleted_orphan_result",
                                "reason": "orphan result in processing/ with no event file and not in done/failed"})

    for event_file in sorted(p_dir.glob("*.yaml")):
        if "-result" in event_file.stem:
            continue  # skip result files in this pass

        event_id = _extract_event_id(event_file.stem)
        result_file = p_dir / f"{event_id}-result.yaml"

        in_done = bool(list(d_dir.glob(f"{event_id}-*.yaml"))) if d_dir.is_dir() else False
        in_failed = bool(list(f_dir.glob(f"{event_id}-*.yaml"))) if f_dir.is_dir() else False

        if in_done or in_failed:
            # already completed — delete stale processing copies
            event_file.unlink(missing_ok=True)
            if result_file.exists():
                result_file.unlink()
            actions.append({"event_id": event_id, "action": "deleted_stale",
                            "reason": "already in done/ or failed/"})
            continue

        if result_file.exists():
            result_status = _read_result_status(result_file)
            if result_status == "pass":
                dst = d_dir
                dst.mkdir(parents=True, exist_ok=True)
                shutil.move(str(event_file), str(dst / event_file.name))
                shutil.move(str(result_file), str(dst / result_file.name))
                actions.append({"event_id": event_id, "action": "moved_to_done",
                                "reason": "result status:pass, step17 did not finish"})
            else:
                dst = f_dir
                dst.mkdir(parents=True, exist_ok=True)
                shutil.move(str(event_file), str(dst / event_file.name))
                shutil.move(str(result_file), str(dst / result_file.name))
                actions.append({"event_id": event_id, "action": "moved_to_failed",
                                "reason": f"result status:{result_status}, step17 did not finish"})
        else:
            # interrupted before step 15 — move back to pending
            pe_dir.mkdir(parents=True, exist_ok=True)
            shutil.move(str(event_file), str(pe_dir / event_file.name))
            actions.append({"event_id": event_id, "action": "returned_to_pending",
                            "reason": "no result file — interrupted before step 15"})

    overall = "pass"
    return _write_output(output_path, "repair-processing", actions, overall)


# ---------------------------------------------------------------------------
# repair-chain
# ---------------------------------------------------------------------------

def repair_chain(workspace: Path, output_path: Path) -> dict:
    """
    Read the last completed event's template on_success.create_events.
    Instantiate any downstream events that are missing from pending/done/failed/.
    Does not invent events — only reinstantiates what the template specifies.
    """
    from .templates import find_template, load_template, build_runtime_event
    from .workspace import workflow_state_path

    repo_root = workspace.parent.parent  # initiatives/<id>/ → repo root
    state_path = workflow_state_path(workspace)
    if not state_path.exists():
        raise RepairError(f"workflow-state.json not found: {state_path}")

    state = json.loads(state_path.read_text(encoding="utf-8"))
    last_event_id = state.get("last_completed_event")
    if not last_event_id:
        return _write_output(output_path, "repair-chain",
                             [{"issue": "no last_completed_event in workflow-state.json"}], "warn")

    # find the done event file
    d_dir = done_dir(workspace)
    matches = list(d_dir.glob(f"{last_event_id}-*.yaml")) if d_dir.is_dir() else []
    event_matches = [m for m in matches if "-result" not in m.stem]
    if not event_matches:
        return _write_output(output_path, "repair-chain",
                             [{"issue": f"event file for {last_event_id} not found in done/"}], "warn")

    done_event = _load_yaml(event_matches[0])
    template_id = done_event.get("meta", {}).get("template_id")
    if not template_id:
        # fallback: match by action
        action = done_event.get("action", "")
        return _write_output(output_path, "repair-chain", [{
            "issue": f"meta.template_id absent from {last_event_id}, action={action}. "
                     f"Add meta.template_id manually and re-run repair-chain."
        }], "warn")

    try:
        template_path = find_template(repo_root, template_id)
        template = load_template(template_path)
    except Exception as e:
        return _write_output(output_path, "repair-chain",
                             [{"issue": f"could not load template {template_id}: {e}"}], "warn")

    create_events = template.get("on_success", {}).get("create_events") or []
    if not create_events:
        return _write_output(output_path, "repair-chain",
                             [{"info": f"template {template_id} has no on_success.create_events"}], "pass")

    counter = int(state.get("event_counter", 0))
    now = _now_iso()
    instantiated: list[dict] = []

    for entry in create_events:
        tpl_ref = entry.get("template") if isinstance(entry, dict) else str(entry)
        reason = entry.get("reason", "") if isinstance(entry, dict) else ""

        # check if already exists
        already = _event_exists_for_template(workspace, tpl_ref)
        if already:
            instantiated.append({"template": tpl_ref, "action": "skipped", "reason": "already exists"})
            continue

        try:
            tpl_path = find_template(repo_root, tpl_ref)
            tpl = load_template(tpl_path)
        except Exception as e:
            instantiated.append({"template": tpl_ref, "action": "failed", "reason": str(e)})
            continue

        counter += 1
        event_id = f"EVT-{counter:05d}"
        notes = reason or f"Auto-instantiated by repair-chain from {last_event_id} on_success"
        event = build_runtime_event(tpl, event_id, now, notes)

        slug = tpl_ref.lower().replace("evt-tpl-", "").split("-", 1)[-1]
        out_file = pending_dir(workspace) / f"{event_id}-{slug}.yaml"
        pending_dir(workspace).mkdir(parents=True, exist_ok=True)
        _write_yaml(out_file, event)
        instantiated.append({"template": tpl_ref, "action": "instantiated",
                              "event_id": event_id, "file": str(out_file.name)})

    # update counter
    state["event_counter"] = counter
    state["last_updated"] = now
    state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")

    return _write_output(output_path, "repair-chain", instantiated, "pass")


# ---------------------------------------------------------------------------
# reset-to-phase
# ---------------------------------------------------------------------------

PHASE_BOUNDARIES: dict[str, dict] = {
    "0-routing": {
        "description": "Full reset — wipes pending/processing/failed, restarts from EVT-TPL-001",
        "clear_buckets": ["pending", "processing", "failed"],
        "restart_template": "EVT-TPL-001",
        "reset_stage": "0-routing",
        "confirm_required": True,
    },
    "2-business-intake": {
        "description": "Reset to before business intake — preserves routing, restarts from EVT-TPL-002",
        "clear_buckets": ["pending", "processing", "failed"],
        "restart_template": "EVT-TPL-002",
        "reset_stage": "1-routing-complete",
        "confirm_required": False,
    },
    "2b-business-analysis": {
        "description": "Reset to before business analysis — preserves routing and intake",
        "clear_buckets": ["pending", "processing", "failed"],
        "restart_template": "EVT-TPL-043",
        "reset_stage": "2-business-intake",
        "confirm_required": False,
    },
    "3-planning": {
        "description": "Reset to before planning — preserves all business analysis artifacts",
        "clear_buckets": ["pending", "processing", "failed"],
        "restart_template": None,
        "reset_stage": "2b-business-analysis",
        "confirm_required": False,
    },
}


def reset_to_phase(workspace: Path, phase: str, output_path: Path) -> dict:
    """
    Back up active state, clear active queue buckets, and restart from a phase boundary.
    Never rewrites business artifacts — only queue and state mechanics.
    """
    if phase not in PHASE_BOUNDARIES:
        raise RepairError(
            f"Unknown phase '{phase}'. "
            f"Valid phases: {list(PHASE_BOUNDARIES.keys())}"
        )

    config = PHASE_BOUNDARIES[phase]
    now = _now_iso()
    repo_root = workspace.parent.parent

    # 1. backup
    backup_dir = state_dir(workspace) / f"backup-{now.replace(':', '-')}"
    backup_dir.mkdir(parents=True, exist_ok=True)
    state_path = workflow_state_path(workspace)
    if state_path.exists():
        shutil.copy2(str(state_path), str(backup_dir / "workflow-state.json"))

    for bucket in config["clear_buckets"]:
        src = {
            "pending": pending_dir, "processing": processing_dir,
            "failed": failed_dir,
        }[bucket](workspace)
        if src.is_dir():
            dst = backup_dir / bucket
            shutil.copytree(str(src), str(dst))

    # 2. clear buckets
    cleared: list[str] = []
    for bucket in config["clear_buckets"]:
        src = {
            "pending": pending_dir, "processing": processing_dir,
            "failed": failed_dir,
        }[bucket](workspace)
        if src.is_dir():
            shutil.rmtree(str(src))
            src.mkdir(parents=True, exist_ok=True)
            cleared.append(bucket)

    # 3. reset workflow-state stage
    if state_path.exists():
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state["current_stage"] = config["reset_stage"]
        state["active_events"] = []
        state["last_updated"] = now
        state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")

    # 4. instantiate restart template if specified
    instantiated = None
    restart_tpl = config.get("restart_template")
    if restart_tpl:
        from .templates import find_template, load_template, build_runtime_event
        state = json.loads(state_path.read_text(encoding="utf-8"))
        counter = int(state.get("event_counter", 0)) + 1
        event_id = f"EVT-{counter:05d}"
        tpl_path = find_template(repo_root, restart_tpl)
        tpl = load_template(tpl_path)
        event = build_runtime_event(tpl, event_id, now, f"Auto-instantiated by reset-to-phase ({phase})")
        slug = restart_tpl.lower().replace("evt-tpl-", "").split("-", 1)[-1]
        out_file = pending_dir(workspace) / f"{event_id}-{slug}.yaml"
        _write_yaml(out_file, event)
        state["event_counter"] = counter
        state["active_events"] = [event_id]
        state["last_updated"] = now
        state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")
        instantiated = {"template": restart_tpl, "event_id": event_id, "file": out_file.name}

    result = {
        "phase": phase,
        "backup_dir": str(backup_dir),
        "cleared_buckets": cleared,
        "reset_stage": config["reset_stage"],
        "instantiated": instantiated,
    }
    return _write_output(output_path, "reset-to-phase", [result], "pass")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _event_exists_for_template(workspace: Path, template_id: str) -> bool:
    """Check if any event with meta.template_id == template_id exists in done/pending/failed."""
    for bucket_fn in (done_dir, pending_dir, failed_dir):
        d = bucket_fn(workspace)
        if not d.is_dir():
            continue
        for f in d.glob("EVT-*.yaml"):
            if "-result" in f.stem:
                continue
            try:
                data = _load_yaml(f)
                if data.get("meta", {}).get("template_id") == template_id:
                    return True
            except Exception:
                continue
    return False


def _read_result_status(result_file: Path) -> str:
    try:
        data = _load_yaml(result_file)
        return str(data.get("status", "fail"))
    except Exception:
        return "fail"


def _load_yaml(path: Path):
    text = path.read_text(encoding="utf-8")
    if _YAML_AVAILABLE:
        return yaml.safe_load(text)
    raise RepairError("PyYAML not installed — run: pip install pyyaml")


def _write_yaml(path: Path, data: dict) -> None:
    if _YAML_AVAILABLE:
        path.write_text(yaml.dump(data, default_flow_style=False, allow_unicode=True), encoding="utf-8")
    else:
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def _extract_event_id(stem: str) -> str:
    parts = stem.split("-")
    if len(parts) >= 2:
        return f"{parts[0]}-{parts[1]}"
    return stem


def _write_output(output_path: Path, command: str, actions: list, overall: str) -> dict:
    bundle = {
        "command": command,
        "ran_at": _now_iso(),
        "actions": actions,
        "overall": overall,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    _write_yaml(output_path, bundle)
    return bundle


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
