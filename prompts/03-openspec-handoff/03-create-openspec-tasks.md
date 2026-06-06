# Prompt — Create OpenSpec Tasks

Recommended environment:
- VS Code Copilot Chat

Owner:
- Engineering Lead / Senior Developer

Repository access is strongly recommended.

You are a senior engineering lead preparing implementation tasks for Copilot and developers.

Input files:
- `features/<feature-name>/openspec-change/proposal.md`
- `features/<feature-name>/openspec-change/design.md`
- `features/<feature-name>/business-intake/user-stories.md`
- `features/<feature-name>/engineering-contracts/bdd-scenarios.md`
- `features/<feature-name>/engineering-contracts/test-plan.md` if available

Task:
Create small implementation tasks.

Rules:
- Each task should be suitable for one PR or one Copilot coding session.
- Avoid combining unrelated backend, frontend, database, and integration changes unless necessary.
- Each task must include tests.
- Each task must include requirements/user stories covered.
- Include "Do Not Do" constraints.
- Include Definition of Done.

Output:
Create `features/<feature-name>/openspec-change/tasks.md`.

Structure:

```markdown
# Tasks — <feature name>

## Task 001 — <title>

Status: Not Started

### Goal

### Requirements Covered

### User Stories / Acceptance Criteria Covered

### BDD / Test Cases Covered

### Context Files to Read First

### Existing Code Areas to Inspect

### Implementation Instructions

### Do Not Do

### Expected Changes

### Tests Required

### Definition of Done

### Review Checklist
```

Each OpenSpec task should include:
- Parent epic
- Parent feature/capability
- Requirements covered
- User stories / acceptance criteria covered
