
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
REQUIRED = [
    "README.md",
    "HOW_TO_USE.md",
    "docs/14-agile-planning-view.md",
    "prompts/7-perspectives/agile-planning/README.md",
    "prompts/7-perspectives/agile-planning/01-create-gitlab-planning-view.md",
    "prompts/7-perspectives/agile-planning/02-refresh-gitlab-planning-view.md",
    "templates/perspectives/agile-planning/gitlab-planning-view.md",
    "templates/perspectives/agile-planning/gitlab-refresh-report.md",
    "examples/real-project-end-to-end/perspectives/agile-planning/gitlab-planning-view.md",
    "prompts/4-engineering-readiness/01-check-engineering-readiness.md",
    "templates/engineering-readiness/readiness-check.md",
]
missing=[p for p in REQUIRED if not (ROOT/p).exists()]
if missing:
    print("Missing required files:")
    for p in missing: print(f" - {p}")
    raise SystemExit(1)
checks={
    "README.md":["v1.0.4","planning projection","source of truth"],
    "docs/14-agile-planning-view.md":["projection","source of truth","GitLab"],
    "prompts/7-perspectives/agile-planning/01-create-gitlab-planning-view.md":["## Role","## Context","## Quality bar","not the source of truth","Do Not Duplicate"],
    "templates/perspectives/agile-planning/gitlab-planning-view.md":["planning projection","Source Artifact Map","Do Not Duplicate"],
}
for file,terms in checks.items():
    text=(ROOT/file).read_text(encoding="utf-8", errors="ignore")
    for term in terms:
        if term not in text:
            print(f"Content check failed: {file} missing {term!r}")
            raise SystemExit(1)
print("Validation passed.")
