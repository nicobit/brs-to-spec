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
    "prompts/0-input-preparation/01-convert-brs-word-to-markdown.md",
    "prompts/0-input-preparation/03-normalize-input-package.md",
    "prompts/2-business-intake/01-create-business-intake-summary.md",
    "templates/input-preparation/input-package.md",
    "tools/scripts/new_feature.py",
    "tools/scripts/add_brs.py",
    "tools/scripts/add_architecture.py",
]

CONTENT_CHECKS = {
    "README.md": [
        "business-intake/business-intake-summary.md",
        "planning/traceability-matrix.md",
        "feature workspace",
    ],
    "HOW_TO_USE.md": [
        "python tools/scripts/new_feature.py onboarding-request --feature-id F001",
        "python tools/scripts/add_brs.py features/F001-onboarding-request compliance",
        "python tools/scripts/add_architecture.py features/F001-onboarding-request security-constraints",
    ],
    ".github/copilot-instructions.md": [
        "input/brs.md or input/brs/*.md",
        "input/architecture.md or input/architecture/*.md",
        "Operate inside one feature workspace at a time.",
    ],
    ".github/prompts/brs-to-spec-run-workflow.prompt.md": [
        "Active Feature Workspace",
        "feature workspace",
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
