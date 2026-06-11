# Business Intake Summary — I004 IT Portal

Purpose
-------
Summarise the core business intent, scope, stakeholders and high-level acceptance criteria so downstream personas can create delivery structure and architecture rules.

Problem Statement
-----------------
IT teams need a unified role-based portal to manage requests, incidents, changes, deployments and runbooks to improve visibility, enforce approvals, and provide auditability across the delivery lifecycle.

Objectives
----------
- Single-pane role-specific operations for IT workflows.
- Automate common request workflows and approvals.
- Integrate with ServiceNow CMDB and ticketing, CI/CD systems, identity provider, and monitoring.
- Enforce RBAC and provide immutable audit trails for compliance.

In-scope (MVP)
---------------
- SSO via Azure AD and role mapping.
- Request intake with approval chains and audit logging.
- Read-only CMDB sync (ServiceNow) and basic asset views.
- CI/CD linking (one provider) to surface build/deploy status in change requests.
- Role-specific dashboards and basic reporting.

Out of scope (MVP)
-------------------
- Full two-way CMDB ownership (deferred to later iteration).
- Replacing enterprise ITSM (ServiceNow remains source-of-record).
- Advanced discovery and automatic topology population.

Primary stakeholders
--------------------
- IT Operations (owners)
- Platform/DevOps
- Security & Compliance
- Service Desk

Key assumptions & constraints
---------------------------
- ServiceNow is available as the primary ticketing and CMDB provider for MVP.
- Azure AD is used for SSO and group-based role mapping.
- Secrets and PII will be masked in non-prod environments; production requires stricter controls.

High-level acceptance criteria
-----------------------------
- End-to-end request intake with approval and audit trail demonstrated.
- RBAC enforced for APIs and UI with role-specific views.
- CMDB read sync shows reconciled assets in UI.
- CI/CD linking surfaces commit/build status for at least one pipeline provider.
- Audit export for a sample period is available and readable.

Suggested MVP epics
-------------------
1. Authentication & Role Mapping (Azure AD integration)
2. Request Intake & Approval Workflow (CRUD, templates, approvals)
3. CMDB Read Sync & Asset Views (ServiceNow connector, reconciliation)
4. CI/CD Linking (connect one pipeline provider and surface statuses)
5. Dashboards, Notifications & Audit Export

Immediate next actions
----------------------
1. Confirm the primary ticketing and CI/CD providers for MVP (Product Owner + Platform/DevOps).
2. Create `planning/delivery-structure.md` with epics mapped to acceptance criteria.
3. Agree environment subscription/resource-group mapping and record in `engineering-readiness`.

Contacts
--------
- Product Owner: (TBD)
- Platform/DevOps: (TBD)
- Security Lead: (TBD)
