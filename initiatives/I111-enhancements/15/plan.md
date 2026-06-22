# Framework Enhancement 15 — Per-Initiative Workflow Bundling

## Problem Statement

Today every initiative reads its workflow definition from the central framework:

```python
FRAMEWORK_ROOT / "workflow" / "stage-actions.yaml"
FRAMEWORK_ROOT / "workflow" / "workflow-definition.yaml"
```

This means:
- All initiatives share one workflow — no way to run a different workflow type per initiative
- Framework changes immediately affect all in-progress initiatives
- There is no concept of "this initiative runs the enterprise-modular workflow, that one runs fast-path"
- The workflow type is implicit (inferred from delivery_mode conditions) rather than explicit

## Design Decision

At `init-workspace` time, copy the selected workflow definition files into the initiative:

```
initiatives/I014-NEXT14/
  .b2s/
    workflow/
      stage-actions.yaml        ← copied from selected workflow type
      workflow-definition.yaml  ← copied from selected workflow type
      workflow-type.json        ← records which type was selected and when
```

Every CLI command reads from `WORKSPACE_ROOT/.b2s/workflow/` first, falling back
to the central framework only if the initiative-local file is absent (backwards
compatibility with existing initiatives).

The central framework maintains a library of named workflow types:

```
.b2s/
  workflow-types/
    enterprise-modular/
      stage-actions.yaml
      workflow-definition.yaml
      README.md
    fast-path/
      stage-actions.yaml
      workflow-definition.yaml
      README.md
    api-product/
      stage-actions.yaml
      workflow-definition.yaml
      README.md
```

`route-initiative` selects the workflow type based on BRS content and delivery mode.
`init-workspace` accepts a `--workflow-type` argument and copies the files.

## What does NOT change

- One workflow per initiative — no parallel workflows
- The engine logic (next-step, validate-artifact, update-state) is unchanged
- Existing initiatives without a local `.b2s/workflow/` continue to work via fallback
- No versioning or patching of copied workflows — the copy is a snapshot; framework
  updates do not propagate automatically

## Implementation Prompts

| # | Prompt | What it changes |
|---|---|---|
| 01 | Update workspace.py to read workflow from initiative first | `load_stage_actions`, `load_workflow_definition` fallback logic |
| 02 | Create workflow-types library | Copy current workflow as `enterprise-modular`; create `fast-path` variant |
| 03 | Update init-workspace to copy selected workflow | `--workflow-type` arg, copy files, write `workflow-type.json` |
| 04 | Update route-initiative skill to recommend workflow type | Skill outputs workflow type recommendation |
| 05 | Add tests for per-initiative workflow loading | Fixture with local workflow override; assert central is not used |
