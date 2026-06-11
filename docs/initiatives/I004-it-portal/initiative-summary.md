# Initiative Summary — I004 IT Portal

> Generated from initiative workspace. Last updated: 2026-06-11.
> Source of truth is the initiative workspace — this document is a readable snapshot.

## At a glance

| Field | Value |
|---|---|
| Initiative ID | I004 |
| Initiative name | IT Portal |
| Business objective | Unified, role-based web portal for IT teams to manage requests, incidents, changes, deployments and runbooks from a single interface |
| Why now | IT teams lack a single-pane view; workflows are fragmented across ServiceNow, CI/CD tools and manual processes; compliance and auditability gaps exist |
| Delivery mode | Standard |
| Execution mode | Standalone |
| Current stage | Engineering readiness — blocked on two open decisions |
| Status | Not ready — awaiting human input on D-002 and D-003 |

## Scope

| Area | In scope | Out of scope |
|---|---|---|
| Authentication | SSO via Azure AD, group-to-role RBAC mapping | Custom IdP providers beyond Azure AD (MVP) |
| Request management | Request intake, approval chains, templates, audit log | Advanced policy engine integration (future) |
| CMDB | Read-only sync from ServiceNow, asset views, reconciliation | Portal owning CMDB records, two-way write (post-MVP) |
| CI/CD integration | Link commits / PRs / builds to change requests for one provider | Multi-provider linking (post-MVP) |
| Incident & change | Incident lifecycle, change requests, emergency paths | Full ITSM replacement — ServiceNow remains source-of-record |
| Dashboards & reporting | Role-specific dashboards, audit export, notifications | Advanced analytics and auto-topology discovery |
| AI assistant | Context-aware answers in dev/qa scope, auditable actions | Production assistant scope (post-MVP) |

## Objectives

| ID | Objective | Success measure |
|---|---|---|
| OBJ-001 | Single-pane role-specific operations for IT workflows | All primary roles (IT Operator, Platform Engineer, Service Desk, IT Manager) can complete core tasks in the portal |
| OBJ-002 | Automate common request workflows and approvals | 60% of routine request types handled end-to-end without manual intervention by launch |
| OBJ-003 | Integrate with ServiceNow, CI/CD, Azure AD and monitoring | End-to-end request intake with ServiceNow integration demonstrated; CI/CD linking surfaces build status |
| OBJ-004 | Enforce RBAC and provide immutable audit trails | RBAC enforced at API and UI level; audit export produced and readable for sample period |
| OBJ-005 | Improve incident response speed | MTTA reduced by 30% within 3 months; 95% of high-priority incidents acknowledged within SLA |

## Key requirements

| ID | Requirement | Priority |
|---|---|---|
| FR-1 | SSO via Azure AD with RBAC (ServiceDesk, ITOperator, PlatformEngineer, ITManager, Admin) | Must have |
| FR-2 | Request intake with approval chains, templates and audit log | Must have |
| FR-3 | Incident and problem management with severity, ownership and root-cause linking | Must have |
| FR-4 | Change management with approvals, maintenance windows and emergency change paths | Must have |
| FR-5 | Read-only CMDB sync from ServiceNow with CI relationship views | Must have (MVP: read-only) |
| FR-6 | CI/CD linking to surface build/deploy status in change requests | Must have |
| FR-7 | Runbooks and playbooks associated with incidents and changes | Should have |
| FR-8 | Configurable notifications (email, Teams/Slack) with SLA breach alerts | Should have |
| FR-9 | Role-specific dashboards and audit export | Must have |
| FR-10 | Immutable append-only audit trail with configurable retention and export | Must have |
| NFR-1 | 99.9% availability in primary region | Must have |
| NFR-4 | Data encrypted in transit and at rest; secrets in Azure Key Vault | Must have |

## Key constraints

| Constraint | Source | Impact |
|---|---|---|
| Audit trail must be append-only and exportable | FR-10, NFR-5 | Requires append-only storage selection and retention policy before handoff |
| SSO via Azure AD only | FR-1 | SAML/OIDC integration required; group-to-role mapping must be validated in PoC |
| Test-data masking in non-prod environments | Data & Privacy (BRS) | CI pipelines must include data-masking step |
| 99.9% availability in primary region | NFR-1 | Design for redundancy, autoscaling and multi-AZ deployment |
| Secrets in Azure Key Vault via managed identities | AR-030 | No secrets in code, config files or plain-text storage |
| ServiceNow is authoritative for CMDB records (MVP) | AR-002 | Portal is read-only for CMDB in MVP; no portal-owned asset records |

## Key decisions made

| Decision | Answer | Decided by |
|---|---|---|
| No decisions resolved yet | — | — |

## Open decisions

| Decision | Owner | Blocking? |
|---|---|---|
| D-001 — Which CI/CD provider for MVP? (GitHub Actions / Azure DevOps) | Product Owner / Platform | No |
| D-002 — Will portal own any asset types or is ServiceNow authoritative? | Product Owner / Platform | **Yes** |
| D-003 — Audit retention policy and storage choice | Security / Compliance | **Yes** |
| D-004 — Claim-to-role mapping approach for Azure AD | Platform / Identity | No |

## Current status

Engineering readiness has been assessed and returned **Not ready**. Two blocking decisions must be resolved before the initiative can advance: D-002 (CMDB ownership — Product Owner / Platform) and D-003 (audit retention and storage — Security / Compliance). Questionnaire stubs have been created at `input/contracts/servicenow-integration.md` and `input/constraints/audit-retention.md`. Five quality gates have been pre-identified as required (security review, data contract, API contract, observability plan, BDD scenarios) and will be created once blocking decisions are resolved.
