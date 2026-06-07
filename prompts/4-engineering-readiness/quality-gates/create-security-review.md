# Quality Gate Prompt — Create Security Review

## Purpose

Review the active deliverable for security, authorization, data protection, audit, and compliance risks.

Use this only when the readiness check or architecture review indicates security relevance.

## Inputs

Use:
- BRS,
- initial architecture,
- global architecture rules,
- OpenSpec proposal/design/tasks,
- API/data/event contracts if available.

## Output file

```text
quality-gates/security-review.md
```

## Output structure

```markdown
# Security Review

## Active Deliverable

## Review Decision
Approved / Approved with risks / Not approved

## Security Scope

## Controls Checked

| Control Area | Required? | Compliant? | Notes |
|---|---|---|---|
| Authentication |  |  |  |
| Authorization |  |  |  |
| Data protection |  |  |  |
| Auditability |  |  |  |
| Input validation |  |  |  |
| Secrets management |  |  |  |
| Logging / monitoring |  |  |  |
| Regulatory / compliance |  |  |  |

## Findings

| Finding ID | Severity | Description | Recommendation |
|---|---|---|---|

## Required Actions
```

## Rules

- Be critical.
- Keep the review scoped to the active deliverable.
- Do not create implementation code.
- Highlight blockers clearly.
