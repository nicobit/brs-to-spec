> **DRAFT — AI-proposed architecture. Not reviewed or approved.**
> This draft was generated from BRS content because no architecture input was provided.
> It must be reviewed and corrected by a qualified architect before the framework treats it as authoritative.
> Mark this notice as REVIEWED when an architect has validated or updated this document.

# Architecture

## Source Metadata

| Field | Value |
|---|---|
| Source name | Draft — derived from BRS |
| Source version / date | 2026-06-11 |
| Draft generated date | 2026-06-11 |
| Draft generated from | `input/brs.md` |
| Architect review status | Pending |
| Architect reviewer | |
| Architect review date | |

## Architecture Summary

This draft proposes a standalone IT Portal that integrates with ServiceNow (ticketing & CMDB), Azure AD for SSO and RBAC, one CI/CD provider for linking builds (GitHub Actions or Azure DevOps), and monitoring (App Insights / Prometheus). The portal is a web-based frontend plus API/backend services, an append-only audit store, integrations adapter layer for external systems, and an operations runbook store. Security, auditability and PII minimization are treated as first-class concerns.

## System Context Diagram

```mermaid
C4Context
	title System Context — I004 IT Portal (DRAFT)

	Person(user_itops, "IT Operator", "Triages incidents, runs runbooks, views dashboards")
	Person(user_platform, "Platform Engineer", "Links builds, monitors pipelines")
	Person(user_service, "Service Desk Agent", "Creates and triages requests")

	System(itportal, "IT Portal", "Provides request intake, incident/change lifecycle, asset views, and dashboards")

	System_Ext(servicenow, "ServiceNow (Ticketing & CMDB)", "Authoritative ticketing and CMDB system (existing)")
	System_Ext(azuread, "Azure AD (IdP)", "Enterprise identity provider for SSO and group claims")
	System_Ext(ci, "CI/CD Provider", "GitHub Actions or Azure DevOps — pipeline status and hooks")
	System_Ext(monitoring, "Monitoring / App Insights / Prometheus", "Observability and alerts")

	Rel(user_itops, itportal, "Uses / manages", "Web UI")
	Rel(user_platform, itportal, "Uses / links builds", "Web UI / API")
	Rel(user_service, itportal, "Creates requests", "Web UI")

	Rel(itportal, servicenow, "Syncs tickets / CMDB / links records", "API / scheduled sync")
	Rel(itportal, azuread, "Authenticates users / maps groups to roles", "SAML / OIDC")
	Rel(itportal, ci, "Links commits/PRs/builds to change requests", "Webhooks / API")
	Rel(itportal, monitoring, "Emits telemetry / reads alerts", "API / SDK")
```

Open decisions: D-001 (Confirm primary CI/CD provider), D-002 (CMDB ownership for any portal-owned asset types), D-003 (Exact audit retention period and storage mechanism).

## Container Diagram

```mermaid
C4Container
	title Container View — I004 IT Portal (DRAFT)

	Person(user, "User")

	System_Boundary(itportal_sys, "IT Portal") {
		Container(frontend, "Web UI", "React (suggested)", "Role-based frontend for operators, platform and service desk")
		Container(api, "API / Backend", "Node.js / .NET (TBD)", "Handles business logic, integrations, auth checks, and orchestration")
		Container(integration, "Integration Adapter", "Serverless functions / microservice (TBD)", "Encapsulates connectors to ServiceNow, CI/CD, Monitoring")
		Container(audit, "Audit Store", "Append-only store (e.g. CosmosDB / Blob + immutability)", "Stores immutable audit records for approvals and actions")
		Container(db, "Domain Data Store", "Relational DB (TBD)", "Persists portal domain models: requests, assets, change records")
		Container(runbooks, "Runbook Store", "Document store (TBD)", "Stores runbooks and playbooks referenced by incidents/changes")
		Container(queue, "Background Queue", "Queue service (TBD)", "Handles asynchronous jobs and webhooks")
	}

	System_Ext(servicenow, "ServiceNow (Ticketing & CMDB)")
	System_Ext(azuread, "Azure AD")
	System_Ext(ci, "CI/CD Provider")
	System_Ext(monitoring, "Monitoring / App Insights / Prometheus")

	Rel(user, frontend, "Uses")
	Rel(frontend, api, "Calls", "HTTPS")
	Rel(api, db, "Reads/Writes")
	Rel(api, audit, "Writes audit events")
	Rel(api, integration, "Calls for external syncs", "HTTPS / SDK / Webhook")
	Rel(integration, servicenow, "Syncs tickets & CMDB", "API / scheduled sync")
	Rel(integration, ci, "Watches build status / triggers", "Webhooks / API")
	Rel(api, monitoring, "Emits telemetry / reads alerts", "App Insights SDK / API")
	Rel(api, queue, "Enqueues background jobs")
```

Note: Technology choices (frontend framework, backend runtime, DB technology) are open decisions.

## Integration Flow Diagram

```mermaid
sequenceDiagram
	actor User
	participant Frontend
	participant API
	participant Integration
	participant ServiceNow

	User->>Frontend: Submit request
	Frontend->>API: POST /requests
	API->>Integration: Create ticket / sync
	Integration->>ServiceNow: Create Ticket (API)
	ServiceNow-->>Integration: Ticket created
	Integration-->>API: Ticket ID
	API-->>Frontend: 201 Created (request + ticket link)
```

This sequence shows the happy path for request intake and ticket creation. Async syncs and reconciliation are handled via the Integration Adapter and background queue.

## Proposed System Context

| System / Service | Role | New or existing | Shown in diagram | Notes |
|---|---|---|---|---|
| IT Portal | Core application providing intake, lifecycle management, dashboards | New | Yes | Integrates with ServiceNow and Azure AD |
| ServiceNow | Ticketing & CMDB | Existing | Yes | Source-of-truth for tickets and CMDB (per BRS assumption) |
| Azure AD | Identity provider | Existing | Yes | Used for SSO and group claims mapping |
| CI/CD Provider | Build and pipeline provider | Existing | Yes | Provider to be confirmed (D-001) |
| Monitoring | Observability & alerts | Existing | Yes | App Insights / Prometheus per BRS |

## Proposed Integrations

| Integration | Direction | Protocol / mechanism implied | Sensitivity | Open decision |
|---|---|---|---|---|
| ServiceNow CMDB / Ticketing | Bi-directional (sync & links) | REST API, scheduled sync, webhooks | High (PII, audit) | D-002 |
| Azure AD | Inbound auth | SAML / OIDC | High (auth) | - |
| CI/CD provider | Inbound status / webhook | Webhooks, API | Medium | D-001 |
| Monitoring | Outbound telemetry / alerts | SDK / API | Medium | - |

## Implied Constraints

| Constraint ID | Constraint | Source requirement | Confidence | Requires architect confirmation? |
|---|---|---|---|---|
| C-001 | Audit trail must be append-only and exportable | FR-10, NFR-5 | High | Yes (storage choice and retention) |
| C-002 | Data masking in non-prod environments | Data & Privacy | High | Yes (masking rules) |
| C-003 | SSO via Azure AD | FR-1 | High | No |

## Implied Governed Boundaries

| Boundary | Type | Implied by | Shown in diagram | Contract likely needed? |
|---|---|---|---|---|
| Portal ↔ ServiceNow | API / Data boundary | Ticketing & CMDB sync | Yes | Yes |
| Portal ↔ CI/CD | Event / webhook boundary | Build linking and triggers | Yes | Yes |
| Portal internal audit store | Data boundary | Audit & compliance | Yes | Possibly |

## Non-Functional Requirements Summary

| NFR ID | Requirement | Architecture implication |
|---|---|---|
| NFR-1 | 99.9% availability | Deploy across availability zones; design for failover |
| NFR-2 | Page load / query performance | Caching, indexed queries, pagination, backend scaling |
| NFR-4 | Data encryption and least privilege | Use Key Vault for secrets; RBAC checks at API layer |

## Open Decisions

| Decision ID | Decision needed | Why it matters | Owner |
|---|---|---|---|
| D-001 | Confirm primary CI/CD provider (GitHub Actions or Azure DevOps) | Affects webhook integration, connectors, and example implementation | Product Owner / Platform |
| D-002 | Confirm whether the portal will own any asset types vs ServiceNow being authoritative | Affects data contracts and sync strategy | Product Owner / Platform |
| D-003 | Audit retention policy and storage choice | Affects cost, compliance and implementation approach | Security / Compliance |

## Assumptions Made in This Draft

| Assumption | Basis | Risk if wrong |
|---|---|---|
| ServiceNow is the primary ticketing and CMDB provider | Stated in BRS and business-intake | High — integration design would change if different |
| Azure AD will be used for SSO and group mapping | Stated in BRS and business-intake | Medium — alternative IdP will require connector changes |
| One CI/CD provider will be chosen for MVP | Delivery-structure and BRS suggest single provider | Medium — multi-provider support increases scope |

## Architect Review Notes

*(Leave blank for architect to complete.)*

