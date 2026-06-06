# Prompt — Create CI/CD Specification

Recommended environment:
- VS Code Copilot Chat
- Approved engineering LLM with access to existing pipeline files

Owner:
- Tech Lead / DevOps Engineer / Deployment Manager

Input files:
- `features/<feature-name>/enablement/enablement-scope.md`
- `features/<feature-name>/enablement/technical-stories.md`
- Existing pipeline files
- Existing deployment conventions

Task:
Create the CI/CD specification.

Output:
Create:

```text
features/<feature-name>/enablement/cicd-spec.md
```

Use this structure:

```markdown
# CI/CD Specification

## 1. Scope

## 2. Existing Pipelines to Reuse

## 3. New or Changed Pipelines

| Pipeline | Purpose | Trigger | Environments | Owner |
|---|---|---|---|---|

## 4. CI Requirements

- Build
- Static analysis
- Unit tests
- Security scanning
- Artifact creation

## 5. CD Requirements

- Deployment targets
- Approval gates
- Environment promotion
- Smoke tests
- Rollback hooks

## 6. Branch / PR / Merge Rules

## 7. Secrets and Credentials

## 8. Artifacts and Versioning

## 9. Deployment Validation

## 10. Failure Handling

## 11. Rollback Integration

## 12. Risks and Open Questions
```

Rules:
- Reuse existing pipeline standards.
- Do not bypass approvals or quality gates.
- Do not store secrets in pipeline code.
