# Prompt — Create Operational Readiness Package

Recommended environment:
- VS Code Copilot Chat
- Approved engineering LLM with architecture and operations context

Owner:
- SRE / Operations Lead / Tech Lead / Deployment Manager

Input files:
- `features/<feature-name>/enablement/enablement-scope.md`
- `features/<feature-name>/enablement/infrastructure-spec.md` if available
- `features/<feature-name>/enablement/cicd-spec.md` if available
- `features/<feature-name>/engineering-contracts/technical-spec.md`

Task:
Create operational readiness artifacts for the feature.

Output:
Create or update:

```text
features/<feature-name>/enablement/observability-spec.md
features/<feature-name>/enablement/release-rollback-plan.md
features/<feature-name>/enablement/operational-readiness.md
```

Use these structures:

```markdown
# Observability Specification

## Logs
## Metrics
## Traces
## Dashboards
## Alerts
## Audit Events
## Smoke Checks
## Support Queries
## Open Questions
```

```markdown
# Release and Rollback Plan

## Release Scope
## Environments
## Deployment Steps
## Validation Steps
## Rollback Trigger Conditions
## Rollback Steps
## Communication Plan
## Risks
```

```markdown
# Operational Readiness

## Support Model
## Runbooks
## Known Failure Modes
## Monitoring Coverage
## Alert Ownership
## On-call / Escalation
## Documentation Links
## Handover Checklist
## Go/No-Go Checklist
```

Rules:
- Do not invent support processes.
- Use existing operational standards where available.
- Mark missing operational decisions as open questions.
