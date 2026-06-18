"""
Flow engine test suite.

Run from the repo root:
  python -m pytest .flow-engine/tests/test_engine.py -v

Or from the scripts directory:
  python -m pytest ../tests/test_engine.py -v

Requires: pytest, pyyaml
  pip install pytest pyyaml
"""

import json
import shutil
import sys
import tempfile
from pathlib import Path

import pytest
import yaml

# ensure engine package is importable
SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

FIXTURES_DIR = Path(__file__).parent / "fixtures"

from brs2spec_engine.workspace import (
    pending_dir, processing_dir, done_dir, failed_dir,
    workflow_state_path, integrity_check_path,
)
from brs2spec_engine.inputs import collect_inputs
from brs2spec_engine.queue import move_event, QueueError
from brs2spec_engine.results import validate_result, validate_artifact_counts, validate_no_placeholders
from brs2spec_engine.repair import check_integrity_impl, repair_processing
from brs2spec_engine.templates import build_runtime_event, load_template, TemplateError
from brs2spec_engine.state import update_state


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_fixture(name: str, tmp_path: Path) -> Path:
    """Copy a fixture into a temp directory and return the workspace root."""
    src = FIXTURES_DIR / name
    dst = tmp_path / name
    shutil.copytree(str(src), str(dst))
    return dst


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def write_yaml(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.dump(data, default_flow_style=False, allow_unicode=True), encoding="utf-8")


# ---------------------------------------------------------------------------
# check-integrity tests
# ---------------------------------------------------------------------------

class TestCheckIntegrity:

    def test_pass_on_clean_workspace(self, tmp_path):
        workspace = load_fixture("valid-intake", tmp_path)
        output = tmp_path / "integrity-check.yaml"
        result = check_integrity_impl(workspace, output)
        assert result["overall"] == "pass"
        assert result["orphan_results"] == []
        assert output.exists()

    def test_detects_orphan_result_in_done(self, tmp_path):
        workspace = load_fixture("orphan-result-done", tmp_path)
        output = tmp_path / "integrity-check.yaml"
        result = check_integrity_impl(workspace, output)
        assert result["overall"] == "fail"
        assert len(result["orphan_results"]) == 1
        assert "EVT-00002" in result["orphan_results"][0]["result_file"]
        assert output.exists()

    def test_detects_orphan_result_in_processing(self, tmp_path):
        workspace = load_fixture("orphan-result-processing", tmp_path)
        output = tmp_path / "integrity-check.yaml"
        result = check_integrity_impl(workspace, output)
        assert result["overall"] in ("fail", "warn")
        assert len(result["processing_orphans"]) == 1

    def test_detects_artifact_status_inconsistency(self, tmp_path):
        workspace = load_fixture("orphan-result-done", tmp_path)
        output = tmp_path / "integrity-check.yaml"
        result = check_integrity_impl(workspace, output)
        # EVT-00002 event file missing → artifact_status entry unverifiable
        assert len(result["artifact_status_inconsistencies"]) >= 1

    def test_output_file_is_written(self, tmp_path):
        workspace = load_fixture("valid-intake", tmp_path)
        output = tmp_path / "sub" / "integrity-check.yaml"
        check_integrity_impl(workspace, output)
        assert output.exists()
        data = load_yaml(output)
        assert "overall" in data
        assert "ran_at" in data

    def test_detects_done_event_with_embedded_result_no_result_file(self, tmp_path):
        # EVT-00002 in done/ has result: block embedded in the event file
        # and no separate *-result.yaml — the I015 bypass pattern
        workspace = load_fixture("done-event-no-result", tmp_path)
        output = tmp_path / "integrity-check.yaml"
        result = check_integrity_impl(workspace, output)
        assert result["overall"] == "fail"
        missing = result["missing_result_files"]
        event_ids = [e["event_id"] for e in missing]
        assert "EVT-00002" in event_ids
        # should flag has_embedded_result
        evt2 = next(e for e in missing if e["event_id"] == "EVT-00002")
        assert evt2["has_embedded_result"] is True
        assert "bypass" in evt2["reason"].lower() or "embedded" in evt2["reason"].lower()

    def test_detects_done_event_with_embedded_result_despite_result_file(self, tmp_path):
        # EVT-00003 in done/ has BOTH a result: block embedded AND a separate result file
        # the embedded block must still be flagged (embedded_results check)
        workspace = load_fixture("done-event-no-result", tmp_path)
        output = tmp_path / "integrity-check.yaml"
        result = check_integrity_impl(workspace, output)
        embedded = result["embedded_results"]
        event_ids = [e["event_id"] for e in embedded]
        assert "EVT-00003" in event_ids
        evt3 = next(e for e in embedded if e["event_id"] == "EVT-00003")
        assert "bypass" in evt3["reason"].lower() or "embedded" in evt3["reason"].lower()

    def test_clean_done_events_pass(self, tmp_path):
        # EVT-00001 in the fixture has a proper separate result file and no embedded block
        workspace = load_fixture("done-event-no-result", tmp_path)
        output = tmp_path / "integrity-check.yaml"
        result = check_integrity_impl(workspace, output)
        missing_ids = [e["event_id"] for e in result["missing_result_files"]]
        embedded_ids = [e["event_id"] for e in result["embedded_results"]]
        assert "EVT-00001" not in missing_ids
        assert "EVT-00001" not in embedded_ids


# ---------------------------------------------------------------------------
# collect-inputs tests
# ---------------------------------------------------------------------------

class TestCollectInputs:

    def _make_event(self, read_from: list, required: list) -> dict:
        return {
            "event_id": "EVT-00001",
            "read_from": read_from,
            "required_inputs": required,
        }

    def test_resolves_existing_required_file(self, tmp_path):
        workspace = load_fixture("valid-intake", tmp_path)
        event = self._make_event(["input/brs.md"], ["input/brs.md"])
        output = tmp_path / "EVT-00001-inputs.json"
        bundle = collect_inputs(workspace, event, output)
        assert bundle["overall"] == "pass"
        assert bundle["missing_required"] == []
        assert len(bundle["read_evidence"]) == 1
        ev = bundle["read_evidence"][0]
        assert ev["exists"] is True
        assert ev["lines"] > 0
        assert ev["first_nonempty_line"] != ""
        assert output.exists()

    def test_fails_on_missing_required_file(self, tmp_path):
        workspace = load_fixture("missing-required-input", tmp_path)
        event = self._make_event(
            ["business-intake/business-intake-summary.md", "input/brs.md"],
            ["business-intake/business-intake-summary.md", "input/brs.md"],
        )
        output = tmp_path / "EVT-00001-inputs.json"
        bundle = collect_inputs(workspace, event, output)
        assert bundle["overall"] == "fail"
        assert "business-intake/business-intake-summary.md" in bundle["missing_required"]

    def test_optional_missing_does_not_fail(self, tmp_path):
        workspace = load_fixture("valid-intake", tmp_path)
        event = self._make_event(
            ["input/brs.md", "input/architecture.md"],
            ["input/brs.md"],
        )
        output = tmp_path / "EVT-00001-inputs.json"
        bundle = collect_inputs(workspace, event, output)
        assert bundle["overall"] == "pass"
        assert bundle["missing_required"] == []
        assert len(bundle["read_evidence"]) == 2
        optional_ev = next(e for e in bundle["read_evidence"] if e["path"] == "input/architecture.md")
        assert optional_ev["exists"] is False
        assert optional_ev["required"] is False

    def test_read_evidence_count_matches_read_from(self, tmp_path):
        workspace = load_fixture("valid-intake", tmp_path)
        read_from = ["input/brs.md", "input/architecture.md"]
        event = self._make_event(read_from, ["input/brs.md"])
        output = tmp_path / "EVT-00001-inputs.json"
        bundle = collect_inputs(workspace, event, output)
        assert len(bundle["read_evidence"]) == len(read_from)

    def test_output_file_is_written_and_parseable(self, tmp_path):
        workspace = load_fixture("valid-intake", tmp_path)
        event = self._make_event(["input/brs.md"], ["input/brs.md"])
        output = tmp_path / "EVT-00001-inputs.json"
        collect_inputs(workspace, event, output)
        assert output.exists()
        data = json.loads(output.read_text())
        assert "read_evidence" in data
        assert "overall" in data

    def test_rejects_path_outside_workspace(self, tmp_path):
        workspace = load_fixture("valid-intake", tmp_path)
        event = self._make_event(["../../etc/passwd"], ["../../etc/passwd"])
        output = tmp_path / "EVT-00001-inputs.json"
        bundle = collect_inputs(workspace, event, output)
        ev = bundle["read_evidence"][0]
        assert ev.get("exists") is False or "error" in ev


# ---------------------------------------------------------------------------
# move-event tests
# ---------------------------------------------------------------------------

class TestMoveEvent:

    def _setup(self, tmp_path: Path) -> Path:
        workspace = load_fixture("valid-intake", tmp_path)
        # ensure all bucket dirs exist
        for d in (pending_dir(workspace), processing_dir(workspace),
                  done_dir(workspace), failed_dir(workspace)):
            d.mkdir(parents=True, exist_ok=True)
        return workspace

    def test_moves_file_not_copies(self, tmp_path):
        workspace = self._setup(tmp_path)
        src = pending_dir(workspace) / "EVT-00001-route-initiative.yaml"
        assert src.exists()
        move_event(workspace, "EVT-00001", "pending", "processing")
        assert not src.exists()
        assert (processing_dir(workspace) / "EVT-00001-route-initiative.yaml").exists()

    def test_rejects_same_bucket(self, tmp_path):
        workspace = self._setup(tmp_path)
        with pytest.raises(QueueError, match="same"):
            move_event(workspace, "EVT-00001", "pending", "pending")

    def test_rejects_invalid_bucket(self, tmp_path):
        workspace = self._setup(tmp_path)
        with pytest.raises(QueueError):
            move_event(workspace, "EVT-00001", "pending", "archive")

    def test_rejects_missing_source(self, tmp_path):
        workspace = self._setup(tmp_path)
        with pytest.raises(QueueError):
            move_event(workspace, "EVT-00099", "pending", "processing")

    def test_rejects_duplicate_in_destination(self, tmp_path):
        workspace = self._setup(tmp_path)
        # put a copy in processing already
        src = pending_dir(workspace) / "EVT-00001-route-initiative.yaml"
        dst = processing_dir(workspace) / "EVT-00001-route-initiative.yaml"
        shutil.copy2(str(src), str(dst))
        with pytest.raises(QueueError, match="already exists"):
            move_event(workspace, "EVT-00001", "pending", "processing")

    def test_moves_result_file_alongside_event(self, tmp_path):
        workspace = self._setup(tmp_path)
        # create a result file in pending (unusual but tests the mechanic)
        result = pending_dir(workspace) / "EVT-00001-result.yaml"
        result.write_text("event_id: EVT-00001\nstatus: pass\n")
        move_event(workspace, "EVT-00001", "pending", "processing", move_result=True)
        assert (processing_dir(workspace) / "EVT-00001-result.yaml").exists()

    def test_done_to_pending_rejected(self, tmp_path):
        workspace = self._setup(tmp_path)
        src = pending_dir(workspace) / "EVT-00001-route-initiative.yaml"
        shutil.copy2(str(src), str(done_dir(workspace) / src.name))
        with pytest.raises(QueueError):
            move_event(workspace, "EVT-00001", "done", "pending")


# ---------------------------------------------------------------------------
# validate-result tests
# ---------------------------------------------------------------------------

class TestValidateResult:

    def _make_event(self, read_from=None, must_include=None, has_natural_language=False):
        event = {
            "event_id": "EVT-00001",
            "event_type": "CREATE_ARTIFACT",
            "read_from": read_from or [],
            "required_inputs": read_from or [],
            "write_to": ["business-analysis/requirements.md"],
        }
        if must_include:
            event["must_include"] = must_include
        if has_natural_language:
            event["validation_rules"] = {"natural_language": "Check quality."}
        return event

    def test_rejects_status_done(self, tmp_path):
        result_path = tmp_path / "EVT-00001-result.yaml"
        result_path.write_text("event_id: EVT-00001\nstatus: done\ncompleted_at: '2026-06-15T10:00:00Z'\nartifacts_written:\n  - business-analysis/requirements.md\n")
        event_path = tmp_path / "EVT-00001-event.yaml"
        event = self._make_event()
        write_yaml(event_path, event)
        output = tmp_path / "result-check.yaml"
        bundle = validate_result(result_path, event, output)
        assert bundle["overall"] == "fail"
        status_check = next(c for c in bundle["checks"] if c["name"] == "status_field_valid")
        assert status_check["result"] == "fail"
        assert "done" in status_check["detail"]

    def test_passes_valid_result(self, tmp_path):
        result_path = tmp_path / "EVT-00001-result.yaml"
        result_path.write_text(
            "event_id: EVT-00001\nstatus: pass\ncompleted_at: '2026-06-15T10:00:00Z'\n"
            "artifacts_written:\n  - business-analysis/requirements.md\n"
        )
        event = self._make_event()
        output = tmp_path / "result-check.yaml"
        bundle = validate_result(result_path, event, output)
        assert bundle["overall"] == "pass"

    def test_rejects_missing_read_evidence(self, tmp_path):
        result_path = tmp_path / "EVT-00001-result.yaml"
        result_path.write_text(
            "event_id: EVT-00001\nstatus: pass\ncompleted_at: '2026-06-15T10:00:00Z'\n"
            "artifacts_written:\n  - business-analysis/requirements.md\n"
        )
        event = self._make_event(read_from=["input/brs.md"])
        output = tmp_path / "result-check.yaml"
        bundle = validate_result(result_path, event, output)
        assert bundle["overall"] == "fail"
        ev_check = next(c for c in bundle["checks"] if c["name"] == "read_evidence_count")
        assert ev_check["result"] == "fail"

    def test_rejects_validation_notes_count_mismatch(self, tmp_path):
        result_path = tmp_path / "EVT-00001-result.yaml"
        result_path.write_text(
            "event_id: EVT-00001\nstatus: pass\ncompleted_at: '2026-06-15T10:00:00Z'\n"
            "artifacts_written:\n  - business-analysis/requirements.md\n"
            "validation_notes:\n  - rule: 'one item'\n    result: pass\n    detail: ok\n"
        )
        event = self._make_event(must_include=["check one", "check two", "check three"])
        output = tmp_path / "result-check.yaml"
        bundle = validate_result(result_path, event, output)
        assert bundle["overall"] == "fail"
        notes_check = next(c for c in bundle["checks"] if c["name"] == "validation_notes_count")
        assert notes_check["result"] == "fail"

    def test_detects_generic_emptiness_contradiction(self, tmp_path):
        result_path = tmp_path / "EVT-00001-result.yaml"
        result_path.write_text(
            "event_id: EVT-00001\nstatus: fail\ncompleted_at: '2026-06-15T10:00:00Z'\n"
            "artifacts_written: []\n"
            "failure_reason: 'BRS has no content -- no extractable requirements found'\n"
            "read_evidence:\n"
            "  - path: 'input/brs.md'\n"
            "    required: true\n"
            "    exists: true\n"
            "    lines: 150\n"
            "    bytes: 9000\n"
            "    first_nonempty_line: '# Business Requirements Specification'\n"
            "    read_at: '2026-06-15T10:00:00Z'\n",
            encoding="utf-8",
        )
        event = self._make_event(read_from=["input/brs.md"])
        output = tmp_path / "result-check.yaml"
        bundle = validate_result(result_path, event, output)
        assert bundle["overall"] == "fail"
        contra = next(c for c in bundle["checks"] if c["name"] == "no_contradiction")
        assert contra["result"] == "fail"
        assert "150" in contra["detail"]

    def test_output_file_gates_dispatcher(self, tmp_path):
        """The output file must exist and be parseable after validate-result runs."""
        result_path = tmp_path / "EVT-00001-result.yaml"
        result_path.write_text("event_id: EVT-00001\nstatus: done\ncompleted_at: '2026-06-15T10:00:00Z'\nartifacts_written: []\n", encoding="utf-8")
        event = self._make_event()
        output = tmp_path / "result-check.yaml"
        validate_result(result_path, event, output)
        assert output.exists()
        data = load_yaml(output)
        assert data["overall"] in ("pass", "fail")
        # a failing check file must report fail so dispatcher stops
        assert data["overall"] == "fail"

    def test_detects_fabricated_failure_no_read_evidence(self, tmp_path):
        """Reproduces I014 EVT-00001 pattern: fail + content claim + no read_evidence."""
        result_path = tmp_path / "EVT-00001-result.yaml"
        result_path.write_text(
            "event_id: EVT-00001\nstatus: fail\ncompleted_at: '2026-06-15T00:00:00Z'\n"
            "artifacts_written: []\n"
            "failure_reason: 'required input insufficient: BRS source file has no extractable requirements'\n",
            encoding="utf-8",
        )
        event = self._make_event(read_from=["input/brs.md"])
        output = tmp_path / "result-check.yaml"
        bundle = validate_result(result_path, event, output)
        assert bundle["overall"] == "fail"
        fabricated = next(c for c in bundle["checks"] if c["name"] == "no_fabricated_failure")
        assert fabricated["result"] == "fail"
        assert "fabricated failure" in fabricated["detail"]
        assert "Step 10" in fabricated["detail"]

    def test_detects_freehand_validation_notes_i014_pattern(self, tmp_path):
        """Reproduces I014 EVT-00004 pattern: freehand labels don't match must_include text."""
        result_path = tmp_path / "EVT-00001-result.yaml"
        result_path.write_text(
            "event_id: EVT-00001\nstatus: pass\ncompleted_at: '2026-06-15T12:15:10Z'\n"
            "artifacts_written:\n  - business-analysis/requirements.md\n"
            "validation_notes:\n"
            "  - rule: 'FR COMPLETENESS'\n    result: pass\n    detail: '30 FRs identified'\n"
            "  - rule: 'NFR COMPLETENESS'\n    result: pass\n    detail: '7 NFRs identified'\n"
            "  - rule: 'ID CONVENTION'\n    result: pass\n    detail: 'FR-NNN used'\n"
            "  - rule: 'DOMAIN CORRECTNESS'\n    result: pass\n    detail: 'Random FR checks trace to input/brs.md lines'\n"
            "  - rule: 'NO PLACEHOLDERS'\n    result: pass\n    detail: 'None found'\n",
            encoding="utf-8",
        )
        event = self._make_event(must_include=[
            "FR count: enumerate every FR-NNN ID found in input/brs.md; enumerate every FR row in artifact; state both counts",
            "NFR count: enumerate every NFR-NNN ID found in input/brs.md; enumerate every NFR row; state both counts",
            "Every FR row has a unique ID matching the BRS convention, a one-sentence statement, a priority, and a source reference — spot-check 3 rows and quote each field",
            "No placeholder text (TBD / TODO / fill in) anywhere in the artifact",
            "Notes field does NOT contain phrases like generated to satisfy must_include",
        ])
        output = tmp_path / "result-check.yaml"
        bundle = validate_result(result_path, event, output)
        assert bundle["overall"] == "fail"
        anchored = next(c for c in bundle["checks"] if c["name"] == "validation_notes_anchored")
        assert anchored["result"] == "fail"
        # freehand labels like "FR COMPLETENESS" and "DOMAIN CORRECTNESS" should be flagged
        assert "COMPLETENESS" in anchored["detail"] or "CORRECTNESS" in anchored["detail"]

    def test_passes_anchored_validation_notes(self, tmp_path):
        """Notes that quote must_include text pass the anchoring check."""
        result_path = tmp_path / "EVT-00001-result.yaml"
        result_path.write_text(
            "event_id: EVT-00001\nstatus: pass\ncompleted_at: '2026-06-15T12:15:10Z'\n"
            "artifacts_written:\n  - business-analysis/requirements.md\n"
            "validation_notes:\n"
            "  - rule: 'FR count: enumerate every FR-NNN ID found in input/brs.md'\n"
            "    result: pass\n    detail: 'BRS has FR-001..FR-030; artifact has 30 FR rows; counts match'\n"
            "  - rule: 'No placeholder text (TBD / TODO / fill in) anywhere in the artifact'\n"
            "    result: pass\n    detail: 'No placeholders found'\n",
            encoding="utf-8",
        )
        event = self._make_event(must_include=[
            "FR count: enumerate every FR-NNN ID found in input/brs.md; state both counts",
            "No placeholder text (TBD / TODO / fill in) anywhere in the artifact",
        ])
        output = tmp_path / "result-check.yaml"
        bundle = validate_result(result_path, event, output)
        anchored = next(c for c in bundle["checks"] if c["name"] == "validation_notes_anchored")
        assert anchored["result"] == "pass"

    def test_detects_missing_first_nonempty_line(self, tmp_path):
        """Reproduces I014 EVT-00004 pattern: read_evidence exists:true but no first_nonempty_line."""
        result_path = tmp_path / "EVT-00001-result.yaml"
        result_path.write_text(
            "event_id: EVT-00001\nstatus: pass\ncompleted_at: '2026-06-15T12:15:10Z'\n"
            "artifacts_written:\n  - business-analysis/requirements.md\n"
            "read_evidence:\n"
            "  - path: 'input/brs.md'\n"
            "    required: true\n"
            "    exists: true\n"
            "    lines: 220\n"
            "    bytes: 15200\n"
            "    read_at: '2026-06-15T12:14:35Z'\n",
            encoding="utf-8",
        )
        event = self._make_event(read_from=["input/brs.md"])
        output = tmp_path / "result-check.yaml"
        bundle = validate_result(result_path, event, output)
        assert bundle["overall"] == "fail"
        fnl = next(c for c in bundle["checks"] if c["name"] == "read_evidence_first_nonempty_line")
        assert fnl["result"] == "fail"
        assert "input/brs.md" in fnl["detail"]

    def test_passes_read_evidence_with_first_nonempty_line(self, tmp_path):
        """Correct read_evidence with first_nonempty_line passes."""
        result_path = tmp_path / "EVT-00001-result.yaml"
        result_path.write_text(
            "event_id: EVT-00001\nstatus: pass\ncompleted_at: '2026-06-15T12:15:10Z'\n"
            "artifacts_written:\n  - business-analysis/requirements.md\n"
            "read_evidence:\n"
            "  - path: 'input/brs.md'\n"
            "    required: true\n"
            "    exists: true\n"
            "    lines: 220\n"
            "    bytes: 15200\n"
            "    first_nonempty_line: '# Business Requirements Specification'\n"
            "    read_at: '2026-06-15T12:14:35Z'\n",
            encoding="utf-8",
        )
        event = self._make_event(read_from=["input/brs.md"])
        output = tmp_path / "result-check.yaml"
        bundle = validate_result(result_path, event, output)
        fnl = next(c for c in bundle["checks"] if c["name"] == "read_evidence_first_nonempty_line")
        assert fnl["result"] == "pass"


# ---------------------------------------------------------------------------
# validate-artifact-counts tests
# ---------------------------------------------------------------------------

class TestValidateArtifactCounts:

    def test_detects_missing_fr_rows(self, tmp_path):
        workspace = load_fixture("missing-fr-rows", tmp_path)
        brs = workspace / "input" / "brs.md"
        artifact = workspace / "business-analysis" / "requirements.md"
        output = tmp_path / "artifact-counts.yaml"
        bundle = validate_artifact_counts(workspace, brs, artifact, output)
        assert bundle["overall"] == "fail"
        fr_check = next(c for c in bundle["checks"] if c["name"] == "fr_count_match")
        assert fr_check["result"] == "fail"
        assert "FR-004" in fr_check["detail"]
        assert "FR-005" in fr_check["detail"]

    def test_detects_missing_nfr_rows(self, tmp_path):
        workspace = load_fixture("missing-fr-rows", tmp_path)
        brs = workspace / "input" / "brs.md"
        artifact = workspace / "business-analysis" / "requirements.md"
        output = tmp_path / "artifact-counts.yaml"
        bundle = validate_artifact_counts(workspace, brs, artifact, output)
        nfr_check = next(c for c in bundle["checks"] if c["name"] == "nfr_count_match")
        assert nfr_check["result"] == "fail"
        assert "NFR-002" in nfr_check["detail"]

    def test_passes_when_counts_match(self, tmp_path):
        workspace = load_fixture("valid-intake", tmp_path)
        brs = workspace / "input" / "brs.md"
        artifact = workspace / "business-intake" / "business-intake-summary.md"
        output = tmp_path / "artifact-counts.yaml"
        bundle = validate_artifact_counts(workspace, brs, artifact, output)
        assert bundle["overall"] == "pass"

    def test_output_file_written(self, tmp_path):
        workspace = load_fixture("missing-fr-rows", tmp_path)
        brs = workspace / "input" / "brs.md"
        artifact = workspace / "business-analysis" / "requirements.md"
        output = tmp_path / "artifact-counts.yaml"
        validate_artifact_counts(workspace, brs, artifact, output)
        assert output.exists()
        data = load_yaml(output)
        assert "overall" in data
        assert "checks" in data


# ---------------------------------------------------------------------------
# validate-no-placeholders tests
# ---------------------------------------------------------------------------

class TestValidateNoPlaceholders:

    def test_detects_tbd_in_artifact(self, tmp_path):
        artifact = tmp_path / "requirements.md"
        artifact.write_text("# Requirements\n\n| FR-001 | TBD | High | source |\n")
        output = tmp_path / "placeholder-check.yaml"
        bundle = validate_no_placeholders(artifact, output)
        assert bundle["overall"] == "fail"
        check = bundle["checks"][0]
        assert "Line 3" in check["detail"]

    def test_allows_placeholders_in_gaps_section(self, tmp_path):
        artifact = tmp_path / "requirements.md"
        artifact.write_text(
            "# Requirements\n\n## Gaps and Questions\n\n| GAP-001 | TBD answer | High |\n"
        )
        output = tmp_path / "placeholder-check.yaml"
        bundle = validate_no_placeholders(artifact, output)
        assert bundle["overall"] == "pass"

    def test_passes_clean_artifact(self, tmp_path):
        artifact = tmp_path / "requirements.md"
        artifact.write_text("# Requirements\n\n| FR-001 | Accept files | High | input/brs.md |\n")
        output = tmp_path / "placeholder-check.yaml"
        bundle = validate_no_placeholders(artifact, output)
        assert bundle["overall"] == "pass"

    def test_detects_todo_and_fill_in(self, tmp_path):
        artifact = tmp_path / "requirements.md"
        artifact.write_text("# Req\n| FR-001 | TODO | High | source |\n| FR-002 | [fill in] | Medium | source |\n")
        output = tmp_path / "placeholder-check.yaml"
        bundle = validate_no_placeholders(artifact, output)
        assert bundle["overall"] == "fail"
        assert "Line 2" in bundle["checks"][0]["detail"]
        assert "Line 3" in bundle["checks"][0]["detail"]


# ---------------------------------------------------------------------------
# repair-processing tests
# ---------------------------------------------------------------------------

class TestRepairProcessing:

    def test_cleans_orphan_results_already_in_done(self, tmp_path):
        workspace = load_fixture("valid-intake", tmp_path)
        # set up: event in done/, stale result in processing/
        done_dir(workspace).mkdir(parents=True, exist_ok=True)
        processing_dir(workspace).mkdir(parents=True, exist_ok=True)
        (done_dir(workspace) / "EVT-00001-route-initiative.yaml").write_text("event_id: EVT-00001\n")
        (processing_dir(workspace) / "EVT-00001-result.yaml").write_text("event_id: EVT-00001\nstatus: pass\n")
        output = tmp_path / "repair.yaml"
        result = repair_processing(workspace, output)
        assert not (processing_dir(workspace) / "EVT-00001-result.yaml").exists()
        assert any(a["action"] == "deleted_orphan_result" for a in result["actions"])

    def test_returns_interrupted_event_to_pending(self, tmp_path):
        workspace = load_fixture("valid-intake", tmp_path)
        processing_dir(workspace).mkdir(parents=True, exist_ok=True)
        # event in processing/ with no result
        src = pending_dir(workspace) / "EVT-00001-route-initiative.yaml"
        dst = processing_dir(workspace) / "EVT-00001-route-initiative.yaml"
        shutil.copy2(str(src), str(dst))
        src.unlink()
        output = tmp_path / "repair.yaml"
        result = repair_processing(workspace, output)
        assert (pending_dir(workspace) / "EVT-00001-route-initiative.yaml").exists()
        assert any(a["action"] == "returned_to_pending" for a in result["actions"])

    def test_moves_pass_result_to_done(self, tmp_path):
        workspace = load_fixture("valid-intake", tmp_path)
        processing_dir(workspace).mkdir(parents=True, exist_ok=True)
        done_dir(workspace).mkdir(parents=True, exist_ok=True)
        event = pending_dir(workspace) / "EVT-00001-route-initiative.yaml"
        shutil.copy2(str(event), str(processing_dir(workspace) / event.name))
        event.unlink()
        (processing_dir(workspace) / "EVT-00001-result.yaml").write_text(
            "event_id: EVT-00001\nstatus: pass\ncompleted_at: '2026-06-15T10:00:00Z'\nartifacts_written: []\n"
        )
        output = tmp_path / "repair.yaml"
        result = repair_processing(workspace, output)
        assert (done_dir(workspace) / "EVT-00001-route-initiative.yaml").exists()
        assert any(a["action"] == "moved_to_done" for a in result["actions"])

    def test_output_file_written(self, tmp_path):
        workspace = load_fixture("valid-intake", tmp_path)
        output = tmp_path / "repair.yaml"
        repair_processing(workspace, output)
        assert output.exists()
        data = load_yaml(output)
        assert "overall" in data


# ---------------------------------------------------------------------------
# instantiate-event tests
# ---------------------------------------------------------------------------

# Minimal template that satisfies _require_template_fields
_MINIMAL_TEMPLATE = {
    "event_template_id": "EVT-TPL-TEST",
    "type": "create_requirements",
    "persona": "analyst",
    "description": "Test template for unit tests",
    "priority": "normal",
    "inputs": {
        "required": ["input/brs.md"],
        "optional": ["input/architecture.md"],
    },
    "outputs": {
        "primary": "business-analysis/requirements.md",
        "secondary": ["business-analysis/requirements-traceability.md"],
    },
    "must_include": [
        "FR count: enumerate all FR IDs in BRS and artifact",
        "NFR count: enumerate all NFR IDs in BRS and artifact",
    ],
    "validation_rules": {
        "natural_language": "Spot-check 3 random FR rows against BRS source.",
    },
    "on_success": {
        "create_events": [{"template": "EVT-TPL-003", "reason": "next step"}],
    },
    "on_failure": {
        "raise_decision": {"question": "Fix requirements", "owner": "human", "blocking": True},
    },
}


class TestInstantiateEvent:

    def test_event_id_follows_evt_pattern(self):
        event = build_runtime_event(_MINIMAL_TEMPLATE, "EVT-00042", "2026-06-15T10:00:00Z", "test")
        assert event["event_id"] == "EVT-00042"

    def test_meta_template_id_preserved(self):
        event = build_runtime_event(_MINIMAL_TEMPLATE, "EVT-00001", "2026-06-15T10:00:00Z")
        assert event["meta"]["template_id"] == "EVT-TPL-TEST"

    def test_must_include_preserved_verbatim(self):
        event = build_runtime_event(_MINIMAL_TEMPLATE, "EVT-00001", "2026-06-15T10:00:00Z")
        assert event["must_include"] == _MINIMAL_TEMPLATE["must_include"]

    def test_validation_rules_preserved_verbatim(self):
        event = build_runtime_event(_MINIMAL_TEMPLATE, "EVT-00001", "2026-06-15T10:00:00Z")
        assert event["validation_rules"] == _MINIMAL_TEMPLATE["validation_rules"]

    def test_on_success_preserved_verbatim(self):
        event = build_runtime_event(_MINIMAL_TEMPLATE, "EVT-00001", "2026-06-15T10:00:00Z")
        assert event["on_success"] == _MINIMAL_TEMPLATE["on_success"]

    def test_on_failure_preserved_verbatim(self):
        event = build_runtime_event(_MINIMAL_TEMPLATE, "EVT-00001", "2026-06-15T10:00:00Z")
        assert event["on_failure"] == _MINIMAL_TEMPLATE["on_failure"]

    def test_read_from_combines_required_and_optional(self):
        event = build_runtime_event(_MINIMAL_TEMPLATE, "EVT-00001", "2026-06-15T10:00:00Z")
        assert "input/brs.md" in event["read_from"]
        assert "input/architecture.md" in event["read_from"]

    def test_write_to_includes_primary_and_secondary(self):
        event = build_runtime_event(_MINIMAL_TEMPLATE, "EVT-00001", "2026-06-15T10:00:00Z")
        assert "business-analysis/requirements.md" in event["write_to"]
        assert "business-analysis/requirements-traceability.md" in event["write_to"]

    def test_type_mapping_create_artifact(self):
        event = build_runtime_event(_MINIMAL_TEMPLATE, "EVT-00001", "2026-06-15T10:00:00Z")
        assert event["event_type"] == "CREATE_ARTIFACT"
        assert event["action"] == "create_requirements"

    def test_type_mapping_route_initiative(self):
        tpl = dict(_MINIMAL_TEMPLATE, type="route_initiative")
        event = build_runtime_event(tpl, "EVT-00001", "2026-06-15T10:00:00Z")
        assert event["event_type"] == "ROUTE_INITIATIVE"

    def test_type_mapping_wait_human(self):
        tpl = dict(_MINIMAL_TEMPLATE, type="gate_business_intake_review")
        event = build_runtime_event(tpl, "EVT-00001", "2026-06-15T10:00:00Z")
        assert event["event_type"] == "WAIT_HUMAN"

    def test_written_to_pending_dir(self, tmp_path):
        workspace = load_fixture("valid-intake", tmp_path)
        event = build_runtime_event(_MINIMAL_TEMPLATE, "EVT-00002", "2026-06-15T10:00:00Z", "test")
        slug = "test"
        out_file = pending_dir(workspace) / f"EVT-00002-{slug}.yaml"
        write_yaml(out_file, event)
        assert out_file.exists()
        loaded = load_yaml(out_file)
        assert loaded["event_id"] == "EVT-00002"
        assert loaded["meta"]["template_id"] == "EVT-TPL-TEST"

    def test_missing_required_field_raises(self):
        bad_tpl = dict(_MINIMAL_TEMPLATE)
        del bad_tpl["persona"]
        with pytest.raises(TemplateError, match="missing required fields"):
            build_runtime_event(bad_tpl, "EVT-00001", "2026-06-15T10:00:00Z")

    def test_loads_real_tpl001_from_repo(self):
        # tests against the actual EVT-TPL-001 in the repo
        repo_root = Path(__file__).parent.parent.parent
        tpl_path = repo_root / ".brs2spec2" / "workflow" / "event-templates" / "EVT-TPL-001-route-initiative.yaml"
        if not tpl_path.exists():
            pytest.skip("EVT-TPL-001 not found in repo")
        tpl = load_template(tpl_path)
        event = build_runtime_event(tpl, "EVT-00001", "2026-06-15T10:00:00Z", "routing")
        assert event["meta"]["template_id"] == "EVT-TPL-001"
        assert event["must_include"] is not None
        assert len(event["must_include"]) > 0
        assert event["on_success"] is not None


# ---------------------------------------------------------------------------
# update-state tests
# ---------------------------------------------------------------------------

class TestUpdateState:

    def _make_event(self, event_id="EVT-00001", event_type="CREATE_ARTIFACT",
                    artifacts=None) -> dict:
        return {
            "event_id": event_id,
            "event_type": event_type,
            "action": "create_requirements",
            "persona": "analyst",
            "write_to": artifacts or ["business-analysis/requirements.md"],
        }

    def _make_result(self, event_id="EVT-00001", status="pass", artifacts=None) -> dict:
        return {
            "event_id": event_id,
            "status": status,
            "completed_at": "2026-06-15T10:00:00Z",
            "artifacts_written": artifacts or ["business-analysis/requirements.md"],
        }

    def test_removes_event_from_active(self, tmp_path):
        workspace = load_fixture("valid-intake", tmp_path)
        event = self._make_event()
        result = self._make_result()
        output = tmp_path / "state-update.json"
        update_state(workspace, event, result, output)
        state = json.loads(workflow_state_path(workspace).read_text())
        assert "EVT-00001" not in state["active_events"]

    def test_sets_last_completed_event_on_pass(self, tmp_path):
        workspace = load_fixture("valid-intake", tmp_path)
        event = self._make_event()
        result = self._make_result(status="pass")
        output = tmp_path / "state-update.json"
        update_state(workspace, event, result, output)
        state = json.loads(workflow_state_path(workspace).read_text())
        assert state["last_completed_event"] == "EVT-00001"

    def test_appends_to_failed_events_on_fail(self, tmp_path):
        workspace = load_fixture("valid-intake", tmp_path)
        event = self._make_event()
        result = self._make_result(status="fail", artifacts=[])
        output = tmp_path / "state-update.json"
        update_state(workspace, event, result, output)
        state = json.loads(workflow_state_path(workspace).read_text())
        assert "EVT-00001" in state["failed_events"]

    def test_artifact_status_updated_on_pass(self, tmp_path):
        workspace = load_fixture("valid-intake", tmp_path)
        event = self._make_event()
        result = self._make_result(status="pass")
        output = tmp_path / "state-update.json"
        update_state(workspace, event, result, output)
        state = json.loads(workflow_state_path(workspace).read_text())
        entry = state["artifact_status"]["business-analysis/requirements.md"]
        assert entry["status"] == "ai_validated"
        assert entry["produced_by"] == "EVT-00001"

    def test_artifact_status_failed_on_fail(self, tmp_path):
        workspace = load_fixture("valid-intake", tmp_path)
        event = self._make_event()
        result = self._make_result(status="fail", artifacts=["business-analysis/requirements.md"])
        output = tmp_path / "state-update.json"
        update_state(workspace, event, result, output)
        state = json.loads(workflow_state_path(workspace).read_text())
        entry = state["artifact_status"]["business-analysis/requirements.md"]
        assert entry["status"] == "failed"

    def test_wait_human_artifact_status_accepted(self, tmp_path):
        workspace = load_fixture("valid-intake", tmp_path)
        event = self._make_event(event_type="WAIT_HUMAN",
                                 artifacts=["routing/routing-decision.md"])
        result = self._make_result(status="pass",
                                   artifacts=["routing/routing-decision.md"])
        output = tmp_path / "state-update.json"
        update_state(workspace, event, result, output)
        state = json.loads(workflow_state_path(workspace).read_text())
        entry = state["artifact_status"]["routing/routing-decision.md"]
        assert entry["status"] == "accepted"

    def test_event_log_appends_once(self, tmp_path):
        workspace = load_fixture("valid-intake", tmp_path)
        event = self._make_event()
        result = self._make_result()
        output = tmp_path / "state-update.json"
        update_state(workspace, event, result, output)
        update_state(workspace, event, result, output)  # second call — must not duplicate
        from brs2spec_engine.workspace import event_log_path
        log = event_log_path(workspace).read_text(encoding="utf-8").strip().splitlines()
        assert len(log) == 1
        entry = json.loads(log[0])
        assert entry["event_id"] == "EVT-00001"

    def test_output_file_written_and_parseable(self, tmp_path):
        workspace = load_fixture("valid-intake", tmp_path)
        event = self._make_event()
        result = self._make_result()
        output = tmp_path / "EVT-00001-state-update.json"
        update_state(workspace, event, result, output)
        assert output.exists()
        data = json.loads(output.read_text())
        assert data["overall"] == "pass"
        assert data["event_id"] == "EVT-00001"

    def test_decisions_written_to_open_decisions_md(self, tmp_path):
        workspace = load_fixture("valid-intake", tmp_path)
        event = self._make_event()
        result = dict(self._make_result(), open_decisions_raised=[{
            "question": "Should we support CSV and JSON?",
            "owner": "architect",
            "blocking": False,
        }])
        output = tmp_path / "state-update.json"
        summary = update_state(workspace, event, result, output)
        assert len(summary["decisions_written"]) == 1
        dec_id = summary["decisions_written"][0]
        from brs2spec_engine.workspace import state_dir
        decisions_md = (state_dir(workspace) / "open-decisions.md").read_text(encoding="utf-8")
        assert dec_id in decisions_md
        assert "Should we support CSV and JSON?" in decisions_md
