#!/usr/bin/env python3
"""
engine_cli.py — deterministic flow-engine mechanics for the brs-to-spec framework.

Usage:
  python engine_cli.py <command> [options]

Commands:
  instantiate-event       Create a runtime event from a template
  collect-inputs          Resolve read_from entries and emit read_evidence
  move-event              Move an event between queue buckets
  check-integrity         Scan for dispatcher bypass / orphan files
  validate-result         Validate result file contract
  validate-artifact-counts  Compare FR/NFR IDs between BRS and artifact
  validate-no-placeholders  Scan artifact for placeholder strings
  update-state            Update workflow-state.json and event-log.jsonl
  repair-processing       Repair stale processing/ contents
  repair-chain            Reinstantiate missing downstream events
  reset-to-phase          Reset queue and state to a phase boundary
"""

import argparse
import json
import sys
from pathlib import Path

# allow running from any cwd
sys.path.insert(0, str(Path(__file__).parent))

from brs2spec_engine.workspace import resolve_workspace, WorkspaceError


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


# ---------------------------------------------------------------------------
# Command implementations
# ---------------------------------------------------------------------------

def cmd_instantiate_event(args: argparse.Namespace) -> int:
    from brs2spec_engine.templates import find_template, load_template, build_runtime_event
    from brs2spec_engine.workspace import pending_dir, workflow_state_path
    from datetime import datetime, timezone
    import yaml

    try:
        workspace = resolve_workspace(args.workspace, _repo_root())
    except WorkspaceError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    repo_root = _repo_root()
    template_id = args.template_id

    try:
        template_path = find_template(repo_root, template_id)
        template = load_template(template_path)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    # allocate next event ID
    state_path = workflow_state_path(workspace)
    if not state_path.exists():
        print(f"ERROR: workflow-state.json not found: {state_path}", file=sys.stderr)
        return 1
    state = json.loads(state_path.read_text(encoding="utf-8"))
    counter = int(state.get("event_counter", 0)) + 1
    event_id = f"EVT-{counter:05d}"

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    notes = args.notes or f"Instantiated from {template_id} at {now}"

    try:
        event = build_runtime_event(template, event_id, now, notes)
    except Exception as e:
        print(f"ERROR building runtime event: {e}", file=sys.stderr)
        return 1

    # pre-write self-check
    if not event.get("meta", {}).get("template_id"):
        print("ERROR: self-check failed — meta.template_id not set", file=sys.stderr)
        return 1
    if template.get("must_include") and not event.get("must_include"):
        print("ERROR: self-check failed — must_include not copied from template", file=sys.stderr)
        return 1
    if template.get("validation_rules") and not event.get("validation_rules"):
        print("ERROR: self-check failed — validation_rules not copied from template", file=sys.stderr)
        return 1
    event_type = event.get("event_type", "")
    if not event.get("write_to") and event_type not in ("WAIT_HUMAN", "ROUTE_INITIATIVE"):
        print("ERROR: self-check failed — write_to is empty", file=sys.stderr)
        return 1

    # derive slug from template filename (most descriptive) or fall back to template_id
    _tpl_stem = template_path.stem.lower()  # e.g. evt-tpl-040-gate-business-intake-review
    _after_num = _tpl_stem.split("-", 3)    # ['evt', 'tpl', '040', 'gate-business-...']
    slug = _after_num[3] if len(_after_num) > 3 else template_id.lower().replace("evt-tpl-", "")
    out_file = pending_dir(workspace) / f"{event_id}-{slug}.yaml"
    pending_dir(workspace).mkdir(parents=True, exist_ok=True)
    out_file.write_text(yaml.dump(event, default_flow_style=False, allow_unicode=True), encoding="utf-8")

    # post-write verification: must_include count
    written = yaml.safe_load(out_file.read_text(encoding="utf-8"))
    if template.get("must_include"):
        t_count = len(template["must_include"])
        w_count = len(written.get("must_include") or [])
        if t_count != w_count:
            out_file.unlink()
            print(
                f"ERROR: post-write check failed — template has {t_count} must_include items "
                f"but written file has {w_count}. File deleted.",
                file=sys.stderr,
            )
            return 1

    # update event_counter in workflow-state.json
    state["event_counter"] = counter
    state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")

    print(f"OK: {event_id} instantiated from {template_id} -> {out_file.relative_to(workspace)}")
    if args.output:
        Path(args.output).write_text(json.dumps({"event_id": event_id, "path": str(out_file)}, indent=2))
    return 0


def cmd_collect_inputs(args: argparse.Namespace) -> int:
    from brs2spec_engine.inputs import collect_inputs
    import yaml

    try:
        workspace = resolve_workspace(args.workspace, _repo_root())
    except WorkspaceError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    event_file = Path(args.event_file)
    if not event_file.exists():
        print(f"ERROR: event file not found: {event_file}", file=sys.stderr)
        return 1

    try:
        import yaml as _yaml
        event = _yaml.safe_load(event_file.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"ERROR loading event file: {e}", file=sys.stderr)
        return 1

    event_id = event.get("event_id", "UNKNOWN")
    output_path = Path(args.output) if args.output else (
        workspace / ".flow" / "events" / "processing" / f"{event_id}-inputs.json"
    )

    bundle = collect_inputs(workspace, event, output_path)

    missing = bundle.get("missing_required") or []
    if missing:
        print(f"FAIL: missing required inputs: {missing}", file=sys.stderr)
        return 1

    print(f"OK: {len(bundle['read_evidence'])} input(s) collected -> {output_path}")
    return 0


def cmd_move_event(args: argparse.Namespace) -> int:
    from brs2spec_engine.queue import move_event, QueueError

    try:
        workspace = resolve_workspace(args.workspace, _repo_root())
    except WorkspaceError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    try:
        result = move_event(
            workspace,
            args.event_id,
            args.from_bucket,
            args.to_bucket,
            move_result=not args.no_result,
        )
    except QueueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    for move in result["moved"]:
        print(f"OK: {move}")
    return 0


def cmd_check_integrity(args: argparse.Namespace) -> int:
    from brs2spec_engine.repair import check_integrity_impl
    from brs2spec_engine.workspace import integrity_check_path

    try:
        workspace = resolve_workspace(args.workspace, _repo_root())
    except WorkspaceError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    output_path = Path(args.output) if args.output else integrity_check_path(workspace)

    bundle = check_integrity_impl(workspace, output_path)
    overall = bundle["overall"]

    n_orphan = len(bundle.get("orphan_results", []))
    n_missing = len(bundle.get("missing_result_files", []))
    n_embedded = len(bundle.get("embedded_results", []))

    if overall == "fail":
        parts = []
        if n_orphan:
            parts.append(f"{n_orphan} orphan result file(s)")
        if n_missing:
            parts.append(f"{n_missing} done event(s) with no result file")
        if n_embedded:
            parts.append(f"{n_embedded} event file(s) with embedded result block")
        print(f"FAIL: {', '.join(parts)} -> {output_path}")
        return 1
    if overall == "warn":
        print(f"WARN: inconsistencies detected -> {output_path}")
        return 0
    print(f"OK: integrity check passed -> {output_path}")
    return 0


def cmd_validate_result(args: argparse.Namespace) -> int:
    from brs2spec_engine.results import validate_result, load_yaml_file

    try:
        workspace = resolve_workspace(args.workspace, _repo_root())
    except WorkspaceError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    result_path = Path(args.result_file)
    event_path = Path(args.event_file)
    event_id = result_path.stem.replace("-result", "")
    output_path = Path(args.output) if args.output else (
        workspace / ".flow" / "events" / "processing" / f"{event_id}-result-check.yaml"
    )

    try:
        event = load_yaml_file(event_path)
    except Exception as e:
        print(f"ERROR loading event file: {e}", file=sys.stderr)
        return 1

    bundle = validate_result(result_path, event, output_path)
    overall = bundle.get("overall", "fail")
    print(f"{'OK' if overall == 'pass' else 'FAIL'}: validate-result -> {output_path}")
    return 0 if overall == "pass" else 1


def cmd_validate_artifact_counts(args: argparse.Namespace) -> int:
    from brs2spec_engine.results import validate_artifact_counts

    try:
        workspace = resolve_workspace(args.workspace, _repo_root())
    except WorkspaceError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    brs_path = workspace / args.brs
    artifact_path = workspace / args.artifact
    event_id = args.event_id or "UNKNOWN"
    output_path = Path(args.output) if args.output else (
        workspace / ".flow" / "events" / "processing" / f"{event_id}-artifact-counts.yaml"
    )

    bundle = validate_artifact_counts(workspace, brs_path, artifact_path, output_path)
    overall = bundle.get("overall", "fail")
    print(f"{'OK' if overall == 'pass' else 'FAIL'}: validate-artifact-counts -> {output_path}")
    return 0 if overall == "pass" else 1


def cmd_validate_no_placeholders(args: argparse.Namespace) -> int:
    from brs2spec_engine.results import validate_no_placeholders

    try:
        workspace = resolve_workspace(args.workspace, _repo_root())
    except WorkspaceError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    artifact_path = workspace / args.artifact
    event_id = args.event_id or "UNKNOWN"
    output_path = Path(args.output) if args.output else (
        workspace / ".flow" / "events" / "processing" / f"{event_id}-placeholder-check.yaml"
    )

    bundle = validate_no_placeholders(artifact_path, output_path)
    overall = bundle.get("overall", "fail")
    print(f"{'OK' if overall == 'pass' else 'FAIL'}: validate-no-placeholders -> {output_path}")
    return 0 if overall == "pass" else 1


def cmd_update_state(args: argparse.Namespace) -> int:
    from brs2spec_engine.state import update_state
    from brs2spec_engine.results import load_yaml_file

    try:
        workspace = resolve_workspace(args.workspace, _repo_root())
    except WorkspaceError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    event_path = Path(args.event_file)
    result_path = Path(args.result_file)
    event_id = Path(args.event_file).stem.split("-")[0] + "-" + Path(args.event_file).stem.split("-")[1] if "-" in Path(args.event_file).stem else "UNKNOWN"

    # derive event_id properly
    stem = Path(args.event_file).stem
    parts = stem.split("-")
    event_id = f"{parts[0]}-{parts[1]}" if len(parts) >= 2 else stem

    output_path = Path(args.output) if args.output else (
        workspace / ".flow" / "events" / "processing" / f"{event_id}-state-update.json"
    )

    try:
        event = load_yaml_file(event_path)
        result = load_yaml_file(result_path)
    except Exception as e:
        print(f"ERROR loading files: {e}", file=sys.stderr)
        return 1

    summary = update_state(workspace, event, result, output_path)
    print(f"OK: state updated -> {output_path}")
    return 0


def cmd_repair_processing(args: argparse.Namespace) -> int:
    from brs2spec_engine.repair import repair_processing
    try:
        workspace = resolve_workspace(args.workspace, _repo_root())
        output_path = Path(args.output) if args.output else workspace / ".flow" / "state" / "repair-processing.yaml"
        repair_processing(workspace, output_path)
    except NotImplementedError as e:
        print(f"NOT IMPLEMENTED: {e}", file=sys.stderr)
        return 2
    except WorkspaceError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


def cmd_repair_chain(args: argparse.Namespace) -> int:
    from brs2spec_engine.repair import repair_chain
    try:
        workspace = resolve_workspace(args.workspace, _repo_root())
        output_path = Path(args.output) if args.output else workspace / ".flow" / "state" / "repair-chain.yaml"
        repair_chain(workspace, output_path)
    except NotImplementedError as e:
        print(f"NOT IMPLEMENTED: {e}", file=sys.stderr)
        return 2
    except WorkspaceError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


def cmd_reset_to_phase(args: argparse.Namespace) -> int:
    from brs2spec_engine.repair import reset_to_phase
    try:
        workspace = resolve_workspace(args.workspace, _repo_root())
        output_path = Path(args.output) if args.output else workspace / ".flow" / "state" / "reset-to-phase.yaml"
        reset_to_phase(workspace, args.phase, output_path)
    except NotImplementedError as e:
        print(f"NOT IMPLEMENTED: {e}", file=sys.stderr)
        return 2
    except WorkspaceError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="engine_cli.py",
        description="brs-to-spec flow engine — deterministic mechanics",
    )
    parser.add_argument("--workspace", help="Path to initiative workspace (auto-detected if omitted)")
    parser.add_argument("--output", help="Override the fixed output file path")
    sub = parser.add_subparsers(dest="command", required=True)

    # instantiate-event
    p = sub.add_parser("instantiate-event", help="Create a runtime event from a template")
    p.add_argument("template_id", help="Template ID, e.g. EVT-TPL-002")
    p.add_argument("--notes", help="Optional notes for meta.notes field")

    # collect-inputs
    p = sub.add_parser("collect-inputs", help="Resolve read_from entries and emit read_evidence")
    p.add_argument("event_file", help="Path to the runtime event YAML file")

    # move-event
    p = sub.add_parser("move-event", help="Move an event between queue buckets")
    p.add_argument("event_id", help="EVT-NNNNN identifier")
    p.add_argument("--from", dest="from_bucket", required=True,
                   choices=["pending", "processing", "done", "failed"])
    p.add_argument("--to", dest="to_bucket", required=True,
                   choices=["pending", "processing", "done", "failed"])
    p.add_argument("--no-result", action="store_true",
                   help="Do not move the result file alongside the event file")

    # check-integrity
    sub.add_parser("check-integrity", help="Scan for dispatcher bypass / orphan files")

    # validate-result
    p = sub.add_parser("validate-result", help="Validate result file contract")
    p.add_argument("result_file", help="Path to the result YAML file")
    p.add_argument("event_file", help="Path to the event YAML file")

    # validate-artifact-counts
    p = sub.add_parser("validate-artifact-counts", help="Compare FR/NFR IDs between BRS and artifact")
    p.add_argument("--brs", required=True, help="Relative path to BRS source (e.g. input/brs.md)")
    p.add_argument("--artifact", required=True, help="Relative path to produced artifact")
    p.add_argument("--event-id", dest="event_id", help="EVT-NNNNN for output file naming")

    # validate-no-placeholders
    p = sub.add_parser("validate-no-placeholders", help="Scan artifact for placeholder strings")
    p.add_argument("--artifact", required=True, help="Relative path to artifact to scan")
    p.add_argument("--event-id", dest="event_id", help="EVT-NNNNN for output file naming")

    # update-state
    p = sub.add_parser("update-state", help="Update workflow-state.json and event-log.jsonl")
    p.add_argument("event_file", help="Path to the event YAML file")
    p.add_argument("result_file", help="Path to the result YAML file")

    # repair-processing
    sub.add_parser("repair-processing", help="Repair stale processing/ contents [NOT IMPLEMENTED]")

    # repair-chain
    sub.add_parser("repair-chain", help="Reinstantiate missing downstream events [NOT IMPLEMENTED]")

    # reset-to-phase
    p = sub.add_parser("reset-to-phase", help="Reset queue and state to a phase boundary [NOT IMPLEMENTED]")
    p.add_argument("phase", help="Phase name, e.g. 0-routing, 2-business-intake")

    return parser


_COMMAND_MAP = {
    "instantiate-event":          cmd_instantiate_event,
    "collect-inputs":             cmd_collect_inputs,
    "move-event":                 cmd_move_event,
    "check-integrity":            cmd_check_integrity,
    "validate-result":            cmd_validate_result,
    "validate-artifact-counts":   cmd_validate_artifact_counts,
    "validate-no-placeholders":   cmd_validate_no_placeholders,
    "update-state":               cmd_update_state,
    "repair-processing":          cmd_repair_processing,
    "repair-chain":               cmd_repair_chain,
    "reset-to-phase":             cmd_reset_to_phase,
}


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    fn = _COMMAND_MAP.get(args.command)
    if fn is None:
        print(f"Unknown command: {args.command}", file=sys.stderr)
        return 1
    return fn(args) or 0


if __name__ == "__main__":
    sys.exit(main())
