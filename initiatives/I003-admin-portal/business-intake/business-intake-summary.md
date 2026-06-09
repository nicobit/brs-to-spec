---
Title: Business Intake Summary (scaffold)
Date: 2026-06-09
Status: Draft
Source: Generated scaffold by Copilot
---

## Initiative Summary
- Short description: Admin Portal for IT to manage and operate cloud environments across tenants and stages (DEV, AIT, UAT, PROD). Centralizes inventory, RBAC, operational actions, diagnostics, and audit trails.

## Primary stakeholders
- Product Owner: Nico
- Business SME(s): IT Operator, Support Engineer
- Technical lead/architect: Engineering

## Users and Personas
- IT Operator: daily environment checks, run diagnostics, respond to incidents.
- Platform Engineer: configure provisioning hooks, manage RBAC roles and policies.
- Support Engineer: investigate incidents, escalate to platform/engineering.
- Auditor / Security Reviewer: review audit trails and access events.

## Key clarifications and answers
Q1: Product Owner confirmed — Nico.
Q2: Tenant mapping: placeholder entry created; please provide sample subscription IDs to replace placeholder.
Q3: Alerting channels for MVP: Microsoft Teams (confirmed).
Q4: Operational actions execution: Synchronous for MVP (confirmed).

## Decisions to capture
D-001: Tenant mapping approach approved (one subscription per tenant confirmed in BRS but needs verification for edge cases).
D-002: MVP scope prioritized (proposed: inventory, tenant/stage exploration, RBAC, audit).
D-003: Product Owner assigned to Nico (2026-06-09).
D-004: Alerting channel for MVP set to Microsoft Teams (2026-06-09).
D-005: Operational actions execution model for MVP set to Sync (2026-06-09).

## Acceptance / Success criteria
AC-001: Platform Engineer role can assign and revoke RBAC roles scoped to tenant/stage; permission checks enforced for UI and API.
AC-002: IT Operator can filter by tenant and stage and perform start/stop operations when authorized; audit log records action and user.
AC-003: Diagnostics probes surface health status and link to Azure Monitor/Log Analytics.
AC-004: APIs return inventory and action status with proper auth and role checks.

## Success Metrics
- MTTD: reduce mean-time-to-diagnose by 50% within 3 months of launch.
- Admin UI action latency: average <= 30s for UI operations.
- RBAC compliance: 100% of environment modification actions tied to auditable identities.

## Risks and constraints
- Risk: Over-permissioning of the service principal — mitigate via least-privilege and scoped roles.
- Risk: Large environment volumes may require pagination/caching to meet performance NFRs.
- Constraint: Azure-only initial target; multi-cloud out of scope for MVP.

## Attachments / referenced inputs
- `input/brs.md`

## Integrations
- Azure Active Directory — authentication and role mapping.
- Azure Subscriptions / Resource Groups — inventory and supported read/write actions.
- Azure Monitor / Log Analytics — diagnostics links.
- Optional: ServiceNow / ITSM for incident creation (follow-up).

## Notes for next stage
- After filling this summary, run the delivery-structure generation and architecture review steps.
Next step: generate `planning/delivery-structure.md` (prioritise MVP FRs) and run the architecture review to validate tenant mapping and RBAC model.
