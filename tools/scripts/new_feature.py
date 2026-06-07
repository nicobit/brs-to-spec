from pathlib import Path
import argparse

def write_if_missing(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(content.strip() + "\n", encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser(description="Create a new BRS-to-delivery workspace.")
    parser.add_argument("name")
    parser.add_argument("--mode", choices=["fast", "standard", "enterprise", "enterprise-modular"], default="standard")
    parser.add_argument("--execution-mode", choices=["openspec", "standalone", "business-copilot"], default="openspec")
    args = parser.parse_args()

    root = Path(args.name)

    write_if_missing(root / "input" / "brs.md", "# BRS\n")
    write_if_missing(root / "input" / "initial-architecture.md", "# Initial Architecture\n\nNo initial architecture document provided.\n")
    write_if_missing(root / "input" / "input-package.md", "# Input Package\n")
    write_if_missing(root / "routing" / "delivery-and-execution-mode-decision.md", "# Delivery and Execution Mode Decision\n")

    if args.mode != "fast":
        write_if_missing(root / "business-intake" / "business-intake-summary.md", "# Business Intake Summary\n")
        write_if_missing(root / "engineering-readiness" / "readiness-check.md", "# Engineering Readiness Check\n")

    if args.mode in ["enterprise", "enterprise-modular"]:
        write_if_missing(root / "planning" / "delivery-structure.md", "# Delivery Structure\n")
        write_if_missing(root / "architecture" / "initial-architecture-review.md", "# Initial Architecture Review\n")
        write_if_missing(root / "architecture" / "global-architecture-rules.md", "# Global Architecture Rules\n")
        write_if_missing(root / "planning" / "traceability-matrix.md", "# Traceability Matrix\n")

    if args.mode == "enterprise-modular":
        write_if_missing(root / "modules" / "software-modules.md", "# Software Modules\n")
        write_if_missing(root / "planning" / "capability-module-map.md", "# Capability to Module Map\n")
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
        write_if_missing(root / "business-copilot" / "sharepoint-output-index.md", "# Business Copilot Output Index\n")

    write_if_missing(root / "quality-gates" / ".gitkeep", "")

    print(f"Created workspace: {root}")
    print(f"Delivery mode: {args.mode}")
    print(f"Execution mode: {args.execution_mode}")

if __name__ == "__main__":
    main()
