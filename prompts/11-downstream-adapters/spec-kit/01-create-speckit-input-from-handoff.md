# Adapter Prompt — Create GitHub Spec Kit Input from Handoff

Use this when GitHub Spec Kit will own the specify / plan / tasks / implement workflow.

Input:
- `features/<feature-name>/handoff/spec-driven-handoff.md`
- Referenced source artifacts

Output:

```text
features/<feature-name>/handoff/spec-kit-input.md
```

Use this structure:

```markdown
# GitHub Spec Kit Input

## Feature Intent
## Business Context
## Scope
## Requirements
## User Stories / Acceptance Criteria
## Architecture Constraints
## Architecture & Contract Artifacts
## Enablement Needs
## Risks and Open Questions
## Instructions for Spec Kit
Use this content as the source for the specify phase.
```
