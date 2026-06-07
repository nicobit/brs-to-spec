---
description: Create GitLab Planning View as a projection, not source of truth.
---

# Create GitLab Planning View

Work inside the active feature workspace.

Use:

```text
prompts/7-perspectives/agile-planning/01-create-gitlab-planning-view.md
templates/perspectives/agile-planning/gitlab-planning-view.md
```

## Rule

The planning view is a projection only.

Do not redefine requirements, architecture constraints, acceptance criteria, quality gates, or implementation tasks.

## Output

Create:

```text
perspectives/agile-planning/gitlab-planning-view.md
```

Every Epic / Feature / User Story / Task must reference a source artifact and source ID where possible.

User stories must use:

```text
As a <persona>,
I want <capability>,
so that <business value>.
```
