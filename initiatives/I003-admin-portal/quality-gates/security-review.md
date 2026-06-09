# Security Review — I003 Admin Portal

## Metadata

| Field | Value |
|---|---|
| Initiative | I003-admin-portal |
| Gate | Security review |
| Triggered | Yes |
| Required | Yes |
| Owner | Security / Architecture |
| Artifact | quality-gates/security-review.md |
| Status | Accepted |
| Review date | 2026-06-09 |
| Reviewer | Security Team |

## Purpose
Scope and capture the security review for operational actions, privileges, secrets, and threat-model mitigations required before handoff to implementation.

## Scope
- Operational action endpoints and job processing (sync + async flows)
- Service principal `AdminPortalActionRunner` role and provisioning
- Azure AD group / app-role mappings and RBAC scoping across tenant→subscription mapping
- Secrets and Key Vault usage patterns
- Audit, authorization checks, and least-privilege controls
- Rate-limiting, dry-run, and rollback controls for high-risk actions

## Checklist (minimum evidence required)
- [ ] Threat model for operational actions (assets, actors, entry points, trust boundaries, mitigations)
- [ ] Review of `AdminPortalActionRunner` role definition (JSON) and IaC snippet from Ops
- [ ] Authentication & authorization flow diagrams and sequence for `actions/{actionId}/run` and `jobs/{jobId}`
- [ ] Verification that secrets (client secrets, certs) are stored and accessed via Key Vault with RBAC/Managed Identity
- [ ] Audit logging strategy for actions (immutability, retention, exportability)
- [ ] Abuse/rate-limiting controls and dry-run mode for potentially destructive operations
- [ ] List of residual risks and compensating controls for `Approved with risks` decision

## Acceptance Criteria
- Security owner records `Status: Accepted` in this artifact only after checklist items and mitigations are satisfied.
- Evidence attachments (threat-model, role JSON, IaC snippet) are present in this artifact or linked evidence folder.
- No blocking unresolved critical findings remain. Any remaining medium/low findings must have owners and remediation plans with timelines.

## Suggested Review Steps
1. Security: run threat-model session with Architecture and Product present (capture decisions in this file).
2. Ops: attach draft custom role JSON and IaC snippet under `evidence/` or inline.
3. Architecture: confirm async API and job model sequence diagrams are included.
4. Product: confirm acceptable dry-run and rollback semantics for each high-risk action.

## Notification to Security reviewers

Summary: The readiness check has triggered the Security review for I003 Admin Portal. Evidence and artifacts are attached under `quality-gates/evidence/` (role JSON, IaC snippet, AppInsights instrumentation, alert rule, dashboard sample, log queries). Please review the threat-model summary, role definition, and alerting proposals.

Key review actions:
- Validate the threat-model summary and add/export the full threat-model artefact here.
- Review `quality-gates/evidence/adminportal-role.json` and `adminportal-role-iac.md`; confirm least-privilege or propose required changes.
- Confirm required mitigations for residual risks and list any blocking findings.

If the Security team is satisfied, update the top Metadata `Status` field to `Accepted` and add `Review date` and reviewer name. If any critical findings are present, record them here with owners and target remediation dates.

Contact: Security on-call / security-team@example.com

## Evidence
- Link or paste threat-model output here.
- Link to `planning/open-decisions.md` for resolved decisions.

## Threat Model (summary)

**Assets**: tenant→subscription mapping, service principal credentials, inventory cache, audit store, action job queue, job status endpoints.

**Actors**: Admin Portal users (operators), service principals (AdminPortalActionRunner), platform admins, attackers (external), internal compromised identities.

**Entry Points**: `POST /actions/{actionId}/run`, `GET /jobs/{jobId}`, API auth endpoints, frontend UI.

**Trust Boundaries**: between frontend users and API; between API and subscription-scoped service principal; between job processor and target Azure resource APIs.

**Threats & Mitigations**:
- Unauthorized action invocation — enforce Azure AD auth, validate group membership and role, require per-tenant scoping.
- Credential leak of service principal — store secrets in Key Vault, use managed identity where possible, rotate creds regularly.
- Excessive privilege abuse — implement least-privilege `AdminPortalActionRunner` role (see evidence/adminportal-role.json) and deny dangerous NotActions.
- Long-running job hijack or spoofing — sign job tokens, validate job ownership, use idempotent job handlers and audit trail.
- Mass destructive operations — require `dry-run` and explicit confirmation for destructive actions; add rate-limiting and admin approval flows for bulk ops.

**Residual Risks**:
- MVP uses per-subscription service principal which increases management surface; mitigation: automation for provisioning and rotation, narrow scope, monitoring alerts.

## Evidence Files
- Role definition JSON: `quality-gates/evidence/adminportal-role.json`
- IaC snippet: `quality-gates/evidence/adminportal-role-iac.md`

- AppInsights / OpenTelemetry instrumentation samples: `quality-gates/evidence/appinsights-instrumentation.md`
- Alert rule sample (Bicep): `quality-gates/evidence/alert-rules.bicep`
- Dashboard sample (Azure dashboard JSON): `quality-gates/evidence/dashboard-sample.json`
- Log Analytics queries: `quality-gates/evidence/log-queries.md`

Attach additional evidence (threat-model export, diagrams) here as they are produced.

---

Generated as a kickoff draft for the security review gate.
