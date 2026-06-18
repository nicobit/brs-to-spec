"""Maintenance command checks for staged `.b2s` engine behavior."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import sys
import textwrap
import unittest


REPO_ROOT = Path(__file__).resolve().parents[2]
CLI_PATH = REPO_ROOT / ".b2s" / "scripts" / "b2s_cli.py"
RUNTIME_ROOT = REPO_ROOT / ".b2s" / "tests" / "runtime"


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CLI_PATH), *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=True,
    )


class EngineMaintenanceTests(unittest.TestCase):
    def setUp(self) -> None:
        RUNTIME_ROOT.mkdir(parents=True, exist_ok=True)
        self.workspace_root = RUNTIME_ROOT / self._testMethodName
        if self.workspace_root.exists():
            shutil.rmtree(self.workspace_root)
        (self.workspace_root / "input").mkdir(parents=True)
        (self.workspace_root / "input" / "brs.md").write_text(
            textwrap.dedent(
                """\
                # BRS

                ## Functional Requirements
                - FR-001: The system shall let an analyst submit an intake request.
                """
            ),
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        if self.workspace_root.exists():
            shutil.rmtree(self.workspace_root)

    def read_json(self, relative_path: str) -> dict:
        return json.loads((self.workspace_root / relative_path).read_text(encoding="utf-8"))

    def read_log(self, relative_path: str) -> list[dict]:
        path = self.workspace_root / relative_path
        return [
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    def test_init_workspace_seeds_execution_log(self) -> None:
        workspace_root = RUNTIME_ROOT / f"{self._testMethodName}-workspace"
        if workspace_root.exists():
            shutil.rmtree(workspace_root)
        try:
            run_cli("init-workspace", "--workspace-root", str(workspace_root), "--initiative-id", "I999-LOG")
            execution_log = workspace_root / ".b2s" / "state" / "execution-log.jsonl"
            self.assertTrue(execution_log.exists())
            log_entries = [
                json.loads(line)
                for line in execution_log.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            self.assertEqual(len(log_entries), 1)
            self.assertEqual(log_entries[0]["command"], "init-workspace")
            self.assertEqual(log_entries[0]["initiative_id"], "I999-LOG")
        finally:
            if workspace_root.exists():
                shutil.rmtree(workspace_root)

    def test_reset_to_phase_creates_backup_and_rewinds_next_action(self) -> None:
        run_cli("next-step", "--workspace-root", str(self.workspace_root))
        (self.workspace_root / "routing").mkdir()
        (self.workspace_root / "routing" / "routing-decision.md").write_text(
            textwrap.dedent(
                """\
                # Routing Decision

                ## Decision Summary

                | Decision | Selected value | Reason | Confidence |
                |---|---|---|---|
                | Delivery mode | OpenSpec | scope | High |
                | Execution mode | Standard | scope | Medium |
                | Small-change path applicable? | No | scope | High |
                """
            ),
            encoding="utf-8",
        )
        run_cli("validate-artifact", "--workspace-root", str(self.workspace_root))
        run_cli("update-state", "--workspace-root", str(self.workspace_root), "--action-id", "route-initiative")

        run_cli(
            "reset-to-phase",
            "--workspace-root",
            str(self.workspace_root),
            "--stage-id",
            "0-routing",
        )
        state = self.read_json(".b2s/state/workflow-state.json")
        update = self.read_json(".b2s/tmp/current-state-update.json")
        self.assertEqual(state["current_stage"], "0-routing")
        self.assertEqual(state["next_action"], "route-initiative")
        backup_rel = update["applied_changes"]["backup_path"]
        self.assertTrue((self.workspace_root / backup_rel).exists())

    def test_gate_rejection_writes_current_gate_output(self) -> None:
        run_cli("next-step", "--workspace-root", str(self.workspace_root))
        (self.workspace_root / "routing").mkdir()
        (self.workspace_root / "routing" / "routing-decision.md").write_text(
            textwrap.dedent(
                """\
                # Routing Decision

                ## Decision Summary

                | Decision | Selected value | Reason | Confidence |
                |---|---|---|---|
                | Delivery mode | OpenSpec | scope | High |
                | Execution mode | Standard | scope | Medium |
                | Small-change path applicable? | No | scope | High |
                """
            ),
            encoding="utf-8",
        )
        run_cli("validate-artifact", "--workspace-root", str(self.workspace_root))
        run_cli("update-state", "--workspace-root", str(self.workspace_root), "--action-id", "route-initiative")

        (self.workspace_root / "business-intake").mkdir()
        (self.workspace_root / "business-intake" / "business-intake-summary.md").write_text(
            "# Business Intake Summary\n\n## Executive Summary\n\ntext\n\n## Objectives\n\n| Objective ID | Objective | Success measure | Source reference |\n|---|---|---|---|\n| OBJ-001 | Improve intake flow | Requests are processed faster | input/brs.md |\n\n## Requirements\n\n| Requirement ID | Summary | Business value | Source reference | Acceptance / validation reference |\n|---|---|---|---|---|\n| FR-001 | Submit | value | source | AC-001 |\n\n## PO Review Checklist\n\n- [x] done\n",
            encoding="utf-8",
        )
        run_cli(
            "validate-artifact",
            "--workspace-root",
            str(self.workspace_root),
            "--action-id",
            "create-business-intake-summary",
        )
        run_cli(
            "update-state",
            "--workspace-root",
            str(self.workspace_root),
            "--action-id",
            "create-business-intake-summary",
        )
        run_cli(
            "reject-current-gate",
            "--workspace-root",
            str(self.workspace_root),
            "--reason",
            "needs revision",
        )
        gate_output = self.read_json(".b2s/tmp/current-gate.json")
        state = self.read_json(".b2s/state/workflow-state.json")
        self.assertEqual(gate_output["decision"], "rejected")
        self.assertEqual(state["blocked_reason"], "needs revision")
        self.assertEqual(state["artifact_status"]["business-intake/business-intake-summary.md"], "failed")

    def test_retry_action_after_rejection_preserves_routing(self) -> None:
        # set up routing
        run_cli("next-step", "--workspace-root", str(self.workspace_root))
        (self.workspace_root / "routing").mkdir()
        (self.workspace_root / "routing" / "routing-decision.md").write_text(
            textwrap.dedent(
                """\
                # Routing Decision

                ## Decision Summary

                | Decision | Selected value | Reason | Confidence |
                |---|---|---|---|
                | Delivery mode | OpenSpec | scope | High |
                | Execution mode | Standard | scope | Medium |
                | Small-change path applicable? | No | scope | High |
                """
            ),
            encoding="utf-8",
        )
        run_cli("validate-artifact", "--workspace-root", str(self.workspace_root))
        run_cli("update-state", "--workspace-root", str(self.workspace_root), "--action-id", "route-initiative")

        # create a minimal business intake summary and drive it through to gate rejection
        (self.workspace_root / "business-intake").mkdir()
        (self.workspace_root / "business-intake" / "business-intake-summary.md").write_text(
            "# Business Intake Summary\n\n## Executive Summary\n\ntext\n\n## Objectives\n\n| Objective ID | Objective | Success measure | Source reference |\n|---|---|---|---|\n| OBJ-001 | Improve intake flow | Requests are processed faster | input/brs.md |\n\n## Requirements\n\n| Requirement ID | Summary | Business value | Source reference | Acceptance / validation reference |\n|---|---|---|---|---|\n| FR-001 | Submit | value | source | AC-001 |\n\n## PO Review Checklist\n\n- [x] done\n",
            encoding="utf-8",
        )
        run_cli(
            "validate-artifact",
            "--workspace-root",
            str(self.workspace_root),
            "--action-id",
            "create-business-intake-summary",
        )
        run_cli(
            "update-state",
            "--workspace-root",
            str(self.workspace_root),
            "--action-id",
            "create-business-intake-summary",
        )
        run_cli(
            "reject-current-gate",
            "--workspace-root",
            str(self.workspace_root),
            "--reason",
            "needs revision",
        )

        # retry
        run_cli(
            "retry-action",
            "--workspace-root",
            str(self.workspace_root),
            "--action-id",
            "create-business-intake-summary",
        )
        state = self.read_json(".b2s/state/workflow-state.json")
        update = self.read_json(".b2s/tmp/current-state-update.json")

        # routing must still be accepted
        self.assertEqual(state["action_status"]["route-initiative"], "accepted")
        self.assertEqual(state["artifact_status"]["routing/routing-decision.md"], "accepted")
        # failed action and gate are cleared
        self.assertNotIn("create-business-intake-summary", state["action_status"])
        self.assertNotIn("gate-business-intake-review", state["action_status"])
        self.assertNotIn("business-intake/business-intake-summary.md", state["artifact_status"])
        # blocker cleared, action queued
        self.assertIsNone(state["blocked_reason"])
        self.assertFalse(state["awaiting_human"])
        self.assertEqual(state["next_action"], "create-business-intake-summary")
        # output contract
        self.assertEqual(update["overall"], "pass")
        self.assertEqual(update["applied_changes"]["action_reopened"], "create-business-intake-summary")
        self.assertIsNone(update["gate_state"])

    def test_retry_action_fails_for_non_failed_action(self) -> None:
        run_cli("next-step", "--workspace-root", str(self.workspace_root))
        with self.assertRaises(subprocess.CalledProcessError):
            run_cli(
                "retry-action",
                "--workspace-root",
                str(self.workspace_root),
                "--action-id",
                "route-initiative",
            )


if __name__ == "__main__":
    unittest.main()
