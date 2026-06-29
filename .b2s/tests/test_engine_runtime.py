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

from b2s_engine import inputs as inputs_module  # noqa: E402
from b2s_engine import coverage as coverage_module  # noqa: E402
from b2s_engine import validation as validation_module  # noqa: E402
from b2s_engine import dispatch as dispatch_module  # noqa: E402
from b2s_engine import state as state_module  # noqa: E402
from b2s_engine import next_step  # noqa: E402
from b2s_engine import workspace as workspace_module  # noqa: E402


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

    def load_action(self, action_id: str) -> dict:
        stage_actions = yaml.safe_load((REPO_ROOT / ".b2s" / "workflow" / "stage-actions.yaml").read_text(encoding="utf-8"))["actions"]
        return next(action for action in stage_actions if action["action_id"] == action_id)

    def test_next_step_then_gate_approval_progresses_to_requirements(self) -> None:
        run_cli("next-step", "--workspace-root", str(self.workspace_root))
        next_step = self.read_json(".b2s/state/next-step.json")
        self.assertEqual(next_step["selected_action"], "route-initiative")

        run_cli("collect-inputs", "--workspace-root", str(self.workspace_root))
        current_inputs = self.read_json(".b2s/tmp/current-inputs.json")
        self.assertEqual(current_inputs["overall"], "pass")
        self.assertEqual(current_inputs["action_id"], "route-initiative")
        self.assertEqual(
            current_inputs["prompt_placeholders"]["required_inputs"],
            ["input/brs.md"],
        )
        self.assertEqual(
            current_inputs["prompt_placeholders"]["optional_inputs"],
            ["input/architecture.md", "input/input-package.md"],
        )
        self.assertEqual(
            current_inputs["prompt_placeholders"]["resolved_required_inputs"],
            ["input/brs.md"],
        )
        self.assertEqual(
            current_inputs["prompt_placeholders"]["resolved_optional_inputs"],
            [],
        )
        self.assertEqual(
            current_inputs["prompt_placeholders"]["resolved_policy_inputs"],
            [],
        )
        self.assertEqual(
            current_inputs["prompt_placeholders"]["primary_output"],
            "routing/routing-decision.md",
        )
        self.assertEqual(
            current_inputs["prompt_placeholders"]["secondary_outputs"],
            [],
        )
        self.assertEqual(current_inputs["prompt_placeholders"]["prompt_family"], "b2s")
        self.assertEqual(current_inputs["prompt_placeholders"]["template_mode"], "strict")

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

    def test_dispatch_renderer_substitutes_supported_placeholders(self) -> None:
        rendered = dispatch_module._render_prompt_text(
            "Read {resolved_required_inputs}\nPolicy {resolved_policy_inputs}\nFamily {prompt_family}\nMode {template_mode}\nWrite {primary_output}\nKeep {workspace_root}",
            {
                "resolved_required_inputs": ["input/brs.md", "routing/routing-decision.md"],
                "resolved_policy_inputs": [".b2s/policies/requirements/requirement-writing-standard.md"],
                "prompt_family": "speckit",
                "template_mode": "strict",
                "primary_output": "routing/routing-decision.md",
                "required_inputs": [],
                "optional_inputs": [],
                "resolved_optional_inputs": [],
                "secondary_outputs": [],
            },
        )
        self.assertIn("- input/brs.md", rendered)
        self.assertIn("- routing/routing-decision.md", rendered)
        self.assertIn("- .b2s/policies/requirements/requirement-writing-standard.md", rendered)
        self.assertIn("Family speckit", rendered)
        self.assertIn("Mode strict", rendered)
        self.assertIn("Write routing/routing-decision.md", rendered)
        self.assertIn("{workspace_root}", rendered)

    def test_dispatch_renderer_fails_when_supported_placeholder_is_missing(self) -> None:
        with self.assertRaisesRegex(ValueError, "Missing prompt placeholder: primary_output"):
            dispatch_module._render_prompt_text(
                "Write {primary_output}",
                {
                    "required_inputs": [],
                    "optional_inputs": [],
                    "resolved_required_inputs": [],
                    "resolved_optional_inputs": [],
                    "resolved_policy_inputs": [],
                    "secondary_outputs": [],
                    "prompt_family": "b2s",
                    "template_mode": "strict",
                },
            )

    def test_collect_action_inputs_reports_policy_paths_for_migrated_action(self) -> None:
        (self.workspace_root / "business-intake").mkdir()
        (self.workspace_root / "business-intake" / "business-intake-summary.md").write_text(
            "# Business Intake Summary\n",
            encoding="utf-8",
        )
        action = self.load_action("create-requirements")
        collected = inputs_module.collect_action_inputs(action, self.workspace_root)
        self.assertEqual(collected["overall"], "pass")
        self.assertEqual(
            collected["prompt_placeholders"]["resolved_policy_inputs"],
            [
                ".b2s/policies/requirements/definition-of-ready.md",
                ".b2s/policies/requirements/requirement-writing-standard.md",
            ],
        )
        self.assertEqual(collected["prompt_placeholders"]["prompt_family"], "speckit")
        self.assertEqual(collected["prompt_placeholders"]["template_mode"], "strict")

    def test_collect_action_inputs_defaults_prompt_family_and_template_mode_for_old_action(self) -> None:
        legacy_action = {
            "action_id": "legacy",
            "title": "Legacy",
            "persona": "orchestrator",
            "skill_ref": ".b2s/skills/orchestrator/route-initiative.md",
            "artifact_template_ref": ".b2s/artifact-templates/routing-decision.md",
            "inputs": {"required": ["input/brs.md"]},
            "outputs": {"primary": "routing/routing-decision.md"},
            "human_gate": {"required": False},
            "artifact_criticality": "high",
        }
        from b2s_engine import action_contract as action_contract_module
        normalized = action_contract_module.normalize_action(legacy_action)
        collected = inputs_module.collect_action_inputs(normalized, self.workspace_root)
        self.assertEqual(collected["overall"], "pass")
        self.assertEqual(collected["prompt_placeholders"]["prompt_family"], "b2s")
        self.assertEqual(collected["prompt_placeholders"]["template_mode"], "strict")

    def test_resolve_skill_prompt_uses_fallback_for_non_b2s_family(self) -> None:
        action = {
            "prompt_family": "hve",
            "skill_ref": ".b2s/skills/nonexistent/missing-skill.md",
            "compatibility": {
                "fallback_skill_ref": ".b2s/skills/engineering-lead/create-compact-handoff.md",
            },
        }
        resolved = dispatch_module._resolve_skill_prompt(action, self.workspace_root, {})
        self.assertTrue(resolved["fallback_used"])
        self.assertEqual(
            resolved["skill_ref"],
            ".b2s/skills/engineering-lead/create-compact-handoff.md",
        )
        self.assertEqual(resolved["prompt_family"], "hve")

    def test_resolve_skill_prompt_fails_clearly_when_non_b2s_family_has_no_fallback(self) -> None:
        action = {
            "prompt_family": "bmad",
            "skill_ref": ".b2s/skills/nonexistent/missing-skill.md",
            "compatibility": {},
        }
        with self.assertRaisesRegex(FileNotFoundError, "family 'bmad'"):
            dispatch_module._resolve_skill_prompt(action, self.workspace_root, {})

    def test_b2s_frontend_condition_ignores_template_placeholder_ui_text(self) -> None:
        (self.workspace_root / "architecture").mkdir()
        (self.workspace_root / "architecture" / "technical-landscape.md").write_text(
            (REPO_ROOT / ".b2s" / "artifact-templates" / "technical-landscape.md").read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        result = next_step.evaluate_condition(
            "architecture/technical-landscape.md contains frontend",
            {"action_status": {}},
            self.workspace_root,
            {},
        )
        self.assertFalse(result)

    def test_b2s_frontend_condition_passes_for_structured_ui_repository(self) -> None:
        (self.workspace_root / "architecture").mkdir()
        (self.workspace_root / "architecture" / "technical-landscape.md").write_text(
            textwrap.dedent(
                """\
                # Technical Landscape

                ## Repositories

                | Name | Status | Type | Technology | Responsibilities | Deployment Target |
                |---|---|---|---|---|---|
                | applicant-portal | existing | ui | React | customer submission UI | Static Web Apps |
                """
            ),
            encoding="utf-8",
        )
        result = next_step.evaluate_condition(
            "architecture/technical-landscape.md contains frontend",
            {"action_status": {}},
            self.workspace_root,
            {},
        )
        self.assertTrue(result)

    def test_next_step_persists_dynamic_selector_metadata_in_state(self) -> None:
        workspace_module.ensure_runtime_layout(self.workspace_root)
        workflow_dir = self.workspace_root / ".b2s" / "workflow"
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

        state = self.read_json(".b2s/state/workflow-state.json")
        state["workflow_type"] = "b2s-dynamic"
        state["current_stage"] = "1-dynamic-selection"
        state["action_status"] = {
            "assess-dynamic-gaps": "accepted",
        }
        (self.workspace_root / ".b2s" / "state" / "workflow-state.json").write_text(
            json.dumps(state, indent=2),
            encoding="utf-8",
        )

        (self.workspace_root / "orchestration").mkdir(parents=True, exist_ok=True)
        (self.workspace_root / "orchestration" / "dynamic-gap-assessment.md").write_text(
            textwrap.dedent(
                """\
                # Dynamic Gap Assessment

                ## Macro Phase

                | Field | Value |
                |---|---|
                | Current macro phase | planning-and-epic-shaping |
                | Assessment confidence | medium |
                | Iteration count | 4 |

                ## Ranked Gaps

                | Gap ID | Category | Severity | Summary | Evidence | Suggested Actions |
                |---|---|---|---|---|---|
                | DYN-GAP-021 | planning_gap | high | Delivery plan missing | no planning artifacts yet | create-delivery-skeleton, create-elaboration-plan |
                """
            ),
            encoding="utf-8",
        )

        run_cli("next-step", "--workspace-root", str(self.workspace_root))

        next_step_result = self.read_json(".b2s/state/next-step.json")
        updated_state = self.read_json(".b2s/state/workflow-state.json")

        self.assertEqual(next_step_result["selected_action"], "select-dynamic-next-action")
        self.assertEqual(next_step_result["selected_stage"], "1-dynamic-selection")
        self.assertEqual(updated_state["dynamic_macro_phase"], "planning-and-epic-shaping")
        self.assertEqual(updated_state["dynamic_confidence"], "medium")
        self.assertEqual(updated_state["dynamic_focus_area"], None)
        self.assertEqual(updated_state["dynamic_goal"], None)
        self.assertEqual(updated_state["dynamic_last_selected_action"], "select-dynamic-next-action")
        self.assertEqual(updated_state["dynamic_iteration_count"], 1)
        self.assertEqual(updated_state["dynamic_last_assessment"]["selected_action"], "select-dynamic-next-action")
        self.assertEqual(updated_state["dynamic_last_assessment"]["gap_id"], None)
        self.assertEqual(len(updated_state["dynamic_gap_backlog"]), 1)

    def test_next_step_bootstraps_dynamic_workspace_without_assessment_artifact(self) -> None:
        workspace_module.ensure_runtime_layout(self.workspace_root)
        workflow_dir = self.workspace_root / ".b2s" / "workflow"
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

        state = self.read_json(".b2s/state/workflow-state.json")
        state["workflow_type"] = "b2s-dynamic"
        state["current_stage"] = "1-dynamic-selection"
        (self.workspace_root / ".b2s" / "state" / "workflow-state.json").write_text(
            json.dumps(state, indent=2),
            encoding="utf-8",
        )

        run_cli("next-step", "--workspace-root", str(self.workspace_root))

        next_step_result = self.read_json(".b2s/state/next-step.json")
        updated_state = self.read_json(".b2s/state/workflow-state.json")

        self.assertEqual(next_step_result["overall"], "pass")
        self.assertEqual(next_step_result["selected_action"], "assess-dynamic-gaps")
        self.assertEqual(next_step_result["selected_stage"], "0-dynamic-assessment")
        self.assertEqual(updated_state["current_stage"], "0-dynamic-assessment")
        self.assertEqual(updated_state["next_action"], "assess-dynamic-gaps")
        self.assertEqual(updated_state["dynamic_last_selected_action"], "assess-dynamic-gaps")

    def test_should_auto_accept_clarification_gate_when_no_blockers(self) -> None:
        gate_state = {
            "interaction_mode": "collect_answers",
            "review_summary": {
                "question_count": 0,
                "no_blockers": True,
            },
        }
        self.assertTrue(state_module._should_auto_accept_gate(gate_state))

    def test_per_item_gate_acceptance_marks_current_item_and_promotes_when_all_done(self) -> None:
        (self.workspace_root / "planning").mkdir()
        (self.workspace_root / "planning" / "delivery-skeleton.md").write_text(
            textwrap.dedent(
                """\
                ### E-001
                ### E-002
                """
            ),
            encoding="utf-8",
        )
        state = {
            "action_status": {},
            "action_item_status": {
                "resolve-epic-open-questions#E-002": "accepted",
            },
        }
        action = {
            "action_id": "resolve-epic-open-questions",
            "item_source": "planning/delivery-skeleton.md",
            "item_pattern": "^###\\s+(E-\\d{3})",
            "iteration_mode": "per_item",
            "status_model": {
                "artifact_on_gate_accept": "accepted",
            },
        }
        actions_by_id = {
            "resolve-epic-open-questions": action,
        }
        from b2s_engine import gates as gates_module
        gates_module._apply_gate_acceptance_to_source_action(
            self.workspace_root,
            state,
            "resolve-epic-open-questions",
            actions_by_id,
            "E-001",
        )
        self.assertEqual(
            state["action_item_status"]["resolve-epic-open-questions#E-001"],
            "accepted",
        )
        self.assertEqual(state["action_status"]["resolve-epic-open-questions"], "accepted")

    def test_action_summary_renders_business_intake_prompt_with_resolved_placeholders(self) -> None:
        (self.workspace_root / "routing").mkdir()
        (self.workspace_root / "routing" / "routing-decision.md").write_text(
            "# Routing Decision\n",
            encoding="utf-8",
        )
        (self.workspace_root / "input" / "brs").mkdir()
        (self.workspace_root / "input" / "brs" / "appendix.md").write_text(
            "# Appendix\n",
            encoding="utf-8",
        )
        (self.workspace_root / "input" / "architecture.md").write_text(
            "# Architecture\n",
            encoding="utf-8",
        )

        action = self.load_action("create-business-intake-summary")
        summary = dispatch_module._action_summary(action, self.workspace_root)
        rendered = summary["rendered_skill_text"]

        self.assertIsNotNone(rendered)
        self.assertIn("- input/brs.md", rendered)
        self.assertIn("- routing/routing-decision.md", rendered)
        self.assertIn("- input/brs/appendix.md", rendered)
        self.assertIn("- input/architecture.md", rendered)
        self.assertIn("Write the artifact to `business-intake/business-intake-summary.md`", rendered)
        self.assertNotIn("{resolved_required_inputs}", rendered)
        self.assertNotIn("{resolved_optional_inputs}", rendered)
        self.assertNotIn("{primary_output}", rendered)

    def test_action_summary_renders_delivery_structure_prompt_with_resolved_placeholders(self) -> None:
        (self.workspace_root / "routing").mkdir()
        (self.workspace_root / "routing" / "routing-decision.md").write_text(
            "# Routing Decision\n",
            encoding="utf-8",
        )
        (self.workspace_root / "business-intake").mkdir()
        (self.workspace_root / "business-intake" / "business-intake-summary.md").write_text(
            "# Business Intake Summary\n",
            encoding="utf-8",
        )
        (self.workspace_root / "business-analysis").mkdir()
        (self.workspace_root / "business-analysis" / "requirements.md").write_text(
            "# Requirements\n",
            encoding="utf-8",
        )
        (self.workspace_root / "business-analysis" / "business-rules.md").write_text(
            "# Business Rules\n",
            encoding="utf-8",
        )
        (self.workspace_root / "business-analysis" / "actors-and-personas.md").write_text(
            "# Actors and Personas\n",
            encoding="utf-8",
        )
        (self.workspace_root / "business-analysis" / "use-cases").mkdir()
        (self.workspace_root / "business-analysis" / "use-cases" / "UC-001.md").write_text(
            "# UC-001\n",
            encoding="utf-8",
        )
        (self.workspace_root / "architecture").mkdir()
        (self.workspace_root / "architecture" / "architecture-review.md").write_text(
            "# Architecture Review\n",
            encoding="utf-8",
        )
        (self.workspace_root / "input" / "appendix.md").write_text(
            "# Appendix\n",
            encoding="utf-8",
        )

        action = self.load_action("create-delivery-structure")
        summary = dispatch_module._action_summary(action, self.workspace_root)
        rendered = summary["rendered_skill_text"]

        self.assertIsNotNone(rendered)
        self.assertIn("- business-analysis/use-cases/", rendered)
        self.assertIn("- architecture/architecture-review.md", rendered)
        self.assertIn("- business-analysis/requirements.md", rendered)
        self.assertIn("- business-analysis/business-rules.md", rendered)
        self.assertIn("- business-analysis/actors-and-personas.md", rendered)
        self.assertIn("Write the main artifact to `planning/delivery-structure.md`", rendered)
        self.assertIn("Also produce any paths listed in `[]`.", rendered)
        self.assertNotIn("{resolved_required_inputs}", rendered)
        self.assertNotIn("{resolved_optional_inputs}", rendered)
        self.assertNotIn("{primary_output}", rendered)
        self.assertNotIn("{secondary_outputs}", rendered)

    def test_action_summary_exposes_prompt_family_for_seeded_handoff_action(self) -> None:
        (self.workspace_root / "engineering-readiness").mkdir()
        (self.workspace_root / "engineering-readiness" / "initiative-context.md").write_text(
            "# Initiative Context\n",
            encoding="utf-8",
        )
        (self.workspace_root / "engineering-readiness" / "readiness-check.md").write_text(
            "# Readiness Check\n",
            encoding="utf-8",
        )
        (self.workspace_root / "planning").mkdir()
        (self.workspace_root / "planning" / "delivery-structure.md").write_text(
            "# Delivery Structure\n",
            encoding="utf-8",
        )
        (self.workspace_root / "architecture").mkdir()
        (self.workspace_root / "architecture" / "architecture-rules.md").write_text(
            "# Architecture Rules\n",
            encoding="utf-8",
        )
        action = self.load_action("create-openspec-handoff")
        summary = dispatch_module._action_summary(action, self.workspace_root)
        self.assertEqual(summary["prompt_family"], "hve")
        self.assertFalse(summary["fallback_used"])

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

    def test_current_validation_yaml_reports_named_rules_stably(self) -> None:
        (self.workspace_root / "business-intake").mkdir()
        (self.workspace_root / "business-intake" / "business-intake-summary.md").write_text(
            "# Business Intake Summary\n",
            encoding="utf-8",
        )
        (self.workspace_root / "business-analysis").mkdir()
        (self.workspace_root / "business-analysis" / "requirements.md").write_text(
            "# Requirements\n\n## Functional Requirements\n\n| Requirement ID | Summary |\n|---|---|\n| FR-001 | TBD |\n",
            encoding="utf-8",
        )
        run_cli(
            "validate-artifact",
            "--workspace-root",
            str(self.workspace_root),
            "--action-id",
            "create-requirements",
        )
        validation = self.read_yaml(".b2s/tmp/current-validation.yaml")
        self.assertIn("named_rule_results", validation)
        self.assertIsInstance(validation["named_rule_results"], list)
        self.assertTrue(validation["named_rule_results"])
        first = validation["named_rule_results"][0]
        self.assertEqual(first["name"], "named_validation_rule")
        self.assertIn("rule_name", first)
        self.assertIn("severity", first)
        self.assertIn("target", first)
        self.assertIn("result", first)
        self.assertIn("detail", first)
        self.assertIn(first["severity"], {"required", "optional"})
        self.assertTrue(any(item["rule_name"] == "requirement_is_testable" for item in validation["named_rule_results"]))

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

    def test_validate_artifact_uses_template_dispatch_when_template_ref_exists(self) -> None:
        (self.workspace_root / "architecture").mkdir()
        (self.workspace_root / "architecture" / "draft-architecture.md").write_text(
            textwrap.dedent(
                """\
                # Draft Architecture

                ## Metadata

                | Field | Value |
                |---|---|
                | Initiative ID | TEST-001 |
                | Created at | 2026-06-18 |
                | Created by | architect |
                | Status | Draft |

                ## Executive Summary

                This initiative introduces a loan origination platform with AI scoring,
                underwriter workflows, and core banking integration for disbursement.

                ## Component Overview

                | Component | Type | Responsibility | Technology |
                |---|---|---|---|
                | Intake API | New | Accept loan applications | Confirmed |

                ## Deployment Topology

                ```mermaid
                graph TD
                  A[Client] --> B[Intake API]
                  B --> C[(Application DB)]
                ```

                ## Data Flow

                ```mermaid
                flowchart LR
                  Applicant --> IntakeAPI
                  IntakeAPI --> ScoringService
                ```

                ## Integration Points

                | External System | Protocol | Auth | Sync/Async | Contract Status |
                |---|---|---|---|---|
                | Experian | REST | API Key | Sync | Assumed |

                ## Technology Constraints

                | Area | Technology | Status | Notes |
                |---|---|---|---|
                | API | REST/JSON | Confirmed | Standard stack |

                ## Security Architecture

                Authentication via OAuth2. PII encrypted at rest. Audit trail for all underwriter actions.

                ## Key Architecture Risks

                | Risk | Type | Impact | Mitigation |
                |---|---|---|---|
                | Experian SLA | Integration | Medium | Fallback to manual review |

                ## Open Architecture Questions

                | Question | Impact | Owner | Default Assumption |
                |---|---|---|---|
                | Final field validation rules | Low | Product | Proceed with documented fields |
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
        self.assertEqual(validation["checks"][1]["detail"], "template: architecture/draft-architecture.md")

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

    def test_template_validation_rejects_shallow_critical_artifact(self) -> None:
        """A minimal artifact that has a template_ref fails template-driven structural checks."""
        (self.workspace_root / "planning").mkdir()
        (self.workspace_root / "planning" / "delivery-structure.md").write_text(
            "# Delivery Structure\n\n## Metadata\n\nText.\n\n## FR Coverage\n\n| FR-NNN | Stories | Status |\n|---|---|---|\n| FR-001 | S-001.1 | Covered |\n",
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
        self.assertTrue(
            any("tmpl_section_" in item for item in validation["failures"]),
            "shallow artifact must fail template section checks",
        )

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

    def test_no_unknown_requirement_references_rule_flags_invented_ids(self) -> None:
        (self.workspace_root / "requirements").mkdir(parents=True, exist_ok=True)
        (self.workspace_root / "planning").mkdir(parents=True, exist_ok=True)
        (self.workspace_root / "requirements" / "atomic-requirements.md").write_text(
            textwrap.dedent(
                """\
                # Atomic Requirements

                ### REQ-001 - Submit request
                | Field | Value |
                |---|---|
                | Actor | Analyst |
                | Business Object | Intake request |
                | Trigger / Event | Submit action |
                | Expected Outcome | Request is stored |
                | Ambiguities | |
                | Blocking Questions | |

                #### Requirement Text
                The analyst can submit an intake request.
                """
            ),
            encoding="utf-8",
        )
        (self.workspace_root / "planning" / "fr-coverage.md").write_text(
            textwrap.dedent(
                """\
                # Requirement Coverage Report

                ## Full Coverage Matrix

                | REQ / FR | Requirement Title | Capability | Epic | Feature | Story | Open Questions Propagated | Evidence | Status |
                |---|---|---|---|---|---|---|---|---|
                | REQ-001 | Submit request | CAP-001 | E-001 | F-001 | S-001.1 | N/A | story exists | Covered |
                | REQ-999 | Invented requirement | CAP-001 | E-001 | F-001 | S-001.1 | N/A | invented | Covered |
                """
            ),
            encoding="utf-8",
        )

        result = validation_module._rule_no_unknown_requirement_references(
            self.workspace_root / "planning" / "fr-coverage.md",
            self.workspace_root,
            {},
            "planning/fr-coverage.md",
            [],
        )
        self.assertEqual(result["result"], "fail")
        self.assertIn("REQ-999", result["detail"])

    def test_epic_directory_validation_requires_contract(self) -> None:
        (self.workspace_root / "planning").mkdir(parents=True, exist_ok=True)
        (self.workspace_root / "epics" / "E-001-submit-request" / "stories").mkdir(parents=True, exist_ok=True)
        (self.workspace_root / ".b2s" / "state").mkdir(parents=True, exist_ok=True)
        (self.workspace_root / ".b2s" / "state" / "workflow-state.json").write_text(
            json.dumps({"current_item": None}),
            encoding="utf-8",
        )
        (self.workspace_root / "planning" / "delivery-skeleton.md").write_text(
            textwrap.dedent(
                """\
                # Delivery Skeleton

                ## Application Layers

                | Layer | Present? | Components | Notes |
                |---|---|---|---|
                | Frontend | Yes | Portal | React |

                ## Requirement Coverage

                | REQ / FR | Feature | Epic | Status |
                |---|---|---|---|
                | REQ-001 | F-001 | E-001 | Covered |
                """
            ),
            encoding="utf-8",
        )
        (self.workspace_root / "epics" / "E-001-submit-request" / "epic.md").write_text(
            "# E-001 - Submit request\n",
            encoding="utf-8",
        )
        (self.workspace_root / "epics" / "E-001-submit-request" / "stories" / "S-001.1-submit.md").write_text(
            textwrap.dedent(
                """\
                # S-001.1 - Submit request

                | Field | Value |
                |---|---|
                | Layers | Frontend |

                ## User Story
                As an analyst, I want to submit a request, so that intake can begin.

                ## Business Context
                This story enables the first business step.

                ## Implementation Guidance
                Use epic context for now.

                ## Acceptance Criteria

                ```gherkin
                Scenario: happy path
                  Given a valid request
                  When the analyst submits it
                  Then the request is accepted
                ```

                ```gherkin
                Scenario: validation failure
                  Given invalid data
                  When the analyst submits it
                  Then the request is rejected
                ```

                ## Test Expectations
                Unit and integration coverage are required.
                """
            ),
            encoding="utf-8",
        )

        checks = validation_module._validate_epic_folders_directory(
            self.workspace_root / "epics",
            self.workspace_root,
        )
        contract_check = next(check for check in checks if check["name"] == "epic_has_contract")
        self.assertEqual(contract_check["result"], "fail")

    def test_epic_directory_validation_passes_with_contract(self) -> None:
        (self.workspace_root / "planning").mkdir(parents=True, exist_ok=True)
        (self.workspace_root / "epics" / "E-001-submit-request" / "stories").mkdir(parents=True, exist_ok=True)
        (self.workspace_root / ".b2s" / "state").mkdir(parents=True, exist_ok=True)
        (self.workspace_root / ".b2s" / "state" / "workflow-state.json").write_text(
            json.dumps({"current_item": None}),
            encoding="utf-8",
        )
        (self.workspace_root / "planning" / "delivery-skeleton.md").write_text(
            textwrap.dedent(
                """\
                # Delivery Skeleton

                ## Application Layers

                | Layer | Present? | Components | Notes |
                |---|---|---|---|
                | Frontend | Yes | Portal | React |

                ## Requirement Coverage

                | REQ / FR | Feature | Epic | Status |
                |---|---|---|---|
                | REQ-001 | F-001 | E-001 | Covered |
                """
            ),
            encoding="utf-8",
        )
        (self.workspace_root / "epics" / "E-001-submit-request" / "epic.md").write_text(
            "# E-001 - Submit request\n",
            encoding="utf-8",
        )
        (self.workspace_root / "epics" / "E-001-submit-request" / "implementation-contract.md").write_text(
            "# Implementation Contract\n\n## Data Entities\n\nApplication entity with ARN.\n",
            encoding="utf-8",
        )
        (self.workspace_root / "epics" / "E-001-submit-request" / "stories" / "S-001.1-submit.md").write_text(
            textwrap.dedent(
                """\
                # S-001.1 - Submit request

                ## Metadata

                | Field | Value |
                |---|---|
                | Story ID | S-001.1 |
                | Story Type | frontend-form |
                | Epic | E-001 - Submit request |
                | Actor | Analyst |
                | Layers | frontend |
                | Priority | Must |
                | Increment | D1 |
                | Status | Draft |

                ## User Story

                As an analyst, I want to submit a request, so that intake can begin.

                ## Business Context

                This story enables the first business step. It captures the initial request for downstream processing.

                ## Linked Requirements

                | ID | Requirement |
                |---|---|
                | REQ-001 | Submit request |

                ## Requirements Implemented

                - REQ-001

                ## Requirements Referenced

                - FR-003

                ## In Scope

                - Render submission flow
                - Validate request details before submission

                ## Implementation Guidance

                - **Entity:** Application
                - **API:** POST /requests
                - **Status:** Draft
                - **Events:** request.submitted
                - **Rules:** Validation must run before submit

                ## Dependency Contracts

                | Dependency | Type | Contract Consumed | Why It Matters |
                |---|---|---|---|
                | S-001.2 | Story | POST /requests returns 201 with requestId | Confirmation depends on backend acceptance |

                ## UI Behaviour

                - **Page:** Submit request /submit
                - **Components affected:** form
                - **Fields:** requestAmount with positive-number validation
                - **States:** loading -> spinner | error -> inline errors | success -> confirmation
                - **Flow:** submit form -> validate -> show confirmation

                ## Acceptance Criteria

                ```gherkin
                Scenario: happy path
                  Given a valid request
                  When the analyst submits it
                  Then the request is accepted
                ```

                ```gherkin
                Scenario: validation failure
                  Given invalid data
                  When the analyst submits it
                  Then the request is rejected
                ```

                ```gherkin
                Scenario: keyboard submission
                  Given the form is complete
                  When the analyst submits using the keyboard
                  Then the request is accepted
                ```

                ## Test Expectations

                | Test Type | What to Test | Why | Automation |
                |---|---|---|---|
                | Unit | amount validator | invalid requests are blocked | Must automate |
                | E2E | submission flow | analyst can submit a request | Automate |

                ## Required Tests

                - Unit: amount validator rejects invalid values
                - E2E: submission flow succeeds
                - Accessibility: keyboard submission works

                ## Out of Scope

                - Backend persistence

                ## Dependencies

                | Dependency | Type | Blocking? |
                |---|---|---|
                | S-001.2 | Story | Yes |

                ## Open Questions

                | ID | Question | Impact |
                |---|---|---|
                | OQ-001 | None identified | No blocker |
                """
            ),
            encoding="utf-8",
        )
        (self.workspace_root / "epics" / "E-001-submit-request" / "stories" / "S-001.1-submit.agent.yaml").write_text(
            textwrap.dedent(
                """\
                story_id: S-001.1
                title: "Submit request"
                story_type: "frontend-form"
                layer: "frontend"
                requirements_implemented:
                  - REQ-001
                requirements_referenced:
                  - FR-003
                depends_on:
                  - story_id: "S-001.2"
                    reason: "Confirmation depends on backend acceptance"
                    consumes_contract:
                      type: "api"
                      summary: "POST /requests returns 201 with requestId"
                blocks: []
                in_scope:
                  - "Render submission flow"
                out_of_scope:
                  - "Backend persistence"
                implementation_contract:
                  touched_components:
                    - "Applicant Portal"
                  touched_files_or_areas:
                    - "submit form"
                  data_inputs:
                    - name: "requestAmount"
                      type: "number"
                      required: true
                      validation: "positive value"
                  operations:
                    - type: "ui action"
                      target: "/submit"
                      expected_result: "Request is submitted"
                  success_behavior:
                    - "Show confirmation"
                  error_handling:
                    - "Show inline validation errors"
                required_tests:
                  unit:
                    - "Amount validator rejects invalid values"
                  integration: []
                  api: []
                  e2e:
                    - "Submission flow succeeds"
                  accessibility:
                    - "Keyboard submission works"
                done_evidence:
                  - "Acceptance criteria mapped to automated tests"
                """
            ),
            encoding="utf-8",
        )

        checks = validation_module._validate_epic_folders_directory(
            self.workspace_root / "epics",
            self.workspace_root,
        )
        contract_check = next(check for check in checks if check["name"] == "epic_has_contract")
        self.assertEqual(contract_check["result"], "pass")
        agent_check = next(check for check in checks if check["name"] == "story_agent_contract_required_tests_present")
        self.assertEqual(agent_check["result"], "pass")

    def test_epic_directory_validation_fails_for_invalid_agent_contract_content(self) -> None:
        (self.workspace_root / "planning").mkdir(parents=True, exist_ok=True)
        (self.workspace_root / "epics" / "E-001-submit-request" / "stories").mkdir(parents=True, exist_ok=True)
        (self.workspace_root / ".b2s" / "state").mkdir(parents=True, exist_ok=True)
        (self.workspace_root / ".b2s" / "state" / "workflow-state.json").write_text(
            json.dumps({"current_item": None}),
            encoding="utf-8",
        )
        (self.workspace_root / "planning" / "delivery-skeleton.md").write_text(
            textwrap.dedent(
                """\
                # Delivery Skeleton

                ## Application Layers

                | Layer | Present? | Components | Notes |
                |---|---|---|---|
                | Backend | Yes | API | FastAPI |

                ## Requirement Coverage

                | REQ / FR | Feature | Epic | Status |
                |---|---|---|---|
                | FR-001 | F-001 | E-001 | Covered |
                """
            ),
            encoding="utf-8",
        )
        (self.workspace_root / "epics" / "E-001-submit-request" / "epic.md").write_text(
            "# E-001 - Submit request\n",
            encoding="utf-8",
        )
        (self.workspace_root / "epics" / "E-001-submit-request" / "implementation-contract.md").write_text(
            "# Implementation Contract\n\n## API Surface\n\nPOST endpoint.\n",
            encoding="utf-8",
        )
        (self.workspace_root / "epics" / "E-001-submit-request" / "stories" / "S-001.1-submit.md").write_text(
            textwrap.dedent(
                """\
                # S-001.1 - Submit request

                ## Metadata

                | Field | Value |
                |---|---|
                | Story ID | S-001.1 |
                | Story Type | backend-endpoint |
                | Epic | E-001 - Submit request |
                | Actor | API owner |
                | Layers | backend |
                | Priority | Must |
                | Increment | D1 |
                | Status | Draft |

                ## User Story

                As an API owner, I want to accept a request, so that intake can begin.

                ## Business Context

                This story accepts incoming requests. It starts the intake flow.

                ## Linked Requirements

                | ID | Requirement |
                |---|---|
                | FR-001 | Submit request |

                ## Requirements Implemented

                - FR-001

                ## Requirements Referenced

                - FR-003

                ## In Scope

                - Accept request payload

                ## Implementation Guidance

                - **Entity:** Application
                - **API:** POST /requests
                - **Status:** Draft
                - **Events:** request.submitted
                - **Rules:** Validate request

                ## Dependency Contracts

                | Dependency | Type | Contract Consumed | Why It Matters |
                |---|---|---|---|
                | Database | External | stored request record | Request must persist |

                ## Acceptance Criteria

                ```gherkin
                Scenario: happy path
                  Given a valid request
                  When the API accepts it
                  Then the request is stored
                ```

                ```gherkin
                Scenario: invalid request
                  Given an invalid request
                  When the API accepts it
                  Then the request is rejected
                ```

                ```gherkin
                Scenario: duplicate request
                  Given the same request twice
                  When the API accepts it
                  Then the duplicate is handled safely
                ```

                ## Test Expectations

                | Test Type | What to Test | Why | Automation |
                |---|---|---|---|
                | API | request contract | API correctness | Must automate |

                ## Required Tests

                - API: request contract test

                ## Out of Scope

                - Frontend rendering

                ## Dependencies

                | Dependency | Type | Blocking? |
                |---|---|---|
                | Database | External | Yes |

                ## Open Questions

                | ID | Question | Impact |
                |---|---|---|
                | OQ-001 | None identified | No blocker |
                """
            ),
            encoding="utf-8",
        )
        (self.workspace_root / "epics" / "E-001-submit-request" / "stories" / "S-001.1-submit.agent.yaml").write_text(
            textwrap.dedent(
                """\
                story_id: S-001.1
                title: "Submit request"
                story_type: "backend-endpoint"
                layer: "backend"
                requirements_implemented: []
                requirements_referenced:
                  - FR-001
                  - FR-001
                depends_on:
                  - story_id: ""
                    reason: ""
                    consumes_contract: {}
                blocks: []
                in_scope: []
                out_of_scope: []
                implementation_contract:
                  touched_components: []
                  touched_files_or_areas: []
                  data_inputs: []
                  operations: []
                  success_behavior: []
                  error_handling: []
                required_tests:
                  unit: []
                  integration: []
                  api: []
                  e2e: []
                  accessibility: []
                done_evidence: []
                """
            ),
            encoding="utf-8",
        )

        checks = validation_module._validate_epic_folders_directory(
            self.workspace_root / "epics",
            self.workspace_root,
        )
        failed = {
            check["name"]: check["result"]
            for check in checks
            if check["target"].endswith("S-001.1-submit.md/S-001.1-submit.agent.yaml")
        }
        self.assertEqual(failed["story_agent_contract_requirements_implemented_valid"], "fail")
        self.assertEqual(failed["story_agent_contract_in_scope_present"], "fail")
        self.assertEqual(failed["story_agent_contract_required_tests_present"], "fail")

    def test_coverage_claim_matches_evidence_detects_missing_story_file(self) -> None:
        (self.workspace_root / "planning").mkdir(parents=True, exist_ok=True)
        (self.workspace_root / "epics" / "E-001-submit-request" / "stories").mkdir(parents=True, exist_ok=True)
        (self.workspace_root / "planning" / "fr-coverage.md").write_text(
            textwrap.dedent(
                """\
                # Requirement Coverage Report

                ## Coverage Summary

                | Metric | Value |
                |---|---|
                | Total requirements (from atomic-requirements) | 1 |
                | Covered by at least one story | 1 |
                | Not covered | 0 |
                | Coverage percentage | 100% |

                ## Full Coverage Matrix

                | REQ / FR | Requirement Title | Capability | Epic | Feature | Story | Open Questions Propagated | Evidence | Status |
                |---|---|---|---|---|---|---|---|---|
                | REQ-001 | Submit request | CAP-001 | E-001 | F-001 | F-001.9 | N/A | missing story | Covered |
                """
            ),
            encoding="utf-8",
        )
        (self.workspace_root / "epics" / "E-001-submit-request" / "stories" / "S-001.1-submit.md").write_text(
            "# story\n",
            encoding="utf-8",
        )

        result = validation_module._rule_coverage_claim_matches_evidence(
            self.workspace_root / "planning" / "fr-coverage.md",
            self.workspace_root,
            {},
            "planning/fr-coverage.md",
            [],
        )
        self.assertEqual(result["result"], "fail")
        self.assertIn("F-001.9", result["detail"])

    def test_selected_epics_have_implementation_contracts_uses_selected_epics_file(self) -> None:
        (self.workspace_root / "input").mkdir(parents=True, exist_ok=True)
        (self.workspace_root / "epics" / "E-001-submit-request").mkdir(parents=True, exist_ok=True)
        (self.workspace_root / "epics" / "E-002-track-status").mkdir(parents=True, exist_ok=True)
        (self.workspace_root / "input" / "selected-epics.md").write_text(
            "E-002\n",
            encoding="utf-8",
        )
        (self.workspace_root / "epics" / "E-001-submit-request" / "implementation-contract.md").write_text(
            "# contract 1\n",
            encoding="utf-8",
        )

        result = validation_module._rule_selected_epics_have_implementation_contracts(
            self.workspace_root / "epics",
            self.workspace_root,
            {},
            "epics/",
            [],
        )
        self.assertEqual(result["result"], "fail")
        self.assertIn("E-002", result["detail"])

        (self.workspace_root / "epics" / "E-002-track-status" / "implementation-contract.md").write_text(
            "# contract 2\n",
            encoding="utf-8",
        )
        result = validation_module._rule_selected_epics_have_implementation_contracts(
            self.workspace_root / "epics",
            self.workspace_root,
            {},
            "epics/",
            [],
        )
        self.assertEqual(result["result"], "pass")

    def test_selected_epics_have_coding_handoffs_uses_selected_epics_file(self) -> None:
        (self.workspace_root / "input").mkdir(parents=True, exist_ok=True)
        (self.workspace_root / "epics" / "E-001-submit-request").mkdir(parents=True, exist_ok=True)
        (self.workspace_root / "epics" / "E-002-track-status").mkdir(parents=True, exist_ok=True)
        (self.workspace_root / "input" / "selected-epics.md").write_text(
            "E-001\nE-002\n",
            encoding="utf-8",
        )
        (self.workspace_root / "epics" / "E-001-submit-request" / "coding-handoff.md").write_text(
            "# handoff 1\n",
            encoding="utf-8",
        )

        result = validation_module._rule_selected_epics_have_coding_handoffs(
            self.workspace_root / "epics",
            self.workspace_root,
            {},
            "epics/",
            [],
        )
        self.assertEqual(result["result"], "fail")
        self.assertIn("E-002", result["detail"])

        (self.workspace_root / "epics" / "E-002-track-status" / "coding-handoff.md").write_text(
            "# handoff 2\n",
            encoding="utf-8",
        )
        result = validation_module._rule_selected_epics_have_coding_handoffs(
            self.workspace_root / "epics",
            self.workspace_root,
            {},
            "epics/",
            [],
        )
        self.assertEqual(result["result"], "pass")

    def test_story_agent_contract_semantic_equivalence_passes_for_matching_pair(self) -> None:
        stories_dir = self.workspace_root / "epics" / "E-001-submit-request" / "stories"
        stories_dir.mkdir(parents=True, exist_ok=True)
        (stories_dir / "S-001.1-submit.md").write_text(
            textwrap.dedent(
                """\
                # S-001.1 - Submit request

                ## Metadata

                | Field | Value |
                |---|---|
                | Story Type | frontend-form |

                ## Requirements Implemented

                - REQ-001

                ## Requirements Referenced

                - FR-003

                ## Implementation Guidance

                - **API:** POST /requests

                ## Dependency Contracts

                | Dependency | Type | Contract Consumed | Why It Matters |
                |---|---|---|---|
                | S-001.2 | Story | POST /requests returns 201 | Confirmation depends on backend acceptance |

                ## UI Behaviour

                - **Page:** Submit request /submit

                ## Dependencies

                | Dependency | Type | Blocking? |
                |---|---|---|
                | S-001.2 | Story | Yes |
                """
            ),
            encoding="utf-8",
        )
        (stories_dir / "S-001.1-submit.agent.yaml").write_text(
            textwrap.dedent(
                """\
                story_id: S-001.1
                title: "Submit request"
                story_type: "frontend-form"
                layer: "frontend"
                requirements_implemented:
                  - REQ-001
                requirements_referenced:
                  - FR-003
                depends_on:
                  - story_id: "S-001.2"
                    reason: "Confirmation depends on backend acceptance"
                    consumes_contract:
                      type: "api"
                      summary: "POST /requests returns 201"
                implementation_contract:
                  operations:
                    - type: "api call"
                      target: "POST /requests"
                    - type: "ui action"
                      target: "/submit"
                """
            ),
            encoding="utf-8",
        )

        result = validation_module._rule_story_agent_contract_semantic_equivalence(
            self.workspace_root / "epics",
            self.workspace_root,
            {},
            "epics/",
            [],
        )
        self.assertEqual(result["result"], "pass")

    def test_story_agent_contract_semantic_equivalence_fails_for_mismatched_pair(self) -> None:
        stories_dir = self.workspace_root / "epics" / "E-001-submit-request" / "stories"
        stories_dir.mkdir(parents=True, exist_ok=True)
        (stories_dir / "S-001.1-submit.md").write_text(
            textwrap.dedent(
                """\
                # S-001.1 - Submit request

                ## Metadata

                | Field | Value |
                |---|---|
                | Story Type | backend-endpoint |

                ## Requirements Implemented

                - FR-001
                - FR-002

                ## Requirements Referenced

                - FR-003

                ## Implementation Guidance

                - **API:** POST /requests

                ## Dependencies

                | Dependency | Type | Blocking? |
                |---|---|---|
                | S-001.4 | Story | Yes |
                """
            ),
            encoding="utf-8",
        )
        (stories_dir / "S-001.1-submit.agent.yaml").write_text(
            textwrap.dedent(
                """\
                story_id: S-001.1
                title: "Submit request adapter"
                story_type: "frontend-form"
                layer: "frontend"
                requirements_implemented:
                  - FR-001
                requirements_referenced:
                  - FR-004
                depends_on:
                  - story_id: "S-001.2"
                    reason: "Different dependency"
                    consumes_contract:
                      type: "api"
                      summary: "POST /requests returns 201"
                implementation_contract:
                  operations:
                    - type: "api call"
                      target: "POST /other"
                """
            ),
            encoding="utf-8",
        )

        result = validation_module._rule_story_agent_contract_semantic_equivalence(
            self.workspace_root / "epics",
            self.workspace_root,
            {},
            "epics/",
            [],
        )
        self.assertEqual(result["result"], "fail")
        self.assertIn("requirements_implemented", result["detail"])
        self.assertIn("requirements_referenced", result["detail"])
        self.assertIn("dependencies", result["detail"])
        self.assertIn("operations missing from markdown context", result["detail"])

    def test_compute_coverage_distinguishes_covered_referenced_spike_and_deferred(self) -> None:
        (self.workspace_root / "requirements").mkdir(parents=True, exist_ok=True)
        (self.workspace_root / "planning").mkdir(parents=True, exist_ok=True)
        (self.workspace_root / "epics" / "E-001-intake" / "stories").mkdir(parents=True, exist_ok=True)
        (self.workspace_root / "requirements" / "atomic-requirements.md").write_text(
            textwrap.dedent(
                """\
                # Atomic Requirements

                ### FR-001 - Submit request
                Text

                ### FR-002 - Perform bureau spike
                Text

                ### FR-003 - Show dashboard status
                Text

                ### FR-004 - Experian adapter
                Text
                """
            ),
            encoding="utf-8",
        )
        (self.workspace_root / "planning" / "delivery-skeleton.md").write_text(
            textwrap.dedent(
                """\
                # Delivery Skeleton

                ## Requirement Coverage

                | REQ / FR | Feature | Epic | Status |
                |---|---|---|---|
                | FR-001 | F-001 | E-001 | Covered |
                | FR-002 | F-002 | E-001 | Covered |
                | FR-003 | F-003 | E-001 | Covered |
                | FR-004 | F-004 | E-002 | Deferred - Wave 2 because external vendor onboarding is pending |
                """
            ),
            encoding="utf-8",
        )
        (self.workspace_root / "epics" / "E-001-intake" / "stories" / "S-001.1-submit.md").write_text(
            textwrap.dedent(
                """\
                # S-001.1 - Submit request

                ## Metadata

                | Field | Value |
                |---|---|
                | Story Type | backend-endpoint |

                ## Requirements Implemented

                - FR-001

                ## Requirements Referenced

                - FR-003
                """
            ),
            encoding="utf-8",
        )
        (self.workspace_root / "epics" / "E-001-intake" / "stories" / "S-001.2-bureau-spike.md").write_text(
            textwrap.dedent(
                """\
                # S-001.2 - Bureau spike

                ## Metadata

                | Field | Value |
                |---|---|
                | Story Type | spike |

                ## Requirements Implemented

                - FR-002
                """
            ),
            encoding="utf-8",
        )

        result = coverage_module.compute_coverage(self.workspace_root)
        rows = {row["req_id"]: row for row in result["coverage_matrix"]}

        self.assertEqual(rows["FR-001"]["status"], "Covered")
        self.assertEqual(rows["FR-002"]["status"], "Spike Only")
        self.assertEqual(rows["FR-003"]["status"], "Referenced Only")
        self.assertEqual(rows["FR-004"]["status"], "Deferred")
        self.assertEqual(result["generated_coverage"]["covered"], 1)
        self.assertEqual(result["generated_coverage"]["weak_coverage_count"], 2)
        self.assertEqual(result["summary"]["deferred_wave_count"], 1)
        self.assertEqual(result["suggested_fixes"][0]["action"], "needs_non_spike_implementation_story")

    def test_coverage_classifications_acceptable_fails_for_weak_or_unjustified_deferred_coverage(self) -> None:
        (self.workspace_root / ".b2s" / "tmp").mkdir(parents=True, exist_ok=True)
        (self.workspace_root / ".b2s" / "tmp" / "computed-coverage.json").write_text(
            json.dumps(
                {
                    "coverage_matrix": [
                        {
                            "req_id": "FR-001",
                            "title": "Submit request",
                            "scope": "in_scope",
                            "status": "Referenced Only",
                            "evidence": "Only referenced in epics/E-001/stories/S-001.1.md",
                        },
                        {
                            "req_id": "FR-002",
                            "title": "Experian adapter",
                            "scope": "deferred_wave",
                            "status": "Deferred",
                            "evidence": "Deferred to E-002",
                        },
                    ]
                }
            ),
            encoding="utf-8",
        )

        result = validation_module._rule_coverage_classifications_acceptable(
            self.workspace_root / "planning" / "fr-coverage.md",
            self.workspace_root,
            {},
            "planning/fr-coverage.md",
            [],
        )
        self.assertEqual(result["result"], "fail")
        self.assertIn("Referenced Only", result["detail"])
        self.assertIn("deferred without explicit rationale", result["detail"])

    def test_parse_routing_fields_accepts_light_workflow_recommendation(self) -> None:
        (self.workspace_root / "routing").mkdir(parents=True, exist_ok=True)
        (self.workspace_root / "routing" / "routing-decision.md").write_text(
            textwrap.dedent(
                """\
                # Routing Decision

                | Field | Value |
                |---|---|
                | Delivery mode | OpenSpec |
                | Execution mode | Standard |
                | Recommended workflow type | agile-delivery-light-flow |
                """
            ),
            encoding="utf-8",
        )
        state = {}
        state_module._parse_routing_fields(self.workspace_root, state)
        self.assertEqual(state.get("workflow_type_recommended"), "agile-delivery-light-flow")

    def test_epic_review_summary_uses_validation_and_story_counts(self) -> None:
        (self.workspace_root / "epics" / "E-001-submit-request" / "stories").mkdir(parents=True, exist_ok=True)
        (self.workspace_root / "epics" / "E-001-submit-request" / "epic.md").write_text(
            textwrap.dedent(
                """\
                # E-001 - Submit request

                ## Stories

                | Story ID | Title | Layers | Priority | Increment | Readiness |
                |---|---|---|---|---|---|
                | S-001.1 | Submit request | Frontend | Must | D1 | Ready |
                | S-001.2 | Track request | Backend | Must | D1 | Not Ready |
                """
            ),
            encoding="utf-8",
        )
        (self.workspace_root / "epics" / "E-001-submit-request" / "stories" / "S-001.1-submit.md").write_text(
            textwrap.dedent(
                """\
                # S-001.1

                ## Acceptance Criteria

                ```gherkin
                Scenario: happy path
                  Given valid input
                  When submitted
                  Then accepted
                ```

                ```gherkin
                Scenario: validation failure
                  Given invalid input
                  When submitted
                  Then rejected
                ```
                """
            ),
            encoding="utf-8",
        )
        (self.workspace_root / "epics" / "E-001-submit-request" / "stories" / "S-001.2-track.md").write_text(
            textwrap.dedent(
                """\
                # S-001.2

                ## Acceptance Criteria

                ```gherkin
                Scenario: status shown
                  Given a request exists
                  When opened
                  Then the status is shown
                ```

                ## Open Questions

                | ID | Question | Impact |
                |---|---|---|
                | OQ-001 | Need status source | Blocks implementation |
                """
            ),
            encoding="utf-8",
        )
        validation_result = {
            "named_rule_results": [
                {"result": "fail", "rule_name": "no_unknown_requirement_references"},
                {"result": "fail", "rule_name": "requirement_title_consistency"},
                {"result": "fail", "rule_name": "coverage_claim_matches_evidence"},
                {"result": "fail", "rule_name": "requirement_semantics_preserved"},
            ]
        }

        summary = state_module._epic_review_summary(self.workspace_root, validation_result)
        self.assertEqual(summary["total_epics"], 1)
        self.assertEqual(summary["total_stories"], 2)
        self.assertEqual(summary["stories_with_2_plus_acceptance_criteria"], 1)
        self.assertEqual(summary["stories_with_open_questions"], 1)
        self.assertEqual(summary["not_ready_stories"], 1)
        self.assertEqual(summary["unknown_requirement_references"], 1)
        self.assertEqual(summary["requirement_title_mismatches"], 1)
        self.assertEqual(summary["coverage_or_semantic_warnings"], 2)

    def test_dispatch_gate_plan_includes_epic_review_summary(self) -> None:
        gate_state = {
            "gate_id": "epic-review",
            "owner": "delivery-lead",
            "artifact_path": "epics/",
            "review_summary": {
                "total_epics": 2,
                "total_stories": 5,
                "stories_with_2_plus_acceptance_criteria": 4,
                "stories_with_open_questions": 1,
                "not_ready_stories": 1,
                "unknown_requirement_references": 1,
                "requirement_title_mismatches": 2,
                "coverage_or_semantic_warnings": 3,
            },
        }
        state = {
            "initiative_id": "I001",
            "current_stage": "3-epic-elaboration",
            "awaiting_human": True,
            "current_gate": gate_state,
        }
        with mock.patch.object(dispatch_module.workspace, "load_state", return_value=state), mock.patch.object(
            dispatch_module.workspace,
            "load_stage_actions",
            return_value=([], {}),
        ), mock.patch.object(dispatch_module.workspace, "check_state_integrity", return_value=[]):
            plan = dispatch_module.build_plan(self.workspace_root)
        self.assertEqual(plan["status"], dispatch_module.STATUS_GATE)
        self.assertEqual(plan["review_summary"]["total_epics"], 2)
        self.assertEqual(plan["review_summary"]["requirement_title_mismatches"], 2)

    def test_augment_gate_payload_uses_registered_summary_builder(self) -> None:
        with mock.patch.dict(
            state_module.GATE_SUMMARY_BUILDERS,
            {"custom-gate": lambda workspace_root, validation_result: {"marker": "ok"}},
            clear=False,
        ):
            gate_state = state_module._augment_gate_payload(
                self.workspace_root,
                {"gate_id": "custom-gate"},
                {"named_rule_results": []},
            )
        self.assertEqual(gate_state["review_summary"], {"marker": "ok"})

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



class TechnicalSpecWorkflowTests(unittest.TestCase):
    """Tests for technical-spec-modular workflow type wiring, state parsing, and prompt rendering."""

    def setUp(self) -> None:
        RUNTIME_ROOT.mkdir(parents=True, exist_ok=True)
        self.workspace_root = RUNTIME_ROOT / self._testMethodName
        if self.workspace_root.exists():
            shutil.rmtree(self.workspace_root)
        (self.workspace_root / "input").mkdir(parents=True)
        (self.workspace_root / "input" / "brs.md").write_text(
            "# BRS\n\n## Functional Requirements\n- FR-001: Submit application.\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        if self.workspace_root.exists():
            shutil.rmtree(self.workspace_root)

    def read_json(self, relative_path: str) -> dict:
        return json.loads((self.workspace_root / relative_path).read_text(encoding="utf-8"))

    def read_yaml(self, relative_path: str) -> dict:
        return yaml.safe_load((self.workspace_root / relative_path).read_text(encoding="utf-8"))

    def _load_tsm_actions(self) -> tuple[list, dict]:
        """Load stage-actions from technical-spec-modular workflow type."""
        from b2s_engine import workspace as ws
        sa_path = REPO_ROOT / ".b2s" / "workflow-types" / "technical-spec-modular" / "stage-actions.yaml"
        data = yaml.safe_load(sa_path.read_text(encoding="utf-8"))
        actions = data["actions"]
        return actions, {a["action_id"]: a for a in actions}

    # --- Workflow-type initialization ---

    def test_init_workspace_with_technical_spec_modular_copies_files(self) -> None:
        """init-workspace --workflow-type technical-spec-modular must copy both YAML files."""
        workspace_root = RUNTIME_ROOT / f"{self._testMethodName}-ws"
        if workspace_root.exists():
            shutil.rmtree(workspace_root)
        try:
            run_cli(
                "init-workspace",
                "--workspace-root", str(workspace_root),
                "--initiative-id", "I099-TSM",
                "--workflow-type", "technical-spec-modular",
            )
            self.assertTrue((workspace_root / ".b2s" / "workflow" / "stage-actions.yaml").exists())
            self.assertTrue((workspace_root / ".b2s" / "workflow" / "workflow-definition.yaml").exists())
            record = json.loads((workspace_root / ".b2s" / "workflow" / "workflow-type.json").read_text(encoding="utf-8"))
            self.assertEqual(record["workflow_type"], "technical-spec-modular")
            state = json.loads((workspace_root / ".b2s" / "state" / "workflow-state.json").read_text(encoding="utf-8"))
            self.assertEqual(state["workflow_type"], "technical-spec-modular")
        finally:
            if workspace_root.exists():
                shutil.rmtree(workspace_root)

    def test_technical_spec_modular_index_entry_is_registered(self) -> None:
        """workflow-types/index.yaml must include technical-spec-modular."""
        index_path = REPO_ROOT / ".b2s" / "workflow-types" / "index.yaml"
        index = yaml.safe_load(index_path.read_text(encoding="utf-8"))
        ids = [wt["id"] for wt in index.get("workflow_types", [])]
        self.assertIn("technical-spec-modular", ids)

    def test_technical_spec_modular_index_entry_has_both_files(self) -> None:
        """The workflow-type path must contain both stage-actions.yaml and workflow-definition.yaml."""
        index_path = REPO_ROOT / ".b2s" / "workflow-types" / "index.yaml"
        index = yaml.safe_load(index_path.read_text(encoding="utf-8"))
        entry = next(wt for wt in index["workflow_types"] if wt["id"] == "technical-spec-modular")
        type_dir = REPO_ROOT / entry["path"]
        self.assertTrue((type_dir / "stage-actions.yaml").exists())
        self.assertTrue((type_dir / "workflow-definition.yaml").exists())

    # --- Stage-action wiring ---

    def test_tech_spec_actions_belong_to_4c_stage(self) -> None:
        """All four create-*-specs actions must have stage_id == 4c-technical-specifications."""
        _, actions_by_id = self._load_tsm_actions()
        for action_id in ("create-exposed-api-specs", "create-consumed-api-specs",
                          "create-data-schema-specs", "create-integration-specs"):
            action = actions_by_id[action_id]
            self.assertEqual(
                action["stage_id"], "4c-technical-specifications",
                msg=f"{action_id}: expected stage_id 4c-technical-specifications, got {action['stage_id']}",
            )

    def test_handoff_action_blocked_by_4d_not_4b_in_tsm(self) -> None:
        """In technical-spec-modular, create-openspec-handoff must be blocked by 4d-quality-gates."""
        _, actions_by_id = self._load_tsm_actions()
        handoff = actions_by_id["create-openspec-handoff"]
        blocked_stages = handoff.get("blocked_by_stage", [])
        self.assertIn("4d-quality-gates", blocked_stages)
        self.assertNotIn("4b-quality-gates", blocked_stages)

    def test_quality_gate_actions_belong_to_4d_stage_in_tsm(self) -> None:
        """In technical-spec-modular, core quality-gate actions must use stage_id 4d-quality-gates."""
        _, actions_by_id = self._load_tsm_actions()
        for action_id in ("create-bdd-scenarios", "create-api-contract", "create-security-review"):
            action = actions_by_id[action_id]
            self.assertEqual(
                action["stage_id"], "4d-quality-gates",
                msg=f"{action_id}: expected 4d-quality-gates in tsm, got {action['stage_id']}",
            )

    def test_tsm_create_exposed_api_specs_blocked_by_engineering_readiness(self) -> None:
        """In technical-spec-modular, create-exposed-api-specs must be blocked by 4-engineering-readiness."""
        _, actions_by_id = self._load_tsm_actions()
        action = actions_by_id["create-exposed-api-specs"]
        self.assertIn("4-engineering-readiness", action.get("blocked_by_stage", []))

    def test_tsm_workflow_definition_has_4c_stage(self) -> None:
        """technical-spec-modular workflow-definition.yaml must define stage 4c-technical-specifications."""
        wd_path = REPO_ROOT / ".b2s" / "workflow-types" / "technical-spec-modular" / "workflow-definition.yaml"
        wd = yaml.safe_load(wd_path.read_text(encoding="utf-8"))
        stage_ids = [s["id"] for s in wd["stages"]]
        self.assertIn("4c-technical-specifications", stage_ids)
        self.assertIn("4d-quality-gates", stage_ids)
        self.assertNotIn("4b-quality-gates", stage_ids)

    # --- State field parsing ---

    def test_api_contract_mode_defaults_to_internal_when_absent(self) -> None:
        """When readiness-check.md has no API contract mode row, state must default to 'internal'."""
        from b2s_engine import state as state_module
        run_cli("next-step", "--workspace-root", str(self.workspace_root))
        (self.workspace_root / "engineering-readiness").mkdir(parents=True, exist_ok=True)
        (self.workspace_root / "engineering-readiness" / "readiness-check.md").write_text(
            textwrap.dedent("""\
                # Engineering Readiness Check

                ## Core Checklist

                | # | Item | Status |
                |---|---|---|
                | 1 | BRS complete | Pass |

                ## Gate Trigger Decisions

                | Gate | Triggered | Trigger Evidence | Required |
                |---|---|---|---|
                | BDD Scenarios | Yes | coverage needed | Yes |

                ## Readiness Decision

                | Field | Value |
                |---|---|
                | Readiness score | 75 / 100 |
                | Decision | Ready |
            """),
            encoding="utf-8",
        )
        state = json.loads((self.workspace_root / ".b2s" / "state" / "workflow-state.json").read_text(encoding="utf-8"))
        state_module._parse_readiness_fields(self.workspace_root, state)
        self.assertEqual(state["api_contract_mode"], "internal")

    def test_api_contract_mode_parsed_as_product(self) -> None:
        """When readiness-check.md has 'API contract mode | product', state must store 'product'."""
        from b2s_engine import state as state_module
        run_cli("next-step", "--workspace-root", str(self.workspace_root))
        (self.workspace_root / "engineering-readiness").mkdir(parents=True, exist_ok=True)
        (self.workspace_root / "engineering-readiness" / "readiness-check.md").write_text(
            textwrap.dedent("""\
                # Engineering Readiness Check

                ## Gate Trigger Decisions

                | Gate | Triggered | Trigger Evidence | Required |
                |---|---|---|---|
                | API contract mode | product | external consumers | Required |

                ## Readiness Decision

                | Field | Value |
                |---|---|
                | Readiness score | 80 / 100 |
                | Decision | Ready |
            """),
            encoding="utf-8",
        )
        state = json.loads((self.workspace_root / ".b2s" / "state" / "workflow-state.json").read_text(encoding="utf-8"))
        state_module._parse_readiness_fields(self.workspace_root, state)
        self.assertEqual(state["api_contract_mode"], "product")

    def test_api_contract_mode_parsed_as_coordinated(self) -> None:
        """When readiness-check.md has 'API contract mode | coordinated', state must store 'coordinated'."""
        from b2s_engine import state as state_module
        run_cli("next-step", "--workspace-root", str(self.workspace_root))
        (self.workspace_root / "engineering-readiness").mkdir(parents=True, exist_ok=True)
        (self.workspace_root / "engineering-readiness" / "readiness-check.md").write_text(
            textwrap.dedent("""\
                # Engineering Readiness Check

                ## Gate Trigger Decisions

                | Gate | Triggered | Trigger Evidence | Required |
                |---|---|---|---|
                | API contract mode | coordinated | draft early | Required |

                ## Readiness Decision

                | Field | Value |
                |---|---|
                | Readiness score | 72 / 100 |
                | Decision | Ready |
            """),
            encoding="utf-8",
        )
        state = json.loads((self.workspace_root / ".b2s" / "state" / "workflow-state.json").read_text(encoding="utf-8"))
        state_module._parse_readiness_fields(self.workspace_root, state)
        self.assertEqual(state["api_contract_mode"], "coordinated")

    def test_api_contract_mode_invalid_value_defaults_to_internal(self) -> None:
        """An unrecognized api_contract_mode value must fall back to 'internal'."""
        from b2s_engine import state as state_module
        run_cli("next-step", "--workspace-root", str(self.workspace_root))
        (self.workspace_root / "engineering-readiness").mkdir(parents=True, exist_ok=True)
        (self.workspace_root / "engineering-readiness" / "readiness-check.md").write_text(
            textwrap.dedent("""\
                # Engineering Readiness Check

                ## Gate Trigger Decisions

                | Gate | Triggered | Trigger Evidence | Required |
                |---|---|---|---|
                | API contract mode | unknown-value | typo | Required |

                ## Readiness Decision

                | Field | Value |
                |---|---|
                | Readiness score | 70 / 100 |
                | Decision | Ready |
            """),
            encoding="utf-8",
        )
        state: dict = {"api_contract_mode": None}
        state_module._parse_readiness_fields(self.workspace_root, state)
        self.assertEqual(state["api_contract_mode"], "internal")

    # --- Condition evaluation for tech-spec sequencing ---

    def test_create_exposed_api_specs_condition_requires_api_contract_triggered(self) -> None:
        """create-exposed-api-specs must require API_CONTRACT in quality_gates_triggered."""
        from b2s_engine.next_step import evaluate_condition
        from b2s_engine import workspace as ws
        _, actions_by_id = self._load_tsm_actions()
        action = actions_by_id["create-exposed-api-specs"]
        conditions = action.get("conditions", [])
        self.assertTrue(conditions, "create-exposed-api-specs must have at least one condition")

        state_with_api = {
            "action_status": {},
            "readiness_score": 80,
            "optional_artifacts_requested": [],
            "quality_gates_triggered": ["API_CONTRACT"],
        }
        state_without_api = {
            "action_status": {},
            "readiness_score": 80,
            "optional_artifacts_requested": [],
            "quality_gates_triggered": ["BDD"],
        }
        condition = conditions[0]
        self.assertTrue(
            evaluate_condition(condition, state_with_api, self.workspace_root, actions_by_id),
            "condition must pass when API_CONTRACT is in quality_gates_triggered",
        )
        self.assertFalse(
            evaluate_condition(condition, state_without_api, self.workspace_root, actions_by_id),
            "condition must fail when API_CONTRACT is absent from quality_gates_triggered",
        )

    def test_blocked_by_stage_satisfied_for_tsm_handoff_after_4d_complete(self) -> None:
        """In tsm, create-openspec-handoff blocked_by_stage must be satisfied when 4d is complete."""
        from b2s_engine.next_step import _blocked_by_stage_satisfied
        _, actions_by_id = self._load_tsm_actions()

        # 4d is complete when all condition-matching actions in it are done
        state = {
            "delivery_mode": "OpenSpec",
            "readiness_score": 78,
            "optional_artifacts_requested": [],
            "quality_gates_triggered": ["API_CONTRACT", "BDD"],
            "action_status": {
                "create-api-contract": "ai_validated",
                "create-bdd-scenarios": "ai_validated",
            },
            "artifact_status": {},
        }
        handoff_action = actions_by_id["create-openspec-handoff"]
        result = _blocked_by_stage_satisfied(handoff_action, state, actions_by_id, self.workspace_root)
        self.assertTrue(result, "tsm handoff must be unblocked when 4d-quality-gates actions are complete")

    # --- Placeholder-driven prompt rendering ---

    def test_create_exposed_api_specs_prompt_renders_without_placeholder_tokens(self) -> None:
        """create-exposed-api-specs skill prompt must render with placeholders substituted."""
        (self.workspace_root / "architecture").mkdir(parents=True)
        (self.workspace_root / "architecture" / "architecture-review.md").write_text("# Review\n", encoding="utf-8")
        (self.workspace_root / "architecture" / "architecture-rules.md").write_text("# Rules\n", encoding="utf-8")
        (self.workspace_root / "engineering-readiness").mkdir()
        (self.workspace_root / "engineering-readiness" / "readiness-check.md").write_text("# Readiness\n", encoding="utf-8")

        tsm_sa_path = REPO_ROOT / ".b2s" / "workflow-types" / "technical-spec-modular" / "stage-actions.yaml"
        actions = yaml.safe_load(tsm_sa_path.read_text(encoding="utf-8"))["actions"]
        action = next(a for a in actions if a["action_id"] == "create-exposed-api-specs")

        summary = dispatch_module._action_summary(action, self.workspace_root)
        rendered = summary.get("rendered_skill_text") or ""

        self.assertNotIn("{resolved_required_inputs}", rendered)
        self.assertNotIn("{resolved_optional_inputs}", rendered)
        self.assertNotIn("{primary_output}", rendered)

    def test_tsm_handoff_skill_references_technical_spec_paths(self) -> None:
        """create-openspec-handoff skill must mention technical-specifications/ paths after imp/08."""
        skill_path = REPO_ROOT / ".b2s" / "skills" / "engineering-lead" / "create-openspec-handoff.md"
        skill_text = skill_path.read_text(encoding="utf-8")
        self.assertIn("quality-gates/nfr-assessment.md", skill_text)
        self.assertIn("technical-specifications/api/exposed/", skill_text)
        self.assertIn("technical-specifications/api/consumed/", skill_text)
        self.assertIn("technical-specifications/data/", skill_text)
        self.assertIn("technical-specifications/integrations/", skill_text)

    def test_tsm_standalone_handoff_skill_references_technical_spec_paths(self) -> None:
        """create-standalone-handoff skill must mention technical-specifications/ paths after imp/08."""
        skill_path = REPO_ROOT / ".b2s" / "skills" / "engineering-lead" / "create-standalone-handoff.md"
        skill_text = skill_path.read_text(encoding="utf-8")
        self.assertIn("quality-gates/nfr-assessment.md", skill_text)
        self.assertIn("technical-specifications/api/exposed/", skill_text)
        self.assertIn("technical-specifications/integrations/", skill_text)


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

    def test_named_required_rule_failure_is_reported(self) -> None:
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            artifact = Path(tmp) / "requirements.md"
            artifact.write_text(
                "# Requirements\n\n## Functional Requirements\n\n| Requirement ID | Summary |\n|---|---|\n| FR-001 | TBD |\n",
                encoding="utf-8",
            )
            action = self._make_action(
                action_id="create-requirements",
                outputs={"primary": "business-analysis/requirements.md", "secondary": []},
                validation_rules={"required": ["requirement_has_id", "requirement_is_testable"], "optional": []},
            )
            base_checks = [
                {"name": "fr_not_template_only", "target": artifact.name, "result": "fail", "detail": "placeholder text"},
                {"name": "nfr_section_not_empty", "target": artifact.name, "result": "fail", "detail": "missing"},
                {"name": "constraints_section_not_empty", "target": artifact.name, "result": "fail", "detail": "missing"},
            ]
            results = validation_module._run_named_validation_rules(
                action,
                artifact,
                Path(tmp),
                "business-analysis/requirements.md",
                base_checks,
            )
            self.assertTrue(any(r["rule_name"] == "requirement_is_testable" and r["result"] == "fail" for r in results))

    def test_named_rule_unknown_is_reported(self) -> None:
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            artifact = Path(tmp) / "result.md"
            artifact.write_text("content", encoding="utf-8")
            action = self._make_action(
                validation_rules={"required": ["unknown_rule_name"], "optional": []},
            )
            results = validation_module._run_named_validation_rules(
                action,
                artifact,
                Path(tmp),
                "test-output/result.md",
                [],
            )
            self.assertEqual(results[0]["rule_name"], "unknown_rule_name")
            self.assertEqual(results[0]["result"], "fail")

    def test_nfr_named_rules_pass_for_complete_assessment(self) -> None:
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            artifact = Path(tmp) / "nfr-assessment.md"
            artifact.write_text(
                textwrap.dedent(
                    """\
                    # NFR Assessment

                    ## NFR Catalog

                    | NFR ID | Domain | Requirement | Measure / Target | Source | Blocking |
                    |---|---|---|---|---|---|
                    | NFR-001 | Security | Encrypt audit events at rest | AES-256 | architecture-review.md | Yes |

                    ## Security

                    Security controls are defined and mapped to the auth boundary.

                    ## Availability

                    Availability target is defined for the core submission path.

                    ## Resiliency

                    Retry and fallback behavior are explicitly defined.

                    ## Observability

                    Logs, metrics, traces, and alert expectations are defined.

                    ## Supportability

                    Diagnostics and ownership are explicit.

                    ## Scalability

                    Capacity and throughput expectations are documented.

                    ## Compliance

                    Regulatory obligations and controls are listed.

                    ## Decision

                    Ready for handoff with monitored operational follow-ups.
                    """
                ),
                encoding="utf-8",
            )
            action = self._make_action(
                action_id="create-nfr-assessment",
                outputs={"primary": "quality-gates/nfr-assessment.md", "secondary": []},
                validation_rules={
                    "required": [
                        "nfr_assessment_has_ids",
                        "nfr_assessment_covers_core_domains",
                        "nfr_assessment_has_decision",
                    ],
                    "optional": [],
                },
            )
            results = validation_module._run_named_validation_rules(
                action,
                artifact,
                Path(tmp),
                "quality-gates/nfr-assessment.md",
                [],
            )
            self.assertTrue(all(result["result"] == "pass" for result in results))

    def test_atomic_requirements_source_first_ids_pass_required_rules_when_summary_rule_is_optional(self) -> None:
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            workspace_root = Path(tmp)
            (workspace_root / "input").mkdir(parents=True)
            (workspace_root / "input" / "brs.md").write_text(
                textwrap.dedent(
                    """\
                    # BRS

                    ## Business objectives
                    | ID | Objective |
                    |---|---|
                    | OBJ-001 | Improve intake speed |

                    ## Functional requirements
                    **FR-001** - Allow intake submission.

                    ## Non-functional requirements
                    | ID | Requirement |
                    |---|---|
                    | NFR-001 | Encrypt applicant data |
                    """
                ),
                encoding="utf-8",
            )

            artifact = workspace_root / "atomic-requirements.md"
            artifact.write_text(
                textwrap.dedent(
                    """\
                    # Atomic Requirements

                    ## Summary

                    | Metric | Value |
                    |---|---|
                    | Total requirements | 99 |
                    | Business objectives | 1 |
                    | Functional | 1 |
                    | Non-functional | 1 |
                    | Constraints | 1 |

                    ## Source Inventory

                    | Source ID | Type | Title / Summary | Preserved In |
                    |---|---|---|---|
                    | OBJ-001 | Objective | Improve intake speed | OBJ-001 |
                    | FR-001 | Functional | Allow intake submission | FR-001 |
                    | NFR-001 | Non-functional | Encrypt applicant data | NFR-001 |
                    | C-001 | Constraint | Data must remain in region | C-001 |

                    ## Requirement Catalogue

                    ### OBJ-001 - Improve intake speed

                    **Source:** Business objectives | **Actor:** Product Owner | **Deps:** None

                    THE SYSTEM SHALL reduce intake turnaround time.

                    ### FR-001 - Allow intake submission

                    **Source:** Functional requirements | **Actor:** Analyst | **Deps:** None

                    WHEN an analyst submits an intake request,
                    THE SYSTEM SHALL store the request and return a confirmation.

                    ### NFR-001 - Encrypt applicant data

                    **Source:** Non-functional requirements | **Actor:** Platform | **Deps:** FR-001

                    THE SYSTEM SHALL encrypt applicant data at rest.

                    ### C-001 - Regional data residency

                    **Source:** Constraints | **Actor:** Platform | **Deps:** None

                    THE SYSTEM SHALL keep applicant data in the approved region.
                    """
                ),
                encoding="utf-8",
            )

            action = self._make_action(
                action_id="create-atomic-requirements",
                outputs={"primary": "requirements/atomic-requirements.md", "secondary": []},
                validation_rules={
                    "required": ["requirement_has_id", "source_brs_ids_preserved"],
                    "optional": ["atomic_requirements_summary_matches_catalog"],
                },
            )
            results = validation_module._run_named_validation_rules(
                action,
                artifact,
                workspace_root,
                "requirements/atomic-requirements.md",
                [],
            )

            by_rule = {result["rule_name"]: result for result in results}
            self.assertEqual(by_rule["requirement_has_id"]["result"], "pass")
            self.assertEqual(by_rule["source_brs_ids_preserved"]["result"], "pass")
            self.assertEqual(by_rule["atomic_requirements_summary_matches_catalog"]["result"], "fail")
            self.assertEqual(by_rule["atomic_requirements_summary_matches_catalog"]["severity"], "optional")


if __name__ == "__main__":
    unittest.main()
