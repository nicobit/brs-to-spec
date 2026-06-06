# Prompt — Identify Enablement Scope

Recommended environment:
- VS Code Copilot Chat
- ChatGPT or another approved LLM if all input artifacts are provided

Owner:
- Architect / Tech Lead
- Platform Engineer / Cloud Engineer
- SRE / Deployment Manager where relevant

Repository/code access needed:
- Useful, especially for existing pipelines, IaC, deployment scripts, and observability patterns

Input files:
- `features/<feature-name>/business-intake/requirements.md`
- `features/<feature-name>/business-intake/epics-and-features.md`
- `features/<feature-name>/business-intake/user-stories.md`
- `features/<feature-name>/business-intake/brs-architecture-alignment.md` if available
- `features/<feature-name>/input/architecture-draft.md`
- Existing repository pipeline/IaC files if available

Task:
Identify whether this feature needs an Enablement Track and what enablement areas are in scope.

Check for:
- Infrastructure / Azure resources
- Database / storage
- Messaging / queue / event topics
- Network / private endpoints / firewall / DNS
- Identity / access / managed identity / service principal
- Secrets / Key Vault / certificates
- CI pipeline
- CD pipeline
- Environment configuration
- Observability / logging / metrics / alerts
- Release / rollback
- Operational readiness / runbooks
- SRE / support readiness
- Platform governance / tagging / cost / compliance

Output:
Create:

```text
features/<feature-name>/enablement/enablement-scope.md
```

Use this structure:

```markdown
# Enablement Scope

## 1. Summary

## 2. Enablement Needed?
Yes / No / Partial

## 3. In-Scope Enablement Areas

| Area | Needed? | Reason | Owner | Risk |
|---|---|---|---|---|

## 4. Out-of-Scope Enablement Areas

| Area | Reason |
|---|---|

## 5. Existing Assets to Reuse

| Asset | Location | Purpose |
|---|---|---|

## 6. New Assets Potentially Needed

| Asset | Type | Reason | Owner |
|---|---|---|---|

## 7. Risks and Open Questions

| ID | Question / Risk | Owner | Blocks implementation? |
|---|---|---|---|

## 8. Recommended Enablement Flow

Minimal / Full

## 9. Recommended Next Prompts
```

Rules:
- Do not invent infrastructure.
- If unsure, mark as open question.
- Prefer reusing existing platform and pipeline patterns.

## Mandatory use of architecture alignment

If this file exists, read it:

```text
features/<feature-name>/business-intake/brs-architecture-alignment.md
```

Use it to identify enablement needs such as:
- infrastructure
- CI/CD
- environment configuration
- secrets
- observability
- release/rollback
- operational readiness
- SRE/platform tasks
