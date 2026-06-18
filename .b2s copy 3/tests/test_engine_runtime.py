"""Engine-level runtime checks for the staged `.b2s` workflow."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import sys
import textwrap
import unittest
from unittest import mock

import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
CLI_PATH = REPO_ROOT / ".b2s" / "scripts" / "b2s_cli.py"
RUNTIME_ROOT = REPO_ROOT / ".b2s" / "tests" / "runtime"
SCRIPT_ROOT = REPO_ROOT / ".b2s" / "scripts"

if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from b2s_engine import validation as validation_module  # noqa: E402


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CLI_PATH), *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=True,
    )


class EngineRuntimeTests(unittest.TestCase):
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

                ## Objectives
                - Improve intake processing speed.

                ## Functional Requirements
                - FR-001: The system shall let an analyst submit an intake request.
                - FR-002: The system shall track request status.
                """
            ),
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        if self.workspace_root.exists():
            shutil.rmtree(self.workspace_root)

    def read_json(self, relative_path: str) -> dict:
        return json.loads((self.workspace_root / relative_path).read_text(encoding="utf-8"))

    def read_yaml(self, relative_path: str) -> dict:
        return yaml.safe_load((self.workspace_root / relative_path).read_text(encoding="utf-8"))

    def read_log(self, relative_path: str) -> list[dict]:
        path = self.workspace_root / relative_path
        return [
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    def test_next_step_then_gate_approval_progresses_to_requirements(self) -> None:
        run_cli("next-step", "--workspace-root", str(self.workspace_root))
        next_step = self.read_json(".b2s/state/next-step.json")
        self.assertEqual(next_step["selected_action"], "route-initiative")

        run_cli("collect-inputs", "--workspace-root", str(self.workspace_root))
        current_inputs = self.read_json(".b2s/tmp/current-inputs.json")
        self.assertEqual(current_inputs["overall"], "pass")
        self.assertEqual(current_inputs["action_id"], "route-initiative")

        (self.workspace_root / "routing").mkdir()
        (self.workspace_root / "routing" / "routing-decision.md").write_text(
            textwrap.dedent(
                """\
                # Routing Decision

                ## Decision Summary

                | Decision | Selected value | Reason | Confidence |
                |---|---|---|---|
                | Delivery mode | OpenSpec | multi-feature initiative | High |
                | Execution mode | Standard | moderate scope | Medium |
                | Small-change path applicable? | No | multiple requirements | High |
                """
            ),
            encoding="utf-8",
        )

        run_cli("validate-artifact", "--workspace-root", str(self.workspace_root))
        validation = self.read_yaml(".b2s/tmp/current-validation.yaml")
        self.assertEqual(validation["overall"], "pass")

        run_cli(
            "update-state",
            "--workspace-root",
            str(self.workspace_root),
            "--action-id",
            "route-initiative",
        )
        state = self.read_json(".b2s/state/workflow-state.json")
        self.assertEqual(state["delivery_mode"], "OpenSpec")
        self.assertEqual(state["next_action"], "create-business-intake-summary")

        (self.workspace_root / "business-intake").mkdir()
        (self.workspace_root / "business-intake" / "business-intake-summary.md").write_text(
            textwrap.dedent(
                """\
                # Business Intake Summary

                ## Executive Summary

                Summary text.

                ## Objectives

                | Objective ID | Objective | Success measure | Source reference |
                |---|---|---|---|
                | OBJ-001 | Improve intake processing speed | Analysts can submit requests faster | input/brs.md |

                ## Requirements

                | Requirement ID | Summary | Business value | Source reference | Acceptance / validation reference |
                |---|---|---|---|---|
                | FR-001 | Submit intake request | Faster intake | input/brs.md | AC-001 |
                | FR-002 | Track request status | Better transparency | input/brs.md | AC-002 |

                ## PO Review Checklist

                - [x] Objectives are understandable and measurable
                """
            ),
            encoding="utf-8",
        )

        run_cli(
            "validate-artifact",
            "--workspace-root",
            str(self.workspace_root),
            "--action-id",
            "create-business-intake-summary",
        )
        validation = self.read_yaml(".b2s/tmp/current-validation.yaml")
        self.assertEqual(validation["overall"], "pass")

        run_cli(
            "update-state",
            "--workspace-root",
            str(self.workspace_root),
            "--action-id",
            "create-business-intake-summary",
        )
        state = self.read_json(".b2s/state/workflow-state.json")
        self.assertTrue(state["awaiting_human"])
        self.assertEqual(state["current_gate"]["gate_id"], "business-intake-review")

        run_cli(
            "approve-current-gate",
            "--workspace-root",
            str(self.workspace_root),
            "--reason",
            "test approval",
        )
        state = self.read_json(".b2s/state/workflow-state.json")
        self.assertFalse(state["awaiting_human"])
        self.assertEqual(state["artifact_status"]["business-intake/business-intake-summary.md"], "accepted")
        self.assertEqual(state["next_action"], "create-requirements")

        run_cli("next-step", "--workspace-root", str(self.workspace_root))
        next_step = self.read_json(".b2s/state/next-step.json")
        self.assertEqual(next_step["selected_action"], "create-requirements")
        self.assertEqual(next_step["selected_stage"], "2b-business-analysis")

    def test_routing_validation_fails_when_decision_values_missing(self) -> None:
        (self.workspace_root / "routing").mkdir()
        (self.workspace_root / "routing" / "routing-decision.md").write_text(
            "# Routing Decision\n\n## Decision Summary\n\n| Decision | Selected value |\n|---|---|\n| Delivery mode | Maybe |\n",
            encoding="utf-8",
        )
        run_cli(
            "validate-artifact",
            "--workspace-root",
            str(self.workspace_root),
            "--action-id",
            "route-initiative",
        )
        validation = self.read_yaml(".b2s/tmp/current-validation.yaml")
        self.assertEqual(validation["overall"], "fail")
        self.assertTrue(any("delivery_mode_present failed" in item for item in validation["failures"]))

    def test_blocked_by_stage_prevents_action_until_stage_complete(self) -> None:
        # create-requirements has blocked_by_stage: ["2-business-intake"]
        # if gate-business-intake-review is not yet complete, next-step must not
        # select create-requirements even if its blocked_by_action is satisfied
        run_cli("next-step", "--workspace-root", str(self.workspace_root))
        (self.workspace_root / "routing").mkdir()
        (self.workspace_root / "routing" / "routing-decision.md").write_text(
            textwrap.dedent(
                """\
                # Routing Decision

                ## Decision Summary

                | Decision | Selected value | Reason | Confidence |
                |---|---|---|---|
                | Delivery mode | OpenSpec | multi-feature | High |
                | Execution mode | Standard | moderate scope | Medium |
                | Small-change path applicable? | No | multiple requirements | High |
                """
            ),
            encoding="utf-8",
        )
        run_cli("validate-artifact", "--workspace-root", str(self.workspace_root))
        run_cli("update-state", "--workspace-root", str(self.workspace_root), "--action-id", "route-initiative")

        (self.workspace_root / "business-intake").mkdir()
        (self.workspace_root / "business-intake" / "business-intake-summary.md").write_text(
            "# Business Intake Summary\n\n## Executive Summary\n\ntext\n\n## Objectives\n\n| Objective ID | Objective | Success measure | Source reference |\n|---|---|---|---|\n| OBJ-001 | Improve intake | Faster processing | input/brs.md |\n\n## Requirements\n\n| Requirement ID | Summary | Business value | Source reference | Acceptance / validation reference |\n|---|---|---|---|---|\n| FR-001 | Submit request | Value | input/brs.md | AC-001 |\n| FR-002 | Track status | Value | input/brs.md | AC-002 |\n\n## PO Review Checklist\n\n- [x] Objectives are understandable and measurable\n",
            encoding="utf-8",
        )
        run_cli("validate-artifact", "--workspace-root", str(self.workspace_root), "--action-id", "create-business-intake-summary")
        run_cli("update-state", "--workspace-root", str(self.workspace_root), "--action-id", "create-business-intake-summary")

        # at this point gate-business-intake-review is waiting_human — stage is
        # incomplete; next-step must not select create-requirements
        run_cli("next-step", "--workspace-root", str(self.workspace_root))
        next_step_result = self.read_json(".b2s/state/next-step.json")
        self.assertNotEqual(next_step_result.get("selected_action"), "create-requirements")
        self.assertEqual(next_step_result["overall"], "fail")

        # now approve the gate — stage becomes complete
        run_cli("approve-current-gate", "--workspace-root", str(self.workspace_root))
        run_cli("next-step", "--workspace-root", str(self.workspace_root))
        next_step_result = self.read_json(".b2s/state/next-step.json")
        self.assertEqual(next_step_result["overall"], "pass")
        self.assertEqual(next_step_result["selected_action"], "create-requirements")

    def test_stage_complete_when_conditional_action_conditions_not_met(self) -> None:
        # The readiness-gate-pending fixture has execution_mode == Standard.
        # identify-software-modules and map-capabilities-to-modules require
        # Enterprise or Enterprise+Modular — their conditions are never met.
        # Stage 3-planning must still be considered complete so that
        # check-engineering-readiness (blocked_by_stage: ["3-planning"]) can run.
        import shutil
        fixtures_root = REPO_ROOT / ".b2s" / "tests" / "fixtures"
        workspace_root = self.workspace_root
        shutil.copytree(fixtures_root / "readiness-gate-pending", workspace_root, dirs_exist_ok=True)

        run_cli("next-step", "--workspace-root", str(workspace_root))
        next_step_result = self.read_json(".b2s/state/next-step.json")
        # generate-initiative-context is the next eligible action (check-engineering-readiness
        # already ai_validated); the important assertion is that the engine does
        # not report a stage-3-planning blocker
        self.assertEqual(next_step_result["overall"], "pass")
        self.assertNotIn("3-planning", (next_step_result.get("blocking_reason") or ""))

    def test_bdd_directory_validation_requires_gherkin(self) -> None:
        bdd_dir = self.workspace_root / "quality-gates" / "bdd"
        bdd_dir.mkdir(parents=True)
        (bdd_dir / "F-001.md").write_text("# Empty Feature\n", encoding="utf-8")
        run_cli(
            "validate-artifact",
            "--workspace-root",
            str(self.workspace_root),
            "--action-id",
            "create-bdd-scenarios",
        )
        validation = self.read_yaml(".b2s/tmp/current-validation.yaml")
        self.assertEqual(validation["overall"], "fail")
        self.assertTrue(any("has_gherkin failed" in item for item in validation["failures"]))

    def test_execution_log_tracks_staged_commands(self) -> None:
        run_cli("next-step", "--workspace-root", str(self.workspace_root))
        run_cli("collect-inputs", "--workspace-root", str(self.workspace_root))

        (self.workspace_root / "routing").mkdir()
        (self.workspace_root / "routing" / "routing-decision.md").write_text(
            textwrap.dedent(
                """\
                # Routing Decision

                ## Decision Summary

                | Decision | Selected value | Reason | Confidence |
                |---|---|---|---|
                | Delivery mode | OpenSpec | multi-feature initiative | High |
                | Execution mode | Standard | moderate scope | Medium |
                | Small-change path applicable? | No | multiple requirements | High |
                """
            ),
            encoding="utf-8",
        )

        run_cli("validate-artifact", "--workspace-root", str(self.workspace_root))
        run_cli(
            "update-state",
            "--workspace-root",
            str(self.workspace_root),
            "--action-id",
            "route-initiative",
        )

        log_entries = self.read_log(".b2s/state/execution-log.jsonl")
        self.assertEqual(
            [entry["command"] for entry in log_entries],
            ["next-step", "collect-inputs", "validate-artifact", "update-state"],
        )
        self.assertEqual(
            [entry["entry_id"] for entry in log_entries],
            ["RUN-00001", "RUN-00002", "RUN-00003", "RUN-00004"],
        )
        self.assertEqual(log_entries[-1]["action_id"], "route-initiative")
        self.assertEqual(log_entries[-1]["details"]["next_action"], "create-business-intake-summary")

    def test_validate_artifact_uses_profile_dispatch_when_no_dedicated_validator_exists(self) -> None:
        (self.workspace_root / "architecture").mkdir()
        (self.workspace_root / "architecture" / "draft-architecture.md").write_text(
            textwrap.dedent(
                """\
                # Draft Architecture

                ## Overview

                This draft architecture covers the initial service design.

                ## Risks

                Integration risk exists if upstream contracts change.
                """
            ),
            encoding="utf-8",
        )
        run_cli(
            "validate-artifact",
            "--workspace-root",
            str(self.workspace_root),
            "--action-id",
            "draft-architecture-from-brs",
        )
        validation = self.read_yaml(".b2s/tmp/current-validation.yaml")
        self.assertEqual(validation["overall"], "pass")
        self.assertEqual(validation["checks"][1]["detail"], "profile: architecture/draft-architecture.md")

    def test_validate_artifact_uses_dedicated_validator_when_available(self) -> None:
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
        run_cli(
            "validate-artifact",
            "--workspace-root",
            str(self.workspace_root),
            "--action-id",
            "route-initiative",
        )
        validation = self.read_yaml(".b2s/tmp/current-validation.yaml")
        self.assertEqual(validation["overall"], "pass")
        self.assertEqual(validation["checks"][1]["detail"], "dedicated: routing/routing-decision.md")
        self.assertTrue(any(check["name"] == "delivery_mode_present" for check in validation["checks"]))

    def test_critical_artifact_without_profile_fails_validation_configuration(self) -> None:
        (self.workspace_root / "architecture").mkdir()
        (self.workspace_root / "architecture" / "architecture-review.md").write_text(
            "# Architecture Review\n\n## Summary\n\nReal text.\n",
            encoding="utf-8",
        )
        state = {
            "active_action": "review-initial-architecture",
            "next_action": "review-initial-architecture",
            "action_status": {},
            "artifact_status": {},
        }
        broken_action = {
            "action_id": "review-initial-architecture",
            "outputs": {"primary": "architecture/architecture-review.md", "secondary": []},
            "artifact_criticality": "critical",
        }
        args = type(
            "Args",
            (),
            {"workspace_root": self.workspace_root, "action_id": "review-initial-architecture", "output": None},
        )()
        with mock.patch.object(validation_module.workspace, "load_state", return_value=state), mock.patch.object(
            validation_module.workspace,
            "load_stage_actions",
            return_value=([broken_action], {"review-initial-architecture": broken_action}),
        ):
            validation_module.run(args)
        validation = self.read_yaml(".b2s/tmp/current-validation.yaml")
        self.assertEqual(validation["overall"], "fail")
        self.assertIn("configuration-fail", validation["checks"][1]["detail"])

    def test_validation_audit_rejects_human_gated_basic_file_profile(self) -> None:
        (self.workspace_root / "architecture").mkdir()
        (self.workspace_root / "architecture" / "architecture-review.md").write_text(
            "# Architecture Review\n\n## Summary\n\nReal text.\n",
            encoding="utf-8",
        )
        state = {
            "active_action": "review-initial-architecture",
            "next_action": "review-initial-architecture",
            "action_status": {},
            "artifact_status": {},
        }
        bad_action = {
            "action_id": "review-initial-architecture",
            "title": "Review initial architecture",
            "artifact_template_ref": ".b2s/artifact-templates/architecture-review.md",
            "outputs": {"primary": "architecture/architecture-review.md", "secondary": []},
            "validation_profile": "basic-file",
            "artifact_criticality": "critical",
            "human_gate": {"required": True},
            "inputs": {"required": [], "optional": []},
        }
        args = type(
            "Args",
            (),
            {"workspace_root": self.workspace_root, "action_id": "review-initial-architecture", "output": None},
        )()
        with mock.patch.object(validation_module.workspace, "load_state", return_value=state), mock.patch.object(
            validation_module.workspace,
            "load_stage_actions",
            return_value=([bad_action], {"review-initial-architecture": bad_action}),
        ):
            validation_module.run(args)
        validation = self.read_yaml(".b2s/tmp/current-validation.yaml")
        self.assertEqual(validation["overall"], "fail")
        audit_failures = [check["detail"] for check in validation["checks"] if check["name"] == "validation_audit" and check["result"] == "fail"]
        self.assertTrue(any("human-gated artifact uses basic-file validation" in detail for detail in audit_failures))

    def test_validation_audit_passes_for_properly_classified_action(self) -> None:
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
        run_cli(
            "validate-artifact",
            "--workspace-root",
            str(self.workspace_root),
            "--action-id",
            "route-initiative",
        )
        validation = self.read_yaml(".b2s/tmp/current-validation.yaml")
        self.assertEqual(validation["overall"], "pass")
        audit_checks = [check for check in validation["checks"] if check["name"] == "validation_audit"]
        self.assertTrue(audit_checks)
        self.assertTrue(all(check["result"] == "pass" for check in audit_checks))

    def test_validation_audit_rejects_high_criticality_profile_without_required_sections(self) -> None:
        (self.workspace_root / "planning").mkdir()
        (self.workspace_root / "planning" / "delivery-structure.md").write_text(
            "# Delivery Structure\n\n## Metadata\n\nText.\n\n## FR Coverage\n\n| FR-NNN | Stories | Status |\n|---|---|---|\n| FR-001 | F-001.1 | Covered |\n",
            encoding="utf-8",
        )
        state = {
            "active_action": "create-delivery-structure",
            "next_action": "create-delivery-structure",
            "action_status": {},
            "artifact_status": {},
        }
        bad_action = {
            "action_id": "create-delivery-structure",
            "title": "Create delivery structure",
            "artifact_template_ref": ".b2s/artifact-templates/delivery-structure.md",
            "outputs": {"primary": "planning/delivery-structure.md", "secondary": []},
            "validation_profile": "structured-document",
            "artifact_criticality": "critical",
            "human_gate": {"required": False},
            "inputs": {"required": [], "optional": []},
        }
        args = type(
            "Args",
            (),
            {"workspace_root": self.workspace_root, "action_id": "create-delivery-structure", "output": None},
        )()
        with mock.patch.object(validation_module.workspace, "load_state", return_value=state), mock.patch.object(
            validation_module.workspace,
            "load_stage_actions",
            return_value=([bad_action], {"create-delivery-structure": bad_action}),
        ):
            validation_module.run(args)
        validation = self.read_yaml(".b2s/tmp/current-validation.yaml")
        self.assertEqual(validation["overall"], "fail")
        audit_failures = [check["detail"] for check in validation["checks"] if check["name"] == "validation_audit" and check["result"] == "fail"]
        self.assertTrue(any("lacks required_sections structural contract" in detail for detail in audit_failures))

    def test_high_criticality_target_set_has_explicit_structural_coverage(self) -> None:
        stage_actions = yaml.safe_load((REPO_ROOT / ".b2s" / "workflow" / "stage-actions.yaml").read_text(encoding="utf-8"))["actions"]
        actions_by_id = {action["action_id"]: action for action in stage_actions}
        targeted = [
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
        ]
        for action_id in targeted:
            action = actions_by_id[action_id]
            artifact_path = action["outputs"]["primary"]
            has_dedicated = artifact_path in validation_module.VALIDATORS_BY_ARTIFACT
            has_required_sections = bool(action.get("required_sections"))
            self.assertTrue(
                has_dedicated or has_required_sections,
                msg=f"{action_id} lacks explicit structural validation coverage",
            )

    def test_evaluate_condition_compound_and(self) -> None:
        """evaluate_condition must handle 'A and B' by requiring both sub-conditions true."""
        from b2s_engine.next_step import evaluate_condition
        from b2s_engine import workspace as ws
        _, actions_by_id = ws.load_stage_actions()

        state_both_true = {
            "action_status": {"gate-engineering-readiness-review": "accepted"},
            "readiness_score": 78,
            "optional_artifacts_requested": [],
            "quality_gates_triggered": [],
        }
        condition = "readiness_score >= 70 and gate-engineering-readiness-review accepted"
        self.assertTrue(
            evaluate_condition(condition, state_both_true, self.workspace_root, actions_by_id),
            "compound 'and' must pass when both sub-conditions are true",
        )

        state_one_false = {
            "action_status": {},
            "readiness_score": 78,
            "optional_artifacts_requested": [],
            "quality_gates_triggered": [],
        }
        self.assertFalse(
            evaluate_condition(condition, state_one_false, self.workspace_root, actions_by_id),
            "compound 'and' must fail when one sub-condition is false",
        )

    def test_evaluate_condition_compound_or(self) -> None:
        """evaluate_condition must handle 'A or B' by requiring at least one sub-condition true."""
        from b2s_engine.next_step import evaluate_condition
        from b2s_engine import workspace as ws
        _, actions_by_id = ws.load_stage_actions()

        state_one_true = {
            "action_status": {},
            "readiness_score": 30,
            "delivery_mode": "OpenSpec",
            "optional_artifacts_requested": [],
            "quality_gates_triggered": [],
        }
        condition = "delivery_mode == OpenSpec or delivery_mode == Standalone"
        self.assertTrue(
            evaluate_condition(condition, state_one_true, self.workspace_root, actions_by_id),
            "compound 'or' must pass when one sub-condition is true",
        )

        state_none_true = {
            "action_status": {},
            "readiness_score": 30,
            "delivery_mode": "Unknown",
            "optional_artifacts_requested": [],
            "quality_gates_triggered": [],
        }
        self.assertFalse(
            evaluate_condition(condition, state_none_true, self.workspace_root, actions_by_id),
            "compound 'or' must fail when no sub-condition is true",
        )

    def test_blocked_by_stage_skips_condition_failing_actions(self) -> None:
        """blocked_by_stage must treat condition-failing actions as satisfied (same as stage_is_complete)."""
        from b2s_engine.next_step import _blocked_by_stage_satisfied
        from b2s_engine import workspace as ws
        _, actions_by_id = ws.load_stage_actions()

        # Mark only the condition-matching actions in 4b-quality-gates as complete;
        # leave condition-failing ones (create-bdd-scenarios, create-threat-model, etc.) absent.
        state = {
            "delivery_mode": "OpenSpec",
            "readiness_score": 78,
            "optional_artifacts_requested": [],
            "quality_gates_triggered": ["TEST_STRATEGY", "SECURITY_REVIEW", "API_CONTRACT", "DATA_CONTRACT", "OBSERVABILITY_PLAN"],
            "action_status": {
                "create-test-strategy": "ai_validated",
                "create-security-review": "ai_validated",
                "create-api-contract": "ai_validated",
                "create-data-contract": "ai_validated",
                "create-observability-plan": "ai_validated",
            },
            "artifact_status": {},
        }
        handoff_action = actions_by_id["create-openspec-handoff"]
        result = _blocked_by_stage_satisfied(handoff_action, state, actions_by_id, self.workspace_root)
        self.assertTrue(
            result,
            "blocked_by_stage must be satisfied when only condition-failing actions are incomplete",
        )

    def test_next_step_does_not_short_circuit_on_stale_blocked_reason(self) -> None:
        """next-step must re-evaluate from scratch rather than propagating a stale blocked_reason."""
        run_cli("next-step", "--workspace-root", str(self.workspace_root))
        next_step = self.read_json(".b2s/state/next-step.json")
        # First run succeeds normally
        self.assertEqual(next_step["overall"], "pass")
        self.assertEqual(next_step["selected_action"], "route-initiative")

        # Simulate a stale blocked_reason written by a previous (now-resolved) next-step run
        state_path = self.workspace_root / ".b2s" / "state" / "workflow-state.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state["blocked_reason"] = "stage `1-routing` is incomplete but no executable action is currently ready"
        state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")

        run_cli("next-step", "--workspace-root", str(self.workspace_root))
        next_step2 = self.read_json(".b2s/state/next-step.json")
        self.assertEqual(next_step2["overall"], "pass", "stale blocked_reason must not prevent next-step from selecting an action")
        self.assertEqual(next_step2["selected_action"], "route-initiative")

    def test_valid_architecture_review_opens_human_gate_after_validation_passes(self) -> None:
        fixtures_root = REPO_ROOT / ".b2s" / "tests" / "fixtures"
        shutil.copytree(fixtures_root / "valid-architecture-review", self.workspace_root, dirs_exist_ok=True)
        run_cli(
            "validate-artifact",
            "--workspace-root",
            str(self.workspace_root),
            "--action-id",
            "review-initial-architecture",
        )
        validation = self.read_yaml(".b2s/tmp/current-validation.yaml")
        self.assertEqual(validation["overall"], "pass")
        run_cli(
            "update-state",
            "--workspace-root",
            str(self.workspace_root),
            "--action-id",
            "review-initial-architecture",
        )
        state = self.read_json(".b2s/state/workflow-state.json")
        self.assertTrue(state["awaiting_human"])
        self.assertEqual(state["current_gate"]["gate_id"], "architecture-review")



class ValidationProfileUnitTests(unittest.TestCase):
    """Unit-level tests for validation module dispatch and criticality enforcement."""

    def _make_action(self, **kwargs: object) -> dict:
        base = {
            "action_id": "test-action",
            "title": "Test Action",
            "outputs": {"primary": "test-output/result.md", "secondary": []},
            "human_gate": {"required": False},
            "artifact_criticality": "low",
        }
        base.update(kwargs)
        return base

    def test_profile_dispatch_uses_analytical_review_when_declared(self) -> None:
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            artifact = Path(tmp) / "result.md"
            artifact.write_text("# Review\n\nsome content\n", encoding="utf-8")
            action = self._make_action(validation_profile="analytical-review", artifact_criticality="high")
            dispatch, _ = validation_module._validator_for_artifact(action, "test-output/result.md", artifact)
            self.assertEqual(dispatch, "profile")

    def test_profile_dispatch_uses_basic_file_when_declared(self) -> None:
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            artifact = Path(tmp) / "result.md"
            artifact.write_text("some content", encoding="utf-8")
            action = self._make_action(validation_profile="basic-file", artifact_criticality="low")
            dispatch, _ = validation_module._validator_for_artifact(action, "test-output/result.md", artifact)
            self.assertEqual(dispatch, "profile")

    def test_profile_dispatch_configuration_fail_for_critical_without_profile(self) -> None:
        """A critical action with no profile and no dedicated validator must resolve to configuration-fail."""
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            artifact = Path(tmp) / "result.md"
            artifact.write_text("some content", encoding="utf-8")
            action = self._make_action(artifact_criticality="critical")
            dispatch, _ = validation_module._validator_for_artifact(action, "test-output/result.md", artifact)
            self.assertEqual(dispatch, "configuration-fail")

    def test_profile_dispatch_configuration_fail_for_high_without_profile(self) -> None:
        """A high-criticality action with no profile and no dedicated validator must resolve to configuration-fail."""
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            artifact = Path(tmp) / "result.md"
            artifact.write_text("some content", encoding="utf-8")
            action = self._make_action(artifact_criticality="high")
            dispatch, _ = validation_module._validator_for_artifact(action, "test-output/result.md", artifact)
            self.assertEqual(dispatch, "configuration-fail")

    def test_profile_dispatch_fallback_for_low_without_profile(self) -> None:
        """A low-criticality action with no profile and no dedicated validator falls back to generic."""
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            artifact = Path(tmp) / "result.md"
            artifact.write_text("some content", encoding="utf-8")
            action = self._make_action(artifact_criticality="low")
            dispatch, _ = validation_module._validator_for_artifact(action, "test-output/result.md", artifact)
            self.assertEqual(dispatch, "fallback")

    def test_profile_dispatch_unknown_profile_name_resolves_to_configuration_fail(self) -> None:
        """An unrecognized profile name must resolve to configuration-fail, not silently fallback."""
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            artifact = Path(tmp) / "result.md"
            artifact.write_text("some content", encoding="utf-8")
            action = self._make_action(validation_profile="nonexistent-profile", artifact_criticality="high")
            dispatch, _ = validation_module._validator_for_artifact(action, "test-output/result.md", artifact)
            self.assertEqual(dispatch, "configuration-fail")

    def test_audit_check_fails_for_human_gated_basic_file_action(self) -> None:
        """A human-gated artifact using basic-file validation must produce a failing audit check."""
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            artifact = Path(tmp) / "result.md"
            artifact.write_text("some content", encoding="utf-8")
            action = self._make_action(
                validation_profile="basic-file",
                artifact_criticality="high",
                human_gate={"required": True, "gate_id": "test-gate"},
            )
            _, actions_by_id = validation_module.workspace.load_stage_actions()
            audit_checks = validation_module._audit_validation_coverage(
                action, actions_by_id, "test-output/result.md", "profile"
            )
            self.assertTrue(
                any(c["result"] == "fail" for c in audit_checks),
                "audit must flag human-gated artifact using basic-file validation",
            )


if __name__ == "__main__":
    unittest.main()
