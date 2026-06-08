---
description: Create GitLab Planning View as a projection, not source of truth.
---

# Create GitLab Planning View

Work inside the active initiative workspace.

Use:

```text
prompts/7-perspectives/agile-planning/01-create-gitlab-planning-view.md
templates/perspectives/agile-planning/gitlab-planning-view.md
```

## Rule

The planning view is a projection only.

Do not redefine requirements, architecture constraints, acceptance criteria, quality gates, or implementation tasks.

Use the view as the team-facing Delivery Planning View, not as a new workflow.

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

User stories are business context and traceability only.

Do not implement from user stories alone.

Implementation must come from approved OpenSpec or standalone tasks.
