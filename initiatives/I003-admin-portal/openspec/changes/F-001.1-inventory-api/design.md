# Design — F-001.1 Inventory API (backend)

What this story touches:
- API Backend: `GET /inventory` endpoint and pagination logic.
- Inventory Store: read-optimized cache or DB table with tenantId, subscriptionId, resourceId, resourceType, lastUpdated.

API surface:
- See `specs/api.md`.

Data model:
- See `specs/data.md` (table: `inventory_items`).

Integration points:
- Azure Subscriptions API (read-only) for ingestion.

Architecture constraints:
- Must use Azure AD for authentication; requests must be validated for role/group membership per `architecture/architecture-rules.md`.

Security decisions:
- Read-only inventory endpoints must still enforce authorization checks; only authorized roles can view inventory for a tenant.

Observability:
- Emit `actions.request.count`, `actions.request.duration` metrics for inventory queries and include trace ids.
- See `specs/observability.md`.

Open questions:
- Which pagination defaults should be used (pageSize default)?
