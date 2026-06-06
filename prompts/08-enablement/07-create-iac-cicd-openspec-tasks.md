# Prompt — Create IaC / CI-CD / Operations OpenSpec Tasks

Recommended environment:
- VS Code Copilot Chat
- Approved engineering LLM with repository context

Owner:
- Engineering Lead / Tech Lead
- Platform Engineer / DevOps Engineer / SRE where relevant

Input files:
- `features/<feature-name>/enablement/enablement-structure.md`
- `features/<feature-name>/enablement/technical-stories.md`
- `features/<feature-name>/enablement/infrastructure-spec.md` if available
- `features/<feature-name>/enablement/cicd-spec.md` if available
- `features/<feature-name>/enablement/observability-spec.md` if available
- `features/<feature-name>/enablement/release-rollback-plan.md` if available
- `features/<feature-name>/openspec-change/tasks.md`

Task:
Create enablement implementation tasks and merge them into, or append them to, the OpenSpec `tasks.md`.

Output:
Update:

```text
features/<feature-name>/openspec-change/tasks.md
```

Add tasks with this structure:

```markdown
## Task <number> — <title>

Type: Enablement / Infrastructure | CI-CD | Environment | Observability | Release | Operations

Status: Not Started

### Parent Enablement Epic

- EPIC-EN-xxx

### Parent Enablement Feature / Capability

- FEAT-EN-xxx

### Technical Stories Covered

- TS-xxx

### Requirements Covered

- INFRA-xxx
- CICD-xxx
- ENV-xxx
- OPS-xxx
- OBS-xxx
- REL-xxx

### Context Files to Read First

### Existing Code / IaC / Pipeline Areas to Inspect

### Implementation Instructions

### Do Not Do

### Expected Changes

### Validation Required

### Definition of Done

### Review Checklist
```

Rules:
- Keep enablement tasks separate from application tasks.
- Do not combine infrastructure, CI/CD, observability, and application code into one large task.
- Each task must have validation.
- Each task must be reviewable in a PR.
