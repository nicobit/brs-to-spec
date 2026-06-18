# Prompt 04 — Update route-initiative Skill to Recommend Workflow Type

## Context

You are working on the `.b2s` framework at the root of this repository.

`init-workspace` now copies a workflow type into the initiative (prompt 03).
But today the workflow type is always `enterprise-modular` by default — the user
must know to pass `--workflow-type fast-path` manually.

`route-initiative` is the first action in every workflow. It reads the BRS and
determines delivery mode and execution mode. It is the natural place to also
recommend which workflow type the initiative should use — so the human or AI
can re-initialise with the right type if the wrong one was chosen.

Read these files in full before making changes:
- `.b2s/skills/orchestrator/route-initiative.md`
- `.b2s/artifact-templates/routing-decision.md`
- `.b2s/workflow-types/index.yaml`

---

## Step 1 — Update routing-decision.md artifact template

Read `.b2s/artifact-templates/routing-decision.md` in full.

Add a new section after the existing Delivery Mode and Execution Mode sections:

```markdown
## Workflow Type

| Field | Value |
|---|---|
| Recommended workflow type | {{enterprise-modular / fast-path}} |
| Rationale | {{one sentence}} |
| Current workflow type | {{read from .b2s/workflow/workflow-type.json}} |
| Match | {{yes / no — yes if recommended == current}} |

### Workflow Type Mismatch Warning

If `Match` is `no`, include this block:

> **Warning:** The initiative was initialised with workflow type `{{current}}` but
> this BRS analysis recommends `{{recommended}}`. To switch workflow type, delete
> this initiative workspace and re-run:
> ```
> python .b2s/scripts/b2s_cli.py init-workspace \
>   --initiative-id {{initiative_id}} \
>   --workflow-type {{recommended}}
> ```
> If you want to continue with the current workflow type, ignore this warning.
```

---

## Step 2 — Update route-initiative skill

Read `.b2s/skills/orchestrator/route-initiative.md` in full.

Add a new step after the existing delivery mode and execution mode determination:

```
## Step N — Recommend workflow type

Read `.b2s/workflow-types/index.yaml` to understand available workflow types.
Read `.b2s/workflow/workflow-type.json` from the initiative workspace to find
the currently active workflow type.

Recommend a workflow type based on these rules:

- Recommend `fast-path` if ALL of the following are true:
  - The BRS has fewer than 10 functional requirements
  - No external integrations are mentioned
  - No regulatory or compliance requirements are present
  - No mention of multiple teams or parallel streams

- Recommend `enterprise-modular` in all other cases.

Write the recommendation and match status into the routing-decision.md output.
If the recommended type does not match the current type, include the mismatch
warning block from the template.
```

---

## Step 3 — Update state.py to parse workflow type recommendation

In `state.py`, `_parse_routing_fields`, add parsing for the workflow type
recommendation from `routing/routing-decision.md`:

```python
workflow_type_recommended = _markdown_row_value(text, "Recommended workflow type")
if workflow_type_recommended in {"enterprise-modular", "fast-path"}:
    state["workflow_type_recommended"] = workflow_type_recommended
```

Add `"workflow_type_recommended": null` to the workflow-state.json template.

This allows future tooling to detect mismatches programmatically.

---

## Step 4 — Update dispatch-next output for mismatch

In `dispatch.py`, `build_plan`, after loading state, check for workflow type mismatch:

```python
current_type = current_state.get("workflow_type")
recommended_type = current_state.get("workflow_type_recommended")
if current_type and recommended_type and current_type != recommended_type:
    plan["workflow_type_warning"] = (
        f"Workflow type mismatch: running '{current_type}' "
        f"but route-initiative recommends '{recommended_type}'. "
        f"Re-initialise with --workflow-type {recommended_type} to switch."
    )
```

Print the warning in human-readable output if present.

---

## Done criteria

- [ ] `routing-decision.md` template has Workflow Type section with mismatch warning block
- [ ] `route-initiative` skill recommends workflow type using the documented rules
- [ ] `route-initiative` skill reads current type from `workflow-type.json` and computes match
- [ ] `state.py` parses `workflow_type_recommended` from routing decision
- [ ] `workflow-state.json` template has `workflow_type_recommended: null`
- [ ] `dispatch-next` prints workflow type warning when mismatch detected
- [ ] All existing tests pass
