#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]

REQUIRED_TOP_LEVEL = [
    "tools/scripts/check_prompt_sequence.py",
    "docs/architecture-alignment-usage.md",
    "templates/quality-gates/enablement-ready-checklist.md",
    "templates/enablement/enablement-scope.md",
    "prompts/08-enablement/07-create-iac-cicd-openspec-tasks.md",
    "prompts/08-enablement/01-identify-enablement-scope.md",
    "docs/enablement-track.md",
    "prompts/01-business-intake/05-create-user-stories.md",
    "docs/business-intake-prompt-sequence.md",
    "docs/architecture-input-guide.md",
    "templates/business-intake/brs-architecture-alignment.md",
    "templates/input/architecture-draft.md",
    "prompts/01-business-intake/03-review-brs-and-requirements-against-architecture.md",
    "prompts/01-business-intake/00b-extract-architecture-from-word.md",
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
    "prompts/01-business-intake/01-summarize-brs.md",
    "prompts/01-business-intake/02-extract-requirements.md",
    "prompts/01-business-intake/04-create-delivery-structure.md",
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
