from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

REQUIRED = [
    "README.md",
    "HOW_TO_USE.md",
    "CHANGELOG.md",
    ".github/copilot-instructions.md",
    ".github/prompts/brs-to-spec-run-workflow.prompt.md",
    ".github/prompts/create-engineering-readiness.prompt.md",
    ".github/prompts/create-openspec-handoff.prompt.md",
    ".github/prompts/create-standalone-handoff.prompt.md",
    ".github/prompts/create-gitlab-planning-view.prompt.md",
    ".vscode/settings.json",
    "docs/14-agile-planning-view.md",
    "docs/15-github-copilot-workflow.md",
    "docs/16-prompt-execution-environments.md",
    "docs/17-copilot-usage.md",
    "prompts/0-input-preparation/01-convert-brs-word-to-markdown.md",
    "prompts/0-input-preparation/03-normalize-input-package.md",
    "prompts/2-business-intake/01-create-business-intake-summary.md",
    "prompts/8-copilot-implementation/01-implement-one-task.md",
    "prompts/8-copilot-implementation/02-fix-review-comments.md",
    "prompts/9-reviewers/01-senior-code-review.md",
    "prompts/9-reviewers/02-qa-review.md",
    "prompts/9-reviewers/03-architecture-review.md",
    "prompts/9-reviewers/04-security-review.md",
    "templates/input-preparation/input-package.md",
    "templates/quality-gates/ready-for-copilot-checklist.md",
    "templates/perspectives/agile-planning/gitlab-planning-view.md",
    "tools/scripts/new_initiative.py",
    "tools/scripts/add_brs.py",
    "tools/scripts/add_architecture.py",
    "examples/initiative-workspace-end-to-end/README.md",
]

CONTENT_CHECKS = {
    "README.md": [
        "business-intake/business-intake-summary.md",
        "planning/traceability-matrix.md",
        "initiative workspace",
        "reviewer prompts are downstream helpers",
    ],
    "HOW_TO_USE.md": [
        "python tools/scripts/new_initiative.py onboarding-request --initiative-id I001",
        "python tools/scripts/add_brs.py initiatives/I001-onboarding-request compliance",
        "python tools/scripts/add_architecture.py initiatives/I001-onboarding-request security-constraints",
    ],
    ".github/copilot-instructions.md": [
        "input/brs.md or input/brs/*.md",
        "input/architecture.md or input/architecture/*.md",
        "Operate inside one initiative workspace at a time.",
        "implement one task at a time",
        "planning/delivery-structure.md",
    ],
    "docs/16-prompt-execution-environments.md": [
        "prompts/8-copilot-implementation",
        "VS Code Copilot Agent mode",
        "Work inside one initiative workspace at a time.",
    ],
    "docs/17-copilot-usage.md": [
        "Implement Task 001",
        "review the task",
    ],
    "docs/14-agile-planning-view.md": [
        "All of the paths above are relative to the active initiative workspace.",
        "As a <persona>,",
        "Engineers implement from approved OpenSpec or standalone tasks",
    ],
    ".github/prompts/brs-to-spec-run-workflow.prompt.md": [
        "Active Initiative Workspace",
        "initiative workspace",
    ],
    "prompts/0-input-preparation/01-convert-brs-word-to-markdown.md": [
        "input/brs.md",
        "input/brs/<short-name>.md",
    ],
    "prompts/0-input-preparation/03-normalize-input-package.md": [
        "input/brs.md or input/brs/*.md",
        "input/architecture.md or input/architecture/*.md",
    ],
    "prompts/2-business-intake/01-create-business-intake-summary.md": [
        "input/brs.md or input/brs/*.md",
        "input/architecture.md or input/architecture/*.md",
    ],
    "prompts/8-copilot-implementation/01-implement-one-task.md": [
        "openspec/changes/D1-<deliverable-name>/tasks.md",
        "standalone-delivery/D1-<deliverable-name>/tasks.md",
    ],
    "prompts/9-reviewers/01-senior-code-review.md": [
        "Finding ID",
        "Required before",
    ],
    "templates/perspectives/agile-planning/gitlab-planning-view.md": [
        "Engineering Notes",
        "Enablement Needs",
        "Engineering Consumption Model",
        "Acceptance Source Notes",
        "Stale View Handling",
        "Engineers use OpenSpec or standalone tasks for implementation.",
    ],
    ".github/prompts/create-gitlab-planning-view.prompt.md": [
        "User stories are business context and traceability only.",
        "Implementation must come from approved OpenSpec or standalone tasks.",
    ],
    ".github/prompts/brs-to-spec-run-workflow.prompt.md": [
        "Do not treat user stories as the engineering implementation contract.",
        "Recommend implementation only from approved OpenSpec or standalone tasks.",
    ],
    "README.md": [
        "single team-facing Delivery Planning View",
        "OpenSpec or standalone tasks remain the engineering implementation contract.",
    ],
    "HOW_TO_USE.md": [
        "Do not implement from user stories alone.",
        "Use one approved OpenSpec or standalone task as the implementation unit.",
    ],
    "prompts/7-perspectives/agile-planning/01-create-gitlab-planning-view.md": [
        "user stories are business context, not engineering contract",
        "Enablement Needs only when relevant",
    ],
}


def main() -> None:
    missing = [path for path in REQUIRED if not (ROOT / path).exists()]
    if missing:
        print("Missing required files:")
        for path in missing:
            print(f" - {path}")
        raise SystemExit(1)

    for path, terms in CONTENT_CHECKS.items():
        text = (ROOT / path).read_text(encoding="utf-8", errors="ignore")
        for term in terms:
            if term not in text:
                print(f"Content check failed: {path} missing {term!r}")
                raise SystemExit(1)

    print("Validation passed.")


if __name__ == "__main__":
    main()
