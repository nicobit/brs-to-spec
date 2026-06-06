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

## Enablement tasks

If enablement artifacts exist under:

```text
features/<feature-name>/enablement/
```

then include both application and enablement tasks.

Enablement task types include:

```text
Infrastructure
CI-CD
Environment
Observability
Release
Operations
```

Each enablement task must reference:
- Parent enablement epic
- Parent enablement feature/capability
- Technical stories covered
- INFRA/CICD/ENV/OPS/OBS/REL requirements covered
- IaC/pipeline/configuration areas to inspect
- validation required

## Mandatory use of architecture alignment

If this file exists, read it:

```text
features/<feature-name>/business-intake/brs-architecture-alignment.md
```

If an alignment finding implies implementation or validation work, create or update a task for it.

Examples:
- missing audit payload definition → task to define/implement audit payload
- missing infrastructure decision → enablement task
- unclear authorization boundary → task to implement/validate authorization
- unsupported integration flow → task or open decision before implementation
