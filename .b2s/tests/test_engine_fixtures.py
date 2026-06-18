"""Static fixture checks for staged `.b2s` repair and input behavior."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import sys
import unittest

import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
CLI_PATH = REPO_ROOT / ".b2s" / "scripts" / "b2s_cli.py"
FIXTURES_ROOT = REPO_ROOT / ".b2s" / "tests" / "fixtures"
RUNTIME_ROOT = REPO_ROOT / ".b2s" / "tests" / "runtime"
SCRIPT_ROOT = REPO_ROOT / ".b2s" / "scripts"

if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from b2s_engine import next_step, workspace  # noqa: E402


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CLI_PATH), *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=True,
    )


class EngineFixtureTests(unittest.TestCase):
    def setUp(self) -> None:
        RUNTIME_ROOT.mkdir(parents=True, exist_ok=True)
        self.workspace_root = RUNTIME_ROOT / self._testMethodName
        if self.workspace_root.exists():
            shutil.rmtree(self.workspace_root)

    def tearDown(self) -> None:
        if self.workspace_root.exists():
            shutil.rmtree(self.workspace_root)

    def materialize_fixture(self, name: str) -> None:
        shutil.copytree(FIXTURES_ROOT / name, self.workspace_root)

    def read_json(self, relative_path: str) -> dict:
        return json.loads((self.workspace_root / relative_path).read_text(encoding="utf-8"))

    def read_yaml(self, relative_path: str) -> dict:
        return yaml.safe_load((self.workspace_root / relative_path).read_text(encoding="utf-8"))

    def test_collect_inputs_reports_missing_brs(self) -> None:
        self.materialize_fixture("missing-brs")
        run_cli(
            "collect-inputs",
            "--workspace-root",
            str(self.workspace_root),
            "--action-id",
            "route-initiative",
        )
        inputs = self.read_json(".b2s/tmp/current-inputs.json")
        self.assertEqual(inputs["overall"], "fail")
        self.assertEqual(inputs["missing_required_inputs"], ["input/brs.md"])
        self.assertEqual(
            inputs["prompt_placeholders"]["required_inputs"],
            ["input/brs.md"],
        )
        self.assertEqual(
            inputs["prompt_placeholders"]["resolved_required_inputs"],
            [],
        )
        self.assertEqual(
            inputs["prompt_placeholders"]["primary_output"],
            "routing/routing-decision.md",
        )
        self.assertEqual(
            inputs["prompt_placeholders"]["secondary_outputs"],
            [],
        )

    def test_next_step_from_valid_business_intake_fixture_selects_requirements(self) -> None:
        self.materialize_fixture("valid-business-intake-flow")
        run_cli("next-step", "--workspace-root", str(self.workspace_root))
        next_step = self.read_json(".b2s/state/next-step.json")
        self.assertEqual(next_step["overall"], "pass")
        self.assertEqual(next_step["selected_action"], "create-requirements")
        self.assertEqual(next_step["selected_stage"], "2b-business-analysis")

    def test_validate_artifact_passes_for_valid_business_intake_fixture(self) -> None:
        self.materialize_fixture("valid-business-intake-flow")
        run_cli(
            "validate-artifact",
            "--workspace-root",
            str(self.workspace_root),
            "--action-id",
            "create-business-intake-summary",
        )
        validation = self.read_yaml(".b2s/tmp/current-validation.yaml")
        self.assertEqual(validation["overall"], "pass")

    def test_validate_artifact_fails_when_requirements_artifact_missing(self) -> None:
        self.materialize_fixture("missing-requirements-artifact")
        run_cli(
            "validate-artifact",
            "--workspace-root",
            str(self.workspace_root),
            "--action-id",
            "create-requirements",
        )
        validation = self.read_yaml(".b2s/tmp/current-validation.yaml")
        self.assertEqual(validation["overall"], "fail")
        self.assertTrue(any("Missing artifact: business-analysis/requirements.md" == item for item in validation["failures"]))

    def test_validate_artifact_fails_for_skeleton_business_intake(self) -> None:
        self.materialize_fixture("skeleton-business-intake")
        run_cli(
            "validate-artifact",
            "--workspace-root",
            str(self.workspace_root),
            "--action-id",
            "create-business-intake-summary",
        )
        validation = self.read_yaml(".b2s/tmp/current-validation.yaml")
        self.assertEqual(validation["overall"], "fail")
        self.assertTrue(any("requirements_not_too_small failed" in item for item in validation["failures"]))

    def test_validate_artifact_fails_for_template_requirements(self) -> None:
        self.materialize_fixture("template-requirements")
        run_cli(
            "validate-artifact",
            "--workspace-root",
            str(self.workspace_root),
            "--action-id",
            "create-requirements",
        )
        validation = self.read_yaml(".b2s/tmp/current-validation.yaml")
        self.assertEqual(validation["overall"], "fail")
        self.assertTrue(any("fr_not_template_only failed" in item for item in validation["failures"]))

    def test_validate_artifact_fails_for_shallow_use_cases(self) -> None:
        self.materialize_fixture("shallow-use-cases")
        run_cli(
            "validate-artifact",
            "--workspace-root",
            str(self.workspace_root),
            "--action-id",
            "create-use-case-diagram",
        )
        validation = self.read_yaml(".b2s/tmp/current-validation.yaml")
        self.assertEqual(validation["overall"], "fail")
        self.assertTrue(any("uc_coverage_not_too_shallow failed" in item for item in validation["failures"]))

    def test_validate_artifact_fails_for_readiness_missing_justification(self) -> None:
        self.materialize_fixture("readiness-missing-justification")
        run_cli(
            "validate-artifact",
            "--workspace-root",
            str(self.workspace_root),
            "--action-id",
            "check-engineering-readiness",
        )
        validation = self.read_yaml(".b2s/tmp/current-validation.yaml")
        self.assertEqual(validation["overall"], "fail")
        self.assertTrue(any("no_gates_have_justification failed" in item for item in validation["failures"]))

    def test_validate_artifact_fails_for_placeholder_architecture_review(self) -> None:
        self.materialize_fixture("placeholder-architecture-review")
        run_cli(
            "validate-artifact",
            "--workspace-root",
            str(self.workspace_root),
            "--action-id",
            "review-initial-architecture",
        )
        validation = self.read_yaml(".b2s/tmp/current-validation.yaml")
        self.assertEqual(validation["overall"], "fail")
        self.assertTrue(any("tmpl_section_" in item for item in validation["failures"]))

    def test_validate_artifact_passes_for_valid_architecture_review(self) -> None:
        self.materialize_fixture("valid-architecture-review")
        run_cli(
            "validate-artifact",
            "--workspace-root",
            str(self.workspace_root),
            "--action-id",
            "review-initial-architecture",
        )
        validation = self.read_yaml(".b2s/tmp/current-validation.yaml")
        self.assertEqual(validation["overall"], "pass")
        self.assertTrue(any(check["name"] == "validation_audit" and check["result"] == "pass" for check in validation["checks"]))

    def test_repair_state_recreates_pending_business_intake_gate(self) -> None:
        self.materialize_fixture("pending-gate")
        run_cli("repair-state", "--workspace-root", str(self.workspace_root))
        state = self.read_json(".b2s/state/workflow-state.json")
        update = self.read_json(".b2s/tmp/current-state-update.json")
        self.assertTrue(state["awaiting_human"])
        self.assertEqual(state["current_gate"]["gate_id"], "business-intake-review")
        self.assertEqual(state["action_status"]["create-business-intake-summary"], "ai_validated")
        self.assertEqual(state["action_status"]["gate-business-intake-review"], "waiting_human")
        self.assertIsNone(state["next_action"])
        self.assertEqual(update["gate_state"]["gate_id"], "business-intake-review")

    def test_repair_state_drops_stale_downstream_statuses(self) -> None:
        self.materialize_fixture("stale-downstream")
        run_cli("repair-state", "--workspace-root", str(self.workspace_root))
        state = self.read_json(".b2s/state/workflow-state.json")
        self.assertEqual(state["next_action"], "create-business-intake-summary")
        self.assertNotIn("create-requirements", state["action_status"])
        self.assertNotIn("business-analysis/requirements.md", state["artifact_status"])
        self.assertEqual(state["action_status"]["route-initiative"], "accepted")

    def test_repair_state_recreates_pending_readiness_gate(self) -> None:
        self.materialize_fixture("readiness-gate-pending")
        run_cli("repair-state", "--workspace-root", str(self.workspace_root))
        state = self.read_json(".b2s/state/workflow-state.json")
        self.assertTrue(state["awaiting_human"])
        self.assertEqual(state["current_gate"]["gate_id"], "engineering-readiness-review")
        self.assertEqual(state["action_status"]["check-engineering-readiness"], "ai_validated")
        self.assertEqual(state["action_status"]["gate-engineering-readiness-review"], "waiting_human")
        self.assertIsNone(state["next_action"])

    def test_retry_action_reopens_failed_action_from_fixture(self) -> None:
        self.materialize_fixture("rejected-gate")
        run_cli(
            "retry-action",
            "--workspace-root",
            str(self.workspace_root),
            "--action-id",
            "create-business-intake-summary",
        )
        state = self.read_json(".b2s/state/workflow-state.json")
        update = self.read_json(".b2s/tmp/current-state-update.json")
        # routing must remain accepted
        self.assertEqual(state["action_status"]["route-initiative"], "accepted")
        self.assertEqual(state["artifact_status"]["routing/routing-decision.md"], "accepted")
        # failed action and its gate are cleared
        self.assertNotIn("create-business-intake-summary", state["action_status"])
        self.assertNotIn("gate-business-intake-review", state["action_status"])
        self.assertNotIn("business-intake/business-intake-summary.md", state["artifact_status"])
        # blocker is gone, action is queued
        self.assertIsNone(state["blocked_reason"])
        self.assertFalse(state["awaiting_human"])
        self.assertEqual(state["next_action"], "create-business-intake-summary")
        # machine-readable output contract
        self.assertEqual(update["overall"], "pass")
        self.assertEqual(update["action_id"], "create-business-intake-summary")
        self.assertEqual(update["applied_changes"]["action_reopened"], "create-business-intake-summary")
        self.assertEqual(update["next_action"], "create-business-intake-summary")
        self.assertIsNone(update["gate_state"])

    def test_retry_action_rejects_non_failed_action(self) -> None:
        self.materialize_fixture("rejected-gate")
        with self.assertRaises(subprocess.CalledProcessError):
            run_cli(
                "retry-action",
                "--workspace-root",
                str(self.workspace_root),
                "--action-id",
                "route-initiative",
            )

    def test_next_step_after_retry_selects_retried_action(self) -> None:
        self.materialize_fixture("rejected-gate")
        run_cli(
            "retry-action",
            "--workspace-root",
            str(self.workspace_root),
            "--action-id",
            "create-business-intake-summary",
        )
        run_cli("next-step", "--workspace-root", str(self.workspace_root))
        next_step_result = self.read_json(".b2s/state/next-step.json")
        self.assertEqual(next_step_result["overall"], "pass")
        self.assertEqual(next_step_result["selected_action"], "create-business-intake-summary")

    # --- Validation profile tests ---

    def test_validate_artifact_passes_for_minimal_architecture_review(self) -> None:
        """Minimal fixture — just enough content to satisfy all analytical-review checks."""
        self.materialize_fixture("minimal-architecture-review")
        run_cli(
            "validate-artifact",
            "--workspace-root",
            str(self.workspace_root),
            "--action-id",
            "review-initial-architecture",
        )
        validation = self.read_yaml(".b2s/tmp/current-validation.yaml")
        self.assertEqual(validation["overall"], "pass")

    def test_validate_artifact_template_dispatch_is_recorded_for_architecture_review(self) -> None:
        """The validation_dispatch check must be present and the outer dispatch must be template."""
        self.materialize_fixture("valid-architecture-review")
        run_cli(
            "validate-artifact",
            "--workspace-root",
            str(self.workspace_root),
            "--action-id",
            "review-initial-architecture",
        )
        validation = self.read_yaml(".b2s/tmp/current-validation.yaml")
        dispatch_checks = [c for c in validation["checks"] if c["name"] == "validation_dispatch"]
        self.assertTrue(dispatch_checks, "validation_dispatch check must be present")
        self.assertTrue(
            any(c["detail"].startswith("template:") for c in dispatch_checks),
            "outer dispatch check must record template dispatch for actions with artifact_template_ref",
        )

    def test_validate_artifact_audit_check_passes_for_valid_architecture_review(self) -> None:
        """validation_audit must pass for a correctly classified critical action."""
        self.materialize_fixture("valid-architecture-review")
        run_cli(
            "validate-artifact",
            "--workspace-root",
            str(self.workspace_root),
            "--action-id",
            "review-initial-architecture",
        )
        validation = self.read_yaml(".b2s/tmp/current-validation.yaml")
        audit_checks = [c for c in validation["checks"] if c["name"] == "validation_audit"]
        self.assertTrue(audit_checks, "validation_audit check must be present")
        self.assertTrue(
            all(c["result"] == "pass" for c in audit_checks),
            "all validation_audit checks must pass for a well-classified critical action",
        )

    def test_validate_artifact_placeholder_analytical_review_fails_multiple_checks(self) -> None:
        """Placeholder text satisfies non-empty but fails structural analytical-review checks."""
        self.materialize_fixture("placeholder-architecture-review")
        run_cli(
            "validate-artifact",
            "--workspace-root",
            str(self.workspace_root),
            "--action-id",
            "review-initial-architecture",
        )
        validation = self.read_yaml(".b2s/tmp/current-validation.yaml")
        self.assertEqual(validation["overall"], "fail")
        self.assertTrue(
            any("tmpl_section_" in item for item in validation["failures"]),
            "placeholder review must fail template section checks",
        )
        self.assertTrue(
            any("tmpl_content_depth failed" in item for item in validation["failures"]),
            "placeholder review must fail the template content depth check",
        )


    # --- rerun-last-action tests ---

    def test_rerun_last_action_clears_ai_validated_action_and_gate(self) -> None:
        """rerun-last-action on ai_validated action clears it and its gate, sets next_action."""
        self.materialize_fixture("gate-pending-architecture")
        run_cli("rerun-last-action", "--workspace-root", str(self.workspace_root))
        state = self.read_json(".b2s/state/workflow-state.json")
        update = self.read_json(".b2s/tmp/rerun-last-action.json")
        # upstream accepted state preserved
        self.assertEqual(state["action_status"]["route-initiative"], "accepted")
        self.assertEqual(state["action_status"]["create-business-intake-summary"], "accepted")
        # reopened action and gate cleared
        self.assertNotIn("review-initial-architecture", state["action_status"])
        self.assertNotIn("gate-architecture-review", state["action_status"])
        self.assertNotIn("architecture/architecture-review.md", state["artifact_status"])
        # gate state cleared
        self.assertFalse(state["awaiting_human"])
        self.assertIsNone(state["current_gate"])
        self.assertIsNone(state["blocked_reason"])
        # next action set to the reopened action
        self.assertEqual(state["next_action"], "review-initial-architecture")
        self.assertEqual(state["active_action"], "review-initial-architecture")
        # output contract
        self.assertEqual(update["overall"], "pass")
        self.assertEqual(update["action_id"], "review-initial-architecture")
        self.assertEqual(update["applied_changes"]["action_reopened"], "review-initial-architecture")
        self.assertEqual(update["next_action"], "review-initial-architecture")

    def test_rerun_last_action_rejects_accepted_action(self) -> None:
        """rerun-last-action must fail when last_completed_action is accepted (human-approved)."""
        self.materialize_fixture("accepted-action")
        with self.assertRaises(subprocess.CalledProcessError):
            run_cli("rerun-last-action", "--workspace-root", str(self.workspace_root))

    def test_rerun_last_action_sets_next_action_in_state(self) -> None:
        """After rerun, workflow state must point next_action at the reopened action."""
        self.materialize_fixture("gate-pending-architecture")
        run_cli("rerun-last-action", "--workspace-root", str(self.workspace_root))
        state = self.read_json(".b2s/state/workflow-state.json")
        self.assertEqual(state["next_action"], "review-initial-architecture")
        self.assertEqual(state["active_action"], "review-initial-architecture")
        self.assertFalse(state["awaiting_human"])
        self.assertIsNone(state["blocked_reason"])


class StoryPackageValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        RUNTIME_ROOT.mkdir(parents=True, exist_ok=True)
        self.workspace_root = RUNTIME_ROOT / self._testMethodName
        if self.workspace_root.exists():
            shutil.rmtree(self.workspace_root)

    def tearDown(self) -> None:
        if self.workspace_root.exists():
            shutil.rmtree(self.workspace_root)

    def materialize_fixture(self, name: str) -> None:
        shutil.copytree(FIXTURES_ROOT / name, self.workspace_root)

    def read_yaml(self, relative_path: str) -> dict:
        return yaml.safe_load((self.workspace_root / relative_path).read_text(encoding="utf-8"))

    def test_validate_story_package_fails_for_shallow_story(self) -> None:
        self.materialize_fixture("shallow-story-package")
        run_cli(
            "validate-artifact",
            "--workspace-root", str(self.workspace_root),
            "--action-id", "create-openspec-handoff",
        )
        validation = self.read_yaml(".b2s/tmp/current-validation.yaml")
        self.assertEqual(validation["overall"], "fail")
        failures = " ".join(validation["failures"])
        self.assertIn("story_not_generic_title", failures)
        self.assertIn("story_has_bdd_scenarios", failures)
        self.assertIn("story_has_coding_prompt", failures)

    def test_validate_story_package_passes_for_valid_story(self) -> None:
        self.materialize_fixture("valid-story-package")
        run_cli(
            "validate-artifact",
            "--workspace-root", str(self.workspace_root),
            "--action-id", "create-openspec-handoff",
        )
        validation = self.read_yaml(".b2s/tmp/current-validation.yaml")
        self.assertEqual(validation["overall"], "pass")


class TechnicalSpecValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        RUNTIME_ROOT.mkdir(parents=True, exist_ok=True)
        self.workspace_root = RUNTIME_ROOT / self._testMethodName
        if self.workspace_root.exists():
            shutil.rmtree(self.workspace_root)

    def tearDown(self) -> None:
        if self.workspace_root.exists():
            shutil.rmtree(self.workspace_root)

    def materialize_fixture(self, name: str) -> None:
        shutil.copytree(FIXTURES_ROOT / name, self.workspace_root)

    def read_yaml(self, relative_path: str) -> dict:
        return yaml.safe_load((self.workspace_root / relative_path).read_text(encoding="utf-8"))

    def test_validate_exposed_api_spec_fails_for_shallow(self) -> None:
        self.materialize_fixture("shallow-exposed-api-spec")
        run_cli(
            "validate-artifact",
            "--workspace-root", str(self.workspace_root),
            "--action-id", "create-exposed-api-specs",
        )
        validation = self.read_yaml(".b2s/tmp/current-validation.yaml")
        self.assertEqual(validation["overall"], "fail")
        failures = " ".join(validation["failures"])
        self.assertIn("exposed_api_has_endpoints", failures)
        self.assertIn("exposed_api_has_contract_mode", failures)
        self.assertIn("exposed_api_no_placeholders", failures)

    def test_validate_exposed_api_spec_passes_for_valid(self) -> None:
        self.materialize_fixture("valid-exposed-api-spec")
        run_cli(
            "validate-artifact",
            "--workspace-root", str(self.workspace_root),
            "--action-id", "create-exposed-api-specs",
        )
        validation = self.read_yaml(".b2s/tmp/current-validation.yaml")
        self.assertEqual(validation["overall"], "pass")

    def test_validate_consumed_api_spec_fails_for_shallow(self) -> None:
        self.materialize_fixture("shallow-consumed-api-spec")
        run_cli(
            "validate-artifact",
            "--workspace-root", str(self.workspace_root),
            "--action-id", "create-consumed-api-specs",
        )
        validation = self.read_yaml(".b2s/tmp/current-validation.yaml")
        self.assertEqual(validation["overall"], "fail")
        failures = " ".join(validation["failures"])
        self.assertIn("consumed_api_has_endpoints", failures)
        self.assertIn("consumed_api_has_auth", failures)
        self.assertIn("consumed_api_no_placeholders", failures)

    def test_validate_consumed_api_spec_passes_for_valid(self) -> None:
        self.materialize_fixture("valid-consumed-api-spec")
        run_cli(
            "validate-artifact",
            "--workspace-root", str(self.workspace_root),
            "--action-id", "create-consumed-api-specs",
        )
        validation = self.read_yaml(".b2s/tmp/current-validation.yaml")
        self.assertEqual(validation["overall"], "pass")

    def test_validate_integration_spec_fails_for_shallow(self) -> None:
        self.materialize_fixture("shallow-integration-spec")
        run_cli(
            "validate-artifact",
            "--workspace-root", str(self.workspace_root),
            "--action-id", "create-integration-specs",
        )
        validation = self.read_yaml(".b2s/tmp/current-validation.yaml")
        self.assertEqual(validation["overall"], "fail")
        failures = " ".join(validation["failures"])
        self.assertIn("integration_has_timeout", failures)
        self.assertIn("integration_has_events", failures)
        self.assertIn("integration_no_placeholders", failures)

    def test_validate_integration_spec_passes_for_valid(self) -> None:
        self.materialize_fixture("valid-integration-spec")
        run_cli(
            "validate-artifact",
            "--workspace-root", str(self.workspace_root),
            "--action-id", "create-integration-specs",
        )
        validation = self.read_yaml(".b2s/tmp/current-validation.yaml")
        self.assertEqual(validation["overall"], "pass")

    def test_technical_spec_validators_are_registered_as_dedicated(self) -> None:
        """All three tech-spec validators must dispatch as dedicated, not profile or fallback."""
        import tempfile
        from b2s_engine import validation as validation_module
        import yaml as _yaml

        tsm_sa_path = REPO_ROOT / ".b2s" / "workflow-types" / "technical-spec-modular" / "stage-actions.yaml"
        actions = _yaml.safe_load(tsm_sa_path.read_text(encoding="utf-8"))["actions"]
        actions_by_id = {a["action_id"]: a for a in actions}

        targets = [
            ("create-exposed-api-specs", "technical-specifications/api/exposed/"),
            ("create-consumed-api-specs", "technical-specifications/api/consumed/"),
            ("create-integration-specs", "technical-specifications/integrations/"),
        ]
        with tempfile.TemporaryDirectory() as tmp:
            for action_id, artifact_path in targets:
                action = actions_by_id[action_id]
                dir_path = Path(tmp) / artifact_path
                dir_path.mkdir(parents=True, exist_ok=True)
                dispatch, _ = validation_module._validator_for_artifact(action, artifact_path, dir_path)
                self.assertEqual(
                    dispatch, "dedicated",
                    msg=f"{action_id}: expected dedicated dispatch for {artifact_path}, got {dispatch}",
                )


class WorkflowLoadingTests(unittest.TestCase):

    def test_local_workflow_is_used_when_present(self):
        """When initiative has .b2s/workflow/stage-actions.yaml, it is used instead of central."""
        ws = FIXTURES_ROOT / "local-workflow-override"
        actions, by_id = workspace.load_stage_actions(workspace_root=ws)
        action_ids = [a["action_id"] for a in actions]
        self.assertNotIn("create-requirements", action_ids)
        self.assertIn("route-initiative", action_ids)

    def test_central_workflow_used_when_no_local(self):
        """When initiative has no .b2s/workflow/, central stage-actions.yaml is used."""
        ws = FIXTURES_ROOT / "no-local-workflow"
        actions, by_id = workspace.load_stage_actions(workspace_root=ws)
        action_ids = [a["action_id"] for a in actions]
        self.assertIn("create-requirements", action_ids)

    def test_workflow_source_local(self):
        """active_workflow_source returns 'local' when initiative has local workflow."""
        ws = FIXTURES_ROOT / "local-workflow-override"
        self.assertEqual(workspace.active_workflow_source(ws), "local")

    def test_workflow_source_central(self):
        """active_workflow_source returns 'central' when initiative has no local workflow."""
        ws = FIXTURES_ROOT / "no-local-workflow"
        self.assertEqual(workspace.active_workflow_source(ws), "central")

    def test_next_step_uses_local_workflow(self):
        """next_step.select_next_action uses initiative-local workflow when present."""
        ws = FIXTURES_ROOT / "local-workflow-override"
        state = workspace.load_state(ws)
        result = next_step.select_next_action(ws, state)
        self.assertEqual(result["selected_action"], "route-initiative")
        self.assertEqual(result["selected_stage"], "0-routing")


if __name__ == "__main__":
    unittest.main()
