# Prompt 03 — Update init-workspace to Copy Selected Workflow

## Context

You are working on the `.b2s` framework at the root of this repository.

The workflow-types library exists from prompt 02.
workspace.py reads initiative-local workflow files from prompt 01.

This prompt updates `init-workspace` to:
1. Accept a `--workflow-type` argument
2. Copy the selected workflow type's files into the initiative workspace
3. Write a `workflow-type.json` record into the initiative

Read `init_workspace.py` in full before making any changes.
Read `b2s_cli.py` in full to understand how to add the new argument.

---

## Step 1 — Add --workflow-type argument to b2s_cli.py

In `build_parser()`, find the `init-workspace` subparser block. Add:

```python
if name == "init-workspace":
    subparser.add_argument(
        "--workflow-type",
        type=str,
        required=False,
        default="enterprise-modular",
        help=(
            "Workflow type to initialise this initiative with. "
            "Must match an entry in .b2s/workflow-types/index.yaml. "
            "Defaults to 'enterprise-modular'."
        ),
    )
```

---

## Step 2 — Update init_workspace.py

In `run(args)`, after creating the `.b2s` runtime layout and before writing
the result JSON, add the workflow copy step:

```python
workflow_type = getattr(args, "workflow_type", None) or "enterprise-modular"
_copy_workflow_type(workspace_root, workflow_type)
```

Implement `_copy_workflow_type`:

```python
def _copy_workflow_type(workspace_root: Path, workflow_type: str) -> None:
    """Copy workflow type files into the initiative workspace."""
    index_path = workspace.FRAMEWORK_ROOT / "workflow-types" / "index.yaml"
    if not index_path.exists():
        raise FileNotFoundError(
            f"Workflow types index not found: {index_path}\n"
            "Run the framework setup to create it."
        )

    import yaml
    index = yaml.safe_load(index_path.read_text(encoding="utf-8"))
    types_by_id = {wt["id"]: wt for wt in index.get("workflow_types", [])}

    if workflow_type not in types_by_id:
        available = ", ".join(types_by_id.keys())
        raise ValueError(
            f"Unknown workflow type: '{workflow_type}'. "
            f"Available types: {available}"
        )

    source_dir = workspace.REPO_ROOT / types_by_id[workflow_type]["path"]
    dest_dir = workspace_root / ".b2s" / "workflow"
    dest_dir.mkdir(parents=True, exist_ok=True)

    # Copy stage-actions.yaml and workflow-definition.yaml
    for filename in ("stage-actions.yaml", "workflow-definition.yaml"):
        source = source_dir / filename
        dest = dest_dir / filename
        if not source.exists():
            raise FileNotFoundError(
                f"Workflow type '{workflow_type}' is missing {filename}: {source}"
            )
        shutil.copyfile(source, dest)

    # Write workflow-type.json record
    record = {
        "workflow_type": workflow_type,
        "source_path": str(source_dir),
        "copied_at": datetime.now(tz=timezone.utc).isoformat(),
        "files_copied": ["stage-actions.yaml", "workflow-definition.yaml"],
    }
    workspace.save_json_file(dest_dir / "workflow-type.json", record)
```

---

## Step 3 — Update the result report

In the result dict returned by `run`, add:

```python
"workflow_type": workflow_type,
"workflow_files": [
    ".b2s/workflow/stage-actions.yaml",
    ".b2s/workflow/workflow-definition.yaml",
    ".b2s/workflow/workflow-type.json",
],
```

And extend the `created` list to include the workflow files.

Update the message:

```python
f"Initiative {initiative_id} workspace created with workflow type '{workflow_type}'. "
f"Fill in {brs_path.relative_to(workspace_root)} then run the workflow."
```

---

## Step 4 — Update workflow-state.json template

Read `.b2s/templates/state/workflow-state.json`.

Add `"workflow_type": null` as a new field.

In `init_workspace.py`, after `_copy_workflow_type`, set it in state:

```python
state["workflow_type"] = workflow_type
```

---

## Step 5 — Verify with a test initiative

Create a temporary test initiative to verify the copy works:

```
python .b2s/scripts/b2s_cli.py init-workspace \
  --initiative-id I999-TEST-WORKFLOW \
  --workflow-type fast-path
```

Verify:
- `initiatives/I999-TEST-WORKFLOW/.b2s/workflow/stage-actions.yaml` exists
- `initiatives/I999-TEST-WORKFLOW/.b2s/workflow/workflow-definition.yaml` exists
- `initiatives/I999-TEST-WORKFLOW/.b2s/workflow/workflow-type.json` contains `"workflow_type": "fast-path"`
- `initiatives/I999-TEST-WORKFLOW/.b2s/state/workflow-state.json` contains `"workflow_type": "fast-path"`

Then delete `initiatives/I999-TEST-WORKFLOW/` — it is a test artefact only.

---

## Step 6 — Run full test suite

```
python -m pytest .b2s/tests/ -q
```

All existing tests must pass.

---

## Done criteria

- [ ] `--workflow-type` argument added to `init-workspace` CLI command, defaults to `enterprise-modular`
- [ ] `_copy_workflow_type` copies `stage-actions.yaml` and `workflow-definition.yaml` into `WORKSPACE_ROOT/.b2s/workflow/`
- [ ] `workflow-type.json` written with type, source path, and timestamp
- [ ] `workflow-state.json` contains `workflow_type` field set at init time
- [ ] Result JSON includes `workflow_type` and `workflow_files`
- [ ] Unknown workflow type raises a clear error with available options listed
- [ ] Manual test with `I999-TEST-WORKFLOW` passes; test folder deleted after
- [ ] All existing tests pass
