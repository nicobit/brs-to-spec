#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]

REQUIRED_TOP_LEVEL = [
    "schemas/business-copilot-intake.schema.json",
    "templates/business-copilot-intake/business-requirements-table.md",
    "prompts/12-business-copilot-intake/08-create-business-approval-checklist.md",
    "prompts/12-business-copilot-intake/01-create-brs-business-summary.md",
    "docs/copilot/copilot-studio-agent-design.md",
    "docs/copilot/how-to-create-m365-copilot-agent.md",
    "docs/copilot/how-to-run-business-intake-in-m365-copilot.md",
    "docs/business-copilot-intake.md",
    "schemas/next-increment-scope.schema.json",
    "schemas/delivery-slicing.schema.json",
    "templates/planning/increment-handoff.md",
    "templates/planning/next-increment-scope.md",
    "templates/planning/delivery-slicing.md",
    "prompts/06-planning/03-create-increment-handoff.md",
    "prompts/06-planning/02-select-next-increment-scope.md",
    "prompts/06-planning/01-create-delivery-slicing-and-roadmap.md",
    "docs/large-feature-planning.md",
    "templates/downstream-adapters/gstack/gstack-review-plan.md",
    "templates/downstream-adapters/gstack/gstack-brief.md",
    "prompts/11-downstream-adapters/gstack/02-create-gstack-review-plan.md",
    "prompts/11-downstream-adapters/gstack/01-create-gstack-brief-from-handoff.md",
    "docs/gstack-adapter.md",
    "schemas/spec-driven-handoff.schema.json",
    "templates/quality-gates/handoff-ready-checklist.md",
    "templates/handoff/spec-driven-handoff.md",
    "prompts/11-downstream-adapters/kiro/01-create-kiro-spec-input-from-handoff.md",
    "prompts/11-downstream-adapters/spec-kit/01-create-speckit-input-from-handoff.md",
    "prompts/11-downstream-adapters/openspec/01-create-openspec-from-handoff.md",
    "prompts/10-handoff/02-assess-handoff-readiness.md",
    "prompts/10-handoff/01-create-spec-driven-handoff.md",
    "docs/downstream-framework-selection.md",
    "docs/framework-boundary-and-handoff.md",
    "schemas/architecture-contract-artifact-decision.schema.json",
    "templates/quality-gates/architecture-contracts-ready-checklist.md",
    "templates/architecture-contracts/openapi.yaml",
    "templates/architecture-contracts/api-contract.md",
    "templates/architecture-contracts/artifact-decision.md",
    "prompts/09-architecture-contracts/09-update-openspec-from-architecture-contracts.md",
    "prompts/09-architecture-contracts/00-decide-architecture-contract-artifacts.md",
    "docs/architecture-contract-extensions.md",
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
