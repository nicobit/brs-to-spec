# Architecture — I004 IT Portal

Overview
--------
This document is a concise, delivery-oriented architecture draft for the IT Portal described in `input/brs.md`.
It focuses on the minimal, well-governed set of components and integration points needed for the MVP and the following iterations.

Goals
-----
- Provide a secure, highly-available web portal with clear separation between UI, API, business services and integration adapters.
- Enforce RBAC and auditability for all sensitive actions and role changes.
- Keep CMDB authoritative while enabling read/write patterns where approved.
- Support safe, auditable assistant actions (RAG + guarded actions) for non-prod scopes first.

High-level components
---------------------
1. Web Client (SPA)
   - Role-specific UI surfaces for `ServiceDesk`, `ITOperator`, `PlatformEngineer`, `ITManager`, `Admin`.
   - Static hosting (Azure Static Web Apps / CDN) and client-side auth via Azure AD / OIDC.

2. API Gateway / BFF
   - Central ingress for all client traffic, handles authentication, request routing, throttling and basic input validation.
   - Terminates TLS, enforces token validation and maps Azure AD groups to portal roles.

3. Backend Microservices (domain services)
   - Request Service: CRUD for requests, templates, approval state machine.
   - Incident Service: incident lifecycle, severity, links to requests/assets/change records.
   - Change Service: change requests, scheduling, approval workflow and links to pipelines.
   - Asset Sync Adapter: connector service that reconciles data from ServiceNow CMDB into portal domain model (read-first for MVP).
   - Runbook Service: stores runbook metadata and execution hooks; integrates with automation runners.
   - Notifications Service: sends email/Teams/Slack and in-portal notifications; supports templates and escalation rules.

4. Integration Adapters
   - CMDB Connector (ServiceNow): periodic reconciliation, webhooks for on-change sync.
   - Ticketing Adapter (ServiceNow primary): two-way sync for ticket status, comments, attachments.
   - CI/CD Connectors: GitHub/GitLab/Azure DevOps adapters that map commits/PRs/builds to change requests.
   - Monitoring Adapter: App Insights/Prometheus links for incidents and runbook context.

5. Data Stores
   - Primary DB: relational store for domain data (Azure SQL / PostgreSQL). Use schemas and audited writes.
   - Audit Store: append-only, immutable audit log (could be a separate table/partition or dedicated storage with write-once semantics).
   - Blob Storage: attachments, artifacts and exported reports (Azure Blob Storage).
   - Search/Vector Index: Azure Cognitive Search (and/or vector DB) for fast portal search and for RAG usage by the assistant.

6. Messaging & Async Processing
   - Event bus (Azure Service Bus / Event Grid): decouple integrations, handle retries and eventual consistency.
   - Background workers (Azure Functions / Kubernetes cron / worker pods): process syncs, reconciles, long-running jobs.

7. Observability & Security
   - Application Insights + Log Analytics for traces, metrics and diagnostics.
   - Centralized logging for audits and compliance exports.
   - Azure Key Vault for secrets; managed identity for service-to-service access.
   - Central policy enforcement: network rules, private endpoints, and conditional access.

Deployment topology
-------------------
- Environments: `dev`, `qa`, `stg`, `prod` mapped to subscription/resource groups (document exact IDs in `engineering-readiness`).
- App hosting options: pair App Service / Azure Static Web Apps for quick MVP, or AKS for full control and scaling later.
- Infrastructure as code: Bicep or Terraform modules for each environment; CI pipeline per environment with gated deployments.
- Networking: VNet for backend services, Application Gateway / WAF in front of API Gateway, private endpoints for DB & Key Vault.

Security model
--------------
- Identity: Azure AD for SSO; map groups to portal roles. Use group claims or Graph lookups for mapping.
- Authorization: enforce RBAC in API layer and re-check at service boundaries for high-risk actions.
- Approvals: approval chains captured as domain objects and produce audit records; emergency paths recorded with post-facto approvals.
- Data protection: encrypt data at rest and in transit; PII fields masked in non-prod environments.

Assistant (AI) integration
-------------------------
- Retrieval: index `openspec`, `planning`, `runbooks` and selected non-sensitive docs into the search/vector store.
- Action gating: assistant-triggered actions are permitted first in `dev`/`qa` with explicit approval workflows; all assistant actions are auditable.
- Secrets: never exposed in responses; any sensitive flow requires a human confirmation recorded in audit logs.

Scalability and resilience
-------------------------
- Design services to be stateless where possible; scale via additional instances behind load balancers.
- Use caching for dashboards and heavy read queries (Redis/Cache). Keep cache invalidation aligned with event bus messages.
- Circuit breakers and retry policies for external integrations (ServiceNow, CI/CD services).

Acceptance and readiness checks (MVP)
-----------------------------------
- SSO via Azure AD configured and RBAC mapping validated.
- Request intake end-to-end with approvals and audit trail demonstrated.
- CMDB sync (read-only) shows reconciled assets in portal UI.
- CI/CD linking surfaces commit/build status for at least one pipeline provider.
- Audit export for a sample period available and readable.

Diagrams and artifacts
----------------------
- Suggest creating two diagrams and saving them under `architecture/diagrams/`:
  - Conceptual component diagram (UI, API Gateway, services, integrations).
  - Deployment topology (VNets, subnets, app instances, DB, Key Vault, private endpoints).

Links
-----
- Component diagram (mermaid): [architecture/diagrams/component.mmd](initiatives/I004-it-portal/architecture/diagrams/component.mmd)
- Deployment diagram (mermaid): [architecture/diagrams/deployment.mmd](initiatives/I004-it-portal/architecture/diagrams/deployment.mmd)

Next steps
----------
1. Review this draft with `Product Owner` and `Platform/DevOps` to confirm which external systems (ServiceNow, GitHub, Azure DevOps) are in-scope for MVP.
2. Create `architecture/architecture-rules.md` to capture binding rules referenced by the delivery lead.
3. Produce simple diagrams under `architecture/diagrams/` and attach to this document.
