from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
REQUIRED = [
    'README.md','HOW_TO_USE.md','CHANGELOG.md',
    '.github/copilot-instructions.md',
    '.github/prompts/brs-to-spec-run-workflow.prompt.md',
    '.github/prompts/create-engineering-readiness.prompt.md',
    '.github/prompts/create-openspec-handoff.prompt.md',
    '.github/prompts/create-standalone-handoff.prompt.md',
    '.github/prompts/create-gitlab-planning-view.prompt.md',
    '.vscode/settings.json','docs/15-github-copilot-workflow.md',
    'docs/14-agile-planning-view.md',
    'prompts/4-engineering-readiness/01-check-engineering-readiness.md',
    'templates/engineering-readiness/readiness-check.md',
]
missing = [p for p in REQUIRED if not (ROOT/p).exists()]
if missing:
    print('Missing required files:')
    [print(' - '+p) for p in missing]
    raise SystemExit(1)
checks = {
    '.github/copilot-instructions.md': ['Source of truth hierarchy','Architecture rule','Conditional Quality Gates','GitLab Planning View','User story format','Do not'],
    '.github/prompts/brs-to-spec-run-workflow.prompt.md': ['Workflow Status','Recommended Next Step'],
    'docs/15-github-copilot-workflow.md': ['GitHub Copilot / VS Code Workflow','.github/copilot-instructions.md','Do not ask Copilot'],
    'README.md': ['v1.0.5','Copilot instructions'],
}
for file, terms in checks.items():
    text = (ROOT/file).read_text(encoding='utf-8', errors='ignore')
    for term in terms:
        if term not in text:
            print(f'Content check failed: {file} missing {term!r}')
            raise SystemExit(1)
print('Validation passed.')
