# Delivery Structure — I004 IT Portal

Overview
--------
This document breaks the suggested MVP epics into features and example user stories suitable for planning and handoff to engineering.

Epic: Authentication & Role Mapping
----------------------------------
Features
- Azure AD SSO integration
- Group-to-role mapping and admin UI

Sample stories
- As a `ServiceDesk` user, I can sign in via Azure AD so I can access the portal.
  - AC: SSO succeeds for test user; group claims map to portal role.
- As an `Admin`, I can map Azure AD groups to portal roles via the admin UI.
  - AC: Mapping saved and applied to user sessions; changes produce an audit record.

Epic: Request Intake & Approval Workflow
----------------------------------------
Features
- Request templates and custom fields
- Approval chain engine and conditional approvals
- Request UI: create/edit/comment/track

Sample stories
- As a `ServiceDesk` agent, I can create a hardware request from a template.
  - AC: Request persisted, approval chain created when required.
- As an `ITOperator`, I can approve a request and trigger fulfillment actions.
  - AC: Approval recorded in audit log; request status transitions accordingly.

Epic: CMDB Read Sync & Asset Views
----------------------------------
Features
- ServiceNow CMDB connector (read-only for MVP)
- Asset reconciliation and basic CI relationship views

Sample stories
- As a `PlatformEngineer`, I can view asset details reconciled from CMDB.
  - AC: Asset data displays and reconciles against last sync snapshot.

Epic: CI/CD Linking
-------------------
Features
- Connector for a single pipeline provider (GitHub Actions or Azure DevOps)
- Link commits/PRs/builds to change requests; surface statuses

Sample stories
- As a `PlatformEngineer`, I can link a PR/build to a change request.
  - AC: Build status displayed in the change request and updated on webhook events.

Epic: Dashboards, Notifications & Audit Export
---------------------------------------------
Features
- Role-specific dashboards (incidents, pending approvals, deployments)
- Notification templates (email, Teams/Slack)
- Audit export and retention configuration

Sample stories
- As an `ITManager`, I can see pending approvals and SLA dashboards.
  - AC: Dashboard shows metrics and links to underlying requests/incidents.

Cross-cutting work
------------------
- Audit & Compliance: implement append-only audit store and export tooling.
- Observability: App Insights instrumentation and dashboards for services.
- Security: secrets in Key Vault and role-checked service access.
- Ops: IaC for environments and CI pipelines for infra and app deployment.

Initial slicing (Sprint 0 / Spike work)
-------------------------------------
1. Spike: Validate Azure AD SSO and group claim mapping (deliverable: SSO PoC).
2. Spike: Validate ServiceNow read-only sync (deliverable: connector prototype).
3. Create prototypical request intake UI and API (deliverable: minimal CRUD + approval state machine).

Acceptance criteria mapping
---------------------------
- Map each story to the BRS acceptance criteria and add SCN- IDs when QA creates BDD scenarios.

Next actions
------------
1. Review and confirm which pipeline provider to support for the initial CI/CD linking story.
2. Assign owners: propose `Delivery Lead` owns epics and `Platform/DevOps` own infra spikes.
3. Create `planning/delivery-increments.md` to define increments and sprint boundaries.
