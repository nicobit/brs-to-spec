# Delivery Overview — I004 IT Portal

> Generated from initiative workspace. Last updated: 2026-06-11.
> Source of truth is `planning/delivery-structure.md` — this document is a readable snapshot.

## Summary

| Field | Value |
|---|---|
| Total epics | 5 |
| Total features | 10 |
| Total user stories | 6 (sample — delivery structure is draft; full stories confirmed after readiness = Ready) |
| Delivery mode | Standard |
| Readiness | Not ready — blocked on D-002 and D-003 |

---

## Delivery structure

### Epic: Authentication & Role Mapping

**Outcome:** IT staff can securely access the portal using their existing corporate identity, with role-appropriate views and admin-managed access control
**Priority:** Must have

#### Feature: Azure AD SSO integration

**Capability:** The portal authenticates users via Azure AD using SAML/OIDC and maps group memberships to portal roles
**Priority:** Must have

| Story ID | Story | Acceptance criteria | Requirement ref | Status |
|---|---|---|---|---|
| — | As a ServiceDesk user, I can sign in via Azure AD to access the portal | SSO succeeds for test user; group claims map to portal role | FR-1 | Pending |
| — | As an Admin, I can map Azure AD groups to portal roles via the admin UI | Mapping saved and applied to user sessions; changes produce an audit record | FR-1 | Pending |

#### Feature: Group-to-role mapping and admin UI

**Capability:** Administrators can manage role assignments and delegated admin scopes through a portal UI, with all changes captured in the audit log
**Priority:** Must have

---

### Epic: Request Intake & Approval Workflow

**Outcome:** Service desk agents and IT staff can submit, track and approve requests end-to-end without leaving the portal, with a full approval and audit trail
**Priority:** Must have

#### Feature: Request templates and custom fields

**Capability:** Users can create requests using configurable templates with custom fields appropriate to request type
**Priority:** Must have

| Story ID | Story | Acceptance criteria | Requirement ref | Status |
|---|---|---|---|---|
| — | As a ServiceDesk agent, I can create a hardware request from a template | Request persisted; approval chain created when required | FR-2 | Pending |

#### Feature: Approval chain engine and conditional approvals

**Capability:** The portal routes requests through configurable approval chains based on request type, cost and risk, and records every approval in the audit log
**Priority:** Must have

| Story ID | Story | Acceptance criteria | Requirement ref | Status |
|---|---|---|---|---|
| — | As an ITOperator, I can approve a request and trigger fulfillment actions | Approval recorded in audit log; request status transitions accordingly | FR-2 | Pending |

#### Feature: Request UI — create, edit, comment and track

**Capability:** All request lifecycle actions are available from a single portal view
**Priority:** Must have

---

### Epic: CMDB Read Sync & Asset Views

**Outcome:** Platform engineers and IT staff have an up-to-date, reconciled view of assets and configuration items from ServiceNow, without owning the CMDB records
**Priority:** Must have

#### Feature: ServiceNow CMDB connector (read-only, MVP)

**Capability:** The portal periodically syncs assets and configuration items from ServiceNow CMDB and surfaces reconciled data in the UI
**Priority:** Must have

| Story ID | Story | Acceptance criteria | Requirement ref | Status |
|---|---|---|---|---|
| — | As a PlatformEngineer, I can view asset details reconciled from CMDB | Asset data displays and reconciles against last sync snapshot | FR-5 | Pending |

#### Feature: Asset reconciliation and CI relationship views

**Capability:** Users can see CI relationships and ownership in the portal; manual CI linking is supported
**Priority:** Must have

---

### Epic: CI/CD Linking

**Outcome:** Platform engineers can trace changes from code commit through to deployment by linking pipeline runs to change requests in the portal
**Priority:** Must have

#### Feature: Connector for a single pipeline provider (GitHub Actions or Azure DevOps)

**Capability:** The portal connects to one CI/CD provider, receives webhook events for build and deploy status, and surfaces them against linked change requests
**Priority:** Must have

| Story ID | Story | Acceptance criteria | Requirement ref | Status |
|---|---|---|---|---|
| — | As a PlatformEngineer, I can link a PR / build to a change request | Build status displayed in the change request and updated on webhook events | FR-6 | Pending |

#### Feature: Link commits, PRs and builds to change requests; surface statuses

**Capability:** Build, PR and deployment artifacts are linked from change requests so any team member can trace deployment history
**Priority:** Must have

---

### Epic: Dashboards, Notifications & Audit Export

**Outcome:** IT managers and operators have real-time visibility of SLA status, pending approvals and deployment health, and can export audit logs for compliance
**Priority:** Must have

#### Feature: Role-specific dashboards

**Capability:** Each role sees a tailored dashboard — incidents and on-call for IT Operators, pending approvals and SLA metrics for IT Managers, deployment health for Platform Engineers
**Priority:** Must have

| Story ID | Story | Acceptance criteria | Requirement ref | Status |
|---|---|---|---|---|
| — | As an ITManager, I can see pending approvals and SLA dashboards | Dashboard shows metrics and links to underlying requests/incidents | FR-9 | Pending |

#### Feature: Notification templates (email, Teams/Slack) with SLA breach alerts

**Capability:** Configurable notifications are sent via email, Teams or Slack for key events including SLA breaches
**Priority:** Should have

#### Feature: Audit export and retention configuration

**Capability:** Administrators can export audit logs for a given period and configure retention policies
**Priority:** Must have

---

## Delivery increments

| Increment | Goal | Sprints | Key scope | Status |
|---|---|---|---|---|
| Inc-1 — MVP | Minimal production-safe portal with request intake, RBAC, CMDB read sync and CI/CD linking | 4 × 2-week sprints | Azure AD SSO, request CRUD + approvals, CMDB sync, CI/CD linking, basic dashboards | Pending |
| Inc-2 — Operations & Automation | Runbook attachments, automation hooks, richer notifications, improved dashboards | 3 sprints | Runbook service, Teams/Slack notifications, dashboard improvements | Pending |
| Inc-3 — Two-way CMDB & Policy | Controlled CMDB writes, policy integration, advanced reporting, audit workflows | 3–4 sprints | Guarded CMDB write flows, compliance export | Pending |

### Inc-1 Sprint breakdown

| Sprint | Focus | Deliverable |
|---|---|---|
| Sprint 1 | Spike & SSO PoC | Azure AD SSO PoC, group-to-role mapping, basic auth plumbing |
| Sprint 2 | Request CRUD + Approval | Minimal request UI, API, approval state machine, audit logging |
| Sprint 3 | CMDB Sync & Asset Views | Read-only ServiceNow connector, reconciliation surface in UI |
| Sprint 4 | CI/CD Linking & Dashboards | Pipeline provider hook, build/deploy status in change requests, basic dashboard |

---

## Dependency wave order

Not yet available — handoff has not been generated. Available after readiness = Ready and all quality gates accepted.

---

## Traceability summary

| Requirement | Epic / Feature that delivers it |
|---|---|
| FR-1 Authentication & Authorization | Authentication & Role Mapping — Azure AD SSO, group-to-role mapping |
| FR-2 Request Management | Request Intake & Approval — templates, approval engine, request UI |
| FR-3 Incident & Problem Management | Cross-cutting — incident lifecycle (stories to be detailed in confirmed delivery structure) |
| FR-4 Change Management | Cross-cutting — change requests and emergency change paths |
| FR-5 CMDB Integration | CMDB Read Sync & Asset Views — ServiceNow connector (read-only MVP) |
| FR-6 CI/CD Integration | CI/CD Linking — connector and build status surface |
| FR-7 Runbooks & Playbooks | Inc-2 — Runbook service (post-MVP) |
| FR-8 Notifications & Alerts | Dashboards, Notifications & Audit Export — notification templates |
| FR-9 Dashboards & Reporting | Dashboards, Notifications & Audit Export — role-specific dashboards |
| FR-10 Audit, Logging & Compliance | Dashboards, Notifications & Audit Export — audit export; cross-cutting audit store |
