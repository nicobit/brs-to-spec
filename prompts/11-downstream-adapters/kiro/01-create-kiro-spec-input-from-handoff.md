# Adapter Prompt — Create Kiro Spec Input from Handoff

Use this when Kiro will own the detailed spec and implementation workflow.

Input:
- `features/<feature-name>/handoff/spec-driven-handoff.md`
- Referenced source artifacts

Output:

```text
features/<feature-name>/handoff/kiro-spec-input.md
```

Use this structure:

```markdown
# Kiro Spec Input

## Goal
## Business Background
## Functional Requirements
## Non-Functional Requirements
## User Stories
## Architecture Constraints
## API / Data / Event / Domain Contracts
## Enablement Needs
## Acceptance Criteria
## Risks / Questions
## Implementation Boundaries
```
