from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

REQUIRED = [
    "templates/advanced-governance/security-review.md",
    "templates/advanced-governance/architecture-review.md",
    "templates/advanced-governance/qa-review.md",
    "templates/advanced-governance/test-strategy.md",
    "templates/advanced-governance/bdd-scenarios.md",
    "prompts/4-engineering-readiness/advanced/create-security-review.md",
    "prompts/4-engineering-readiness/advanced/create-architecture-review.md",
    "prompts/4-engineering-readiness/advanced/create-qa-review.md",
    "prompts/4-engineering-readiness/advanced/create-test-strategy.md",
    "prompts/4-engineering-readiness/advanced/create-bdd-scenarios.md",
    "README.md",
    "HOW_TO_USE.md",
    "docs/00-input-preparation.md",
    "docs/01-overview.md",
    "docs/07-architecture-aware-flow.md",
    "prompts/0-input-preparation/01-convert-brs-word-to-markdown.md",
    "prompts/0-input-preparation/02-convert-architecture-word-to-markdown.md",
    "prompts/0-input-preparation/03-normalize-input-package.md",
    "prompts/1-routing/01-select-delivery-mode.md",
    "prompts/2-business-intake/01-create-business-intake-summary.md",
    "prompts/3-planning-and-modular-delivery/02-review-initial-architecture.md",
    "prompts/3-planning-and-modular-delivery/07-create-traceability-matrix.md",
    "prompts/4-engineering-readiness/01-check-engineering-readiness.md",
    "prompts/5-handoff-to-openspec/01-create-openspec-change-for-active-deliverable.md",
    "prompts/6-business-copilot/01-create-brs-business-summary.md",
    "templates/input-preparation/brs.md",
    "templates/input-preparation/initial-architecture.md",
    "templates/planning-and-modular-delivery/initial-architecture-review.md",
    "templates/planning-and-modular-delivery/traceability-matrix.md",
    "schemas/input-package.schema.json",
    "schemas/traceability-matrix.schema.json",
]

missing = [p for p in REQUIRED if not (ROOT / p).exists()]
if missing:
    print("Missing required files:")
    for p in missing:
        print(f" - {p}")
    raise SystemExit(1)

print("Validation passed.")
