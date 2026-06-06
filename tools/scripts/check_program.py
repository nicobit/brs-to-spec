#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]

REQUIRED_TOP_LEVEL = [
    "templates/input/brs-original.md",
    "docs/business-intake-step-guide.md",
    "prompts/01-business-intake/00a-extract-brs-from-word.md",
    "docs/change-size-decision-model.md",
    "prompts/00-change-assessment/01-classify-change-size.md",
    "templates/quality-gates/change-size-assessment.md",

    "README.md",
    "docs/workflow.md",
    "docs/pilot-quickstart.md",
    ".github/copilot-instructions.md",
    "prompts/01-business-intake/00-business-brs-summary.md",
    "prompts/01-business-intake/01-extract-business-requirements.md",
    "prompts/01-business-intake/02a-create-epics-and-features.md",
    "templates/business-intake/epics-and-features.md",
    "docs/delivery-hierarchy.md",
    "docs/prompt-execution-environments.md",
    "docs/business-user-guide.md",
    "docs/engineering-user-guide.md",
    "prompts/03-openspec-handoff/03-create-openspec-tasks.md",
]

def main():
    errors = []
    for rel in REQUIRED_TOP_LEVEL:
        if not (ROOT / rel).exists():
            errors.append(f"Missing required file: {rel}")

    if errors:
        print("\n".join(errors))
        sys.exit(1)

    print("Validation passed.")

if __name__ == "__main__":
    main()
