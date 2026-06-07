from pathlib import Path
import argparse


def write_if_missing(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(content.strip() + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(
        description="Create a new BRS-to-delivery workspace."
    )
    parser.add_argument("name", help="Initiative or feature name")
    parser.add_argument(
        "--mode",
        choices=["fast", "standard", "enterprise", "enterprise-modular"],
        default="standard",
        help="Delivery mode (how much ceremony the change needs).",
    )
    parser.add_argument(
        "--execution-mode",
        choices=["openspec", "standalone"],
        default="openspec",
        help="Execution mode (which downstream builds the deliverable).",
    )
    args = parser.parse_args()

    root = Path(args.name)
    deliverable = "D1-active-deliverable"

    # Inputs are always created (normalized inputs are official in every mode).
    write_if_missing(root / "input" / "brs.md", "# BRS\n")
    write_if_missing(
        root / "input" / "initial-architecture.md",
        "# Initial Architecture\n\nNo initial architecture document provided.\n",
    )
    write_if_missing(root / "input" / "input-package.md", "# Input Package\n")

    # Routing records both delivery mode and execution mode.
    write_if_missing(
        root / "routing" / "delivery-mode-decision.md",
        "# Delivery Mode Decision\n\n"
        f"## Recommended Delivery Mode\n{args.mode}\n\n"
        f"## Recommended Execution Mode\n{args.execution_mode}\n",
    )

    # Fast Path skips business intake; every other mode reviews the summary.
    if args.mode != "fast":
        write_if_missing(
            root / "business-intake" / "business-intake-summary.md",
            "# Business Intake Summary\n",
        )

    if args.mode in ["enterprise", "enterprise-modular"]:
        write_if_missing(
            root / "planning" / "delivery-structure.md", "# Delivery Structure\n"
        )
        write_if_missing(
            root / "architecture" / "initial-architecture-review.md",
            "# Initial Architecture Review\n",
        )
        write_if_missing(
            root / "architecture" / "global-architecture-rules.md",
            "# Global Architecture Rules\n",
        )
        write_if_missing(
            root / "engineering-readiness" / "readiness-check.md",
            "# Engineering Readiness Check\n",
        )

    if args.mode == "enterprise-modular":
        write_if_missing(
            root / "modules" / "software-modules.md", "# Software Modules\n"
        )
        write_if_missing(
            root / "planning" / "capability-module-map.md",
            "# Capability to Module Map\n",
        )
        write_if_missing(
            root / "planning" / "delivery-increments.md", "# Delivery Increments\n"
        )
        write_if_missing(
            root / "planning" / "traceability-matrix.md", "# Traceability Matrix\n"
        )

    # Execution-mode-specific output tree.
    if args.execution_mode == "openspec":
        base = root / "openspec" / "changes" / deliverable
        write_if_missing(base / "proposal.md", "# Proposal\n")
        write_if_missing(base / "design.md", "# Design\n")
        write_if_missing(base / "tasks.md", "# Tasks\n")
    else:  # standalone
        base = root / "standalone-delivery" / deliverable
        write_if_missing(base / "delivery-spec.md", "# Delivery Spec\n")
        write_if_missing(base / "implementation-plan.md", "# Implementation Plan\n")
        write_if_missing(base / "tasks.md", "# Tasks\n")
        write_if_missing(base / "validation-plan.md", "# Validation Plan\n")
        write_if_missing(base / "review-checklist.md", "# Review Checklist\n")

    print(
        f"Created workspace: {root} "
        f"(mode={args.mode}, execution-mode={args.execution_mode})"
    )


if __name__ == "__main__":
    main()
