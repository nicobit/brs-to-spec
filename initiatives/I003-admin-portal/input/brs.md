# Business Requirements Specification — Admin Portal

## Initiative

| Field | Value |
|---|---|
| Initiative ID | I003 |
| Slug | admin-portal |
| Title | Admin Portal — Environment & Tenant Management |
| Prepared date | 2026-06-09 |

## Owners

| Role | Name |
|---|---|
| Product | TBD |
| Engineering | Engineering |
| Security | TBD |

## Executive Summary

This initiative delivers an Admin Portal for the IT team to manage and operate cloud environments across tenants and stages (DEV, AIT, UAT, PROD...). The portal centralizes environment inventory, role-based access controls (RBAC), discovery and exploration by tenant and stage, operational actions (start/stop, provisioning hooks), diagnostics, and audit trails to reduce mean-time-to-diagnose and operational toil.

Primary consumers: IT operations, platform engineers, support engineers.

## Business Objectives

- Reduce time-to-diagnose environment issues by 50% within 3 months of launch.
- Provide a single-pane view of tenant and stage environments to improve situational awareness.
- Enforce centralized RBAC and auditability for all environment management actions.

## Scope (In-scope)

- Inventory and discovery of environments by tenant and by stage (DEV, AIT, UAT, PROD).
- Role-based access control (RBAC) integrated with Azure AD for permission management.
- Environment actions: view status, start/stop/restart, view logs/metrics links, trigger reprovision or configuration sync, and run diagnostics probes.
- Tenant context switching and filters (tenant selector, stage selector).
- Audit logging for all user actions and admin operations.
- Search and filter capabilities across environments, resources, and tags.
- Integration with Azure subscriptions and resource groups; read/write limited to permitted operations.

## Out of scope

- Full CI/CD pipeline orchestration (only action triggers and links to CI/CD). 
- Automated multi-cloud account provisioning beyond Azure (initially Azure-only). 

## Users and Personas

- IT Operator: daily environment checks, run diagnostics, and respond to incidents.
- Platform Engineer: configure provisioning hooks, manage RBAC roles and policies.
- Support Engineer: investigate incidents, escalate to platform/engineering.
- Auditor / Security Reviewer: review audit trails and access events.

## Key Features / Functional Requirements

FR-001: Environment Inventory — The portal lists all managed environments grouped by tenant and stage, showing health, availability, and last-updated time.

FR-002: Tenant & Stage Explorer — Allow users to filter and navigate environments by tenant and stage (DEV, AIT, UAT, PROD). Support free-text search and tag-based filtering.

FR-003: RBAC Management — Integrate with Azure AD to assign roles (Admin, Operator, ReadOnly) scoped to tenant and stage. Permission enforcement is required for UI and API.

FR-004: Operational Actions — Authorized users can perform environment-level actions: start, stop, restart, run diagnostics, trigger provisioning, and link to logs/metrics dashboards.

FR-005: Diagnostics & Links — Surface quick diagnostic probes (ping, health-check endpoint), recent errors, and one-click links to Azure Monitor/Log Analytics for deeper investigation.

FR-006: Audit & Change History — Record all admin actions with user identity, timestamp, action details, and affected resources. Provide exportable audit view.

FR-007: Integration APIs — Provide machine-readable API endpoints for inventory, actions, and RBAC queries to support automation and external tooling.

FR-008: Notifications & Alerts — Optional notifications for critical environment state changes (configurable via subscriptions). Integrate with existing alerting channels.

## Non-Functional Requirements

- NFR-001 Security: Use Azure AD for authentication and RBAC linkage. Enforce least-privilege and audit logging. All PII or sensitive data must be encrypted at rest and in transit.
- NFR-002 Availability: Portal UI should be available 99.9% monthly for Platform/IT users during business hours; APIs should be resilient with retry/backoff.
- NFR-003 Performance: Environment list must render within 2s for up to 2,000 environments.
- NFR-004 Observability: Emit telemetry events for actions, feature usage, errors, and latencies; integrate with Azure Monitor.
- NFR-005 Compliance: Capture sufficient audit trails to satisfy internal audit and security review requirements.

## Acceptance Criteria

- AC-001: Platform Engineer role can assign and revoke RBAC roles tied to tenant/stage, and permission checks are enforced for all operational actions.
- AC-002: IT Operator can filter by tenant and stage and perform start/stop operations when authorized; audit log contains the action and user.
- AC-003: Diagnostics probe returns health status and links to Azure Monitor logs within the portal.
- AC-004: APIs return inventory and action status with proper auth and role checks.

## Success Metrics

- Mean-time-to-diagnose (MTTD): reduce by 50% within 3 months.
- Admin action task completion time: average <= 30s for UI operations.
- RBAC compliance: 100% of environment modification actions tied to an auditable identity.

## Integrations

- Azure Active Directory — authentication and role mapping.
- Azure Subscriptions / Resource Groups — inventory and supported read/write actions.
- Azure Monitor / Log Analytics — links and diagnostics.
- Optional: ITSM (ServiceNow) integration for incident creation (as a follow-up).

## Constraints and Assumptions

- Initial implementation targets Azure-only environments.
- Tenant model assumes logical tenant identifiers map to one or more Azure subscriptions/resource groups.
- Tenant mapping: one Azure subscription per tenant (confirmed).
- Platform will provision a service principal with scoped permissions for actions; no hardcoded credentials.

## Risks

- Over-permissioning of service principal could lead to security exposure — mitigated by least-privilege and scoped roles.
- Large numbers of environments may need pagination and caching strategies to meet performance targets.

## Next Steps

1. Confirm initiative ID and owners to populate `input/input-package.md`.
2. Validate tenant mapping approach (how tenant identifiers map to subscriptions/resource groups).
3. Prioritize FRs for an MVP slice (inventory, tenant/stage exploration, RBAC, audit).
