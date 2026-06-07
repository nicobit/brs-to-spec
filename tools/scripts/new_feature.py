from pathlib import Path
import argparse

def write_if_missing(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(content.strip() + "\n", encoding="utf-8")

def main():
    parser = argparse.ArgumentParser(description="Create a new BRS-to-OpenSpec workspace.")
    parser.add_argument("name", help="Initiative or feature name")
    parser.add_argument("--mode", choices=["standard", "enterprise", "enterprise-modular"], default="standard")
    args = parser.parse_args()

    root = Path(args.name)

    write_if_missing(root / "input" / "brs.md", "# BRS\n")
    write_if_missing(root / "input" / "initial-architecture.md", "# Initial Architecture\n\nNo initial architecture document provided.\n")
    write_if_missing(root / "input" / "input-package.md", "# Input Package\n")
    write_if_missing(root / "routing" / "delivery-mode-decision.md", "# Delivery Mode Decision\n")
    write_if_missing(root / "business-intake" / "business-intake-summary.md", "# Business Intake Summary\n")

    if args.mode in ["enterprise", "enterprise-modular"]:
        write_if_missing(root / "planning" / "delivery-structure.md", "# Delivery Structure\n")
        write_if_missing(root / "architecture" / "initial-architecture-review.md", "# Initial Architecture Review\n")
        write_if_missing(root / "architecture" / "global-architecture-rules.md", "# Global Architecture Rules\n")
        write_if_missing(root / "engineering-readiness" / "readiness-check.md", "# Engineering Readiness Check\n")

    if args.mode == "enterprise-modular":
        write_if_missing(root / "modules" / "software-modules.md", "# Software Modules\n")
        write_if_missing(root / "planning" / "capability-module-map.md", "# Capability to Module Map\n")
        write_if_missing(root / "planning" / "delivery-increments.md", "# Delivery Increments\n")
        write_if_missing(root / "planning" / "traceability-matrix.md", "# Traceability Matrix\n")

    write_if_missing(root / "openspec" / "changes" / "D1-active-deliverable" / "proposal.md", "# Proposal\n")
    write_if_missing(root / "openspec" / "changes" / "D1-active-deliverable" / "design.md", "# Design\n")
    write_if_missing(root / "openspec" / "changes" / "D1-active-deliverable" / "tasks.md", "# Tasks\n")

    print(f"Created workspace: {root}")

if __name__ == "__main__":
    main()
