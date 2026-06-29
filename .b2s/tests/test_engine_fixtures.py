"""Static fixture checks for staged `.b2s` repair and input behavior."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
CLI_PATH = REPO_ROOT / ".b2s" / "scripts" / "b2s_cli.py"
FIXTURES_ROOT = REPO_ROOT / ".b2s" / "tests" / "fixtures"
RUNTIME_ROOT = REPO_ROOT / ".b2s" / "tests" / "runtime"
SCRIPT_ROOT = REPO_ROOT / ".b2s" / "scripts"

if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from b2s_engine import next_step, workspace  # noqa: E402
from b2s_engine import action_contract, inputs as inputs_module  # noqa: E402
from b2s_engine import dispatch as dispatch_module  # noqa: E402
from b2s_engine import validation as validation_module  # noqa: E402
from b2s_engine import dynamic_next_step as dynamic_next_step_module  # noqa: E402
from b2s_engine import dynamic_state as dynamic_state_module  # noqa: E402


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
            inputs["prompt_placeholders"]["resolved_policy_inputs"],
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
        self.assertEqual(inputs["prompt_placeholders"]["prompt_family"], "b2s")
        self.assertEqual(inputs["prompt_placeholders"]["template_mode"], "strict")

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

    def test_stage_actions_are_normalized_with_v2_defaults(self):
        """Central workflow actions should expose additive v2 defaults when fields are omitted."""
        actions, by_id = workspace.load_stage_actions()
        action = by_id["route-initiative"]
        self.assertEqual(action["prompt_family"], "b2s")
        self.assertEqual(action["policy_refs"], [])
        self.assertEqual(action["template_mode"], "strict")
        self.assertEqual(action["validation_rules"]["required"], [])
        self.assertEqual(action["validation_rules"]["optional"], [])

    def test_stage_actions_preserve_seeded_v2_metadata(self):
        """Representative actions should retain their explicit v2 metadata after normalization."""
        actions, by_id = workspace.load_stage_actions()
        requirements = by_id["create-requirements"]
        self.assertEqual(requirements["prompt_family"], "speckit")
        self.assertEqual(
            requirements["policy_refs"],
            [
                ".b2s/policies/requirements/definition-of-ready.md",
                ".b2s/policies/requirements/requirement-writing-standard.md",
            ],
        )
        self.assertEqual(requirements["template_mode"], "strict")
        self.assertIn("requirement_has_id", requirements["validation_rules"]["required"])

        nfr = by_id["create-nfr-assessment"]
        self.assertEqual(nfr["prompt_family"], "b2s")
        self.assertEqual(
            nfr["policy_refs"],
            [
                ".b2s/policies/security/security-policy.md",
                ".b2s/policies/nfr/availability-standard.md",
                ".b2s/policies/nfr/performance-standard.md",
                ".b2s/policies/nfr/regulatory-standard.md",
            ],
        )
        self.assertIn("nfr_assessment_covers_core_domains", nfr["validation_rules"]["required"])

    def test_old_style_action_record_remains_compatible_across_engine_surfaces(self):
        """An old-style action with no v2 metadata should still normalize, collect inputs, dispatch, and validate."""
        ws = FIXTURES_ROOT / "local-workflow-override"
        old_action = {
            "action_id": "legacy-route",
            "title": "Legacy route",
            "persona": "orchestrator",
            "skill_ref": ".b2s/skills/orchestrator/route-initiative.md",
            "artifact_template_ref": ".b2s/artifact-templates/routing-decision.md",
            "inputs": {"required": ["input/brs.md"]},
            "outputs": {"primary": "routing/routing-decision.md"},
            "human_gate": {"required": False},
            "artifact_criticality": "high",
        }
        normalized = action_contract.normalize_action(old_action)
        self.assertEqual(normalized["prompt_family"], "b2s")
        self.assertEqual(normalized["policy_refs"], [])
        self.assertEqual(normalized["template_mode"], "strict")
        self.assertEqual(normalized["validation_rules"], {"required": [], "optional": []})

        collected = inputs_module.collect_action_inputs(normalized, ws)
        self.assertEqual(collected["overall"], "pass")
        self.assertEqual(collected["prompt_placeholders"]["resolved_required_inputs"], ["input/brs.md"])
        self.assertEqual(collected["prompt_placeholders"]["resolved_policy_inputs"], [])

        summary = dispatch_module._action_summary(normalized, ws)
        self.assertEqual(summary["prompt_family"], "b2s")
        self.assertTrue(summary["skill_exists"])
        self.assertIsNotNone(summary["rendered_skill_text"])

        with mock.patch.object(validation_module.workspace, "load_stage_actions", return_value=([], {})):
            artifact = Path("C:/tmp/legacy-route.md")
            dispatch, _ = validation_module._validator_for_artifact(
                normalized,
                "routing/routing-decision.md",
                artifact,
            )
        self.assertIn(dispatch, {"dedicated", "template", "profile"})

    def test_mixed_family_local_workflow_fixture_loads_expected_families(self):
        ws = FIXTURES_ROOT / "mixed-family-local-workflow"
        actions, by_id = workspace.load_stage_actions(workspace_root=ws)
        self.assertEqual(by_id["create-business-intake-summary"]["prompt_family"], "b2s")
        self.assertEqual(by_id["create-requirements"]["prompt_family"], "speckit")
        self.assertEqual(by_id["review-initial-architecture"]["prompt_family"], "b2s")
        self.assertEqual(by_id["create-openspec-handoff"]["prompt_family"], "hve")
        self.assertEqual(len(actions), 5)

    def test_mixed_family_local_workflow_dispatches_requirements_step(self):
        ws = FIXTURES_ROOT / "mixed-family-local-workflow"
        plan = dispatch_module.build_plan(ws)
        self.assertEqual(plan["status"], "ready")
        self.assertEqual(plan["action"]["action_id"], "create-requirements")
        self.assertEqual(plan["action"]["prompt_family"], "speckit")
        self.assertEqual(
            plan["action"]["prompt_placeholders"]["resolved_policy_inputs"],
            [
                ".b2s/policies/requirements/definition-of-ready.md",
                ".b2s/policies/requirements/requirement-writing-standard.md",
            ],
        )

    def test_b2s_dynamic_workflow_type_is_registered(self):
        index_path = REPO_ROOT / ".b2s" / "workflow-types" / "index.yaml"
        payload = yaml.safe_load(index_path.read_text(encoding="utf-8"))
        entries = {entry["id"]: entry for entry in payload["workflow_types"]}
        self.assertIn("b2s-dynamic", entries)
        self.assertEqual(
            entries["b2s-dynamic"]["path"],
            ".b2s/workflow-types/b2s-dynamic",
        )

    def test_b2s_dynamic_workflow_scaffold_files_exist_and_parse(self):
        workflow_root = REPO_ROOT / ".b2s" / "workflow-types" / "b2s-dynamic"
        self.assertTrue((workflow_root / "README.md").exists())
        workflow_definition = yaml.safe_load((workflow_root / "workflow-definition.yaml").read_text(encoding="utf-8"))
        stage_actions = yaml.safe_load((workflow_root / "stage-actions.yaml").read_text(encoding="utf-8"))

        self.assertEqual(workflow_definition["framework"], "b2s")
        self.assertEqual(stage_actions["framework"], "b2s")
        self.assertEqual(
            [stage["id"] for stage in workflow_definition["stages"]],
            [
                "0-dynamic-assessment",
                "1-dynamic-selection",
                "2-dynamic-stop-review",
            ],
        )
        self.assertEqual(
            [action["action_id"] for action in stage_actions["actions"][:3]],
            [
                "assess-dynamic-gaps",
                "select-dynamic-next-action",
                "evaluate-dynamic-stop-condition",
            ],
        )

    def test_b2s_dynamic_action_references_and_prompt_exist(self):
        workflow_root = REPO_ROOT / ".b2s" / "workflow-types" / "b2s-dynamic"
        actions = yaml.safe_load((workflow_root / "stage-actions.yaml").read_text(encoding="utf-8"))["actions"]
        for action in actions:
            skill_ref = action.get("skill_ref")
            if skill_ref:
                self.assertTrue(
                    (REPO_ROOT / skill_ref).exists(),
                    msg=f"missing skill_ref target for {action['action_id']}: {skill_ref}",
                )
            artifact_template_ref = action.get("artifact_template_ref")
            if artifact_template_ref:
                self.assertTrue(
                    (REPO_ROOT / artifact_template_ref).exists(),
                    msg=f"missing artifact_template_ref target for {action['action_id']}: {artifact_template_ref}",
                )

        self.assertTrue((REPO_ROOT / ".b2s" / "prompts" / "run-workflow-dynamic.md").exists())

    def test_load_state_exposes_additive_dynamic_defaults_for_non_dynamic_workflows(self):
        ws = FIXTURES_ROOT / "no-local-workflow"
        state = workspace.load_state(ws)
        self.assertIn("dynamic_goal", state)
        self.assertIn("dynamic_gap_backlog", state)
        self.assertEqual(state["dynamic_goal"], None)
        self.assertEqual(state["dynamic_gap_backlog"], [])
        self.assertEqual(state["dynamic_iteration_count"], 0)

    def test_dynamic_state_helper_updates_only_dynamic_fields(self):
        state = {
            "workflow_type": "b2s-dynamic",
            "current_stage": "0-dynamic-assessment",
        }
        dynamic_state_module.ensure_dynamic_state_defaults(state)
        dynamic_state_module.update_dynamic_state(
            state,
            dynamic_goal="clarify architecture impact",
            dynamic_macro_phase="requirements-and-architecture",
            dynamic_iteration_count=2,
        )
        self.assertTrue(dynamic_state_module.is_dynamic_workflow(state))
        self.assertEqual(state["dynamic_goal"], "clarify architecture impact")
        self.assertEqual(state["dynamic_macro_phase"], "requirements-and-architecture")
        self.assertEqual(state["dynamic_iteration_count"], 2)
        self.assertEqual(state["current_stage"], "0-dynamic-assessment")

    def test_dynamic_state_helper_knows_when_to_return_to_assessment(self):
        state = {
            "workflow_type": "b2s-dynamic",
        }
        self.assertTrue(
            dynamic_state_module.should_return_to_dynamic_assessment(
                state,
                "create-solution-decisions",
            )
        )
        self.assertFalse(
            dynamic_state_module.should_return_to_dynamic_assessment(
                state,
                "select-dynamic-next-action",
            )
        )
        self.assertFalse(
            dynamic_state_module.should_return_to_dynamic_assessment(
                state,
                "create-solution-decisions",
                awaiting_human=True,
            )
        )

    def test_dynamic_state_helper_resets_orchestration_cycle_statuses(self):
        state = {
            "action_status": {
                "assess-dynamic-gaps": "accepted",
                "select-dynamic-next-action": "accepted",
                "evaluate-dynamic-stop-condition": "accepted",
                "create-solution-decisions": "accepted",
            },
            "artifact_status": {
                "orchestration/dynamic-gap-assessment.md": "accepted",
                "orchestration/dynamic-next-action-decision.md": "accepted",
                "orchestration/dynamic-stop-decision.md": "accepted",
                "architecture/solution-decisions.md": "accepted",
            },
        }
        actions_by_id = {
            "assess-dynamic-gaps": {"outputs": {"primary": "orchestration/dynamic-gap-assessment.md", "secondary": []}},
            "select-dynamic-next-action": {"outputs": {"primary": "orchestration/dynamic-next-action-decision.md", "secondary": []}},
            "evaluate-dynamic-stop-condition": {"outputs": {"primary": "orchestration/dynamic-stop-decision.md", "secondary": []}},
        }

        dynamic_state_module.reset_dynamic_orchestration_cycle(state, actions_by_id)

        self.assertNotIn("assess-dynamic-gaps", state["action_status"])
        self.assertNotIn("select-dynamic-next-action", state["action_status"])
        self.assertNotIn("evaluate-dynamic-stop-condition", state["action_status"])
        self.assertIn("create-solution-decisions", state["action_status"])
        self.assertNotIn("orchestration/dynamic-gap-assessment.md", state["artifact_status"])
        self.assertNotIn("orchestration/dynamic-next-action-decision.md", state["artifact_status"])
        self.assertNotIn("orchestration/dynamic-stop-decision.md", state["artifact_status"])
        self.assertIn("architecture/solution-decisions.md", state["artifact_status"])

    def test_dynamic_selector_bootstraps_when_gap_assessment_is_missing(self):
        ws = FIXTURES_ROOT / "no-local-workflow"
        state = {
            "workflow_type": "b2s-dynamic",
            "current_stage": "1-dynamic-selection",
        }
        result = dynamic_next_step_module.select_next_dynamic_action(ws, state)
        self.assertEqual(result["overall"], "pass")
        self.assertEqual(result["selected_action"], "assess-dynamic-gaps")
        self.assertEqual(result["selected_stage"], "0-dynamic-assessment")
        self.assertEqual(result["ready_actions"], ["assess-dynamic-gaps"])

    def test_dynamic_selector_routes_to_selection_stage_after_assessment(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace_root = Path(tmp)
            (workspace_root / "orchestration").mkdir(parents=True, exist_ok=True)
            (workspace_root / "orchestration" / "dynamic-gap-assessment.md").write_text(
                "\n".join(
                    [
                        "# Dynamic Gap Assessment",
                        "",
                        "## Macro Phase",
                        "",
                        "| Field | Value |",
                        "|---|---|",
                        "| Current macro phase | solution-design |",
                        "| Assessment confidence | high |",
                        "| Iteration count | 3 |",
                        "",
                        "## Ranked Gaps",
                        "",
                        "| Gap ID | Category | Severity | Summary | Evidence | Suggested Actions |",
                        "|---|---|---|---|---|---|",
                        "| DYN-GAP-002 | planning_gap | high | Need plan sequencing | planning missing | create-delivery-skeleton, create-elaboration-plan |",
                        "| DYN-GAP-001 | solution_design_gap | critical | Need design choices | solution decisions missing | create-solution-decisions, create-ui-specification |",
                        "",
                        "## Notes",
                        "",
                        "Test fixture.",
                    ]
                ),
                encoding="utf-8",
            )
            state = {
                "workflow_type": "b2s-dynamic",
                "current_stage": "1-dynamic-selection",
                "action_status": {
                    "assess-dynamic-gaps": "accepted",
                },
            }

            result = dynamic_next_step_module.select_next_dynamic_action(workspace_root, state)

            self.assertEqual(result["overall"], "pass")
            self.assertEqual(result["selected_action"], "select-dynamic-next-action")
            self.assertEqual(result["selected_stage"], "1-dynamic-selection")
            self.assertEqual(result["dynamic_macro_phase"], "solution-design")
            self.assertEqual(result["dynamic_confidence"], "high")
            self.assertEqual(len(result["dynamic_gap_backlog"]), 2)

    def test_dynamic_selector_does_not_reuse_stale_next_action_after_reassessment(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace_root = Path(tmp)
            (workspace_root / "orchestration").mkdir(parents=True, exist_ok=True)
            (workspace_root / "orchestration" / "dynamic-gap-assessment.md").write_text(
                "\n".join(
                    [
                        "# Dynamic Gap Assessment",
                        "",
                        "## Macro Phase",
                        "",
                        "| Field | Value |",
                        "|---|---|",
                        "| Current macro phase | requirements-and-architecture |",
                        "| Assessment confidence | medium |",
                        "| Iteration count | 2 |",
                        "",
                        "## Ranked Gaps",
                        "",
                        "| Gap ID | Category | Severity | Summary | Evidence | Suggested Actions |",
                        "|---|---|---|---|---|---|",
                        "| DYN-GAP-002 | repository_mapping_gap | high | Need epic mapping next | no epics present | create-epic-shells |",
                    ]
                ),
                encoding="utf-8",
            )
            (workspace_root / "orchestration" / "dynamic-next-action-decision.md").write_text(
                "\n".join(
                    [
                        "# Dynamic Next Action Decision",
                        "",
                        "## Decision",
                        "",
                        "| Field | Value |",
                        "|---|---|",
                        "| Selected action | create-atomic-requirements |",
                        "| Persona | product-owner |",
                        "| Current macro phase | requirements-and-architecture |",
                        "| Primary gap addressed | DYN-GAP-001 |",
                        "| Decision confidence | medium |",
                    ]
                ),
                encoding="utf-8",
            )
            (workspace_root / "orchestration" / "dynamic-stop-decision.md").write_text(
                "\n".join(
                    [
                        "# Dynamic Stop Decision",
                        "",
                        "## Decision",
                        "",
                        "| Field | Value |",
                        "|---|---|",
                        "| Outcome | continue |",
                        "| Current macro phase | requirements-and-architecture |",
                        "| Decision confidence | medium |",
                        "| Stop reason | other |",
                    ]
                ),
                encoding="utf-8",
            )
            state = {
                "workflow_type": "b2s-dynamic",
                "current_stage": "0-dynamic-assessment",
                "action_status": {
                    "assess-dynamic-gaps": "accepted",
                },
            }

            result = dynamic_next_step_module.select_next_dynamic_action(workspace_root, state)

            self.assertEqual(result["overall"], "pass")
            self.assertEqual(result["selected_action"], "select-dynamic-next-action")
            self.assertEqual(result["selected_stage"], "1-dynamic-selection")

    def test_dynamic_selector_routes_to_stop_review_after_selection(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace_root = Path(tmp)
            (workspace_root / "orchestration").mkdir(parents=True, exist_ok=True)
            (workspace_root / "orchestration" / "dynamic-gap-assessment.md").write_text(
                "\n".join(
                    [
                        "# Dynamic Gap Assessment",
                        "",
                        "## Ranked Gaps",
                        "",
                        "| Gap ID | Category | Severity | Summary | Evidence | Suggested Actions |",
                        "|---|---|---|---|---|---|",
                        "| DYN-GAP-003 | ui_gap | high | UI detail missing | no page mapping | invent-new-action, create-ui-specification |",
                        "",
                        "## Notes",
                        "",
                        "Test fixture.",
                    ]
                ),
                encoding="utf-8",
            )
            state = {
                "workflow_type": "b2s-dynamic",
                "current_stage": "2-dynamic-stop-review",
                "action_status": {
                    "assess-dynamic-gaps": "accepted",
                    "select-dynamic-next-action": "accepted",
                },
            }

            result = dynamic_next_step_module.select_next_dynamic_action(workspace_root, state)

            self.assertEqual(result["overall"], "pass")
            self.assertEqual(result["selected_action"], "evaluate-dynamic-stop-condition")
            self.assertEqual(result["selected_stage"], "2-dynamic-stop-review")

    def test_dynamic_selector_picks_first_eligible_action_after_stop_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace_root = Path(tmp)
            (workspace_root / "orchestration").mkdir(parents=True, exist_ok=True)
            (workspace_root / "orchestration" / "dynamic-gap-assessment.md").write_text(
                "\n".join(
                    [
                        "# Dynamic Gap Assessment",
                        "",
                        "## Ranked Gaps",
                        "",
                        "| Gap ID | Category | Severity | Summary | Evidence | Suggested Actions |",
                        "|---|---|---|---|---|---|",
                        "| DYN-GAP-010 | planning_gap | high | Planning is missing | no plan artifact | create-delivery-skeleton, create-elaboration-plan |",
                        "",
                        "## Notes",
                        "",
                        "Integration test fixture.",
                    ]
                ),
                encoding="utf-8",
            )
            (workspace_root / "orchestration" / "dynamic-next-action-decision.md").write_text(
                "\n".join(
                    [
                        "# Dynamic Next Action Decision",
                        "",
                        "## Decision",
                        "",
                        "| Field | Value |",
                        "|---|---|",
                        "| Selected action | create-delivery-skeleton |",
                        "| Persona | delivery-lead |",
                        "| Current macro phase | planning-and-epic-shaping |",
                        "| Primary gap addressed | planning_gap |",
                        "| Decision confidence | medium |",
                    ]
                ),
                encoding="utf-8",
            )
            (workspace_root / "orchestration" / "dynamic-stop-decision.md").write_text(
                "\n".join(
                    [
                        "# Dynamic Stop Decision",
                        "",
                        "## Decision",
                        "",
                        "| Field | Value |",
                        "|---|---|",
                        "| Outcome | continue |",
                        "| Current macro phase | planning-and-epic-shaping |",
                        "| Decision confidence | medium |",
                        "| Stop reason | other |",
                    ]
                ),
                encoding="utf-8",
            )
            state = {
                "workflow_type": "b2s-dynamic",
                "current_stage": "2-dynamic-stop-review",
                "action_status": {
                    "assess-dynamic-gaps": "accepted",
                    "select-dynamic-next-action": "accepted",
                    "evaluate-dynamic-stop-condition": "accepted",
                },
            }

            result = dynamic_next_step_module.select_next_dynamic_action(workspace_root, state)

            self.assertEqual(result["overall"], "pass")
            self.assertEqual(result["selected_action"], "create-delivery-skeleton")
            self.assertEqual(result["selected_stage"], "2-dynamic-stop-review")
            self.assertEqual(result["dynamic_gap_category"], "planning_gap")

    def test_next_step_uses_dynamic_selector_for_dynamic_workflow_type(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace_root = Path(tmp)
            workspace.ensure_runtime_layout(workspace_root)
            workflow_dir = workspace_root / ".b2s" / "workflow"
            workflow_dir.mkdir(parents=True, exist_ok=True)

            dynamic_workflow_root = REPO_ROOT / ".b2s" / "workflow-types" / "b2s-dynamic"
            shutil.copyfile(
                dynamic_workflow_root / "stage-actions.yaml",
                workflow_dir / "stage-actions.yaml",
            )
            shutil.copyfile(
                dynamic_workflow_root / "workflow-definition.yaml",
                workflow_dir / "workflow-definition.yaml",
            )

            state = workspace.load_state(workspace_root)
            state["workflow_type"] = "b2s-dynamic"
            state["current_stage"] = "2-dynamic-stop-review"
            state["action_status"] = {
                "assess-dynamic-gaps": "accepted",
                "select-dynamic-next-action": "accepted",
                "evaluate-dynamic-stop-condition": "accepted",
            }
            workspace.save_state(workspace_root, state)

            (workspace_root / "orchestration").mkdir(parents=True, exist_ok=True)
            (workspace_root / "orchestration" / "dynamic-gap-assessment.md").write_text(
                "\n".join(
                    [
                        "# Dynamic Gap Assessment",
                        "",
                        "## Ranked Gaps",
                        "",
                        "| Gap ID | Category | Severity | Summary | Evidence | Suggested Actions |",
                        "|---|---|---|---|---|---|",
                        "| DYN-GAP-010 | planning_gap | high | Planning is missing | no plan artifact | create-delivery-skeleton, create-elaboration-plan |",
                        "",
                        "## Notes",
                        "",
                        "Integration test fixture.",
                    ]
                ),
                encoding="utf-8",
            )
            (workspace_root / "orchestration" / "dynamic-next-action-decision.md").write_text(
                "\n".join(
                    [
                        "# Dynamic Next Action Decision",
                        "",
                        "## Decision",
                        "",
                        "| Field | Value |",
                        "|---|---|",
                        "| Selected action | create-delivery-skeleton |",
                        "| Persona | delivery-lead |",
                        "| Current macro phase | planning-and-epic-shaping |",
                        "| Primary gap addressed | planning_gap |",
                        "| Decision confidence | medium |",
                    ]
                ),
                encoding="utf-8",
            )
            (workspace_root / "orchestration" / "dynamic-stop-decision.md").write_text(
                "\n".join(
                    [
                        "# Dynamic Stop Decision",
                        "",
                        "## Decision",
                        "",
                        "| Field | Value |",
                        "|---|---|",
                        "| Outcome | continue |",
                        "| Current macro phase | planning-and-epic-shaping |",
                        "| Decision confidence | medium |",
                        "| Stop reason | other |",
                    ]
                ),
                encoding="utf-8",
            )

            result = next_step.select_next_action(workspace_root, state)

            self.assertEqual(result["overall"], "pass")
            self.assertEqual(result["selected_action"], "create-delivery-skeleton")
            self.assertEqual(result["selected_stage"], "2-dynamic-stop-review")

    def test_dynamic_selector_pauses_when_stop_decision_requests_human_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace_root = Path(tmp)
            (workspace_root / "orchestration").mkdir(parents=True, exist_ok=True)
            (workspace_root / "orchestration" / "dynamic-gap-assessment.md").write_text(
                "\n".join(
                    [
                        "# Dynamic Gap Assessment",
                        "",
                        "## Ranked Gaps",
                        "",
                        "| Gap ID | Category | Severity | Summary | Evidence | Suggested Actions |",
                        "|---|---|---|---|---|---|",
                        "| DYN-GAP-011 | planning_gap | high | Planning is blocked | external dependency | create-delivery-skeleton |",
                    ]
                ),
                encoding="utf-8",
            )
            (workspace_root / "orchestration" / "dynamic-next-action-decision.md").write_text(
                "\n".join(
                    [
                        "# Dynamic Next Action Decision",
                        "",
                        "## Decision",
                        "",
                        "| Field | Value |",
                        "|---|---|",
                        "| Selected action | create-delivery-skeleton |",
                        "| Persona | delivery-lead |",
                        "| Current macro phase | planning-and-epic-shaping |",
                        "| Primary gap addressed | planning_gap |",
                        "| Decision confidence | low |",
                    ]
                ),
                encoding="utf-8",
            )
            (workspace_root / "orchestration" / "dynamic-stop-decision.md").write_text(
                "\n".join(
                    [
                        "# Dynamic Stop Decision",
                        "",
                        "## Decision",
                        "",
                        "| Field | Value |",
                        "|---|---|",
                        "| Outcome | pause_for_human |",
                        "| Current macro phase | planning-and-epic-shaping |",
                        "| Decision confidence | low |",
                        "| Stop reason | human_clarification_required |",
                    ]
                ),
                encoding="utf-8",
            )
            state = {
                "workflow_type": "b2s-dynamic",
                "current_stage": "2-dynamic-stop-review",
                "action_status": {
                    "assess-dynamic-gaps": "accepted",
                    "select-dynamic-next-action": "accepted",
                    "evaluate-dynamic-stop-condition": "accepted",
                },
            }

            result = dynamic_next_step_module.select_next_dynamic_action(workspace_root, state)

            self.assertEqual(result["overall"], "fail")
            self.assertEqual(result["selected_action"], None)
            self.assertIn("human_clarification_required", result["blocking_reason"])

    def test_dynamic_selector_stops_when_stop_decision_ends_loop(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace_root = Path(tmp)
            (workspace_root / "orchestration").mkdir(parents=True, exist_ok=True)
            (workspace_root / "orchestration" / "dynamic-gap-assessment.md").write_text(
                "\n".join(
                    [
                        "# Dynamic Gap Assessment",
                        "",
                        "## Ranked Gaps",
                        "",
                        "| Gap ID | Category | Severity | Summary | Evidence | Suggested Actions |",
                        "|---|---|---|---|---|---|",
                        "| DYN-GAP-015 | readiness_gap | low | Only minor refinements remain | validation mostly complete | create-epic-shells |",
                    ]
                ),
                encoding="utf-8",
            )
            (workspace_root / "orchestration" / "dynamic-next-action-decision.md").write_text(
                "\n".join(
                    [
                        "# Dynamic Next Action Decision",
                        "",
                        "## Decision",
                        "",
                        "| Field | Value |",
                        "|---|---|",
                        "| Selected action | create-epic-shells |",
                        "| Persona | delivery-lead |",
                        "| Current macro phase | planning-and-epic-shaping |",
                        "| Primary gap addressed | readiness_gap |",
                        "| Decision confidence | high |",
                    ]
                ),
                encoding="utf-8",
            )
            (workspace_root / "orchestration" / "dynamic-stop-decision.md").write_text(
                "\n".join(
                    [
                        "# Dynamic Stop Decision",
                        "",
                        "## Decision",
                        "",
                        "| Field | Value |",
                        "|---|---|",
                        "| Outcome | stop |",
                        "| Current macro phase | handoff-readiness |",
                        "| Decision confidence | high |",
                        "| Stop reason | macro_phase_ready |",
                    ]
                ),
                encoding="utf-8",
            )
            state = {
                "workflow_type": "b2s-dynamic",
                "current_stage": "2-dynamic-stop-review",
                "action_status": {
                    "assess-dynamic-gaps": "accepted",
                    "select-dynamic-next-action": "accepted",
                    "evaluate-dynamic-stop-condition": "accepted",
                },
            }

            result = dynamic_next_step_module.select_next_dynamic_action(workspace_root, state)

            self.assertEqual(result["overall"], "pass")
            self.assertEqual(result["selected_action"], None)
            self.assertEqual(result["reason"], "dynamic stop decision ended the loop")

    def test_dynamic_selector_stops_when_iteration_budget_is_reached(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace_root = Path(tmp)
            (workspace_root / "orchestration").mkdir(parents=True, exist_ok=True)
            (workspace_root / "orchestration" / "dynamic-gap-assessment.md").write_text(
                "\n".join(
                    [
                        "# Dynamic Gap Assessment",
                        "",
                        "## Ranked Gaps",
                        "",
                        "| Gap ID | Category | Severity | Summary | Evidence | Suggested Actions |",
                        "|---|---|---|---|---|---|",
                        "| DYN-GAP-020 | planning_gap | high | Planning still incomplete | no plan artifact | create-delivery-skeleton |",
                    ]
                ),
                encoding="utf-8",
            )
            state = {
                "workflow_type": "b2s-dynamic",
                "current_stage": "0-dynamic-assessment",
                "dynamic_iteration_count": 8,
                "action_status": {
                    "assess-dynamic-gaps": "accepted",
                },
            }

            result = dynamic_next_step_module.select_next_dynamic_action(workspace_root, state)

            self.assertEqual(result["overall"], "fail")
            self.assertEqual(result["selected_action"], None)
            self.assertEqual(result["blocking_reason"], "iteration_budget")
            self.assertEqual(result["dynamic_stop_reason"], "iteration_budget")

    def test_dynamic_selector_stops_when_same_top_gap_repeats(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace_root = Path(tmp)
            (workspace_root / "orchestration").mkdir(parents=True, exist_ok=True)
            (workspace_root / "orchestration" / "dynamic-gap-assessment.md").write_text(
                "\n".join(
                    [
                        "# Dynamic Gap Assessment",
                        "",
                        "## Ranked Gaps",
                        "",
                        "| Gap ID | Category | Severity | Summary | Evidence | Suggested Actions |",
                        "|---|---|---|---|---|---|",
                        "| DYN-GAP-030 | architecture_gap | critical | Architecture uncertainty persists | same unresolved boundary | review-initial-architecture |",
                    ]
                ),
                encoding="utf-8",
            )
            state = {
                "workflow_type": "b2s-dynamic",
                "current_stage": "0-dynamic-assessment",
                "dynamic_last_assessment": {
                    "gap_id": "DYN-GAP-030",
                },
                "dynamic_repeat_gap_count": 1,
                "action_status": {
                    "assess-dynamic-gaps": "accepted",
                },
            }

            result = dynamic_next_step_module.select_next_dynamic_action(workspace_root, state)

            self.assertEqual(result["overall"], "fail")
            self.assertEqual(result["selected_action"], None)
            self.assertEqual(result["blocking_reason"], "no_progress")
            self.assertEqual(result["dynamic_stop_reason"], "no_progress")
            self.assertEqual(result["dynamic_repeat_gap_count"], 2)

    def test_dynamic_selector_rejects_action_outside_current_macro_phase(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace_root = Path(tmp)
            (workspace_root / "orchestration").mkdir(parents=True, exist_ok=True)
            (workspace_root / "orchestration" / "dynamic-gap-assessment.md").write_text(
                "\n".join(
                    [
                        "# Dynamic Gap Assessment",
                        "",
                        "## Macro Phase",
                        "",
                        "| Field | Value |",
                        "|---|---|",
                        "| Current macro phase | solution-design |",
                        "| Assessment confidence | medium |",
                        "| Iteration count | 2 |",
                        "",
                        "## Ranked Gaps",
                        "",
                        "| Gap ID | Category | Severity | Summary | Evidence | Suggested Actions |",
                        "|---|---|---|---|---|---|",
                        "| DYN-GAP-040 | solution_design_gap | high | Solution details missing | missing decisions | create-solution-decisions |",
                    ]
                ),
                encoding="utf-8",
            )
            (workspace_root / "orchestration" / "dynamic-next-action-decision.md").write_text(
                "\n".join(
                    [
                        "# Dynamic Next Action Decision",
                        "",
                        "## Decision",
                        "",
                        "| Field | Value |",
                        "|---|---|",
                        "| Selected action | create-delivery-skeleton |",
                        "| Persona | delivery-lead |",
                        "| Current macro phase | solution-design |",
                        "| Primary gap addressed | DYN-GAP-040 |",
                        "| Decision confidence | medium |",
                    ]
                ),
                encoding="utf-8",
            )
            (workspace_root / "orchestration" / "dynamic-stop-decision.md").write_text(
                "\n".join(
                    [
                        "# Dynamic Stop Decision",
                        "",
                        "## Decision",
                        "",
                        "| Field | Value |",
                        "|---|---|",
                        "| Outcome | continue |",
                        "| Current macro phase | solution-design |",
                        "| Decision confidence | medium |",
                        "| Stop reason | other |",
                    ]
                ),
                encoding="utf-8",
            )
            state = {
                "workflow_type": "b2s-dynamic",
                "current_stage": "2-dynamic-stop-review",
                "action_status": {
                    "assess-dynamic-gaps": "accepted",
                    "select-dynamic-next-action": "accepted",
                    "evaluate-dynamic-stop-condition": "accepted",
                },
            }

            result = dynamic_next_step_module.select_next_dynamic_action(workspace_root, state)

            self.assertEqual(result["overall"], "fail")
            self.assertEqual(result["selected_action"], None)
            self.assertIn("outside the current macro phase", result["blocking_reason"])

    def test_dynamic_selector_fails_for_unknown_gap_category(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace_root = Path(tmp)
            (workspace_root / "orchestration").mkdir(parents=True, exist_ok=True)
            (workspace_root / "orchestration" / "dynamic-gap-assessment.md").write_text(
                "\n".join(
                    [
                        "# Dynamic Gap Assessment",
                        "",
                        "## Ranked Gaps",
                        "",
                        "| Gap ID | Category | Severity | Summary | Evidence | Suggested Actions |",
                        "|---|---|---|---|---|---|",
                        "| DYN-GAP-050 | invented_gap | high | Unknown category drift | test evidence | create-solution-decisions |",
                    ]
                ),
                encoding="utf-8",
            )
            state = {
                "workflow_type": "b2s-dynamic",
                "current_stage": "1-dynamic-selection",
                "action_status": {
                    "assess-dynamic-gaps": "accepted",
                },
            }

            result = dynamic_next_step_module.select_next_dynamic_action(workspace_root, state)

            self.assertEqual(result["overall"], "fail")
            self.assertEqual(result["selected_action"], None)
            self.assertIn("unsupported categories", result["blocking_reason"])

    def test_next_step_bootstraps_dynamic_workflow_before_assessment_exists(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace_root = Path(tmp)
            workspace.ensure_runtime_layout(workspace_root)
            workflow_dir = workspace_root / ".b2s" / "workflow"
            workflow_dir.mkdir(parents=True, exist_ok=True)

            dynamic_workflow_root = REPO_ROOT / ".b2s" / "workflow-types" / "b2s-dynamic"
            shutil.copyfile(
                dynamic_workflow_root / "stage-actions.yaml",
                workflow_dir / "stage-actions.yaml",
            )
            shutil.copyfile(
                dynamic_workflow_root / "workflow-definition.yaml",
                workflow_dir / "workflow-definition.yaml",
            )

            state = workspace.load_state(workspace_root)
            state["workflow_type"] = "b2s-dynamic"
            state["current_stage"] = "1-dynamic-selection"
            workspace.save_state(workspace_root, state)

            result = next_step.select_next_action(workspace_root, state)

            self.assertEqual(result["overall"], "pass")
            self.assertEqual(result["selected_action"], "assess-dynamic-gaps")
            self.assertEqual(result["selected_stage"], "0-dynamic-assessment")

    def test_dynamic_workspace_loads_local_and_b2s_flow_specialist_actions(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace_root = Path(tmp)
            workspace.ensure_runtime_layout(workspace_root)
            workflow_dir = workspace_root / ".b2s" / "workflow"
            workflow_dir.mkdir(parents=True, exist_ok=True)
            dynamic_workflow_root = REPO_ROOT / ".b2s" / "workflow-types" / "b2s-dynamic"
            shutil.copyfile(
                dynamic_workflow_root / "stage-actions.yaml",
                workflow_dir / "stage-actions.yaml",
            )
            shutil.copyfile(
                dynamic_workflow_root / "workflow-definition.yaml",
                workflow_dir / "workflow-definition.yaml",
            )
            workspace.save_json_file(
                workflow_dir / "workflow-type.json",
                {"workflow_type": "b2s-dynamic"},
            )

            actions, by_id = workspace.load_stage_actions(workspace_root)

            self.assertIn("select-dynamic-next-action", by_id)
            self.assertIn("create-solution-decisions", by_id)
            self.assertIn("create-delivery-skeleton", by_id)
            self.assertGreater(len(actions), 3)


if __name__ == "__main__":
    unittest.main()
