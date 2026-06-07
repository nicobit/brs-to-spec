from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
SEQUENCE = [
    'prompts/0-input-preparation/01-convert-brs-word-to-markdown.md',
    'prompts/0-input-preparation/02-convert-architecture-word-to-markdown.md',
    'prompts/0-input-preparation/03-normalize-input-package.md',
    'prompts/1-routing/01-select-delivery-and-execution-mode.md',
    'prompts/2-business-intake/01-create-business-intake-summary.md',
    'prompts/3-planning-and-modular-delivery/01-review-initial-architecture.md',
    'prompts/3-planning-and-modular-delivery/02-create-global-architecture-rules.md',
    'prompts/3-planning-and-modular-delivery/03-create-delivery-structure.md',
    'prompts/4-engineering-readiness/01-check-engineering-readiness.md',
    'prompts/5-handoff/01-create-openspec-change-for-active-deliverable.md',
    'prompts/5-handoff/02-create-standalone-delivery-package.md',
]
for p in SEQUENCE:
    if not (ROOT / p).exists():
        print(f'Missing prompt: {p}')
        raise SystemExit(1)
print('Prompt sequence validation passed.')
