# Prompt — Create Enablement Structure

Recommended environment:
- VS Code Copilot Chat
- Approved engineering LLM with architecture and repository context

Owner:
- Architect / Tech Lead
- Platform Engineer / Cloud Engineer
- SRE / Deployment Manager where relevant

Input files:
- `features/<feature-name>/enablement/enablement-scope.md`
- `features/<feature-name>/input/architecture-draft.md`
- `features/<feature-name>/business-intake/brs-architecture-alignment.md` if available
- `features/<feature-name>/engineering-contracts/technical-spec.md` if available

Task:
Create the enablement delivery structure.

This is parallel to the product delivery structure, but for infrastructure, CI/CD, environment, observability, release, and operational readiness.

Output:
Create:

```text
features/<feature-name>/enablement/enablement-structure.md
```

Use this structure:

```markdown
# Enablement Structure

## 1. Enablement Objectives

### EO-001 — <title>

Description:

Success measures:

## 2. Enablement Epics

### EPIC-EN-001 — <title>

Enablement objectives:
- EO-001

Description:

Value:

In scope:

Out of scope:

Related product epics/features:
- EPIC-xxx
- FEAT-xxx

## 3. Enablement Features / Capabilities

### FEAT-EN-001 — <title>

Parent enablement epic:
- EPIC-EN-001

Description:

Value:

Related requirements:
- INFRA-xxx
- CICD-xxx
- ENV-xxx
- OPS-xxx
- OBS-xxx
- REL-xxx

Candidate technical stories:
- TS-xxx — <candidate title>

Dependencies:

Assumptions:

Open questions:

## 4. Product-to-Enablement Mapping

| Product Feature | Enablement Epic | Enablement Feature | Why Needed |
|---|---|---|---|

## 5. Enablement Delivery Slicing

Suggest a safe order, for example:
1. Infrastructure foundation
2. CI validation
3. CD deployment
4. Environment configuration
5. Observability
6. Release/rollback
7. Operational readiness
```

Rules:
- Keep enablement separate from business user stories.
- Use technical/operational language.
- Do not create implementation tasks yet.
