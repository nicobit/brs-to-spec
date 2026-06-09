# Proposal — D2: Support Tools and Retry Flows

> OpenSpec change proposal. Drive implementation with `/opsx:apply` against this folder.
> Copy this folder (`openspec/changes/D2-support-and-retry/`) into the target code repository before applying.
> **Depends on D1 being deployed** — D2 reads `verification_records` and `profiles` tables created in D1.

## Why

After D1 goes live, onboarding failures will occur — IDP timeouts, webhook delivery failures, payment errors. Without support tooling, support agents cannot diagnose or recover failed flows, and users are left stuck. This increment delivers the support UI, operator retry endpoints, and verification failure handling that make the onboarding flow operable.

## What changes

- New support UI — view onboarding state and verification details by onboarding ID
- New `POST /support/onboarding/{id}/retry` endpoint — operator-triggered verification retry
- RBAC for support UI — least-privilege access for support agent role
- Verification failure handling — structured failure reasons surfaced to support UI
- Notification template management — SendGrid template configuration for operators
- Audit logging for all support actions
- Enhanced telemetry — `support_retries_total`, support UI event tracking

## Scope

### In scope

| Feature | User story summary | Requirement |
|---|---|---|
| F-002.2 Verification failure handling | Support agent sees failure details and can retry verification | FR-005 |
| F-003.2 Notification template management | Operator manages SendGrid templates and configuration | FR-004 |
| F-004.1 Support UI | Support agent views onboarding state and triggers retries | FR-005 |
| F-004.2 Support RBAC and audit | Role-based access and audit logs for all support actions | FR-005, AR-SEC-002 |

### Out of scope (explicitly)

- Core onboarding flow changes — D1
- Regional deployment hardening — D3
- Data residency enforcement — D3
- CRM sync — D3
- Payment Provider A integration — not required for pilot

## Success criteria

| Criterion | Target | Source |
|---|---|---|
| Support agents can search by onboarding ID | UI returns state within 2 s | FR-005 |
| Retry endpoint triggers new IDP verification | New `verification_records` row created | FR-005 |
| All support actions audit-logged | Audit log entry present for every support action | AR-SEC-002 |
| RBAC enforced | Support role cannot access admin endpoints | AR-SEC-002 |

## Constraints inherited from upstream

| Constraint | Source artifact |
|---|---|
| D1 DB schema must be live before D2 coding starts | D1 `tasks.md` handoff checklist |
| RBAC: least-privilege for support agent role | `architecture/architecture-rules.md` AR-SEC-002 |
| All support actions audit-logged | `quality-gates/security-review.md` |
| Secrets in Azure Key Vault | `architecture/architecture-rules.md` AR-SEC-001 |
| Correlation ID propagated through support endpoints | `quality-gates/observability-plan.md` |

## Reference artifacts

| Artifact | Path | What to read there |
|---|---|---|
| D1 handoff | `openspec/changes/D1-guided-onboarding/` | DB schema, API surface, integration contracts established in D1 |
| Architecture rules | `architecture/architecture-rules.md` | RBAC and audit requirements |
| Security review | `quality-gates/security-review.md` | RBAC and audit checklist |
| Observability plan | `quality-gates/observability-plan.md` | Support UI telemetry, `support_retries_total` |
| Data contract | `quality-gates/data-contract.md` | `audit_logs` table spec |
