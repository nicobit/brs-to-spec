# Business Requirements Specification (BRS) — I004: IT Portal

Overview
--------
This document describes the business requirements for the IT Portal: a unified, role-based web portal that enables the IT team to manage the full lifecycle of IT assets, requests, incidents, changes, deployments and operational runbooks. The portal's goal is to centralize visibility, improve efficiency, enforce approvals and compliance, and provide traceability across the delivery and operational lifecycle.

Objectives
----------
- Provide a single-pane view for IT teams to manage requests, incidents, and lifecycle events.
- Automate common workflows (request intake, approvals, provisioning, decommissioning).
- Integrate with ticketing, CMDB, source control, CI/CD, monitoring, and identity providers.
- Enforce role-based access, approval policies, and audit trails for compliance.
- Provide dashboards and KPIs to measure SLA adherence, throughput, and operational health.

Scope (In-scope)
-----------------
- Request intake and fulfillment workflows (hardware, software, access, provisioning).
- Incident, problem, and change lifecycle management (linking tickets to changes and deployments).
- Asset and configuration management integration (CMDB synchronization and UI views).
- Deployment orchestration hooks and CI/CD integration for automated releases.
- Role-based dashboards, reporting, notifications and audit logs.

Out of scope (initial release)
------------------------------
- Full ITSM replacement — existing enterprise ticketing system remains the source-of-record for tickets.
- Deep discovery/auto-population of topology beyond CMDB integrations (future enhancement).

Primary Stakeholders
--------------------
- IT Operations (owners of incident & on-call workflows)
- Platform/DevOps (deployment, pipeline owners)
- Security & Compliance (audit, access control policies)
- Service Desk (request triage)

User Personas
-------------
- IT Operator: triages incidents, runs runbooks, views on-call dashboard.
- Platform Engineer: creates deployments, links releases to changes, monitors pipelines.
- Service Desk Agent: creates/triages requests, escalates to IT Operator.
- IT Manager: reviews KPI dashboards, approves escalations and major changes.

High-level Workflows
--------------------
1. Request Intake: user submits request → automated validation → assignment/approval → fulfillment (manual or automated) → closure.
2. Incident to Change: incident raised → diagnosis → create change request → schedule deployment → post-deployment validation → close.
3. Asset Lifecycle: create asset entry from provisioning → track ownership, warranty, decommission schedule → archive on decommission.
4. Deployment Flow: create release → link to change request → trigger CI/CD → monitor runbooks and metrics → automated rollback on failure (where supported).

Functional Requirements
-----------------------
FR-1: Authentication & Authorization
- Support SSO via enterprise IdP (SAML or OIDC).
- Role-based access control (RBAC) with at least roles: ServiceDesk, ITOperator, PlatformEngineer, ITManager, Admin.

FR-2: Request Management
- Create, edit, comment, and track requests with customizable templates and fields.
- Support request approval chains and conditional approvals based on request type and cost/risk.

FR-3: Incident & Problem Management
- Create incidents with severity, assign owners, link related requests and assets.
- Support incident timelines, root-cause linking to problems and changes.

FR-4: Change Management
- Create change requests, propose maintenance windows, capture approvals, and link to deployment artifacts.
- Support emergency change paths with expedited approvals and post-facto audit trails.

FR-5: Asset & Configuration (CMDB) Integration
- Sync assets and configuration items from the CMDB (periodic and on-change sync).
- Display CI relationships and ownership in UI; allow manual CI linking.

FR-6: Deployment & CI/CD Integration
- Link change requests to pipeline runs (Git commit, PR, build ID) and surface status in portal.
- Provide buttons/links to trigger approved automated deployments where permitted.

FR-7: Runbooks & Playbooks
- Associate runbooks with incidents and changes, present step-by-step remediation and capture run results.

FR-8: Notifications & Alerts
- Configurable notifications via email, chat (Teams/Slack), and in-portal; include SLA breach alerts.

FR-9: Dashboards & Reporting
- Role-specific dashboards: open/incidents, SLA status, pending approvals, deployment health, asset inventories.
- Ad-hoc reporting and export (CSV/JSON) for audits.

FR-10: Audit, Logging & Compliance
- Immutable audit trail for approvals, changes, and sensitive actions (who/what/when).
- Support export of audit logs for compliance review.

Non-Functional Requirements
---------------------------
- NFR-1: Availability — portal must achieve 99.9% uptime for the primary region.
- NFR-2: Performance — typical pages load within 2s; dashboard queries under 5s for data sets up to 10k rows.
- NFR-3: Scalability — support horizontal scaling for web and API layers.
- NFR-4: Security — data encrypted in transit and at rest; enforce least privilege; protect PII.
- NFR-5: Retention — audit logs retained for configurable periods (default 1 year) for compliance.

Integrations
------------
- ServiceDesk (primary): integrate with ServiceNow as the first-class ticketing/service-desk system. Implement two-way sync for ticket status, comments, attachments and cross-references; portal tickets become linked records in ServiceNow and vice-versa.
- CMDB (authoritative): ServiceNow CMDB is authoritative for assets and configuration items. The portal treats CMDB as the source of truth and reconciles local asset records against CMDB during sync.
- Identity provider (SAML/OIDC / Azure AD): use Azure AD groups for SSO and map groups to portal RBAC roles.
- Source control & CI/CD (GitHub/GitLab, Azure DevOps, Jenkins): link commits, PRs, build IDs and pipeline runs to change requests; allow guarded triggers from the portal where policy permits.
- Monitoring/Alerting (App Insights, Prometheus): surface alerts, link incidents to alert sources and provide runbook context.
- ChatOps (Teams/Slack): in-portal notifications and optional ChatOps actions; ChatOps actions that perform changes must be gated by RBAC and explicit approval flows.

Data & Privacy
--------------
- Minimize collection of personal data. When collected, mark PII fields explicitly and restrict visibility.
- Ensure role-based controls on access to sensitive configuration and secrets; do not store secrets in plain text.
- Test Data Policy (configurable): non-prod environments (`dev`, `qa`, `stg`) must use masked or synthetic test data by default. The masking rules, retention and allowed exception processes are configurable and must be documented in `engineering-readiness`.

Acceptance Criteria
-------------------
- Core workflows (request intake → approval → fulfillment) implemented and demonstrated end-to-end with ServiceNow integration.
- CI/CD linking surfaces build and deployment status and artifacts for supported pipeline providers (GitHub Actions or Azure DevOps) and is visible in change requests.
- RBAC enforcement validated: role-based UI views, API access control tests, and administrative role-change approvals produce audit records.
- AI assistant operates in `dev`/`qa` scopes initially; assistant-triggered actions are auditable and respect RBAC and approval rules.
- Audit trail exports for a sample period are produced and readable.

Success Metrics
---------------
- Mean Time To Acknowledge (MTTA): reduce by 30% within 3 months of launch (baseline measured at launch).
- Automation Coverage: 60% of routine request types handled end-to-end without manual intervention by launch.
- Approval Cycle Time: median approval time for standard changes under 4 hours.
- SLA Compliance: 95% of high-priority incidents acknowledged within defined SLA windows.
- Deployment Success Rate: 98% automated deployment success rate in `dev` and `qa`.

Delivery Increments (Suggested)
--------------------------------
1. MVP: Authentication, request intake, approvals, basic dashboard, audit logs, CMDB sync (read-only), simple reporting.
2. Iteration: Incident/change linking, runbook attachments, CI/CD link, notifications.
3. Iteration: Automated provisioning, two-way CMDB sync, advanced dashboards, performance tuning.

Open Questions / Decisions
-------------------------
- Which ticketing system(s) must be integrated in the initial release?
- Source of truth for assets: is the CMDB authoritative or should the portal own certain asset types?
- Approval policy definitions — where are organizational policies defined (portal vs external policy engine)?

Next Steps
----------
1. Review this BRS and confirm stakeholders and integrations.
2. Identify the initial ticketing and CI/CD providers to integrate for MVP.
3. Break MVP into epics and acceptance criteria and wire to planning workspace.

Environments & Access (Developer / QA Guidance)
-----------------------------------------------
Environments
- Development (`dev`): for active feature work and developer testing. Accessible to engineers and CI service accounts.
- Integration / QA (`qa`): for QA test runs, integration tests, and pre-staging validation.
- Staging (`stg`): production-like environment for release verification and rehearsals.
- Production (`prod`): customer-facing; controlled access and strict change windows.

Environment Access
- Azure Subscriptions / Resource Groups: each environment maps to an Azure subscription or resource group per org policy.
- Access Methods: developers and QA access via corporate SSO (SAML/OIDC) and are assigned Azure RBAC roles (Reader/Contributor/Owner as appropriate).
- Service Accounts & CI: CI/CD systems use service principals or managed identities stored and rotated in Key Vault.
- Network Access: access to non-prod may be allowed from corporate network or VPN only; production may restrict to approved IP ranges.

Developer & QA Workflows
------------------------
- Dev workflow: branch → CI build → deploy to `dev` automatically → developer tests → create PR.
- QA workflow: merge to integration branch → deploy to `qa` for regression and integration tests; link test runs to change/PR.
- Staging/Release: after QA sign-off, create change request and schedule deployment to `stg` for final validation.
- Test Data & Secrets: use masked or synthetic test data in non-prod. Secrets are retrieved at runtime from Key Vault; do not store secrets in repo.

AI Assistant (In-Portal Chat) Integration
----------------------------------------
Purpose
- Provide an integrated AI-driven assistant to help developers, QA, and operators find information, runbooks, troubleshooting steps, and answer common portal questions.

Capabilities
- Context-aware answers: use the initiative's docs, runbooks, CMDB metadata, and change history as knowledge sources.
- Quick actions: where authorized, allow the assistant to open tickets, surface runbooks, or link to CI/CD build details (actions gated by RBAC).
- Conversation history: retain short-term session context; redact or avoid exposing secrets.

Privacy & Safety
- PII and secrets: exclude secrets and sensitive PII from the assistant knowledge base. If an answer would expose sensitive data, provide a safe fallback pointing to guarded resources.
- Auditability: log assistant-triggered actions and who authorized them.

Integration Options
- Hosted LLM service (e.g., Azure OpenAI) or internal embeddings/search over indexed docs.
- Use vector embeddings of `openspec`, `planning`, `runbooks`, and `CMDB` fields for retrieval-augmented generation (RAG).
- Provide an explicit scope selector so users limit the assistant to specific namespaces (dev/qa/stg/prod read-only).

RBAC Administration & Governance
--------------------------------
- Admin Role: Portal `Admin` can manage role assignments and editable area permissions through a UI; changes are captured in audit logs.
- Delegated Administrators: allow scoped delegation (e.g., `EnvironmentAdmin` for `qa` & `stg`).
- Editable Areas: administrators can enable editing for sections such as `planning`, `runbooks`, and `quality-gates`.
- Approval for Role Changes: sensitive role assignments (e.g., Owner, ProductionContributor) require multi-step approval and produce an audit record.

Azure Environment Considerations
--------------------------------
- Subscriptions & Resource Groups: document the subscription IDs and resource group mapping for `dev`, `qa`, `stg`, and `prod` in `engineering-readiness`.
- Naming Conventions: follow the org naming standard for resources, e.g., `rg-itportal-<env>-<region>`.
- Identity: use Azure AD for SSO and group-to-role mappings; map Azure AD groups to portal RBAC roles.
- Secrets & Keys: store secrets in Azure Key Vault; grant the portal access via managed identity.
- Monitoring & Observability: wire App Insights / Log Analytics per environment; expose links in the portal dashboards.

Updated Acceptance Criteria (adds Dev/QA and AI assistant)
---------------------------------------------------------
- Environment documentation exists for `dev`, `qa`, `stg`, and `prod` including subscription/resource-group IDs and access procedures.
- CI/CD linking surfaces build/deploy status and artifacts for `dev` and `qa` at minimum.
- AI assistant answers documentation and runbook queries in `dev` and `qa` scopes and logs actions; no secrets are exposed.
- Admins can manage RBAC assignments via the portal UI and role changes produce auditable events.

Next Steps (revised)
--------------------
1. Confirm Azure subscription and resource-group mappings and capture them in `engineering-readiness`.
2. Decide which LLM provider or embedding store to use for the AI assistant and define data sources for RAG.
3. Define role-change approval flow and identify delegated administrators.

Files
-----
- Save this document as `input/brs.md` inside the initiative workspace.

