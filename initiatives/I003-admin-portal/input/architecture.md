---
Title: Draft Architecture
Status: DRAFT
Generated: 2026-06-09
Source: Generated from `input/brs.md` and Business Intake answers (PO: Nico)
---

## Overview

This draft architecture outlines a high-level solution for the Admin Portal described in the BRS. It is intentionally lightweight and marked DRAFT — an architect must validate and refine before it is treated as authoritative.

## Goals
- Provide a secure, scalable UI and API surface for environment inventory, RBAC management, diagnostics, and operational actions.
- Minimize blast radius by scoping actions through tenant/subscription mapping and least-privilege service principals.

## High-level components

- **Admin Portal (Web UI)** — React-based single-page application used by IT Operators and Platform Engineers. Authenticates via Azure AD.
- **API Backend** — REST API (stateless) that serves inventory, RBAC checks, action orchestration, and diagnostics links. Autoscaled behind an API gateway.
- **Action Orchestrator** — service responsible for executing operational actions (start/stop/reprovision). For MVP configured to run actions synchronously; supports enqueueing for long-running ops in future.
- **Inventory Store / Cache** — read-optimized store or cache holding consolidated inventory derived from Azure subscriptions and resource groups; backed by a database or cache layer for performance.
- **Audit Store** — append-only store for audit records (action, user, timestamp, resource) writable by API backend.
- **Telemetry / Observability** — Application Insights / Azure Monitor for logs, traces, and metrics; diagnostic links from UI to Log Analytics.
- **Notification Adapter** — integrates with Microsoft Teams (webhook) for MVP alerts.

## Integrations

- Azure Active Directory — authentication + group/role mapping for RBAC.
- Azure Subscriptions / Resource Groups — inventory source and action targets. (Placeholder mapping present in `input/input-package.md`; real subscription IDs required.)
- Azure Monitor / Log Analytics — diagnostics links and probe data.
- Microsoft Teams — alerting via webhooks for MVP.

## Security & Identity

- Use Azure AD for UI and API authentication (OAuth/OIDC). Map roles to Azure AD groups or app roles.
- Service Principal used by the Action Orchestrator with least-privilege scoped role assignments per subscription/resource group.
- All audit records are stored with immutable timestamps and tamper-evident storage where supported.

## Constraints & Assumptions

- Initial deployment targets Azure only.
- Tenant mapping follows "one subscription per tenant" pattern (placeholder entries exist; sample subscription IDs needed to validate scale and naming patterns).
- MVP executes operational actions synchronously; Action Orchestrator must return status immediately or error. Future work may add async job queue.

## Operational considerations

- For actions that may touch many resources, the implementation should guard with dry-run/preview and rate limiting.
- Use pagination and caching in Inventory Store to meet performance NFRs.

## Open architecture risks

- If tenant → subscription mapping varies (shared subscriptions), RBAC scoping complexity increases and may require a different data model.
- Synchronous action model may time out for long-running reprovision operations; consider async fallback.

## Next steps for architects

1. Validate tenant → subscription placeholder mapping and replace with sample IDs.
2. Review and approve DRAFT architecture, remove DRAFT notice once validated.
3. Provide guidance on the Action Orchestrator SSO/service principal provisioning and required least-privilege role set.
