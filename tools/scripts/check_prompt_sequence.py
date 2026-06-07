from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

SEQUENCE = [
    "prompts/0-input-preparation/01-convert-brs-word-to-markdown.md",
    "prompts/0-input-preparation/02-convert-architecture-word-to-markdown.md",
    "prompts/0-input-preparation/03-normalize-input-package.md",
    "prompts/1-routing/01-select-delivery-mode.md",
    "prompts/2-business-intake/01-create-business-intake-summary.md",
    "prompts/3-planning-and-modular-delivery/01-create-delivery-structure.md",
    "prompts/3-planning-and-modular-delivery/02-review-initial-architecture.md",
    "prompts/3-planning-and-modular-delivery/03-create-global-architecture-rules.md",
    "prompts/3-planning-and-modular-delivery/06-define-delivery-increments.md",
    "prompts/3-planning-and-modular-delivery/07-create-traceability-matrix.md",
    "prompts/4-engineering-readiness/01-check-engineering-readiness.md",
    "prompts/5-handoff-to-openspec/01-create-openspec-change-for-active-deliverable.md",
]

for p in SEQUENCE:
    if not (ROOT / p).exists():
        print(f"Missing prompt in sequence: {p}")
        raise SystemExit(1)

print("Prompt sequence validation passed.")
