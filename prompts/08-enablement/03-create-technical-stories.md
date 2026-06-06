# Prompt — Create Technical Stories

Recommended environment:
- VS Code Copilot Chat
- Approved engineering LLM with repository and architecture context

Owner:
- Tech Lead
- Platform Engineer / Cloud Engineer
- SRE / Deployment Manager where relevant

Input files:
- `features/<feature-name>/enablement/enablement-scope.md`
- `features/<feature-name>/enablement/enablement-structure.md`
- `features/<feature-name>/engineering-contracts/technical-spec.md` if available
- Existing pipeline/IaC conventions if available

Task:
Create technical stories with operational acceptance criteria.

Output:
Create:

```text
features/<feature-name>/enablement/technical-stories.md
```

Use this structure:

```markdown
# Technical Stories

## TS-001 — <title>

Parent enablement epic:
- EPIC-EN-001 — <title>

Parent enablement feature:
- FEAT-EN-001 — <title>

As a <Platform Engineer / SRE / Developer / Deployment Manager>,  
I want <technical capability>,  
so that <operational or delivery outcome>.

### Requirements Covered
- INFRA-xxx
- CICD-xxx
- ENV-xxx
- OBS-xxx
- REL-xxx

### Acceptance Criteria

#### AC-TS-001 — <title>
Given ...
When ...
Then ...

### Validation Method
- IaC plan/apply
- Pipeline run
- Deployment validation
- Smoke test
- Monitoring check
- Manual operational review

### Dependencies

### Risks

### Open Questions
```

Rules:
- Do not create business user stories here.
- Use technical stories for infrastructure, CI/CD, observability, release, and operations.
- Include clear validation criteria.
