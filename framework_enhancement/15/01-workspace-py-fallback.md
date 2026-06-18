# Prompt 01 — Update workspace.py to Read Workflow from Initiative First

## Context

You are working on the `.b2s` framework at the root of this repository.

Today `load_stage_actions()` and `load_workflow_definition()` in `workspace.py`
always read from the central framework:

```python
def load_stage_actions():
    payload = load_yaml_file(FRAMEWORK_ROOT / "workflow" / "stage-actions.yaml")
    ...

def load_workflow_definition():
    return load_yaml_file(FRAMEWORK_ROOT / "workflow" / "workflow-definition.yaml")
```

These functions have no knowledge of the initiative workspace — they always use
the central `.b2s/workflow/` files. This means all initiatives share one workflow.

This prompt changes both functions to accept an optional `workspace_root` and look
for initiative-local workflow files first, falling back to the central framework.

Read `workspace.py` in full before making any changes.

---

## Step 1 — Update load_stage_actions

Change the signature to:

```python
def load_stage_actions(
    workspace_root: Path | None = None,
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
```

Logic:
1. If `workspace_root` is not None, check for `workspace_root / ".b2s" / "workflow" / "stage-actions.yaml"`
2. If that file exists, load it — this is the initiative-local workflow
3. If it does not exist, fall back to `FRAMEWORK_ROOT / "workflow" / "stage-actions.yaml"`
4. Build and return `(actions, by_id)` as before

---

## Step 2 — Update load_workflow_definition

Change the signature to:

```python
def load_workflow_definition(
    workspace_root: Path | None = None,
) -> dict[str, Any]:
```

Same logic:
1. If `workspace_root` is not None, check for `workspace_root / ".b2s" / "workflow" / "workflow-definition.yaml"`
2. If exists, load it
3. If not, fall back to `FRAMEWORK_ROOT / "workflow" / "workflow-definition.yaml"`

---

## Step 3 — Update all callers to pass workspace_root

Search the entire `.b2s/scripts/` directory for every call to `load_stage_actions()`
and `load_workflow_definition()`. Pass `workspace_root` where it is available in
the calling context.

The callers are in:
- `next_step.py` — `select_next_action` already receives `workspace_root`
- `state.py` — `run` and `repair_state` both have `workspace_root`
- `validation.py` — `run` has `workspace_root`
- `gates.py` — gate functions have `workspace_root`
- `dispatch.py` — `build_plan` has `workspace_root`

For any caller that does not have `workspace_root` in scope, pass `None`
(falls back to central — safe default).

---

## Step 4 — Add a helper to report which workflow is active

Add to `workspace.py`:

```python
def active_workflow_source(workspace_root: Path) -> str:
    """Return 'local' if initiative has its own workflow, 'central' otherwise."""
    local = workspace_root / ".b2s" / "workflow" / "stage-actions.yaml"
    return "local" if local.exists() else "central"
```

This is used in `dispatch-next` output and execution log to make the active
workflow source visible.

---

## Step 5 — Update dispatch.py to report workflow source

In `dispatch.py`, `build_plan`, add `workflow_source` to the returned plan dict:

```python
"workflow_source": workspace.active_workflow_source(workspace_root),
```

Print it in the human-readable output:

```
[dispatch-next] I014-NEXT14  stage=0-routing  status=ready  workflow=local
```

---

## Step 6 — Verify

Run the full test suite:

```
python -m pytest .b2s/tests/ -q
```

All 55 existing tests must pass. No test should fail because the fallback to
central workflow is the default when `workspace_root` has no local workflow files.

---

## Done criteria

- [ ] `load_stage_actions(workspace_root=None)` loads local file when present, central otherwise
- [ ] `load_workflow_definition(workspace_root=None)` same behaviour
- [ ] All callers in `.b2s/scripts/` pass `workspace_root` where available
- [ ] `active_workflow_source(workspace_root)` helper added
- [ ] `dispatch-next` output includes `workflow_source`
- [ ] All 55 existing tests pass
