from pathlib import Path
import argparse
import re


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value or "feature"


def write_if_missing(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(content.strip() + "\n", encoding="utf-8")


def build_workspace_name(feature_id: str | None, name: str) -> str:
    slug = slugify(name)
    if feature_id:
        return f"{feature_id}-{slug}"
    return slug


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a new feature-scoped BRS-to-delivery workspace."
    )
    parser.add_argument("name", help="Feature name or slug.")
    parser.add_argument("--feature-id", help="Optional feature identifier such as F001.")
    parser.add_argument(
        "--mode",
        choices=["fast", "standard", "enterprise", "enterprise-modular"],
        default="standard",
    )
    parser.add_argument(
        "--execution-mode",
        choices=["openspec", "standalone", "business-copilot"],
        default="openspec",
    )
    parser.add_argument(
        "--root",
        default="features",
        help="Workspace parent directory. Defaults to features.",
    )
    args = parser.parse_args()

    workspace_name = build_workspace_name(args.feature_id, args.name)
    root = Path(args.root) / workspace_name

    write_if_missing(
        root / "README.md",
        f"""
        # {workspace_name}

        This feature workspace holds all inputs and outputs for one delivery initiative.

        Default inputs:
        - `input/brs.md`
        - `input/architecture.md`
        - `input/input-package.md`

        Expand to `input/brs/` or `input/architecture/` only when the same initiative has multiple source documents.
        Treat every other path in this workspace as relative to this feature root.
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

        ## Feature Workspace

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
        write_if_missing(base / "proposal.md", "# Proposal\n")
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

    print(f"Created workspace: {root}")
    print(f"Feature workspace: {workspace_name}")
    print(f"Initial BRS file: {root / 'input' / 'brs.md'}")
    print(f"Initial architecture file: {root / 'input' / 'architecture.md'}")
    print(f"Delivery mode: {args.mode}")
    print(f"Execution mode: {args.execution_mode}")


if __name__ == "__main__":
    main()
