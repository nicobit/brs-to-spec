# Initiative Context — I003 Admin Portal

**Metadata**

| Field | Value |
|---|---|
| Initiative | I003-admin-portal |
| Prepared by | Copilot (draft) |
| Date | 2026-06-09 |

## Purpose
Provide concise, engineering-focused context required to prepare handoff and implementation. This document summarizes affected components, compatibility constraints, operational dependencies, and contract surfaces that implementation and SRE teams must consume.

## Primary Consumers
- Delivery engineers
- Platform/Ops
- Security
- QA

## Summary
I003 Admin Portal implements an Azure-only admin UI and API for inventory, RBAC management, diagnostics, audit, and operational actions across tenant→subscription scoped environments. The MVP uses a one-to-one tenant→subscription mapping, a hybrid action orchestrator (sync for short ops, async job queue for long ops), and a custom `AdminPortalActionRunner` service principal per subscription (see planning/open-decisions.md).

## Affected Components
- UI: Admin Portal frontend components (tenant/stage selector, inventory, actions, audit view)
- API: Inventory ingestion, action endpoints, RBAC APIs, audit write/read
- Data stores: Inventory cache, append-only audit store
- Platform integrations: Azure AD (groups/app-roles), Log Analytics / Application Insights, Key Vault

## Compatibility & Regression Risks
- Tenant→subscription mapping changes may require data model migration and RBAC re-scoping.
- Action orchestration synchronous paths risk timeouts for large operations — must use async fallback for reprovision/restart flows.
- Service principal provisioning approach may require subscription-scoped automation and runbook updates.

## Contract & Schema Impact
- API: Add `actions/{actionId}/run` async status pattern (`202 Accepted` + `job_id`) and a `jobs/{jobId}` status endpoint. Document in `quality-gates/api-contract.md` and OpenAPI draft.
- Data: Inventory export CSV schema and audit event schema must be included in the traceability matrix.

## Operational Dependencies
- Platform/Ops to provide IaC snippet for `AdminPortalActionRunner` role and a sample subscription set for validation.
- Security to run threat-model on operational actions and confirm mitigations for high-risk flows.
- Product to provide representative subscription IDs and tenancy mapping examples for validation.

## Required Before Handoff
- Representative subscription samples (Product)
- Draft custom role JSON + IaC snippet (Ops)
- OpenAPI async pattern draft (Architect)
- Threat-model mitigations captured and agreed (Security)

## Links
- Open decisions: [planning/open-decisions.md](planning/open-decisions.md)
- Architecture review: [architecture/architecture-review.md](architecture/architecture-review.md)
- Delivery structure: [planning/delivery-structure.md](planning/delivery-structure.md)

---

Generated to satisfy the engineering-readiness artifact requirement for handoff.
