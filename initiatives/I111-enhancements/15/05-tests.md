# Prompt 05 — Tests for Per-Initiative Workflow Loading

## Context

You are working on the `.b2s` framework at the root of this repository.

Per-initiative workflow loading was implemented in prompts 01-04.
This prompt adds tests that verify the fallback logic and local workflow override.

Read these files in full before writing tests:
- `.b2s/tests/test_engine_fixtures.py` — existing test style and fixtures
- `.b2s/scripts/b2s_engine/workspace.py` — `load_stage_actions`, `load_workflow_definition`
- `.b2s/workflow-types/fast-path/stage-actions.yaml` — used in fixture

---

## Step 1 — Create fixture: local-workflow-override

Create `.b2s/tests/fixtures/local-workflow-override/`:

**`.b2s/state/workflow-state.json`:**
```json
{
  "initiative_id": "I999-LOCAL-WF",
  "workflow_type": "fast-path",
  "active_action": "route-initiative",
  "next_action": "route-initiative",
  "action_status": {},
  "artifact_status": {}
}
```

**`.b2s/workflow/stage-actions.yaml`:**
Copy the fast-path `stage-actions.yaml` from `.b2s/workflow-types/fast-path/stage-actions.yaml`.
This is the initiative-local workflow file.

**`.b2s/workflow/workflow-definition.yaml`:**
Copy the fast-path `workflow-definition.yaml` from `.b2s/workflow-types/fast-path/workflow-definition.yaml`.

**`.b2s/workflow/workflow-type.json`:**
```json
{
  "workflow_type": "fast-path",
  "copied_at": "2026-06-17T00:00:00+00:00",
  "files_copied": ["stage-actions.yaml", "workflow-definition.yaml"]
}
```

---

## Step 2 — Create fixture: no-local-workflow (central fallback)

Create `.b2s/tests/fixtures/no-local-workflow/`:

**`.b2s/state/workflow-state.json`:**
```json
{
  "initiative_id": "I998-CENTRAL-WF",
  "workflow_type": null,
  "active_action": "route-initiative",
  "next_action": "route-initiative",
  "action_status": {},
  "artifact_status": {}
}
```

No `.b2s/workflow/` folder — this initiative has no local workflow.
The engine must fall back to the central framework workflow.

---

## Step 3 — Add WorkflowLoadingTests to test_engine_fixtures.py

Add a new test class `WorkflowLoadingTests`:

```python
class WorkflowLoadingTests(unittest.TestCase):

    def test_local_workflow_is_used_when_present(self):
        """When initiative has .b2s/workflow/stage-actions.yaml, it is used instead of central."""
        ws = FIXTURES_DIR / "local-workflow-override"
        actions, by_id = workspace.load_stage_actions(workspace_root=ws)
        action_ids = [a["action_id"] for a in actions]
        # fast-path does NOT include create-requirements (enterprise-modular only)
        self.assertNotIn("create-requirements", action_ids)
        # fast-path DOES include route-initiative
        self.assertIn("route-initiative", action_ids)

    def test_central_workflow_used_when_no_local(self):
        """When initiative has no .b2s/workflow/, central stage-actions.yaml is used."""
        ws = FIXTURES_DIR / "no-local-workflow"
        actions, by_id = workspace.load_stage_actions(workspace_root=ws)
        action_ids = [a["action_id"] for a in actions]
        # enterprise-modular includes create-requirements
        self.assertIn("create-requirements", action_ids)

    def test_workflow_source_local(self):
        """active_workflow_source returns 'local' when initiative has local workflow."""
        ws = FIXTURES_DIR / "local-workflow-override"
        self.assertEqual(workspace.active_workflow_source(ws), "local")

    def test_workflow_source_central(self):
        """active_workflow_source returns 'central' when initiative has no local workflow."""
        ws = FIXTURES_DIR / "no-local-workflow"
        self.assertEqual(workspace.active_workflow_source(ws), "central")

    def test_next_step_uses_local_workflow(self):
        """next_step.select_next_action uses initiative-local workflow when present."""
        ws = FIXTURES_DIR / "local-workflow-override"
        state = workspace.load_state(ws)
        result = next_step.select_next_action(ws, state)
        # fast-path first action is route-initiative
        self.assertEqual(result["selected_action"], "route-initiative")
        # verify it read the local workflow (not central) by checking stage
        self.assertEqual(result["selected_stage"], "0-routing")
```

---

## Step 4 — Run full test suite

```
python -m pytest .b2s/tests/ -q
```

Expected: 55 existing tests + 5 new tests = 60 tests passing.

---

## Done criteria

- [ ] Fixture `local-workflow-override` created with fast-path workflow files
- [ ] Fixture `no-local-workflow` created with no local workflow folder
- [ ] `WorkflowLoadingTests` class with 5 tests added to `test_engine_fixtures.py`
- [ ] `test_local_workflow_is_used_when_present` asserts fast-path actions loaded
- [ ] `test_central_workflow_used_when_no_local` asserts central actions loaded
- [ ] `test_workflow_source_local` and `test_workflow_source_central` pass
- [ ] `test_next_step_uses_local_workflow` passes
- [ ] All 60 tests pass
