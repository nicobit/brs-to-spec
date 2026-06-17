"""Initiative workspace initializer for the staged `.b2s` engine."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from b2s_engine import workspace


_BRS_TEMPLATE = """\
# Business Requirements Specification — {initiative_id}

## Metadata

| Field | Value |
|---|---|
| Initiative ID | {initiative_id} |
| Created at | {date} |
| Status | Draft |

## Objectives

| OBJ-NNN | Objective | Success Measure |
|---|---|---|
| OBJ-001 | | |

## Functional Requirements

| FR-NNN | Requirement | Business Value | Priority |
|---|---|---|---|
| FR-001 | | | |

## Non-Functional Requirements

| NFR-NNN | Requirement | Category | Measure |
|---|---|---|---|
| NFR-001 | | | |

## Constraints

| C-NNN | Constraint | Category | Source |
|---|---|---|---|
| C-001 | | | |

## Open Questions

| OQ-NNN | Question | Impact | Owner |
|---|---|---|---|
| OQ-001 | | | |
"""


def run(args: object) -> None:
    initiative_id = getattr(args, "initiative_id", None)
    workspace_root_arg = getattr(args, "workspace_root", None)

    # Derive workspace root from initiative_id if not explicitly passed
    if workspace_root_arg is not None:
        workspace_root = workspace_root_arg.resolve()
    elif initiative_id is not None:
        initiatives_dir = workspace.FRAMEWORK_ROOT.parent / "initiatives"
        workspace_root = initiatives_dir / initiative_id
    else:
        raise ValueError("Provide --initiative-id or --workspace-root.")

    if workspace_root.exists():
        raise FileExistsError(
            f"Workspace already exists: {workspace_root}\n"
            "Use reset-to-phase to restart an existing initiative."
        )

    # Infer initiative_id from the folder name if only workspace_root was given
    if initiative_id is None:
        initiative_id = workspace_root.name

    today = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")

    # --- Create folder structure ---
    input_dir = workspace_root / "input"
    input_dir.mkdir(parents=True)

    # --- Seed input/brs.md ---
    brs_path = input_dir / "brs.md"
    brs_path.write_text(
        _BRS_TEMPLATE.format(initiative_id=initiative_id, date=today),
        encoding="utf-8",
    )

    # --- Seed .b2s runtime layout (state + tmp) ---
    workspace.ensure_runtime_layout(workspace_root)

    # --- Write initiative_id into workflow-state.json ---
    state = workspace.load_state(workspace_root)
    state["initiative_id"] = initiative_id
    state["state_validated"] = True
    state["last_updated"] = datetime.now(tz=timezone.utc).isoformat()
    workspace.save_state(workspace_root, state)

    # --- Report ---
    result = {
        "overall": "pass",
        "initiative_id": initiative_id,
        "workspace_root": str(workspace_root),
        "created": [
            str(brs_path.relative_to(workspace_root)),
            ".b2s/state/workflow-state.json",
            ".b2s/state/open-decisions.md",
        ],
        "next_action": "route-initiative",
        "message": (
            f"Initiative {initiative_id} workspace created. "
            f"Fill in {brs_path.relative_to(workspace_root)} then run the workflow."
        ),
    }

    output_path = workspace_root / ".b2s" / "tmp" / "init-workspace.json"
    if getattr(args, "output", None) is not None:
        output_arg = args.output
        output_path = (
            output_arg.resolve()
            if output_arg.is_absolute()
            else (workspace_root / output_arg).resolve()
        )

    workspace.save_json_file(output_path, result)
    workspace.append_execution_log(
        workspace_root,
        command="init-workspace",
        overall=result["overall"],
        details={
            "created": result["created"],
            "message": result["message"],
        },
    )
    print(json.dumps(result, indent=2))
