from pathlib import Path
import argparse
import json
import re
from datetime import date


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value or "initiative"


def write_if_missing(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(content.strip() + "\n", encoding="utf-8")


def build_workspace_name(initiative_id: str | None, name: str) -> str:
    slug = slugify(name)
    if initiative_id:
        return f"{initiative_id}-{slug}"
    return slug


def create_v2_workspace(root: Path, workspace_name: str, args) -> None:
    """Create a v2 initiative workspace with .flow/ event queue scaffolding."""

    today = date.today().isoformat()

    # Standard input files (same as v1)
    write_if_missing(
        root / "input" / "brs.md",
        """
# BRS

## Source Metadata

| Field | Value |
|---|---|
| Source name |  |
| Source version/date |  |
| Extracted by |  |
| Extraction date |  |

## Executive Summary
        """,
    )
    write_if_missing(
        root / "input" / "architecture.md",
        """
# Architecture

No architecture document provided.
        """,
    )
    write_if_missing(
        root / "input" / "input-package.md",
        """
# Input Package

## Initiative Workspace

## Input Inventory

## Consolidation Notes

## Known Limitations

## Assumptions
        """,
    )

    # .flow/ event queue folders
    for subfolder in ["pending", "processing", "done", "failed"]:
        (root / ".flow" / "events" / subfolder).mkdir(parents=True, exist_ok=True)

    # .flow/state/
    state_dir = root / ".flow" / "state"
    state_dir.mkdir(parents=True, exist_ok=True)

    # workflow-state.json
    workflow_state = {
        "initiative_id": workspace_name,
        "created": today,
        "current_stage": "0-routing",
        "delivery_mode": args.delivery_mode,
        "execution_mode": args.execution_mode,
        "project_type": args.project_type,
        "readiness_score": None,
        "quality_gates_triggered": [],
        "optional_artifacts_requested": [],
        "artifact_status": {},
        "event_counter": 1,
        "active_events": ["EVT-00001"],
        "failed_events": [],
        "last_completed_event": None,
        "open_decisions": 0,
        "blocking_decisions": 0,
        "last_updated": today,
    }
    state_path = state_dir / "workflow-state.json"
    if not state_path.exists():
        state_path.write_text(
            json.dumps(workflow_state, indent=2) + "\n", encoding="utf-8"
        )

    # event-log.jsonl — empty but present
    write_if_missing(state_dir / "event-log.jsonl", "")

    # open-decisions.md
    write_if_missing(
        state_dir / "open-decisions.md",
        f"""# Open Decisions — {workspace_name}

| ID | Question | Raised by | Status | Resolution |
|---|---|---|---|---|
""",
    )

    # Initial routing event in pending/ — must be a runtime event, not a template
    event_file = root / ".flow" / "events" / "pending" / "EVT-00001-route-initiative.yaml"
    if not event_file.exists():
        event_content = f"""\
event_id: EVT-00001
event_type: ROUTE_INITIATIVE
action: route_initiative
persona: orchestrator
stage: "0-routing"
priority: critical
status: pending

task:
  title: "Route initiative — select delivery mode and execution mode"
  objective: >
    Analyse the BRS input and available context to select the delivery mode
    (OpenSpec, Standalone, FastPath, or BusinessCopilot) and execution mode
    (Enterprise, Enterprise+Modular, or Standard) for this initiative.
    Produce routing/routing-decision.md. All subsequent events read this artifact
    to understand scope and expected output shape.

skill_ref: ".brs2spec2/skills/orchestrator/route-initiative.md"
persona_ref: ".brs2spec2/personas/orchestrator.md"
artifact_template_ref: ".brs2spec2/artifact-templates/routing-decision.md"

read_from:
  - "input/brs.md"
  - "input/brs/*.md"
  - "input/architecture.md"
  - "input/architecture/*.md"
  - "input/input-package.md"

required_inputs:
  - "input/brs.md"

optional_inputs:
  - "input/brs/*.md"
  - "input/architecture.md"
  - "input/architecture/*.md"
  - "input/input-package.md"

write_to:
  - "routing/routing-decision.md"

blocked_by: []

on_success:
  create_events:
    - template: "EVT-TPL-002"
      reason: "Routing complete — begin business intake"
  update_state:
    current_stage: "0-routing"
    delivery_mode: "{{from routing-decision.md}}"
    execution_mode: "{{from routing-decision.md}}"

on_failure:
  raise_decision:
    question: >
      Routing failed — delivery mode or execution mode could not be determined.
      A human must review the BRS source and either provide a cleaner input or
      override the routing decision manually.
    owner: human
    blocking: true

meta:
  template_id: EVT-TPL-001
  created_by: orchestrator
  created_at: {today}
  notes: "Auto-created by new_initiative.py --v2 on initiative init"
"""
        event_file.parent.mkdir(parents=True, exist_ok=True)
        event_file.write_text(event_content, encoding="utf-8")

    # README
    write_if_missing(
        root / "README.md",
        f"""# {workspace_name}

v2 initiative workspace. Uses the flow-engine event queue.

**To run:** say `dispatch-next` or `dispatch-all` in Claude Code.

Inputs:
- `input/brs.md`
- `input/architecture.md`
- `input/input-package.md`

State: `.flow/state/workflow-state.json`
Queue: `.flow/events/pending/`
""",
    )

    print(f"Created v2 workspace: {root}")
    print(f"  Event queue: {root / '.flow' / 'events' / 'pending'}")
    print(f"  First event: EVT-00001-route-initiative.yaml")
    print(f"  State: {state_dir / 'workflow-state.json'}")
    print(f"  Say 'dispatch-next' to begin.")


def create_v1_workspace(root: Path, workspace_name: str, args) -> None:
    """Create a v1 initiative workspace (legacy, no .flow/ folder)."""

    write_if_missing(
        root / "README.md",
        f"""# {workspace_name}

This initiative workspace holds all inputs and outputs for one delivery initiative.

Default inputs:
- `input/brs.md`
- `input/architecture.md`
- `input/input-package.md`

Expand to `input/brs/` or `input/architecture/` only when the same initiative has multiple source documents.
Treat every other path in this workspace as relative to this initiative root.
""",
    )
    write_if_missing(
        root / "input" / "brs.md",
        """
# BRS

## Source Metadata

| Field | Value |
|---|---|
| Source name |  |
| Source version/date |  |
| Extracted by |  |
| Extraction date |  |

## Executive Summary
        """,
    )
    write_if_missing(
        root / "input" / "architecture.md",
        """
# Architecture

No architecture document provided.
        """,
    )
    write_if_missing(
        root / "input" / "input-package.md",
        """
# Input Package

## Initiative Workspace

## Input Inventory

## Consolidation Notes

## Known Limitations

## Assumptions
        """,
    )
    write_if_missing(root / "routing" / "routing-decision.md", "# Routing Decision\n")

    if args.mode != "fast":
        write_if_missing(
            root / "business-intake" / "business-intake-summary.md",
            "# Business Intake Summary\n",
        )
        write_if_missing(
            root / "engineering-readiness" / "readiness-check.md",
            "# Engineering Readiness Check\n",
        )

    if args.mode in ["enterprise", "enterprise-modular"]:
        write_if_missing(root / "planning" / "delivery-structure.md", "# Delivery Structure\n")
        write_if_missing(
            root / "architecture" / "architecture-review.md",
            "# Architecture Review\n",
        )
        write_if_missing(
            root / "architecture" / "architecture-rules.md",
            "# Architecture Rules\n",
        )
        write_if_missing(root / "planning" / "traceability-matrix.md", "# Traceability Matrix\n")

    if args.mode == "enterprise-modular":
        write_if_missing(root / "modules" / "software-modules.md", "# Software Modules\n")
        write_if_missing(
            root / "planning" / "capability-module-map.md",
            "# Capability to Module Map\n",
        )
        write_if_missing(root / "planning" / "delivery-increments.md", "# Delivery Increments\n")

    if args.execution_mode == "openspec":
        base = root / "openspec" / "changes" / "D1-active-deliverable"
        write_if_missing(base / "story.md", "# Story\n")
        write_if_missing(base / "design.md", "# Design\n")
        write_if_missing(base / "tasks.md", "# Tasks\n")
    elif args.execution_mode == "standalone":
        base = root / "standalone-delivery" / "D1-active-deliverable"
        write_if_missing(base / "delivery-spec.md", "# Delivery Spec\n")
        write_if_missing(base / "implementation-plan.md", "# Implementation Plan\n")
        write_if_missing(base / "tasks.md", "# Tasks\n")
        write_if_missing(base / "validation-plan.md", "# Validation Plan\n")
        write_if_missing(base / "review-checklist.md", "# Review Checklist\n")
    else:
        write_if_missing(
            root / "business-copilot" / "sharepoint-output-index.md",
            "# Business Copilot Output Index\n",
        )

    write_if_missing(root / "quality-gates" / ".gitkeep", "")
    write_if_missing(root / "perspectives" / "agile-planning" / ".gitkeep", "")
    write_if_missing(root / "reviews" / "implementation" / ".gitkeep", "")

    print(f"Created v1 workspace: {root}")
    print(f"Initiative workspace: {workspace_name}")
    print(f"Initial BRS file: {root / 'input' / 'brs.md'}")
    print(f"Delivery mode: {args.mode}")
    print(f"Execution mode: {args.execution_mode}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a new initiative-scoped BRS-to-delivery workspace."
    )
    parser.add_argument("name", help="Initiative name or slug.")
    parser.add_argument(
        "--initiative-id",
        dest="initiative_id",
        help="Optional initiative identifier such as I001.",
    )
    parser.add_argument(
        "--v2",
        action="store_true",
        default=False,
        help="Create a v2 initiative workspace with .flow/ event queue (brs-to-spec v2).",
    )

    # v1 arguments
    parser.add_argument(
        "--mode",
        choices=["fast", "standard", "enterprise", "enterprise-modular"],
        default="standard",
        help="(v1 only) Delivery mode.",
    )
    parser.add_argument(
        "--execution-mode",
        dest="execution_mode",
        choices=["openspec", "standalone", "business-copilot"],
        default="openspec",
        help="(v1 only) Execution mode.",
    )

    # v2 arguments
    parser.add_argument(
        "--delivery-mode",
        dest="delivery_mode",
        choices=["FastPath", "Standard", "Enterprise", "Enterprise+Modular"],
        default="Standard",
        help="(v2 only) Delivery mode written into workflow-state.json.",
    )
    parser.add_argument(
        "--v2-execution-mode",
        dest="v2_execution_mode",
        choices=["OpenSpec", "Standalone", "FastPath"],
        default="OpenSpec",
        help="(v2 only) Execution mode written into workflow-state.json.",
    )
    parser.add_argument(
        "--project-type",
        dest="project_type",
        choices=["greenfield", "brownfield"],
        default="greenfield",
        help="(v2 only) Project type written into workflow-state.json.",
    )

    parser.add_argument(
        "--root",
        default="initiatives",
        help="Workspace parent directory. Defaults to initiatives.",
    )
    args = parser.parse_args()

    workspace_name = build_workspace_name(args.initiative_id, args.name)
    root = Path(args.root) / workspace_name

    if args.v2:
        # Normalise v2 execution_mode onto args for create_v2_workspace
        args.execution_mode = args.v2_execution_mode
        create_v2_workspace(root, workspace_name, args)
    else:
        create_v1_workspace(root, workspace_name, args)


if __name__ == "__main__":
    main()
