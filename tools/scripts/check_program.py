from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

QUALITY_GATES = [
    "bdd-scenarios",
    "test-strategy",
    "qa-review",
    "architecture-review",
    "security-review",
    "release-readiness-review",
    "api-contract",
    "data-contract",
    "event-contract",
    "threat-model",
    "observability-plan",
]

REQUIRED = [
    # top-level docs
    "README.md",
    "HOW_TO_USE.md",
    "docs/00-input-preparation.md",
    "docs/01-overview.md",
    "docs/02-delivery-modes.md",
    "docs/05-handoff.md",
    "docs/06-conditional-quality-gates.md",
    "docs/07-architecture-aware-flow.md",
    "docs/08-execution-modes.md",
    "docs/09-migration-0.0.7-to-0.0.8.md",
    # input preparation prompts
    "prompts/0-input-preparation/01-convert-brs-word-to-markdown.md",
    "prompts/0-input-preparation/02-convert-architecture-word-to-markdown.md",
    "prompts/0-input-preparation/03-normalize-input-package.md",
    # routing
    "prompts/1-routing/01-select-delivery-mode.md",
    # business intake
    "prompts/2-business-intake/01-create-business-intake-summary.md",
    # planning: architecture review + traceability matrix prompts
    "prompts/3-planning-and-modular-delivery/02-review-initial-architecture.md",
    "prompts/3-planning-and-modular-delivery/07-create-traceability-matrix.md",
    # engineering readiness + conditional quality gates
    "prompts/4-engineering-readiness/01-check-engineering-readiness.md",
    "prompts/4-engineering-readiness/02-identify-required-quality-gates.md",
    # OpenSpec handoff prompt + standalone handoff prompt
    "prompts/5-handoff/01-create-openspec-change-for-active-deliverable.md",
    "prompts/5-handoff/03-create-standalone-delivery-package.md",
    # business Copilot prompt
    "prompts/6-business-copilot/01-create-brs-business-summary.md",
    # key templates
    "templates/input-preparation/brs.md",
    "templates/input-preparation/initial-architecture.md",
    "templates/planning-and-modular-delivery/initial-architecture-review.md",
    "templates/planning-and-modular-delivery/traceability-matrix.md",
    "templates/engineering-readiness/readiness-check.md",
    "templates/openspec-handoff/proposal.md",
    "templates/openspec-handoff/design.md",
    "templates/openspec-handoff/tasks.md",
    "templates/standalone-delivery/delivery-spec.md",
    "templates/standalone-delivery/implementation-plan.md",
    "templates/standalone-delivery/tasks.md",
    "templates/standalone-delivery/validation-plan.md",
    "templates/standalone-delivery/review-checklist.md",
    # schemas
    "schemas/input-package.schema.json",
    "schemas/traceability-matrix.schema.json",
]

# conditional quality gate prompts + templates (the full set must exist)
for gate in QUALITY_GATES:
    REQUIRED.append(f"prompts/4-engineering-readiness/quality-gates/create-{gate}.md")
    REQUIRED.append(f"templates/quality-gates/{gate}.md")

missing = [p for p in REQUIRED if not (ROOT / p).exists()]
if missing:
    print("Missing required files:")
    for p in missing:
        print(f" - {p}")
    raise SystemExit(1)

print("Validation passed.")
